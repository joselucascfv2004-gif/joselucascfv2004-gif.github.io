#!/usr/bin/env python3
"""Preço justo por três métodos conhecidos, a partir do JSON do dados.py.

- Graham: raiz(22,5 x LPA x VPA). Só faz sentido com lucro e patrimônio positivos.
- Bazin (preço teto): média dos dividendos por ação dos últimos anos completos / DY mínimo.
  O padrão é 6% (o original); com a Selic alta, compare também com --dy-min maior.
- Fluxo de caixa descontado (FCD) simples: fluxo de caixa livre crescendo --g1 ao ano por
  --anos anos, perpetuidade a --gp, descontado a --taxa; tira a dívida líquida e divide pelas
  ações. Inclui tabela de sensibilidade 5x5 (taxa x crescimento na perpetuidade), centro = caso base.

Não use FCD nem Graham para bancos, seguradoras e fundos imobiliários (use P/VP, ROE e DY).
Uso: python3 valuation.py /tmp/PETR4_SA_2026-10-31.json [--taxa 16] [--g1 4] [--gp 3] [--dy-min 6]
"""
import argparse
import json
import math


def fmt(x, casas=2):
    if x is None:
        return "–"
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fcd(fcl, g1, gp, taxa, anos, divida_liq, acoes):
    if taxa <= gp:
        return None
    vp, f = 0.0, fcl
    for t in range(1, anos + 1):
        f *= 1 + g1
        vp += f / (1 + taxa) ** t
    perp = f * (1 + gp) / (taxa - gp) / (1 + taxa) ** anos
    return (vp + perp - divida_liq) / acoes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--taxa", type=float, help="taxa de desconto %% a.a. (padrão: CDI + 5)")
    ap.add_argument("--g1", type=float, default=4.0, help="crescimento do fluxo de caixa nos primeiros anos, %%")
    ap.add_argument("--gp", type=float, default=3.0, help="crescimento na perpetuidade, %% (perto da inflação de longo prazo)")
    ap.add_argument("--anos", type=int, default=5)
    ap.add_argument("--dy-min", type=float, default=6.0, help="DY mínimo do Bazin, %%")
    ap.add_argument("--anos-bazin", type=int, default=5)
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    f, preco = d["fundamentos_hoje"], d["preco"]["ultimo"]
    setor = (d.get("setor") or "") + " " + (d.get("industria") or "")
    nao_fcd = any(k in setor for k in ("Bank", "Insurance", "REIT", "Financial Services", "Capital Markets"))
    out = [f"# Preço justo — {d['ticker']} (preço {fmt(preco)} em {d['preco']['data']})", ""]
    if d.get("ponto_no_tempo"):
        out.append("> Atenção: análise com data no passado. LPA, VPA, fluxo de caixa e dívida abaixo são os de HOJE "
                   "(o Yahoo não guarda o histórico deles); o resultado serve só como referência.\n")

    # Graham
    lpa, vpa = f.get("lpa"), f.get("vpa")
    if nao_fcd and "REIT" in setor:
        out.append("**Graham:** não se aplica a fundos imobiliários.")
    elif lpa and vpa and lpa > 0 and vpa > 0:
        g = math.sqrt(22.5 * lpa * vpa)
        out.append(f"**Graham:** {fmt(g)} (LPA {fmt(lpa, 4)}, VPA {fmt(vpa, 4)}) → {fmt((g / preco - 1) * 100, 1)}% em relação ao preço.")
    else:
        out.append("**Graham:** sem LPA e VPA positivos, não se aplica.")

    # Bazin
    ano_ref = int(d["data_analise"][:4])
    por_ano = {int(k): v for k, v in d["dividendos"]["por_ano"].items()}
    anos = list(range(ano_ref - a.anos_bazin, ano_ref))  # anos completos seguidos, antes do ano da análise
    sem = [y for y in anos if not por_ano.get(y)]
    if any(por_ano.get(y) for y in anos):
        media = sum(por_ano.get(y) or 0 for y in anos) / len(anos)
        linhas = []
        for dy in sorted({a.dy_min, 8.0, 10.0}):
            teto = media / (dy / 100)
            linhas.append(f"DY mínimo {fmt(dy, 0)}% → teto {fmt(teto)} ({fmt((teto / preco - 1) * 100, 1)}%)")
        out.append(f"**Bazin:** média de dividendos de {anos[0]} a {anos[-1]} = {fmt(media, 4)} por ação. " + "; ".join(linhas) + ".")
        if sem:
            out.append(f"  Anos sem dividendo registrado no Yahoo: {', '.join(map(str, sem))} (contados como zero). "
                       "Confira no site de RI ou na B3 se é falta de dado.")
        out.append("  Dividendo muito irregular (ano extraordinário) distorce o Bazin: olhe a lista por ano antes de confiar.")
    else:
        out.append("**Bazin:** sem histórico de dividendos.")

    # FCD
    fcl, acoes = f.get("fluxo_caixa_livre"), f.get("acoes")
    divida_liq = (f.get("divida_total") or 0) - (f.get("caixa_total") or 0)
    cdi = (d["macro_brasil"].get("CDI (% a.a.)") or {}).get("valor")
    taxa = a.taxa if a.taxa else ((cdi or 11.0) + 5.0)
    if nao_fcd:
        out.append(f"**Fluxo de caixa descontado:** não se aplica a este setor ({setor.strip()}). Use P/VP, ROE e DY.")
    elif not fcl or not acoes or fcl <= 0:
        out.append("**Fluxo de caixa descontado:** fluxo de caixa livre ausente ou negativo; não dá para calcular com segurança.")
    else:
        base = fcd(fcl, a.g1 / 100, a.gp / 100, taxa / 100, a.anos, divida_liq, acoes)
        out.append(f"**Fluxo de caixa descontado:** {fmt(base)} por ação ({fmt((base / preco - 1) * 100, 1)}%). "
                   f"Premissas: FCL {fmt(fcl / 1e9, 1)} bi, cresce {fmt(a.g1, 1)}% a.a. por {a.anos} anos, perpetuidade {fmt(a.gp, 1)}%, "
                   f"taxa {fmt(taxa, 1)}% a.a. ({'CDI ' + fmt(cdi, 2) + '% + 5' if not a.taxa else 'informada'}), "
                   f"dívida líquida {fmt(divida_liq / 1e9, 1)} bi, {fmt(acoes / 1e6, 0)} mi de ações.")
        taxas = [taxa - 2, taxa - 1, taxa, taxa + 1, taxa + 2]
        gps = [a.gp - 1, a.gp - 0.5, a.gp, a.gp + 0.5, a.gp + 1]
        out += ["", "Sensibilidade (linhas = taxa de desconto, colunas = crescimento na perpetuidade; centro = caso base):", "",
                "| taxa \\ g | " + " | ".join(f"{fmt(g, 1)}%" for g in gps) + " |",
                "|---|" + "---|" * len(gps)]
        for t in taxas:
            cel = [fcd(fcl, a.g1 / 100, g / 100, t / 100, a.anos, divida_liq, acoes) for g in gps]
            out.append(f"| {fmt(t, 1)}% | " + " | ".join(fmt(c) if c is not None else "–" for c in cel) + " |")
        out.append("\nO FCD é muito sensível às premissas: trate como faixa, não como número exato.")
    print("\n".join(out))


if __name__ == "__main__":
    main()

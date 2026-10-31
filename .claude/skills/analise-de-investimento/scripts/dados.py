#!/usr/bin/env python3
"""Coleta gratuita dos dados de um ativo para a skill analise-de-investimento.

Fontes (todas gratuitas, sem chave): Yahoo Finanças (yfinance: cotações, indicadores,
balanços, dividendos; ações da B3 terminam em .SA) e Banco Central (API SGS: Selic, CDI,
IPCA, dólar). Nada aqui compra, vende ou se conecta a corretora.

Regra de "ponto no tempo": com --data, preços e séries só vão até essa data, para a
análise não usar o futuro. Os fundamentos do Yahoo são os de hoje; com --data no passado
o resumo avisa isso, e só entram demonstrativos com data de referência 45+ dias antes.

Uso:
  python3 dados.py PETR4.SA                     # hoje, 2 anos de preços
  python3 dados.py ITUB4.SA --data 2026-06-30   # como se fosse 30/06/2026
  python3 dados.py PETR4.SA --pares PRIO3.SA RECV3.SA --saida /tmp/petr4
Saída: <saida>.json (tudo) e <saida>.md (resumo para ler).
"""
import argparse
import datetime as dt
import json
import math
import sys

try:
    import pandas as pd
    import requests
    import yfinance as yf
except ImportError:
    sys.exit("Faltam bibliotecas: pip install -q yfinance pandas requests")

BCB = {  # código SGS -> nome
    432: "Selic meta (% a.a.)",
    4389: "CDI (% a.a.)",
    13522: "IPCA acumulado 12 meses (%)",
    1: "Dólar PTAX venda (R$)",
}


def num(x, casas=2):
    try:
        x = float(x)
        return None if math.isnan(x) or math.isinf(x) else round(x, casas)
    except (TypeError, ValueError):
        return None


def serie_bcb(codigo, ate):
    ini = (ate - dt.timedelta(days=400)).strftime("%d/%m/%Y")
    url = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
           f"?formato=json&dataInicial={ini}&dataFinal={ate.strftime('%d/%m/%Y')}")
    try:
        lst = requests.get(url, timeout=30).json()
        lst = [x for x in lst if dt.datetime.strptime(x["data"], "%d/%m/%Y").date() <= ate]
        if not lst:
            return None
        ult, ano = lst[-1], lst[0]
        return {"data": ult["data"], "valor": num(ult["valor"], 4), "ha_um_ano": num(ano["valor"], 4)}
    except Exception as e:  # sem internet ou série fora do ar: segue sem ela
        return {"erro": str(e)[:120]}


def indicadores(h):
    """Indicadores técnicos calculados à mão (sem bibliotecas pagas)."""
    c, alta, baixa = h["Close"], h["High"], h["Low"]
    out = {}
    out["sma50"] = c.rolling(50).mean().iloc[-1]
    out["sma200"] = c.rolling(200).mean().iloc[-1]
    out["ema10"] = c.ewm(span=10, adjust=False).mean().iloc[-1]
    d = c.diff()
    ganho = d.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    perda = (-d.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    out["rsi14"] = (100 - 100 / (1 + ganho / perda)).iloc[-1]
    macd = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    sinal = macd.ewm(span=9, adjust=False).mean()
    out["macd"], out["macd_sinal"], out["macd_hist"] = macd.iloc[-1], sinal.iloc[-1], (macd - sinal).iloc[-1]
    m20, dp20 = c.rolling(20).mean(), c.rolling(20).std()
    out["bollinger_sup"], out["bollinger_inf"] = (m20 + 2 * dp20).iloc[-1], (m20 - 2 * dp20).iloc[-1]
    tr = pd.concat([alta - baixa, (alta - c.shift()).abs(), (baixa - c.shift()).abs()], axis=1).max(axis=1)
    out["atr14"] = tr.rolling(14).mean().iloc[-1]
    ret = c.pct_change().dropna()
    out["vol_anual_%"] = ret.tail(252).std() * math.sqrt(252) * 100
    pico = c.cummax()
    out["queda_max_1a_%"] = ((c.tail(252) / pico.tail(252)) - 1).min() * 100
    return {k: num(v) for k, v in out.items()}


def retorno(c, dias):
    return num((c.iloc[-1] / c.iloc[-dias - 1] - 1) * 100) if len(c) > dias else None


def demonstrativo(df, ate, ponto_no_tempo):
    """DataFrame do yfinance (linhas = contas, colunas = datas) -> dict das 4 datas mais recentes."""
    if df is None or getattr(df, "empty", True):
        return {}
    cols = [c for c in df.columns if not ponto_no_tempo or c.date() <= ate - dt.timedelta(days=45)]
    cols = sorted(cols, reverse=True)[:4]
    contas = ["Total Revenue", "Gross Profit", "EBITDA", "EBIT", "Net Income", "Free Cash Flow",
              "Operating Cash Flow", "Capital Expenditure", "Total Debt", "Cash And Cash Equivalents",
              "Stockholders Equity", "Total Assets", "Net Debt", "Diluted EPS", "Basic EPS"]
    return {c.strftime("%Y-%m-%d"): {k: num(df.at[k, c], 0 if "EPS" not in k else 4)
                                     for k in contas if k in df.index} for c in cols}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--data", help="data da análise AAAA-MM-DD (padrão: hoje)")
    ap.add_argument("--anos", type=int, default=2)
    ap.add_argument("--pares", nargs="*", default=[], help="concorrentes para comparar")
    ap.add_argument("--indice", default=None, help="índice de referência (padrão ^BVSP para .SA)")
    ap.add_argument("--saida", default=None)
    a = ap.parse_args()

    hoje = dt.date.today()
    ate = dt.date.fromisoformat(a.data) if a.data else hoje
    ponto_no_tempo = ate < hoje
    tk = a.ticker.upper()
    indice = a.indice or ("^BVSP" if tk.endswith(".SA") else "^GSPC")
    ini = ate - dt.timedelta(days=365 * a.anos + 30)
    fim = ate + dt.timedelta(days=1)

    t = yf.Ticker(tk)
    h = t.history(start=ini.isoformat(), end=fim.isoformat(), auto_adjust=False)
    if h.empty:
        sys.exit(f"Sem cotações para {tk}. Confira o código (ações da B3 terminam em .SA, ex.: PETR4.SA).")
    h = h[h.index.date <= ate]
    c = h["Close"]
    info = {}
    try:
        info = t.info or {}
    except Exception:
        pass

    divs = t.dividends
    divs = divs[divs.index.date <= ate] if len(divs) else divs
    div_12m = float(divs[divs.index.date > ate - dt.timedelta(days=365)].sum()) if len(divs) else 0.0
    div_ano = {}
    if len(divs):
        for ano, v in divs.groupby(divs.index.year).sum().items():
            div_ano[int(ano)] = num(v, 4)

    ref = yf.Ticker(indice).history(start=ini.isoformat(), end=fim.isoformat())
    ref = ref[ref.index.date <= ate]["Close"] if not ref.empty else None

    pares = {}
    for p in a.pares:
        try:
            pt = yf.Ticker(p)
            pi = pt.info or {}
            ph = pt.history(start=(ate - dt.timedelta(days=400)).isoformat(), end=fim.isoformat())
            ph = ph[ph.index.date <= ate]["Close"]
            pares[p] = {"nome": pi.get("shortName"), "preco": num(ph.iloc[-1]) if len(ph) else None,
                        "retorno_12m_%": retorno(ph, 250) if len(ph) else None,
                        "p_l": num(pi.get("trailingPE")), "p_vp": num(pi.get("priceToBook")),
                        "dy_%": num(pi.get("dividendYield")), "roe_%": num((pi.get("returnOnEquity") or 0) * 100),
                        "margem_liq_%": num((pi.get("profitMargins") or 0) * 100),
                        "valor_mercado": pi.get("marketCap")}
        except Exception as e:
            pares[p] = {"erro": str(e)[:100]}

    preco = num(c.iloc[-1])
    out = {
        "ticker": tk, "nome": info.get("longName") or info.get("shortName"), "data_analise": ate.isoformat(),
        "ponto_no_tempo": ponto_no_tempo, "moeda": info.get("currency"), "setor": info.get("sector"),
        "industria": info.get("industry"), "descricao": (info.get("longBusinessSummary") or "")[:1200],
        "preco": {"ultimo": preco, "data": c.index[-1].strftime("%Y-%m-%d"),
                  "min_52s": num(c.tail(252).min()), "max_52s": num(c.tail(252).max()),
                  "volume_medio_21d": num(h["Volume"].tail(21).mean(), 0),
                  "retorno_%": {"1m": retorno(c, 21), "3m": retorno(c, 63), "6m": retorno(c, 126), "12m": retorno(c, 250)}},
        "indice": {"codigo": indice, "retorno_12m_%": retorno(ref, 250) if ref is not None and len(ref) else None},
        "tecnico": indicadores(h),
        "fundamentos_hoje": {
            "valor_mercado": info.get("marketCap"), "valor_firma": info.get("enterpriseValue"),
            "p_l": num(info.get("trailingPE")), "p_l_projetado": num(info.get("forwardPE")),
            "p_vp": num(info.get("priceToBook")), "ev_ebitda": num(info.get("enterpriseToEbitda")),
            "lpa": num(info.get("trailingEps"), 4), "vpa": num(info.get("bookValue"), 4),
            "roe_%": num((info.get("returnOnEquity") or 0) * 100), "margem_liq_%": num((info.get("profitMargins") or 0) * 100),
            "margem_ebitda_%": num((info.get("ebitdaMargins") or 0) * 100),
            "divida_total": info.get("totalDebt"), "caixa_total": info.get("totalCash"),
            "fluxo_caixa_livre": info.get("freeCashflow"), "acoes": info.get("sharesOutstanding"),
            "payout_%": num((info.get("payoutRatio") or 0) * 100), "beta": num(info.get("beta")),
            "preco_alvo_medio_analistas": num(info.get("targetMeanPrice")), "n_analistas": info.get("numberOfAnalystOpinions"),
            "recomendacao_media": info.get("recommendationKey"),
        },
        "dividendos": {"ultimos_12m_por_acao": num(div_12m, 4),
                       "dy_12m_%": num(div_12m / preco * 100) if preco else None, "por_ano": div_ano},
        "demonstrativos": {
            "anual_dre": demonstrativo(getattr(t, "financials", None), ate, ponto_no_tempo),
            "anual_balanco": demonstrativo(getattr(t, "balance_sheet", None), ate, ponto_no_tempo),
            "anual_caixa": demonstrativo(getattr(t, "cashflow", None), ate, ponto_no_tempo),
            "trimestral_dre": demonstrativo(getattr(t, "quarterly_financials", None), ate, ponto_no_tempo),
        },
        "macro_brasil": {nome: serie_bcb(cod, ate) for cod, nome in BCB.items()},
        "pares": pares,
        "fontes": ["Yahoo Finanças (biblioteca yfinance)", "Banco Central do Brasil, API SGS (séries 432, 4389, 13522, 1)"],
        "avisos": [],
    }
    if ponto_no_tempo:
        out["avisos"].append("Análise com data no passado: cotações, dividendos e macro vão só até a data; os indicadores "
                             "de 'fundamentos_hoje' e a opinião dos analistas são de HOJE e não devem pesar na decisão.")
    if not out["demonstrativos"]["anual_dre"]:
        out["avisos"].append("Sem demonstrativos no Yahoo: buscar na CVM (dados abertos DFP/ITR) ou no site de RI.")
    if len(c) < 200:
        out["avisos"].append("Menos de 200 pregões: média de 200 dias e retorno de 12 meses ficam incompletos.")

    saida = a.saida or f"/tmp/{tk.replace('^', '').replace('.', '_')}_{ate.isoformat()}"
    with open(saida + ".json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    with open(saida + ".md", "w", encoding="utf-8") as f:
        f.write(resumo(out))
    print(resumo(out))
    print(f"\n(arquivos: {saida}.json e {saida}.md)")


def resumo(o):
    f, p, t, m = o["fundamentos_hoje"], o["preco"], o["tecnico"], o["macro_brasil"]
    l = [f"# {o['ticker']} — {o['nome']} (dados até {o['data_analise']})", "",
         f"Setor: {o['setor']} / {o['industria']}",
         f"Preço: {p['ultimo']} {o['moeda']} em {p['data']} | 52 semanas: {p['min_52s']} a {p['max_52s']}",
         f"Retornos: 1m {p['retorno_%']['1m']}% | 3m {p['retorno_%']['3m']}% | 6m {p['retorno_%']['6m']}% | "
         f"12m {p['retorno_%']['12m']}% (índice {o['indice']['codigo']}: {o['indice']['retorno_12m_%']}%)", "",
         "## Técnico", ", ".join(f"{k}={v}" for k, v in t.items()), "",
         "## Fundamentos (fonte: Yahoo, valores de hoje)",
         ", ".join(f"{k}={v}" for k, v in f.items() if v not in (None, 0)), "",
         f"## Dividendos\nÚltimos 12 meses: {o['dividendos']['ultimos_12m_por_acao']} por ação "
         f"(DY {o['dividendos']['dy_12m_%']}%). Por ano: {o['dividendos']['por_ano']}", "",
         "## Macro Brasil (Banco Central)"]
    for k, v in m.items():
        l.append(f"- {k}: {v}")
    if o["pares"]:
        l += ["", "## Concorrentes"] + [f"- {k}: {v}" for k, v in o["pares"].items()]
    if o["avisos"]:
        l += ["", "## Avisos"] + [f"- {x}" for x in o["avisos"]]
    return "\n".join(l) + "\n"


if __name__ == "__main__":
    main()

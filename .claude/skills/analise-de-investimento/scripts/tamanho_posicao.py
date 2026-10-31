#!/usr/bin/env python3
"""Quantas ações comprar sem arriscar mais do que o combinado (gestão de risco).

Risco fixo: perda máxima aceita (padrão 1% da carteira) dividida pela distância entre a
entrada e o stop. O stop pode ser um preço (--stop) ou N vezes o ATR (--atr --mult, padrão 2).
Depois aplica o limite de concentração (padrão 10% da carteira num só ativo) e arredonda
para o lote (100 no lote padrão da B3, 1 no fracionário).

Uso: python3 tamanho_posicao.py --carteira 20000 --entrada 52.71 --stop 48
     python3 tamanho_posicao.py --carteira 20000 --entrada 52.71 --atr 1.92 --mult 2 --lote 1
"""
import argparse
import math


def br(x, c=2):
    return f"{x:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


ap = argparse.ArgumentParser()
ap.add_argument("--carteira", type=float, required=True, help="valor total investido, R$")
ap.add_argument("--entrada", type=float, required=True)
ap.add_argument("--stop", type=float)
ap.add_argument("--atr", type=float)
ap.add_argument("--mult", type=float, default=2.0)
ap.add_argument("--risco", type=float, default=1.0, help="perda máxima por operação, %% da carteira")
ap.add_argument("--max-posicao", type=float, default=10.0, help="máximo num só ativo, %% da carteira")
ap.add_argument("--lote", type=int, default=1, help="1 = fracionário, 100 = lote padrão")
a = ap.parse_args()

stop = a.stop if a.stop else (a.entrada - a.mult * a.atr if a.atr else None)
if not stop or stop >= a.entrada:
    raise SystemExit("Informe --stop abaixo da entrada, ou --atr (stop = entrada - mult x ATR).")
dist = a.entrada - stop
risco_rs = a.carteira * a.risco / 100
q_risco = risco_rs / dist
q_conc = a.carteira * a.max_posicao / 100 / a.entrada
q = math.floor(min(q_risco, q_conc) / a.lote) * a.lote
limite = "risco por operação" if q_risco <= q_conc else "limite de concentração"
if q == 0:
    limite = (f"um lote de {a.lote} ações custa R$ {br(a.lote * a.entrada)}, mais do que as regras permitem "
              f"(até {br(min(q_risco, q_conc), 1)} ações)")
print(f"Stop: {br(stop)} ({br(dist / a.entrada * 100, 1)}% abaixo da entrada)")
print(f"Quantidade: {q} ações = R$ {br(q * a.entrada)} ({br(q * a.entrada / a.carteira * 100, 1)}% da carteira)")
print(f"Se o stop for atingido, a perda é de R$ {br(q * dist)} ({br(q * dist / a.carteira * 100, 2)}% da carteira)")
print(f"O que limitou a quantidade: {limite}.")
if q == 0:
    print("Com essas regras não cabe nenhum lote: use o mercado fracionário (--lote 1).")

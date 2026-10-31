# Modelo do relatório

Salvar em `investimentos/analises/<ATIVO>-<AAAA-MM-DD>.md`. Curto em cima, detalhe embaixo.

```markdown
# <ATIVO> — <nome> · análise de <dd/mm/aaaa>

**Nota: <Comprar | Aumentar aos poucos | Manter | Reduzir | Vender / Evitar | REVISAR>** · prazo <curto/médio/longo> · perfil <...>
Preço na análise: R$ <x> (<data>) · Preço justo (faixa): R$ <a> a R$ <b> · Comparação: CDI <x>% a.a.

## Em uma frase
<a decisão e o motivo principal, em linguagem simples>

## Plano (se a pessoa decidir seguir)
| Entrada | Stop (tese deixa de valer) | Alvo | Prazo | Quantidade sugerida pelo risco |
|---|---|---|---|---|

## Por que (a evidência que decidiu)
- ...
## O que mudaria a decisão
- ...
## Principais riscos
- ...

---
## Detalhe
### Fundamentos e preço justo
### Gráfico
### Notícias e economia
### Sentimento
### Debate (resumo de cada lado e quem venceu)
### Proposta do operador e visão da equipe de risco
### Dados usados (fonte e data de cada um)

> Material de estudo, gerado por IA com dados públicos gratuitos. Não é recomendação de investimento (atividade
> regulada pela CVM). Resultados passados não garantem resultados futuros. A decisão e a responsabilidade são de quem
> investe; confira os números nas fontes oficiais antes de qualquer operação.
```

Linha no `investimentos/decisoes.md` (crie o arquivo com o cabeçalho se não existir):

```markdown
| Data | Ativo | Preço | Nota | Prazo | Stop | Alvo | Arquivo | Revisão (preço, resultado, lição) |
|---|---|---|---|---|---|---|---|---|
```

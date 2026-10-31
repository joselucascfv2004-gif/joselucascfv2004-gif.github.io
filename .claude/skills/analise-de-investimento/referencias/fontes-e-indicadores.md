# Fontes gratuitas e indicadores

Todas testadas em 31/10/2026 a partir da nuvem do Claude, sem chave e sem custo.

## Fontes
| Fonte | O que dá | Como |
|---|---|---|
| Yahoo Finanças (`yfinance`) | cotações diárias (B3 com `.SA`, exterior sem sufixo, índices `^BVSP`), dividendos, balanços anuais e trimestrais, múltiplos de hoje, consenso de preço-alvo | `scripts/dados.py` |
| Banco Central, API SGS | Selic meta (432), CDI anual (4389), IPCA 12 meses (13522), dólar PTAX (1), CDI diário (12) | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.<código>/dados?formato=json&dataInicial=dd/mm/aaaa&dataFinal=dd/mm/aaaa` |
| CVM, dados abertos | demonstrações oficiais de todas as companhias abertas (DFP anual, ITR trimestral), fatos relevantes, informes de fundos (inclusive FII) | `https://dados.cvm.gov.br/` (arquivos CSV/ZIP por ano) |
| Site de RI da empresa | releases de resultado, apresentações, calendário, histórico de proventos | busca "<empresa> relações com investidores" |
| B3 | proventos, data-com, informações de FIIs e ETFs | site da B3 |
| Notícias | fatos e contexto, sempre com data | busca na internet (WebSearch), preferindo veículos conhecidos e o próprio RI |

O Yahoo às vezes falha em fundos imobiliários (sem balanço, anos de dividendos faltando) e em empresas pequenas: confira
na CVM/B3/RI. Nunca use serviço pago, nem os gratuitos que exigem cadastro com chave, sem o José pedir.

## Indicadores, em linguagem simples
- **P/L** (preço / lucro por ação): quantos anos de lucro o preço paga. Baixo pode ser barato ou lucro que vai cair.
- **P/VP** (preço / patrimônio por ação): abaixo de 1 = vale menos que o patrimônio contábil. Principal para bancos e FIIs.
- **EV/EBITDA**: valor da empresa (com a dívida) sobre a geração de caixa operacional; bom para comparar com dívidas diferentes.
- **DY** (dividend yield): dividendos dos últimos 12 meses / preço. Compare com o CDI e veja se é recorrente ou extraordinário.
- **Payout**: parte do lucro paga como dividendos.
- **ROE**: lucro / patrimônio. Mostra quanto a empresa rende sobre o dinheiro dos sócios.
- **Margem líquida / EBITDA**: quanto de cada real vendido sobra.
- **Dívida líquida / EBITDA**: quantos anos de geração de caixa pagam a dívida (acima de 3 costuma pesar).
- **Fluxo de caixa livre**: dinheiro que sobra depois dos investimentos; é dele que saem dividendos sustentáveis.
- **JCP** (juros sobre capital próprio): forma de provento das empresas brasileiras, com imposto retido na fonte.
- **Data-com**: último dia com a ação para ter direito ao provento anunciado.

## Por tipo de ativo
- **Empresas em geral:** todos acima + preço justo (Graham, Bazin, fluxo de caixa descontado).
- **Bancos e seguradoras:** P/VP, ROE, índice de Basileia, inadimplência, custo do crédito. Fluxo de caixa descontado não se aplica.
- **Fundos imobiliários (FII):** DY mensal e constância, P/VP, vacância física e financeira, inadimplência, prazo e
  indexador dos contratos (IPCA, IGP-M), qualidade dos imóveis ou dos papéis (CRIs), taxa de administração. Compare o DY
  com o CDI e com o Tesouro IPCA+.
- **ETFs:** índice que copia, taxa, tamanho e liquidez; não há "balanço" para analisar.
- **Estatais:** pese o risco de interferência do governo (preços, dividendos, investimentos).
- **Sempre** compare com a alternativa sem risco: CDI/Tesouro Selic (`macro_brasil` do `dados.py`).

## Imposto
Regras de imposto mudam (proventos, JCP, isenção de vendas até R$ 20 mil/mês em ações, FIIs). Antes de afirmar qualquer
regra de imposto, confira o texto vigente com a skill `leis`.

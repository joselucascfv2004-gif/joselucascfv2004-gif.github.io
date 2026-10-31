# Depois da análise: tese, calendário, checklist e revisão

Ideias trazidas de `thesis-tracker` e `catalyst-calendar` (anthropics/financial-services, Apache 2.0),
`pre-trade-discipline-gate`, `position-sizer` e `signal-postmortem` (tradermonty/claude-trading-skills, MIT) e da
memória de decisões do TradingAgents.

## Tese (`investimentos/teses/<ATIVO>.md`)
- **Tese em 1–2 frases** (ex.: "Comprar ITUB4: banco mais rentável do país, ROE acima de 20% com inadimplência controlada").
- **Pilares** (3 a 5 argumentos) e **riscos que derrubam a tese** (3 a 5).
- **Catalisadores** com data (resultado, assembleia, decisão de governo).
- **Preço-alvo / faixa justa** e **quando sair** (o fato ou preço que invalida a tese).
- **Registro** de cada novidade: data | fato | efeito em qual pilar (fortalece/enfraquece/neutro) | ação | convicção (alta/média/baixa).
- **Placar**: pilar | esperado | situação atual | tendência.
Uma tese precisa poder ser provada errada; anote as evidências contra com o mesmo cuidado das a favor.

## Calendário de eventos
Para a lista de ativos e o prazo pedido: datas de resultado (RI), data-com de dividendos/JCP (B3/RI), assembleias,
reuniões do Copom e divulgação do IPCA (Banco Central/IBGE), eventos do setor. Tabela: data | evento | ativo | impacto
esperado (alto/médio/baixo) | o que observar. Na semana: os 3 eventos que mais importam e por quê.

## Checklist antes de comprar (a pessoa responde; se algum item falhar, diga claramente para não comprar ainda)
1. Existe um plano escrito (motivo, preço de entrada, stop e alvo)?
2. O tamanho cabe no limite (risco de 1% por operação e no máximo 10% da carteira num ativo)?
3. Não é compra por impulso, por dica de rede social ou para "recuperar" uma perda recente?
4. A carteira não fica concentrada demais num setor só?
5. Comparou com deixar o dinheiro no CDI/Tesouro Selic pelo mesmo prazo?
6. Sabe o que vai fazer se cair até o stop?

## Revisão de decisões (`investimentos/decisoes.md`)
Para cada decisão cujo prazo venceu (ou quando a pessoa pedir): preço atual e máximo/mínimo no período (`dados.py`),
retorno contra o Ibovespa e contra o CDI, se bateu stop ou alvo. Classifique: **acerto pelo motivo certo**, **acerto por
sorte** (o motivo da tese não aconteceu), **erro de análise**, **erro de execução** (não seguiu o plano). Escreva uma
lição curta na coluna "Revisão". As próximas análises leem essas lições antes de decidir.

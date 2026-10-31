---
name: analise-de-investimento
description: Analisa uma ação, fundo imobiliário, ETF ou BDR (B3 ou exterior) como uma mesa de investimentos com vários papéis — analistas de fundamentos, gráfico, notícias e sentimento, debate otimista × pessimista, operador, equipe de risco e gestor — e entrega um relatório em português com nota em 5 níveis, preço justo, plano e riscos. Tudo com dados gratuitos (Yahoo Finanças, Banco Central, CVM, notícias), sem chave de API paga. Também cria e atualiza teses, calendário de eventos, tamanho de posição, checklist antes de comprar e revisão de decisões passadas. Use para "analisa PETR4", "vale a pena comprar ITUB4", "o que acha de MXRF11", "preço justo de", "faz o TradingAgents", "revisa minha tese", "quantas ações compro", "como foi minha decisão de", ou qualquer pergunta sobre investir num ativo específico.
---

# Análise de investimento (mesa de analistas)

Método do **TradingAgents** (Tauric Research, Apache 2.0, artigo arXiv 2412.20138), refeito para rodar **de graça** com o
próprio Claude no lugar das IAs pagas, e reforçado com ideias das melhores skills de investimento abertas (ver
`CREDITOS.md`). Criada a pedido do José em 31/10/2026.

## Regras que valem sempre

1. **Não é recomendação de investimento.** É material de estudo. Recomendar valores mobiliários a terceiros é atividade
   regulada pela CVM (analista credenciado, Resolução CVM 20/2021). Todo relatório termina com o aviso do modelo. Nunca
   prometa ganho, nunca diga "compre agora" como ordem, e deixe claro o que pode dar errado.
2. **Nada pago e nada automático.** Só fontes gratuitas (`referencias/fontes-e-indicadores.md`). Nunca conectar em
   corretora, enviar ordem, nem pedir senha ou chave. Quem decide e opera é a pessoa.
3. **Ponto no tempo.** Com data no passado (teste de "e se eu tivesse comprado em…"), use só o que existia até a data:
   `dados.py --data`. Notícia, balanço ou cotação posterior não entram. Se uma informação for de hoje (fundamentos do
   Yahoo), diga isso e não deixe pesar na nota.
4. **Fato separado de opinião, com fonte e data.** Número sem fonte não entra. Se um dado faltar ou estiver estranho
   (dividendo que some, balanço velho), diga "não encontrei" em vez de inventar. Prefira o oficial: CVM, RI da empresa,
   B3, Banco Central.
5. **Português do Brasil e linguagem simples** — o leitor não é do mercado. Explique cada indicador na primeira vez
   (ex.: "P/L 5 = o preço equivale a 5 anos de lucro").
6. **Guarde só em repositório privado** (padrão: `projetos-jose/investimentos/`). Nunca em `estudos-enem-fotos` nem em
   `joselucascfv2004-gif.github.io`, que são públicos.

## Antes de começar (pergunte só o que faltar, numa mensagem)

- **Ativo** (código da B3 com `.SA` no fim: `PETR4.SA`, `MXRF11.SA`, `BOVA11.SA`; exterior sem sufixo: `AAPL`).
- **Data da análise** (padrão: hoje) e **prazo** (curto: semanas; médio: meses; longo: anos — padrão longo).
- **Perfil** (conservador, moderado, arrojado — padrão moderado) e se **já tem o ativo** (quanto e a que preço).
- Opcional: valor da carteira, para o tamanho da posição.
- **Modo:** `rápido` (padrão: todos os papéis nesta conversa, um depois do outro) ou `completo` (os 4 analistas como
  subagentes em paralelo e 2 rodadas de debate — mais completo, gasta bem mais do limite do Claude; ofereça, não force).

Leia antes, se existir, `investimentos/decisoes.md` e a tese do ativo em `investimentos/teses/`: decisões passadas e
as lições delas entram no contexto do gestor (é a "memória" do TradingAgents).

## Passo a passo

**1. Dados.** Rode (instala o que faltar: `pip install -q yfinance pandas requests`):
```bash
python3 .claude/skills/analise-de-investimento/scripts/dados.py PETR4.SA --pares PRIO3.SA RECV3.SA [--data AAAA-MM-DD] --saida /tmp/petr4
python3 .claude/skills/analise-de-investimento/scripts/valuation.py /tmp/petr4.json [--taxa 16 --g1 4 --gp 3 --dy-min 6]
```
Escolha 2 a 4 concorrentes da B3 do mesmo setor. Para notícias, fatos relevantes, calendário e o que o Yahoo não traz
(fundos imobiliários, balanço trimestral recente), busque na internet e nas fontes oficiais.

**2. Analistas (relatórios curtos, cada um termina com uma tabela de pontos-chave).** Papéis em `referencias/papeis.md`:
- **Fundamentos** — negócio, lucro, margens, dívida, geração de caixa, dividendos, múltiplos contra os concorrentes e o
  preço justo (Graham, Bazin, fluxo de caixa descontado com a tabela de sensibilidade). Bancos: P/VP, ROE, índice de
  Basileia, inadimplência. Fundos imobiliários: DY, P/VP, vacância, inadimplência, qualidade dos imóveis ou papéis.
- **Gráfico (técnico)** — escolha até 8 indicadores que se completam (médias de 50/200, RSI, MACD, Bollinger, ATR,
  volatilidade, queda máxima) e diga a tendência, sem prever preço exato.
- **Notícias e economia** — últimos 30 dias até a data: fatos relevantes, resultados, governo/regulação, petróleo,
  câmbio, Selic e IPCA (Banco Central), com data e link de cada notícia.
- **Sentimento** — tom do mercado e das redes sobre o ativo (notícias, fóruns, recomendações de casas). Se a amostra for
  fraca, diga que é fraca; não invente consenso.

**3. Debate otimista × pessimista** (1 rodada no modo rápido, 2 no completo). Cada lado usa os relatórios e responde
diretamente ao último argumento do outro, com dados. Proibido repetir sem rebater.

**4. Gerente de pesquisa** — julga o debate, diz quem venceu e por quê, e escreve o **plano de investimento** com a
nota provisória.

**5. Operador** — transforma o plano em proposta concreta: faixa de preço de entrada, stop (preço que invalida a tese),
alvo, prazo e tamanho (`scripts/tamanho_posicao.py --carteira ... --entrada ... --atr ...`, padrão 1% de risco por
operação e no máximo 10% da carteira num só ativo; fracionário se o lote de 100 não couber).

**6. Equipe de risco** — agressivo, conservador e neutro, cada um respondendo aos outros dois (1 rodada; 2 no completo).
Considere o perfil da pessoa e o que ela já tem.

**7. Gestor (decisão final)** — uma nota, exatamente uma:
| Nota | Quer dizer |
|---|---|
| **Comprar** | convicção forte para entrar ou aumentar |
| **Aumentar aos poucos** | visão favorável; ir comprando em partes |
| **Manter** | ficar como está; nada a fazer agora |
| **Reduzir** | diminuir a exposição, realizar parte |
| **Vender / Evitar** | sair da posição ou não entrar |
Discordância entre os papéis **não é motivo para "Manter"**: decidir qual lado tem a evidência mais forte é o trabalho.
Use "Manter" só se a evidência continuar equilibrada ou fraca demais. Se não der para decidir com o que há, diga
**REVISAR** e o que falta — nunca disfarce dúvida de "Manter".

**8. Relatório** no formato de `referencias/modelo-relatorio.md`, salvo em
`investimentos/analises/<ATIVO>-<AAAA-MM-DD>.md`, e uma linha em `investimentos/decisoes.md` (data, ativo, preço, nota,
prazo, stop, alvo). Mostre na conversa o resumo de cima (nota, por quê, plano, riscos) e o caminho do arquivo.

## Outros pedidos (detalhes em `referencias/acompanhamento.md`)

- **Tese:** criar ou atualizar a tese de um ativo (pilares, riscos que a derrubam, catalisadores, preço-alvo, quando sair).
- **Calendário de eventos:** resultados trimestrais, data-com de dividendos e JCP, Copom, IPCA, assembleias.
- **Tamanho da posição:** só o `tamanho_posicao.py`, explicando o resultado.
- **Checklist antes de comprar:** plano escrito? stop definido? tamanho dentro do limite? não é compra por impulso ou
  para "recuperar" uma perda? carteira não fica concentrada demais?
- **Revisão de decisões:** compara cada decisão do `decisoes.md` com o que o preço fez depois (no prazo combinado e
  contra o Ibovespa), separa acerto por sorte de acerto pelo motivo certo e grava a lição para as próximas análises.
- **Comparar ativos:** a mesma mesa com 2 a 5 ativos lado a lado (só fundamentos, preço justo e riscos; sem debate).

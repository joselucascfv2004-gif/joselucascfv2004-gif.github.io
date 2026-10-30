# Tela com "cara de feita por IA"

Vale para qualquer tela nova feita com o Claude (site, cardápio, painel, página de vendas). Junta quatro vídeos do
TikTok de 30/10/2026: os 20 sinais de @millee.md, a "evolução do vibe coding" de @100dayvibecoding, os 5
repositórios de @alexandrekleppa e as 3 configurações de @migue.baena. Use junto com a lista geral do `SKILL.md`.
As regras do projeto vêm antes: se o dono escolheu uma cor ou uma fonte, ela fica.

## Os 20 sinais (procure e troque)

| Sinal | Troque por |
|---|---|
| 1. Degradê roxo para azul | Uma cor de marca com uso contido; fundo neutro puxado para essa cor |
| 2. Título com degradê no texto | Título numa cor sólida, com peso e tamanho fazendo o destaque |
| 3. Emoji nos títulos | Ícone do mesmo conjunto da tela, ou nada |
| 4. Fonte Inter em tudo | Um par escolhido para o assunto (título com personalidade + texto legível) |
| 5. Cartões com borda colorida de um lado | Cartão neutro; cor só onde é estado (erro, novo, pago) |
| 6. Cartões de vidro fosco (glassmorphism) | Superfície sólida com borda fina ou sombra leve |
| 7. Modo escuro com pouco contraste | Contraste de 4,5:1 no texto; cinzas que dá para ler |
| 8. Três caixinhas de ícone lado a lado | Arrumação que vem do conteúdo (lista, comparação, número em destaque) |
| 9. Etiqueta em cima do título ("Novo!") | Só quando a etiqueta informa algo real |
| 10. Ícones Lucide em tudo, sem escolha | Um conjunto escolhido, mesmo traço e tamanho, usado só onde ajuda |
| 11. Componentes shadcn sem mudar nada | Ajustar raio, cores, espaçamento e estados à marca |
| 12. Seções que aparecem ao rolar | Conteúdo visível de cara; animação só onde explica algo |
| 13. Luz que segue o cursor | Nada (ou um efeito que tenha a ver com o produto) |
| 14. Botão que só fica transparente ao passar o mouse | Estado claro: cor, sombra ou borda mudando, e foco visível no teclado |
| 15. Espaçamento desigual | Escala fixa (4, 8, 12, 16, 24, 32, 48) repetida em tudo |
| 16. Travessão (—) em todo texto | Frases curtas com ponto, vírgula ou dois-pontos |
| 17. Frases de efeito genéricas ("potencialize", "revolucione") | O que o produto faz, com números e palavras do cliente |
| 18. Palavra em itálico com serifa no meio do título | Destaque pelo peso ou pela cor, se precisar |
| 19. Space Grotesk + Instrument Serif | Outro par, escolhido para o assunto |
| 20. Textura granulada no fundo | Fundo liso; textura só se fizer parte da marca |

Nenhum item é proibido sozinho. O problema é a soma: cinco ou mais na mesma tela = cara de modelo pronto.

## A "evolução" que o vídeo mostra

O mesmo painel em três versões: (1) roxo neon, brilho e degradê; (2) cinza escuro com o roxo apagado; (3) tela
calma, neutra, com um único destaque de cor nos números importantes e um gráfico de linha fino. O caminho certo é
esse: **tirar efeito até sobrar só o que informa**, e deixar a cor para o que precisa chamar atenção.

## Como pedir ao Claude (para não sair genérico)

- Não peça só "faz uma tela bonita". Dê **referências** (2 ou 3 sites ou telas de que o dono gosta), **regras**
  (as do projeto + esta lista) e **um jeito de conferir** (fotos com `scripts/fotos.js`).
- Antes de escrever código, defina e anote: 4 a 6 cores com nome, 2 fontes, a escala de espaço e o raio dos cantos.
- Depois de pronto, compare a tela com os 20 sinais e com a lista geral do `SKILL.md`, e mostre o antes e depois.

## Ferramentas que ajudam (veja `ferramentas.md`)

- Já instaladas na conta: **Taste Skill** (`design-taste-frontend-v1`), **Impeccable** (`impeccable`),
  **frontend-design** e **animacoes-interface**.
- Recomendadas nos vídeos e ainda não instaladas: UI UX Pro Max, Design Motion Principles (regras de animação do
  Emil Kowalski e outros), Awesome Claude Design (DESIGN.md prontos) e o extrator de DESIGN.md para Chrome.

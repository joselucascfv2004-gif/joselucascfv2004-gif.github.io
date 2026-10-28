# Como usar o cérebro

Este repositório tem um "cérebro" no estilo Obsidian, para o Claude **ler menos e gastar menos** do seu limite
(ideia do vídeo que você mandou em 28/10/2026, feita do nosso jeito e de graça).

## O que acontece sozinho

1. **Mapa**: no começo de toda sessão do Claude, o [[00 - Mapa]] é refeito. Ele diz, em poucas linhas, o que tem em
   cada pasta. O Claude lê o mapa primeiro e abre só o que precisa, em vez de ler o projeto inteiro.
2. **Busca**: quando o Claude precisa achar um assunto, ele usa a busca do cérebro, que devolve só os trechos certos
   (arquivo e linha). É um programa pequeno, grátis, que roda sem internet e sem nenhuma chave.
3. **Diário**: decisões e aprendizados importantes de cada tarefa ficam em `cerebro/Diário/` (um arquivo por dia).
   As regras que valem para sempre continuam no `CLAUDE.md`.

## Como ver no Obsidian (no seu computador)

1. Baixe o Obsidian, que é grátis: https://obsidian.md
2. Tenha a pasta deste repositório no computador (pelo GitHub Desktop: "Clone repository").
3. No Obsidian, clique em **"Abrir pasta como cofre"** e escolha a pasta do repositório.
4. Abra `cerebro/00 - Mapa` e `cerebro/Diário`. O "Graph view" (gráfico) mostra como as notas se ligam.
5. Antes de abrir, use "Fetch/Pull" no GitHub Desktop para pegar as anotações mais novas.

## E o LightRAG do vídeo?

O LightRAG monta um "grafo de conhecimento", mas para isso ele precisa de um modelo de IA lendo todos os arquivos.
Com uma API de IA isso custa dinheiro; de graça, só rodando um modelo no seu próprio computador (Ollama). Por isso,
aqui usamos a **busca grátis do cérebro**, que dá o mesmo resultado prático (o Claude acha o trecho certo sem ler
tudo). Se um dia você quiser o LightRAG no seu PC com o Ollama, é só pedir.

# Menu lateral (sidebar)

Barra vertical com a navegação principal, ao lado do conteúdo: painéis, sistemas internos, CRMs (no SUI, no
painel da Degust e no `caca-clientes`). Tirado do carrossel "How to Design Better Sidebar" de @ux_dose
(TikTok, 30/10/2026, medidas de Jan Mráz). Use junto com a lista geral do `SKILL.md` e com
`sistema-interno.md`.

## Estrutura, de cima para baixo

1. **Marca** (logo e nome) e o botão de **recolher/abrir** o menu.
2. **Busca** ("Buscar…"), se o sistema tiver muitas telas.
3. **Itens principais**, com um rótulo de grupo pequeno em cima ("Principal").
4. **Grupo secundário** com o próprio rótulo ("Comunicação"), separado do primeiro por espaço.
5. **Indicador de status** à direita do item quando há novidade (contador "9+", bolinha).
6. **Chamada para ação** perto do fim: um cartão pequeno (uso do plano, novidade, "Experimente"), com no máximo
   um botão. Pode ter um X para fechar.
7. **Configurações e Ajuda**, sempre embaixo.
8. **Conta/espaço de trabalho** no rodapé: foto, nome, e-mail e o botão de sair.

O **item ativo** tem fundo destacado (e, se quiser, um traço na borda). Todo item tem **estado de passar o mouse**.

## Medidas que funcionam (menu aberto com 240 px; recolhido com 80 px)

- Margem interna dos lados: **16 px**. Topo e rodapé: **44 px** até o primeiro e o último elemento.
- Linha do logo: **32 px** de altura. Busca: **32 px**. Do logo até a busca: **16 px**.
- Cada item: **40 px** de altura, com **4 px** entre um item e outro, e **8 px** entre o ícone e o texto.
- Rótulo de grupo: **16 px** de altura e **4 px** até o primeiro item. Entre grupos: **24 px**.
- Antes e depois do cartão de chamada: **48 px**. Dentro dele: 24 em cima, 12–16 entre as partes, 32 embaixo.
- Rodapé (conta): **40 px**, separado de Configurações/Ajuda por uma divisória com **16 px** de cada lado.

Use os mesmos números em todo o menu: é a repetição que deixa o menu "calmo".

## Menu recolhido

- Só os ícones, centralizados, na mesma altura de 40 px; a busca vira só a lupa; o cartão de chamada some.
- Ao passar o mouse num ícone, aparece uma **dica escura com o nome** ("Documentação").
- O botão de abrir fica no mesmo lugar do botão de recolher, com a seta invertida.
- O contador vira uma bolinha no canto do ícone.

## Segundo nível

- Mostre páginas internas como **subitens que abrem e fecham** debaixo de um item principal (seta para baixo e
  para cima), recuados e ligados por uma **linha guia** vertical que mostra a quem pertencem.
- **No máximo dois níveis.** Se precisar de um terceiro, a organização das telas está errada, não o menu.

## No celular

O menu lateral vira uma gaveta (abre por cima do conteúdo com um botão de menu) ou uma barra de abas embaixo
com até 5 destinos. Nunca deixe o menu de 240 px empurrando o conteúdo numa tela de 375 px.

---
name: revisar-tela
description: Revisa e melhora o visual e a facilidade de uso de qualquer tela com front-end (site, loja, página de vendas, cardápio online, sistema interno, painel, tabela, formulário, app de celular em React Native/Expo, landing page, e-mail em HTML), com uma lista de erros comuns de espaçamento, alinhamento, cor, letra, ícones e ordem da informação, e explica o porquê de cada mudança. Use quando o pedido for "deixa essa tela mais bonita", "redesign", "melhora o visual", "essa página está feia", "está apertado/bagunçado", "revisa o layout", "deixa mais profissional", "por que essa tela não convence", ou antes de entregar uma tela nova.
---

# Revisar tela (UI/UX)

Nasceu do vídeo "UI/UX redesign" de @codevibes_1 (TikTok, https://vt.tiktok.com/ZSgttKNBK/), em que
uma página de produto é corrigida em 15 passos. Aqui o método foi generalizado para **qualquer tela**.
A ideia central: **não basta deixar bonito; a tela tem que deixar mais fácil entender, confiar e agir.**
Cada mudança precisa de um motivo que o dono do projeto entenda.

**As regras do projeto vêm antes desta lista** (leia o `CLAUDE.md`). Exemplos: no app `estudos` não se usa
emoji, só ícones; nos modelos de cardápio cada tipo tem cor fixa e no máximo 4 cores; no
`orcamentopaulista` o site é um HTML único montado pelo `build.py`.

## 1. Entender a tela

1. **Tipo de tela** e o arquivo de apoio para abrir (só o que servir):

   | Tipo | Exemplos | Abrir |
   |---|---|---|
   | Produto, loja, cardápio | página de produto, item do cardápio, sacola, checkout | `tipos/produto.md` |
   | Página de vendas, site institucional | landing page, página de captura, "sobre", portfólio | `tipos/pagina-de-vendas.md` |
   | Sistema interno, painel | tabelas, relatórios, conferência, CRM, painel de pedidos | `tipos/sistema-interno.md` |
   | Formulário | cadastro, login, checkout, configurações, filtros | `tipos/formulario.md` |
   | App de celular | React Native / Expo, telas de app, PWA | `tipos/app-celular.md` |
   | Menu lateral | sidebar de painel, sistema interno, CRM | `tipos/menu-lateral.md` |
   | Tela nova feita com IA | qualquer tela criada do zero pelo Claude | `tipos/cara-de-ia.md` (os 20 sinais) |

   Para escolher fontes, cores e animações com mais critério, veja as skills e ferramentas em
   `tipos/ferramentas.md` (Taste Skill, Impeccable e outras).

   Uma tela pode ser de dois tipos (um checkout é produto e formulário): abra os dois.
2. **Objetivo principal:** o que a pessoa veio fazer (comprar, pedir, conferir um valor, achar um
   cadastro, responder uma questão, salvar). Tudo na tela deve ajudar isso ou sair do caminho.
3. **Quem usa e onde:** cliente no celular, funcionário no computador do trabalho, gente com pressa.
   Sistema interno é usado o dia todo: rapidez e clareza valem mais que enfeite.

## 2. Ver a tela como ela é (antes)

Use os scripts desta skill (pasta `scripts/`; Playwright já vem instalado na nuvem):

```bash
SK=<pasta desta skill>
# páginas que carregam arquivos .json/.js ao lado precisam de servidor (file:// não deixa)
cd <raiz do repositório> && python3 -m http.server 8765 --bind 127.0.0.1 &
node $SK/scripts/fotos.js /tmp/antes "http://127.0.0.1:8765/caminho/pagina.html" --larguras 375,1280
```

- Tire as fotos **tela por tela, rolando** (o script faz isso). Foto da página inteira de uma vez engana:
  avisos fixos ("Carregando…", barra de compra) ficam por cima e imagens "lazy" saem em branco.
- **Celular (375 px)** sempre. **Computador (1280 px)** quando a tela for usada no computador
  (sistemas internos, painéis, sites institucionais).
- Para ver janelas e menus, use `--clicar "Texto do botão"` antes das fotos.
- Teste com **conteúdo difícil**: nome comprido, número grande (R$ 1.234.567,89), lista vazia, lista com
  200 linhas, foto clara e foto escura, mensagem de erro. Uma tela de verdade não vive só do exemplo.
- Se a tela depende de serviço de fora (Firebase, API), o navegador de teste precisa usar a rede da máquina:
  `--rede` no `fotos.js` (proxy do ambiente, sem passar o servidor local por ele). Firebase/Firestore que
  fica em "Carregando" na nuvem: a conexão contínua dele não atravessa o proxy; para **só ver**, force
  `experimentalForceLongPolling` com um `addInitScript` (exemplo em `scripts/firebase-ver.js`), sem mexer no
  arquivo do site. Se nem assim abrir, diga isso ao dono em vez de mexer às cegas.
- App em React Native: veja `tipos/app-celular.md`.

## 3. Lista geral (vale para qualquer tela)

Percorra a lista e anote **só o que achar de verdade**, com a foto como prova.

**Espaço e alinhamento**
1. **Margens iguais.** Tudo começa na mesma linha da esquerda (ex.: 16 px no celular, 24 px no
   computador). Elemento "quase alinhado" passa descuido, mesmo sem a pessoa saber por quê.
2. **Espaço conta a relação.** O que é ligado fica perto; o que é diferente fica mais longe. Use poucos
   tamanhos de espaço (4, 8, 12, 16, 24, 32, 48) e repita-os. Espaço demais deixa "solto"; de menos, apertado.
3. **Colunas que batem.** Em listas e opções, o que é igual fica na mesma coluna: preços à direita,
   caixinhas de marcar na mesma posição mesmo quando a linha não tem preço.
4. **Nada vaza nem quebra feio.** Sem rolagem para o lado no celular; texto longo quebra ou corta com
   "…"; valores como "R$ 14,90" e datas não se partem em duas linhas (`&nbsp;` ou `white-space:nowrap`).

**Hierarquia (o que chama atenção primeiro)**
5. **Uma coisa principal por tela.** Um só botão forte; os outros mais discretos (contorno ou texto).
6. **Título se destaca sem gritar.** Ajuste tamanho e peso. Evite tudo em maiúsculas em textos longos e
   botões grandes.
7. **Texto corrido confortável:** altura de linha 1,4 a 1,6, linhas de até ~70 letras, cor um pouco mais
   clara que o título. Título chama atenção; parágrafo ajuda a entender.

**Cor e letra**
8. **Poucas cores, com função.** Cor forte só para a ação principal e para avisos (erro, sucesso). Cores
   saturadas demais cansam e disputam atenção.
9. **Contraste legível:** texto sobre fundo com contraste de pelo menos 4,5:1 (texto pequeno cinza-claro
   sobre branco é o erro mais comum). Ícones sobre fotos precisam de fundo próprio.
10. **Uma família de letra basta.** Hierarquia vem de tamanho, peso e cor, não de várias fontes.

**Ícones, etiquetas e divisórias**
11. **Ícones do mesmo jeito:** todos de traço ou todos cheios, mesma espessura, mesmo tamanho, poucas
    cores. Emojis misturados com ícones (ou emojis de estilos diferentes) bagunçam: troque por um conjunto
    de ícones em SVG. Cuidado com CSS que faz `svg {display:block}`: ponha `display:inline-block` no ícone.
12. **Etiquetas curtas:** lidas num relance ("20% off", "Pago", "Atrasado"). Etiqueta pequena em
    maiúsculas pede um pouco de espaço entre as letras.
13. **Divisórias leves:** linha fina e clara, ou só espaço. Linha grossa e escura corta a tela em blocos.
14. **Sem rótulo repetitivo:** "Preço: R$ 6,20" não precisa de "Preço"; o símbolo já diz.

**Informação no lugar certo**
15. **Ordem da decisão:** o que a pessoa precisa saber para agir vem antes e perto do botão (no produto:
    nome, avaliação, preço; num relatório: o total e o que está errado; num cadastro: o que é obrigatório).
16. **Nada engana:** nome, número e botão dizem exatamente o que vai acontecer ("Adicionar · R$ 30,00",
    "Excluir 3 lançamentos").

**Estados e toque**
17. **Todos os estados existem e são bonitos:** carregando, vazio ("Nenhum pedido hoje"), erro (o que
    fazer), sucesso, desabilitado (por quê).
18. **Área de toque de pelo menos 44 px** no celular; botões e links não ficam colados.
19. **Foco visível no teclado** e `aria-label` em botões que só têm ícone.
20. **Tema escuro**, se a tela tiver: confira as mesmas coisas nele (contraste, ícones, sombras).

## 4. Corrigir e mostrar

1. **Nunca remova funcionalidade** (regra do dono, 30/10/2026): botão, link, atalho, informação, aviso ou
   dica que existe continua existindo, inclusive nos protótipos. Isso **não** é "mexer o mínimo": o visual
   pode mudar bastante (arrumação, cartões, grade, destaque, cores, ordem), como no protótipo aprovado.
   Juntar duas colunas só se nenhuma informação se perder. Antes de entregar, liste o que a tela
   tinha e confira que tudo ainda está lá.
2. Corrija primeiro o que **atrapalha de verdade** (lido, achado, clicado). Mudança de gosto só se o
   dono pedir. Mude o **componente comum** (CSS/JS compartilhado) quando o erro se repete em várias telas.
3. Respeite o projeto: cores fixas, sem emoji onde é proibido, arquivos autocontidos, cópias de deploy
   iguais à raiz, gerador em vez do arquivo gerado, `build.py` em vez do `dist/`.
4. Tire as fotos **depois** com o mesmo comando e monte o antes e depois:
   `python3 $SK/scripts/juntar.py saida.jpg "ANTES · Loja" /tmp/antes/x.jpg "DEPOIS · Loja" /tmp/depois/x.jpg`
   e envie a imagem ao dono.
5. Explique em português simples: **o problema, por que atrapalha e o que mudou**. Nada de jargão
   ("hierarquia visual" vira "o que chama atenção primeiro").
6. Nunca publique (Netlify, EAS Update, artefato) sem o dono pedir.

# App de celular (React Native / Expo, PWA)

Use junto com a lista geral do `SKILL.md`. Os princípios são os mesmos; muda o jeito de ver e de corrigir.

## Como ver a tela

1. Se o projeto roda na web, monte uma cópia à parte e fotografe em 375 px. Confira antes se o projeto tem
   `react-native-web` (veja `package.json`); **não instale pacote novo só para isso** sem perguntar (no
   `estudos`, pacotes entram com `npx expo install`). Receita testada no `estudos` (30/10/2026):
   `git worktree add <pasta-temporária> <ramo mais recente> --detach`, `cd app && npm ci`,
   `CI=1 npx expo export --platform web --output-dir dist-web`, sirva `dist-web` com
   `python3 -m http.server` e navegue com Playwright. O app rola dentro da própria lista (não a página):
   role com `page.mouse.wheel` e passe pelo cadastro inicial clicando nos botões por texto. Guarde o estado
   (`context.storageState`) para abrir direto no Início nas próximas fotos. No fim, `git worktree remove`.
2. Se não rodar na web, revise pelo código: estilos (`StyleSheet`, tema), componentes de lista e cartão,
   e as telas de `app/src/`. Diga ao dono que a revisão foi pelo código e peça uma captura de tela do
   celular dele quando precisar ver algo.

## O que olhar em app

- **Área segura:** nada embaixo do entalhe da câmera nem da barra de gestos (`SafeAreaView`/insets).
- **Toque:** botões com pelo menos 44×44; `hitSlop` em ícones pequenos; retorno visual ao tocar.
- **Teclado:** o campo e o botão de enviar continuam visíveis com o teclado aberto
  (`KeyboardAvoidingView`), e o teclado fecha ao tocar fora.
- **Listas longas** com `FlatList`; estado vazio, carregando (esqueleto ou indicador) e erro com
  "Tentar de novo".
- **Tamanho de letra do sistema:** a tela não quebra com a fonte do celular aumentada.
- **Tema claro e escuro** com as cores do tema escolhido, sem cor fixa no meio do código.
- **Botão voltar do Android** faz o esperado; tarefa longa guarda o andamento.
- **Ícones de um só conjunto** (no `estudos`: componente `Icone` com MaterialCommunityIcons; nunca emoji).
- Componentes repetidos (cartão, botão, cabeçalho): corrija no componente comum, não em cada tela.

## Entregar

- Rode as checagens do projeto (no `estudos`: `npm run typecheck`).
- Publicar para os celulares (EAS Update) só quando o dono pedir.

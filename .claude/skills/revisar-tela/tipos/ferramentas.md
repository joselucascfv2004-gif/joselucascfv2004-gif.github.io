# Ferramentas de design para o Claude

Levantadas a partir dos vídeos de @alexandrekleppa (5 repositórios) e @migue.baena (3 configurações), em
30/10/2026. Todas gratuitas. Conferido no GitHub: licença e o que cada uma faz.

## Já instaladas na conta do José (usar direto)

| Skill | Para quê |
|---|---|
| `design-taste-frontend-v1` (Taste Skill) | Tirar a cara de "feito por IA" e dar acabamento profissional |
| `impeccable` | Revisar, polir, ajustar hierarquia, estados vazios, formulários |
| `frontend-design` | Escolher direção visual, fontes e cores que não pareçam modelo pronto |
| `animacoes-interface` | Animações de interface prontas (números que contam, gráficos que se desenham, abas) |

## Recomendadas e ainda não instaladas

| Projeto | Licença | O que faz | Observação |
|---|---|---|---|
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | Monta um design system para o projeto (estilos, paletas, pares de fontes, 119 regras de UX) | ~3,7 MB; tem scripts Python de busca local (rodam na nuvem, não nos PCs do José) |
| [Design Motion Principles](https://github.com/kylezantos/design-motion-principles) | MIT | Criar e auditar animações com as regras de Emil Kowalski, Jakub Krehel e Jhey Tompkins | Só textos e modelos HTML, ~250 KB |
| [Awesome Claude Design](https://github.com/VoltAgent/awesome-claude-design) | ver repositório | 68 arquivos DESIGN.md prontos (inspirações de design system) | Escolher um e usar como ponto de partida |
| [design-md-chrome](https://github.com/bergside/design-md-chrome) | ver repositório | Extensão do Chrome que lê as cores, fontes e espaçamentos de um site aberto e gera um DESIGN.md | Instala no Chrome do José (modo desenvolvedor) |

Para instalar uma skill de fora: o José precisa aprovar, porque ela traz código de terceiros. Copie a pasta da skill
para `.claude/skills/` com o arquivo de licença e anote no `CLAUDE.md`. Pergunte se vai para os 7 repositórios.

## Testar o próprio resultado

- **Playwright** (já vem instalado na nuvem): `scripts/fotos.js` tira fotos tela por tela em 375 e 1280 px, clica em
  botões e monta antes e depois. O Claude deve olhar as fotos e corrigir antes de entregar.
- **Figma**: se o José passar a desenhar no Figma, conectar o conector do Figma no claude.ai para o Claude ler os
  quadros e transformar em código.

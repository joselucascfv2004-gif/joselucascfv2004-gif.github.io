# Instruções do repositório `joselucascfv2004-gif.github.io`

<!-- cerebro -->
## Cérebro do repositório (ler menos, gastar menos)

Pedido do dono em 28/10/2026, a partir de um vídeo sobre economizar o limite do Claude com Obsidian + mapa + busca.

- **Antes de abrir arquivos, leia `cerebro/00 - Mapa.md`** (curto: uma linha por pasta). Abra só o mapa detalhado
  da pasta que interessa (`cerebro/Mapa/<pasta>.md`) e só os arquivos de que precisa. Não leia pastas inteiras.
- **Para achar um assunto, busque em vez de ler:** `python3 ferramentas/cerebro.py buscar "assunto"` mostra os trechos
  certos com arquivo e linha (grátis, sem internet, sem API).
- **Ao terminar uma tarefa, anote o que importa** (decisão do dono, regra nova, problema e solução):
  `python3 ferramentas/cerebro.py anotar "texto curto"`. Vai para `cerebro/Diário/`, que o dono lê no Obsidian.
  Regras permanentes continuam indo para este `CLAUDE.md`.
- O mapa é refeito sozinho no começo de cada sessão (gancho `SessionStart` em `.claude/settings.json`); não edite
  o mapa à mão. A pasta `.cerebro-cache/` é só cache da busca (fica fora do Git).

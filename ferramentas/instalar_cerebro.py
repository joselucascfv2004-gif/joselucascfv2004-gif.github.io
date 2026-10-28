#!/usr/bin/env python3
"""Instala (ou atualiza) o "cérebro" num repositório: mapa, busca, diário, cofre do Obsidian e o gancho
que refaz o mapa no começo de cada sessão do Claude. Pode rodar quantas vezes quiser: não duplica nada.

Uso:  python3 ferramentas/instalar_cerebro.py [--publico] /caminho/do/repositorio [outro ...]
      (--publico: repositório público; não grava a lista dos outros repositórios, que são privados)
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCA = "<!-- cerebro -->"

SECAO_CLAUDE = f"""
{MARCA}
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
"""

COMO_USAR = """# Como usar o cérebro

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
"""

OUTROS = """# Outros repositórios do dono

Todos no GitHub de joselucascfv2004-gif. Cada um tem o seu próprio cérebro (`cerebro/00 - Mapa.md`).

| Repositório | O que é |
|---|---|
| `estudos` | App Estudos (questões no estilo Duolingo para ENEM, militares e concursos) e o canal do TikTok |
| `estudos-enem-fotos` | Fotos dos enunciados das provas oficiais do ENEM (2009 a 2025) que o App Estudos baixa |
| `orcamentopaulista` | Sistema Unificado de Informações (SUI) da execução orçamentária da Prefeitura de Paulista – PB |
| `projetos-jose` | Projetos pessoais: sistema da Degust Pizzaria, Emulador JLC e Sistema para Clientes |
| `videos-teste` | Gerador de vídeos curtos animados (animação flat + narração + legenda karaokê) |
| `vendasteste` | Vendas online: e-book "Revisão Final ENEM 2026" (ativo) e loja de dropshipping BlendGo (pausada) |
| `joselucascfv2004-gif.github.io` | Site público no GitHub Pages (página do app e política de privacidade) |
"""

OBSIDIAN = {"userIgnoreFilters": ["node_modules/", "dist/", "saida/", ".cerebro-cache/", ".claude/"],
            "alwaysUpdateLinks": True, "newFileLocation": "folder", "newFileFolderPath": "cerebro"}

GANCHO = {"type": "command",
          "command": "python3 \"$CLAUDE_PROJECT_DIR/ferramentas/cerebro.py\" mapa --silencioso 2>/dev/null; "
                     "echo 'Cérebro: leia cerebro/00 - Mapa.md antes de abrir arquivos; busque com "
                     "python3 ferramentas/cerebro.py buscar \"assunto\"; anote decisões com "
                     "python3 ferramentas/cerebro.py anotar \"...\"'"}


def instalar(repo: Path, publico: bool = False) -> None:
    (repo / "ferramentas").mkdir(exist_ok=True)
    for nome in ("cerebro.py", "instalar_cerebro.py"):
        if (repo / "ferramentas" / nome).resolve() != (AQUI / nome).resolve():
            shutil.copy2(AQUI / nome, repo / "ferramentas" / nome)
    cerebro = repo / "cerebro"
    (cerebro / "Diário").mkdir(parents=True, exist_ok=True)
    (cerebro / "01 - Como usar.md").write_text(COMO_USAR, encoding="utf-8")
    if not publico:
        (cerebro / "Outros repositórios.md").write_text(OUTROS, encoding="utf-8")
    leia = cerebro / "Diário" / "LEIA-ME.md"
    if not leia.exists():
        leia.write_text("# Diário\n\nUm arquivo por dia, criado pelo Claude com "
                        "`python3 ferramentas/cerebro.py anotar \"...\"`.\n", encoding="utf-8")
    # cofre do Obsidian
    (repo / ".obsidian").mkdir(exist_ok=True)
    app = repo / ".obsidian" / "app.json"
    dados = json.loads(app.read_text(encoding="utf-8")) if app.exists() else {}
    dados.update(OBSIDIAN)
    app.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # .gitignore: cache da busca e arquivos pessoais do Obsidian
    gi = repo / ".gitignore"
    atual = gi.read_text(encoding="utf-8") if gi.exists() else ""
    faltam = [l for l in (".cerebro-cache/", ".obsidian/workspace*.json") if l not in atual.splitlines()]
    if faltam:
        gi.write_text(atual + ("" if atual.endswith("\n") or not atual else "\n") + "\n".join(faltam) + "\n", encoding="utf-8")
    # gancho que refaz o mapa no começo de cada sessão
    cfg = repo / ".claude" / "settings.json"
    cfg.parent.mkdir(exist_ok=True)
    config = json.loads(cfg.read_text(encoding="utf-8")) if cfg.exists() else {}
    inicio = config.setdefault("hooks", {}).setdefault("SessionStart", [])
    if not any("cerebro.py" in h.get("command", "") for bloco in inicio for h in bloco.get("hooks", [])):
        inicio.append({"hooks": [GANCHO]})
    cfg.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # regra no CLAUDE.md
    claude = repo / "CLAUDE.md"
    texto = claude.read_text(encoding="utf-8") if claude.exists() else f"# Instruções do repositório `{repo.name}`\n"
    if MARCA not in texto:
        claude.write_text(texto.rstrip("\n") + "\n" + SECAO_CLAUDE, encoding="utf-8")
    subprocess.run([sys.executable, str(repo / "ferramentas" / "cerebro.py"), "mapa"], check=True)


if __name__ == "__main__":
    publico = "--publico" in sys.argv
    for caminho in [a for a in sys.argv[1:] if not a.startswith("--")]:
        instalar(Path(caminho).resolve(), publico)

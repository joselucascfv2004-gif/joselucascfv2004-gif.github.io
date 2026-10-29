#!/usr/bin/env python3
"""Cérebro do repositório: mapa, busca e anotações, para o Claude ler menos e gastar menos.

Inspirado na dica "Claude + Obsidian + mapa + busca" (vídeo enviado pelo dono em 28/10/2026), feito do
nosso jeito e 100% grátis (só Python, sem internet, sem API):

    python3 ferramentas/cerebro.py mapa            # refaz cerebro/00 - Mapa.md (o que tem em cada pasta)
    python3 ferramentas/cerebro.py buscar "texto"  # acha os trechos certos sem abrir arquivo por arquivo
    python3 ferramentas/cerebro.py anotar "texto"  # guarda uma decisão/aprendizado no diário (cerebro/Diário/)

A pasta do repositório pode ser aberta no Obsidian (app grátis) como "cofre": as notas ficam em `cerebro/`.
O mapa é refeito sozinho no começo de cada sessão do Claude (gancho em `.claude/settings.json`).
"""

import json
import math
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA = RAIZ / "cerebro"
CACHE = RAIZ / ".cerebro-cache"
MAPA = PASTA / "00 - Mapa.md"
TEXTO = {".md", ".txt", ".py", ".js", ".mjs", ".ts", ".tsx", ".jsx", ".html", ".css", ".json", ".sh", ".ps1",
         ".yml", ".yaml", ".toml", ".csv", ".sql", ".java", ".kt", ".c", ".h", ".cpp", ".cs", ".go", ".rs", ".php"}
IGNORAR = {"node_modules", "dist", "build", ".git", ".cerebro-cache", "saida", "__pycache__", ".venv", "venv",
           ".next", "coverage", ".obsidian"}
LIMITE_ARQUIVO = 400_000      # acima disto (bytes) o mapa não lê a descrição do arquivo
LIMITE_BUSCA = 8_000_000      # acima disto o arquivo não entra na busca
FORA_DA_BUSCA = (".claude/skills/", "cerebro/Mapa/")  # manuais de ferramentas e o próprio mapa só atrapalham a busca
JUNTAR_ACIMA = 12             # pasta com mais arquivos do mesmo tipo que isto vira uma linha só no mapa
BRASILIA = timezone(timedelta(hours=-3))


def arquivos() -> list[Path]:
    """Arquivos do Git (rastreados e novos), sem as pastas pesadas."""
    try:
        saida = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=RAIZ,
                               capture_output=True, text=True, check=True).stdout.splitlines()
        lista = [Path(s) for s in saida]
    except (subprocess.CalledProcessError, FileNotFoundError):
        lista = [p.relative_to(RAIZ) for p in RAIZ.rglob("*") if p.is_file()]
    return sorted(p for p in lista if not any(parte in IGNORAR for parte in p.parts) and (RAIZ / p).is_file())


def descricao(caminho: Path) -> str:
    """Uma linha dizendo o que é o arquivo (título, docstring, <title> ou primeiro comentário)."""
    alvo = RAIZ / caminho
    if caminho.suffix.lower() not in TEXTO or alvo.stat().st_size > LIMITE_ARQUIVO:
        return ""
    try:
        linhas = alvo.read_text(encoding="utf-8", errors="ignore").splitlines()[:60]
    except OSError:
        return ""
    texto = "\n".join(linhas)
    ext = caminho.suffix.lower()
    achado = None
    if ext == ".md":
        achado = next((l.lstrip("# ").strip() for l in linhas if l.startswith("#")), None)
    elif ext == ".py":
        m = re.search(r'^\s*(?:"""|\'\'\')\s*(.+)', texto, re.M)
        achado = m.group(1) if m else next((l.lstrip("# ").strip() for l in linhas if l.startswith("# ") and len(l) > 6), None)
    elif ext == ".html":
        m = re.search(r"<title>(.*?)</title>", texto, re.S | re.I)
        achado = m.group(1).strip() if m else None
    elif ext == ".json":
        try:
            dados = json.loads((RAIZ / caminho).read_text(encoding="utf-8"))
            if isinstance(dados, dict):
                achado = "chaves: " + ", ".join(list(dados)[:6])
        except (ValueError, OSError):
            pass
    if not achado and ext in {".js", ".mjs", ".ts", ".tsx", ".jsx", ".css", ".sh", ".ps1", ".yml", ".yaml"}:
        m = re.search(r"^\s*(?://|/\*+|\*|#)\s*([^\s*/#].{8,})", texto, re.M)
        achado = m.group(1) if m else None
    if not achado:
        return ""
    achado = re.sub(r"\s+", " ", achado).strip(" */-")
    return achado[:110] + ("…" if len(achado) > 110 else "")


def tamanho(n: int) -> str:
    return f"{n / 1_048_576:.1f} MB" if n >= 1_048_576 else f"{n / 1024:.0f} KB" if n >= 1024 else f"{n} B"


def descricao_pasta(pasta: Path, lista: list[Path]) -> str:
    """O que a pasta guarda: título do README/CLAUDE/SKILL dela, senão os tipos de arquivo."""
    for nome in ("README.md", "CLAUDE.md", "SKILL.md", "AGENTS.md", "index.html"):
        p = pasta / nome
        if p in lista:
            d = descricao(p)
            if p.name == "SKILL.md":
                texto = (RAIZ / p).read_text(encoding="utf-8", errors="ignore")
                m = re.search(r"^description:\s*(.+)", texto, re.M)
                d = m.group(1).strip()[:110] if m else d
            if d:
                return d
    return ""


def linhas_arquivos(itens: list[Path], prefixo: str) -> list[str]:
    linhas = []
    tipos = Counter(p.suffix.lower() or "(sem extensão)" for p in itens)
    juntar = {ext for ext, n in tipos.items() if n > JUNTAR_ACIMA}
    for ext in sorted(juntar):
        grupo = [p for p in itens if (p.suffix.lower() or "(sem extensão)") == ext]
        total = sum((RAIZ / p).stat().st_size for p in grupo)
        linhas.append(f"- **{len(grupo)} arquivos {ext}** ({tamanho(total)}), por exemplo: " + ", ".join(p.name for p in grupo[:3]))
    for p in itens:
        if (p.suffix.lower() or "(sem extensão)") not in juntar:
            d = descricao(p)
            linhas.append(f"- [{p.name}]({prefixo}{p.as_posix()})" + (f" — {d}" if d else ""))
    return linhas


def escrever(arquivo: Path, texto: str) -> None:
    """Só grava se mudou (assim o Git não acusa mudança à toa a cada sessão)."""
    if not arquivo.exists() or arquivo.read_text(encoding="utf-8") != texto:
        arquivo.write_text(texto, encoding="utf-8")


def fazer_mapa(silencioso: bool = False) -> None:
    """Mapa curto (uma linha por pasta) + um mapa detalhado por pasta principal, aberto só quando precisa."""
    lista = [p for p in arquivos() if not p.as_posix().startswith("cerebro/Mapa/")]  # o mapa não conta a si mesmo
    nome = RAIZ.name
    PASTA.mkdir(exist_ok=True)
    detalhes = PASTA / "Mapa"
    detalhes.mkdir(exist_ok=True)
    feitos = set()
    linhas = [f"# Mapa de `{nome}`", "",
              "> Gerado sozinho por `python3 ferramentas/cerebro.py mapa` (também no começo de cada sessão do Claude).",
              "> **Claude: leia este mapa antes de abrir arquivos.** Abra só o mapa detalhado da pasta que interessa",
              "> (`cerebro/Mapa/<pasta>.md`) e, para achar um assunto, use `python3 ferramentas/cerebro.py buscar \"assunto\"`.", "",
              f"{len(lista)} arquivos.", ""]
    guias = [p for p in lista if p.name in ("CLAUDE.md", "README.md", "AGENTS.md") and ".claude" not in p.parts]
    if guias:
        linhas += ["## Comece por aqui", ""] + [f"- [{p.as_posix()}](../{p.as_posix()})" for p in guias] + [""]
    raiz = [p for p in lista if len(p.parts) == 1]
    if raiz:
        linhas += ["## Arquivos da raiz", ""] + linhas_arquivos(raiz, "../") + [""]
    linhas += ["## Pastas", ""]
    topo = sorted({p.parts[0] for p in lista if len(p.parts) > 1})
    for t in topo:
        dentro = [p for p in lista if p.parts[0] == t]
        sub = defaultdict(list)
        for p in dentro:
            sub[Path(*p.parts[:2]) if len(p.parts) > 2 else Path(t)].append(p)
        d = descricao_pasta(Path(t), dentro)
        linhas.append(f"- **[[Mapa/{t}|{t}/]]** ({len(dentro)} arquivos)" + (f" — {d}" if d else ""))
        subpastas = sorted(k for k in sub if k != Path(t))
        if len(subpastas) > 15:
            linhas.append(f"  - {len(subpastas)} subpastas: " + ", ".join(k.name for k in subpastas[:40]) + ("…" if len(subpastas) > 40 else ""))
        else:
            for k in subpastas:
                dk = descricao_pasta(k, sub[k])
                linhas.append(f"  - `{k.as_posix()}/` ({len(sub[k])})" + (f" — {dk}" if dk else ""))
        # mapa detalhado da pasta principal
        det = [f"# Mapa de `{t}/`", "", "Voltar para [[00 - Mapa]].", ""]
        por_pasta = defaultdict(list)
        for p in dentro:
            por_pasta[p.parent].append(p)
        for pasta in sorted(por_pasta, key=lambda p: (len(p.parts), str(p))):
            det.append(f"## {pasta.as_posix()}/")
            det += linhas_arquivos(por_pasta[pasta], "../../") + [""]
        escrever(detalhes / f"{t}.md", "\n".join(det))
        feitos.add(f"{t}.md")
    linhas.append("")
    if (PASTA / "Outros repositórios.md").exists():
        linhas += ["## Outros repositórios do dono", "", "Veja [[Outros repositórios]].", ""]
    escrever(MAPA, "\n".join(linhas))
    for velho in detalhes.glob("*.md"):
        if velho.name not in feitos:
            velho.unlink()
    if not silencioso:
        print(f"mapa atualizado: {MAPA.relative_to(RAIZ)} ({len(lista)} arquivos, {len(linhas)} linhas) + {len(topo)} mapas detalhados")


# ---------- busca (BM25 simples, sem API) ----------

def normalizar(texto: str) -> list[str]:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return [t for t in re.findall(r"[a-z0-9_]{2,}", texto)]


def limpar(linha: str) -> str:
    """Tira imagens embutidas (base64) e corta linhas gigantes (código minificado), que só pesam."""
    linha = re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]{40,}", "data:…", linha)
    return linha[:400]


def pedacos() -> list[dict]:
    """Divide os arquivos de texto em pedaços de ~30 linhas (guardados em cache até o arquivo mudar)."""
    CACHE.mkdir(exist_ok=True)
    arquivo_cache = CACHE / "pedacos.json"
    antigo = {}
    if arquivo_cache.exists():
        try:
            antigo = json.loads(arquivo_cache.read_text(encoding="utf-8"))
        except ValueError:
            antigo = {}
    novo = {}
    for p in arquivos():
        alvo = RAIZ / p
        if p.suffix.lower() not in TEXTO:
            continue
        info = alvo.stat()
        chave = p.as_posix()
        if info.st_size > LIMITE_BUSCA or chave.startswith(FORA_DA_BUSCA):
            continue
        if chave in antigo and antigo[chave]["mtime"] == info.st_mtime:
            novo[chave] = antigo[chave]
            continue
        linhas = [limpar(l) for l in alvo.read_text(encoding="utf-8", errors="ignore").splitlines()]
        partes = []
        for i in range(0, max(1, len(linhas)), 30):
            bloco = "\n".join(linhas[i:i + 30])
            if bloco.strip():
                partes.append({"linha": i + 1, "termos": Counter(normalizar(chave + " " + bloco))})
        novo[chave] = {"mtime": info.st_mtime, "partes": partes}
    arquivo_cache.write_text(json.dumps(novo), encoding="utf-8")
    return [{"arquivo": a, **parte} for a, dados in novo.items() for parte in dados["partes"]]


def buscar(consulta: str, quantos: int = 8) -> None:
    termos = normalizar(consulta)
    if not termos:
        print("escreva o que procurar, por exemplo: buscar \"capa do quiz\"")
        return
    docs = pedacos()
    n = len(docs) or 1
    media = sum(sum(d["termos"].values()) for d in docs) / n
    df = Counter(t for d in docs for t in set(d["termos"]) if t in termos)
    notas = []
    for d in docs:
        tamanho_doc = sum(d["termos"].values()) or 1
        nota = 0.0
        caminho = set(normalizar(d["arquivo"]))
        for t in termos:
            if t in caminho:  # o nome do arquivo ou da pasta tem a palavra: forte sinal de que é o lugar certo
                nota += 1.5 * math.log(1 + (n - df[t] + .5) / (df[t] + .5))
            f = d["termos"].get(t, 0)
            if f:
                idf = math.log(1 + (n - df[t] + .5) / (df[t] + .5))
                nota += idf * f * 2.2 / (f + 1.2 * (.25 + .75 * tamanho_doc / media))
        if nota:
            notas.append((nota, d))
    notas.sort(key=lambda x: -x[0])
    if not notas:
        print("nada encontrado")
        return
    por_arquivo, escolhidos = Counter(), []
    for nota, d in notas:  # no máximo 2 trechos por arquivo, para mostrar mais lugares diferentes
        if por_arquivo[d["arquivo"]] < 2:
            por_arquivo[d["arquivo"]] += 1
            escolhidos.append((nota, d))
        if len(escolhidos) == quantos:
            break
    for nota, d in escolhidos:
        linhas = [limpar(l) for l in (RAIZ / d["arquivo"]).read_text(encoding="utf-8", errors="ignore").splitlines()]
        trecho = linhas[d["linha"] - 1:d["linha"] + 29]
        melhor = max(range(len(trecho)), key=lambda i: sum(t in normalizar(trecho[i]) for t in termos)) if trecho else 0
        inicio = d["linha"] + max(0, melhor - 1)
        print(f"\n{d['arquivo']}:{inicio}  (relevância {nota:.1f})")
        for l in linhas[inicio - 1:inicio + 2]:
            print("   " + l[:160])


# ---------- diário ----------

def anotar(texto: str) -> None:
    agora = datetime.now(BRASILIA)
    pasta = PASTA / "Diário"
    pasta.mkdir(parents=True, exist_ok=True)
    nota = pasta / f"{agora:%Y-%m-%d}.md"
    if not nota.exists():
        nota.write_text(f"# Diário de {agora:%d/%m/%Y}\n\nVeja também [[00 - Mapa]].\n\n", encoding="utf-8")
    with nota.open("a", encoding="utf-8") as f:
        f.write(f"- **{agora:%H:%M}** {texto.strip()}\n")
    print(f"anotado em {nota.relative_to(RAIZ)}")


if __name__ == "__main__":
    os.chdir(RAIZ)
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    import signal
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # cortar a saída (| head) não é erro
    comando = sys.argv[1] if len(sys.argv) > 1 else "ajuda"
    resto = " ".join(a for a in sys.argv[2:] if not a.startswith("--"))
    if comando == "mapa":
        fazer_mapa("--silencioso" in sys.argv)
    elif comando == "buscar":
        buscar(resto)
    elif comando == "anotar":
        anotar(resto)
    else:
        print(__doc__)

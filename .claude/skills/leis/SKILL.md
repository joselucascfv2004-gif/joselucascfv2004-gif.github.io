---
name: leis
description: Consulta a legislação brasileira (Constituição, leis federais, decretos, medidas provisórias, atos de órgãos reguladores, súmulas e jurisprudência) no repositório público ctresb/leis, em Markdown. Use sempre que uma decisão, questão, aula, resumo ou texto do app depender de lei — questões de concurso e de Direito, política de privacidade (LGPD), regras de consumidor, propaganda, menores, direitos autorais — para conferir o texto vigente em vez de responder de memória.
---

# Legislação brasileira (ctresb/leis)

O repositório https://github.com/ctresb/leis (licença MIT) tem a Constituição Federal e cerca de 30 mil
normas federais, além de atos de agências, súmulas e tratados, convertidos das fontes oficiais para
Markdown. Os textos são informativos: **não substituem o Diário Oficial**. Antes de citar num conteúdo do
app, confira a fonte indicada no cabeçalho do arquivo.

## 1. Deixar o acervo disponível

A sessão na nuvem começa sem ele. Clone só as partes úteis (o repositório inteiro tem 1,2 milhão de
arquivos e ~13 GB; as partes abaixo, ~5,5 GB):

```bash
L=/home/user/ctresb/leis
if ! git -C "$L" rev-parse HEAD >/dev/null 2>&1; then
  mkdir -p /home/user/ctresb
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --no-checkout https://github.com/ctresb/leis "$L"
  git -C "$L" sparse-checkout set --no-cone '/*.md' '/LICENSE' '/federal/' '/jurisprudencia/' '/tratados/' '/reguladores/'
  git -C "$L" checkout
fi
```

Use um tempo limite longo (até 10 min). Se só precisar de uma lei ou da Constituição, troque a lista do
`sparse-checkout` por `'/constituicao.md' '/federal/leis-ordinarias/'` para ficar bem mais rápido.

## 2. Onde está cada coisa

```
constituicao.md                                   Constituição Federal de 1988 (texto vigente)
federal/leis-ordinarias/AAAA/lei-NUMERO-AAAA-MM-DD.md
federal/leis-complementares/AAAA/  federal/decretos/AAAA/dec-NUMERO-...  federal/decretos-lei/
federal/medidas-provisorias/  federal/emendas-constitucionais/  federal/resolucoes-senado/ ...
reguladores/<orgão>/<tipo>/        bcb, cvm, cmn, anvisa, contran, rfb, cne, conama, aneel ...
jurisprudencia/<tribunal>/         stf/sumulas, stf/sumulas-vinculantes, stj, tst ...
tratados/
```

Cada arquivo começa com um cabeçalho YAML: `titulo`, `tipo`, `numero`, `data`, `ementa`,
`revogada` (true/false), `versao_texto` (ex.: "compilada (texto vigente)") e `fonte` (link oficial).

## 3. Como procurar

```bash
L=/home/user/ctresb/leis
# por número (ex.: LGPD, Lei 13.709/2018)
ls $L/federal/leis-ordinarias/2018/ | grep 13709
# pelo assunto, olhando só as ementas (rápido)
grep -rl --include=*.md -m1 '^ementa: .*[Pp]roteção de [Dd]ados' $L/federal/leis-ordinarias | head
# um artigo específico dentro de uma lei
grep -n '^\*\*Art\. 14' $L/federal/leis-ordinarias/2018/lei-13709-2018-08-14.md
# Constituição: artigo 5º
grep -n -A3 '^\*\*Art\. 5º' $L/constituicao.md
```

Leis muito usadas: Constituição (`constituicao.md`); LGPD 13.709/2018; Marco Civil da Internet
12.965/2014; Código de Defesa do Consumidor 8.078/1990; ECA 8.069/1990; Direitos Autorais 9.610/1998;
Lei de Licitações 14.133/2021; Estatuto do Servidor 8.112/1990; Código Civil 10.406/2002;
Código Penal (Decreto-Lei 2.848/1940); CLT (Decreto-Lei 5.452/1943); Código Tributário 5.172/1966.

## 4. Regras ao usar

- Confira `revogada: false` e prefira o texto "compilado (vigente)". Se a lei foi alterada, cite a
  redação atual e, se importar, a lei que alterou (aparece em itálico no próprio artigo).
- Em questões do app (conteúdos/), cite a norma e o artigo na explicação (ex.: "art. 7º da Lei
  13.709/2018") e confira o número do artigo no arquivo antes de escrever.
- O acervo pode ter erro de conversão ou OCR: em dúvida, abra o link `fonte` do cabeçalho.
- Para direito estadual ou municipal, o repositório também tem `estaduais/UF/` e
  `municipais/UF/<município>/`; acrescente essas pastas ao `sparse-checkout` só quando precisar.
- Ao explicar algo ao dono do projeto, use linguagem simples e diga qual lei e artigo embasam a decisão.

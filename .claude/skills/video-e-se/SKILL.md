---
name: video-e-se
description: Faz vídeos curtos verticais do tipo "E se...?" (cenários impossíveis contados com ciência) do jeito que viraliza, em 7 passos - premissa de uma linha, checagem se já postaram, fonte para cada fato, mundo montado em código (2D no motor/ ou 3D no motor3d/ com Three.js, nunca vídeo de IA), revisão dos próprios quadros, render no computador e legenda para postar. Use quando o pedido for "faz um vídeo e se", "vídeo viral", "vídeo 3D", "vídeo pro TikTok/Shorts/Reels", "cenário impossível", ou ao criar roteiro para o motor de vídeos deste repositório.
---

# Vídeo "E se...?"

> Os motores (`motor/` e `motor3d/`) e os roteiros ficam no repositório **`joselucascfv2004-gif/videos-teste`**. Se
> esta skill estiver aberta em outro repositório, trabalhe dentro do `videos-teste` (clone ou peça para adicioná-lo).

Processo tirado do vídeo "How to make viral 3D videos with Claude Code" de @whatif.sim (TikTok, 30/10/2026: 56
vídeos, ~35 milhões de visualizações, sem custo além do plano do Claude). Junta com o motor 2D que já existe neste
repositório (`motor/`, narração + legenda karaokê) e o motor 3D novo (`motor3d/`).

## Os 7 passos

1. **Uma linha.** A premissa cabe numa frase de até 12 palavras, com um número que dá para imaginar:
   "E se toda a borracha sumisse por 5 segundos?". Bom tema: algo do dia a dia + uma regra da física que muda.
2. **Ninguém postou ainda?** Antes de escrever, procure (WebSearch: TikTok, YouTube, Reels) a mesma premissa. Se já
   existe e foi bem, mude o ângulo ("NYC tsunami: 3,1 mi, já feito → novo twist"). Anote o que achou.
3. **Uma fonte para cada fato.** Liste cada afirmação do roteiro com o link da fonte (NASA, USGS, IBGE, artigos,
   órgãos oficiais). Número que é estimativa vira "cerca de" e fica marcado como estimativa. Nada inventado. A
   lista de fontes vai no fim do roteiro e um resumo vai na legenda do post.
4. **O mundo é código, não vídeo de IA.** Nada de gerador de vídeo por IA: a cena é montada em código e sai igual
   toda vez.
   - **2D** (mais rápido): roteiro em `roteiros/*.json` e `./gerar.sh` (veja o `README.md`).
   - **3D**: copie `motor3d/cena.html`, troque `ROTEIRO`, o mundo e a função `desenhar(t)`. Tudo depende só do tempo
     `t`, com números "aleatórios" de semente fixa. Use objetos simples (caixas, cilindros) em grande quantidade
     (o vídeo de referência tinha 352 carros na Times Square) e um painel (HUD) com o número que muda.
5. **Revise os próprios quadros.** Gere prévias dos momentos-chave e olhe cada uma antes de renderizar tudo:
   `node motor3d/render3d.js motor3d/minha-cena.html saida/previa --previa 1,3,5,7`
   (2D: `node motor/render.js build/<nome> previa --previa 3,10,25`). Confira: câmera atravessando objeto, texto
   ilegível ou fora da área segura, quadro vazio, número errado, ritmo parado. Corrija e gere de novo.
6. **Render no computador.** `node motor3d/render3d.js motor3d/minha-cena.html saida/minha-cena.mp4` (1080×1920,
   30 fps, H.264). Na nuvem sem placa de vídeo: ~20 s de render por segundo de vídeo (8 s levaram 157 s).
   Narração e trilha: use `motor/preparar.py` (voz neural pt-BR, edge-tts) e junte com o ffmpeg.
7. **Post.** Gancho falado no primeiro segundo (a pergunta), a resposta em 3 a 5 etapas com o número na tela, e
   um final que puxa comentário ("E se fosse a gravidade?"). Legenda com a pergunta, 3 a 5 hashtags e "fontes
   nos comentários".

## Regras da tela vertical

- Área segura: deixe livres os 250 px de baixo (legenda e botões do TikTok) e os 150 px da direita (curtir,
  comentar). Textos importantes entre 120 px e 1600 px de altura.
- Etapa no topo ("A BORRACHA SUMIU"), pergunta grande no começo, painel com número embaixo. Letras grossas,
  contraste alto, no máximo 2 cores de destaque.
- Corte ou mudança de câmera a cada 2 a 4 segundos; nada parado por mais de 4 segundos.

## Arquivos

- `motor3d/cena.html`: cena de exemplo (cidade, 120 carros, pneus somem aos 2,5 s e voltam aos 7,5 s).
- `motor3d/render3d.js`: render quadro a quadro com Playwright + ffmpeg; `--previa` para fotos; `--fps`.
- `motor3d/vendor/three.module.min.js`: Three.js 0.169.0 (licença MIT em `LICENSE-three.txt`).
- `motor/`: motor 2D com narração e legenda karaokê.

Nunca publique no TikTok, YouTube ou Instagram pelo dono: entregue o MP4, a legenda e as fontes para ele postar.

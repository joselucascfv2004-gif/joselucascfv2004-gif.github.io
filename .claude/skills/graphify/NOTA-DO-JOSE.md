# Nota (31/10/2026)
Skill graphify (github.com/safishamsi/graphify, Apache 2.0 / MIT; pacote do PyPI `graphifyy`), instalada a pedido do
José a partir do carrossel "42 coisas pra instalar no Claude". Monta o mapa de ligações do projeto (graphify-out/:
página interativa, GRAPH_REPORT.md e graph.json). Na nuvem o pacote não vem instalado: o passo 1 da skill instala com
`pip install graphifyy`. Regras para o José: só o modo gratuito (nada de GEMINI_API_KEY, Neo4j ou serviços pagos);
a leitura de código é local e grátis, mas documentos, imagens e vídeos passam pelo próprio Claude e gastam o limite —
em pastas grandes (questões do app Estudos, dados do SUI) rode só no código (ex.: `app/src`, `src/`). A pasta
`graphify-out/` não vai para o Git. Complementa o "cérebro" do repositório (ferramentas/cerebro.py), não substitui.

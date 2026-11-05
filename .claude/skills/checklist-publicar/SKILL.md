---
name: checklist-publicar
description: Revisão antes de publicar ou atualizar um site, app ou sistema (cardápio online, painel, app de celular, sistema interno, página de vendas) em quatro listas - segurança, gastos e limites de uso, velocidade e parte jurídica (LGPD, termos, cookies, reembolso) - com um relatório em português simples do que passou, do que falhou e de como corrigir. Use quando o pedido for "vou publicar", "posso colocar no ar?", "revisa antes de lançar", "está seguro?", "pode dar conta alta?", "o site está lento", "preciso de termos de uso/política de privacidade", ou antes de qualquer deploy feito a pedido do dono.
license: MIT (escrita para o José, 05/11/2026, a partir de dicas de vídeos do TikTok de afcodehub, davidossite e mr_leoandrade)
---

# Checklist antes de publicar

Uma revisão rápida e honesta antes de colocar algo no ar. Não substitui um advogado nem uma auditoria
profissional; serve para não esquecer o básico. Responda sempre em português simples.

## Como usar

1. Descubra o que é (site estático, app com login, app com pagamento, sistema com dados pessoais, app que chama
   uma IA paga) e onde roda (Netlify, Firebase, Vercel, artefato, loja de apps).
2. Leia só os arquivos que importam (configuração, regras do banco, chamadas de API, formulários). Busque antes
   de ler (`grep` por "key", "secret", "token", "apiKey", "password", "fetch(").
3. Passe pelas 4 listas abaixo, pulando o que não se aplica (diga que pulou e por quê).
4. Entregue uma tabela: **item | ok / falha / não se aplica | o que fazer** e, no topo, as 3 falhas mais graves.
   Corrija só o que o dono pedir. Nunca publique sem ele pedir.

## 1. Segurança

- **Nenhuma chave secreta no front-end** (HTML/JS que vai para o navegador): chaves de IA, banco, pagamento e
  e-mail ficam no servidor ou em variáveis de ambiente. Chave pública de propósito (ex.: config web do Firebase)
  pode aparecer, mas precisa de regras e restrição de domínio.
- **Segredos fora do Git**: `.env` no `.gitignore`; procure chaves no histórico (`git log -p | grep -i key`).
  Se uma chave vazou, **trocar a chave** (apagar do código não basta).
- **Regras do banco fechadas** (Firestore/Supabase): ninguém lê nem escreve o que não é dele; teste as regras.
- **Login protegido**: limite de tentativas, senha nunca guardada em texto, sessão que expira.
- **Validar dados nos dois lados** (tela e servidor); nada de montar consulta juntando texto do usuário
  (injeção de SQL); formulários que mudam dados com proteção contra CSRF quando houver sessão por cookie.
- **Uploads** com tipo e tamanho máximos; nunca executar o arquivo enviado.
- **HTTPS sempre**; nenhum arquivo sensível exposto (backup, `.env`, planilha, PDF com dados pessoais).
- **Dependências atualizadas** e sem pacote abandonado com falha conhecida.

## 2. Gastos e limites de uso (para a conta não explodir)

- Toda chamada a serviço pago (IA, SMS, e-mail, mapas) passa pelo **servidor**, nunca direto do navegador.
- **Limite por usuário e por IP** (ex.: X pedidos por minuto) e **cota diária** por conta.
- **Alerta de orçamento** no painel do serviço (Google Cloud/Firebase, OpenAI, Vercel) **antes** de estourar, e
  um jeito rápido de **desligar** o recurso caro ("botão de pânico": variável ou regra que bloqueia).
- Tamanho máximo de upload, de texto enviado à IA e de resposta; cache do que se repete.
- Nada de laço que chama a API sozinho (ex.: `useEffect` sem dependências certas chamando a cada render).
- Plano grátis do serviço: saiba o limite e o que acontece ao passar (cobra ou para?).

## 3. Velocidade

- **Os 4 estados** em toda tela que carrega dados: carregando (esqueleto), vazia, erro (com "Tentar de novo")
  e cheia. Botão de enviar/pagar trava no primeiro toque.
- Imagens em **WebP/AVIF**, no tamanho em que aparecem, com `loading="lazy"` abaixo da dobra.
- Listas longas com **paginação** ou lista virtualizada; busca com atraso curto (debounce).
- Nada de baixar o banco inteiro para mostrar 10 itens; cache do que não muda.
- **Teste em rede lenta** (DevTools → 3G lento) e num celular simples. Metas: primeira tela útil em até ~2,5 s;
  resposta a toque em até 0,1 s; acima de 1 s mostre carregando; acima de 10 s mostre progresso.

## 4. Parte jurídica (Brasil)

- **Política de privacidade** (LGPD): quais dados pessoais coleta, para quê, com quem compartilha, por quanto
  tempo guarda e como a pessoa pede para ver, corrigir ou apagar (contato do responsável).
- Coletar **só o necessário**; dado sensível (saúde, CPF, documentos) com cuidado extra.
- **Termos de uso** se houver conta, venda ou conteúdo do usuário.
- **Cookies e rastreamento** (Analytics, Pixel): avisar e permitir recusar os não essenciais.
- **Venda online** (Código de Defesa do Consumidor): preço total claro, frete e taxas antes de pagar, direito de
  arrependimento de 7 dias em compra pela internet quando se aplica, contato e CNPJ/CPF do vendedor visíveis.
- **Licenças**: imagens, fontes, músicas e código de terceiros com licença que permite o uso; crédito quando a
  licença pede. Nada de marca ou imagem de outra empresa como se fosse sua.
- Em dúvida jurídica real, diga claramente que é bom consultar um advogado.

## Projetos do dono (lembretes)

- Degust (cardápio e painel, Firebase): regras do Firestore no arquivo `Degust/firebase/firestore.rules` e
  testadas no emulador; chave web do Firebase restrita por domínio.
- SUI (prefeitura): dados pessoais de servidores e fornecedores; nada de compartilhar o artefato como público.
- App Estudos (Expo): nada de chave paga no app; atualização por EAS Update só quando o dono pedir.

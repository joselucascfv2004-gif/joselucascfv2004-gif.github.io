---
name: psicologia-ux
description: Aplica seis princípios de psicologia do comportamento ao desenho de telas e fluxos (padrões inteligentes, progresso que não começa do zero, dar valor antes de pedir, deixar a pessoa montar algo, mostrar o que se perde, e contraste de preço), com regras de ética para não virar manipulação. Use ao desenhar ou revisar cadastro, primeiro uso (onboarding), formulários, telas de oferta, planos e preços, carrinho e checkout, metas e progresso, ou quando o pedido for "aumentar conversão", "fazer o usuário voltar", "menos gente desistindo", "deixar mais viciante" ou "por que ninguém termina o cadastro".
---

# Psicologia de UX

Tirado do vídeo "The UX Psychology Behind Apps People Can't Stop Using" de @codevibes_1 (TikTok, 30/10/2026).
A ideia: as pessoas não decidem de forma lógica. A tela certa diminui o esforço e dá motivo para continuar.
Use junto com a skill `revisar-tela` (o visual) e respeite as regras do `CLAUDE.md` de cada projeto.

## Os seis princípios

### 1. Padrões inteligentes (menos decisões)
Cada campo vazio é uma decisão, e decisões demais cansam e fazem a pessoa desistir. No estudo das geleias (Iyengar e
Lepper, 2000), com 24 sabores à mostra só 3% compraram; com 6 sabores, 30%.
**Faça:** deixe já escolhida a opção mais comum (tamanho mais pedido, data mais próxima, quantidade usual) e mostre
o resultado no botão ("Ver 12 mesas livres"). A pessoa passa de "preencher do zero" para "conferir e ajustar".

### 2. Gradiente de meta (nunca começar do zero)
Quanto mais perto do fim a pessoa se sente, mais rápido ela anda. No lava-jato (Nunes e Drèze, 2006), um cartão de
10 carimbos com 2 já carimbados foi completado por quase o dobro de gente que o cartão de 8 vazios, com o mesmo
número de lavagens faltando.
**Faça:** conte o que a pessoa já fez como primeiro passo ("Conta criada" já marcado, barra em 20%), mostre onde
ela está e quanto falta.

### 3. Reciprocidade (dar antes de pedir)
Pedir cadastro antes de entregar qualquer coisa ("crie uma conta para ver o resultado") parece sequestro. Quem
recebe algo útil primeiro sente vontade de retribuir (Robert Cialdini).
**Faça:** entregue um pedaço real do valor antes (resultado parcial, demonstração funcionando, primeira aula) e só
depois convide ("Quer o relatório completo? Salve aqui").

### 4. Efeito IKEA e posse (deixar a pessoa montar)
O que a pessoa montou ou escolheu vale mais para ela, e sair passa a ser "abandonar algo meu". O Duolingo deixa
escolher idioma, meta e fazer a primeira lição antes de pedir a conta.
**Faça:** antes do cadastro, deixe a pessoa escolher e montar (nome, objetivo, cores, primeiro pedido) e chame o
botão de "Continuar" em vez de "Cadastrar".

### 5. Aversão à perda (mostrar o que se perde)
Perder dói mais do que ganhar a mesma coisa alegra (Kahneman e Tversky). "Ganhe mais espaço" pesa menos que
"estes 3 arquivos seus vão ser apagados em 3 dias".
**Faça:** quando a perda é **real**, mostre o que é da pessoa e está em risco (a ofensiva de 12 dias, o pedido no
carrinho, o progresso da semana), com o nome das coisas.

### 6. Contraste (o primeiro número vira a régua)
O mesmo valor parece caro sozinho e pequeno ao lado de um valor maior. R$ 50 numa tela própria assusta; R$ 50 logo
abaixo de um notebook de R$ 1.900 ("só 2,6%") quase passa despercebido.
**Faça:** nunca mostre um custo isolado; escolha o que a pessoa vê antes (o preço do item, o plano maior, o total
economizado) e mostre a diferença em relação a ele.

## Ética: o que não fazer

O dono vende para pequenos negócios e tem um app de estudos usado por estudantes. Confiança vale mais que um clique.
- **Nada de mentira:** sem contador falso ("só hoje!" que nunca acaba), sem estoque inventado, sem avaliação ou número
  que não existe, sem perda que não vai acontecer.
- **Nada de culpa no botão de recusar** (o vídeo usa "I'll risk it"): o "não, obrigado" tem que ser claro e neutro.
- **Padrão a favor da pessoa:** nunca deixe marcado por padrão algo que custa dinheiro a mais, assinatura, seguro ou
  compartilhamento de dados (no Brasil, o Código de Defesa do Consumidor e a LGPD; use a skill `leis` se precisar).
- **Progresso honesto:** o "já começou" tem que contar algo que a pessoa fez de verdade.
- **Sair fácil:** cancelar, apagar conta ou desligar notificação nunca fica escondido.

## Onde isso entra nos projetos do José

| Projeto | Ideias |
|---|---|
| App Estudos | A ofensiva e a meta já usam perda e progresso: mostre o que está em jogo de verdade ("sua ofensiva de 12 dias"). No primeiro uso, comece com o teste de nível ou a 1ª aula antes de qualquer pedido. Plano de hoje nunca em 0% se a pessoa já respondeu algo hoje. |
| Cardápios (Degust e modelos) | Tamanho mais pedido já marcado; borda e adicionais mostrados como "+ R$ 8" ao lado do preço da pizza; sacola mostrando o que falta para o frete grátis ou para o pedido mínimo. |
| Sistema para Clientes | Na abordagem do lead, mostre o cardápio dele pronto (demonstração com o nome e as fotos dele) antes de falar de preço. |
| SUI (prefeitura) | Filtros já no mais usado (mês atual, conta mais comum); progresso da conferência ("32 de 41 lançamentos conferidos"). |

## Como entregar

1. Diga ao dono qual princípio está usando, em português simples, e por que ajuda a pessoa.
2. Mantenha todos os botões e opções que já existem (regra do dono); mude a ordem, o texto e o que vem marcado.
3. Mostre antes e depois com as fotos da skill `revisar-tela`.
4. Quando der para medir (pedidos, cadastros, lições terminadas), sugira comparar antes e depois em vez de confiar
   só na teoria.

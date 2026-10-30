# Formulários

Cadastro, login, checkout, configurações, filtros. Use junto com a lista geral do `SKILL.md`.

- **Rótulo em cima do campo**, sempre visível. Exemplo dentro do campo (placeholder) não substitui o
  rótulo, porque some quando a pessoa digita.
- **Uma coluna** no celular. Campos curtos lado a lado só quando andam juntos (CEP e número; validade e CVV).
- **Largura do campo indica o tamanho da resposta** (UF curto, endereço comprido).
- **Teclado certo no celular:** `type="email"`, `type="tel"`, `inputmode="numeric"` (CPF, CEP, valores),
  `autocomplete` (nome, e-mail, endereço) para o navegador preencher sozinho.
- **Marque o opcional**, não o obrigatório, quando a maioria é obrigatória (ou o contrário, o que for menor).
- **Erro perto do campo**, em vermelho com ícone, dizendo como resolver ("CPF com 11 números"), e só
  depois que a pessoa sair do campo ou tentar enviar. O texto digitado nunca se perde.
- **Agrupe** em blocos com título curto (1. Seus dados, 2. Entrega, 3. Pagamento) quando o formulário
  for longo; mostre em que passo a pessoa está.
- **Botão de envio** com o resultado ("Criar conta", "Ir para o pagamento"), largo no celular, e
  desabilitado com aviso do que falta, ou mostrando o que falta ao tocar.
- **Depois de enviar:** carregando no próprio botão; sucesso diz o que acontece agora.
- **Máscaras** (CPF, telefone, data, dinheiro) ajudam, mas aceite o que a pessoa colar (com ou sem pontos).
- Caixas de marcar e opções com área de toque grande (a linha inteira clicável).

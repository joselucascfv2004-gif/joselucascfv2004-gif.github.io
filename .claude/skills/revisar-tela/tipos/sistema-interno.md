# Sistema interno, painel e tabelas

Telas usadas o dia todo por funcionários (conferência bancária, suplementação, CRM, painel de pedidos,
relatórios). Rapidez, clareza e poucos erros valem mais que enfeite. Use junto com a lista geral do
`SKILL.md` e fotografe também em **1280 px** de largura.

## Tabelas e listas

- **Números alinhados à direita**, com algarismos do mesmo tamanho (`font-variant-numeric: tabular-nums`)
  e o mesmo formato (R$ 1.234,56; datas dd/mm/aaaa). Texto alinhado à esquerda. Cabeçalho alinhado como a
  coluna.
- **Cabeçalho fixo** ao rolar tabelas longas; primeira coluna fixa se a tabela rolar para o lado.
- **Linhas fáceis de seguir:** divisória clara ou faixas alternadas suaves; destaque ao passar o mouse.
  Altura de linha confortável (mín. ~36 px), sem apertar para caber mais.
- **Totais** destacados (negrito, linha acima), no fim ou no topo, e batendo com a soma das linhas.
- **Cor só com significado:** vermelho = problema, verde = ok, amarelo = atenção, roxo/azul = revisar.
  Sempre com texto ou ícone junto (quem não distingue cores também entende) e uma legenda.
- **Lista vazia** explica o porquê e o próximo passo ("Nenhum extrato ainda. Adicione o PDF do banco.").
- Muitas colunas: esconda as raras atrás de um "mais detalhes" ou de uma linha que abre.

## Filtros, busca e ações

- Filtros e busca **acima** do que filtram, na ordem de uso; mostre quantos itens sobraram e um
  "Limpar filtros".
- Ação principal da tela em destaque, uma só. Ações perigosas (excluir, sobrescrever, limpar lista)
  afastadas, em vermelho, com confirmação que diz o que vai acontecer.
- Botões com verbo claro ("Conferir extratos", "Gerar PDF"), não "OK" ou "Enviar".
- Ação demorada mostra progresso e permite cancelar.

## Painel com números (dashboard)

- No máximo 4 a 6 números grandes no topo, cada um com rótulo e comparação ("+12% sobre o mês passado").
- Gráfico só quando a forma importa (tendência, comparação); senão, tabela.
- O que precisa de ação ("3 pendências", "5 a revisar") aparece primeiro, com link direto para resolver.

## Navegação

- Abas e menus com nomes que o usuário usa (os nomes que ele pediu valem mais que os técnicos).
- A aba atual é bem visível; o endereço (#hash) leva direto à aba, para dar F5 sem perder o lugar.
- Avisos e mensagens perto de onde a pessoa está olhando, não só no topo da página.

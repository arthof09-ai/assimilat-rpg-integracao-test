# Guia operacional de consulta do Sistema Universal de PA para qualquer Comestre e CRAFT

**MESTRE-SIDE — versão de TEST consultivo R05.** Não é nova regra, não cria calculador e não instala runtime.

## Pergunta central

Quando o Mestre disser "Qual o PA deste item?", o Comestre deve **ler a ficha viva no Notion Mestre** e, sem exigir que o Mestre prepare JSON, identificar:

- **Identidade da página e proveniência:** UUID/URL, data observada, Catálogo Itens Mestre ou item pessoal do espelho. Não misturar registros parecidos nem migrar dados para Party.
- **Natureza do pedido:** CÁLCULO DE ITEM NOVO versus CONSULTA DE ITEM EXISTENTE. Existente conserva custo histórico e unidades (PA/dia, PA/ativação, PA/turno, carga ou capacidade); sem ordem competente, nunca reprecificar silenciosamente.
- **RI independente de RE:** classificação do ITEM e de CADA EFEITO com fonte mecânica; rank no nome do pergaminho não vale automaticamente como RE E0. Se não documentado, `PENDENTE` e pesquisa dirigida, sem chute.
- **Mecânica de cada habilidade:** nome exato, passiva/ativa, alcance, magnitude, alvo, condição, duração, recorrência, frequência e usos no cenário. Separar +atributo, +dano por ataque de dano por turno, CA física de CA mágica, PA capacidade de débito PA.
- **Entrada para fornecedor existente:** adaptador CRAFT R27 consulta R26, que aplica pisos RI, tarifas RE, bônus aceitos e arredondamento histórico vigente. Não copiar fórmulas para motor paralelo; usar o fornecedor real e seus retornos.
- **Gate de entrada:** R02 valida habilidade duplicada e identificadores de usos; R03 barra piso isolado sem efeito descrito; R04 vincula recibo ao item/receita em TEST. No ambiente CRAFT real, a instalação desses complementos depende de autorização, TEE e NAC-PASS específicos.
- **Resultado em conversa:** mostrar `PA/dia`, `PA/ativação`, `cenário de X usos`, `custo total`, `valores históricos preservados`, `rank/evidência`, `pendências` e `ESTADO` E3/INDETERMINADO/E0 VERIFICADO quando houver decisão real. `null` nunca é zero.
- **Produção:** custo de PA calculável **não** comprova eficácia mágica, transferência, estoque, RC5, projeto produtivo ou permissão de escrita. F5/C19 e writer/fencing são gates distintos.

### Respostas-modelo ligadas a evidências reais

**Amplificador de Atributo:** "A ficha Mestre apresenta +3 em um atributo e 15 PA/dia. Se o item é Bronze conforme decisão do Mestre e o bônus for aplicado em exatamente um atributo escolhido, as seis possibilidades simuladas retornaram igualmente 15 PA/dia no R27→R26. Isso **confere o valor numérico prospectivo em TEST**, mas não altera o histórico nem homologa E0 ou a classificação no texto da página." 

**Bota Caminho Veloz:** "O documento existente diz 18 PA/dia e Velocidade Sobrenatural 5 PA por ativação. Registro ambos sem converter um em outro. Sem RI/RE completos, o total prospectivo é PENDENTE. Posso informar o histórico, não substituir custo." 

**Toque Chocante:** "A ficha original informa preço 4.100.000 MED e rank nominal Ouro da técnica. A mecânica só está na imagem, não examinada. Não existe custo PA demonstrado; um piso Ouro aritmético não representa custo aprovado dessa técnica." 

**Armadura de Zephyr:** "Há dois registros pessoais distintos com unidades 90/dia e 90/turno; devo primeiro resolver qual é a ficha/versão competente para o pedido, sem fusão ou correção automática. Não usar este conflito como prova de falha da fórmula do PA." 

**Anel da Alma:** "Concede +50 PA de capacidade/recurso. Isso não significa que consuma 50 PA/dia. O custo energético do item não está determinado por esta frase." 

### Fluxo de decisão compacto

`FONTE FÍSICA → IDENTIDADE + HISTÓRICO? → EXTRAIR RI/RE + EFEITOS → VALIDAR CONFIANÇA/DUPLICIDADES/UNIDADES → CHAMAR R27→R26 → GATE CONSULTIVO → RESULTADO NUMÉRICO E3 ou PENDENTE → REGISTRAR → NAC-PASS PROPORCIONAL`.

Se o cálculo de PA ficar `PENDENTE` por uma habilidade específica, prosseguir com outras tarefas seguras do CRAFT; não travar toda a operação por uma classificação isolada. Se houver conflito de autoridade ou necessidade de escrever, respeitar NAC-NORM-01/NAC-CONT-03/STOP e o gate competente.

**Retomada:** se o chat travar, recuperar o checkpoint R05 e o pacote na Biblioteca Mestre; não repetir 560 testes R04 sem alteração técnica. Próxima Rodada 6/10, restando cinco após encerrar a R05.
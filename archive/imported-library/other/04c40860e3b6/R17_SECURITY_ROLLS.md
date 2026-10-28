# R17 — análise do registrador de rolagens

## Propriedades exercitadas em laboratório
1. Um `roll_id` inclui evento e propósito/benefício; a tabela de dados e quantidade do contrato estão seladas.
2. Entropia de sistema operacional `secrets.token_bytes(32)` é persistida por gravador local antes de revelar qualquer resultado (`COMMITTED_HIDDEN`).
3. O commit SHA-256 vincula seed e contrato por `LEVELUP-R17-COMMIT-V1`.
4. A derivação utiliza SHA-256 com separação de domínio, counter e amostragem de rejeição para evitar viés de `mod` em dados `d4` até `d60`.
5. O recibo revela seed e valores; `RollLedger.verify` recompõe os dados exatos, commitment e SHA do recibo. Interrupção entre etapas usa o seed já salvo.
6. `fcntl.flock` serializa operadores locais cooperantes; `fsync` mais `os.replace` cria checkpoint durável local de cada etapa.
7. Dois pedidos com o mesmo ID e mesmos termos retornam o mesmo recibo; alteração de termo ou evento gera conflito e exige intervenção.
8. Para FF o ID é o MARCO, não o tipo de benefício: trocar de tipo após rolar não abre segunda chance.

## O que NÃO se comprova
- O hash é de consistência **local**. Se um operador malicioso controlar os arquivos e escolher/regravar a seed, pode criar registros internos consistentes; sem ancoragem de compromisso independente, não há prova criptográfica de imparcialidade contra esse operador.
- Nenhum runtime externo, O Primeiro, player ou serviço Notion foi usado como testemunha do compromisso.
- As rolagens **são simulações locais**, ainda não recebem liberação operacional ou certificação independente NAC-NORM/NAC-PASS.
- Não há garantia de `fsync` ou `flock` em plataforma Notion ou em múltiplas máquinas. A semântica do Notion exige mecanismo próprio e fencing técnico comprovado.
- Não são permitidos bônus/rerolls não definidos na regra. Dados físicos externos exigem importação com recibo de origem verificável, ainda não implementada.

## Gates futuros
Definir fonte autorizada de entropia, compromisso visível ao jogador ou testemunha externa, marcação de ordem de eventos, verificação independente, apresentação segura do resultado e recuperação entre processos. Depois testar integração sem mensagens Master-only no canal player.

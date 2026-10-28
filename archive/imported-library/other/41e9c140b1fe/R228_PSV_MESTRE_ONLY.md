# R228 — Flecha de Trava × movimento nativo × expiração — PSV MESTRE-ONLY

**Operação:** OP-VLAB-FUSION-SANDBOX-01. **Data-base:** 21/10/2026. **Executante lógico:** CM-000006 / MESTRE-SIDE / TEST. **Produção, Party, O Primeiro e fichas originais:** HOLD/NO-WRITE.

## Evidência nova e execução

**Fonte principal reaberta:** Sikong Iskiel — Arqueira da Cornija, [página Mestre-side](https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966). Habilidade Flecha de Trava ON5: Ação Padrão, 55 PA, um inimigo até 65 m, 8d10+12 perfurante, FF+21 quando elegível, Luta DES contra CA, −6 m de deslocamento após acerto até o final do turno seguinte do alvo, sem Imobilização. **NPC ainda é proposta Mestre-side.** Varok tem CA83, RD35 e Vida734 em fixture histórica. Sua velocidade natural oficial NÃO estava demonstrada; adotamos **12 m estritamente em cena TEST** e declaramos caminho aberto. Não usar a posição 1,5 m do ensaio para deduzir bloco universal.

**ANTES:** R226–R227 comprovaram redução de velocidade na janela de um item semicanônico, porém sem publicar movimento efetivo durante a penalidade. **DEPOIS:** R228 chama `apply_weapon_attack`, `apply_flecha_trava_post_hit`, `begin_source_turn`, `move_via_verified_path`, `end_source_turn` e `expire_flecha_trava_next_turn` com R18 persistente na mesma coorte.

**Execuções novas:** 2 seeds, ambas com 3 commits R18 = **6 commits e 21 eventos nativos**. Ambas encerraram por **censura**, sem KO, não constituem dois duelos terminais de campanha. Quatro ataques físicos nativos e quatro movimentos nativos: dois de 5 m durante o primeiro turno do alvo e dois de 7 m no turno de observação seguinte.

- **R228_HIT S22871003:** Iskiel acertou; Varok perdeu 26 PV físicos sob RD35, ficou temporariamente com limite de 6 m na velocidade TEST de 12 m e moveu legitimamente 5 m. No fim desse turno, a habilidade expirou e o próximo movimento de 7 m ocorreu com limite 12 m. Iskiel gastou 55 PA, uma vez.
- **R228_NEG_CRIT_MISS S22871004:** ataque teve falha crítica negativa, e o motor LAB tratou como erro; não houve dano nem lentidão, mas a técnica executada consumiu 55 PA; Varok moveu com velocidade TEST integral. **A consequência de falha crítica negativa é LAB-only, não uma decisão normativa promovida.**
- **Controle negativo adicional:** um deslocamento de 7 m enquanto o redutor deixava velocidade TEST 6 m foi rejeitado **antes de qualquer alteração** da cópia em memória. Não houve journal de efeito inválido.

**Auditoria independente READ-ONLY:** dois bancos admitidos, 6 commits, 21 eventos, hashes de linhas e final reconstituídos, ataque, dano/RD, Vida, PA, turno, movimento real e expiração comprovados. Quatro clones adulterados com hashes forjados/reconstruídos foram rejeitados por semântica (PA grátis, posição falsificada, efeito expirado indevidamente, canonização falsificada).

**Quarentena preservada:** o primeiro RUN-ID R228_HIT_S22871001 falhou por identificador de comando R18 sem prefixo `LAB-CMD-`, **antes de commit**. Não houve retry desse RUN-ID. Pré-registro v1 e banco inválido foram preservados; o pre-registro v2 atribuiu seeds não utilizadas 22871003/04 e corrigiu somente o prefixo do comando.

## Limites e governança

O evento R228 comprova **integração TEST de uma habilidade de contenção leve**, não Controle de Besta e não regra mundial de velocidade ou adjacência. Entre os turnos de observação do alvo, não foi executado turno ofensivo intermediário de Iskiel; portanto, isso é uma **janela multietapas dirigida**, não um scheduler bilateral integral. O dano veio de habilidade de Iskiel e fonte proposta; a velocidade de Varok e a geometria são explícitas fixtures TEST.

**NAC-PASS local:** PASS TEST condicional. **Canonização:** HOLD. **17 contratos terminais:** 0 homologados. **Matriz R91:** 0/1.875 células oficiais homologadas. **Não reexecutar nenhuma seed R228 nem histórica.**

**LAST-VERIFIED-UNIT:** R228 readback/extração fria quando a publicação for concluída. **FIRST-PENDING:** R229 candidato, preflight obrigatório. **NEXT-5:** escolher velocidade realmente fonte-provada; reforçar scheduler bilateral com turnos intercalados; consolidar arredondamento para baixo pela rota NAC-NORM; validar um Controle de Besta fonte-completo ou Bateria E P4; enviar recibos novos ao DMG pela roteação legítima sem duplicar IBX-126.

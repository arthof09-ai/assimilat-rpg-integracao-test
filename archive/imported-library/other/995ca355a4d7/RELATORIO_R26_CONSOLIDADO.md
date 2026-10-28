# Relatório científico R26 — CM-000001 / OP-DMG-CORPUS-EMP-01

**AS-OF:** 2026-10-13, Mestre-side; R26 documental + preflight fail-closed, **sem execução do VLAB**.

## PSV / ANTES → DEPOIS

- Pai R25 SHA256 `b3e90a31f5df1ce16bbe4dfdc3bbd17d4d8de1eb6d661f90fb21a843706896b1`: **VALIDADO FISICAMENTE**, 16 ZIP entries, CRC PASS, hashes 15/15, R24 original integral e oráculo R13 byte-idêntico.
- 1/18 (5,56%) → **1/18 (5,56%)**; 9 PARTIAL, 6 BLOCKED, 2 NOT_TESTED inalterados. Dois STRICT: 0/2→0/2. CSV I0003 originais: 0/9→0/9. DEC-B11/B12: 0/5→0/5.
- R26 ações oficiais: **0 alterações em regras/fichas/Party/O Primeiro/VLAB/DMG-RANK**. R26 documentação em sandbox; encaminhamento ao CM-000006 somente como pedido de triagem, caso a Inbox seja efetivamente escrita e readback verificado. Não confundir PASS documental e gate de produção.

## I. Ação bônus

**Evidência inédita:** texto das Manoplas do RPG corresponde muito de perto a *Gauntlets of Flaming Fury* de D&D (fonte Portões de Baldur/Descent into Avernus): ambos têm duas manoplas, bônus, arma mágica, chamas mágicas, duram até soltar/guardar, nova ativação ao amanhecer. A versão externa `+1d6 Fogo` foi adaptada na Assimilação para `+1d8+2`, com 13PA/dia. A ocorrência externa prova linhagem textual provável, NÃO autorização de economia de D&D. Novo `DEC-BONUS-JAKU-01`, alternativas N1 padrão (menor ruptura, recomendada para revisão, não aprovada), N2 movimento, N3 livre, N4 categoria própria, N5 HOLD.

**Status legal:** manoplas como acessórios listados e passivo de tornar arma não mágica em mágica são documentados. Ativação de chamas = `UNMAPPED_ACTION`, HOLD. Nenhuma definição/errata específica do Mestre encontrada nas buscas dirigidas e nas versões vigente/histórica de combate consultadas.

## II. Infusão / sobreposição

- Texto original: `+2d8+2 dano espiritual flamejante`; não há definição primária independente pesquisada que converta automaticamente em Fogo canônico ou bypass espiritual.
- Manoplas: `+1d8+2 Fogo mágico` textual, se ativadas por ação legal. A descrição do item permite chamas numa arma corpo-a-corpo, não exige que a arma seja não mágica para a segunda propriedade; a primeira cláusula apenas concede status mágico a arma não mágica segurada.
- `2d8 + 2d8 + 1d8 = 5d8` confere com impresso Jaku, mas não prova origem de `1d6+33`; soma fixa explícita dos itens é +6, residual `1d6+27` **sem fonte individualizada**. Não presumir que a infusão seja simultaneamente Fogo e espiritual de modo a dobrar pool ou bypass.
- Fraqueza Dragão elegível somente ao componente realmente Fogo e magia; ao menos `1d8` Manoplas é elegível se legalmente ativo, gerando **+3d8** (DME 13,5) uma vez pelo maior dado elemental, sem bonus extra por contar duas fontes de d8. B15 continua PARTIAL até recibo.

## III. CA, RD e impossibilidade de ataque certificado

Dragão Ouro1, CA literal39 Vida523 DES28 CON33, fraqueza a ataques mágicos Fogo. Criação de Besta formula 10+DES+CON/5=44,6 antes do arredondamento; nenhuma retificação canônica da CA39 efetuada. Ataque de Jaku `2d6+30` (máximo42): versus CA39, supera em 6/36 pares de dados; versus CA44,6 supera em 0/36. Adotar CA normativa silenciosamente eliminaria o acerto, portanto esta decisão é um gate material de legalidade. RD Ouro normal 25 / Ouro Titã45, flag de cena desconhecida; ordem de aplicar por ação, por componente e resistência específica ainda não foi demonstrada. Nenhum HP após golpe.

## IV. VLAB / integração

Biblioteca contém readback técnico R14: serviço experimental HTTP+SQLite externo ao processo, recuperação e idempotência, pacote `libfile_b3d4268069248191b98664593d518807` SHA `132457231b74939e17036c2d4cf4399bc6456dfc4e19bf6dd9e31ab9c7520c51`; relatório readback não comprova implantação compartilhada nem fencing. Central reaberta em 2026-10-13, IBX-56 R06: gateway compartilhado= NÃO; DENY antigas rotas= NÃO; canário exclusividade= NÃO; CM-000006-I0001 consumida NÃO COMPROVADO; writer epoch lease GREEN HOLD. Não foi localizado pacote R15+ autenticado nesta conexão para elevar esse limite. Contrato preparado para encaminhamento em INBOX, somente autorização de triagem, sem executar. Resposta do CM-000006 pendente.

## V. Outros requisitos, corpora e decisões

R25 B05/B12 sangramento Estocada Cruel preservado, nenhuma aproximação indevida ao veneno Serpente. B08 nova evidência de divergência de hit contra duas CA; B10 RD normal/Titã e precedência não resuelta; B06 ação bônus sem equivalência; B15 tags explícitas/ambíguas separadas; os outros 14 predicados sem prova terminal nova, preservar. Liu×Macaco sem ledger real. 9 CSV I0003 sem identificador novo autenticado, não repetir varredura 47 CSV/114 ZIP. 198 IDs e 46 ocorrências em 20 páginas intactos. Cinco decisões do R23 0/5 aprovadas.

## Fim / retomada exata

1. Mestre resolve `DEC-BONUS-JAKU-01` e, se necessário, `DEC-INFUSION-JAKU-01`; decide se CA literal39 da cena é autoridade do epoch ou se fórmula vigente exige rebase explícito. Isso não implica aprovar decisões B11/B12.
2. CM-000006 aceita/rejeita **apenas preflight** no Inbox com INSTANCE e isolamento comprovados, retorna catálogo de capacidades reais, sem reserva criada por CM-000001.
3. Executor legítimo VLAB autorizado, em sandbox, captura estado, action ledger, RNG, defesa/reação, tags, mitigação, HP e commits idempotentes. Reabrir e auditar antes de creditar B15. Se impossível, manter HOLD e selecionar alvo/ator com ação física+Fogo e CA legal testável.

**NAC-PASS-02 terminal: HOLD. REG-ROUTE-03: não registrar logs na ficha da Jaku nem no item.**

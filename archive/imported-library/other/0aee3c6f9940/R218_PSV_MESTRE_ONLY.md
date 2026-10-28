# PSV R218 — INICIATIVA ROLADA NATIVA, AUDITORIA CRONOLÓGICA E RESULTADO NEGATIVO

**AS-OF:** 2026-10-21. **MESTRE-SIDE / TEST**. **CM-000006** lógico. **OP:** OP-VLAB-FUSION-SANDBOX-01. Produção HOLD. Party/O Primeiro/fichas/normas oficiais NO-WRITE.

## ANTES

- R217: cinco pares e duas agendas congeladas, sem rolagem de Iniciativa; Eristan sempre agia por último. Dez combates, invariância terminal restrita à fixture. Base SHA256 `9eaa0b945f5838f1e5046c00a6bbd5ef6525c807299e4161c9a4a36ff997f666`.
- Motor nativo R18/v0.8.1 e R216 de movimento, AOO, magia, defesa, cura já existentes. R216 `turn` fixava o encerramento do horizonte no turno de Eristan (último na agenda antiga).

## DEPOIS — CAPACIDADE MATERIAL

- Novo pré-registro antes dos combates: `sources/R218_PREREG_BEFORE_NEW_COMBATS.json`, 24 seeds independentes × 2 arms de iniciativa (`INIT_A`, `INIT_B`), preservando streams ofensivos vinculados à mesma seed, ator e ação.
- Iniciativa **efetivamente rolada em TEST** para os três atores ON5, com expressões fonte-vinculadas: Varok `4d6+29`, Arveth `4d6+25`, Eristan `4d6+30`. Cada ator ganha um turno conforme a pontuação rolada; nenhum desempate arbitrário por ID. Empate não resolvido pela autoridade: bloqueio antes de commit.
- Adaptador **mínimo e add-only** sobre cópia do reducer R216: término de horizonte pelo último ator na ordem efetiva; novo recibo de iniciativa no journal do primeiro turno. Resolvedores de ataque/magia/movimento/cura/defesa e R18 **não foram reescritos**.

## RESULTADOS VERIFICADOS

- 48 braços pré-registrados; 33 admitidos; 15 bloqueados: 9 empates pré-commit, 6 `UNKNOWN_HALF_ODD_ROUNDING_SOURCE_HOLD` com bancos separados e intenção pendente.
- 13 pares completos (unidades independentes); em 10 deles, a ordem rolada mudou entre arms.
- **Nenhum dos 13 pares completos apresentou diferença terminal de Vida/PA por ator**, apesar da variação cronológica. **Resultado negativo na amostra**; não existe evidência de justiça universal nem de irrelevância da iniciativa.
- 33 combates novos, 396 commits, 2.452 eventos, 99 movimentos, 297 ataques físicos (33 oportunidades), 43 curas, 132 conjurações. Todos censurados no horizonte de quatro rodadas; zero KO, zero vitórias atribuídas.
- Auditor independente sem imports de engine: checa SHA chain R18, Vida, PA, movimentos, geometria, reação, danos/curas, pré-registro, PRF de dados de iniciativa, ordem efetiva de 12 turnos por luta. `PASS_R218_INDEPENDENT_NATIVE_ROLLED_INITIATIVE_SOURCE_GATED`.
- Três cópias adversariais com hashes reconstruídos rejeitadas por critérios materiais (rolagem falsificada; ordem incompatível; pré-registro divergente). Observação: a primeira versão do teste adversarial falhou metodologicamente ao rejeitar pelo filename; foi corrigida para usar ID fixo verificado nas cópias.

## LIMITES / PENDÊNCIAS

- NPCs fonte: páginas Mestre-side de Varok, Arveth, Eristan, todos **PROPOSTOS**, não homologados.
- Geometria de adjacência: contrato TEST explícito R44, não conversão canônica bloco↔metros. Custo de movimento interrompido por KO continua UNKNOWN.
- RD mágica zero é convenção TEST, não prova canônica.
- Iniciativa com empate permanece `BLOCKED-SOURCE`; nenhum bloco de desempate improvisado.
- Sucesso de salvaguarda + dano ímpar sem arredondamento oficial segue `UNKNOWN_EFFECT/HOLD`; não reexecutar seeds bloqueadas.
- Ausência de diferença na Vida terminal na fixture de 4 rodadas não garante ausência de diferenças em cenários não comutativos, movimento, KO, curas no começo de rodada, mudanças de alvo ou consumo de Reações.
- Contratos terminais 0/17 e células R91 oficiais 0/1.875 homologadas.

## AUTORIDADE E INTEROPERABILIDADE

Sem INSTANCE-ID/writer/epoch/lease reclamados; nenhum Notion/Party/produção alterado. IBX-125 e IBX-126 já publicadas pela Coordenação, com destinatário lógico `CM-000001`, ainda sem readback final do Executor correto; não duplicadas. IBX-138 adotada na interpretação, sem ACK persistente reivindicado.

## NAC-PASS PROPORCIONAL

**PASS TEST local** para rolagem real de iniciativa, integração com scheduler, auditoria independente e adversarial. **HOLD** científico para justiça generalizada e força canônica; produção HOLD.

## CONTINUIDADE

**LAST-VERIFIED-UNIT:** R218 após recuperação fria + readback. **FIRST-PENDING:** R219 candidato, sujeito a preflight e sem reutilização de IDs. **NEXT-5:** (1) fixture de ordem **não comutativa** fonte-delimitada, com aliado já ferido no início e turnos E/R em ordens diferentes, sem inventar dano durante a cena; (2) resolver desempate da Iniciativa apenas por autoridade competente; (3) identificar Beast control fonte-completo com ação, oposição, duração e escape; (4) aprofundar transformação Prata1+ sob TAP/BAP source-bound; (5) transpor dados para benchmark exploratório, sem homologação automática.

# PSV R22 — OP-DMG-CORPUS-EMP-01 | Recuperação de eventos e decisões científicas

**Identidade funcional:** CM-000001, Coordenador científico de dano, MESTRE-SIDE. **Destino:** Mestre e continuidade interna, NUNCA Party/O Primeiro. **Escrita Notion:** 0. **Writer, instância, lease, epoch, ACK Inbox e NAC-PASS-02 terminal:** nenhum reivindicado; HOLD.

## Preservação e método

R21 ZIP recuperado e verificado byte a byte: SHA-256 `06d7a30aa2ae9d9c482ae69c9e8c912741334a8a99e784d66546dd5167ccf3ba`, 22 membros CRC PASS. O verificador herdado reexecutou 36/36 testes, 21/21 SHA internos, reconstrução sem diferenças, cadeia R20/R19/R14 e R13 oráculo original preservado. R22 aninha R21 **intacto**, mais cópia byte-idêntica de `r13_oracle.py` usada somente por testes locais. Não houve reexecução massiva ou reconstrução dos motores históricos.

IBX-73 consultada em 09/10/2026 e suas restrições respeitadas: `Estado=NOVA`, `Exige ACK`, `Lida por INSTANCE-ID` em branco. Não se declara ACK ou entrega canônica sem habilitação.

## Resultado R21→R22 verificável

| Indicador | R21 | R22 | Delta verdadeiro |
|---|---:|---:|---|
| I0003 CSV originais autenticados | 0/9 | 0/9 | 0; pista nova de arquivo não encontrada |
| Identidades parciais de corpus | 198 | 198 | 0, **deliberadamente não alterado** |
| Ocorrências de fórmula / páginas | 46 / 20 | 46 / 20 | 0, **não recadastrado** |
| B certificados | 1/18 | 1/18 | 0, B02 documental apenas |
| STRICT real | 0/2 | 0/2 | 0; cena e autoridade ausentes |
| Ambiguidade de reaplicação de DoT B12 | Indeterminada no R21 | Default v1.1 localizado: renovar, não acumular infinitamente | **1 fronteira normativa resolvida por fonte vigente** |
| Decepadora Liu vs homônimas | Não comparadas em detalhe | **+18 em Liu, +30 em outra instância; machado × texto espada** | **2 conflitos de identidade/elegibilidade delimitados** |
| História da Adaga Serpente e omissão de duração | Nenhuma versão legada confrontada | Página antiga excluída recuperada por ID e comparada; mesmo efeito, ausência de duração já histórica | **Nova fonte histórica documental recuperada; explica o bloqueio como legado** |
| B15 tipagem/incomunicabilidade Veneno→Fogo | Regras gerais conhecidas | §21–23 e §32 DMG-RANK explicitamente revisadas | Gate tipado mais preciso; ausência é de evento, não de regra geral |

## Evidências dirigidas e decisões

Resumo completo com URL, literal/trecho, aspecto VERIFICADO/PENDENTE, hipóteses de erro e propostas sujeitas ao Mestre em [`DECISOES_NORMATIVAS_R22.md`](DECISOES_NORMATIVAS_R22.md) e [`R22_B11_B12_B15_RESOLUTIONS.json`](R22_B11_B12_B15_RESOLUTIONS.json).

- **B11 — PARTIAL:** crítico normal físico `3d6` sequencial, base 1/108, Patada Macaco condicionada `2d6+54 → 2d6+66`; magias não critam sem exceção. O Crítico Brutal de Liu expressa um multiplicador +2, enquanto regra vigente é aditiva; falta operador. Decepadora no machado de Liu tem +18 cortante, não +30 de outros equipamentos, e chama arma de espada; condicional a elegibilidade e ordem de gatilhos. Decisões DEC-B11-A/B/C explicitadas; nenhum efeito extra presumido.
- **B12 — PARTIAL com delta normativo real:** veneno Serpente `3d12/tick` condicionado à falha CON CD25, média19,5; ausência de duração/timing/cura permanece. **DMG-RANK v1.1 §23 determina reaplicação que renova duração por default e proíbe acúmulo infinito**. Outro item explicita 1 minuto e outro explicita remoção Fortitude CD80, **regras locais não transferíveis**. Foi reaberta a página histórica excluída `4a9c2b...93948` e cruzados cinco campos contra a ficha atual: dano imediato, save, veneno por turno, custo e duração; os quatro primeiros coincidem e **ambas carecem de duração**. Logo, a omissão não surgiu comprovadamente na migração recente. Imunidade por tag do alvo exige prova; natureza do dano imediato Serpente não está tipada na ficha. Decisões DEC-B12-A/B restantes.
- **B15 — PARTIAL:** regra documental suficiente para ataque `1d8 físico +2d6 Fogo →1d8+5d6` com alvo fraqueza Fogo, DME11,5→22. DMG-RANK determina fraqueza somente no pool elemental de fonte tipada, sem converter veneno/impacto em Fogo. **Não há ambiguidade matemática geral do exemplo a resolver**, mas faltam ataque efetivo, fraqueza atual alvo, defesa/RD e replay do evento.

### Cena Liu e dois STRICT

Notion foi pesquisado por `Liu Xiaua` + `Macaco Rei` + `event_id/effective_at`, logs/diários, `Perdido -46`, proficiências e recibos de cena. Os resultados apontaram fichas e relatórios científicos/sandbox, **sem prova de evento real**. Os arquivos herdados R04–R21 exibem rolagens sintéticas `(3,4)` e `(5,3)`; **não** constituem episódio de campanha/STRICT. Detalhes em `R22_LIU_SCENE_AND_STRICT_GAPS.json`.

Os faltantes B04/B09 são precisamente: origem e tempo de PA Livre/`Perdido -46`, custos e ativação dos equipamentos, ação completa e Reação subsequente, proficiências efetivas Fortitude/Luta/Reflexo, forma, Vida/Alma/camadas, geometria/LoS, iniciativa e rolagens, estado antes/depois e executor/recibo assinado. O segundo combate STRICT sequer tem par e cena congelados. **0/2 mantido corretamente**.

### I0003

Sem varredura equivalente dos 47 CSV/114 ZIP já auditados. Pesquisas dirigidas por termos específicos ao predecessor e manifesto não trouxeram nome físico, Library ID ou hash SHA original dos nove arquivos (sete de itens, dois de Fogo). Mantemos 0/9 originais, 198 IDs **derivados**, e aguardamos **identificador ou pacote bruto real** para retomar. Descrição do esforço/falha em `R22_I0003_FOCUSED_AUDIT.json`.

### Matriz B01–B18 / governança

**1 PASS_DOCUMENTAL B02, 9 PARTIAL, 6 BLOCKED, 2 NOT_TESTED integrais (B14/B17 examinados documentalmente); 0 novos PASS**. `R22_B01_B18_MATRIX.csv/json` preserva TODOS os predicados originais e estados do R21. Contratos não relaxados. R22 testa pontos normativos, não finge eventos oficiais. Estado documental científico local `QA-PASS`; NAC-PASS-02 terminal/canonização `HOLD`.

## Próxima meta baseada em gargalo verificável

1. Submeter **apenas** as decisões DEC-B11-A/B/C e DEC-B12-A/B sob autoridade Mestre e NAC-NORM-01; não multiplicar simulações sem decisão. Em B15, buscar par real ou fixture oficialmente atestado com componentes e fraqueza, não alterar a regra.
2. Investigar originais de ledger real da cena Liu por `scene_id/event_id/effective_at/actor snapshot`, evitando redescrever fixtures. Sem disponibilidade, permanecer HOLD e redirecionar esforço a contratos com fonte completa.
3. Reabrir I0003 somente se aparecer nome/ID/arquivo original, para auditoria SHA real dos 9 CSV; não refazer 198 ou 46.
4. Após qualquer decisão/integração autorizada: registro ANTES, gate, execução, reabertura, REGISTRO DEPOIS, REPA/NAC-CONT/NAC-PASS e handoff sem duplicatas. Não alterar live, Party, Primeiro ou VLAB sem executor e governança próprios.

**Gate de conclusão deste checkpoint:** arquivo ZIP R22 + manifesto SHA, R21 inteiro preservado, teste de contratos dirigido, recuperação limpa, handoff. Esta entrega **não conclui** o objetivo 9/18 nem a pesquisa científica.

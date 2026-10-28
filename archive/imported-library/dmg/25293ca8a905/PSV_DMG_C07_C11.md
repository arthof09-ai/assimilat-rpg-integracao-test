# PSV — CM-000001 · OP-DMG-CORPUS-EMP-01 · POST-R10-C07–C11

**Data:** 16/10/2026 · **Ambiente:** exclusivamente MESTRE-SIDE · **Baseline:** DMG-RANK-01 v1.1 inalterada  
**Operação existente, sem duplicação.** C07, C08, C09, C10 e C11 executados **sequencialmente**, com bloqueios tratados antes do avanço seguinte. Zero writes no Notion, Party, O Primeiro, motor do VLAB ou campanha. **NAC-PASS produtivo HOLD.**

## ANTES — recuperação física

O checkpoint `POST-R10-C02-C06` estava disponível. O conjunto histórico indicado em seu manifesto permaneceu imutável; 18/18 artefatos R10/C01 foram reabertos e seus hashes históricos conferem. Dos 18 artefatos C02–C06 relacionados no manifesto, cinco estavam montados por path e seus hashes conferem; demais históricos não foram reconstituídos nem classificados como verificados por bytes nesta sessão. O arquivo final do checkpoint C02–C06 também estava disponível; não foi alterado.

A OP VLAB [R47–R49](https://app.notion.com/p/3f3c2b324ede819496ddd7f93bd7e5d2) agora contém REGISTRO DEPOIS, ausente no checkpoint C06. Pacote físico da Biblioteca materializado somente-leitura com **SHA256** `fada8b0a413edfcdccc54af60c258c0bd25274848a9c10ff4df37d11cf0ed7d2`; `39/39` membros de manifesto conferidos e CRC íntegro. Auditor standalone original reexecutado: **6/6 cenas**, **15/15 eventos**, **6/6 checkpoints** PASS, sem importar motor executante. Isto é auditoria independente read-only de resultados históricos, NÃO execuções nativas novas da DMG.

## C07 — identidade/natureza, reconciliação dirigida

- [Veado das Montanhas](https://app.notion.com/p/8acc2b324ede827b9bc801746ae97409): parent real identificado; folha intitulada **Bronze 4**, corpo **Bronze 2 (1d6)**. A fórmula `Galha mortal: 1d6+FOR11` possui distribuição bruta 12–17, média 14,5; não há `Luta` individual na folha. A divergência de **estrela** não muda os **dados de rank Bronze 1d6**: esta parte da classificação é invariante nas duas leituras. `CA49` é compatível com `10 + DES38 + CON3/5 = 48,6`, mas não certifica a regra de arredondamento nem resolve o rank/estrela. Se normal Bronze sem modificação competente, a RD geral Bronze5 seria a mesma em ambos os estados. A ação completa **não está admitida** sem Luta ou mecanismo de acerto autorizado, natureza, custo e alcance.
- [Regalis voltmane](https://app.notion.com/p/bd4c2b324ede8381929e815d7159fe4d) é o parent da ficha [Ouro 2](https://app.notion.com/p/5fac2b324ede8381a25581194ebf9bd7); título e classificação do corpo Ouro 2 concordam, porém o campo **Nome está vazio**, e descrições dizem **Aurora Radiante**, uma família diferente. Fórmulas brutas `Raio eletrizante 2d4+INT72`, `Raio purificador 2d4+INT72` (74–80, média77); `Toque macabro 1d4+INT72` (73–76, média74,5). Em Raio eletrizante, `1d4=1` abre teste de Fortitude com probabilidade 1/4 de **testar**, não 1/4 de paralisar incondicionalmente. A condição efetiva depende do teste. Faltam tipagem de habilidade, PA, alcance, hit/salvaguarda e identidade do texto copiado.
- **Regra relevante:** [Sistema de Magia](https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373) NÃO possui teste de acerto universal para magia e NÃO aplica crítico físico a magia, salvo exceção individual expressa; 1 Ação Padrão é default quando a ação é **legitimamente classificada como magia**. Não se pode adotar nem negar essa classificação pelos nomes 'Raio'/'Toque'.

**Resultado C07:** parte da classificação Bronze é invariante, mas **Veado e Regalis continuam BLOCKED_NORMATIVE para experimentos nativos completos**. Consulta de páginas e buscas dirigidas não encontrou autorização de Luta para Veado nem autenticação operacional das magias de Regalis; ausência de busca não equivale a prova de inexistência universal.

## C08 — R47–R49 nativo recuperado, com fronteiras respeitadas

- **R47**: Cabra obtém crítico válido que ultrapassa CA123 de Feryn, mas dano todo mitigado por RD22; Contra anunciado ANTES da RNG, Reação consumida, **resposta bloqueada por ambiguidade**.
- **R47B**: crítico `6→6→6`, dano bruto23, RD22, dano líquido1, Vida de Feryn 479→478. Crítico acertou apesar da CA123. Counter de resposta **não aconteceu**.
- **R48**: primeiro Counter fonte-completo; Reação aninhada **não admitida** sem precedência normativa e turno próprio; não classificar como contra-aninhamento executado.
- **R49**: duas instâncias de Feryn ON5 com DES80 empataram em Destreza; desempate com **4d6** e R26, não d6 universal. Três janelas fonte-documentadas produziram 6 AoOs e dano líquido Varok 83, 104 e 100, cada uma em cena independente.

**Fronteiras que a DMG NÃO deve resolver por inferência:** (1) se Contra-atacar predeclarado gera resposta a crítico autoacertador cujo score é menor que CA; (2) se e como Reação aninhada em próprio turno é legal. R47–R49 já executadas pelo executor VLAB distinto; a DMG não as reexecutou.

## C09 — comparação 3×ON5 com falha crítica negativa LAB separada

Fichas oficiais consultadas para o sandbox de encontro: [Feryn](https://app.notion.com/p/3f6c2b324ede81ce9c61db8127bf0e31), [Varok](https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091), [Arveth](https://app.notion.com/p/3f6c2b324ede8105891fc647242e61ca). São **propostas Mestre-side de encontro, admitidas em janelas VLAB**, não amostra populacional ON5 nem combates da campanha.

**Premissas congeladas:** 4d6 categoria ON5; testes equipados Feryn `4d6+92`, Varok `4d6+100`, Arveth `4d6+72`; danos `8d8+47`, `10d10+48`, `8d10+35`; CA Feryn123/Varok83/Arveth93, RD Feryn22/Varok35/Arveth30. Crítico positivo (decisão Mestre): 1/108 acerto automático com dano de dados máximos adicionados. Crítico negativo (decisão **LAB-only R42**): 1/108 autoerro. Para demais verificações, acerto comum supera numericamente CA. Os dados de verificação e de ataque são independentes conforme modelo de estudos anteriores. Sem ataques extras, Reações, consumíveis ou movimentação neste *oráculo de uma tentativa*.

| Origem → destino | P(acerto comum condicionado a não crítico) | P(acerto efetivo por tentativa) | Vida líquida esperada / tentativa |
|---|---:|---:|---:|
| Feryn → Varok | 100% | 99,0741% | **48,14815** |
| Feryn → Arveth | 100% | 99,0741% | **53,10185** |
| Varok → Feryn | 0,07716% | 1,00166% | **1,73727** |
| Varok → Arveth | 100% | 99,0741% | **73,25000** |
| Arveth → Feryn | 0% | 0,92593% | **1,26852** |
| Arveth → Varok | 76,08025% | 75,59728% | **34,00354** |

**Descoberta material:** Varok utiliza o MESMO golpe equipado e tem dano efetivo por tentativa **42,16× maior contra Arveth que contra Feryn**, mesmo rank e estrela. O gargalo é a defesa do alvo, não uma alteração de dano-base. Com Esquiva Feryn125, Varok já não possui nenhum acerto comum e seu dano esperado se restringe ao ramo crítico. Não declarar que esta diferença é necessariamente desbalanceamento: equipamento, ações especiais, iniciativa e composição de encontros importam.

**Correção frente a C03:** incorporar a regra LAB-only de falha crítica negativa reduz Feryn→Varok de 48,5926 no modelo sem falha negativa para 48,1481 neste modelo. Não corrigir retroativamente o C03 como se os pressupostos fossem os mesmos.

## C10 — efeito de precedência e custo marginal por ativação

**R49 ao longo de duas ações básicas:** cada ataque equipado de Feryn contra Varok, já mitigado por RD35, causa 20–76 de Vida se normal; se crítico, máximo140. Nem **dois críticos máximos** podem eliminar Varok HP734 (2×140=280). Com dois atacantes com ficha idêntica, sem efeito adicional, interrupção ou decisão tática pós-golpe, trocar a ordem dos dois AoOs altera **zero** da distribuição de dano total. Assim a precedência de R43 é exigência causal normativa, mas não é uma vantagem de dano **nesse caso fixo**. O controle de seis golpes comuns teria média288; os três cenários R49 **selecionados dirigidamente** deram287 (83+104+100). **Não utilizar isso como amostra aleatória.**

**Dado competente da prioridade ON5:** probabilidade exata de empate entre `4d6` e `4d6` é `7553/93312` ≈ 8,09435%; número esperado de rodadas de desempate com rerrolagem apenas dos empatados é `93312/85759` ≈ 1,08807.

**Ativações no golpe equipado, cada uma 1 vez/cena sem Ação Padrão adicional:** Feryn +5d8 Vento/45 PA, Varok +6d12 impacto/60 PA, Arveth +6d10 Terra/55 PA. PA livre inicial 424/324/344 respectivamente; os vínculos diários já estão compromissados e NÃO são cobrados novamente por golpe. Médias **brutas extras** 22,5 / 39 / 33 Vida.

Há uma lacuna material de interpretação da RD para parcelas no mesmo golpe:

| Extra | Se uma mitigação conjunta já absorvida pela parcela física | Se RD do alvo incidir separadamente na parcela extra (contrafactual) |
|---|---:|---:|
| Feryn contra Varok | +22,5 | **+0,006409** |
| Varok contra Feryn | +39 | **+17,056874** |
| Arveth contra Feryn | +33 | **+11,165792** |

**Estes dois ramos NÃO possuem igual autoridade:** o segundo é limite de sensibilidade, não autorização para aplicar RD duplicada. Tipos Vento, impacto e Terra podem ter resistência específica. O cálculo mostra o risco de inflar ou reduzir a eficiência de itens ao aplicar mitigação indevida. Também não cobrar PA quando a ação não acerta; alcance/ação da cena e primeiro golpe legal permanecem necessários.

## C11 — quantificação da decisão mínima de Contra-atacar

A R47B comprova que uma Investida crítica contra CA123 de Feryn pode acertar automaticamente e atravessar RD22 por um ponto: dano crítico `1d6+19` gera valores 20..25, e o dano líquido `0,0,0,1,2,3`. No modelo com rolagem crítica válida independente, a chance de **dano positivo por tentativa** é `1/216` e a expectativa líquida é `1/108`, sem outras ações.

Se um Contra-atacar predeclarado **puder** responder a esse ataque crítico autoacertador, o golpe equipado de Feryn com Vantagem possui mínimo `4d6+94` →102 contra CA20/Esquiva26 e dano líquido mínimo `8d8+47−RD5=50`, suficiente para incapacitar uma Cabra de Vida38 sempre que o próprio golpe não seja cancelado por um mecanismo competente (por exemplo, falha crítica negativa no LAB). Se o gatilho exigir **erro real**, não haverá golpe de resposta e a Cabra sobreviverá nessa janela. A situação R47B observada permanece Feryn HP478 e Cabra HP38, **resposta bloqueada**, sem promover qualquer alternativa a regra.

**Decisões mínimas reservadas ao Mestre/NAC:**
1. Contra-atacar declarado antes de crítico que autoacerta, com score comum insuficiente para CA, permite ou não a resposta? A redação 'não superar CA' e a regra expressa de acerto crítico precisam de precedência.
2. É legal Contra-atacar aninhado em resposta a outro Contra-atacar durante o turno próprio do agressor? Qual ordem de declarações e consumo do slot?

Pedir isso **apenas ao canal Mestre competente**, não criar regra paralela; DMG mantém ramo afetado HOLD. Outros contrastes independentes já executados não dependem dessas respostas.

## Auditoria de reprodução, critérios de refutação e estado final

- Script científico `C07_C11_EXACT_REPLAY.py`: probabilidade por convolução exata e matrizes fonte-definidas; 5 deltas JSON com status distintos.
- Implementação separada `C07_C11_INDEPENDENT_CHECK.py`: não importa o primeiro script, reenumera dados e sequências críticas, audita **62 verificações** locais e novamente compara CRC/hash da R47–R49 e hashes históricos. Os testes demonstram consistência computacional, **não 62 descobertas ou aceites canônicos**.
- Novo VLAB nativo executado pela DMG: **0**. Новo combate canônico: **0**. Novas páginas, fichas ou regras escritas: **0**.
- F0 documental: **4/8**, sem aceitar fases; Lote003: **0/71** individualmente autenticado; VLAB contratos terminais **0/17**; células canônicas **0/1.875**; writer produtivo HOLD.

**Falsificadores:** se fonte competente atribuir Luta à Galha ou classificar os raios de Regalis, reabrir **somente** as ações afetadas; se contra-ataque crítico receber decisão Mestre, substituir cenários condicionais por ramo autorizado e solicitar execução do VLAB em **novo** ID; se fonte estabelecer RD específica Vento/Terra, recalcular incrementos condicionais e não reutilizar tabela sem correção.

**ANTES:** C06, R47–R49 ainda em REGISTRO ANTES, Veado/Regalis em BLOCKED, ON5 sem negativo LAB integrado a matriz.  
**DEPOIS:** cinco ciclos científicos C07–C11 com R47–R49 fisicamente reaberto/auditado, fonte parcialmente normalizada, matriz ON5 atualizada, AoO de dois golpes provado não letal sob todos os críticos e nova quantificação do bloqueio normativo de Contra-atacar.

**Retomada exata:** decisões mínimas do Mestre sobre duas Reações Contra-atacar; contrato Regalis/Veado continua bloqueado sem Luta/natureza; no ramo técnico independente, VLAB R47–R49 tem auditor PASS, próximo multi-turno entre Feryn e Varok usando Iniciativa individual `4d6+82/4d6+29` é **proposto** e depende do gateway VLAB próprio, sem executá-lo aqui. Não reexecutar cenas nem sementes R47–R49, não reutilizar pending UNKNOWN_EFFECT. Data, origem e SHA dos anexos consolidados no checkpoint.

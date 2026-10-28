# Oficina CRAFT v03 — operação pelo chat do celular

**Destinatário: Mestre. Nenhuma instalação, Python ou computador necessários.** O próprio Comestre executa o motor R48 isoladamente; as decisões pertencem ao Mestre.

## Use assim

1. Escreva: **“Comestre, quero fabricar 3 Tábuas e 2 pares de Mica em sandbox.”**
2. O Comestre identifica B30-01 e B30-03, os ingredientes, as ferramentas e habilidades da receita experimental. Se não houver sessão fictícia anterior disponível, oferece uma escolha de estoque de TESTE; não inventa estoque real.
3. O Comestre executa `craft_chat.py prepare` no seu ambiente e mostra **prévia do R48**, estoques antes, déficits, QA por tentativa, custo MED indisponível e peças previstas. **Prévia não reserva nem debita estoque.**
4. O Mestre diz **“Confirmo a fabricação experimental do plano <ID>”** ou **“Cancelo o plano <ID>”**. Só a confirmação explícita libera `craft_chat.py confirm`.
5. O Comestre reabre o ledger R48, confere hash/quantidades/status/recibos, relata resultados, salva um **backup portátil da sessão** e o disponibiliza na Biblioteca/arquivo de conversa.
6. Para consultar outra vez, diga **“Mostre meu estoque CRAFT”**, **“Mostre os recibos”**, **“Repita o mesmo pedido”**, **“Reverta o último lote de teste”** ou **“Recupere a sessão CRAFT <ID>”**.

### Receita e quantidade

- **B30-01**: uma Tábua Lamelar de Inscrição de TESTE; contrato experimental: 1 lâmina de Ardósia por tentativa; ferramentas de clivagem, apoio, régua/esquadro, paquímetro, abrasivo e EPI; habilidades lapidação mineral/metrologia.
- **B30-03**: um PAR de espaçadores de Mica de TESTE (2 peças); contrato experimental: 1 folha de Mica A e 1 de Mica B por tentativa; ferramentas de corte fino, apoio, micrômetro, régua e EPI; habilidades laminação mineral/metrologia.
- **Limite R48**: 1–16 tentativas por lote, no mesmo ledger sintético; cada tentativa tem laudo/QA/recibo individual.
- **Custo real e preço MED**: PENDENTES, NÃO inferidos. Tempos, geometria, QA e rendimentos são parâmetros PROPOSTOS para a simulação, não medições de campo. Chaves e assinaturas R47 de TESTE.

### Exemplo demonstrativo preparado, ainda não confirmado

Sessão `sim-75192d55b85e`, plano `SBX-R48-BATCH-UI-2afb696406a6e839` (sempre conferir readback/HEAD antes da confirmação). Estoque inicial escolhido somente para demonstração: Ardósia apta=8, Mica A=8, Mica B=8. Resultado projetado pelo R48: 3 Tábuas + 2 Pares de Mica, 5 tentativas/7 peças, saídas com 5 Ardósias, 6 Mica A, 6 Mica B. **Commit ainda não realizado nessa sessão.** Backup independente: `CRAFT-CHAT-SESSAO-MESTRE-v03.zip`.

### Segurança e falhas

- Cancelamento anterior ao commit = zero débito. Repetição com **mesmo batch-ID/hash** = sem duplicidade; novo batch-ID é um novo pedido, não replay.
- QA individual altera só o laudo sintético daquela tentativa; a decisão passa pelos mesmos motores R46/R47/R44/R48. Um lote pode terminar misto, desde que o Mestre autorize explicitamente quarentenas na prévia.
- Evidência QA simulada **não** prova fabricação, estoque ou ensaio físico. O contrato do motor determina o débito/rejeição.
- Reversão em sandbox gera **outra sessão derivada do checkpoint anterior**, preservando a primeira. Não equivale a estorno oficial.
- Sem processo persistente presumido: exportar backup por sessão após decisão; se necessário, recuperar ZIP antes de nova operação. No caso de efeito desconhecido, **reabrir/reconciliar antes de retentar**.
- Governo oficial invariável: **0/26 gaps encerrados, 0/30 RC5, F5 RED, C19-021 UNKNOWN-SIDE-EFFECT e NAC-PASS material HOLD.** Nenhuma escrita em fichas, Party/O Primeiro ou Notion.

## Nota operacional para futuro Comestre (o Mestre NÃO executa isto)

O projeto contém `craft_chat.py` (adaptador de entrada/saída) e a pasta original `Oficina-v02/`. Com ambiente Python + `cryptography` instalado e ferramentas de execução autorizadas:

- `python craft_chat.py --data <pasta-da-sessao> status`
- `python craft_chat.py --data <pasta-da-sessao> prepare --counts '{"B30-01":3,"B30-03":2}' --intent CHAT-MESTRE-20261014-3T-2M-01`
- `python craft_chat.py --data <pasta-da-sessao> preview --batch <batch-id>`
- Após confirmação humana explícita: `python craft_chat.py --data <pasta-da-sessao> confirm --batch <batch-id> --ack CONFIRMO-SANDBOX`
- `python craft_chat.py --data <pasta-da-sessao> history` / `replay --batch <batch-id>` / `rollback`
- `python craft_chat.py --data <pasta-da-sessao> export --out <backup.zip>`
- `python craft_chat.py --data <pasta-vazia> restore --archive <backup.zip> --into <pasta-vazia>`
- `python demo_chat_v03.py --out demonstracao.json` reproduz escolhas AUTOMATIZADAS, **não uma UAT humana**.

**Fonte de verdade da sessão**: último backup persistente verificado + ledger readback, nunca relatório de chat isolado. **Fonte do RPG**: Notion canônico, independente deste sandbox.

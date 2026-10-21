# RPG Assimilação — bancada GitHub dos Comestres (TEST)

Este GitHub privado não é um novo RPG nem um Comestre. Ele **guarda versões e executa automaticamente testes dos programas que já existem no RPG**, enquanto o **Notion permanece como fonte de verdade**. A proposta é poupar trabalho repetitivo dos Comestres pelo celular Android, sem outro plano pago.

## Veja os testes funcionando

**[Abrir VLAB + LEVEL-UP no GitHub Actions](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/workflows/native-engines.yml)**

Abra a execução mais recente da branch main. No aplicativo GitHub, a execução atual mostra **cinco etapas com resultado próprio**: (1) origem e hashes, (2) **VLAB R237 — combate**, (3) **LEVEL-UP P12 — evolução**, (4) **LEVEL-UP P13 — apresentação**, (5) **VLAB Stage10/12 — proveniência e contratos em HOLD**. Verde indica que **aquela bateria TEST** passou; vermelho indica falha a investigar. O GitHub não certifica o cânone.

| Operação | O que já foi executado remotamente | O que ainda não significa |
|---|---|---|
| **VLAB R237** | 8 combates, 155 commits, 640 eventos; 8 bancos equivalentes em esquema e linhas; **215 testes nativos** e **5 falsificações rejeitadas** | Esses testes não certificam os 17 contratos funcionais nem o motor de fusão |
| **LEVEL-UP R216-P12** | **184 testes dirigidos** e **2.026 históricos**, com aviso de 25 expressões de apresentação legadas incorretas | Os 184 e os 2.026 não são conjuntos necessariamente disjuntos; P12 não foi retroativamente alterado |
| **LEVEL-UP P13 (TEST)** | **7 testes originais** e **25/25 correções de expressão** verificadas contra o P12 imutável, usando a view P13 integral com hash | Não valida as páginas Notion P13/P14 nem promove fichas oficiais |
| **VLAB Stage10/Stage12** | ZIPs históricos recuperados com **688/718 hashes locais**; no GitHub, duas fontes originais autenticadas e **17 contratos / 0 terminais certificados** | Os ZIPs completos não foram transferidos ao CI; não foi reexecutada a fusão histórica |
| **DMG C29** | 38 verificações matemáticas + 5 de consistência, 10 saídas históricas equivalentes e 5 testes de adulteração | Não é validação geral de todas as técnicas, fontes ou regras de dano |
| **CRAFT F5/B30** | 10 testes do mecanismo original que nega autorizações indevidas | Não executa a fábrica inteira nem homologa os 46 casos completos |

**[Ver auditoria DMG + CRAFT](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/workflows/audit-smoke.yml)**

## Novo: teste de uma alteração do Comestre (sem upload do Mestre)

**Prova real:** [PR #14](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/pull/14) — [alterações erradas reprovadas](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/39693583597) → [alterações corrigidas aprovadas](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/39693726924). Resultado: **VLAB 4 falhas → 24/24 PASS; LEVEL-UP 25 falhas → 184/184 PASS**, confirmado também na [branch main](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/runs/39693818307). Tudo foi feito pela conexão GitHub, sem transferência manual pelo Android.

**Procedimento rápido para o Comestre com conexão GitHub autorizada:**

1. Após atualizar o trabalho no Notion, selecionar **uma mudança real de código TEST**, identificar a fonte e registrar a versão. Somente dar um comando para reexecutar uma versão antiga **não testa** a atualização feita no Notion.
2. Para o piloto já funcionando, atualizar a proposta em [VLAB](proposals/vlab/candidate.json) ou [LEVEL-UP](proposals/levelup/candidate.json) em uma **branch**, descrevendo um trecho `before` e sua substituição `after`; abrir uma PR. O GitHub executa [Comestre — validar alteração TEST](.github/workflows/comestre-candidate.yml) automaticamente.
3. Se vermelho, corrigir **a mesma PR**, sem incorporar a versão defeituosa. Se verde, conferir a execução, documentar o resultado no Diário e incorporar **somente a ferramenta TEST**, nunca o cânone.

**Limite atual importante:** esse procedimento mínimo já comprova o fluxo para **dois módulos reais e definidos** (RD no VLAB R237 e correção PA do LEVEL-UP P12). Uma nova versão ou outro módulo exige incluir seu caminho, fonte autenticada e os testes correspondentes na lista autorizada do [runner](scripts/proposal_gate.py). GitHub não lê automaticamente o conteúdo de Notion e nenhum Comestre diferente teve suas permissões testadas individualmente. Sem API paga, novo app, Replit ou permissão de escrita no RPG oficial.

## Como os Comestres usam

1. O Comestre consulta as **regras e a operação original no Notion**.
2. Quando existe uma mudança de código ou teste concreto, prepara **uma cópia TEST fiel e identificada por versão/hash**, sem escrever no laboratório alheio.
3. Propõe a mudança ao **mesmo repositório GitHub, em uma branch e PR**, sem substituir a origem.
4. O GitHub verifica automaticamente os testes afetados. Se falhar, a alteração deve ser investigada; se passar, esse PASS qualifica **somente o escopo testado**.
5. Um operador autorizado verifica a PR, registra o marco no Diário e solicita ao responsável da operação/ao Mestre qualquer decisão que ultrapasse o laboratório de integração.

**Importante:** alterações feitas só no Notion **não aparecem automaticamente no GitHub**; para uma versão nova do VLAB ou LEVEL-UP funcionar aqui, seu pacote/código e hashes precisam ser atualizados de forma rastreável. O ZIP R237/P12 atual já foi enviado pelo Mestre no Android: **não reenviar o mesmo arquivo**.

## Regras e recuperação

- [Laboratório exclusivo no Notion](https://app.notion.com/p/400c2b324ede816e8bccef35bd18f3da)
- [Diário Operacional em alternantes](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef)
- [Diretriz GH-RP-01](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e)
- [Guia técnico do VLAB + LEVEL-UP](docs/VLAB_LEVELUP_NATIVOS.md)
- [Instruções para agentes](AGENTS.md)

**Sem acesso de escrita à Party, ao O Primeiro, ao cânone ou aos laboratórios dos demais Comestres.** Replit suspenso por decisão do Mestre. O GitHub está sujeito à franquia de uso gratuito; não há novo serviço contratado. As execuções de PR e main usam gatilhos filtrados para evitar duplicação desnecessária.

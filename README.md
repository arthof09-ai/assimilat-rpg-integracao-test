# RPG Assimilação — bancada GitHub dos Comestres (TEST)

Este GitHub privado não é um novo RPG nem um Comestre. Ele **guarda versões e executa automaticamente testes dos programas que já existem no RPG**, enquanto o **Notion permanece como fonte de verdade**. A proposta é poupar trabalho repetitivo dos Comestres pelo celular Android, sem outro plano pago.

## Se o GitHub gratuito esgotar: Comestre continua no ChatGPT

**Regra oficial GH-RP-01 — continuidade nativa sem gasto:** GitHub Free oferece **2.000 minutos mensais de Actions para repositórios privados** (franquia da conta proprietária, compartilhada entre repositórios; conferir [documentação oficial](https://docs.github.com/en/billing/concepts/product-billing/github-actions)). É uma ferramenta **opcional**: não permita que falta de minutos, acesso, fila ou Actions fora do ar bloqueie VLAB, LEVEL-UP, DMG, CRAFT ou qualquer operação.

**Decisão rápida:** GitHub útil e com quota → testes pela PR; quota esgotada/indisponível ou minutos reservados para tarefas críticas → **executar os motores e testes ORIGINAIS nativamente no ChatGPT**, em cópias TEST isoladas, como antes da integração. Os testes locais devem registrar motor e versão, hashes quando disponíveis, testes efetivamente executados, falhas, correção, logs e limitação. A ausência de GitHub é `GH-NOT-RUN`, **não reprovação do código**, e sucesso local é `LOCAL-TEST-PASS`, **não `GITHUB-CI-PASS`**. Se o runtime ou ZIP não estiver disponível ao Comestre, continuar com outras tarefas seguras e registrar precisamente apenas os testes não executados.

**PR já aberta e sem minutos?** Continuar a evolução e os testes nativos; manter a aprovação CI dessa PR em `CI-HOLD` sem mesclar como validada remotamente. Ao voltar a ter quota, rodar os testes remotos somente se realmente necessários. Não criar novo executor paralelo, não pagar, não publicar repositório privado, não estender cronogramas por causa do GitHub.

**Economia de minutos:** a auditoria integral não precisa disparar por mudanças apenas em README/AGENTS/docs; evitar reexecuções obsoletas, usar testes do módulo alterado primeiro e bateria completa nos marcos reais. A leitura do consumo/faturas é feita no painel da conta proprietária: não existe uma medição de quota validada por esta conexão. Para evitar custo extra, conferir [orçamentos e alertas GitHub](https://docs.github.com/en/billing/how-tos/set-up-budgets) sem autorizar cobrança.

## Disponível a todo o RPG — autorização transversal TEST

**Decisão expressa do Mestre (21/10/2026):** este repositório privado é infraestrutura compartilhada de programação, versionamento, simulação, testes e auditoria **TEST** para **todas as operações autorizadas** do RPG Assimilação: VLAB, LEVEL-UP, DMG, CRAFT, inventário, consumo de PA e outras que se beneficiem de código. A autorização **não obriga** ninguém a integrar módulos desnecessários e **não dá acesso técnico automático a outras instâncias**. O Comestre continua titular da sua operação; GitHub não é Comestre e não altera o RPG Central.

**Rotina mais curta:** concluir no Notion da operação → enviar **a alteração real de código TEST**, com versão e origem, pela conexão GitHub autorizada → branch + PR → GitHub executa os testes pertinentes → Comestre consulta PASS/FAIL/PENDING **na mesma conversa** → se FAIL, corrige na mesma PR; se PASS, confere o commit, o diff e os testes antes de qualquer integração TEST → registra somente resultado material. **Notion não precisa se sincronizar automaticamente.** O GitHub não manda resposta espontânea ao chat; a consulta é feita pelo Comestre.

**Fronteiras:** apenas o repositório e o laboratório TEST recebem escritas desta integração. Fichas oficiais, Party, O Primeiro, cânone e outros laboratórios são **NO-WRITE**. Não incorporar código experimental direto na `main`, nem PR com testes obrigatórios vermelhos, pendentes ou incorretos; não afirmar que há proteção técnica automática de branch, ainda não comprovada na conta atual. Nenhum custo extra, Replit suspenso e nenhuma estrutura administrativa nova.

**Cobertura existente versus autorização:** os scripts de propostas já testam alterações reais em **dois módulos** (VLAB redução de dano e LEVEL-UP anéis PA); existem ainda baterias de VLAB, LEVEL-UP, DMG e CRAFT. Isso **não significa** que todos os demais módulos já tenham runner: só cadastrar a fonte e os testes originais de um novo módulo quando houver necessidade concreta. [Diretriz GH-RP-01](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e) · [Instruções do Comestre](AGENTS.md).


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

## Na mesma conversa: enviar → receber → corrigir

O Comestre **não precisa esperar o Mestre olhar o GitHub**. Após registrar sua versão no Notion, usa sua conexão GitHub (se disponível), envia a alteração TEST por PR e **consulta a execução do GitHub Actions ainda na mesma interação**. O GitHub não escreve espontaneamente no chat: o Comestre consulta status e logs.

| Retorno do GitHub | O Comestre faz |
|---|---|
| ✅ **PASS** | Confere PR, hash/commit, testes necessários e autoridade; incorpora apenas a alteração TEST autorizada e registra no Diário |
| ❌ **FAIL** | Lê o erro, corrige **na mesma PR**, espera a nova execução e confere novamente; não incorpora versão defeituosa |
| ⏳ **PENDING** | Consulta novamente enquanto a sessão permitir; se continuar pendente, fornece link e estado real — nunca inventa conclusão |

**[Abrir o workflow de propostas do Comestre](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/workflows/comestre-candidate.yml)** · [Prova RED → GREEN da PR #14](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/pull/14).

**Regra operacional:** não alterar `main` diretamente, não mesclar falhas, não promover regra canônica. A proteção técnica de branch do repositório privado não foi confirmada na configuração gratuita: estes controles exigem atuação responsável do Comestre e conferência do estado real. Não contratar plano para instalar controles adicionais. O piloto aceita dois módulos; ampliar somente quando houver uma mudança concreta. [Instruções completas para agentes](AGENTS.md).

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

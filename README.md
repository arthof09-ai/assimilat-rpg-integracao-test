# RPG Assimilação — bancada GitHub dos Comestres (TEST)

Este GitHub privado não é um novo RPG nem um Comestre. Ele **guarda versões e executa automaticamente testes dos programas que já existem no RPG**, enquanto o **Notion permanece como fonte de verdade**. A proposta é poupar trabalho repetitivo dos Comestres pelo celular Android, sem outro plano pago.

## Veja os testes funcionando

**[Abrir VLAB + LEVEL-UP no GitHub Actions](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/workflows/native-engines.yml)**

Abra a execução mais recente da branch main. No aplicativo GitHub, a execução mostra **três etapas com resultado próprio**: (1) verificação do ZIP e das hashes de origem, (2) **VLAB — combate**, (3) **LEVEL-UP — evolução**. Verde indica que **aquela bateria TEST** passou; vermelho indica falha a investigar. O GitHub não certifica o cânone.

| Operação | O que já foi executado remotamente | O que ainda não significa |
|---|---|---|
| **VLAB R237** | 8 combates, 155 commits, 640 eventos; 8 bancos equivalentes em esquema e linhas; **215 testes nativos** e **5 falsificações rejeitadas** | Os 17 contratos terminais continuam sem certificação; casos Stage12 com fontes originais ausentes seguem HOLD |
| **LEVEL-UP R216-P12** | **184 testes dirigidos**, **2.026 testes históricos** em 55 módulos / 8 grupos e aviso de **25 campos de ataque/dano P12 com apresentação incorreta** | Verde significa que o motor P12 passou e que os 25 problemas foram reconhecidos; **não significa que a apresentação P13 foi testada ou que as fichas foram corrigidas**. Os 184 se sobrepõem à bateria histórica |
| **DMG C29** | 38 verificações matemáticas + 5 de consistência, 10 saídas históricas equivalentes e 5 testes de adulteração | Não é validação geral de todas as técnicas, fontes ou regras de dano |
| **CRAFT F5/B30** | 10 testes do mecanismo original que nega autorizações indevidas | Não executa a fábrica inteira nem homologa os 46 casos completos |

**[Ver auditoria DMG + CRAFT](https://github.com/arthof09-ai/assimilat-rpg-integracao-test/actions/workflows/audit-smoke.yml)**

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

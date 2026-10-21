# Bancada técnica do RPG Assimilação — TEST / GitHub gratuito

Apoio ao [laboratório independente](https://app.notion.com/p/400c2b324ede816e8bccef35bd18f3da) do Mestre. **Notion continua como fonte de verdade**; este GitHub armazena cópias TEST e executa testes sem direito de escrever nos sistemas oficiais.

## O que já está funcionando

1. **Auditor ZIP:** [scripts/audit_zip.py](../scripts/audit_zip.py) valida manifestos, CRC e caminhos em arquivos fornecidos localmente. Oito testes sintéticos estão em [tests/test_archive_audit.py](../tests/test_archive_audit.py).
2. **Replay real e nativo do DMG C29:** [experiments/dmg_c29/README.md](../experiments/dmg_c29/README.md) documenta os **dois scripts originais** do C29, preservados sem alteração de bytes em cópia compacta. O runner [tests/run_dmg_c29_native.py](../tests/run_dmg_c29_native.py) confere SHA-256, reproduz **43 verificações (38 matemáticas e 5 de consistência documental)** e valida que **10 arquivos derivados são byte-idênticos aos históricos**. `F0=4/8 HOLD`, `A5=0/7 HOLD`, sem alteração canônica.
3. **Cinco regressões de integridade:** [tests/test_dmg_c29_guards.py](../tests/test_dmg_c29_guards.py) executa o caso válido e demonstra rejeição de bundle adulterado, script com hash incorreto, saída indevidamente alterada e ausência do arquivo. Nenhum teste autoriza alteração de produção.

## Evidência e reprodução

- GitHub Actions em [Test Integrity Auditor](../.github/workflows/audit-smoke.yml) faz as verificações em runner temporário com acesso **somente leitura** ao repositório e sem credenciais Notion.
- [PR #1](../../pull/1): CI remoto sucesso na execução **#10**, incorporado à `main`. A etapa DMG nativa passou.
- [PR #2](../../pull/2): CI remoto sucesso na execução **#13**, incorporado à `main`. Os cinco testes de regressão passaram junto com as etapas anteriores.
- No computador/runner com Python, use `python -I -B -m unittest discover -s tests -v` e `python -I -B tests/run_dmg_c29_native.py`. Pelo celular Android, basta acompanhar o painel **Actions**; não é necessário executar Python manualmente.

## Escopo e limitações

- O GitHub não executa as operações completas VLAB/CRAFT/LEVEL-UP e não substitui uma instância de Comestre nem garante trabalho autônomo de 30–60 minutos.
- Replit está **SUSPENSO SEM PRAZO** por decisão do Mestre: não esperar cota mensal, não pagar assinatura e não torná-lo obrigatório.
- Nunca mover/alterar a origem, Party, O Primeiro, outros laboratórios ou cânone. O status PASS só qualifica os testes concretamente executados e observados.
- Alterações devem seguir [diretriz GH-RP-01](https://app.notion.com/p/400c2b324ede8147bc9af2160e0b1a8e), [Diário em alternantes](https://app.notion.com/p/400c2b324ede8102ad79e3c9d54a34ef) e [AGENTS.md](../AGENTS.md), sempre com readback e próximo passo recuperável.

**Sem custo adicional contratado. Execução sujeita aos limites gratuitos do GitHub Actions.**

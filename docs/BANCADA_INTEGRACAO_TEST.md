# Bancada de integridade do RPG Assimilação — TEST

Este repositório é o **apoio técnico** ao laboratório independente GitHub + Replit do Mestre no Notion: https://app.notion.com/p/400c2b324ede816e8bccef35bd18f3da

## Objetivo
Rodar testes reproduzíveis de integridade de pacotes em GitHub Actions, sem criar nem substituir motores VLAB, DMG, CRAFT ou LEVEL-UP.

## Restrições
- O auditor só lê os ZIPs locais fornecidos deliberadamente; não executa o código contido neles, não extrai arquivos, não consulta APIs e não grava no Notion.
- Os testes automáticos deste repositório são **inteiramente sintéticos**. Os ZIPs originais não são publicados aqui.
- O resultado PASS comprova integridade estrutural; não certifica a qualidade mecânica, nem promove um resultado ao cânone.
- GitHub Actions usa permissão **somente de leitura** para conteúdo do repositório.
- Operações de outros Comestres e Party permanecem **fora do perímetro de escrita**.

## Teste local reproduzido em 21/10/2026
- **8/8 testes sintéticos PASS** usando Python standard library.
- Auditor ZIP executado em **quatro cópias locais** de artefatos do Mestre, hashes internos **299/299 VLAB R237; 331/331 LEVEL-UP R216P11; 18/18 DMG C29; 9/9 CRAFT F5/B30**.
- Os artefatos originais e os recibos de seus Comestres continuam na Biblioteca/Notion do Mestre; a gravação do código aqui é a **primeira integração remota**, não o transporte desses motores.
- A execução **GitHub Actions** exige verificação independente do status no painel Actions; não declarar PASS remoto antes de observar logs/status.

## Reprodução
Execute `python -m unittest discover -s tests -v`; opcionalmente rode o script `scripts/audit_zip.py` sobre uma cópia local de ZIP com manifesto.

## Fronteiras de progresso
1. GitHub privado com arquivos e workflow testados.
2. Verificar execução remota de Actions.
3. Replit com demonstração sintética de checkpoint/retomada, sem acesso de escrita externo.
4. Registrar evidências no laboratório independente, sem tocar laboratórios vizinhos.

**Estado:** TEST; sem direito de alterar produção/Party/O Primeiro.
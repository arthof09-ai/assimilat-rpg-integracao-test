# Integração Claude ↔ ChatGPT/Codex — RPG Assimilação

**Índice técnico público; não substitui as normas canônicas do Notion.** Atualizado em 27/10/2026.

## Responsabilidades das plataformas

| Plataforma | Responsabilidade |
| --- | --- |
| Notion Mestre | Fonte de verdade para regras, decisões, operações e rastreabilidade |
| GitHub | Código, testes, commits, branches, PRs e integração |
| Google Drive | ZIPs, modelos, mídias e backups recuperáveis |
| Windows | Godot, Blender, arquivos de produção e testes locais |
| Claude / ChatGPT / Codex | Agentes de execução e coordenação conforme autorização do Mestre, com escopos de edição reais |

O **Mestre** designou Claude e ChatGPT com **autoridade funcional equivalente de coordenação**; isso não dá automaticamente acesso técnico, writer, lease, epoch ou a mesma instância. A identidade institucional Claude foi registrada como **CM-000008**, subordinada à ID-COMESTRE-01.

## Portas de entrada

- [Portal do Jogo 2.5D](https://app.notion.com/p/406c2b324ede81548b70e872c64d29a0)
- [Onboarding do Claude CM-000008 v1.0](https://app.notion.com/p/406c2b324ede81d1a297ca9c3f4e8c63)
- [Quadro de Continuidade Compartilhada](https://app.notion.com/p/406c2b324ede81459c57f4cef02620b1)
- [Registro Mestre de Identidades](https://app.notion.com/p/3f1c2b324ede8165bf92d95e4af89f77)
- [Laboratório do Inovador](https://app.notion.com/p/401c2b324ede809585d3d1907c194df9)
- [Laboratório do Claude](https://app.notion.com/p/400c2b324ede80d294c2ddf8b7d337cb)
- [Drive — Código-Mãe VLAB R315 a R326](https://drive.google.com/drive/folders/1dV_oQjtRVHRp0KA3FSJX5Wt1EqPrVW_3)
- [Drive — manifesto dos 12 ZIPs](https://drive.google.com/file/d/1eIqx3FWb3Vi3rvcNGN7pJ-KP0fFzWMVP/view)

## Regras de integração de código

1. Conferir `git status`, `remote`, HEAD e branch antes de escrever. Não usar reset destrutivo nem forçar push sobre arquivos de outros agentes.
2. Cada executor trabalha em branch ou worktree isolado, com diff, testes e commit. A integração é feita após inspeção e gates aplicáveis; não alterar o motor VLAB oficial por desconhecimento.
3. Fonte do jogo e testes versionados aqui; ZIPs/SQLite grandes mantidos preferencialmente no Drive com hash/manifesto. O GitHub é público por escolha do Mestre, sem impor bloqueio genérico de publicação de código.
4. R326 é o pacote posterior a R325, mas o manifesto interno da R326 exige reconciliação: três divergências de hash em README_MESTRE_ONLY.md, index.html e manifest.json. ZIP do Drive = ZIP Biblioteca por SHA-256 conforme conferência independente. Isso **não** é terminal PASS do VLAB.
5. Todo handoff deve indicar `LAST-VERIFIED`, `FIRST-PENDING`, `NEXT`, `NO-REPEAT`, links dos arquivos, testes, escopo de escrita e backup efetivo.
6. Normas, status oficial de R326, decisões de combate e direitos das operações permanecem no Notion autorizado. Não criar normas ou fontes mecânicas concorrentes.

## Primeiro teste de acesso do Claude

Ler o onboarding completo no Notion. Validar separadamente Notion, Drive, GitHub e acesso aos arquivos Windows pelo aplicativo Claude Desktop/Claude Code/Cowork. Acesso ao GitHub ou Drive **não** prova acesso ao disco do notebook. Registrar o que foi de fato aberto, não presumir que o Claude já leu esta página.

**Esta página é apenas o ponteiro público. Não contém cópia do motor, arquivos da campanha ou credenciais.**

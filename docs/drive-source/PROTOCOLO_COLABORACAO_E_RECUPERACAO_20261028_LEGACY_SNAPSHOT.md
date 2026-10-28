> **MIRROR DO DRIVE RPG, com redações de política supersedidas anotadas; não é novo cânone nem prova de execução.** Origem: https://drive.google.com/file/d/1PzO1TYp0uxjoZvDsTW-GzlSnp0tOfnSb/view (acesso à conta autorizada). Capturado 28/10/2026. Decisão expressa do Mestre em 28/10/2026 prevalece sobre restrição antiga ao GitHub público.

# Oficina e arquivo persistente — RPG Assimilação

WRITER / SCOPE: decisão do Mestre; execução técnica Codex nas cópias, evidências e derivado TEST próprio. Nenhuma identidade COMESTRE, lease ou aprovação de produção é herdada deste documento.

O Drive privado da conta [EMAIL_SUPRIMIDO] é o arquivo principal. Notebook mantém Godot, Blender, código e assets ativos. GitHub recebe códigos e artefatos técnicos Mestre-side, conforme decisão expressa de 28/10/2026, inclusive no repositório público; Notion mantém o cânone e a governança. [REDAÇÃO HISTÓRICA ANTERIOR SUPERADA: vedação genérica de Mestre-only.] O nome PARTY da conta Google não autoriza compartilhar com jogadoras.

## Entradas reais

- [Raiz RPG nova](https://drive.google.com/drive/folders/1tii1iub3gNaK1CBTbC-5n0jNjUA-hzB4).
- [Central e continuidade](https://drive.google.com/drive/folders/18Kg2z45qhG3R9GoSQhrQZYLyuasQpCHX).
- [Preservação Windows e versões](https://drive.google.com/drive/folders/1_UZV48WjlmLF_O-Gny94Bkw-quFTj4_9).
- [Jogo interativo](https://drive.google.com/drive/folders/1GtWvDoD_c_FPWtMF7zFfBblHKMVZbFe5).
- [Área Codex no Notion](https://app.notion.com/p/406c2b324ede81bea8cbd7368542908c) e [quadro de continuidade](https://app.notion.com/p/406c2b324ede81459c57f4cef02620b1).

## Escrita e integração

1. Mestre decide prioridades e promoção de resultados. Notion não é substituído por arquivos de backup.
2. Codex escreve em sua área 03_CODEX e nos registros desta migração. Claude mantém sua área Claude-Assimilacao. Ler uma área não concede permissão para sobrescrevê-la.
3. Antes de integrar: registrar responsável, arquivos, branch/commit, hash de entrada e janela de edição no quadro autorizado. Um escritor por arquivo. Em conflito, preservar ambas as versões, comparar o diff e pedir decisão sobre a integração específica.
4. Trabalhar em cópia local funcional. Não editar projeto Godot/Blender de produção por streaming instável. Reutilizar o motor VLAB oficial e os fontes existentes.
5. Entrega gera versão imutável com manifesto, hashes, testes e recibos. Só atualizar o índice de versão corrente depois do readback. Não criar projeto oficial concorrente nem sobrescrever arquivos mais novos.
6. Publicação pública, deploy e compartilhamento às players exigem seu escopo próprio. Credenciais OAuth ficam privadas no Windows e nunca entram em Drive, Git, Notion ou pacotes.

## Recuperar em outro ambiente autorizado

Codex Cloud e Claude não possuem acesso presumido ao disco do notebook. Usar a própria conexão autorizada com o Drive ou o repositório GitHub apropriado. Acessar a raiz nova com a credencial antiga pode retornar404; isso não prova ausência.

Na preservação Windows, cada LIVE_VERSIONS contém FILES.json e RECEIPT.json. Conferir o SHA-256 do manifesto contra o recibo. Escolher apenas os caminhos necessários à tarefa e criar destino local novo. Cada registro descreve uma das representações:

- binary: baixar o ID apontado, validar tamanho/SHA-256 e materializar o caminho relativo original.
- ordered_parts: baixar as partes na ordem indexada, conferir cada SHA, concatenar sem gerar cópias intermediárias desnecessárias e conferir SHA/tamanho integrais.
- verified_zip_member: usar o ZIP identificado por ID e SHA-256, conferir seus bytes e recuperar o membro indicado; conferir o SHA do arquivo final. Os ZIPs VLAB existentes são reaproveitados dessa forma.
- cloud_zip_member: usar as 15 partes Cloud existentes identificadas no recibo, verificar hashes, abrir o ZIP concatenado e extrair somente o membro indicado. É possível recuperar por Range sem baixar todo o ZIP, se a ferramenta suportar; sempre conferir o hash do arquivo extraído.

Não usar nomes/tamanhos como prova de igualdade. Não tratar atalhos ou permissões de leitura da conta antiga como preservação independente. As cópias verificadas desta operação pertencem à conta RPG nova e são privadas.

Diretórios e nomes relativos do manifesto são dados: rejeitar caminhos absolutos, .. e escapes fora do destino. Não executar scripts recuperados automaticamente. Instalações Windows não são ambientes executáveis Linux; código e assets precisam das ferramentas do ambiente de destino.

## Backup e espaço

Assimilacao-Checkpoint-Local é uma tarefa nativa Windows de30min, usuário interativo. Não depende de Codex/Claude; precisa de computador ligado, usuário logado, runtime, rede e credencial válidos. Consultar último recibo, escopos e código de saída; tarefa registrada não equivale a sucesso remoto.

Blobs novos locais têm reserva7GiB/teto2GiB; sem poda automática. Backup remoto usa CAS por hash, referências verificadas e metadados locais pequenos com teto64MiB. Backups remotos anteriores são imutáveis. Um gate HOLD não permite apagar conteúdo para forçar conclusão.

O cliente compartilhado do rclone apresenta403 rateLimitExceeded intermitente e aviso de retirada em2026. Há retentativas limitadas e logs. Uma credencial OAuth própria do projeto será necessária se esse cliente deixar de funcionar; não pedir ou publicar segredos no chat.

## Continuidade

LAST-VERIFIED: consultar CHECKPOINT_VIVO.md, GATES_MIGRACAO.json e recibos atuais. A restauração completa de2340arquivos/2474320927bytes corresponde ao corte congelado20261027T225942Z-549ea49d. Um caminho duplicado foi materializado por hardlink no TEST isolado; isso não demonstra duas cópias editáveis independentes.

FIRST-PENDING: fechar os gates aindaHOLD. NEXT: recuperar apenas o escopo da tarefa, validar e registrar novo resultado. NO-REPEAT: migração cega, censo já concluído, novo VLAB, originais apagados ou dados privados publicados. PASS / HOLD: nenhum resultado deste protocolo certifica produção ou sucessão perfeita por si só.

Fechamento de28/10/2026: rotina remota nativa testada no Agendador com código0; quatro classes de recuperação real PASS. Limpeza local permanece HOLD por bloqueio automático e indisponibilidade física do Mestre. Relatório/manifestos estão na pasta07_RELATORIOS_E_AUDITORIAS.

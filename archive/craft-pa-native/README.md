# CRAFT + PA — consulta nativa recuperada, 29/10/2026

Pacote de consulta assistida do Mestre. A bancada QMC-05 real lê o texto de uma ficha e chama o adaptador R28, a ponte R27 e o fornecedor R26 originais. Nenhuma tarifa foi reimplementada. Não fabrica estoque, não altera Notion e não decide cânone automaticamente.

## Usar

Requer apenas Python 3.11 ou superior, sem instalar dependências.

```sh
python verify_release.py
python CRAFT-QMC04/QMC-05/qmc05.py --url https://app.notion.com/p/3edc2b324ede816f98a1fa7babd3c0d3 --readback live-inputs/lamina.txt --pa-r28
```

Para consulta nova, obter a página viva pelo conector Notion, salvar o retorno textual e usar a URL canônica da própria página. O texto salvo é evidência da leitura observada, não assinatura da plataforma nem prova de atualização futura. Os três arquivos em `live-inputs/` foram lidos em 29/10/2026; o conteúdo pode ser anterior conforme o `as_of` da própria fonte. A consulta histórica preserva os custos antigos e os campos desconhecidos.

Um projeto novo pode usar a interface estruturada de `provider_r27/ponte_pa_craft_r27.py`; o exemplo `fixture_craft_acessorio.json` já acompanha o fornecedor. Validar classificação e mecanismo com as fontes antes de interpretar seu cenário de PA. Bônus, efeito, preço, custo autorizado e PA efetivamente gasto são coisas diferentes.

## Reprodução verificável

`verify_release.py` confere o manifesto do pacote e executa 149 testes: 48 originais PA R26/R27; 47 da bancada QMC-05; 8 de aceitação da ligação nativa e de três leituras recentes; 46 do consumidor read-only R03, em extração temporária com os fontes R26/R51 congelados. A cópia da fonte R26 dentro de R27 mantém SHA256 `7d18b43220c18e3797c9e5bac3532392ac10a30f976911c1e259e1117b13c3a8`.

O patch de QMC-05 acrescenta somente os argumentos de consulta `--pa-r28` e `--pa-projeto-json` e a chamada ao adaptador. O modo anterior continua disponível. O adaptador e a versão de QMC-05 com esse patch foram recuperados dos componentes arquivados no mesmo commit dos demais pacotes.

## Fontes

- GitHub: `arthof09-ai/assimilat-rpg-integracao-test`, commit de recuperação `ee50b5b4932a3a4a7dd79a1292b116c3f6e36050`.
- Baseline QMC-05: ZIP SHA256 `f2471657eed68b7349518d0a7d902004bd6969e1add7fc0b29741957675a52ff`, 128/128 arquivos verificados antes da montagem; recuperado do baseline DELTA01 preservado em DELTA02.
- PA R27: ZIP SHA256 `912db6db289d0e90e6fd4e824c7028b7af5fe05ad2934d4ac07df563ebdfab9d`, 102/102 arquivos do manifesto verificados na recuperação.
- Consumidor R03: ZIP SHA256 `cf96100598169f831af2d70d0b03c00754ac91ccc6e0d4fcb08e07391230e9db`.
- Fontes operacionais: https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516 ; perfil de fabricação https://app.notion.com/p/3eec2b324ede81ecb058f59f5b67e4f4 ; biblioteca https://app.notion.com/p/407c2b324ede8199b616cb8a99750584 .

## Interpretação dos resultados

`null` permanece desconhecido. As classificações automáticas são pareceres e exigem revisão; a recuperação e os testes não provam acurácia universal. Os indicadores TEST/HOLD dos fornecedores históricos descrevem a ausência de fabricação e de publicação por essas APIs read-only; não são uma ordem para bloquear novamente a operação de mesa liberada no Notion.

Este pacote conclui a entrega técnica da consulta nativa para o fluxo assistido. Fabricação em mesa continua pelo perfil de PR-ITEM-02 e pela versão da receita, com conhecimento, insumos, ferramentas, energia, teste e registro do resultado. PS de projeto não se transforma em fabricação passada, conhecimento Player ou P4 por cálculo de PA.

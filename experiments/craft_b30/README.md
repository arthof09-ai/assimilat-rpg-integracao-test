# CRAFT F5/B30 — admissão negativa de evidências (TEST)

**Não é outro motor de fabricação.** Este experimento importa, sem mudar bytes, a função `evidence_row` do código original `code/dual_replay.py` do pacote `CRAFT_F5_B30_DUAL_REPLAY_GATE_20261021.zip` (SHA-256 `706d38ac23c09044a2567d55d099eedc2ae631fe68f4288b31c68efac28ad825`).

A cópia congelada do módulo está em `original_evidence_gate.xz.b64`. A suíte valida os hashes do pacote e da origem antes de importar esse módulo em diretório temporário. **Não carrega nenhum dos três ZIPs de baseline, não executa a função composed(), não usa Notion e não cria receitas, RC5 ou escritor de produção.**

### O que realmente foi testado

Em [tests/test_craft_b30_gate.py](../../tests/test_craft_b30_gate.py), dez testes conferem as negações de admissão para candidatos B30-06 e B30-13:

- Mesmo com oito campos declarados verdadeiros, continua `EXTERNAL_REVIEW_REQUIRED_NO_AUTOCANON`, com `actual_writer_verified=false`, `physical_efficacy_verified=false`, efeitos materiais zero e sem REC-ID.
- Entrada vazia, candidato desconhecido, estrutura nula, campos extras, falso booleano e autoatribuição `RC5_PASS` não liberam a produção.
- Saída determinística, sem escrita na Party ou O Primeiro.

### Resultado e limites

Os **10/10 testes passaram localmente**. A execução automática remota depende de confirmação do GitHub Actions no PR associado.

**Importante:** a bateria completa de 46 testes do pacote CRAFT **não foi movida nem reproduzida pelo CI**. O trabalho atual prova apenas o portão original de admissão de evidências, sem medições físicas, sem germinação/sorção e sem direito de alterar o laboratório CRAFT.

As regras e o registro operacional continuam no [Laboratório independente do Notion](https://app.notion.com/p/400c2b324ede816e8bccef35bd18f3da). Estado: **TEST / PRODUÇÃO HOLD**.

# CRAFT R47 — Recibo Mestre-side / CM-000002-I0016

**Artefato entregue:** `CRAFT-R47-I0016-AUTENTICIDADE-CUSTODIA-v02.zip`  
**SHA-256:** `be76bc7ea2218dce388b1197797d6015891b3bbb1801351f99a2b49bab56252e`  
**Tamanho:** 2.719.996 bytes  
**Integridade:** ZIP CRC PASS, manifesto 138/138, R46 expandido 103/103, ZIP R46 original SHA `966e137b5092b419e8a94804c97711d36ba0f119a96ba212cf53d0a1953b25f4`; inclui intactos R45 e R44.

**Testes em extração limpa:** regressões R44 52/52, R45 64/64, R46 70/70, novos R47 87/87; replay de 8/8 SHA dos outputs/snapshots; 120 operações sintéticas de stress, 260 mutações em quarentena, quatro processos de teste compartilhando filesystem com cinco commits verificados (um ACK perdido resolvido sem efeito duplicado). Nenhum teste demonstrou credencial externa legítima, medição física ou exclusividade Notion.

**Readback Notion:** `CP-CRAFT-I0016-R47-ANTES-001` e `CP-CRAFT-I0016-R47-DEPOIS-002` aparecem no thread documental da OP original e o hash R47 coincide. O corpo da OP não foi modificado por esse registro. [Thread Mestre-side](https://app.notion.com/p/3f1c2b324ede81d7aa79c83106240516?d=3f4c2b324ede81f1a51c001c18ba1040&pvs=42).

**Estado:** duas receitas experimentais preservadas; RC5 0/30; F5 RED; IBX-38 NOVA sem ACK; C19-021 UNKNOWN; fencing externo não demonstrado; NAC-PASS MATERIAL HOLD; Party/O Primeiro 0 alterações; medições físicas verificadas 0. Testes criptográficos usam chaves determinísticas deliberadamente públicas, NÃO são certificação real.

**Handoff R48:** admissão independente de trust roots externos, credenciais reais, timestamps e revogação independente; manter quarentena enquanto faltar prova. Restaurar motor R47 com SHA do trust policy e HEAD externo, sem reiniciar R44–R46 nem assumir writer F5.

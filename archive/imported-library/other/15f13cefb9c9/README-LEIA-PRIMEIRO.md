# Oficina CRAFT do Mestre — v02 | fabricação em lote

A Oficina CRAFT é uma **ferramenta local experimental**, com o **motor R48 original e inalterado** (ele utiliza R44 + R47). Todos os lotes, laudos, medições, estoques, recibos, custos e produtos são **fictícios**. Ela não consulta ou escreve no Notion; não adiciona nenhum item à Party nem cria REC-ID.

## Abrir em três passos — sem programar

1. **Extraia o ZIP inteiro** em uma pasta no computador, por exemplo `C:\CRAFT` no Windows. Não execute diretamente dentro do ZIP nem mova arquivos individuais para fora da pasta.
2. **Windows:** clique duas vezes em `INICIAR_CRAFT.bat` (requer Python 3.10+; na primeira execução a biblioteca `cryptography` poderá ser instalada). **Mac/Linux:** rode `./INICIAR_CRAFT.sh` em um terminal na pasta extraída. O script inicia o servidor **somente no próprio computador**.
3. Seu navegador poderá abrir automaticamente. Caso não abra, entre em **http://127.0.0.1:8765**. Clique **Criar estoque e começar** e depois **Planejar lote** no menu. Alternativamente, entre direto em **Planejar lote** e clique **Criar cenário fictício 3+2 pronto** para preencher o estoque de demonstração automaticamente.

**Você não precisa editar código, JSON, scripts ou laudos.** As assinaturas digitais usadas nos testes são sintéticas, com chaves de TESTE, sem validade como laboratório real.

## Faça um lote de 3 tábuas e 2 pares de mica

1. No formulário inicial de estoque, coloque **8** em `Ardósia apta`, **8** em `Mica A` e **8** em `Mica B`. Os demais saldos podem ficar como aparecem. Clique **Criar estoque e começar**.
2. Abra **Planejar lote**. Em **B30-01**, escolha `3` tentativas; em **B30-03**, escolha `2` (cada tentativa produz um **par** de espaçadores, ou 2 peças).
3. Use os lotes fictícios aptos selecionados por padrão. Deixe **QA de teste aprovada**.
4. Clique **Conferir necessidade, custo e estoque**. A prévia deve mostrar 3 lâminas de Ardósia + 2 folhas Mica A + 2 folhas Mica B; exibirá **MED indisponível**, porque custo canônico não está comprovado.
5. Escolha **Confirmar lote e registrar no R48** ou **Cancelar plano SEM consumir**. Se confirmar, o resultado esperado é **3 tábuas e 2 pares (4 espaçadores)** = **7 peças fictícias**, processadas em **5 tentativas dentro de um único commit local R48**. A prévia, sozinha, NÃO consome estoque. **Cancelar** marca o planejamento como cancelado e impede que ele seja confirmado mais tarde.
6. Veja o **Resumo do lote**, os cinco **recibos individuais JSON**, o **recibo completo**, as etapas de QA, o estoque antes/depois e o **Histórico**.
7. Feche o programa e abra novamente com `INICIAR_CRAFT`. A sessão é recuperada automaticamente de `SESSOES-FICTICIAS/`. Em **Sessões**, escolha uma sessão anterior se desejar.

### Experimente falha, repetição e reversão

- **Estoque insuficiente:** em **Início**, crie **nova sessão** com Ardósia apta = 0, planeje 3 tábuas e confira. O botão de confirmar lote não aparece; mesmo um POST direto é recusado. Nada é consumido.
- **QA inválida:** no planejador selecione **Simular 1 laudo reprovado/quarentenado**. Confirme apenas se a prévia mostrar a reprovação. O R46/R47/R48 determinam o status e o débito; para o fixture demonstrado, `QUARANTINE_EVIDENCE`, 0 produto e 0 consumo nessa tentativa. Se houver outras tentativas aprovadas, o lote pode ser **misto**; essa composição fica explícita.
- **Repetir:** no resumo ou no recibo, clique **Repetir mesma operação**. O motor identifica o lote já existente e não consome novamente.
- **Reverter:** em **Início**, clique **Reverter último lote fictício**. O aplicativo cria uma **nova sessão derivada do checkpoint anterior**, preservando a sessão original, o histórico e os comprovantes. Para reencontrar a anterior, use **Sessões**.
- **Adicionar lote fictício:** em **Planejar lote**, escolha **Adicionar um lote fictício para testes**. Como R48 **não tem evento de entrada de estoque em um ledger existente**, a interface cria uma **nova sessão independente** a partir dos saldos atuais acrescida do lote de teste. Produtos/commits da sessão anterior não são copiados; ela continua integralmente recuperável em **Sessões**. Esta operação não é reabastecimento produtivo.

## O que mudou da v01 para a v02

| Comportamento | v01 | v02 |
|---|---|---|
| Tentativa individual B30-01 / B30-03 | Sim | Preservada |
| Pedido de 3 tábuas + 2 pares em uma única confirmação | Não na interface | **Sim**, até 16 tentativas no R48 |
| Planejar total por lote e alertar insuficiência | Uma tentativa por vez | **Somatório e projeção do motor R48** |
| Confirmar ou cancelar depois da prévia | Individual | **Lote completo com HEAD/versão conferido e cancelamento persistente sem débito** |
| Resumo e recibos individuais de pedidos dentro de um lote | Não | **Sim** |
| Estoque fictício adicional sem alterar ledger antigo | Recriar sessão manual | **Nova sessão derivada com lote adicional** |
| Custos MED sem fontes suficientes | Fórmula simbólica | **Indisponível** destacado |
| Persistência, histórico, reversão por fork | Sim | Preservados |

## Limitações reais e segurança

- O engine original R48 realiza a **transação de até 16 tentativas** com confirmação **atômica do estado do lote**. Isso **não** garante sucesso de todas as tentativas: pode haver lote confirmado com algumas recusas/QA reprovada. A interface bloqueia confirmação com **estoque insuficiente** na prévia; uma reprovação de QA pode ser demonstrada intencionalmente com aviso claro.
- A prévia é um **ensaio isolado pelo motor R48 original**, não um cálculo mecânico paralelo nem uma reserva duradoura. Ela registra o `HEAD` do ledger; se outro pedido for confirmado antes, a confirmação antiga é recusada como **prévia desatualizada**. O contrato R48 mantém idempotência por ID de lote e hash do pedido.
- R48 não contém **reabastecimento de estoque em sessão já iniciada**. Adicionar um lote na v02 cria outra sessão (o histórico da antiga permanece). Rendimento e refugo reportados pelo R48 valem apenas para fixtures; valores geométricos e tempos são parâmetros propostos e não medições reais.
- O app usa somente a interface `127.0.0.1`, acessível no computador que o hospeda. Não é um `EXE` standalone; requer Python 3.10+ e `cryptography`. No Android não instala diretamente sem ambiente capaz de rodar servidor Python.
- Os únicos projetos de receita integrados são **B30-01** e **B30-03**. Não há 3ª receita com documentação suficiente adicionada por conveniência.
- A UAT humana é **PENDENTE**: os testes são HTTP automatizados. Para homologar a experiência do Mestre, é necessário utilizá-la de fato no computador.
- Separação oficial: **gaps F5 0/26, RC5 oficiais 0/30, F5 RED, C19-021 UNKNOWN-SIDE-EFFECT, NAC-PASS material HOLD**. Nenhuma alteração em Party/O Primeiro, fichas PS, REC-LIB, recursos e estoques oficiais.

## Arquivos importantes

- `INICIAR_CRAFT.bat`, `INICIAR_CRAFT.sh` — inicializadores **v02**.
- `oficina_v02.py` — interface em lote sobre o `app.py` v01 preservado (sem engine próprio).
- `app.py` — interface anterior preservada; pode ser aberta independentemente via `python app.py`.
- `CRAFT-R48-SANDBOX-I0016/` — motor **original** não modificado.
- `testes/test_lotes_v02.py` — testes específicos da camada nova.
- `demonstracoes/v02/demo_lotes_v02_http.py` — prova dos cenários A–F por HTTP real; evidência distribuída em `demonstracoes/v02/resultados_lotes_v02.json` e novas execuções em `SESSOES-FICTICIAS/demonstracoes/`, sem sobrescrever a prova original.
- `historico/CRAFT-OFICINA-MESTRE-v01.zip` — **pacote v01 original**, dentro do ZIP v02, verificado pelo hash esperado.
- `historico/CRAFT-R52-I0016-DESBLOQUEIO-COORDENADO-v01.zip` e `historico/CRAFT-R48-I0016-FABRICA-INTEGRADA-v01.zip` — originais preservados; R01–R52 estão preservados na cadeia anterior.
- `MANIFEST-SHA256.json` e `verificar_pacote.py` — integridade do pacote v02.

### Modo avançado (opcional)

```bash
python -m pip install -r requirements.txt
python oficina_v02.py --port 8765 --data ./SESSOES-FICTICIAS
python -m unittest discover -s testes -p 'test_lotes_v02.py' -v
python demonstracoes/v02/demo_lotes_v02_http.py
```

**Próximo incremento recomendado:** após UAT humana, permitir escolher ordens variadas na mesma carteira com QA editável por unidade e uma simulação explícita de recuperação diante de falha de energia. **Não é necessário recriar os motores para isso.**

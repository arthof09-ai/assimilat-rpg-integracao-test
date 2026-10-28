# VLAB R18 — Combate experimental interativo, Mestre-side

> **ENTREGA EXPERIMENTAL / NÃO CANÔNICA.** A interface é um adaptador aditivo para o **VLAB R17 original**. Não grava em Notion, Party, O Primeiro, fichas, catálogos, nem recursos oficiais. `CM-000006-I0001`, writer, epoch, lease, fencing, GREEN, NAC-PASS terminal e 17/17 certificações **NÃO** são reivindicados. Estado oficial permanece **0/17** contratos terminais. A v0.9 original não foi recuperada.

## Como abrir e jogar (sem programar)

1. **Extraia o arquivo ZIP inteiro**, mantendo a estrutura de pastas. Não execute programas de dentro da janela do ZIP compactado.
2. **Windows:** dê dois cliques em `START_VLAB.bat`. **Linux/macOS:** abra o Terminal na pasta e execute `./START_VLAB.sh` (ou `sh START_VLAB.sh`). É necessário **Python 3.10 ou mais recente** instalado. Não é necessário instalar pacotes Python adicionais nem acessar a internet.
3. A ferramenta abre uma página no navegador; se não abrir, copie o endereço `http://127.0.0.1:PORTA/` exibido no Terminal.
4. Escolha um de **dois cenários Bronze fictícios** e clique em **Iniciar novo combate**.
5. Em cada turno, selecione **Ataque normal** ou **Passar turno**, confirme o alvo e escolha se o defensor usa **Não reagir**, **Defender** ou **Esquivar**. Clique em **Executar ação**.
6. Confira Vida/Alma, iniciativa, turno, recibos e rolagens. Execute até algum combatente chegar a **Vida 0** no experimento.
7. Use **Desfazer última ação** para rollback local, **Recuperar gravação** para readback e **Exportar recibo** para salvar os cálculos. Novo combate preserva o arquivo local do anterior.
8. Para encerrar, feche o Terminal ou pressione **Ctrl+C**. O servidor é limitado a `127.0.0.1` e não transmite os dados do combate pela internet.

**Onde ficam os dados:** `~/VLAB-R18-Experimentos/` (Windows: pasta do usuário, `VLAB-R18-Experimentos`). Há um arquivo JSON por sessão, com decisões, recibos, reversões e hash de integridade. Faça backup dessa pasta se desejar preservar as sessões. A exportação de recibo tem verificação SHA-256; não é assinatura de autoridade canônica.

### Instalação/execução alternativa

```bash
python fusion_stage12/vlab_r18_http_ui.py
```

Para controlar o destino e a porta local:

```bash
python fusion_stage12/vlab_r18_http_ui.py --port 8765 --data-dir /caminho/experimentos
```

O programa **não** instala serviço persistente e não precisa de token Notion. O navegador e o computador executam tudo localmente. Não exponha a porta por proxy nem a abra para a rede pública.

## O que funciona e de onde vêm as regras

- **2 cenários** ficcionais Bronze com fichas de treino isoladas.
- **Iniciativa:** fórmula da página Mestre `Sistema de Combate` para Bronze: `1d6 + DES + bônus de Iniciativa`. Os dados de iniciativa são **pré-fixados no cenário**, com resultados diferentes, porque a regra de desempate ainda não foi decidida. Isto não é implementação do scheduler canônico completo.
- **Ataque:** `1d6 + FOR + Luta` contra CA humana calculada por `6 + DES + Armadura`. A interface rola 1d6 e prepara a entrada; o acerto é determinado no **executor original v0.8.1**, chamado pelo gateway R17.
- **Dano:** `1d6 + bônus FIXTURE`, cortante, RD geral 0. É **hipótese experimental**, não um valor certificado de uma arma ou personagem. Mitigação/HP/registro atômico são resolvidos no **módulo histórico v0.8.1**; a interface não replica esse cálculo.
- **Reação defensiva:** `DEFENDER = 6 + CON + Armadura + Fortitude`; `ESQUIVAR = CA + Reflexo`, consumindo a janela de reação, segundo o efeito v0.8.1 existente. **Não atribui custo de 5 PA à Esquiva.** Um ataque com defesa é uma transação atômica única no gateway original.
- **Turnos:** a interface emite `manual_turn_budget_reset` **somente como declaração externa LAB**, na sequência do cenário, sem decidir empates, múltiplas interrupções ou duração. Uma ação por turno neste MVP; movimento e demais possibilidades não estão conectados.
- **Vitória experimental:** quando a Vida de um dos dois participantes fica em 0. **Não é decisão de morte ou de status canônico.**
- **Persistência e rollback:** escreve um diário JSON de cópia isolada após confirmação da ação; produz um novo estado em memória a partir do diário autenticado e confere os hashes do executor. `UNDO` registra revogação e reconstrói o cenário desde o início **somente dentro do laboratório local**. Nenhum efeito nativo externo é publicado nem repetido. Pedido com `request_id` duplicado recebe resposta deduplicada, sem nova mutação.

### Limites assumidos

O motor existente é preservado; os scripts novos adicionam interface, controle humano, rolagem explícita, cenário e jornal local. **Não** recriam regras de ataque, redução de dano ou reação. v0.9 original indisponível; uso do executor v0.8.1 e de módulos reconstruídos e pinados Stage12. O combate é **LAB_FIXTURE_ONLY**: não certifica nenhum dos 17 contratos terminais nem dá autorização para usar Galidemus, Jaku, Dragão ou fichas reais. Jaku × Dragão, reação 5 PA, desempate de iniciativa, cancelamento e interrupções simultâneas continuam fora dos cenários suportados. Sem infraestrutura cross-host.

## Evidências de teste e reprodutibilidade

A partir da pasta `fusion_stage12`:

```bash
python -m unittest -v test_vlab_r18_interactive
```

A suíte usa a árvore histórica da própria extração, abre um servidor HTTP **local** temporário para testar os endpoints e realiza combates de teste. Ela não acessa o Notion ou a internet.

Teste funcional automatizado adicional:

```bash
python fusion_stage12/run_vlab_r18_interactive_demo.py --output ./VLAB-R18-DEMO-LOCAL
```

O resultado contém um recibo JSON do combate terminado e um relatório de readback. A execução de demonstração automatizada **não** é UAT humana. A UAT com o Mestre permanece pendente até uso real.

## Provedores e fronteira

- Origem histórica: `VLAB_STAGE12_A1A2A3_FUNCTIONAL_R17_SANDBOX.zip`, SHA-256 `30004e72da2d905badfeaab1dc1a3e245d4f3b1bce0227be2e81504589eec6c0`.
- Interfaces históricas chamadas: `fusion_stage12/unified_gateway.py`, `stage11_manual_bridge.py`, `vlab_turn_runtime_v09plus_rebuilt.py`, `vlab_effects_v08.py`, `vlab_rd_v08.py`.
- Arquivos R18 adicionados: `fusion_stage12/vlab_r18_interactive_core.py`, `vlab_r18_http_ui.py`, `vlab_r18_ui.html`, `vlab_r18_ui.js`, `vlab_r18_ui.css`, `run_vlab_r18_interactive_demo.py`, `test_vlab_r18_interactive.py`, `START_VLAB.bat`, `START_VLAB.sh`.
- O R17 é imutável dentro da entrega; os membros do ZIP original devem ser preservados byte a byte no pacote final. Nenhum writer Notion disponível, nenhum ACK de IBX-91/92 presumido. NAC-PASS material: HOLD.

**Próximo passo funcional de maior valor:** permitir importação versionada e só-leitura de uma ficha TESTE fiel ao RPG, após verificar raça, título, equipamento, Espírito, habilidades e fonte dos danos, sem promover a personagem real nem contornar os gates de integração. Após isso, ampliar as opções de combate por habilitação de regras comprovadas.

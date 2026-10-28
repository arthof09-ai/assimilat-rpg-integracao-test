from pathlib import Path
import json,hashlib,subprocess,cv2,re,html
from datetime import date
from PIL import Image
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image as RLImage,PageBreak,KeepTogether,HRFlowable
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
ROOT=Path('/mnt/data/playlist_20261024');REPORTS=ROOT/'reports';REPORTS.mkdir(exist_ok=True)
media={x['stem']:x for x in json.loads((ROOT/'media_manifest.json').read_text())}
D={
'496150':{
 'heading':'Dia 1 — Da folha de sprites ao mapa visual', 'category':'VISUAL / MÉTODO', 'novelty':'DUPLICATA de vídeo anteriormente enviado como 495862.mp4 (mesmo SHA-256 verificado nos checkpoints históricos). Não reabrir uma implementação já examinada.', 'p':1,
 'chronology':[
 ('00:00–00:18','Abertura com floresta 2D, grandes árvores e rio. A cena final é apresentada antes das etapas de construção.'),
 ('00:18–00:49','Solicitação de personagem; aparecem folhas de sprite com várias direções, teste de transparência e recortes de quadros. A tela menciona Claude/ChatGPT, sem comprovar um único pipeline automático.'),
 ('00:49–01:13','Imagens/objetos são incorporados e ajustados; aparecem pedidos de corrigir cortes e remover fundo PNG, com ferramentas de programação assistida.'),
 ('01:13–01:40','O criador contrasta um cenário verde mais cru com personagens animados, sprites de objetos e iteração rápida.'),
 ('01:40–02:24','Mostra evolução de palmeiras, sistema ilustrado de terreno/rios e ambiente com oclusão, rio e nado. Não há demonstração de turno de combate.'),
 ],
 'finding':'A aparência rica não vem de HTML “mágico”: é composição de atlas coerentes, controle de camadas, recortes limpos, terreno e apresentação sobre um jogo iterativamente testado.',
 'transfer':'A Arena deve consumir sprite atlas com direção, FPS, âncora nos pés, alpha e proveniência. Cenários florestais precisam separar solo, água, unidades e copas, preservando a grade tática e o FOV existente.',
 'alternatives':'Claude Code pago não é pré-requisito: manter editor HTML/JS, Codex/ChatGPT já disponíveis quando autorizados, sprites originais e pacotes CC0 sob licença confirmada. A Oficina de Sprites TEST (vídeo 496132 anterior) já validou o formato; reutilizar em vez de reconstruir.',
 'risks':'Sprite de diferentes perspectivas pode variar em escala ou pés; não copiar assets da gravação; sombra/oclusão visual não pode revelar unidades invisíveis nem burlar FOV. Uso de Claude/GPT mostrado não demonstra gratuitamente a mesma experiência.',
 'action':'DESENVOLVEDOR: testar um atlas autoral de 4 direções no renderer de tokens existente do último RUN, com FOV, escala, 49 casas e zoom preservados. Não implementar navegação livre.',
 'accept':'Em TEST Android, alternar orientação do token e caminhar entre duas casas por ação autorizada; conferir que nenhum cálculo VLAB é substituído por quadros de animação.'},
'496165':{
 'heading':'Dia 2 — Fauna, cadeia alimentar e comportamento contextual', 'category':'IA/CRIATURAS / ARTE', 'novelty':'NOVO neste conjunto verificado. Não há prova de que IA comportamental do vídeo use as regras do Assimilação.', 'p':3,
 'chronology':[
 ('00:00–00:22','Fauna brasileira é apresentada em pixel art; folha de sprites da onça gerada/associada ao Gemini, com quadros de corrida/espreita/salto.'),
 ('00:22–00:49','Diagrama animado de cadeia alimentar: onça, queixada, fruto do açaí, palmeira e besouros polinizadores; isto é representação explicativa, não código validado.'),
 ('00:49–01:10','Flores, besouros e árvores ilustram reprodução/frutos e dispersão, com onça e queixada em interações.'),
 ('01:10–01:23','Comportamento do animal: rastrear, espreitar e bandos reagindo em arco; aparece explicitamente a palavra “bugado” para uma situação.'),
 ('01:23–01:50','O criador fala em mundo “infinito”, chunks e folhas; exemplos de tiles revelam padrões visuais e correções.'),
 ],
 'finding':'O diferencial transferível é transformar comportamento em decisões contextuais legíveis (rastrear, espreitar, fugir), acompanhado de efeitos visuais e testes de borda. O vídeo mostra erros assumidos publicamente.',
 'transfer':'Para monstros/NPCs do Assimilação, separar INTENÇÃO TÁTICA do RESULTADO MECÂNICO. Um agente só poderia selecionar entre ações LEGALMENTE OFERECIDAS pelo motor VLAB; a sala valida ator/turno/revisão e aplica recibos oficiais. Exemplos: patrulha, aproximação, procurar cobertura, reagir a aproximação.',
 'alternatives':'Gemini para arte pode ser substituído por sprites próprios, atlas de domínio/CC0 e ferramentas já testadas. Para IA, classificação determinística de prioridades é gratuita em JavaScript/Python, mas precisa de contrato com VLAB e testes adversariais; NÃO criar segundo motor.',
 'risks':'Não copiar predador/presa nem criar sistema ecológico com estatísticas extras; pathfinding e movimentação precisam respeitar terreno legal e economia de ações; viés da IA ou alvos invisíveis causam vazamento Mestre/Party.',
 'action':'PESQUISADOR: especificar contrato `legal_actions` + `chosen_action_id` + justificativa visível só Mestre; confrontar com VLAB tática adaptativa previamente testada, evitando duplicação. Exigir recusa explícita sem legalActions.',
 'accept':'No laboratório com opções artificiais previamente fornecidas, jamais selecionar comando ausente da lista; testes negativos com target não autorizado, turno errado e erro de revisão.'},
'496174':{
 'heading':'Dia 3 — Rios, sementes, relevo e continuidade do mapa', 'category':'MAPAS / REPRODUTIBILIDADE', 'novelty':'NOVO: tem trechos com gráficos concretos de seed, chunks, hidrografia e correção de descontinuidade.', 'p':2,
 'chronology':[
 ('00:00–00:25','O criador compara lago simples com novo rio e mostra geração por seed; apresenta primeiro mapa por grade.'),
 ('00:25–00:53','Mostra rio com zonas de água rasa e funda, animais em margens, calendário de meses e duração dia/noite.'),
 ('00:53–01:22','Expõe problema de rio sem entrada e exemplo de mapa hidrográfico com relevo; o criador diz que regras do mundo geram rios, em vez de desenhá-los um por um.'),
 ('01:22–01:54','Confluência, nascentes, lençol freático, alagamento e fluxo são ilustrados; há demonstração de personagem na água.'),
 ('01:54–02:39','Vídeo mostra chuva, animadores de partículas, cadeia alimentar, riscos de desnivelamento inadequado e emendas entre pedaços do mapa; antes/depois na tela.'),
 ],
 'finding':'Conteúdo com implicação direta para arenas: mapas determinísticos, seed e validação das bordas, especialmente rios e obstáculos não cortados entre chunks.',
 'transfer':'Usar um gerador/validador de cenas como editor, não substituir a Arena. Terrain ID e propriedades de movimentação são canônicos; camada artística pode propor rio e margens, mas o motor VLAB define legalidade de travessia. Rastrear `seed`, `scene_version`, `terrain_kind`, adjacência e bordas entre chunks.',
 'alternatives':'Sem engine 3D paga: mapa 2D do HTML/Canvas existente, algoritmo de conexão de bordas e JSON exportável. Os mapas e seus testes podem ser gerados com Python padrão/JS, desde que o desenvolvedor decida o contrato.',
 'risks':'A geração procedural pode trocar posicionamento tático entre sessões e quebrar alcance/oclusão; mundo “infinito” não é objetivo da primeira batalha. O calendário CG/RS deve vir da regra temporal do RPG, não do relógio fictício do vídeo.',
 'action':'DESENVOLVEDOR: acrescentar opcionalmente `scene_seed` e validador de continuidade de terreno ao editor já existente, com antes/depois visual e teste de save/replay, sem modificar FOV/cálculos.',
 'accept':'Mesmo seed + mesmos parâmetros geram mesmo mapa TEST; bordas A/B coincidem; carregar/salvar não altera posição nem conteúdo da cena existente.'},
'496183':{
 'heading':'Interlúdio — Escolha pública da fauna brasileira', 'category':'COMUNIDADE / CURADORIA', 'novelty':'NOVO, mas é vídeo de chamada/consulta à audiência, não tutorial de programação.', 'p':5,
 'chronology':[
 ('00:00–00:07','Silhueta de animal e pergunta “Que bicho você colocaria num jogo brasileiro?”'),
 ('00:07–00:13','Explica referência a fauna, flora, biomas brasileiros e biodiversidade.'),
 ('00:13–00:30','Pede sugestões sobre próximos animais e apresenta silhouettes; nenhuma demonstração de implementação de combate/IA no vídeo.'),
 ],
 'finding':'Metodologia de feedback comunitário: selecionar prioridades entre várias propostas, validar valor percebido e receber necessidades do público.',
 'transfer':'No Assimilação, a referência é usar um catálogo visual curado pelo Mestre para escolher quais monstros/fichas receberão sprites primeiro; não canonizar criaturas novas por votação de comunidade.',
 'alternatives':'Sem plataforma paga: checklist com prioridades de arte em Notion Mestre ou relatório do Desenvolvedor existente, mantendo referências apenas MESTRE-SIDE.',
 'risks':'Comunidade não decide cânone do RPG, estatísticas, identidade de Party ou segredos do Mestre; não tratar vídeo curto como prova de IA animal avançada.',
 'action':'COORDENAÇÃO: matriz de prioridade de assets com 3 criaturas NPC já autorizadas + estado ARTE PENDENTE, sem duplicar fichas/objetos; revisão pelo Mestre antes de compartilhar imagens.',
 'accept':'Cada asset escolhido referencia ficha canônica, autoria/licença, estado de entrega e teste visível no TEST; não são geradas fichas novas.'},
'496192':{
 'heading':'Dia 4 — Clima, água, umidade e ciclo ambiental', 'category':'APRESENTAÇÃO / ESTADOS AMBIENTAIS', 'novelty':'NOVO: os textos na tela descrevem explicitamente diversas limitações conhecidas no protótipo do criador.', 'p':4,
 'chronology':[
 ('00:00–00:25','O criador faz chuva em código e desenha painéis de calor, umidade e temperatura, além de um sorteio de condições.'),
 ('00:25–00:59','Apresenta vento, frente fria, seca, temperatura, umidade e ciclo dia/noite em mapa gradeado.'),
 ('01:00–01:32','Demonstra sol de tarde, tabela climática por mês, trajetória solar, sombras, floresta influindo na água e seca.'),
 ('01:32–02:02','Chuva/frente fria aparecem com partículas, temperatura e mudança de vento; o estado visual muda no cenário.'),
 ('02:02–02:27','Painel “Ainda tá imperfeito” revela: temperatura não afeta personagem, empurrão é ruído, frente fria é ruído, seca afeta demasiadamente sal. Demonstra correções futuras, não sistema finalizado.'),
 ],
 'finding':'Separar sinais observáveis do cenário (chuva, noite, neblina) dos efeitos de regras. O próprio criador marca limites; isso deve entrar no nosso gate de aceite.',
 'transfer':'Incluir canal `scene.presentation.weather` para aparência e, separadamente, `mechanical_conditions` exclusivamente oriundas do VLAB. Condição “chuva” NÃO passa a reduzir deslocamento ou PA por inferência do frontend.',
 'alternatives':'CSS/JS no HTML existente demonstram dia, chuva e noite sem APIs nem assinaturas; executado neste lote com 31/31 verificações em três viewports. Renderização sem depender de Claude Code, Unity ou cloud.',
 'risks':'Diferenciar calendário canônico do RPG de relógio simulado; clima estético não pode virar informação escondida da Party; filtros escuros não substituem FOV ou invisibilidade do servidor; sobreposição não pode bloquear toques.',
 'action':'DESENVOLVEDOR: revisar o addon isolado `ARENA_TEST36_CAMADAS_AMBIENTAIS_OFFLINE.html` como efeito VISUAL opcional, sem alterar código oficial ou status de mecânicas; priorizar integração da batalha real.',
 'accept':'Dia/chuva/noite alteram apresentação, mas não alteram 49 tiles, entidades, Vida, Alma, PA, status de sala nem ações; 0 requests externos, Android físico só com teste.'},
'496201':{
 'heading':'Dia 5 — Solo, plantas, matéria e trilhas de uso', 'category':'TERRENO / CUSTO-COMPLEXIDADE', 'novelty':'NOVO: demonstra um sistema granular de nutrientes e sua insuficiência; não é necessário para as mecânicas de combate do projeto.', 'p':5,
 'chronology':[
 ('00:00–00:25','Abertura de floresta, crescimento de mato e árvore, água e elementos como N/P/Ca/K representados em ícones.'),
 ('00:25–01:05','Apresenta tipos de solo como areia quartzosa, argila e aluvião de várzea; grade de “uma célula 48×48” com recursos de água e nutrientes.'),
 ('01:05–01:28','Exibe folha apodrecendo, lixiviação/evaporação e uma simulação de orgânico da várzea com e sem cheia por quatro anos.'),
 ('01:28–02:04','Floresta com “serrapilheira”, desgaste por pisoteio e recuperação de trilha em anos; o próprio vídeo mostra variáveis de simulação.'),
 ('02:04–02:36','Mostra fator limitante, perfis de N/água/Ca e painel admitindo que os índices relativos e a taxa de perda da várzea ainda não estão calibrados.'),
 ],
 'finding':'O vídeo mostra como uma ideia simples vira uma simulação extensa de dependências, com riscos de índices não calibrados. É um alerta contra repetir isso no Tabletop antes do combate.',
 'transfer':'Para a Arena, solo significa somente TerrainKind+camada visual e propriedades canônicas. Sistemas de nutrientes, fotossíntese e história do solo são P4, salvo autorização do Mestre e efeitos normativos existentes.',
 'alternatives':'Camadas visual e fichas de terreno simples em HTML/Canvas com assets livres; não necessitam modelo físico-químico, assinaturas nem 3D.',
 'risks':'Não inventar penalidades de lama, crescimento de planta, terrenos novos ou custo de PA; a simulação do vídeo não pode ser usada como regra oficial do RPG.',
 'action':'COORDENAÇÃO: documentar contrato enxuto de tipos de terreno e efeitos visuais, com validação de que scripts não mutam atributos/custos; não propor subsistema eco até a primeira batalha oficial.',
 'accept':'Nenhum parâmetro de nutrientes no motor de combate; o único estado de terreno aplicado à mecânica vem da ficha/regra homologada.'},
'496210':{
 'heading':'Prólogo — Método de prototipagem por etapas e limites gratuitos', 'category':'METODOLOGIA / RISCO DE COTAS', 'novelty':'DUPLICATA integral do arquivo já enviado antes como 495907.mp4 (SHA-256 idêntico segundo checkpoint original). Reutilizar descoberta; não somar relatório como pesquisa inédita.', 'p':2,
 'chronology':[
 ('00:00–00:13','Pergunta como criar um jogo; o criador usa um prompt para pedir protótipo HTML simples primeiro, focado nas mecânicas.'),
 ('00:13–00:23','Mostra grade, caixas e personagens geométricos e um ciclo de teste, ajuste e reteste.'),
 ('00:23–00:49','Solicita aparência pixel art, prompts de imagens e checklist independente de etapas.'),
 ('00:49–01:07','A tela aponta fim de cota gratuita e exportação em ZIP como opção demonstrada.'),
 ('01:07–01:19','Mostra protótipo com recursos posicionados, sem provar motor oficial ou multiplayer.'),
 ],
 'finding':'O ensinamento mais direto para nossa coordenação é que cada entrega precisa ter um ciclo simples jogável, um teste de aceitação e uma mudança observável, antes de mais sofisticação.',
 'transfer':'Aplicar gate antes/depois AO COMBATE: Mestre escolhe token + ação + alvo e recebe resultado VLAB autorizado. Um teste visual offline não satisfaz gate mecânico.',
 'alternatives':'Não depender de plano pago ou do Claude Code. ChatGPT/Codex já presentes, arquivos HTML/JS/zip e revisão TEST permitida; serviços de IA com cota não são requisitos de runtime do jogo.',
 'risks':'Não repetir DEMO de caminhada, cena ecológica ou painel de recibos falsos como se fosse batalha real; prova do vídeo não certifica engenharia ou velocidade do autor.',
 'action':'COORDENAÇÃO+DESENVOLVEDOR: adotar aceite de uma rodada de combate com VLAB apenas quando disponível e sem duplicar motor; UX + turnos, dano e PA com fontes de verdade e sigilo server-side.',
 'accept':'Ação tática executada no TEST sob recibo oficial, resultando em mudanças coerentes e reversão segura; até lá estado HOLD explícito.'},
}

parts=[]
intro='''# Playlist VibeCode — 7 vídeos, 5 episódios inéditos e 2 duplicatas

**Projeto:** RPG Assimilação / Tabletop; **papel:** Coordenador Inovador MESTRE-SIDE; **data da análise:** 24/10/2026.

**Método:** sete MP4 lidos fisicamente; durações/codec/SHA256 via ffprobe/hashlib; 28 quadros por arquivo (196 quadros amostrados) em 14 folhas de contato, cada uma com timestamp. As legendas e letreiros são gravados no próprio vídeo em muitos trechos. Não há faixa separada de legendas, nem transcrição integral feita por ASR. Apenas textos visíveis nos quadros inspecionados foram tratados como observáveis; explicações sobre funcionamento interno só são inferências quando o vídeo não expõe fonte/teste.

**Deduplicação importante:** `496150` tem SHA256 já registrado como vídeo anterior `495862`; `496210` coincide com `495907`. Contam como 7 arquivos recebidos, 5 vídeos de conteúdo novo neste conjunto, 2 obras repetidas. Não criar duplicações normativas nem tratar revisão como descoberta inédita.

**Critério de utilidade:** ganho observável na própria Arena tática com Mestre+Party, ações mecânicas do VLAB e servidor único; melhorias gráficas/cenográficas são subordinadas a esse objetivo. Nunca transferir condições ambientais dos vídeos para cálculos de Vida, Alma, PA, alcance, dano ou FOV.
'''
parts.append(intro)
for stem,rec in D.items():
 m=media[stem]
 secs=m['duration']; dur=f'{int(secs//60)}min{int(secs%60):02d}s'
 lines=[f'# RELATÓRIO INDIVIDUAL — {stem}.mp4',f'## {rec["heading"]}',f'**Duração:** {dur}. **SHA-256:** `{m["sha256"]}`. **Categoria:** {rec["category"]}. **Prioridade para a primeira batalha:** P{rec["p"]}.',f'**Status de novidade:** {rec["novelty"]}',
'\n## Cronologia de evidências visuais (amostragem, não transcrição integral)']
 for timer,desc in rec['chronology']:lines.extend([f'**{timer}:** {desc}'])
 lines.extend(['\n## O que o vídeo comprova e o que NÃO comprova',rec['finding'], 'A observação comprova a apresentação exibida. **Não comprova** código integral disponível, licença de recursos de terceiros, tempo real de implementação, testes no Android, multiplayer, autenticidade da autoridade mecânica ou que a IA tomou decisões reproduzíveis. Falas não lidas diretamente na legenda exibida não são atribuídas como citações.', '\n## Aplicação correta ao RPG Assimilação',rec['transfer'],'\n## Ferramentas, custo e alternativas concretas',rec['alternatives'],'\n## Riscos de compatibilidade, governança e privacidade',rec['risks'],'\n## Entrega técnica à equipe existente',rec['action'],'\n## Critério de aceite mensurável',rec['accept'],'\n## Procedimento seguro de retomada','1. Revalidar o RUN/TEST e as normas canônicas vigentes antes de editar. 2. Executar apenas no laboratório do executor competente. 3. Demonstrar ANTES→DEPOIS com arquivos/testes e proteção Mestre/Party. 4. Reabrir a entrega e conferir integridade, sem canonizar protótipos.','\n## Lacunas e evidência pendente','Sem ASR integral. Para confirmar tutorial verbal específico, dependência, preço ou algoritmo, consultar fala diretamente com fonte e data; não resolver por inferência. TEST e vídeo não provam funcionamento em três Android físicos.','\n---\n'])
 text='\n\n'.join(lines);(REPORTS/f'RELATORIO_{stem}.md').write_text(text);parts.append(text)
Path(ROOT/'SINTese_PLAYLIST_7_VIDEOS.md').write_text('''# Síntese de coordenação — método e prioridades da playlist\n\n'''+intro+'''\n## Avanço cronológico observado\n\n- **Prólogo (496210, duplicata):** mecânica simples primeiro, testes e sprites depois, exportação com custo/cotas em mente.\n- **Dia 1 (496150, duplicata):** animar personagem, tirar fundo de atlas, corrigir recortes, compor cenário de rio.\n- **Dia 2 (496165):** atlas de fauna, estados rastrear/espreitar, cadeia alimentar ilustrativa; há bugs assumidos.\n- **Dia 3 (496174):** seed, água, rios com entrada, confluências, chunks e emendas; mapa precisa ser determinístico.\n- **Interlúdio (496183):** consulta à audiência para priorizar animais, não implementação.\n- **Dia 4 (496192):** clima, temperatura, sol e chuva; o vídeo admite sistemas incompletos.\n- **Dia 5 (496201):** nutrientes e ciclos de solo; demonstra como cresce a complexidade e aparecem variáveis não calibradas.\n\n## Transferência prioritária AO COMBATE do Assimilação\n\n**P0 — Não adiar:** Arena existente deve mostrar comando autorizado e resultado mecânico VLAB com Mestre+players, ação legal, alvo e recibo. A playlist não ensina essa integração, logo não declarar que resolve o bloqueio.\n\n**P1 — Apresentação:** sprite atlas direcional no token e estado visual do campo (chuva/noite/rios) APENAS se não afetar cálculo/FOV/visibilidade.\n\n**P2 — Terreno reproduzível:** seeds/salvamentos e validação entre bordas de cenas; não gerar mundo aberto.\n\n**P3 — Criaturas inteligentes:** testar seleção entre ações LEGALMENTE fornecidas pelo VLAB, sem motor de combate paralelo; VLAB já tem pesquisa de tática adaptativa, portanto evitar duplicar.\n\n**P4 — Recusar escopo:** fotossíntese, nutrientes, reprodução animal, cadeia alimentar completa e voto público para cânone.\n\n## Ferramentas e substitutos\n\nClaude Code aparece no vídeo; não é requisito. Já existem HTML/JS, a Arena TEST36, codificação por Codex quando autorizada, Pillow e arquivos CSV/JSON, além de sprites originais/CC0 candidatos. **A prova TEST da playlist usa somente CSS/JS do Tabletop existente** sem assinar serviços. Não usar imagem de vídeo alheio no produto público.\n\n## Prova executada nesta análise\n\n`ARENA_TEST36_CAMADAS_AMBIENTAIS_OFFLINE.html`: addon opcional em cópia do TEST36 original, três modos *Dia/Chuva/Noite*, contrato `assim.tabletop.scene.presentation.test.v1`; 31/31 checks Playwright em Chromium Linux, 360×740 / 390×844 / 412×915, 49 células, zero chamadas de rede e nenhum resultado mecânico alterado. **Não é combate, não é Android real e não foi integrado à branch oficial.**\n\n## Checklist da próxima passagem\n\n1. Verificar novo RUN/TEST e ABI VLAB/estado Codex, impedindo regressão/repetição.\n2. Entregar ao Desenvolvedor relatório de prioridades e POC isolado, sem atribuir escrita de outro executor.\n3. Somente adotar clima visual após validação FOV/ACL e UX Android; não redirecionar Dev de combate P0.\n4. Reavaliar tempo canônico de RS/CG antes de eventuais sistemas de calendário; não adotar o calendário fictício da playlist.\n''')
# PDF
pdffile=str(ROOT/'COMPENDIO_PLAYLIST_7_VIDEOS_ASSIMILACAO_20261024.pdf')
pdfmetrics.registerFont(TTFont('DVS','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVS-B','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='coverCustom',fontName='DVS-B',fontSize=23,leading=30,textColor=HexColor('#133b42'),spaceAfter=15))
styles.add(ParagraphStyle(name='hCustom',fontName='DVS-B',fontSize=15,leading=20,textColor=HexColor('#174350'),spaceBefore=14,spaceAfter=7,keepWithNext=True))
styles.add(ParagraphStyle(name='shCustom',fontName='DVS-B',fontSize=10,leading=14,textColor=HexColor('#1f574e'),spaceBefore=8,spaceAfter=4,keepWithNext=True))
styles.add(ParagraphStyle(name='bodyCustom',fontName='DVS',fontSize=8.8,leading=14,spaceAfter=5))
styles.add(ParagraphStyle(name='fineCustom',fontName='DVS',fontSize=7.7,leading=11,textColor=HexColor('#526268'),spaceAfter=5))
styles.add(ParagraphStyle(name='callCustom',fontName='DVS-B',fontSize=9,leading=13,textColor=HexColor('#355a47'),spaceAfter=8))
doc=SimpleDocTemplate(pdffile,pagesize=(210*mm,297*mm),leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,author='Coordenação Inovador — Mestre-side',title='Playlist VibeCode — 7 vídeos e aplicações ao Tabletop Assimilação')
story=[]
def para(t,sty='bodyCustom'):
 st=styles[sty];story.append(Paragraph(html.escape(str(t)).replace('\n','<br/>'),st))
para('PLAYLIST: 7 VÍDEOS / 5 INÉDITOS','coverCustom')
para('RPG Assimilação — investigação operacional MESTRE-SIDE, 24 de outubro de 2026','callCustom')
para('Uma série com método de desenvolvimento progressivo: sprites, comportamento, rios, clima, plantas e protótipo. Evidências visuais; sem narração integral transcrita.','bodyCustom')
para('Confiabilidade da evidência','hCustom')
para('196 quadros extraídos dos 7 MP4, em 14 folhas de contato com timestamp. Legendas aparecem gravadas na imagem em muitos trechos, mas não existe faixa de subtítulos e não houve ASR integral. 496150 e 496210 são duplicatas de arquivos já estudados.','bodyCustom')
para('Valor principal','hCustom')
para('A playlist ensina a evoluir um sistema em camadas pequenas e verificáveis. Não autoriza criar um novo RPG ecológico. Nossa prioridade permanece batalha tática oficial, com Mestre + players e VLAB.','bodyCustom')
para('Prova adicional','hCustom')
para('Camadas ambientais Dia / Chuva / Noite sobre uma cópia offline do TEST36: 31/31 verificações Chromium; sem alteração de mecânicas, FOV ou estado de sala; não homologado em Android físico.','bodyCustom')
para('Prioridades para a equipe','hCustom')
for s in ['P0 — ciclo real ação, alvo, recibo VLAB e apresentação segura, não demonstrado por estes vídeos.','P1 — sprites direcionais e cenário visual legível, sem substituir a grade ou revelar dados.','P2 — mapas/seeds reprodutíveis em cenas finitas, sem mundo infinito.','P3 — escolhas de monstros apenas sobre opções legais do motor competente.','P4 — não construir subsistema ecológico completo sem necessidade canônica.']:para(s)
story.append(PageBreak())
for stem,rec in D.items():
 m=media[stem];mins=int(m['duration']//60);secs=int(m['duration']%60)
 para(f'{stem} • {rec["heading"]}','hCustom')
 para(f'{mins:02d}:{secs:02d}  |  {rec["category"]}  |  P{rec["p"]}  |  {rec["novelty"]}','fineCustom')
 para('Evidências cronológicas','shCustom')
 for t,x in rec['chronology']:para(f'{t} — {x}')
 # single representative keyframe
 try:
  sec=float(m['duration']*.42);cap=cv2.VideoCapture('/mnt/data/'+stem+'.mp4');cap.set(cv2.CAP_PROP_POS_MSEC,sec*1000);ok,f=cap.read();cap.release()
  if ok:
   framep=ROOT/'contact'/f'{stem}_evidencia.png';cv2.imwrite(str(framep),f)
   pic=Image.open(framep);w,h=pic.size;hpt=118;wpt=hpt*w/h;story.append(RLImage(str(framep),width=wpt,height=hpt));para(f'Quadro de referência extraído em {int(sec)} s — imagem do arquivo fornecido; uso analítico privado.','fineCustom')
 except Exception as e:pass
 for hd,key in [('Constatação / limite','finding'),('Aplicação ao Assimilação','transfer'),('Ferramentas e substitutos','alternatives'),('Riscos e governança','risks'),('Entrega ao executor','action'),('Critério de aceite','accept')]:
  para(hd,'shCustom');para(rec[key])
 para('Limitações do levantamento','shCustom');para('Amostras de quadros e legendas impressas na imagem; sem transcrição integral, testes no Android, código do criador, licença dos assets ou demonstração de mecânicas VLAB.','fineCustom')
 story.append(PageBreak())
para('Conclusão de coordenação','hCustom');para('Há uma técnica clara: delimitar capacidades, mostrar provas de falha e melhorar o mesmo jogo sem recriar sua infraestrutura. Para a Arena, o resultado de maior valor é a batalha tática oficial, não o ecossistema completo.','bodyCustom')
para('Pendências exatas','hCustom')
for x in ['Conferir estado posterior ao TEST36 e os contratos de sala/CodeX já vigentes.','Homologar a ABI do VLAB para ação, alvo, recursos, dano e condição; sem isso, interface segue HOLD.','Testar efeitos visuais e sprites reais no Android e avaliar desempenho/legibilidade sem burlar FOV.','Não atribuir automaticamente a jogadores/monstros regras ecológicas da série.']:para(x)
def footer(canvas,doc):
 canvas.saveState();canvas.setFont('DVS',7);canvas.setFillColor(HexColor('#6e7c7d'));canvas.drawString(18*mm,12*mm,'ASSIMILAÇÃO • MESTRE-SIDE • evidência TEST');canvas.drawRightString(192*mm,12*mm,str(doc.page));canvas.restoreState()
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF',Path(pdffile).stat().st_size)
print('Reports',[(x.name,x.stat().st_size) for x in REPORTS.glob('*.md')])

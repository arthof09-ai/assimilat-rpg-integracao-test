# Snapshot técnico Notion — MAGIA

> **MESTRE-SIDE · SNAPSHOT DOCUMENTAL · NAO E NOVO CANON.** Fonte viva e historico: https://app.notion.com/p/3ebc2b324ede81f7b343f7270ff91373. Captura realizada em 2026-10-28. Nao confundir snapshot com implementacao testada, release, aprovacao NAC-PASS ou autorizacao para escrita Party.
> Origem Notion UUID: `3ebc2b32-4ede-81f7-b343-f7270ff91373`. Marcacoes de Notion (<mention>, <callout>, <page>) podem estar em formato Notion Markdown; consultar fonte viva para as versoes vigentes. Estado da busca: pagina completa recebida pelo conector em 2026-10-28, sem prova de execucao mecanica.

---

<callout icon="🧭" color="gray_bg">
<b>Objetivo desta página:</b> consolidar as regras de magia que já existem espalhadas pelo Sistema em uma única referência limpa e prática.

A antiga página <b>Sistema de magia</b> está vazia, então esta versão foi construída somente com regras já registradas em <b>Criação de Ficha</b>, <b>Sistema de Combate</b> e <b>Mecânicas testes</b>. Onde falta uma regra, a dúvida foi marcada em vez de ser preenchida por suposição.
</callout>

## Fluxo rápido de uma magia

<table fit-page-width="true" header-row="true">
<tr>
<td>
Regra
</td>
<td>
Etapa
</td>
<td>
O que verificar
</td>
</tr>
<tr>
<td>
1
</td>
<td>
Fonte de poder
</td>
<td>
PA, PA Livre e risco de esgotamento da Alma.
</td>
</tr>
<tr>
<td>
2
</td>
<td>
Conjuração
</td>
<td>
Ação necessária e custo da magia.
</td>
</tr>
<tr>
<td>
3
</td>
<td>
Classificação da magia
</td>
<td>
Patamar da magia e interações com outras regras.
</td>
</tr>
<tr>
<td>
4
</td>
<td>
CD e resistência
</td>
<td>
CD da magia e Salvaguardas.
</td>
</tr>
<tr>
<td>
5
</td>
<td>
Magias ofensivas
</td>
<td>
Teste de ataque, dano, crítico e Fraqueza Elemental.
</td>
</tr>
<tr>
<td>
6
</td>
<td>
Reflexão
</td>
<td>
Como tentar refletir uma magia inimiga.
</td>
</tr>
<tr>
<td>
7
</td>
<td>
PA Divino
</td>
<td>
Conversão de PA em PAD e potencialização de magia.
</td>
</tr>
<tr>
<td>
8
</td>
<td>
Registro da magia
</td>
<td>
Informações mínimas para uma magia ficar pronta para jogo.
</td>
</tr>
</table>

---

<toggle color="blue_bg">
💙 <b>Regra 1 — PA é a fonte espiritual da magia</b>

<b>PA significa Pontos de Alma.</b>

PA não é uma barra de mana separada do personagem. Ele representa a própria <b>reserva espiritual</b> do ser.

Utilizar magia consome uma parte real dessa reserva.

### PA Total e PA Livre

<b>PA Total − PA comprometido = PA Livre</b>

Antes de conjurar, o personagem deve saber quanto de sua Alma está realmente disponível.

### PA insuficiente

Se o personagem tentar conjurar uma magia <b>sem possuir PA Livre suficiente para pagar o custo</b>, ele entra em <b>Exaustão Espiritual extrema</b>.

Consequência:

<b>fica inconsciente por 2d10 dias.</b>

Em uma batalha, esse colapso é considerado, na prática:

<b>Morte.</b>

Isso acontece porque o personagem força a própria Alma além do que ainda possui disponível.

<callout icon="☠️" color="red_bg">
Chegar ao limite da Alma não é equivalente a simplesmente “ficar sem mana”. Forçar uma magia sem PA Livre suficiente provoca um colapso espiritual severo.
</callout>
</toggle>

<toggle color="purple_bg">
🪄 <b>Regra 2 — Conjuração e ação necessária</b>

### Ação padrão de conjuração

Se uma magia <b>não informar outro tempo de conjuração em sua própria descrição</b>, conjurá-la exige:

<b>1 Ação Padrão</b>

Essa é a regra padrão do Sistema.

### Exceções

Se a própria magia disser que usa:

- Ação Livre;
- Ação de Movimento;
- Ação Completa;
- Reação;
- duas ações;
- ritual;
- ou qualquer outro tempo específico,

a descrição da magia <b>substitui a regra padrão</b>.

### Teste para lançar magia

<b>Não existe teste universal para conseguir conjurar uma magia.</b>

Se o personagem conhece a magia, possui recursos para usá-la e cumpre suas condições, ele a conjura normalmente.

Só existe teste de conjuração quando <b>a própria magia ou habilidade disser explicitamente que existe um teste</b>.
</toggle>

<toggle color="orange_bg">
⭐ <b>Regra 3 — Classificação e evolução das magias</b>

As magias seguem as mesmas 5 Classificações principais do restante do RPG:

<table fit-page-width="true" header-row="true">
<tr>
<td>
Ordem
</td>
<td>
Classificação
</td>
</tr>
<tr>
<td>
1
</td>
<td>
Bronze
</td>
</tr>
<tr>
<td>
2
</td>
<td>
Prata
</td>
</tr>
<tr>
<td>
3
</td>
<td>
Ouro
</td>
</tr>
<tr>
<td>
4
</td>
<td>
Ouro Negro
</td>
</tr>
<tr>
<td>
5
</td>
<td>
Lendária
</td>
</tr>
</table>

<b>Bronze é o patamar mais fraco e Lendária é o mais forte.</b>

### Evolução de uma magia

Uma magia pode evoluir junto com o personagem.

Uma magia que nasceu como <b>Bronze</b> pode ser aprimorada progressivamente até se tornar <b>Lendária</b>.

Isso significa que a mesma magia pode possuir versões diferentes por Classificação, aumentando seu poder, alcance, duração, dano, efeito, custo ou outras propriedades conforme sua própria evolução.

### Limite pela Classificação do conjurador

Um personagem <b>não pode usar uma magia em uma Classificação superior à própria</b>.

Porém, ele pode conhecer uma magia originalmente mais avançada e utilizá-la em uma versão reduzida compatível com seu próprio patamar.

### Exemplo

Um Espiritualista Demoníaco <b>Prata 2</b> conhece uma magia cuja versão máxima atual é <b>Ouro Negro</b>.

Ele <b>não conjura a versão Ouro Negro</b>.

Ele pode usar:

<b>a versão Prata dessa mesma magia.</b>

Quando sua própria Classificação aumentar, ele poderá acessar versões mais fortes da magia, desde que a progressão daquela magia permita.

<callout icon="📝" color="gray_bg">
A Classificação da magia não é necessariamente fixa para sempre. Ela representa o <b>patamar daquela versão da magia</b>.
</callout>
</toggle>

<toggle color="green_bg">
🎯 <b>Regra 4 — CD e Salvaguarda</b>

### Classe de Dificuldade

<b>CD da Magia = Proficiência + INT + bônus</b>

A CD representa a dificuldade de resistir ao efeito da magia.

### Salvaguarda

Sempre que uma magia permitir Salvaguarda, o alvo realiza o teste indicado pela própria magia.

A Salvaguarda é comparada diretamente com:

<b>a CD da magia.</b>

Se o resultado da Salvaguarda <b>superar a CD</b>, o alvo resiste conforme a descrição da magia.

O efeito pode ser:

- reduzido;
- parcialmente resistido;
- ou anulado,

dependendo da própria magia.

### Qual teste usar

A magia deve informar qual resistência é aplicável, como:

- Fortitude;
- Reflexo;
- Vontade;
- ou outro teste determinado pela magia.

### Bônus de CD

Títulos, itens e habilidades podem aumentar a CD.

Exemplo já existente no sistema:

<b>Grão Mestre Mago: +7 de CD.</b>
</toggle>

<toggle color="red_bg">
🔥 <b>Regra 5 — Magias ofensivas, dano e Fraqueza Elemental</b>

### Não existe ataque mágico universal

Magias <b>não precisam de teste para serem lançadas ou acertarem</b>, a menos que a própria magia diga explicitamente que exige algum teste.

Assim:

- uma magia que exige Salvaguarda usa a CD da magia;
- uma magia que exige teste próprio segue sua própria descrição;
- uma magia que não exige nenhum desses testes simplesmente produz seu efeito conforme descrito.

### Magias não causam Crítico

<b>Magias não utilizam o sistema de Crítico.</b>

A regra sequencial:

<b>6 → 6 → 6 / 6 → 6 → 5</b>

não se aplica a magias.

Isso continua verdadeiro mesmo quando uma magia possuir algum teste próprio, salvo se uma habilidade específica criar uma exceção explícita.

### Fraqueza Elemental

Quando uma magia causa dano de um Elemento ao qual o alvo possui Fraqueza:

<b>pegue o maior dado do dano elemental e role esse dado mais 3 vezes.</b>

Exemplo:

<b>2d6 de Fogo → 5d6 de Fogo</b> contra um alvo com Fraqueza a Fogo.

### Bônus externos

Títulos, itens e habilidades podem acrescentar dano ou outros bônus a magias.

Exemplo já existente:

<b>Grão Mestre Mago: +2d12 de dano em magias.</b>
</toggle>

<toggle color="purple_bg">
🪞 <b>Regra 6 — Refletir Magias</b>

Refletir Magia utiliza a <b>Reação</b> do personagem.

O teste atual é:

<b>Arcanismo contra a CD da magia inimiga</b>

Se o teste superar a CD:

- o personagem <b>não sofre o dano original da magia</b>;
- reflete <b>metade do dano da magia</b>.

Para magias sem dano, permanece valendo o efeito específico escrito na própria magia ou habilidade; a regra atual de Reflexão define objetivamente apenas a parte de dano.
</toggle>

<toggle color="blue_bg">
✨ <b>Regra 7 — PAD: Pontos de Alma Divinos</b>

O <b>PAD — Pontos de Alma Divinos</b> é uma forma superior da própria Alma.

### Formação do PAD

O sistema registra que o PA pode se transformar em PAD por uma combinação de fatores, incluindo:

- grande quantidade de <b>Força do Mundo</b>;
- Reino da Alma em <b>completa harmonia Elemental</b>;
- condições para existir <b>vida dentro do Reino da Alma</b>.

### Relação entre PA e PAD

O PAD corresponde a uma porcentagem do PA Total do personagem.

A parcela convertida em PAD deixa de permanecer disponível como PA comum.

### Custo

Uma magia paga <b>o mesmo valor numérico</b> quando utiliza PAD.

Exemplo:

<b>magia de 30 PA → custa 30 PAD quando conjurada com Alma Divina.</b>

O custo não fica menor.

A diferença é que a energia usada é muito mais poderosa.

### Potencialização por Classificação

Ao conjurar uma magia usando PAD, ela recebe:

<b>+3d13 por Classificação da magia.</b>

<table fit-page-width="true" header-row="true">
<tr>
<td>
Classificação da magia
</td>
<td>
Bônus com PAD
</td>
</tr>
<tr>
<td>
Bronze
</td>
<td>
+3d13
</td>
</tr>
<tr>
<td>
Prata
</td>
<td>
+6d13
</td>
</tr>
<tr>
<td>
Ouro
</td>
<td>
+9d13
</td>
</tr>
<tr>
<td>
Ouro Negro
</td>
<td>
+12d13
</td>
</tr>
<tr>
<td>
Lendária
</td>
<td>
+15d13
</td>
</tr>
</table>

### O que o PAD potencializa

O PAD pode potencializar <b>qualquer magia</b> usada com Alma Divina.

Quando a magia possui um efeito numérico, o bônus de PAD pode aumentar o componente relevante daquela magia, como:

- dano;
- cura;
- proteção;
- escudo;
- ou outro valor numérico que represente diretamente o poder produzido pela magia.

Para efeitos puramente qualitativos, a forma concreta de potencialização deve estar descrita na própria magia ou ser definida pelo Mestre conforme a natureza daquele efeito.

<callout icon="✨" color="blue_bg">
PAD não reduz o custo. Ele substitui o PA comum como fonte da conjuração e transforma a magia em uma versão alimentada por <b>Alma Divina</b>.
</callout>
</toggle>

<toggle color="gray_bg">
📋 <b>Regra 8 — Como registrar uma magia na ficha</b>

Esta seção organiza as informações de uma magia sem criar novos efeitos.

Para que uma magia fique pronta para uso em sessão, registre sempre que aplicável:

- <b>Nome</b>
- <b>Classificação</b>
- <b>Elemento</b>
- <b>Forma do Elemento</b>, se houver
- <b>Ação necessária</b>
- <b>Custo em PA ou PAD</b>
- <b>Alcance</b>
- <b>Alvo ou área</b>
- <b>Duração</b>
- <b>CD</b>
- <b>Salvaguarda</b>, quando existir
- <b>Teste de ataque</b>, quando existir
- <b>Dano ou cura</b>
- <b>Efeito</b>
- <b>Condição de manutenção</b>, quando existir
- <b>Limitações, recarga ou número de usos</b>, quando existirem

### Atalho de magia

Na ficha final, uma magia usada com frequência deve ficar escrita de forma que o Mestre consiga resolvê-la imediatamente.

Exemplo de organização:

<b>Nome — ação \| alcance \| custo \| CD/ataque \| dano/efeito \| duração</b>

> <b>A descrição narrativa explica o que a magia faz; o atalho mecânico explica como usá-la sem reconstruir a regra durante a sessão.</b>
</toggle>

---

## 📝 Regras confirmadas nesta revisão

<callout icon="✅" color="green_bg">
- Magias possuem as Classificações <b>Bronze, Prata, Ouro, Ouro Negro e Lendária</b>.
- Uma mesma magia pode <b>evoluir de Bronze até Lendária</b> junto com o personagem.
- O conjurador não utiliza uma versão de magia acima da própria Classificação; ele usa uma <b>versão reduzida equivalente ao próprio patamar</b>.
- Se a magia não informar outro tempo, sua conjuração exige <b>1 Ação Padrão</b>.
- Não existe teste universal para conjurar magia.
- Magias <b>não utilizam Crítico</b>.
- Salvaguardas são comparadas diretamente com a <b>CD da magia</b>.
- Tentar conjurar sem PA Livre suficiente causa <b>Exaustão Espiritual</b>, deixando o personagem inconsciente por <b>2d10 dias</b>; em batalha isso representa, na prática, morte.
- Uma magia alimentada por PAD custa o <b>mesmo valor numérico</b> que custaria em PA.
- PAD concede <b>+3d13 por Classificação da magia</b>: Bronze +3d13, Prata +6d13, Ouro +9d13, Ouro Negro +12d13 e Lendária +15d13.
- PAD potencializa qualquer magia alimentada com <b>Alma Divina</b>.
</callout>

---

## 📜 Arquivo histórico — versão antiga

<callout icon="🗃️" color="gray_bg">
A página abaixo é a <b>versão antiga do Sistema de Magia</b>, mantida apenas como registro histórico. Ela estava vazia antes desta revisão. As regras atuais são as desta página.
</callout>

<page url="https://app.notion.com/p/31ac2b324ede8274bb7b01bd84c9c9fe">
Sistema de Magia — Versão Antiga (registro)
</page>

## Bridge — DMG-RANK-01

Magia ofensiva sem dano numérico explícito usa <mention url="https://app.notion.com/p/3f2c2b324ede815498cddb7844245f7e" /> depois que a versão/rank da magia estiver definida. Área, controle, duração, garantia e bypass ajustam o orçamento. Magias continuam sem Crítico por padrão; PAD e Fraqueza Elemental permanecem camadas externas.

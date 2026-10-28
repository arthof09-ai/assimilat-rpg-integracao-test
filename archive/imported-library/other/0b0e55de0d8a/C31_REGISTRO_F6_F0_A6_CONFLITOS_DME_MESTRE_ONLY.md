# DMG C31 — Registro adicional de conflitos ofensivos literais e precedência

**Operação existente:** OP-DMG-CORPUS-EMP-01 · **Âmbito:** MESTRE-SIDE / TEST · **Norma:** DMG-RANK-01 v1.1 intocada · **F0:** 4/8 HOLD · **D0:** parcial · **F6:** sem prova positiva. **Sem writer Notion**; nenhuma escrita em fichas, Party, O Primeiro, VLAB ou DMG-RANK. Fontes reabertas diretamente no Notion Mestre depois da primeira publicação C31. Este é um registro científico de divergências, não uma errata canônica.

## Conflito 1 — Bola de Putrificação de Do Ze (fonte narrativa com pool literal)

- **Fonte:** https://app.notion.com/p/1c7c2b324ede83648b6e0104f9bd2146 · ficha “Do Ze”.
- **Classificação conflitante:** cabeçalho abre como `Do ze (O5)` mas o corpo declara `Espiritualista Demoníaco Ouro 2`. Não adjudicar rank de ator sem autoridade.
- **Dano principal:** mesmo trecho de magia apresenta `9d8+Int` e `(9d6+Int de dano)`. Médias condicionais antes de INT externa: `9d8` = 40,5; `9d6` = 31,5. **Diferença de 9**. Não assumir que a segunda expressão é erro ou que substitui a primeira sem procedência.
- **Rider:** texto menciona `4d12 de dano de Morte por turno`, média bruta 26 por tick, em caso de falha na Fortitude. Isso não comprova quantos turnos dura, a ordem do tick, imunidade parcial, sobreposição ou qual CD deve ser usado. O custo **20 PA** está no trecho, mas sem ação e RE/FIP verificáveis não há fallback DMG v1.1 admissível.
- **Status:** CONFLITO-LITERAL + DURAÇÃO-PENDENTE + RE/FIP-NÃO-COMPROVADOS. Nenhum cálculo de dano total por rodada ou TTK legitimado.

## Conflito 2 — Ataques de Pan Tueimor / Lan Treimor

- **Fonte:** https://app.notion.com/p/8f6c2b324ede82c88e5d8184dc3a3b90, página indexada como **Pan Tueimor**, corpo abre como **Lan Treimor (ON1)**. Divergência de identidade, sem decisão canônica.
- **Trecho H – Ataque:** `4d6+65` (média 79) e `(5d10+4d8+3d10+80)` (média 142), delta 63.
- **Trecho Pressão:** `4d6+80` (média 94) e `(5d10+4d8+3d10+4d12+105)` (média 193), delta 99.
- **Interpretação:** números entre parênteses coexistem com expressões anteriores, mas o fragmento não prova se são chassi, transformação, modo, histórico, erro aritmético ou versão alternativa. **Não somar, não substituir por escolha silenciosa e não contar como ações independentes**. FF, transformação, atributos e arma exigem decomposição e evidência competente.
- **Status:** IDENTIDADE-HOLD + DECOMPOSIÇÃO-HOLD + RE/FIP-NÃO-COMPROVADOS.

## Conflito 3 — Ravin e utilidade estatística da distribuição

- **Fonte:** https://app.notion.com/p/14bc2b324ede834daba501e769feda9d.
- **Fórmulas literais** `2d6+37` (média 44) e `(7d6+20)` (média 44,5), diferença bruta 0,5. A pequena diferença de DME bruta **não assegura equivalência sob RD**: o experimento C31 do adendo anterior mostrou, com RD flat hipotética de 50, dano líquido esperado da primeira igual a 0 e da segunda estritamente positivo (frações e algoritmos independentes preservados no ZIP `DMG_C31_ADENDO_PERSONAGENS_120_GATES_MESTRE_ONLY.zip`). Não significa dano comprovado contra algum alvo real.
- **Status:** MODOS-DESCONHECIDOS. Avaliação de distribuição funcional, não seleção de fórmula canônica.

## Controles de auditoria e decisão

As médias foram recalculadas com aritmética racional dos dados discretos, sem arredondamento de faces, não incluem INT, FF não identificado, precisão, RD real, imunidades, crítico, PA de execução por turno ou habilidade defensiva. Não considerar média de dano intrínseco um valor final por tentativa. A presente auditoria prova que **o obstáculo de D0/F6 não é ausência de pools em todo o corpus**, mas a **falta de decomposição, autoridade e precedência** sobre pools já presentes. As páginas reais não devem ser modificadas pelo DMG sem writer e decisão competente.

**Gate:** F0 4/8 HOLD; F6 0 novos casos autenticamente elegíveis para preencher dano; D0 Personagens 233/233 páginas-filhas diretas lidas, mas D0 global permanece parcial. **Próxima ação objetiva:** depois de identificar autoridade do mesmo personagem e a forma ativa, anotar versão, RE/FIP de cada efeito separadamente, ação, alvo, tipo, custo e duração; somente então planejar pares VLAB. Até lá, manter essas linhas em quarentena classificatória.

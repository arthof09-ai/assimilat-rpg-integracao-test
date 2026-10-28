/* PROPOSTA INDEPENDENTE (NÃO INTEGRADA AO TEST15), cenário MESTRE-SIDE TEST.
 * O estado antigo não é trocado antes de persistência confirmada.
 * A função de interface publishState é chamada APÓS gravar.
 * Em produção, considerar handling de erro de render e compatibilidade. */
function restaurarBackupSeguro({texto, valida, storage, chave, publica, clona}) {
  let candidato;
  try {
    if (typeof texto !== 'string' || texto.length > 750000) throw Error('Limite');
    candidato = JSON.parse(texto);
    if (!valida(candidato)) throw Error('Schema incompatível');
    candidato = clona(candidato);
    const bytes = JSON.stringify(candidato);
    // Preflight sem alterar a aplicação; a escrita substitui uma chave atômica no Storage.
    storage.setItem(chave, bytes);
  } catch (err) {
    return {ok:false,erro:String(err.message)};
  }
  publica(candidato);
  return {ok:true};
}
if (typeof module !== 'undefined') module.exports={restaurarBackupSeguro};

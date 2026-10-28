'use strict';
let model = null;
const $ = (id) => document.getElementById(id);
const text = (id, value) => {$(id).textContent = value;};
let busy = false;
const makeId = () => (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID().replaceAll('-', '') : (Date.now().toString(36) + Math.random().toString(36).slice(2));
function showFeedback(message, error=false) {
  const node = $('feedback');node.hidden = false;node.textContent = message;node.className = error ? 'error' : '';
}
async function request(path, body) {
  const opts = body === undefined ? {} : {method: 'POST',headers:{'Content-Type':'application/json','X-VLAB-UI':'1'},body:JSON.stringify(body)};
  const response = await fetch(path, opts);
  const data = await response.json();
  if (!response.ok || data.status === 'HOLD') throw new Error(data.error || 'Falha no experimento');
  return data;
}
async function run(action) {
  if (busy) return;
  busy = true;updateButtons();
  try { model = await action(); render(); }
  catch (err) {showFeedback('HOLD — ' + err.message, true);}
  finally {busy = false;updateButtons();}
}
function updateButtons() {
  const finished = model && model.winner;
  $('executeBtn').disabled = busy || !model || finished;
  $('undoBtn').disabled = busy || !model || model.active_events <= 0;
  for (const name of ['newBtn','recoverBtn','receiptBtn']) $(name).disabled = busy;
  for (const name of ['target','action','reaction']) $(name).disabled = busy || !model || finished || (name === 'reaction' && $('action').value === 'PASS');
}
function selectOptions(el, options, selected) {
  el.replaceChildren();
  for (const option of options) {const elOption=document.createElement('option');elOption.value=option.value;elOption.textContent=option.label;el.append(elOption);}
  if (options.some(o=>o.value===selected)) el.value=selected;
}
function statEl(label, value){const span=document.createElement('span');const strong=document.createElement('strong');strong.textContent=value;span.textContent=label+' ';span.append(strong);return span;}
function makeFighter(id) {
  const holder = $('actor'+id), a = model.actors[id];
  holder.replaceChildren();holder.className='fighter surface '+id.toLowerCase()+(model.active_actor===id ? ' active' : '');
  const heading=document.createElement('div');heading.className='fighter-head';
  const names=document.createElement('div');const eyebrow=document.createElement('div');eyebrow.className='eyebrow';eyebrow.textContent='BRONZE · FICHA EXPERIMENTAL';
  const title=document.createElement('h3');title.textContent=a.name;
  const sub=document.createElement('div');sub.className='subtitle';sub.textContent=id+(model.active_actor===id?' · Ação atual':' · '+(a.hp===0?'Incapacitado em teste':'Aguardando'));
  names.append(eyebrow,title,sub);const portrait=document.createElement('div');portrait.className='portrait';portrait.textContent=id==='ED'?'✦':'◈';heading.append(names,portrait);holder.append(heading);
  const stats=document.createElement('div');stats.className='health-head';const vida=document.createElement('span');vida.textContent='Vida';const number=document.createElement('span');number.textContent=a.hp+' / '+a.max_hp;stats.append(vida,number);holder.append(stats);
  const progress=document.createElement('div');progress.className='progress';const bar=document.createElement('span');bar.style.width=Math.max(0,100*a.hp/a.max_hp)+'%';progress.append(bar);holder.append(progress);
  const values=document.createElement('div');values.className='stats';for(const [label,value] of [['Alma',a.pa+'/'+a.max_pa],['CA',a.ca],['FOR',a.for],['DES',a.des],['Luta',a.luta],['Reação',a.reaction ? 'Disponível':'Usada']])values.append(statEl(label,value));holder.append(values);
}
function makeInitiative(){const root=$('initiative');root.replaceChildren();for(const who of model.order){const a=model.actors[who];const row=document.createElement('div');row.className='initiative-row';const left=document.createElement('div');const name=document.createElement('strong');name.textContent=a.name;const details=document.createElement('span');details.className='roll';details.textContent='1d6 ('+model.initiative.rolls[who]+') + DES ('+a.des+') + 0';left.append(name,details);const score=document.createElement('div');score.className='score';score.textContent=model.initiative.scores[who];row.append(left,score);root.append(row);}}
function displayEvent(event) {
  const row=document.createElement('div');row.className='history-event';
  const main=document.createElement('div');const h=document.createElement('strong');const actor=model.actors[event.actor_id];h.textContent='#'+event.turn+' — '+actor.name+' · '+(event.action==='PASS'?'Passou o turno':'Atacou');main.append(h);
  const p=document.createElement('p');const receipt=event.receipt;if (event.action==='ATTACK'){
    const result=receipt.attack_result;
    const effective=result.effective ?? result.net ?? result.damage_effective ?? '?';
    const hpBefore=event.before[event.target_id].hp,hpAfter=event.after[event.target_id].hp;
    p.textContent=receipt.attack_roll+' | '+receipt.damage_roll_fixture+' | Reação: '+event.reaction+' | Vida do alvo: '+hpBefore+' → '+hpAfter+' (−'+(hpBefore-hpAfter)+')';
    if(receipt.defense_result){const d=document.createElement('p');d.textContent='Defesa: '+receipt.defense_result.action+' | defesa '+receipt.defense_result.defense_exact+' | negou dano: '+(receipt.defense_result.damage_negated?'SIM':'NÃO');main.append(d);}
  } else p.textContent='Turno encerrado sem ataque; nenhum dano aplicado.';
  main.append(p);const code=document.createElement('code');code.textContent='Motor SHA: '+(receipt.native_engine_chain_sha256 || '—');main.append(code);const badge=document.createElement('div');badge.className='event-badge';badge.textContent='TURN '+event.turn;row.append(main,badge);return row;
}
function render() {
  if (!model) return;
  text('sessionCode','SESSÃO '+model.session_id.slice(0,8).toUpperCase());
  selectOptions($('scenario'),model.available_scenarios.map(s=>({value:s.key,label:s.title})),$('scenario').value);
  if (!model.available_scenarios.some(s=>s.key===$('scenario').value)) $('scenario').value=model.scenario_key;
  text('scenarioDescription',model.description);
  for (const id of ['ED','BE']) makeFighter(id);
  text('turnPill','TURNO '+model.turn_number);
  const complete=Boolean(model.winner);
  const winner=$('winnerNote');winner.hidden=!complete;
  if(complete)winner.textContent='Fim da simulação: '+model.actors[model.winner].name+' venceu pelo critério experimental Vida 0. Não equivale a morte canônica.';
  text('activeTurn',complete?'Cenário encerrado. Você pode conferir o recibo, desfazer a última ação ou iniciar outro combate.':'Agora: '+model.actors[model.active_actor].name+' — selecione a ação e a resposta do defensor.');
  selectOptions($('target'),model.next_target?[{value:model.next_target,label:model.actors[model.next_target].name}]:[],model.next_target);
  selectOptions($('reaction'),model.reaction_options.map(x=>({value:x,label:x==='NONE'?'Não reagir':x==='DEFENDER'?'Defender (CON + Armadura + Fortitude)':'Esquivar (CA + Reflexo)'})),$('reaction').value);
  if ($('action').value==='PASS')$('reaction').value='NONE';
  makeInitiative();
  text('eventCount',model.active_events+' ações · '+model.history_entries_total+' registros');
  const list=$('historyList');list.replaceChildren();
  if (!model.events.length){const p=document.createElement('p');p.className='muted';p.textContent='Nenhuma ação executada. Selecione uma ação para iniciar a demonstração.';list.append(p);}
  else for(const event of [...model.events].reverse())list.append(displayEvent(event));
  const limits=$('limitations');limits.replaceChildren();for(const item of model.limitations){const li=document.createElement('li');li.textContent=item;limits.append(li);}
  updateButtons();
}
$('action').addEventListener('change', () => {if($('action').value==='PASS')$('reaction').value='NONE';updateButtons();});
$('executeBtn').addEventListener('click',()=>run(async()=>{const action=$('action').value,reaction=action==='PASS'?'NONE':$('reaction').value;const before=model.active_events;const result=await request('/api/act',{request_id:makeId(),action,reaction,target:$('target').value});showFeedback('Ação registrada. '+(result.active_events-before)+' novo evento experimental.');return result;}));
$('newBtn').addEventListener('click',()=>{if(!confirm('Iniciar novo cenário? O combate atual ficará preservado no histórico local.'))return;run(async()=>{const result=await request('/api/new',{scenario:$('scenario').value});showFeedback('Novo experimento iniciado; o anterior continua preservado.');return result;});});
$('recoverBtn').addEventListener('click',()=>run(async()=>{const result=await request('/api/recover',{});showFeedback('Recuperação local: diário relido e efeitos simulados conferidos sem acesso externo.');return result;}));
$('undoBtn').addEventListener('click',()=>{if(!confirm('Desfazer a última ação? O histórico de reversão será preservado.'))return;run(async()=>{const result=await request('/api/undo',{request_id:makeId()});showFeedback('Última ação revertida em cópia local; reversão registrada.');return result;});});
$('receiptBtn').addEventListener('click',()=>{window.location.href='/api/receipt';});
run(()=>request('/api/state'));

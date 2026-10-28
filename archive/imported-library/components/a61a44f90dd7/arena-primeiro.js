/* Aditivo TEST; apenas apresentação. NUNCA simula ataque/PA/turno ou altera storage. */
(()=>{'use strict';
 const btn=document.getElementById('arenaFocusToggle');const units=document.getElementById('arenaUnitsJump');
 const viewport=document.getElementById('viewport');const map=viewport?.closest('.card');
 if(!btn||!units||!map)return;
 map.classList.add('battle-map-primary');
 document.body.classList.add('arena-primeiro');
 btn.setAttribute('aria-expanded','false');
 btn.addEventListener('click',()=>{
  const open=document.body.classList.toggle('arena-tools-open');
  btn.textContent=open?'🗺 Priorizar Arena':'⚙ Ferramentas';
  btn.setAttribute('aria-expanded',String(open));
  if(!open)map.scrollIntoView({block:'nearest',behavior:'auto'});
 });
 units.addEventListener('click',()=>document.getElementById('unitList')?.scrollIntoView({block:'start',behavior:'auto'}));
})();

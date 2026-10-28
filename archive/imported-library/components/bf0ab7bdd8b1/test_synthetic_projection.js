'use strict';
const assert=require('node:assert/strict'),{projectSyntheticEvent,projectSeries}=require('./synthetic_projection_poc');
const fixture=(n=1,type='ACTION_NOTE')=>({version:1,scope:'MESTRE_SIDE_TEST',source:{kind:'SYNTHETIC_FIXTURE',id:'toy'},id:'event'+n,order:n,type,payload:type==='ACTION_NOTE'?{actor:'Hero TEST',action:'Movimento declarado',target:'Alvo TEST'}:type==='TURN_NOTE'?{actor:'Hero TEST',round:n}:{actor:'Hero TEST',resource:'PA TEST',before:20,after:18}});
const cases=[];function ck(name,cb){cb();cases.push(name)}
ck('valid action',()=>assert.equal(projectSyntheticEvent(fixture(1)).type,'ACTION_NOTE'));
ck('valid turn',()=>assert.equal(projectSyntheticEvent(fixture(2,'TURN_NOTE')).payload.round,2));
ck('valid resource',()=>assert.equal(projectSyntheticEvent(fixture(2,'RESOURCE_NOTE')).payload.after,18));
ck('reject external scope',()=>assert.equal(projectSyntheticEvent({...fixture(),scope:'PARTY'}),null));
ck('reject nonfixture',()=>assert.equal(projectSyntheticEvent({...fixture(),source:{kind:'VLAB_REAL',id:'r205'}}),null));
ck('reject unknown action type',()=>assert.equal(projectSyntheticEvent({...fixture(),type:'DAMAGE_CALCULATE'}),null));
ck('reject malicious id',()=>assert.equal(projectSyntheticEvent({...fixture(),id:'__proto__'}),null));
ck('reject bad order',()=>assert.equal(projectSyntheticEvent({...fixture(),order:-1}),null));
ck('drop unlisted payload keys',()=>assert.deepEqual(Object.keys(projectSyntheticEvent({...fixture(),payload:{...fixture().payload,secret:'MESTRE_ONLY',x:3,y:4}}).payload),['actor','action','target']));
ck('does not invent XY',()=>assert.ok(!('x' in projectSyntheticEvent(fixture()).payload)));
ck('reject malformed text',()=>assert.equal(projectSyntheticEvent({...fixture(),payload:{...fixture().payload,actor:'<svg>'}}),null));
ck('accept ordered series',()=>assert.equal(projectSeries([fixture(1),fixture(3)]).length,2));
ck('reject duplicate ID',()=>assert.equal(projectSeries([fixture(1),{...fixture(2),id:'event1'}]),null));
ck('reject regressive order',()=>assert.equal(projectSeries([fixture(3),fixture(1)]),null));
// Seeded generative contract probes, separate from directed assertion denominator.
let seed=20261022;function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0;}
let accepted=0,rejected=0;for(let i=0;i<240;i++){const e=fixture(i+1),bad=rnd()%5===0;if(bad)e.type='RNG_DAMAGE';const out=projectSyntheticEvent(e);assert.equal(Boolean(out),!bad);if(bad)rejected++;else accepted++;}
console.log(JSON.stringify({directed:{pass:cases.length,checks:cases},seed:20261022,generative:{trials:240,accepted,rejected},scope:'SYNTHETIC_FIXTURE_ONLY'}));

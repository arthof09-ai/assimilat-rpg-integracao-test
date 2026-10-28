/* D-INOV-027: TEST-only pure projection contract. Not connected to VLAB/Party/production.
 * Rejects unknown sources/types, projects only explicit allowed keys, never invents XY.
 */
'use strict';
const SAFE_ID=/^[a-z][a-z0-9_-]{0,31}$/;
const TYPES={
 TURN_NOTE:['actor','round'],
 ACTION_NOTE:['actor','action','target'],
 RESOURCE_NOTE:['actor','resource','before','after']
};
const plain=o=>o!==null&&typeof o==='object'&&!Array.isArray(o)&&Object.getPrototypeOf(o)===Object.prototype;
const safeName=x=>typeof x==='string'&&x.length>0&&x.length<=48&&!/[<>\x00-\x1f]/.test(x);
function projectSyntheticEvent(evt){
 if(!plain(evt)||evt.version!==1||evt.scope!=='MESTRE_SIDE_TEST'||!plain(evt.source)||evt.source.kind!=='SYNTHETIC_FIXTURE'||!safeName(evt.source.id)||
    !SAFE_ID.test(evt.id)||!Number.isSafeInteger(evt.order)||evt.order<0||!Object.hasOwn(TYPES,evt.type)||!plain(evt.payload))return null;
 const out={version:1,scope:'MESTRE_SIDE_TEST',source:'SYNTHETIC_FIXTURE',id:evt.id,order:evt.order,type:evt.type,payload:{}};
 for(const key of TYPES[evt.type]){
  const v=evt.payload[key];
  if((key==='round'||key==='before'||key==='after')?(!Number.isSafeInteger(v)||v<0||v>99999):!safeName(v))return null;
  out.payload[key]=v;
 }
 return out;
}
function projectSeries(events){
 if(!Array.isArray(events)||events.length>1000)return null;
 const ids=new Set();let last=-1;const result=[];
 for(const e of events){const p=projectSyntheticEvent(e);if(!p||ids.has(p.id)||p.order<=last)return null;result.push(p);ids.add(p.id);last=p.order;}
 return result;
}
module.exports={projectSyntheticEvent,projectSeries};

from pathlib import Path
p=Path(__file__).resolve().parent/'native_v081_controlled/vlab_effects_v08.py'
s=p.read_text()
assert 'def apply_casulo_brotos(' not in s
s+='''
# R153 additive source-bound native support. Two-turn exact expiry is NOT assigned.
def apply_casulo_brotos(scene:Scene,caster_id:str,target_id:str,*,source:AbilitySource,
      state:ActorActionState,proofs:tuple[FrozenRuleEvidence,...],range_m:int,
      same_caster_effect_active:bool=False):
    a=scene.actors[caster_id];t=scene.actors[target_id]
    if source.kind!='control' or source.economy!='STANDARD' or source.required_pa!=60 or source.target_scope!='ALLY':
        raise EffectBlocked('Casulo source type and action mismatch')
    if a.hp<=0 or t.hp<=0 or a.standard!=1 or a.pa is None or a.pa<60:
        raise EffectBlocked('Casulo action or PA unavailable')
    if same_caster_effect_active:raise EffectBlocked('same caster Casulo cannot stack')
    if type(range_m)!=int or not 0<=range_m<=15:raise EffectBlocked('Casulo 15m range')
    _require_option(scene,caster_id,source,state,proofs,target=target_id)
    before_ca=t.ca
    t.ca+=22;a.standard=0;a.pa-=60
    return scene.record({'action':'CASULO_BROTOS','by':caster_id,'to':target_id,'PA_spent':60,
        'standard_spent':1,'range_m':range_m,'ca_before':str(before_ca),'ca_after':str(t.ca),
        'CA_delta':22,'movement_delta_m':-4,'duration_literal':'2 TURNOS',
        'expiration_boundary':'HOLD_SOURCE_NOT_DEFINED','same_caster_nonstack':True,
        'source_page':source.source_page_id})
'''
p.write_text(s)

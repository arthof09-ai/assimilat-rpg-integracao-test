"""R226 independent R18 SQLite scanner; reconstruct dice, source economics, actions, magic and condition. NO combat engine import."""
import json,hashlib,sqlite3,random,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def ck(ok,label):
    if not ok:raise AssertionError(label)
def dig(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def dice(seed,tag,n,faces):
    h=hashlib.sha256(f'R215|{seed}|{tag}|{n}d{faces}'.encode()).digest();r=random.Random(int.from_bytes(h,'big'));return [r.randint(1,faces) for _ in range(n)]
def audit_one(path,p,source_hash,pre_hash,arm,seed):
    c=sqlite3.connect(f'file:{path}?mode=ro&immutable=1',uri=True)
    try:
        m=dict(c.execute('select key,value from meta'));st=json.loads(m['state']);rows=[json.loads(a[0]) for a in c.execute('select row_json from events order by seq')]
        recs=list(c.execute('select seq,cmd_id,prev,row_sha,before_sha,after_sha from events order by seq'));pending=c.execute('select count(*) from pending').fetchone()[0]
    finally:c.close()
    ck(len(rows)==2 and not pending and int(m['revision'])==2,'R18_REV_OR_PENDING')
    ck(st['r227']['pre_sha256']==pre_hash and st['r227']['item_excerpt_sha256']==source_hash and st['r227']['world_canon'] is False,'WRONG_SOURCE_AUTHORITY')
    ck(st['r227']['magical_rd_assumption']==p['magic_RD_assumptions'][arm],'R227_MAGIC_RD_PRECONDITION')
    ck(st['r227']['arm']==arm and st['seed']==seed and st['r227']['item_equipped_both'] is True and st['r227']['physical_chassis_same_in_both'] is True,'WRONG_FIXTURE')
    prior=m['genesis'];last=None;ev=[]
    for k,(row,rec) in enumerate(zip(rows,recs),1):
        ck(row['seq']==k and row['prev']==prior and row['before_sha']==rec[4] and row['after_sha']==rec[5],'ROW_CHRONOLOGY')
        ck(rec[:4]==(k,row['cmd_id'],row['prev'],dig(row)),'HASH_REBUILT_EVENT_RECEIPT')
        ck(row['official_effects']==0,'UNAUTHORIZED_PRODUCTION')
        if last is not None:ck(row['before_sha']==last,'BEFORE_AFTER_CHAIN')
        ck(row['cmd_id']==f'LAB-CMD-R227-{seed}-{arm}-'+('ATTACK' if k==1 else 'TARGET_TURN'),'UNEXPECTED_CMD_ID')
        ev.extend(row['detail']['events_added']);prior=dig(row);last=row['after_sha']
    ck(prior==m['head'] and last==dig(st) and ev==st['native_events'],'FINAL_CHAIN_AND_EVENT_MIRROR')
    ck(st['phase']=='CENSORED_SOURCE_EFFECT_WINDOW' and st['turn']==2 and st['r227']['turns']=={'R':1,'V':1},'CENSORED_TWO_TURN_WINDOW')
    for i,e in enumerate(ev,1):ck(e['seq']==i,'NATIVE_EVENT_SEQ')
    types=[e['action'] for e in ev];
    for typ in ['turn_start','R227_ATTACK_HIT_AND_CRITICAL_RNG','R227_DAMAGE_RNG_AFTER_DECLARATION','weapon_attack','turn_end','R227_SLOWED_TARGET_TURN_OBSERVATION','R227_STANDARD_PASS_NOT_A_COMBAT_BENCHMARK']:
        ck(typ in types,'MISSING_EVENT:'+typ)
    hit_e=next(e for e in ev if e['action']=='R227_ATTACK_HIT_AND_CRITICAL_RNG');attack=next(e for e in ev if e['action']=='weapon_attack');dmg_event=next(e for e in ev if e['action']=='R227_DAMAGE_RNG_AFTER_DECLARATION')
    atk=dice(seed,'R227-ATTACK-4D6',4,6);crit=dice(seed,'R227-CRIT-3D6',3,6);physical=dice(seed,'R227-PHYSICAL-DAMAGE-8D10',8,10)
    score=sum(atk)+72;kind='POSITIVE' if crit[:2]==[6,6] and crit[2]>=5 else 'NEGATIVE' if crit[:2]==[1,1] and crit[2]<=2 else 'NONE'
    hit=(score>83 or kind=='POSITIVE') and kind!='NEGATIVE';phys_raw=sum(physical)+35
    ck(hit_e['rolls']==atk and hit_e['crit_rolls']==crit and hit_e['roll_score']==score and hit_e['hit']==hit and hit_e['critical']==kind,'ATTACK_DICE_AND_HIT_SOURCE')
    ck(dmg_event['physical_rolls']==physical and attack['normal_damage']==phys_raw and attack['attack_roll_attempts']==[atk],'PHYSICAL_DICE_SOURCE')
    ck(attack['roll_score']==score and attack['critical']==kind and attack['hit']==hit and attack['from']=='R' and attack['to']=='V','NATIVE_ATTACK_VERIFICATION')
    phys_net=max(0,phys_raw+(80 if kind=='POSITIVE' else 0)-35) if hit else 0
    ck(attack['hp_loss_actual']==phys_net and attack['rd_applied']==(35 if hit else 0),'PHYSICAL_RD_INDEPENDENT_ARITHMETIC')
    want_magic=bool(hit)
    item_decs=[e for e in ev if e['action']=='R227_ITEM_DECLARATION_BEFORE_DAMAGE_RNG'];lightning=[e for e in ev if e['action']=='R227_ITEM_LIGHTNING_AND_CONDITION'];no_item=[e for e in ev if e['action']=='R227_ITEM_NO_ACTIVATION']
    ck(len(item_decs)==int(want_magic) and len(lightning)==int(want_magic) and len(no_item)==int(not want_magic),'ITEM_ACTION_ADMISSION')
    ck(st['r227']['item_used']==want_magic and st['r227']['item_recovery_rest_verified'] is False,'ITEM_ONCE_PER_8H_COOLDOWN')
    magic_net=0
    if want_magic:
        dc=item_decs[0];li=lightning[0];mdice=dice(seed,'R227-LIGHTNING-DAMAGE-5D8',5,8);raw_magic=sum(mdice)+3+(40 if kind=='POSITIVE' else 0);magical_rd=p['magic_RD_assumptions'][arm];magic_net=max(0,raw_magic-magical_rd)
        ck(types.index('R227_ATTACK_HIT_AND_CRITICAL_RNG')<types.index('R227_ITEM_DECLARATION_BEFORE_DAMAGE_RNG')<types.index('R227_DAMAGE_RNG_AFTER_DECLARATION')<types.index('weapon_attack')<types.index('R227_ITEM_LIGHTNING_AND_CONDITION'),'SOURCE_DECLARATION_BEFORE_DAMAGE_RNG')
        ck(dc['pa_spent']==22 and dc['source_sha256']==source_hash and dc['page_id']=='3f5c2b324ede81f5ac62fb940204cdac','ITEM_COST_AND_SOURCE')
        ck(dmg_event['lightning_rolls']==mdice and li['magic_dice']==mdice and li['magic_raw']==raw_magic and li['magic_effective']==magic_net and li['magic_rd']==magical_rd,'LIGHTNING_DAMAGE_AND_RD_ASSUMPTION')
        ck(li['hp_before']==734-phys_net and li['hp_after']==734-phys_net-magic_net,'LIGHTNING_HP_CONSERVATION')
        ck(li['semicanon_TEST'] is True and li['slow_applied'] is (magic_net>0) and li['slow_m']==(3 if magic_net>0 else 0) and li['slow_until']=='END_TARGET_NEXT_OWN_TURN','SLOW_ENFORCEMENT')
    else:ck(dmg_event['lightning_rolls']==[],'FALSE_ITEM_RNG_DRAW')
    ck(st['actors']['V']['hp']==734-phys_net-magic_net and st['actors']['R']['pa']==344-(22 if want_magic else 0),'FINAL_HP_PA_CONSERVATION')
    speed=next(e for e in ev if e['action']=='R227_SLOWED_TARGET_TURN_OBSERVATION');exp=[e for e in ev if e['action']=='R227_SOURCE_ITEM_SLOW_EXPIRES']
    ck(speed['available_speed_in_declared_4m_lab_fixture']==('1' if magic_net>0 else '4') and speed['source_speed_4m_is_TEST_assumption'] is True,'SLOWED_NEXT_TURN_SPEED')
    ck(len(exp)==int(magic_net>0) and st['actors']['V']['timed_source_speed_penalty_m']==0,'SLOW_EXPIRY_ONCE')
    if magic_net>0:ck(exp[0]['speed_before']=='1' and exp[0]['speed_after']=='4' and exp[0]['boundary']=='END_TARGET_NEXT_OWN_TURN','EXACT_EXPIRY_BOUNDARY')
    ck(types.count('turn_start')==2 and types.count('turn_end')==2 and types.count('weapon_attack')==1,'ACTION_ECONOMY')
    return {'seed':seed,'arm':arm,'hit':hit,'critical':kind,'physical_gross':phys_raw,'physical_net':phys_net,'magic_net':magic_net,'activation':want_magic,'events':len(ev),'commits':2,'hp_final':st['actors']['V']['hp'],'pa_final':st['actors']['R']['pa'],'head':m['head']}

def audit(root=ROOT):
    root=Path(root);pre=(root/'sources/R227_PREREG_BEFORE_EXEC.json').read_bytes();p=json.loads(pre);it=(root/'sources/R226_MANOPLA_PRIMARY_MECHANICAL_EXCERPT.json').read_bytes();pr=hashlib.sha256(pre).hexdigest();ih=hashlib.sha256(it).hexdigest()
    data=json.loads((root/'evidence/reports/R227_EXECUTION_RESULTS.json').read_text())
    ck(len(p['seeds'])==6 and len(data['pairs'])==6 and len(data['runs'])==12,'PREREG_DENOMINATOR')
    dbs=sorted((root/'evidence/db').glob('R227_MANOPLA_*.sqlite'))
    ck(len(dbs)==12,'DATABASE_DENOMINATOR')
    rec=[]
    for seed in p['seeds']:
        for arm in p['arms']:
            f=root/'evidence/db'/f'R227_MANOPLA_{arm}_S{seed}.sqlite'
            ck(f.exists(),'MISSING_NEW_RUN')
            rec.append(audit_one(f,p,ih,pr,arm,seed))
    ck({str(p) for p in dbs}=={str(root/'evidence/db'/f'R227_MANOPLA_{arm}_S{seed}.sqlite') for seed in p['seeds'] for arm in p['arms']},'EXTRA_RUN_NOT_IN_PREREG')
    by=collections.defaultdict(dict)
    for r in rec:by[r['seed']][r['arm']]=r
    pairs=[]
    for seed,v in sorted(by.items()):
        a=v['LIGHTNING_RD0'];b=v['LIGHTNING_RD100']
        ck((a['hit'],a['critical'],a['physical_gross'],a['physical_net'])==(b['hit'],b['critical'],b['physical_gross'],b['physical_net']),'PAIRED_OFFENSIVE_STREAM_DIVERGENCE')
        ck(b['hp_final']-a['hp_final']==a['magic_net']-b['magic_net'],'MAGIC_RD_DELTA_MISMATCH')
        pairs.append({'seed':seed,'hp_preserved_by_higher_rd':b['hp_final']-a['hp_final'],'activated':b['activation'],'rd0_magic':a['magic_net'],'rd100_magic':b['magic_net']})
    invalid=list((root/'evidence/quarantine').glob('R227_*.sqlite'))
    ck(len(invalid)==0,'UNEXPECTED_QUARANTINE')
    return {'status':'PASS_R227_INDEPENDENT_MAGIC_RD_SOURCE_CONTROL_PAIR_TEST','arms':len(rec),'pairs':len(pairs),'commits':sum(x['commits'] for x in rec),'events':sum(x['events'] for x in rec),'hits':sum(a['hit'] for a in rec if a['arm']=='LIGHTNING_RD0'), 'item_activations':sum(x['activated']*2 for x in pairs),'item_pa_total':sum(x['activated']*44 for x in pairs),'hp_preserved_by_rd100':sum(x['hp_preserved_by_higher_rd'] for x in pairs),'magic_rd100_net_total':sum(x['rd100_magic'] for x in pairs),'slow_expirations':sum(x['rd0_magic']>0 for x in pairs),'precommit_quarantines':0,'historical_replays':0,'pairs_data':pairs}
if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))

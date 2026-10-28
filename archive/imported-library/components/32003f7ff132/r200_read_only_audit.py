"""R200 separate-code read-only semantic replay of already executed R18 SQLite records.
No fight runner imports or restarts, no write access to combat databases.
"""
from __future__ import annotations
import hashlib,json,pathlib,sqlite3,collections,re
from fractions import Fraction
from r200_equipment_and_profiles import build_profile,SOURCES
BASE=pathlib.Path(__file__).resolve().parents[1]
PRE=json.loads((BASE/'source/R200_PRE_REG.json').read_text())
PRE_SHA=hashlib.sha256((BASE/'source/R200_PRE_REG.json').read_bytes()).hexdigest()
VERSION='R200-SOURCE-FROZEN-ED-REF-01-SWORD-PHYSICAL-AND-RING-PROXY-LAB-1'
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def check(x,m):
    if not x:raise AssertionError(m)
def audit_one(path):
    p=pathlib.Path(path)
    c=sqlite3.connect(f'file:{p.as_posix()}?mode=ro',uri=True)
    try:
        meta=dict(c.execute('SELECT key,value FROM meta'))
        check(c.execute('SELECT COUNT(*) FROM pending').fetchone()[0]==0,'PENDING_INTENT')
        rows=list(c.execute('SELECT seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha FROM events ORDER BY seq'))
        st=json.loads(meta['state']);rev=int(meta['revision'])
        check(len(rows)==rev,'REV_DRIFT')
        check(st['phase'] in ('ACTIVE','FINISHED'),'PHASE_UNEXPECTED')
        check(st['r200_pre_sha']==PRE_SHA,'PRE_REG_DRIFT')
        check(st['r200_policy'] in PRE['policies'],'UNKNOWN_POLICY')
        check(st['scope']=='LAB_SOURCE_PROFILE_BASIC_PHYSICAL_ATTACKS_WITH_EXPLICIT_ASSUMPTIONS','SCOPE_UNEXPECTED')
        ref=next(x for x in st['actors'] if x.startswith('ED-REF-01'))
        pair=st['pair'];check(len(pair)==2 and ref in pair,'PAIR_NOT_TWO')
        level=1 if ref.endswith('B1') else 6
        pr=build_profile(level)
        magic=st['r200_policy']!='SEM_MAGIA_ITEM'
        r=st['ring'];check(r['active']==magic and r['source']==SOURCES['ring'],'RING_STATE_DRIFT')
        check(r['source_rank']=='UNPUBLISHED','HIDDEN_RANK_PROMOTION')
        stats=st['actors'][ref]['stats'];rr=st['actors'][ref]['resource']
        check(stats['damage_dice']==[list(pr['weapon']['physical_dice'])],'PHYSICAL_DICE_CHANGED')
        check(stats['damage_flat']==pr['ff_damage_bonus'],'FF_VALUE_DRIFT')
        check(Fraction(str(stats['ca']))==Fraction(pr['ca_physical_exact']),'PHYSICAL_CA_CHANGED')
        check(Fraction(str(rr['ca']))==Fraction(pr['ca_physical_exact'])+(2 if magic else 0),'MAGIC_CA_DRIFT')
        check(rr['pa']==pr['natural_pa_max']-(13 if magic else 0),'DAILY_COST_NOT_PRESERVED')
        prev=meta['genesis'];last_after=None;ev_count=0;attacks=0;damage_by=collections.Counter();hits=collections.Counter()
        for j,(seq,cmd,prv,rowjson,rhash,bef,aft) in enumerate(rows,1):
            row=json.loads(rowjson)
            check(seq==j and row['seq']==j and cmd==row['cmd_id'],'SEQ_OR_CMD_DRIFT')
            check(prv==prev==row['prev'],'HASH_CHAIN_BREAK')
            check(sha(row)==rhash and bef==row['before_sha'] and aft==row['after_sha'],'HASH_FORGERY_MISMATCH')
            if last_after is not None:check(bef==last_after,'BEFORE_AFTER_BREAK')
            prev=rhash;last_after=aft
            check(row['official_effects']==0,'OFFICIAL_EFFECT_CLAIM')
            if j==1:
                check(row['kind']=='R200_SOURCE_SCOPED_INIT','INVALID_INIT')
                check(row['payload']['policy']==st['r200_policy'],'INIT_POLICY_DRIFT')
                continue
            check(row['kind']=='R200_SOURCE_SWORD_OR_BEAST_ATTACK','UNSUPPORTED_ATTACK_KIND')
            detail=row['detail'];ev=detail['attack'];payload=row['payload']
            actor=payload['actor'];target=payload['target'];actor_stats=st['actors'][actor]['stats']
            check(ev['from']==actor and ev['to']==target and detail['to']==target,'TARGET_CHANGED')
            check(detail['tape']==payload['roll_tape'],'TAPE_CHANGED')
            check(ev['damage_roll_groups']==detail['tape']['damage'],'DAMAGE_ROLL_CHANGED')
            check(ev['critical_sequence']==detail['tape']['crit'],'CRIT_TAPE_CHANGED')
            bonus=actor_stats['attack_bonus'];rolls=detail['tape']['hit']
            check(ev['attack_roll_attempts']==rolls,'ATTACK_ROLLS_CHANGED')
            expected=(min(map(sum,rolls))+bonus-2 if ev['weak_attacker'] else sum(rolls[0])+bonus)
            check(ev['roll_score']==expected,'ATTACK_SCORE_IMPOSSIBLE')
            check(len(ev['damage_roll_groups'])==len(actor_stats['damage_dice']),'DMG_GROUP_COUNT')
            for q,(n,sides) in zip(ev['damage_roll_groups'],actor_stats['damage_dice']):
                check(len(q)==n and all(1<=x<=sides for x in q),'DICE_ROLL_OUT_OF_RANGE')
            base_dmg=sum(sum(g) for g in ev['damage_roll_groups'])+actor_stats['damage_flat']
            crit=ev['critical_sequence'];expect_crit='POSITIVE' if crit[:2]==[6,6] and crit[2]>=5 else ('NEGATIVE' if crit[:2]==[1,1] and crit[2]<=2 else 'NONE')
            check(ev['critical']==expect_crit,'CRITICAL_DRIFT')
            ca=Fraction(ev['ca_exact'])
            check(ca==Fraction(str(st['actors'][target]['stats']['ca']))+(2 if magic and target==ref else 0),'CA_TARGET_MISMATCH')
            hit=(ev['roll_score']>ca or expect_crit=='POSITIVE') and expect_crit!='NEGATIVE'
            check(ev['hit']==hit,'HIT_DRIFT')
            crit_max=sum(n*sides for n,sides in actor_stats['damage_dice'])
            raw=base_dmg+(crit_max if expect_crit=='POSITIVE' and hit else 0) if hit else 0
            check(ev['raw']==raw,'RAW_DAMAGE_FABRICATED')
            expected_rd=st['actors'][target]['stats']['rd']
            check(ev['rd_applied']==(expected_rd if hit else 0),'RD_DRIFT')
            expected_net=max(0,raw-expected_rd) if hit else 0
            check(ev['net']==expected_net,'POST_RD_DRIFT')
            check(ev['after_hp']==max(0,ev['before_hp']-expected_net),'HP_TRANSITION_DRIFT')
            check(ev['hp_loss_actual']==ev['before_hp']-ev['after_hp'],'HP_ACTUAL_DRIFT')
            check(ev['overkill']==max(0,expected_net-ev['before_hp']),'OVERKILL_DRIFT')
            attacks+=1;damage_by[actor]+=ev['hp_loss_actual'];hits[actor]+=int(hit)
            ev_count+=len(detail.get('events_added',[]))
        check(prev==meta['head'] and last_after==sha(st),'HEAD_OR_SNAPSHOT_DRIFT')
        check(len(st['native_events'])==1+ev_count,'NATIVE_EVENT_COUNT_DRIFT')
        check(len(st['history'])==attacks,'HISTORY_ATTACK_COUNT_DRIFT')
        check(st['metrics']['attempts']==attacks,'ATTEMPTS_DRIFT')
        check(st['metrics']['hits']==sum(hits.values()),'HITS_DRIFT')
        if st['phase']=='FINISHED':
            check(st['winner'] in pair and st['actors'][next(x for x in pair if x!=st['winner'])]['resource']['hp']==0,'ILLEGAL_WINNER')
        else:check(st['winner'] is None,'CENSORED_HAS_WINNER')
        return {'id':p.stem,'status':st['phase'] if st['phase']=='FINISHED' else 'CENSORED_HORIZON',
           'winner':st['winner'],'level':level,'policy':st['r200_policy'],'seed':st['seed'],'commits':rev,
           'native_events':len(st['native_events']),'attacks':attacks,'damage_by_actor':dict(damage_by),
           'hits_by_actor':dict(hits),'head':meta['head']}
    finally:c.close()

def main():
    p=BASE/'evidence/db';dbs=sorted(p.glob('*.sqlite'))
    records=[audit_one(x) for x in dbs]
    original=json.loads((BASE/'evidence/R200_EXECUTED_FIGHTS.json').read_text())
    check(len(records)==len([x for x in original if x['db'] is not None]),'DB_COUNT_NOT_MATCH_REPORT')
    report={'result':'PASS_R200_INDEPENDENT_SOURCE_SEMANTIC_AUDIT','battles':len(records),
        'commits':sum(x['commits'] for x in records),'native_events':sum(x['native_events'] for x in records),
        'attacks':sum(x['attacks'] for x in records),'KO':sum(x['status']=='FINISHED' for x in records),
        'censored':sum(x['status']=='CENSORED_HORIZON' for x in records),
        'precommit_ties':sum(x['status']=='PRECOMMIT_TIE_HOLD' for x in original),
        'source_claims':{'ring_rank':'UNKNOWN','beast_luta_prof':'TEST_HYPOTHESIS'},
        'human_independent_audit':False,'official_contract_credit':0}
    (BASE/'evidence/R200_AUDIT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

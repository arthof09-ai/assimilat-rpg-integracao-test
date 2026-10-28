#!/usr/bin/env python3
"""DMG R09: discrete exact, source-conditional bounded attack model.
No VLAB engine, no real combat execution, no Notion or canonical writes.
Prior DMG R08 files read-only. New model only: reaction economy, hit thresholds,
expected attempted attacks to defeat 38 HP, possible crit resolution boundaries.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import hashlib, json

here = Path(__file__).resolve().parent
tests = 0
def check(cond, message):
    global tests
    tests += 1
    if not cond: raise AssertionError(message)
def show(q):
    return {"fraction": str(q), "decimal": round(float(q), 12)}
def expected_attempts(hp, damage_faces, hit_p):
    """E(h)=[1+p*average(E(h-d))+(1-p)*E(h)] -> (1/p)+average(E(h-d)).
    Damage faces correspond to independent hit-conditioned damage; no crit.
    """
    if hit_p == 0: return None
    E = [Q(0)]*(hp+1)
    for h in range(1, hp+1):
        E[h] = 1/hit_p + sum(E[max(0,h-d)] for d in damage_faces)/len(damage_faces)
    return E[hp]
def exact_survival(hp, damage_faces, hit_p, attempts):
    states = {hp: Q(1)}
    for _ in range(attempts):
        fresh = {}
        for remaining, prob in states.items():
            if remaining == 0:
                fresh[0] = fresh.get(0,Q(0))+prob
                continue
            fresh[remaining] = fresh.get(remaining,Q(0))+prob*(1-hit_p)
            for d in damage_faces:
                next_remaining=max(0,remaining-d)
                fresh[next_remaining]=fresh.get(next_remaining,Q(0))+prob*hit_p/len(damage_faces)
        check(sum(fresh.values())==1, "probabilities total 1")
        states=fresh
    return sum(prob for remain,prob in states.items() if remain > 0)

# Frozen authoritative source-specific numbers:
# Cabra B1 source 391c... Investida authorized Luta+6 only (VLAB R34)
# Cabra Esquiva26 Reflexo+6 only (VLAB R36/R39B); R37 defensive ties.
# Frigido B5 source f0dc... Rabada Luta+6 only (VLAB R32).
goat_attack=[die+13+6 for die in range(1,7)] # 20..25
frig_attack=[die+18+6 for die in range(1,7)] # 25..30
goat_damage=[die+13-5 for die in range(1,7)] # 9..14 (RD5)
frig_damage=[die+18-5 for die in range(1,7)] # 14..19 (RD5)
goat_no_evade=Q(sum(x>20 for x in goat_attack),6)
goat_evade=Q(sum(x>26 for x in goat_attack),6)
frig_no_evade=Q(sum(x>20 for x in frig_attack),6)
frig_evade=Q(sum(x>26 for x in frig_attack),6)
check(goat_attack==list(range(20,26)), "goat attack domain")
check(frig_attack==list(range(25,31)), "frig attack domain")
check(goat_damage==list(range(9,15)), "goat net damage domain")
check(frig_damage==list(range(14,20)), "frig net damage domain")
check((goat_no_evade,goat_evade,frig_no_evade,frig_evade)==(Q(5,6),Q(0),Q(1),Q(2,3)), "source hit probabilities")
check(goat_no_evade*Q(sum(goat_damage),6)==Q(115,12), "goat expected attack without evasion")
check(frig_no_evade*Q(sum(frig_damage),6)==Q(33,2), "frig expected attack without evasion")
check(frig_evade*Q(sum(frig_damage),6)==Q(11), "frig expected attack with evasion")
check(goat_evade==0, "all 1d6 goat attacks neutralized if legal evasion is renewed")

# Exact renewal model: one incoming Investida per opportunity, reaction initially
# ready, pre-declared for each attack, refresh by defender's own turn, 0PA.
# Under such bounded conditions, unchanged HP after arbitrary finite n.
for n in (1,2,8,16,100):
    check((Q(1)-goat_evade)**n==1, f"deterministic absence of basic damaging hits through n={n}")
# Without Esquiva, or Evasion only on the first ever incoming attack:
goat_e0=expected_attempts(38,goat_damage,goat_no_evade)
goat_efirst=1+goat_e0
check(goat_e0==Q(4979,1080),"goat full HP 38 fixed-target expected attempts")
check(goat_efirst==Q(6059,1080),"EVADE_FIRST one guaranteed blocked attempt")

# R09 verifies R08 two-hit 1/36, and Master's newly supplied prediction
# via a genuinely independent recurrence, rather than averaging hit damage.
two_fr_hit=Q(sum(a+b>=38 for a,b in product(frig_damage,repeat=2)),36)
check(two_fr_hit==Q(1,36), "only double 19 damage kills goat in two hits")
frig_e0=expected_attempts(38,frig_damage,frig_no_evade)
frig_econt=expected_attempts(38,frig_damage,frig_evade)
check(frig_e0==Q(107,36), "Frigido E tries DECLINE")
check(frig_econt==Q(107,24), "Frigido E tries continuous Evasion")
check(frig_econt / frig_e0 == Q(3,2), "Frigido E attempts +50%")
frig_survive8_e=exact_survival(38,frig_damage,frig_evade,8)
frig_survive8_base=exact_survival(38,frig_damage,frig_no_evade,8)
check(frig_survive8_base==0, "no evasion, <=3 successful attempts kills")
check(0<frig_survive8_e<1,"Frigido ongoing Evasion finite chance survives 8 tries")

# Two incoming attacks in the same reaction-refresh window:
# One protected, second no reaction; no crit, unchanged geometry assumed.
two_incoming_second_p = goat_no_evade
two_incoming_expected_net = goat_no_evade*Q(sum(goat_damage),6)
check(two_incoming_second_p==Q(5,6), "once reaction spent, next uses CA20")
check(two_incoming_expected_net==Q(115,12), "R39B-style second incoming expected net")
check(goat_evade==0 and goat_no_evade>0,"counterexample to universal permanent invulnerability")

# Critical verification probability is NOT a critical-bypasses-evasion rule.
critical_verification_p=Q(2,216)
hyp_crit_probability_no_event_16=(1-critical_verification_p)**16
check(critical_verification_p==Q(1,108),"system +0 critical verification odds")
check(0<hyp_crit_probability_no_event_16<1,"hypothetical no-crit probability")

past_files = ["R08_PSV_MECHANICAL.md","R08_RESULTS_MECHANICAL.json",
              "R08_VLAB_HANDOFF_READONLY.json","R08_REPLAY_MECHANICAL.py"]
old_hashes={name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in past_files}
report={
 "operation":"OP-DMG-CORPUS-EMP-01","round":"R09","environment":"MESTRE-SIDE",
 "status":"R09 mathematics complete / VLAB new full-fight admission pending","executed_new_VLAB_combats":0,"canonical_writes":0,
 "official_baseline":"DMG-RANK-01 v1.1 unchanged",
 "evidence_classification":{
  "verified_rules":["Cabra Investida +6 hit-only R34","Cabra Esquiva Reflexo+6 R36, R39B reused","Defensive ties winner R37","R26 reaction refresh at start own turn","R39B second attack landed after reaction spent"],
  "math_only":["Cabra repeat one attack per refresh zero ordinary damaging hits under continuous legal precommitted evade","Frigido vs Cabra exact duration no crit","multiple attackers model separate"],
  "unresolved":["Critical verification interaction with a missed attack / Esquiva","new full-fight initiative values and legal reaction policy","different offensive options/attack of opportunity Luta scope","R40 native admission"],
 },
 "source_ids":{
  "Cobra":"391c2b324ede8252b0cc810423cdbfa6",
  "Frigido":"f0dc2b324ede820ab9470168d4a53315",
  "VLAB_operation":"3f3c2b324ede819496ddd7f93bd7e5d2",
  "Combat":"3ebc2b324ede81f1be4be8804ac113c0",
  "Besta":"3ebc2b324ede81f4992ac88a3588cacd"},
 "source_attack_domains":{
  "goat_investida_scores":goat_attack,"frig_rabada_scores":frig_attack,
  "goat_net_damage_vs_RD5":goat_damage,
  "frig_net_damage_vs_RD5":frig_damage},
 "policies":{
  "DECLINE":{"goat_vs_goat_hit_probability":show(goat_no_evade),
             "damage_expected_per_attack_goat":show(two_incoming_expected_net),
             "expected_incoming_goat_attacks_to_deal_HP38_vs_passive_goat":show(goat_e0)},
  "EVADE_FIRST_ONE_TIME":{"first_incoming_attack_damage":0,
      "expected_incoming_goat_attacks_to_deal_HP38_vs_passive_goat":show(goat_efirst)},
  "EVADE_WHEN_AVAILABLE":{"legal_scope":"one Investida arrives per renewal cycle, defender always has a Reaction and announces Esquiva BEFORE the result",
    "goat_vs_goat_hit_probability_noncritical":show(goat_evade),
    "HP_drain_after_8_and_16_opportunities":0,
    "mathematical_expected_attempts_to_kill":"INFINITY ONLY IN THIS CLOSED NONCRITICAL ONE-ATTACK MODEL, NOT A CANONICAL FIGHT"},
  "TWO_INCOMING_BEFORE_REFRESH":{"first_blocked":True,"second_has_no_Reaction":True,
    "second_hit_probability_against_CA20":show(two_incoming_second_p),
    "expected_second_attack_damage":show(two_incoming_expected_net),
    "prior_native_R39B_observed_second_hit_damage":14}
 },
 "frigido_vs_goat":{
  "p_hit_decline":show(frig_no_evade),"p_hit_evasion26":show(frig_evade),
  "p_two_hits_exact_kill":show(two_fr_hit),
  "E_attacks_decline_noncritical":show(frig_e0),
  "E_attacks_evasion_noncritical":show(frig_econt),
  "ratio":show(frig_econt/frig_e0),
  "p_goat_survives_8_frig_attacks_evasion":show(frig_survive8_e),
  "p_goat_survives_8_frig_attacks_decline":show(frig_survive8_base)
 },
 "crit":{
  "system_base_critical_verification_probability":show(critical_verification_p),
  "probability_0_critical_verification_in_16_attempts_IF_independent_per_attempt":show(hyp_crit_probability_no_event_16),
  "critical_auto_hit_or_bypass_evasion":"NOT RESOLVED; 1/108 does not authorize bypass"
 },
 "native_preexisting_observations":{
  "R34":{"source":"Notion OP; coordinator independently audited original ZIP per Mestre","three_rabadas_hit_two_investidas_miss":True},
  "R37":{"source":"Notion OP; coordinator independently audited ZIP per Mestre",
         "censored_scenes":2,"rounds_each":8,"attacks_each":16,"reactions_each":16,"HP_end":"38/38","winner":None,
         "DECLINE_control_scenes_finished":2},
  "R39B":{"source":"Notion OP; not freshly independently replayed by DMG",
           "two_sequential_incoming":True,"one_evasion_blocks_first":True,
           "second_damage_net":14,"target_HP":"38 -> 24"}
 },
 "preserved_R08_artifact_hashes_sha256":old_hashes,
 "exact_local_checks_passed":tests,
 "scope_notes":["The numbers are attack-opportunity math, not whole-fight winners or initiative model.",
                "No retroactive choice of Evasion by reading dice outcomes.",
                "Movement, geometry, initiative, opportunity attacks and critical bypass not modeled.",
                "Only one attacking allowed per reaction-renewal interval for deterministic no-damage proof.",
                "No write to Notion, no VLAB task accepted or executed."]}
out=here/"R09_RESULTS_EXACT.json"
out.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
read=json.loads(out.read_text(encoding="utf-8"))
check(read["frigido_vs_goat"]["E_attacks_evasion_noncritical"]["fraction"]=="107/24","JSON readback")
check(all(hashlib.sha256((here/name).read_bytes()).hexdigest()==sha for name,sha in old_hashes.items()),"R08 untouched")
# persist final test count after readback
report["exact_local_checks_passed"]=tests
out.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
assert json.loads(out.read_text())["exact_local_checks_passed"]==tests
print("R09_EXACT_PASS",tests)
print("goat E tries",goat_e0,"goat evade_first",goat_efirst)
print("frig E tries",frig_e0,frig_econt, "survival after 8 attacks",frig_survive8_e,float(frig_survive8_e))
print("expected 2nd attack before reaction refresh",two_incoming_expected_net)
print("JSON_SHA256",hashlib.sha256(out.read_bytes()).hexdigest())

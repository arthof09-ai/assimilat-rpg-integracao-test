#!/usr/bin/env python3
"""Secondary read-only DMG R10 audit, independent of R10_MODEL implementation.
Derives bilateral distribution via scipy binomial PMFs; two-threat counterexample;
verifies original R40/R39B manifests and discovers adapter-vs-Mestre disagreement.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import zipfile,json,math,subprocess,sys,ast
import numpy as np
from scipy.stats import binom

ROOT=Path(__file__).resolve().parent
R=ROOT/'source_readonly'
main=json.loads((ROOT/'R10_RESULTS.json').read_text())
q=1/108
H=2400
n=np.arange(H+1)
# Different oracle: X_n ~ Binomial(n,p). Crit damage 15..20, KO if first 2 sum>=38
# (probability 1/6), otherwise third positive crit kills.
S=binom.pmf(0,n,q)+binom.pmf(1,n,q)+(5/6)*binom.pmf(2,n,q)
S[0]=1.0
E=float(np.sum(S[:-1]**2))
Ftime=S[:-1]-S[1:]
pA=float(np.sum(Ftime*S[:-1]))
assert abs(E-main['goat_crit_only']['health_state_matrix_bilateral']['mean_rounds'])<1e-9
assert abs(pA-main['goat_crit_only']['health_state_matrix_bilateral']['p_first_actor_wins'])<1e-11
assert max(abs(S[t]**2-main['goat_crit_only']['health_state_matrix_bilateral']['survival_horizon'][str(t)]) for t in [8,16,50,100,200,500,1000])<1e-10

# State machine independent of the main; each attack has exactly defined discrete outcomes.
qF=F(1,108)
pr_hit_noevade=F(5,6)
pmf_block={0:1-qF}
for d in range(15,21):pmf_block[d]=qF/6
pmf_free={0:(1-qF)*(1-pr_hit_noevade)}
for d in range(9,15):pmf_free[d]=(1-qF)*pr_hit_noevade/6
for d in range(15,21):pmf_free[d]=qF/6
assert sum(pmf_block.values())==sum(pmf_free.values())==1

def expected_windows(hp, series, horizon=200):
    # Independent float absorbing-state propagation; fractions above give exact PMF.
    state=np.zeros(hp+1,dtype=float);state[hp]=1.0
    mat=[]
    for pmf in series:
        T=np.zeros((hp+1,hp+1),dtype=float);T[0,0]=1.0
        for remaining in range(1,hp+1):
            for damage,w in pmf.items(): T[remaining,max(0,remaining-damage)]+=float(w)
        mat.append(T)
    e=0.;survival=[]
    for step in range(horizon):
        survive=float(state[1:].sum()); survival.append(survive);e+=survive
        for M in mat:state=state@M
        if survive<1e-14 and step>50:break
    return e,survival

singleE,singleSurv=expected_windows(38,[pmf_block],horizon=10000)
twoE,twoSurv=expected_windows(38,[pmf_block,pmf_free],horizon=100)
freeE,freeSurv=expected_windows(38,[pmf_free],horizon=100)
assert abs(singleE-306)<1e-8
expected_first=sum(F(k)*v for k,v in pmf_block.items())
expected_second=sum(F(k)*v for k,v in pmf_free.items())
assert expected_first==F(35,216)
assert expected_second>F(9)

# Margins exact q used only as counterfactual; check no margin label assigned to real Goat.
margin_range={m:F(2+m,216) for m in range(5)}
assert margin_range[0]==F(1,108) and margin_range[4]==F(1,36)

zip_values={
'R40':(R/'VLAB_R40_INTEGRACAO_TRES_ATORES_VALIDACAO_MECANICA_MESTRE_ONLY.zip','2be2d7b8cb39fd4aa340afc07a200c8c1c5234475256635e2dad85a2aeeb1e71'),
'R39B':(R/'VLAB_R39B_ERRATA_FONTE_INVESTIDA_REACAO_MESTRE_ONLY.zip','3333d215042d0de9ec92a1d10d125f2417864cd5dc474e5f62b9090bf3552166'),
}
zip_checks={}
for key,(path,expected_hash) in zip_values.items():
    actual=sha256(path.read_bytes()).hexdigest()
    assert actual==expected_hash
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        zip_checks[key]={'sha256':actual,'entries':len(z.namelist()),'crc':'PASS','size_bytes':path.stat().st_size}
        if key=='R40':
            manifest=json.loads(z.read('delivery/R40_DELTA_FILE_MANIFEST.json'))
            assert len(manifest['sha256'])==25
            assert all(sha256(z.read(name)).hexdigest()==v for name,v in manifest['sha256'].items())
            zip_checks[key]['manifest_25_shas']='PASS'
        else:
            m=json.loads(z.read('R39B_MANIFEST.json'))
            zip_checks[key]['manifest_type']=m.get('schema','present')

# Audited original SQLite/backup by original standalone auditor without native engine.
audit={}
for seed in [91001,91002]:
    p=ROOT/f'R10_R40_AUDIT_{seed}.json'; v=json.loads(p.read_text())
    assert v['status']=='PASS' and v['mechanical']=='PASS'
    audit[str(seed)]={k:v[k] for k in ['status','events','attacks','reactions','second_reactions_rejected','pushes','movement_actions','winner','rounds']}
assert sum(x['events'] for x in audit.values())==44
assert sum(x['attacks'] for x in audit.values())==42

# Key static source contradiction with Master's NEW binding decision.
engine=R/'v081_runtime_readonly'/'vlab_effects_v08.py'
r40=R/'R40_extracted'/'extension'/'r40_integrated_three_actors.py'
aud=R/'R40_extracted'/'extension'/'verify_r40_mechanics_standalone.py'
s_eng=engine.read_text();s_r40=r40.read_text();s_aud=aud.read_text()
assert 'hit=roll_score>d.ca' in s_eng
assert "negated=bool(defense_event.get('damage_negated'))" in s_eng
assert "damage_tag='impacto',rd=Resistances(general=5" in s_r40
assert "hit_bool=score>20" in s_aud
assert "net=0 if (not hit_bool or re is not None) else max(0,raw-5)" in s_aud
assert "raw['critical_positive']" not in s_r40[s_r40.index('def do_turn'):s_r40.index('def payload')]
probe=json.loads((ROOT/'R10_NATIVE_CRITICAL_GAP.json').read_text())
assert probe['status']=='CONTROLLED_NATIVE_MODULE_COMPATIBILITY_DEFECT_REPRODUCED'

# R40 observed 0 crit in 42 attacks is unsurprising; R40 holdout positive 4/1200 merits cautious note.
prob_zero_42=(1-q)**42
p_at_most_four_in_1200=float(binom.cdf(4,1200,q))
# Generic 95% sampling SE for mean model under preregistered random sampling:
S0=S[:-1]**2
variance_time=float(np.sum((2*np.arange(H)+1)*S0)-E**2)
SE=math.sqrt(variance_time/20000)
mc=main['sampling']['MC_BILATERAL']['goat_symmetric_always_evasion']['mean_rounds_observed_uncensored']
assert abs(mc-E)<3*SE

output={
 'method':'independent scipy.stats binomial marginal kill-time; Fraction probability-state sequences; stdlib ZIP SHA+CRC+manifest and historical native unit fixture readback',
 'independent_oracle':{'E_rounds':E,'first_actor_win_p':pA,'difference_vs_original_markov':E-main['goat_crit_only']['health_state_matrix_bilateral']['mean_rounds'],
    'analytic_round_sd':math.sqrt(variance_time),'MC_mean_standard_error_at_20000':SE,
    'actual_MC_mean_20000':mc},
 'two_incoming_in_one_reaction_window':{
  'first_protected_attack_expected_net':{'fraction':str(expected_first),'decimal':float(expected_first)},
  'second_unprotected_attack_expected_net':{'fraction':str(expected_second),'decimal':float(expected_second)},
  'expected_damage_per_two_attempt_window':{'fraction':str(expected_first+expected_second),'decimal':float(expected_first+expected_second)},
  'expected_reaction_windows_to_KO_38HP_two_threats':twoE,
  'expected_reaction_windows_to_KO_38HP_single_protected_threat':singleE,
  'expected_attempts_HP38_one_unprotected_threat':freeE,
  'p_alive_after_8_windows_two_threats':twoSurv[8],
  'scope':'one defended incoming + one unprotected incoming before own-turn refresh; no actual 3-actor full fight; no geometry/initiative/crit-failure effects; original R39B sequence proves qualitative scenario'},
 'audited_original_R40_R39B_packages':zip_checks,
 'read_only_VLAB_R40_independent_verifier_results':audit,
 'historical_native_core_byte_sha256':sha256(engine.read_bytes()).hexdigest(),
 'critical_auto_hit_source_conflict':{
   'historic_engine_expression':'hit=roll_score>d.ca',
   'historic_reaction_expression':"negated=bool(defense_event.get('damage_negated'))",
   'R40_independent_auditor_expression':'hit_bool=score>20',
   'synthetic_live_original_core_probe_result':'AUTO-CRIT MISS WRONG RESULT 0 DAMAGE; expected 17 net for known 6,6,5 crit vs numeric CA/Esquiva26',
   'R40_actual_42_attack_incidents':'0 positive crit, so native scene result not falsified by that missing branch',
   'gate':'VLAB must verify critical flag reaches reaction and hit resolver, official source admitted, replay independently checked'},
 'R40_sampling_context':{'probability_0_critical_among_42_independent_attacks':prob_zero_42,
    'R40_positive_crit_out_of_1200':4,'expected':1200*q,'one_sided_exploratory_P_X_le_4':p_at_most_four_in_1200,
    'disclaimer':'post hoc one-sided look; preregistered multinomial criterion alpha 1% not rejected, does not imply biased RNG'},
 'baseline_R09_sha256_before_after_preserved':main['original_immutable_sha256'],
 'canonical_writes':0,'new_VLAB_attacks':0,'native_original_module_fixture_runs':2
}
p=ROOT/'R10_SECONDARY_AUDIT.json';p.write_text(json.dumps(output,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'independent_E_rounds':E,'SD_rounds':math.sqrt(variance_time),'MC_SE':SE,
       'two_threat_windows_E':twoE,'one_threat_windows_E':singleE,
       'first_damage_expected':float(expected_first),'second_expected':float(expected_second),
       'prob_no_crit_42':prob_zero_42,'holdout_le4':p_at_most_four_in_1200,'audits':audit},ensure_ascii=False,indent=2))

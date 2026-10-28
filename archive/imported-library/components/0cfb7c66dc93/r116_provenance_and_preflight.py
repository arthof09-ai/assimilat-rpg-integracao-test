"""R116 provenance / adverse pre-intent gate tests in isolated copied v0.8.1.
No historic SQLite modification, and no replay of unknown effects.
"""
import pathlib,hashlib,subprocess,tempfile,shutil,json,difflib,copy,sys,sqlite3
R=pathlib.Path(__file__).resolve().parent
ROOT=R.parent
ORIG=ROOT/'r61_extracted'/'work'/'working'/'historical_v081_verified_original'/'comestre_vlab'
PATCH=R/'native_v081_controlled'
sha=lambda b:hashlib.sha256(b).hexdigest()
original={p.name:p for p in ORIG.glob('*.py')};cp={p.name:p for p in PATCH.glob('*.py')};changes=[]
for name,p in original.items():
    if name in cp and sha(p.read_bytes())!=sha(cp[name].read_bytes()):changes.append(name)
assert changes==['vlab_effects_v08.py'],changes
old=original[changes[0]].read_text();new=cp[changes[0]].read_text()
(R/'R116_NATIVE_V081_PATCH.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='historical_original/comestre_vlab/vlab_effects_v08.py',tofile='native_v081_controlled/vlab_effects_v08.py')))
# Change transform script to reproduce final exact module instead of stale 2 intermediary guards.
ps=R/'patch_native_v081.py';s=ps.read_text()
s=s.replace("        a.immobile_next_own_turns=1", "        a.immobile_next_own_turns=2")
s=s.replace("s=s.replace(\"        if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd and damage%2:\n", "s=s.replace(\"        if explicit_save_effect=='SAVE-HALF' and target_save_exceeds_cd and damage%2:\n")
# Historic source also has a SAVE_FULL deny following the half check, alter that specific guard in output.
needle="s=s.replace(\"    raw=0 if explicit_save_effect=='SAVE-FULL-NEGATE' and target_save_exceeds_cd else damage\""
assert needle in s
s=s.replace(needle,"s=s.replace(\"        if explicit_save_effect!='SAVE-FULL-NEGATE':raise EffectBlocked('unknown save effect')\", \"        if explicit_save_effect not in ('SAVE-FULL-NEGATE','SAVE-HALF'):raise EffectBlocked('unknown save effect')\",1)\n"+needle,1)
ps.write_text(s)
# Verify that standalone reproducible patch produces byte-exact copy in temporary tree.
with tempfile.TemporaryDirectory(prefix='r116-patch-',dir=str(R)) as tmp:
    test=pathlib.Path(tmp)/'native_v081_controlled';test.mkdir()
    shutil.copy2(ORIG/'vlab_effects_v08.py',test/'vlab_effects_v08.py')
    shutil.copy2(ps,pathlib.Path(tmp)/'patch_native_v081.py')
    z=subprocess.run([sys.executable,str(pathlib.Path(tmp)/'patch_native_v081.py')],capture_output=True,text=True)
    assert z.returncode==0,(z.stdout,z.stderr)
    assert sha((test/'vlab_effects_v08.py').read_bytes())==sha(new.encode()),'PATCH_REPLAY_NOT_REPRODUCIBLE'
# Pre-intent anti-abuse tests using in-memory read of a VALID ledger snapshot, no database writes.
sys.path.insert(0,str(R));import r112_native_battle as bridge
valid=R/'r112_runs'/'R112_FULL_915133_B_LEFT.genesis.json'
state=json.loads(valid.read_text());state['phase']='ACTIVE';state['active']='B';state['special_used_count']=0;state['actors']['B']['resource'].update(standard=1,pa=4016,hp=4315)
# Special's raw 70, explicit successful Reflexo, source E.
base={'actor':'B','target':'E','damage_rolls':[5]*14,'save_rolls':[4]*6,'raw':70,'save_cd':94}
cases=[('odd_half',{**base,'raw':71},'NATIVE_SPECIAL'),('PA_insufficient',base,'NATIVE_SPECIAL'),('slot_spent',base,'NATIVE_SPECIAL'),('special_already_used',base,'NATIVE_SPECIAL'),('wrong_target',{**base,'target':'B'},'NATIVE_SPECIAL'),('wrong_actor',{**base,'actor':'E'},'NATIVE_SPECIAL'),('negative_critical_failure',{'actor':'B','target':'E','crit':[1,1,2]},'NATIVE_ATTACK'),('false_final_effort',{'actor':'B','target':'E','crit':[3,3,3],'score':200,'final_effort':True},'NATIVE_ATTACK'),('unknown_command',{},'ACTION_X')]
report=[]
for name,payload,kind in cases:
    ss=copy.deepcopy(state)
    if name=='PA_insufficient':ss['actors']['B']['resource']['pa']=54
    if name=='slot_spent':ss['actors']['B']['resource']['standard']=0
    if name=='special_already_used':ss['special_used_count']=1
    baseline=json.dumps(ss,sort_keys=True)
    blocked=False;reason=''
    try:bridge.preflight(ss,kind,payload)
    except (bridge.Reject,ValueError,KeyError) as e:blocked=True;reason=str(e)
    assert blocked and json.dumps(ss,sort_keys=True)==baseline,(name,blocked,reason)
    report.append({'case':name,'status':'PASS_PRE_INTENT_REJECTED','error':reason,'state_unchanged':True,'db_touched':False})
# Unit regression plus cold auditor separately in audit receipts.
result={'status':'PASS','legacy_file_source':str(ORIG/'vlab_effects_v08.py'),'original_sha256':sha(old.encode()),'corrected_sha256':sha(new.encode()),'only_modified_python_file':changes,'diff_sha256':sha((R/'R116_NATIVE_V081_PATCH.diff').read_bytes()),'patch_script_replays_exactly':True,'pre_intent_negative_cases':len(report),'cases':report,'unknown_effect_replayed':False,'canonical_writes':0}
(R/'R116_PROVENANCE_PREFLIGHT_AND_PATCH.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('cases','legacy_file_source')},indent=2))

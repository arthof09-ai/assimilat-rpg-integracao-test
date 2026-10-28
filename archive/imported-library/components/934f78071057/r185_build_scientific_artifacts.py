import pathlib,json,csv,sqlite3,hashlib,statistics,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=pathlib.Path('/mnt/data/vlab_r177_186_work/r176')
BEAST='https://app.notion.com/p/3f3c2b324ede813987deda0b382e83c7'
AUREN='https://app.notion.com/p/3ebc2b324ede814bb730d47dd7bd5f02'
VAROK='https://app.notion.com/p/3f6c2b324ede81f49ea9efbe1a811091'
COMBAT='https://app.notion.com/p/3ebc2b324ede81f1be4be8804ac113c0'
CREATE='https://app.notion.com/p/3ebc2b324ede81f4992ac88a3588cacd'
INIT=[]
for name,des,prof,rank,source,attack in [('Roc da Tempestade de Vidro',128,22,'L3',BEAST,'6d6+150'),('Grifo-Matriarca de Silica',116,22,'L3',BEAST,'6d6+138'),('Serpente Prismatica Regente',132,22,'L3',BEAST,'6d6+154'),('Crocodilo de Lodo Astral Anciao',64,22,'L3',BEAST,'6d6+134'),('Leviata de Ferro Mnemonico',60,22,'L4',BEAST,'6d6+142'),('Vaelthyr',128,26,'L4/Besta Divina',BEAST,'6d6+186')]:
 INIT.append({'entity':name,'rank':rank,'DES':des,'general_prof':prof,'source':source,'combat_initiative_rule':COMBAT,'beast_prof_rule':CREATE,'required_named_initiative_prof':None,'known_dice':'6d6','expression_without_named_skill':f'6d6+{des}','attack_expression_separate':attack,'norm_status':'NAMED_INITIATIVE_UNVERIFIED','applicability': 'CAN_COMPARE_ORDER_BY_PROVEN_BOUND_ONLY;NO_GENERAL_PROF_AUTO_IMPORT','source_version':'2026-10-08T02:25:14.539Z'})
INIT.append({'entity':'Sikong Varok','rank':'ON5','DES':27,'general_prof':None,'source':VAROK,'known_dice':'4d6','required_named_initiative_prof':2,'expression':'4d6+29','norm_status':'SHEET_PUBLISHED_SPECIFIC_INIT','source_version':'2026-10-16T10:33:26.087Z'})
INIT.append({'entity':'Sikong Auren','rank':'L3','DES':164,'general_prof':2,'source':AUREN,'known_dice':'6d6','required_named_initiative_prof':2,'expression':'6d6+166','norm_status':'SHEET_PUBLISHED_SPECIFIC_INIT','source_version':'2026-09-30T23:10:35.044Z'})
source={'R177_initiative_matrix':INIT,'exact_named_bestial_initiative_from_six_consulted':0,'bestial_candidates_consulted':6,'unsupported_import_general_prof':True,'tie_break':'NO_CANONICAL_TIE_RULE_LOCATED_IN_CONSULTED_COMBAT_SECTION','pending':'NAMED_BESTIAL_INITIATIVE_AND_EXTERNAL_MODIFIERS','decision':'NOT_CANONIZE_ANY_BEAST_PLUS22_ON_INIT'}
(ROOT/'source'/'R177_INITIATIVE_SOURCE_MATRIX.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
GEO={'R178_source_rules':{'combat':COMBAT,'beast':CREATE,'distance_melee_m':'UNKNOWN','contact':'ADJACENT_BLOCK_CONCEPT_EXISTS, NOT_METRIC_UNIVERSAL','AOO':'leaving adjacent block triggers opportunity with advantage, costs reaction','withdraw':'one standard then movement against one enemy','forced_movement_aoo':'NOT_INFERRED','grid_meters':'UNKNOWN'}, 'documented_range_tests':[{'character':'Sikong Iskiel','source':'https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966','weapon':'Arco da Asa Rasgada','range_m':80,'one_physical_arrow_each_attack':True},{'character':'Sikong Veyun','source':'https://app.notion.com/p/3f6c2b324ede819e879bebb795001ba','weapon':'Cetro da Prisao Prismatica','range_m':30,'PA_per_activation':65}], 'source_beast_reach_m':'UNKNOWN','R180_pilot_geometry':'SCENARIO_FROZEN_DIRECT_PHYSICAL_SURFACE_CONTACT_NO_MOVEMENT','certification':'SOURCE_NUMERIC_RANGE_TEST_IS_PREFLIGHT_ONLY, NOT_CAMPAIGN_POSITION_OR_FULL_SPATIAL_ENGINE'}
(ROOT/'source'/'R178_SOURCE_GEOMETRY_MATRIX.json').write_text(json.dumps(GEO,ensure_ascii=False,indent=2)+'\n')
candidates=[
 {'match':'Auren L3 × Roc L3','sources':[AUREN,BEAST],'reused':'R175;NO_NEW_FIGHT','attack_can_hit_both_ordinary':False,'impactful_reaction':'R50 Auren response after beast misses','initiative':'ROC_NAMED_PROF_UNKNOWN','reach':'CONTACT_TEST_ONLY','status':'DO_NOT_REPEAT'},
 {'match':'Auren L3 × Grifo L3','sources':[AUREN,BEAST],'reused':'R176;NO_NEW_FIGHT','attack_can_hit_both_ordinary':False,'initiative':'GRIFFIN_NAMED_PROF_UNKNOWN','status':'DO_NOT_REPEAT'},
 {'match':'Varok ON5 × Leviatã L4','sources':[VAROK,BEAST],'reused':False,'attack_can_hit_both_ordinary':True,'varok_attack_range':'4d6+100=104..124 versus Leviatã CA110','leviathan_attack_range':'6d6+142=148..178 versus Varok CA83','initiative':'BEAST_ALWAYS_FIRST_IN_NO_EXTERNAL_MODIFIER_ORDINARY_SCOPE:66>53','reaction':'VAROK_ARMOR_50PA_PREVENT70_AFTER_RD_ONCE_PER_SCENE','PA':'Varok324 free, Leviatã4260','reach':'CONTACT_TEST_ONLY','status':'SELECTED_SOURCE_SCOPED_EXPERIMENT_NOT_ED_NOT_OFFICIAL_BEAST'},
 {'match':'Liu Xiaua P5 × Macaco Rei P5','sources':['https://app.notion.com/p/0b4c2b324ede837cb6be818dc8e36010','https://app.notion.com/p/301c2b324ede828caccb813d3979267a'],'reused':False,'initiative':'BOTH_SKILL_PROF_UNRESOLVED','conflict':'Macaco HP sheet750 vs new base formula810; to-hit, PA free and RD uncertain','status':'SOURCE_HOLD_FULL_FIGHT'},
 {'match':'Iskiel ON5 × ranged geometry / Varok ON5','sources':['https://app.notion.com/p/3f6c2b324ede81a78a59d3d81fd5e966',VAROK],'range':'Iskiel bow80m sourced, numeric preflight safe; no fight executed','status':'R178_RANGE_PREFLIGHT_ONLY'}]
(ROOT/'source'/'R179_CANDIDATE_SHORTLIST.json').write_text(json.dumps({'coverage':{'candidate_pairs':len(candidates),'fully_source_admissible':0,'source_scoped_selected':1},'candidates':candidates},ensure_ascii=False,indent=2)+'\n')
res=json.loads((ROOT/'evidence'/'R184_PAIRED_RESULTS.json').read_text());rows=res['runs'];paired=[]
for seed in [17718001,17718002,17718011,17718012,17718013]:
 on=next(x for x in rows if x['seed']==seed and x['policy']=='ARMOR_ON_FIRST_SOURCE_ATTACK');off=next(x for x in rows if x['seed']==seed and x['policy']=='ARMOR_OFF')
 paired.append({'seed':seed,'cohort':'development' if seed==17718001 else ('validation' if seed==17718002 else 'holdout'),'rounds_armor':on['rounds'],'rounds_off':off['rounds'],'survival_round_delta':on['rounds']-off['rounds'],'winner_on':on['winner'],'winner_off':off['winner'],'armor_damage_prevented':on['metrics']['item_prevention'],'armor_PA_spent':on['metrics']['pa_activation'],'additional_varok_damage_to_beast':off['HP_final']['LEVIATHAN']-on['HP_final']['LEVIATHAN']})
hold=[x for x in paired if x['cohort']=='holdout']
scientific={'R180_new_source_scoped_physical_matchup':'VAROK_ON5_NPC_PROPOSAL_VS_LEVIATHAN_L4_PRECREATE','not_ED':True,'not_fully_source_admissible':True,'seed_unit':5,'paired_runs':10,'independent_beast_species':1,'independent_npc_profiles':1,'holdout_independent_seeds':3,'holdout_pre_registered_before_runs':True,'policies_not_independent':True,'hypothesis':'documented item reaction prevents damage and may prolong survival','source_verdict':'PASS_DIRECT_SOURCE_EFFECT_CONDITIONAL_SCENARIO','executions':paired,'holdout_summary':{'n':3,'winners_changed':sum(x['winner_on']!=x['winner_off'] for x in hold),'rounds_extended':sum(x['survival_round_delta']>0 for x in hold),'mean_round_extension_this_matchup_only':sum(x['survival_round_delta'] for x in hold)/len(hold),'observed_extra_damage_from_additional_turns':[x['additional_varok_damage_to_beast'] for x in hold],'no_general_win_probability_inference':True},'metrics_scope':'post RD before item; item prevention; actual life lost excluding overkill, PA activation vs item daily commitment distinct'}
(ROOT/'evidence'/'R184_RESEARCH_SUMMARY.json').write_text(json.dumps(scientific,ensure_ascii=False,indent=2)+'\n')
# DMG bridge: one receipt per physical attempt; no synthetic/duplicate observational credit.
cols=['seed','cohort','policy','run_db','tx_seq','actor','target','source_actor','source_target','hit','roll_score','critical','damage_raw_hit','rd_applied','post_rd_before_item','prevented_item','hp_effective_loss','overkill','pa_reaction_spent','item_reaction_used','target_hp_after','target_pa_after','conditional_source_scope']
with open(ROOT/'evidence'/'R185_DMG_TRANSFERRABLE_OFFENSIVE_RECEIPTS.csv','w',newline='') as fp:
 wr=csv.DictWriter(fp,fieldnames=cols);wr.writeheader();total=0
 for info in rows:
  db=ROOT/'evidence'/info['db'];con=sqlite3.connect(db)
  for seq,row in con.execute('SELECT seq,row_json FROM events ORDER BY seq'):
   r=json.loads(row)
   if r['kind']!='SOURCE_PHYSICAL_ATTACK_WITH_OPTIONAL_ARMOR':continue
   d=r['detail'];e=d['attack'];seed=info['seed'];who=d['actor'];target=d['target']
   wr.writerow({'seed':seed,'cohort':'dev' if seed==17718001 else ('validation' if seed==17718002 else 'holdout'),'policy':info['policy'],'run_db':info['db'],'tx_seq':seq,'actor':who,'target':target,'source_actor':d['source_page'],'source_target':d['target_page'],'hit':int(e['hit']),'roll_score':e['roll_score'],'critical':e['critical'],'damage_raw_hit':e['raw'],'rd_applied':e['rd_applied'],'post_rd_before_item':e['net'],'prevented_item':d['item_prevented'],'hp_effective_loss':d['final_hp_loss'],'overkill':d['final_overkill'],'pa_reaction_spent':50 if d['item_active'] else 0,'item_reaction_used':int(d['item_active']),'target_hp_after':d['HP_after'][target],'target_pa_after':d['PA_after'][target],'conditional_source_scope':'NPC_PROPOSAL_VS_PRECREATE_BEAST_CONTACT_TEST'})
   total+=1
  con.close()
assert total==sum(x['attacks'] for x in rows)
contract=json.loads((BASE/'R176_17_CONTRACT_CROSSWALK.json').read_text())
updates={
 'ACTOR_SNAPSHOT_SCENARIO':'NEW Varok ON5 encounter-proposal and Leviatã L4 precreate snapshots with source UUID/edit timestamps, no official promotion',
 'ACTION_CATALOG_AIN01':'SOURCE-gated Varok item ARMOR reaction 50PA and first trigger, rejected insufficient PA proof',
 'AUTHORITATIVE_RULES_AND_ADAPTERS':'Named beast initiative remains unproven across 6 source profiles; order dominance proof, exact item reaction literal and metric range sourced',
 'BATTLE_1X1_2X1_20X20':'NEW 1 NPC×precreate-BE matchup in 10 policy/seed runs, not ED and not 2×1/20×20, all conditional',
 'ED_VS_BE_DAMAGE':'NONE NEW: R175/R176 ED×BE preserved, new candidate is NPC×BE deliberately excluded from ED×BE contract',
 'GENERAL_SPECIFIC_RD':'Single native general RD35/75, item -70 AFTER RD, final HP and overkill independently audited; elemental stacking still HOLD',
 'ITEM_EQUIPMENT_AND_ENHANCEMENTS':'Native item-mediated once/cena armor Reaction 50PA reduces 70 damage after RD on physically documented Varok armor',
 'PA_AND_PREBUFF_COSTS':'50PA activation proven once; item PA/day already committed and NOT debited again; 50pa vs 0 source-scoped test',
 'REACTION_TRIGGER_AND_SINGLE_USE':'Armor effect correlated declaration→attack→prevention in one R18 transaction, 10 replayed banks, one use per scene despite turn-start reaction refresh',
 'RNG_REPLAY_STATISTICS':'5 seeds preregistered (1 dev,1 validation,3 reserved holdout) ×2 paired policies, 10 local independent-code replays; NOT independent species',
 'SOURCE_FREEZE_AND_RANK':'R176 exact ZIP embedded; source URLs/last-edit from Notion, not binary canonical freeze; Besta not physically promoted',
 'TACTICAL_AI_AB_FAIRNESS':'Predefined armor vs no armor policies, actor/turn keyed dice; 3 holdout seed pairs, no retrospective seed selection',
 'TURN_SCHEDULER_EVENT_SOURCING':'Initiative order invariant Varok max53 vs Leviatã min66, turn-start reaction restoration and 10 combat runs native R18',
 'OFFICIAL_QA_NAC_LEDGERS':'R18 source-scope tests, negative forged hash clones; administrative/terminal signatures absent'}
for row in contract['rows']:
 row['R177_to_R186_new_evidence']=updates.get(row['id'],'NONE_NEW')
 row['terminal_certified']=False
 row['R177_to_R186_admission']='PARTIAL_TEST_ONLY' if row['id'] in updates else 'NO_NEW_CREDIT'
contract.update({'R177_to_R186_terminals':0,'official_cells':{'before':0,'after':0,'denominator':1875},'R177_to_R186_actor_scope':'NPC_PROPOSAL_vs_BESTA_PRECREATE_CONDITIONAL','original_matrix_unchanged':True,'no_contract_redefinition':True})
assert len(contract['rows'])==17 and set(row['id'] for row in contract['rows'])==set(contract['original_id_sequence'])
(ROOT/'R185_17_CONTRACT_CROSSWALK.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_beasts':6,'candidate_pairs':len(candidates),'scoped_runs':len(rows),'attack_receipts':total,'seed_pairs_holdout':len(hold),'total_commits':sum(z['commits'] for z in rows),'total_native_events':sum(z['native_events'] for z in rows),'holdout':scientific['holdout_summary']},ensure_ascii=False,indent=2))

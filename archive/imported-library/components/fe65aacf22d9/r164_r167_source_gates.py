"""MESTRE-SIDE source-gate inventory, grounded on pages reopened in Notion 2026-10-17.
Does not assert formal source-freeze or authority to alter any canonical RPG page.
"""
from pathlib import Path
import json
H=Path(__file__).parent
link=lambda i:'https://app.notion.com/p/'+i
S={
 'Grifo Matriarca de Sílica L3':{'page':link('3f3c2b324ede813987deda0b382e83c7'),'class':'BE_FULLSPEC_PROPOSED','Vida':4315,'Alma':4016,'CA':153,'RD_general':75,'DES':116,'generic_prof':22,'speed_m':63,'initiative_proficiency_specific':'UNKNOWN','attack':'Talão 6d6+138, 20d10 físico','Descarga':'55 PA, 14d10 Lightning, Reflexo CD94 meia-dano, linha curta','Descarga_numeric_range':'UNKNOWN','RD_Lightning_Auren_target':'UNKNOWN','gate':'SOURCE_CONDITIONAL_ONLY'},
 'Crocodilo de Lodo Astral Ancião L3':{'page':link('3f3c2b324ede813987deda0b382e83c7'),'precreate':link('3f2c2b324ede81878ef3ecad4977794e'),'class':'BE_FULLSPEC_PRECREATE','Vida':5580,'Alma':3625,'CA':112,'RD_general':75,'DES':64,'generic_prof':22,'speed_m':50,'initiative_proficiency_specific':'UNKNOWN','basic_attack':'Mordida 6d6+134, 20d10 físico perfurante/impacto','mixed_effects':'SOURCE_HOLD_FULL_RESOLUTION','gate':'LAB_PHYSICAL_BASIC_WITH_EXOGENOUS_OPEN_ONLY'},
 'Sikong Auren L3':{'page':link('3ebc2b324ede814bb730d47dd7bd5f02'),'class':'ED_SOURCE_DOCUMENTED','Vida':523,'PA_free':719,'CA':225,'RD_physical':35,'RD_Dark':60,'RD_Lightning':'UNKNOWN','initiative':'6d6+166 (specific +2 documented)','speed_ground_m':16,'basic_attack':'6d6+193, 8d8+211','transform_cost_disagreement':'100+15/turn vs current Lendário 320 PA','gate':'SOURCE_CONDITIONAL_NORMAL_FORM_ONLY'},
 'Sikong Feryn ON5':{'page':link('3f6c2b324ede81ce9c61db8127bf0e31'),'class':'MESTRE_SIDE_NPC_NO_SPIRIT','Vida':479,'PA_free':424,'CA':123,'RD_physical':22,'initiative':'4d6+82','basic_attack':'4d6+92 8d8+47','RD_Wind':'UNKNOWN','RD_Plant':'UNKNOWN','absolute_speed':'UNKNOWN','gate':'LAB_NPC_ONLY'},
 'Sikong Eristan ON5':{'page':link('3f6c2b324ede819cae98ec0f6a63de76'),'class':'MESTRE_SIDE_NPC_NO_SPIRIT','Vida':630,'PA_free':804,'CA':76,'RD_physical':25,'initiative':'4d6+30','heal':'75 PA, 8d10+25 plus glove +20 once','Casulo':'60 PA +22 CA -4m two turns literal','Casulo_expiry':'SOURCE_HOLD_EXACT_BOUNDARY','RD_Wind':'UNKNOWN','RD_Plant':'UNKNOWN','absolute_speed':'UNKNOWN','gate':'LAB_NPC_ONLY'},
 'Sikong Iskiel ON5':{'page':link('3f6c2b324ede81a78a59d3d81fd5e966'),'class':'MESTRE_SIDE_NPC_NO_SPIRIT','Vida':514,'PA_free':484,'CA':132,'RD_physical':25,'initiative':'4d6+89','Flecha_de_Trava':'55 PA, 8d10+12 perfurante +21 FF, Luta DES vs CA, range 65m; -6m through END OF NEXT TURN','gate':'LAB_SOURCE_SCOPED_EXPLICIT_TEMPORAL'},
 'Sikong Varok ON5':{'page':link('3f6c2b324ede81f49ea9efbe1a811091'),'class':'MESTRE_SIDE_NPC_NO_SPIRIT','Vida':734,'PA_free':324,'CA':83,'RD_physical':35,'DES':29,'initiative':'4d6+29','basic_attack':'4d6+100 10d10+48 físico impacto/corte','absolute_speed':'UNKNOWN','gate':'LAB_SOURCE_AOO_ONLY'},
 'Sistema de Combate vigente':{'page':link('3ebc2b324ede81f1be4be8804ac113c0'),'R3_AOO':'Saída voluntária de adjacência, Vantagem, Reação consumida','R6_failure':'1->1->1 /1->1->2 trigger only','R18':'Ledger experimental separate source','time_exact_two_turn':'NOT_EXPLICIT_FOR_CASULO'},
 'OP VLAB R42/R43':{'page':link('3f3c2b324ede819496ddd7f93bd7e5d2'),'R42':'LAB-ONLY negative critical miss zero damage, consume action/cost, no extra mishap','R43':'AoO concurrent descending DES then die when tied; dice per competent rank'},
}
remaining={
 'Beast_specific_initiative':{'status':'SOURCE_HOLD','proof':'General +22 proficiency in BEAST-FULLSPEC is not explicit Initiative skill','minimum':'Specific natural initiative proficiency rule or decision'},
 'Descarga_Curta_reach':{'status':'SOURCE_HOLD','proof':'Only "linha curta" text, no length in meters','minimum':'Numeric authoritative range/path for Grifo Descarga'},
 'Auren_RD_Lightning':{'status':'SOURCE_HOLD','proof':'Auren lists physical RD35 and Dark60, no Lightning entry','minimum':'Verified precise resistance/absence convention or resolution without assumption'},
 'Feryn_Eristan_RD_Wind_Plant':{'status':'SOURCE_HOLD','proof':'Equipped physical RD exists; Wind/Plant specific RD not explicit','minimum':'Authoritative elemental resistance fields / missing resistance handling'},
 'Casulo_two_turn_expiry':{'status':'TEMPORAL_HOLD','proof':'"Duração: 2 turnos" without exact expiration marker','minimum':'Competent source-specific time boundary / NAC-NORM-01'},
 'Casulo_abs_speed_on_Eristan':{'status':'SOURCE_HOLD','proof':'No numeric baseline movement in Eristan page inspected','minimum':'Current movement baseline if testing Casulo on Eristan'},
 'Mixed_damage':{'status':'SOURCE_HOLD','proof':'Impacto/Água and cortante/Vento are type descriptions; proportions not explicitly separated','minimum':'Source-separated components and correct stacking/mitigation selection'},
 'Transformation_Auren':{'status':'NAC_NORM_CONFLICT_HOLD','proof':'Auren sheet says 100PA +15/turn, Combat/Transformation systems L3 says 320PA activation','minimum':'Competent NAC-NORM reconciliation; leave original sheet intact'},
 'Second_ED_team':{'status':'SOURCE_HOLD','proof':'Auren valid; other candidates inspected missing identity of Spirit, full mechanics, or assembly','minimum':'One second unique ED fully documented without creating new canon'},
}
R={'as_of':'2026-10-17','operation':'OP-VLAB-FUSION-SANDBOX-01','source_capture':'Reopened read-only Notion source excerpts via connector 2026-10-17, not full binary verified freeze','page_facts':S,'individually_localized_gates':remaining,'normalization_warning':'Unknown RD is not zero; generic Beast prof is not Initiative bonus. No official benchmark admission.'}
(H/'R164_MECHANICAL_SOURCE_AND_RESISTANCE_GATES.json').write_text(json.dumps(R,ensure_ascii=False,indent=2)+'\n')
can=[
 {'name':'Sikong Auren L3','id':'3ebc2b324ede814bb730d47dd7bd5f02','class':'ED_EXPLICIT','source':'VERIFIED_MASTER_SIDE_PROFILE','necessary':'Normal combat sheet complete for scoped technical fight','missing':'Transform cost authority, elemental RD, full endgame admission','eligible_second_ED':False},
 {'name':'Sikong Hongyue O5','id':'e9ac2b324ede82229e5201e5275d9d5e','class':'ED_LABEL_ONLY','source':'HISTORICAL_PARTIAL_SHEET','necessary':'HP448, PA300, CA53','missing':'Spirit identity blank; abilities,costs, initiative, equipment state','eligible_second_ED':False},
 {'name':'Pan Tueimor ON4','id':'8f6c2b324ede82c88e5d8184dc3a3b90','class':'ED_NOT_CONFIRMED','source':'HISTORICAL_PARTIAL_SHEET','necessary':'HP416, PA321, CA63','missing':'Spirit identity blank; initiative and real offensive repertoire uncertain','eligible_second_ED':False},
 {'name':'Sikong Yip Rei','id':'2b0c2b324ede826cbc79011030f2f86e','class':'ED_LORE_REFERENCE','source':'LORE_ONLY','necessary':'Illness lore, Lendário label','missing':'No confirmed operational stats, spirit, timing, abilities, initiative or combat health','eligible_second_ED':False},
 {'name':'Sel-Myr Ivara','id':'3f2c2b324ede810689adf0467e59fdc0','class':'CHARACTER_FUTURE_PRECREATE','source':'LORE-COMPLETE/MECH-PENDING (literal)','necessary':'ON5 identity and narrative','missing':'Actual mechanical ED sheet, spirit identity, attacks/PA/CA/HP, equipment and transformation','eligible_second_ED':False},
 {'name':'Kael Soryn','id':'3f2c2b324ede8191a268f89d0cbdc203','class':'CHARACTER_FUTURE_PRECREATE','source':'LORE-COMPLETE/MECH-PENDING (literal)','necessary':'L3 identity and narrative','missing':'Actual mechanical ED sheet, spirit identity, attacks/PA/CA/HP, equipment and transformation','eligible_second_ED':False},
 {'name':'Nym Rhae','id':'3f2c2b324ede81aeb2fefa7c9866afcb','class':'CHARACTER_FUTURE_PRECREATE','source':'LORE-COMPLETE/MECH-PENDING-RACE (literal)','necessary':'L2 identity and narrative','missing':'Race mechanics, ED spirit, snapshot, combat loadout, transformation','eligible_second_ED':False},
]
P={'as_of':'2026-10-17','operation':'OP-VLAB-FUSION-SANDBOX-01','candidate_count':len(can),'ED_current_source_scoped_eligible':1,'additional_ED_mechanically_eligible':0,'battery_C_25_official':0,'results':can,'decision':'SECOND_ED_SOURCE_HOLD; Feryn/Eristan/Iskiel/Varok ON5 are explicitly without Spirit and not substitutes'}
(H/'R167_SECOND_ED_ELIGIBILITY.json').write_text(json.dumps(P,ensure_ascii=False,indent=2)+'\n')
md=['# R167 — segundo ED: elegibilidade físico-documental','',f"AS-OF {P['as_of']} · MESTRE-SIDE · 7 candidatos distintos examinados",'','| Candidato | Estado | Menor pendência |','|---|---|---|']
for c in can:md.append(f"| [{c['name']}]({link(c['id'])}) | {c['source']} | {c['missing']} |")
md+=['','**Conclusão:** nenhum segundo ED completo e independente encontrado neste lote de fontes. Auren permanece a única entrada ED fonte-condicionada. Não criar NPC/atributos, não contar fichas ON5 sem Espírito como ED.','', 'As lacunas são localizadas; não constituem busca global exaustiva de todo o Notion.']
(H/'R167_SECOND_ED_ELIGIBILITY.md').write_text('\n'.join(md)+'\n')
print('CREATED source matrices',len(S),len(remaining),len(can))

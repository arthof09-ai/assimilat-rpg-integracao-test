#!/usr/bin/env python3
"""Read-only audit of the F0-F6 local scientific dataset and prior R31 archive.
File validation is NOT scientific or canonical certification.
"""
import pathlib,csv,json,hashlib,zipfile,sys,collections,math,statistics
p=pathlib.Path(__file__).resolve().parent
R=lambda n:list(csv.DictReader(open(p/n,encoding='utf-8')))
J=lambda n:json.loads((p/n).read_text(encoding='utf-8'))
checks=[]
def c(name,ok):
    checks.append((name,bool(ok)))
    if not ok:raise AssertionError(name)
src=R('01_FONTES_FISICAS.csv'); eff=R('02_DEFINICOES_EFEITOS.csv'); occ=R('03_OCORRENCIAS_DEDUP.csv'); parts=R('12_COMPONENTES_MATEMATICOS.csv'); alt=R('04_ALTERNATIVAS_EM_CONFLITO.csv'); stats=R('05_ESTATS_DOCUMENTAIS_ESTRATIFICADAS.csv'); phase=R('08_PROGRESSO_F0_F18.csv'); rank=R('14_COBERTURA_POSICOES_RN_25_ED_BE.csv'); res=J('00_RESUMO_DENOMINADORES.json'); d0=J('13_D0_D9_LOTE_SEM_GLOBAL.json')
c('45 physical pages local',len(src)==45)
c('45 unique source IDs',len({r['page_id'] for r in src})==45)
c('URLs match ids',all(r['url'].endswith(r['page_id']) for r in src))
c('excerpt fingerprints NOT full-native digest',all(hashlib.sha256(r['source_excerpt'].encode()).hexdigest()==r['excerpt_sha256'] and not r['full_native_page_sha256'] for r in src))
c('58 mechanical records',len(eff)==58)
c('58 unique mechanical IDs',len({e['definition_id'] for e in eff})==58)
c('38 distinct damage effect groups',len({e['damage_effect_group_id'] for e in eff if e['role'] in ('damage','damage_dot','reflect')})==38)
c('64 occurrences',len(occ)==64)
c('6 not independent',sum(o['count_as_independent_definition']=='False' for o in occ)==6)
c('5 mirrors one form',sum(o['version_variant']!='SECOND_FORM_SAME_SOURCE_NOT_INDEPENDENT_NEW_OBJECT' and o['count_as_independent_definition']=='False' for o in occ)==5)
c('no missing sources for effects',all(e['source_key'] in {x['source_key'] for x in src} for e in eff))
c('68 numeric parts',len(parts)==68)
c('68 numeric parts nonindependent',all(x['independent_observation']=='False' for x in parts))
c('38 mean-calculable source records',sum(bool(x['intrinsic_dme']) for x in eff)==38)
c('4 conflict alternatives not source-vetted chosen',len(alt)==4 and all(x['status']=='CONFLICT_ALTERNATIVE_NOT_SELECTED' for x in alt))
c('conflicting primary effects have no authoritative damage value',all(next(x for x in eff if x['definition_id']==e)['intrinsic_dme']=='' for e in ('FRIO_V3_MAIN','COLUNA_V2_DOT')))
c('no native auto combats',all(e['eligible_native_auto_combat']=='False' for e in eff))
c('no scientific certified B05/B06',res['DMG_B_certified']=='1/18' and res['first_full_fight_canonical_eligible']==0)
c('global D0-9 not invented',res['source_pages_global_denominator'] is None and d0['D0_D9_GLOBAL']=='UNDETERMINED')
c('phase F0-F18 19 rows',len(phase)==19 and [x['phase'] for x in phase]==['F'+str(i) for i in range(19)])
c('F0 not promoted',res['F0_prior_verified_documentary_milestones']=='4/8')
c('50 positional cells (ED+BE) no filled fights',len(rank)==50 and all(x['full_scene_eligible']=='0' for x in rank))
c('18 statistical strata, each n=1',len(stats)==18 and all(x['n_effects']=='1' for x in stats))
c('reserved holdout group not a claim of blinded independent test',any(x['split_precalibration']=='HOLDOUT_RESERVED_NO_TUNING' for x in src) and all('BLIND' not in x['split_precalibration'] for x in src))
c('basic Galidemus and Cabra conditional arithmetic',next(x for x in eff if x['definition_id']=='GAL_PATADA')['conditional_dme_with_printed_attribute']=='15.5' and next(x for x in eff if x['definition_id']=='CABRA_INVESTIDA')['conditional_dme_with_printed_attribute']=='16.5')
c('Behemoth mean inversion math',next(x for x in eff if x['definition_id']=='BEHEMOTH_MORDIDA')['intrinsic_dme']=='10.5' and next(x for x in eff if x['definition_id']=='BEHEMOTH_ESTILHACO')['conditional_dme_with_printed_attribute']=='59.0')
c('Sword strong outlier correctly separated',next(x for x in eff if x['definition_id']=='ESPADA_LEND')['intrinsic_dme']=='768.0' and next(x for x in eff if x['definition_id']=='ESPADA_LEND')['split_precalibration']=='HOLDOUT_RESERVED_NO_TUNING')
c('VLAB preflight DENY and no native source hash',J('VLAB_PREFLIGHT_GALIDEMUS_B1_NO_DISPATCH.json')['action_dispatch']=='DENY' and J('VLAB_PREFLIGHT_GALIDEMUS_B1_NO_DISPATCH.json')['source_digest'] is None)
c('exact conditional PMF evidence',all(abs(sum(a['gross_outcome'] for a in x['pmf'])/len(x['pmf'])-x['mean'])<1e-9 for x in J('15_PMF_EXATAS_EXEMPLOS.json')))
prior=p/'HISTORICO_R31_INTACTO.zip'
c('R31 expected sha preserved',hashlib.sha256(prior.read_bytes()).hexdigest()=='c0153e57bb3c0755c147c4ba44550045f3d244984d5d7777153ad6fac0a23c4b')
with zipfile.ZipFile(prior) as z:
 c('R31 CRC valid',z.testzip() is None)
 man=z.read('MANIFESTO_SHA256_R31.txt').decode().splitlines()
 c('R31 manifest 150 entries preserved',len(man)==150)
 c('R31 manifest SHA 150/150 preserved',all(hashlib.sha256(z.read(line.split('  ',1)[1])).hexdigest()==line.split('  ',1)[0] for line in man))
manifest=p/'MANIFESTO_PACOTE_SHA256.txt'
if manifest.exists():
 rows=[line.strip().split('  ',1) for line in manifest.read_text().splitlines() if line.strip()]
 c('current lot manifest valid',all(hashlib.sha256((p/name).read_bytes()).hexdigest()==digest for digest,name in rows))
print('VERIFICACOES_LOCAIS',sum(ok for _,ok in checks),'/',len(checks),'PASS')
for name,ok in checks:print('PASS' if ok else 'FAIL',name)

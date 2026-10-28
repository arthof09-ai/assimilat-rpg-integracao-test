#!/usr/bin/env python3
"""Recheck science-only R07 handoff ZIP, not a Notion engine or official combat.

Usage: python DMG-F1-R07-REPLAY-VERIFICADOR-v01.py /path/to/DMG-F1-R07-HANDOFF-ENGENHARIA-v01.zip
Only standard Python modules. Does not import/execute engineering code.
"""
import hashlib,itertools,json,sys,zipfile

def main(path):
    tests=[]
    def check(name,ok):
        tests.append((name,bool(ok)))
        if not ok: raise AssertionError(name)
    with zipfile.ZipFile(path,'r') as z:
        check('ZIP CRC',z.testzip() is None)
        manifest=json.loads(z.read('MANIFEST/R07_FILE_HASHES.json'))
        check('manifest states not Notion uploaded',manifest['notion_uploaded'] is False)
        check('manifest denies canonical execution',manifest['full_fight'] is False and manifest['lab_accepted'] is False)
        for f in manifest['included_files']:
            sub='read_only/' if f['original_R03_R06_untouched'] else 'R07/'
            data=z.read(sub+f['path'])
            check('SHA256 '+f['path'],hashlib.sha256(data).hexdigest()==f['sha256'])
        check('member denominator',len(z.namelist())==len(manifest['included_files'])+1)
        gate=json.loads(z.read('R07/DMG-F1-R07-MATRIZ-B01-B18-v01.json'))
        check('original B01-B18 retained', [r['original_id'] for r in gate['records']]==[f'B{i:02}' for i in range(1,19)])
        check('0 of 18 certified',gate['fully_certified']==0 and all(not r['full_criterion_certified'] for r in gate['records']))
        check('status sum',sum(gate['statuses'].values())==18)
        science=json.loads(z.read('R07/DMG-F1-R07-PREFLIGHT-STRICT-PATADA-v01.json'))
        check('strict denial not treated as engine execution',science['CURRENT_STRICT_PRECHECK']['decision']=='DENY' and science['acceptance_levels']['FULL_FIGHT']=='BLOCKED_0_OF_2')
        check('R07 source snapshot counts',len(science['sources_SHA256_R07'])==8)
        check('Stage10 exact guarded',science['STAGE10_ACTUAL_RUNTIME_INTERLOCKS']['strict_compile']=='STRICT_AUDITED_SOURCES_AND_NAC_PASS_NOT_AVAILABLE')
        check('Stage10 real-engineer not ACKed',science['routing']['lab_ACK'] is None)
        branches=science['expected_oracles']
        for name,f in [('A_literal',54),('B_hypothetical',56)]:
            b=branches[name]
            check(name+' uses independent FOR',b['FOR']==f)
            check(name+' attack versus CA',b['defense_CA46']['attack_total']==3+4+f)
            check(name+' gross if hit',b['defense_CA46']['gross_if_hit']==5+3+f)
            check(name+' 36/36 conditional CA/dodge',all((x+y+f>46 and x+y+f>49) for x,y in itertools.product(range(1,7),repeat=2)))
            check(name+' damage conditional RDF',b['if_RDF10_safely_adjudicated']['net_if_hit']==5+3+f-10)
            check(name+' no applied damage cert',b['unconditional_damage_applied'] is None)
        actual=json.loads(z.read('R07/DMG-F1-R07B-CROSSWALK-STAGE10-v01.json'))
        check('Crosswalk sources Stage10', 'STAGE10' in json.dumps(actual).upper())
        check('24 static checks reported, separate class', len(actual.get('static_checks',[]))==24)
        suite=json.loads(z.read('R07/DMG-F1-R07-SUITE-DE-TESTES-v01.json'))
        check('73 new science-only checks',suite['new_scientific_tests']==73 and suite['passed']==73 and suite['failed']==0)
        check('earlier tests not recredited',suite['prior_R04_R05_tests_reexecuted'] is False)
    print('REPLAY_R07_PACKAGE_VERIFY='+str(sum(v for _,v in tests))+'/'+str(len(tests))+' PASS')
    print('GATES_INTEGRALLY_CERTIFIED=0/18')
    print('LAB_ACTION_RUNTIME=LUI_MACACO_NOT_RUN; STRICT=REJECT; FULL_FIGHT=0/2')
    print('THIS_IS_STANDALONE_SCIENCE_VALIDATOR_NOT_THE_LAB_ENGINE')

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/DMG-F1-R07-HANDOFF-ENGENHARIA-v01.zip')

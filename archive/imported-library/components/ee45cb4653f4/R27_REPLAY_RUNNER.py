import pathlib,json,hashlib,sys,concurrent.futures
BASE=pathlib.Path(__file__).parent
sys.path.insert(0,str(BASE/'work'/'fusion_stage12'))
import vlab_r27_scientific_baseline as v
SRC=BASE/'scientific_runs'
CASES=[(83,None,None),(11,'OFENSIVO','DEFENSIVO'),(23,'EQUILIBRADO','EQUILIBRADO'),(41,'OFENSIVO','EQUILIBRADO')]
def run(case):
 seed,a,b=case
 target=BASE/'independent_replays'/str(seed if a is None else a+'__'+b+'__'+str(seed))
 target.mkdir(parents=True,exist_ok=True)
 fresh=v.run(target,seed,a,b)
 key=('ORIGINAL_R26' if a is None else a+'__'+b)+'__SEED_'+str(seed)
 old=json.loads((SRC/'receipts'/f'{key}.json').read_text())
 matches={k:fresh[k]==old[k] for k in ('status','revision','head','winner','last_state_hp','a1_chain','config_sha','sqlite_sha256','events')}
 return {'key':key,'same_mechanics_and_exact_sqlite':all(matches.values()),'matches':matches,
   'new_run':str(target),'sqlite_sha256':fresh['sqlite_sha256']}
if __name__=='__main__':
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:result=list(ex.map(run,CASES))
 out=BASE/'scientific_report'/'R27_INDEPENDENT_REPLAYS.json'
 out.write_text(json.dumps({'schema':'R27_INDEPENDENT_REPLAY','cases':result,'passed':sum(x['same_mechanics_and_exact_sqlite'] for x in result),'total':len(result)},indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(result,ensure_ascii=False,indent=2))

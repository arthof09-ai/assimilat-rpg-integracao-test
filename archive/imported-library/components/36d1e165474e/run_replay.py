from pathlib import Path
import hashlib,subprocess,sys,zipfile,json,tempfile
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'baselines/CRAFT_H2P2_EVOLUCAO_TEST_20261020.zip'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='a0a2ed07a504edc67014d80bb63d6787afb9a0b4c2d53ca52371f7909a20d030'
with zipfile.ZipFile(base) as z:
 assert z.testzip() is None
 with tempfile.TemporaryDirectory(prefix='craft_old_h2p2_') as td:
  z.extractall(td)
  code=Path(td)/'CRAFT_H2P2_EVOLUCAO_TEST_20261020/code/run_replay.py'
  r=subprocess.run([sys.executable,str(code)],capture_output=True,text=True,timeout=80)
  assert r.returncode==0,(r.stdout[-1000:],r.stderr[-1000:])
  print('PREVIOUS_H2P2_BASELINE_REPLAY_OK',r.stdout[-250:].replace('\n',' '))
new=subprocess.run([sys.executable,str(ROOT/'code/lot_and_ticket.py')],capture_output=True,text=True)
assert new.returncode==0,(new.stdout,new.stderr)
print('NEW_ACTUAL_EVIDENCE_GATE',new.stdout.strip())
tests=subprocess.run([sys.executable,str(ROOT/'tests/test_actual_new_delta.py')],capture_output=True,text=True)
assert tests.returncode==0,(tests.stdout,tests.stderr)
print('NEW_TARGETED_TESTS', next((s for s in tests.stderr.splitlines() if s.startswith('Ran ')),'UNKNOWN'), tests.stderr.strip().splitlines()[-1])
result=json.loads((ROOT/'outputs/H2_3_ACTUAL_READONLY_PRECHECK.json').read_text())
assert result['p2']['stage_A']=='HOLD_NO_APPLICATION'
assert result['p2']['controlled_actor_actions']==0
assert result['p2']['consumed_units']==0
assert result['p2']['new_R48_orders']==0
assert result['p2']['in_game_magic_observations']==0
assert result['oil_stock_search']['usable_lots']==0
assert result['baseline']['historical_r48_seq']==1
assert result['party_or_primeiro_writes']==0
print('COLD_REPLAY_PASS_REAL_DOCUMENTARY_NEGATIVE_NO_STOCK_NO_MAGIC_NO_WRITES')

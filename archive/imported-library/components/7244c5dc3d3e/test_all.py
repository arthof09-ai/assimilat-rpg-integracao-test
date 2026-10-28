from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'runtime'))
sys.path.insert(0,str(ROOT/'history'))
import r127_receipt_protocol as r127
import r131_spirit_reserves_t6b as r131old
import r132_structural_selector as r132old
import r133_source_bound_previews as r133old
import r134_conversation_authorization as r134old
import r137_observation_ledger as r137
import r138_native_refusal_triage as r138
import r141_source_binding as r141
import r142_143_activation_engine as r142
import r144_structural_multiregion as r144
import r145_chat_preview as r145
import r146_contract_audit as r146
results={
 'historical_R127':r127.selftest(),
 'historical_R131':r131old.checks(),
 'historical_R132':r132old.checks(),
 'historical_R133':len(r133old.checks()),
 'historical_R134':r134old.tests(),
 'new_R137':r137.main()['assertions'],
 'new_R138':len(r138.main()),
 'new_R141':r141.main()['checks'],
 'new_R142_143':len(r142.scenario()),
 'new_R144':r144.test(),
 'new_R145':r145.selftest()['checks'],
 'new_R146':r146.run()['checks'],
}
assert all(isinstance(v,int) and v>0 for v in results.values())
assert len(results)==12
print(json.dumps({'status':'PASS','commands':12,'checks_or_cases':results,'production':'HOLD','native_tool_calls_executed_by_this_script':0},ensure_ascii=False,indent=2))

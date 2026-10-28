"""Run ONLY authentic R39->R34->R27->R26. No calculation in this file."""
from pathlib import Path
import json,sys,hashlib
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root))
from AUDITOR_COMPARADORES_R39 import envelope_craft_qualificado
inp=json.loads((root/'PINGENTE_R39_INPUT.json').read_text('utf8'))
res=envelope_craft_qualificado(inp['descricao_original'],inp['interpretacao'])
p=root/'recomputed_r39_envelope.json'
p.write_text(json.dumps(res,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'output':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                  'status':res['gate_r39'],'custo_pa_qualificado':res['custo_pa_qualificado']},ensure_ascii=False))

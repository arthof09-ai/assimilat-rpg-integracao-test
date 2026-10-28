#!/usr/bin/env python3
from pathlib import Path
import json,sys
import jsonschema
from qmc02_pa_adapter import qmc_sidecar_receive
P=Path(__file__).resolve().parent
schema=json.loads((P/'QMC_PA_INTERCHANGE_R04.schema.json').read_text('utf8'))
asserted=[]
for f in sorted((P/'SAIDAS_INTEGRACAO').glob('*_REQUEST_RESPONSE.json')):
 dat=json.loads(f.read_text('utf8'))
 jsonschema.Draft202012Validator.check_schema(schema)
 jsonschema.validate(dat,schema)
 receipt=qmc_sidecar_receive(dat)
 assert receipt['production_hold'] and receipt['no_recipe_created']
 asserted.append({'input':f.name,'state':receipt['receipt_state'],'hash':receipt['received_digest_sha256'],'status':'VALIDADO_EM_TEST'})
print(json.dumps({'schema':'QMC_PA_INTERCHANGE_R04.schema.json','validations':asserted,'n':len(asserted),'production':'HOLD'},indent=2,ensure_ascii=False))

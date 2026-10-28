import zipfile,sqlite3,tempfile,json,os,collections,re
from pathlib import Path
src=Path('/mnt/data/inovador_pesq_pos15/vlab_readonly/VLAB_R205_DEFESA_DE_VENTO_ANEL_CLASSIFICADO_MESTRE_ONLY.zip');out=Path('/mnt/data/inovador_pesq_pos15/evidence')
paths=collections.Counter();values=collections.defaultdict(collections.Counter);examples=[];validseq=[];events_total=0;pos=[]
def walk(v,path='',depth=0):
 if depth>7:return
 if isinstance(v,dict):
  for k,item in v.items():
   p=f'{path}.{k}' if path else k
   paths[p]+=1
   if re.search(r'(coord|position|map|grid|wall|obstacle|location|\.x$|\.y$|origin|destination|target|actor|type|kind|turn|phase|seq|step|before|after)',p,re.I):
    if not isinstance(item,(list,dict)):values[p][str(item)[:60]]+=1
   walk(item,p,depth+1)
 elif isinstance(v,list):
  if len(v) and depth<7:walk(v[0],path+'[]',depth+1)
with zipfile.ZipFile(src) as z:
 for name in sorted(n for n in z.namelist() if n.endswith('.sqlite') and '/r205/' in n):
  with tempfile.NamedTemporaryFile(delete=False,suffix='.db') as f:f.write(z.read(name));p=f.name
  try:
   con=sqlite3.connect(f'file:{p}?mode=ro&immutable=1',uri=True)
   d=con.execute('select seq,cmd_id,prev,row_json,row_sha,before_sha,after_sha from events order by seq').fetchall()
   validseq.append({'database':name.split('/')[-1],'rows':len(d),'seq_contiguous': [int(x[0]) for x in d]==list(range(1,len(d)+1)),'cmd_unique':len({x[1] for x in d})==len(d),'prev_link':all(d[i][2]==d[i-1][4] for i in range(1,len(d)))})
   events_total+=len(d)
   for seq,cmd,prev,row,hashr,sha1,sha2 in d:
    payload=json.loads(row);walk(payload)
    if len(examples)<4 and ('BEAST-' in cmd or 'MAGIC_ON-' in cmd):examples.append({'source_db':name.split('/')[-1],'seq':seq,'event_id':cmd,'payload_keys':list(payload),'detail_keys':list(payload.get('detail',{})) if isinstance(payload.get('detail'),dict) else None,'sample':{k:payload.get(k) for k in ('kind','type','round','turn')}})
   con.close()
  finally:os.unlink(p)
report={'events_total':events_total,'all_databases_sequence_contiguous':all(x['seq_contiguous'] for x in validseq),'all_unique_cmd_per_db':all(x['cmd_unique'] for x in validseq),'all_prev_link_to_prior_row_hash':all(x['prev_link'] for x in validseq),'paths':dict(paths.most_common()),'selected_value_counts':{k:dict(v.most_common(7)) for k,v in values.items() if len(v)<80},'examples':examples,'per_database_integrity':validseq}
(out/'VLAB_R205_ROWJSON_FIELD_CENSUS.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('events',events_total,'seq,ids,prev',report['all_databases_sequence_contiguous'],report['all_unique_cmd_per_db'],report['all_prev_link_to_prior_row_hash']);print('paths',list(paths.most_common(95)));print('details',examples[:2]);

"""Read-only physical inspection of signed Library ZIP R205; NEVER execute runners."""
import hashlib,json,zipfile,sqlite3,tempfile,os,collections,re
from pathlib import Path
path=Path('/mnt/data/inovador_pesq_pos15/vlab_readonly/VLAB_R205_DEFESA_DE_VENTO_ANEL_CLASSIFICADO_MESTRE_ONLY.zip');out=Path('/mnt/data/inovador_pesq_pos15/evidence');out.mkdir(exist_ok=True)
sha=hashlib.sha256(path.read_bytes()).hexdigest();EXPECTED='62a9851b3a5ae7919b9225d9379a3d32c8736448e76bfcea4729dcbfe933cead';assert sha==EXPECTED
rows=[];all_tables=collections.defaultdict(set);fieldnames=collections.defaultdict(set);evsamples=[];json_desc=[]
with zipfile.ZipFile(path) as z:
 assert z.testzip() is None
 dbs=[x for x in z.namelist() if x.lower().endswith('.sqlite') and '/r205/' in x.lower()]
 for fn in dbs:
  raw=z.read(fn)
  with tempfile.NamedTemporaryFile(suffix='.sqlite',delete=False) as t:t.write(raw);tmp=t.name
  try:
   conn=sqlite3.connect(f'file:{tmp}?mode=ro&immutable=1',uri=True)
   names=[x[0] for x in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
   counts={};columns={}
   for name in names:
    safe='"'+name.replace('"','""')+'"'
    counts[name]=conn.execute(f'SELECT count(*) FROM {safe}').fetchone()[0]
    col=[{'name':r[1],'type':r[2]} for r in conn.execute(f'PRAGMA table_info({safe})')]
    columns[name]=col
    all_tables[name].add(str(tuple((c['name'],c['type']) for c in col)))
    for c in col:fieldnames[name].add(c['name'])
   rows.append({'file':fn,'sha256':hashlib.sha256(raw).hexdigest(),'size':len(raw),'tables':names,'counts':counts,'columns':columns})
   if not evsamples:
    for tbl in names:
     if re.search('event|journal|trace|commit',tbl,re.I):
      safe='"'+tbl.replace('"','""')+'"'
      cursor=conn.execute(f'SELECT * FROM {safe} LIMIT 2');heads=[x[0] for x in cursor.description]
      for row in cursor.fetchall():
       data={k:(str(v)[:240] if v is not None else None) for k,v in zip(heads,row)}
       evsamples.append({'table':tbl,'fields':heads,'example':data})
   conn.close()
  finally:os.unlink(tmp)
 for name in z.namelist():
  if name.startswith('new/r205/evidence/') and name.endswith('.json') and '/db/' not in name:
   try:
    d=json.loads(z.read(name));json_desc.append({'name':name,'top_level_keys':list(d)[:30] if isinstance(d,dict) else None,'top_level_type':type(d).__name__})
   except Exception as e:json_desc.append({'name':name,'error':str(e)})
report={'zip':path.name,'size':path.stat().st_size,'sha256_verified':sha,'zip_crc_pass':True,'total_sqlite':len(dbs),'schema_groups':{k:len(v) for k,v in all_tables.items()},'columns_by_table':{k:sorted(v) for k,v in fieldnames.items()},'db_files':rows,'event_samples':evsamples,'json_files':json_desc,'limitations':['Physical binary authenticated; individual gameplay mechanics and event claims not recomputed','Event times, IDs and positions require field-level interpretation','No R205 runner executed and no Notion write performed']}
(out/'MAPA_FISICO_VLAB_R205_READONLY.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('COUNT',len(dbs),'TYPES',report['schema_groups']);print('TABLE COLUMNS',report['columns_by_table']);print('FIRST COUNTS',rows[0]['counts']);print('TOTAL TABLE COUNTS',dict((k,sum(x['counts'].get(k,0) for x in rows)) for k in all_tables));print('SAMPLE',evsamples[:3]);print('JSON',json_desc)

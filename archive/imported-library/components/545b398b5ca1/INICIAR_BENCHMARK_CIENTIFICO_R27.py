#!/usr/bin/env python3
"""Comestre: offline CLI inspection & one seed independent replay; user needs no installation."""
from __future__ import annotations
import argparse,json,pathlib,sys,tempfile
BASE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'fusion_stage12'))
import vlab_r27_scientific_baseline as r27

def main():
 p=argparse.ArgumentParser(description='VLAB R27 science read-only report and reproducible replay')
 p.add_argument('operation',choices=('summary','replay','new-experiment'))
 p.add_argument('--left',choices=tuple(r27.PROFILES))
 p.add_argument('--right',choices=tuple(r27.PROFILES))
 p.add_argument('--seed',type=int,default=11)
 p.add_argument('--directory',type=pathlib.Path)
 p.add_argument('--lab-policy-ack',action='store_true',help='acknowledge noncanonical conditional experiment')
 args=p.parse_args()
 file=BASE/'reconstruction'/'r27_delivery'/'R27_SCIENTIFIC_RESULTS_MASTER_ONLY.json'
 if args.operation=='summary':
  x=json.loads(file.read_text());print(json.dumps({'schema':x['schema'],'total':x['total'],
    'original_8_seed_comparison':x['original_8_seed_comparison']['r27_completed'],
    'full_canonical_fights':0},indent=2,ensure_ascii=False));return
 if not args.left or not args.right: p.error('--left and --right required')
 if args.operation=='new-experiment' and not args.lab_policy_ack:
  p.error('new experiment requires --lab-policy-ack: noncanonical and not authorized for production')
 if args.operation=='replay' and args.seed not in r27.SEEDS:p.error('replay must use a frozen original seed')
 def inner(root):
  result=r27.run(root,args.seed,args.left,args.right)
  if args.operation=='new-experiment':
   print(json.dumps({'status':result['status'],'seed':result['seed'],'id':result['id'],
   'sqlite_sha256':result['sqlite_sha256'],'canon':0},indent=2,ensure_ascii=False));return
  key=f'{args.left}__{args.right}__SEED_{args.seed}.json'
  reference=json.loads((BASE/'reconstruction'/'r27_delivery'/'runs'/'receipts'/key).read_text())
  fields=('head','revision','a1_chain','events','winner','last_state_hp','sqlite_sha256')
  matches={k:reference[k]==result[k] for k in fields}
  print(json.dumps({'status':'PASS' if all(matches.values()) else 'FAIL','id':result['id'],
    'matches':matches,'experimental_not_canonical':True},ensure_ascii=False,indent=2))
  if not all(matches.values()):raise SystemExit(2)
 if args.directory:
  args.directory.mkdir(parents=True,exist_ok=True)
  inner(args.directory)
 else:
  with tempfile.TemporaryDirectory(prefix='VLAB_R27_INDEPENDENT_REPLAY_') as temp:inner(pathlib.Path(temp))
if __name__=='__main__':main()

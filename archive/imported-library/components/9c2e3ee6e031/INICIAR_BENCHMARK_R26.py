#!/usr/bin/env python3
"""R26 Mestre-side incremental scientific laboratory entrypoint.
No browser, no new engine, no canonical writes. Existing SQLite never replaced.
"""
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'fusion_stage12'))
import vlab_r26_master_rulings as r26
import vlab_r26_sensitivity as sens

def main():
 parser=argparse.ArgumentParser(description='VLAB R26 — decisões Mestre e baseline derivada condicional')
 parser.add_argument('--directory',default='benchmarks_r26_meus_salvamentos')
 parser.add_argument('--seed',type=int)
 parser.add_argument('--sensitivity',action='store_true')
 opts=parser.parse_args()
 if opts.sensitivity:
  result=sens.run()
 elif opts.seed is not None:
  result=r26.one(opts.directory,opts.seed)
 else:
  result=r26.batch(opts.directory)
 print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()

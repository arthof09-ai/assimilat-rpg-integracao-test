"""Reproducible bounded R18 LAB demo, using the exact same Runner as the UI.

This program is a test harness, NOT the primary user interface.
"""
import argparse
import json
from pathlib import Path
from vlab_r18_interactive_core import BattleService, canonical


def main():
    parser=argparse.ArgumentParser(description="Executa e audita batalha LAB com o motor R17")
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    out=Path(args.output).expanduser().resolve()
    if out.exists():
        parser.error("Pasta de saída já existe; nunca sobrescrever experimento desconhecido")
    service=BattleService(out)
    before=service.view()
    results=[]
    for turn in range(1,100):
        current=service.view()
        if current["winner"]:
            break
        # Covers both defensive styles, ordinary attack and explicit pass.
        reaction="ESQUIVAR" if turn==1 else "DEFENDER" if turn==3 else "NONE"
        action="PASS" if turn==4 else "ATTACK"
        if action=="PASS":reaction="NONE"
        new=service.act({"request_id":f"r18_demo_turn_{turn:04d}",
             "action":action,"reaction":reaction,"target":current["next_target"]})
        results.append({"turn":turn,"action":action,"reaction":reaction,
                        "hp_ed":new["actors"]["ED"]["hp"],"hp_be":new["actors"]["BE"]["hp"]})
    final=service.view()
    if not final["winner"]:
        raise RuntimeError("BATTLE_NOT_TERMINATED_WITHIN_99_TURNS")
    recovered=service.recover()
    if recovered["events"] != final["events"] or not service.runner.runtime.validate_trace():
        raise RuntimeError("READBACK_DIVERGENCE")
    receipt=service.receipt()
    (out/"VLAB_R18_RECIBO_DEMONSTRACAO.json").write_bytes(canonical(receipt)+b"\n")
    report={"scenario":final["scenario_key"],"source":"R17_STAGED_ENGINE_LOCAL_ONLY",
            "before":before["actors"],"after":final["actors"],"winner":final["winner"],
            "actions":final["active_events"],"engine_effects":final["engine_audit"]["executed"],
            "native_chain_sha256":final["engine_audit"]["engine_tail"],
            "recovered_hash_match":True,"official_combat_count":0,
            "terminals":0,"nac_pass_terminal":"HOLD",
            "fixture_only":True,"trace":results,"receipt_sha256":receipt["receipt_sha256"]}
    (out/"VLAB_R18_RESULTADO_DEMONSTRACAO.json").write_bytes(canonical(report)+b"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ('trace','before','after')},ensure_ascii=False,indent=2))

if __name__=="__main__":main()

"""R18 LOCAL test suite. No internet, Notion, Party or canonical writer.
Run: python -m unittest -v test_vlab_r18_interactive (cwd fusion_stage12).
"""
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer

from vlab_r18_interactive_core import BattleHold, BattleService, SCENARIOS
from vlab_r18_http_ui import Handler


def action(battle, number, reaction="NONE", kind="ATTACK", request_id=None):
    snap = battle.view()
    return battle.act({"request_id": request_id or f"r18test_{number:05d}",
                       "action": kind, "reaction": reaction, "target": snap["next_target"]})


class CoreCases(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.battle = BattleService(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_existing_engine_is_used_and_native_trace_valid(self):
        old = self.battle.view()
        res = action(self.battle, 1, reaction="ESQUIVAR")
        e = res["events"][0]
        self.assertTrue(self.battle.runner.runtime.validate_trace())
        self.assertIn("V081_HISTORIC_NATIVE", e["receipt"]["source"])
        self.assertEqual(res["engine_audit"]["executed"], 1)
        self.assertEqual(res["turn_number"], 2)
        self.assertEqual(res["actors"]["BE"]["reaction"], 0)
        self.assertEqual(res["actors"]["BE"]["pa"], old["actors"]["BE"]["pa"])
        self.assertEqual(res["source_status"], "LAB_FIXTURE_ONLY_NOT_STRICT_NOT_CANON")

    def test_defender_and_normal_attacks_and_pass(self):
        one = action(self.battle, 1, reaction="DEFENDER")
        self.assertIsNotNone(one["events"][0]["receipt"]["defense_result"])
        two = action(self.battle, 2)
        self.assertEqual(two["engine_audit"]["executed"], 2)
        three = action(self.battle, 3, kind="PASS")
        self.assertEqual(three["engine_audit"]["executed"], 2)
        self.assertEqual(three["active_events"], 3)
        self.assertEqual(three["events"][-1]["action"], "PASS")

    def test_idempotency_and_duplicate_mismatch(self):
        payload = {"request_id":"test_same_abc", "action":"ATTACK", "reaction":"NONE", "target":"BE"}
        a = self.battle.act(payload)
        b = self.battle.act(payload)
        self.assertEqual(a["engine_audit"], b["engine_audit"])
        self.assertEqual(b["deduplicated_request"], "test_same_abc")
        with self.assertRaisesRegex(BattleHold,"DUPLICATE_ID"):
            self.battle.act({**payload,"action":"PASS"})

    def test_recover_deterministic_and_new_process(self):
        action(self.battle,1)
        action(self.battle,2,reaction="DEFENDER")
        before=self.battle.view()
        self.assertEqual(self.battle.recover()["engine_audit"],before["engine_audit"])
        another=BattleService(self.tmp.name)
        self.assertEqual(another.view()["events"],before["events"])
        self.assertEqual(another.view()["engine_audit"],before["engine_audit"])

    def test_undo_has_history_and_recovery(self):
        action(self.battle,1)
        first=self.battle.view()
        action(self.battle,2)
        x=self.battle.undo("undo_req_001")
        self.assertEqual(x["events"],first["events"])
        self.assertEqual(x["active_events"],1)
        self.assertEqual(len(x["void_events"]),1)
        self.assertEqual(len(self.battle.session["decisions"]),2)
        self.assertTrue(self.battle.session["decisions"][1]["voided"])
        self.assertEqual(self.battle.recover()["events"],first["events"])
        self.assertEqual(self.battle.undo("undo_req_001")["deduplicated_undo"],"undo_req_001")
        action(self.battle,3)
        self.assertEqual(self.battle.view()["active_events"],2)

    def test_invalid_action_and_target_leave_state_unchanged(self):
        old=self.battle.receipt()
        for data in [{"request_id":"bad_target_a","action":"ATTACK","reaction":"NONE","target":"ED"},
                     {"request_id":"bad_action_abc","action":"MAGIC","reaction":"NONE","target":"BE"},
                     {"request_id":"bad_react_abc","action":"ATTACK","reaction":"ESQUIVAR","target":"ED"}]:
            with self.assertRaises(BattleHold):self.battle.act(data)
        self.assertEqual(self.battle.receipt(),old)

    def test_two_scenarios_distinct_and_fixture_initiative_no_tie(self):
        for key in SCENARIOS:
            self.battle.new(key)
            state=self.battle.view()
            self.assertNotEqual(state["initiative"]["scores"]["ED"],state["initiative"]["scores"]["BE"])
            self.assertEqual(len(state["order"]),2)
            self.assertEqual(state["initiative"]["formula"],"Bronze: 1d6 + DES + bônus de Iniciativa")
            action(self.battle,1)

    def test_battle_can_finish_without_any_official_effect(self):
        for i in range(1,70):
            state=self.battle.view()
            if state["winner"]:
                break
            action(self.battle,i)
        final=self.battle.view()
        self.assertTrue(final["winner"])
        self.assertEqual(final["status"],"FINISHED_EXPERIMENTAL_HP0")
        self.assertEqual(final["engine_audit"]["canonical_credits"],0)
        self.assertEqual(self.battle.receipt()["official_combat_count"],0)
        self.assertLessEqual(final["active_events"],70)
        with self.assertRaises(BattleHold):action(self.battle,71)

    def test_corrupt_journal_does_not_silently_reset(self):
        action(self.battle,1)
        f=self.battle._path(self.battle.session["session_id"])
        j=json.loads(f.read_text());j["scenario"]="BRONZE_RESISTENCIA"
        f.write_text(json.dumps(j))
        with self.assertRaisesRegex(BattleHold,"JOURNAL_INTEGRITY"):
            self.battle.recover()


class HTTPFlow(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.server=ThreadingHTTPServer(("127.0.0.1",0),Handler)
        self.server.battle=BattleService(self.tmp.name)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.base=f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join(timeout=2)
        self.tmp.cleanup()

    def get(self,path):
        with urllib.request.urlopen(self.base+path,timeout=5) as response:
            return response.read(),response.headers

    def post(self,path,obj,allow_err=False,custom=True):
        raw=json.dumps(obj).encode()
        headers={"Content-Type":"application/json"}
        if custom:headers["X-VLAB-UI"]="1"
        req=urllib.request.Request(self.base+path,data=raw,headers=headers,method="POST")
        try:
            with urllib.request.urlopen(req,timeout=10) as response:
                return response.status,json.loads(response.read())
        except urllib.error.HTTPError as e:
            if not allow_err:raise
            return e.code,json.loads(e.read())

    def test_browser_assets_and_continuous_combat(self):
        body,heads=self.get("/")
        self.assertIn(b"Combate experimental",body)
        self.assertIn(b"Content-Security-Policy",str(heads).encode())
        self.assertIn(b"fetch",self.get("/vlab.js")[0])
        self.assertIn(b".surface",self.get("/vlab.css")[0])
        before=json.loads(self.get("/api/state")[0])
        self.assertEqual(before["active_events"],0)
        status,new=self.post("/api/new",{"scenario":"BRONZE_RESISTENCIA"})
        self.assertEqual(status,200)
        self.assertEqual(new["scenario_key"],"BRONZE_RESISTENCIA")
        status,result=self.post("/api/act",{"request_id":"test_http_001","action":"ATTACK","reaction":"ESQUIVAR","target":new["next_target"]})
        self.assertEqual(status,200)
        self.assertEqual(result["active_events"],1)
        self.assertEqual(result["events"][0]["receipt"]["defense_result"]["action"],"ESQUIVAR")
        status,recovered=self.post("/api/recover",{})
        self.assertEqual(status,200)
        self.assertEqual(result["events"],recovered["events"])
        receipt,headers=self.get("/api/receipt")
        self.assertIn(b"receipt_sha256",receipt)
        self.assertIn("attachment",headers.get("Content-Disposition"))
        status,undone=self.post("/api/undo",{"request_id":"test_http_undo1"})
        self.assertEqual(status,200)
        self.assertEqual(undone["active_events"],0)

    def test_http_denials(self):
        code,invalid=self.post("/api/act",{"request_id":"r18_http01","action":"ATTACK","reaction":"NONE","target":"BE"},allow_err=True,custom=False)
        self.assertEqual(code,403)
        self.assertEqual(invalid["status"],"HOLD")
        code,invalid=self.post("/api/new",{"scenario":"INVALID"},allow_err=True)
        self.assertEqual(code,409)
        self.assertEqual(json.loads(self.get("/api/state")[0])["active_events"],0)

if __name__=="__main__":unittest.main()

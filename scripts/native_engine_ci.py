"""Runner only for exact, pinned VLAB R237 / LEVEL-UP R216-P12 original archives.

Notion, Party, other laboratories and canonical RPG remain unwritable. Original
scripts run in disposable directory with reduced environment, not in source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sqlite3
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
 "vlab": {
  "name": "VLAB_R237_LIVE_FRACO_TRANSITION_NATIVE_COLD_AUDITED_MESTRE_ONLY.zip",
  "sha": "49c2db6ebf8fdae8e378355c3f017e95afe879c7e29ba72086044afdd190d4de",
  "manifest": "SHA256_MANIFEST.json",
  "files": 299
 },
 "levelup": {
  "name": "IBX114_SUCESSOR_R216P12_MESTRE_CORRIGIDO_20261021_MESTRE_ONLY.zip",
  "sha": "619fe210a2e8469df59f7db001220c97309cae79054b7574284a5047c633e4de",
  "manifest": "MANIFEST_R216P12_CORRECTED_SHA256.json",
  "files": 370
 }
}

def digest(buf):
 return hashlib.sha256(buf).hexdigest()

def verify(zippath, meta):
 if zippath.name != meta["name"]:
  raise ValueError("WRONG_SOURCE_ARCHIVE_NAME")
 if digest(zippath.read_bytes()) != meta["sha"]:
  raise ValueError("ARCHIVE_SHA_MISMATCH")
 with zipfile.ZipFile(zippath) as z:
  info = [x for x in z.infolist() if not x.is_dir()]
  names = [x.filename for x in info]
  if len(set(names)) != len(names):
   raise ValueError("DUPLICATE_PATHS")
  if any(x.filename.startswith("/") or ".." in PurePosixPath(x.filename).parts
         or "\\" in x.filename or stat.S_ISLNK(x.external_attr >> 16)
         for x in info):
   raise ValueError("UNSAFE_ZIP_PATH")
  if z.testzip() is not None:
   raise ValueError("ZIP_CRC_MISMATCH")
  manifest = json.loads(z.read(meta["manifest"]))["files"]
  if len(manifest) != meta["files"] or set(manifest) != set(names) - {meta["manifest"]}:
   raise ValueError("MANIFEST_COVERAGE_FAILURE")
  for name, entry in manifest.items():
   expected = entry if isinstance(entry, str) else entry["sha256"]
   if digest(z.read(name)) != expected:
    raise ValueError("MEMBER_SHA_MISMATCH:" + name)
  if sum(x.file_size for x in info) > 15_000_000:
   raise ValueError("UNCOMPRESSED_BYTES_OVER_LIMIT")
 return meta["files"]

def sqlite_content_fingerprint(path):
 """Canonical semantic fingerprint of SQLite tables, schema and rows.
 Physical SQLite pages and file headers can vary between runner versions.
 No SQL writes and no source database changes are made.
 """
 uri=path.resolve().as_uri()+"?mode=ro&immutable=1"
 con=sqlite3.connect(uri,uri=True)
 try:
  if con.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
   raise AssertionError("SQLITE_INTEGRITY_FAILURE:"+path.name)
  schema=con.execute(
    "SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name,tbl_name"
  ).fetchall()
  h=hashlib.sha256()
  def feed(record):
   h.update(json.dumps(record,sort_keys=True,ensure_ascii=False,
                       separators=(",",":"),default=str).encode("utf-8"))
   h.update(b"\n")
  feed(["schema",schema])
  feed(["user_version",con.execute("PRAGMA user_version").fetchone()[0]])
  feed(["application_id",con.execute("PRAGMA application_id").fetchone()[0]])
  for kind,name,_,_ in schema:
   if kind!="table":
    continue
   safe_name=name.replace('"','""')
   # Compare all rows, ignoring only their incidental physical page order.
   encoded=[]
   for row in con.execute('SELECT * FROM "'+safe_name+'"'):
    values=[{"blob_hex":v.hex()} if isinstance(v,bytes)
            else {"float_hex":v.hex()} if isinstance(v,float)
            else v for v in row]
    encoded.append(json.dumps(values,ensure_ascii=False,separators=(",",":")))
   feed(["table",name,"rows",len(encoded)])
   for item in sorted(encoded):
    h.update(item.encode("utf-8")+b"\n")
  return h.hexdigest()
 finally:
  con.close()


def run_original(root, relative, timeout=90):
 env={"PATH":os.environ.get("PATH",""),"HOME":str(root),"PYTHONNOUSERSITE":"1",
      "PYTHONDONTWRITEBYTECODE":"1","LC_ALL":"C.UTF-8"}
 res=subprocess.run([sys.executable,"-I","-B",relative],cwd=root,
                    env=env,timeout=timeout,capture_output=True,text=True)
 if res.returncode:
  raise AssertionError("ORIGINAL_RUN_FAILED:"+relative+"\n"+res.stderr[-2500:])
 return res.stdout

def replay_vlab(root,z):
 receipt=run_original(root,"R237_COLD_PORTABLE_RECOVERY.py",60)
 if "PASS_R237_PORTABLE_COLD_LIVE_FRACO 299 HASHES 8 ARMS 155 COMMITS 640 EVENTS NO_REPLAY" not in receipt:
  raise AssertionError("COLD_BASELINE_MISMATCH")
 original={n:digest(z.read(n)) for n in z.namelist()
           if n.startswith("evidence/db/") and n.endswith(".sqlite")}
 if len(original)!=8:
  raise AssertionError("EXPECTED_EIGHT_COMBAT_BANKS")
 for f in (root/"evidence/db").glob("*.sqlite"):
  f.unlink()
 for f in (root/"evidence/reports").glob("R237_*.json"):
  f.unlink()
 run_original(root,"code/r237_live_weak_onset.py",100)
 run_original(root,"code/r237_independent_readonly_audit.py",100)
 audit=json.loads((root/"evidence/reports/R237_INDEPENDENT_SQL_AUDIT.json").read_text())
 counts=audit["counts"]
 expected={"arms":8,"commits":155,"native_events":640,"hits":104,
           "normal_to_weak_transitions":8,"source_normal_croc_turns":6,
           "source_weak_croc_turns":55,"hp0_lab_stops":2,"censored_horizon":6}
 if audit["status"]!="PASS_R237_LIVE_NORMAL_TO_WEAK_NATIVE_CONDITIONAL":
  raise AssertionError("INDEPENDENT_VLAB_AUDIT_HOLD")
 if any(counts.get(k)!=v for k,v in expected.items()):
  raise AssertionError("R237_METRICS_NOT_IDENTICAL")
 generated={f.relative_to(root).as_posix():digest(f.read_bytes())
            for f in (root/"evidence/db").glob("*.sqlite")}
 if set(original)!=set(generated):
  raise AssertionError("R237_SQLITE_SET_MISMATCH")
 byte_identical=sum(original[n]==generated[n] for n in original)
 semantically_different=[]
 for n in sorted(original):
  reference=root/"_ci_reference"/Path(n).name
  reference.parent.mkdir(exist_ok=True)
  reference.write_bytes(z.read(n))
  if sqlite_content_fingerprint(reference)!=sqlite_content_fingerprint(root/n):
   semantically_different.append(n)
 if semantically_different:
  raise AssertionError("R237_SQLITE_CONTENT_MISMATCH:"+",".join(semantically_different))
 return {"suite":"VLAB_R237","native_battles":8,"events":640,"commits":155,
         "weak_transitions":8,"sqlite_byte_identical":byte_identical,
         "sqlite_semantically_identical":8}

def replay_levelup(root):
 env={"PATH":os.environ.get("PATH",""),"HOME":str(root),
      "PYTHONNOUSERSITE":"1","PYTHONDONTWRITEBYTECODE":"1"}
 # Official P12 targeted suite; NOT the historical 2026 full regression battery.
 source=(
  'import sys,unittest,os;sys.path.insert(0,os.getcwd());'
  'sys.path.insert(0,os.path.join(os.getcwd(),"baseline","code"));'
  'suite=unittest.defaultTestLoader.loadTestsFromName('
  '"test_ibx114_r216p12_master_correction");'
  'r=unittest.TextTestRunner(verbosity=1).run(suite);'
  'print("LEVELUP_P12_RUN="+str(r.testsRun)+";ERR="+str(len(r.errors))+'
  '";FAIL="+str(len(r.failures)));sys.exit(0 if r.wasSuccessful() else 1)'
 )
 p=subprocess.run([sys.executable,"-I","-B","-c",source],cwd=root,
                  env=env,timeout=120,text=True,capture_output=True)
 if p.returncode:
  raise AssertionError("LEVELUP_P12_FAILURE\n"+p.stderr[-2500:])
 if "LEVELUP_P12_RUN=184;ERR=0;FAIL=0" not in p.stdout:
  raise AssertionError("LEVELUP_P12_NOT_COMPLETE\n"+p.stdout[-300:])
 return {"suite":"LEVELUP_R216P12","targeted_native_tests":184,
         "historical_full_regression_2026":"NOT_EXECUTED_IN_THIS_GATE"}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--engine",required=True,choices=sorted(PINS))
 p.add_argument("--archive",required=True,type=Path)
 a=p.parse_args()
 zippath=a.archive.resolve()
 count=verify(zippath,PINS[a.engine])
 with tempfile.TemporaryDirectory(prefix="assimilat_native_CI_TEST_") as folder:
  root=Path(folder)
  with zipfile.ZipFile(zippath) as z:
   z.extractall(root)
   data=replay_vlab(root,z) if a.engine=="vlab" else replay_levelup(root)
 data.update({"status":"PASS_NATIVE_TEST_ONLY","zip_members_verified":count,
              "source_sha256":PINS[a.engine]["sha"],"canonical_promotion":"HOLD",
              "notion_writes":0,"replit_calls":0})
 print(json.dumps(data,sort_keys=True,ensure_ascii=False))

if __name__=="__main__":
 main()

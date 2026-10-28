"""Initialize a disposable LOCAL demonstration (never a live CM instance)."""
import json
import os
import secrets
import sys
from pathlib import Path
from vlab_gateway import Gateway


def main():
    if len(sys.argv)!=3:
        raise SystemExit('Usage: python scripts/bootstrap_local_demo.py /private/demo.sqlite /private/credentials.json')
    db,cred=map(Path,sys.argv[1:])
    if db.resolve()==cred.resolve():
        raise SystemExit('Credential and DB paths must differ')
    cred.parent.mkdir(parents=True,exist_ok=True)
    master=secrets.token_bytes(32)
    controller=secrets.token_urlsafe(42)
    operator=secrets.token_urlsafe(42)
    g=Gateway(db,master)
    g.bootstrap_principal('demo-controller','CM-000001','CONTROLLER',controller,bootstrap_secret=master)
    g.bootstrap_principal('demo-lab','CM-000006','OPERATOR',operator,bootstrap_secret=master)
    # Restrict secrets file to owner. Never copy it into the distributed package.
    fd=os.open(str(cred),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:
        json.dump({'VLAB_GATE_MASTER_KEY_HEX':master.hex(), 'controller_bearer':controller,
                   'operator_bearer':operator,'db':str(db),'environment':'LOCAL_DEMO_ONLY'},f,indent=2)
    print('Created disposable LOCAL sandbox DB and 0600 credentials file; NOTION=OFF; GREEN=HOLD')

if __name__=='__main__':main()

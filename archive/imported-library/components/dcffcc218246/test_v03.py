"""Regressão V03 sem atribuir UAT humana ou Windows real não testado."""
from __future__ import annotations
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from iniciar_levelup import bronze1_fixture, prata_fixture
from mesa_levelup import LocalSession, list_runs, read_run, restore_folder, LocalHold
from fonte_v03 import import_v03, ImportHold, RealSourceHold
from adaptador_copia_local import canonical_sha
from win_filelock_compat import install_windows_flock

ROOT=Path(__file__).resolve().parent
EXAMPLE=json.loads((ROOT/'fichas_locais'/'exemplo_ficticio.json').read_text(encoding='utf-8'))

def bronze(root,state=None,evidence=None):
    session=LocalSession('EXEMPLO TESTE BRONZE', state or bronze1_fixture(),2,
                         root=root,source_evidence=evidence)
    for x in ('CONFIRMO_NIVEIS',2,'FIXO',{'INT':2},{'FOR':3,'CON':3}):session.respond(x)
    assert session.phase=='CONFIRM',session.phase
    return session

def prata(root):
    state=prata_fixture();state['TRANSFORM']['spirit']['cap']=7
    from iniciar_levelup import validate_r17
    validate_r17(state)
    session=LocalSession('EXEMPLO PRATA',state,8,root=root)
    for x in ('CONFIRMO_NIVEIS',2,'ROLAR',{'DES':2},{'FOR':3,'CON':3},{'SAB':2},'ROLAR_AGORA'):
        session.respond(x)
    assert session.phase=='CONFIRM',session.phase
    return session

class V03Tests(unittest.TestCase):
    def test_a_windows_launcher_structure_and_portable_module(self):
        bat=(ROOT/'INICIAR_LEVELUP_WINDOWS.bat').read_bytes()
        self.assertIn(b'cd /d "%~dp0"',bat)
        self.assertIn(b'py -3 iniciar_levelup_gui.py',bat)
        self.assertIn(b'python iniciar_levelup_gui.py',bat)
        self.assertNotIn(b' wsl ',bat.lower())
        self.assertNotIn(b' wsl.exe ',bat.lower())
        from unittest.mock import MagicMock
        fake=types.ModuleType('msvcrt');fake.LK_LOCK=1;fake.LK_UNLCK=2;fake.LK_NBLCK=3
        fake.locking=MagicMock()
        before=sys.modules.get('fcntl')
        try:
            sys.modules.pop('fcntl',None)
            with patch('win_filelock_compat.sys.platform','win32'),patch.dict(sys.modules,{'msvcrt':fake}):
                self.assertTrue(install_windows_flock())
                shim=sys.modules['fcntl']
                with tempfile.TemporaryDirectory() as folder:
                    with open(Path(folder)/'cas.lock','a+b') as f:
                        shim.flock(f.fileno(),shim.LOCK_EX)
                        shim.flock(f.fileno(),shim.LOCK_UN)
                self.assertEqual(fake.locking.call_count,2)
        finally:
            sys.modules.pop('fcntl',None)
            if before is not None:sys.modules['fcntl']=before
        # Simulação de API, NÃO execução Windows real.

    def test_b_bronze_previa_commit_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=bronze(tmp)
            view=s.preview()
            for item in ('Bronze 1★','Bronze 2★','INT:','Vida atual:',
                         'Espírito','DECISÕES','RECIBOS','HABILIDADES','TÍTULOS',
                         'EQUIPAMENTO','INTEGRIDADE','ANTES/DEPOIS'):
                self.assertIn(item,view)
            self.assertEqual(s.store.get_all(),s.initial)
            s.respond('CONFIRMO');receipt=s.commit()
            self.assertEqual(receipt['status'],'EVOLUIDO_MANTIDO_EM_COPIA_LOCAL')
            self.assertEqual(read_run(s.folder)['current']['NORMAL']['level'],2)
            self.assertEqual(s.restore()['status'],'EVOLUIDO_E_RESTAURADO_LOCAL')
            self.assertEqual(read_run(s.folder)['current'],s.initial)
            self.assertEqual(s.store.get_all()['TRANSFORM']['activation_state'],'INACTIVE_NEVER_LEGAL_BRONZE')

    def test_c_prata_rolls_conditions_inactive(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=prata(tmp)
            self.assertIn('6',''.join(s.preview()))
            s.respond('CONFIRMO');r=s.commit()
            self.assertEqual(r['rolled_receipts'],6)
            read=read_run(s.folder)
            self.assertEqual(read['current']['TRANSFORM']['effective_level'],7)
            self.assertEqual(read['current']['TRANSFORM']['activation_state'],s.initial['TRANSFORM']['activation_state'])
            self.assertIn('ativação',read['comparison'].lower())
            self.assertEqual(s.restore()['rollback_exact'],True)

    def test_d_import_preserves_unknown_fields_and_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'fichas_locais').mkdir()
            payload=copy.deepcopy(EXAMPLE)
            payload['snapshot']['campos_desconhecidos']={'originais':{'a':[1,2,{'qualquer':'não descartar'}]}}
            payload['snapshot']['equipamentos'].append({'nome':'Colar fictício','bonus':{'não confirmado':'???'},'objeto_estranho':[1,2]})
            payload['snapshot_sha256']=canonical_sha(payload['snapshot'])
            raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')
            path=root/'fichas_locais'/'ficticio_complexo.json';path.write_bytes(raw)
            state,evidence=import_v03(path,root)
            manifest=evidence['field_provenance']['field_manifest']
            self.assertTrue(any(x['mechanical_equivalence']=='MATCHED_SYNTHETIC_ONLY' for x in manifest))
            self.assertTrue(any(x['mechanical_equivalence']=='NOT_MAPPED_PRESERVED_EXACTLY' for x in manifest))
            self.assertTrue(all(x['authenticity']=='NOT_INDEPENDENTLY_AUTHENTICATED' for x in manifest))
            s=bronze(root,state,evidence)
            s.respond('CONFIRMO');s.commit()
            self.assertEqual((s.folder/'SNAPSHOT_ORIGINAL_IMUTAVEL.json').read_bytes(),raw)
            self.assertEqual(path.read_bytes(),raw)
            obj=json.loads((s.folder/'PROJECAO_SEM_REESCREVER_FICHA.json').read_text())
            self.assertEqual(obj['snapshot_original'],payload['snapshot'])
            self.assertEqual(obj['snapshot_original']['campos_desconhecidos'],payload['snapshot']['campos_desconhecidos'])
            self.assertEqual(obj['engine_projection_after']['NORMAL']['level'],2)
            self.assertFalse(obj['mechanical_source_authenticated'])

    def test_e_real_quarantine_not_promoted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'fichas_locais').mkdir()
            payload=copy.deepcopy(EXAMPLE)
            payload['kind']='FICHA_EXISTENTE_EXPORTADA'
            f=root/'fichas_locais'/'export.json';raw=json.dumps(payload,ensure_ascii=False).encode('utf8');f.write_bytes(raw)
            with self.assertRaises(RealSourceHold) as err:import_v03(f,root)
            from adaptador_copia_local import quarantine_real
            folder=quarantine_real(err.exception.evidence,root)
            self.assertEqual((folder/'COPIA_BRUTA_SEM_EVOLUCAO.json').read_bytes(),raw)
            self.assertFalse((folder/'COPIA_LOCAL_3_DOCS').exists())
            self.assertEqual(len(list_runs(root)),0)

    def test_f_reopen_receipt_rollback_and_replay_denial(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=bronze(tmp);s.respond('CONFIRMO');r=s.commit()
            self.assertEqual(len(list_runs(tmp)),1)
            # Recriação do DurableStore representa reinício do processo.
            view=read_run(s.folder)
            self.assertEqual(view['receipt']['event_id'],r['event_id'])
            with self.assertRaises(LocalHold):s.commit()
            restore_folder(s.folder)
            with self.assertRaises(LocalHold):restore_folder(s.folder)
            self.assertEqual(read_run(s.folder)['receipt']['status'],'EVOLUIDO_E_RESTAURADO_LOCAL')

    def test_g_invalid_choice_and_cancel_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=LocalSession('INVÁLIDO',bronze1_fixture(),2,root=tmp)
            for ans in ('CONFIRMO_NIVEIS',2,'FIXO'):s.respond(ans)
            with self.assertRaises(ValueError):s.respond({'INT':900})
            self.assertEqual(s.phase,'NORMAL')
            self.assertEqual(s.store.get_all(),s.initial)
            s.cancel()
            self.assertFalse((s.folder/'ESTADO_APLICADO.json').exists())
            self.assertEqual(json.loads((s.folder/'RECIBO_CANCELAMENTO.json').read_text())['status'],
                             'CANCELADO_SEM_APLICACAO')

    def test_tamper_wal_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            s=bronze(tmp);s.respond('CONFIRMO');s.commit()
            p=s.folder/'ESTADO_APLICADO.json';data=json.loads(p.read_text());data['NORMAL']['attrs']['INT']+=1
            p.write_text(json.dumps(data))
            with self.assertRaisesRegex(LocalHold,'HOLD'):read_run(s.folder)
            with self.assertRaises(LocalHold):restore_folder(s.folder)

if __name__=='__main__':unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Teste de caixa-preta da MESMA entrada usada por uma pessoa; stdin automatizado != UAT humana."""
from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class TerminalFunctionalTests(unittest.TestCase):
    def run_cli(self, answers):
        before = set((ROOT / 'execucoes').glob('*')) if (ROOT/'execucoes').exists() else set()
        p = subprocess.run([sys.executable, '-u', str(ROOT/'iniciar_levelup.py')], cwd=str(ROOT),
                           input='\n'.join(answers)+'\n', text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=35)
        added = set((ROOT/'execucoes').glob('*')) - before
        self.assertLessEqual(len(added), 1, p.stdout[-1500:])
        return p, (next(iter(added)) if added else None)

    def read(self, directory, basename):
        return json.loads((directory/basename).read_text(encoding='utf-8'))

    def test_bronze_confirma_rollback_e_invalidas(self):
        p, folder = self.run_cli(['1','2','1','2','1','FOR=3','INT=2',
                                  'INT=6','FOR=3,CON=3','1','1'])
        self.assertEqual(p.returncode,0,p.stdout[-1800:])
        self.assertIn('RESPOSTA REJEITADA PELO MOTOR',p.stdout)
        self.assertIn('Atributo',p.stdout)
        r=self.read(folder,'RECIBO_EVOLUCAO.json')
        self.assertEqual(r['status'],'EVOLUIDO_E_RESTAURADO_LOCAL')
        self.assertEqual(r['rollback'],'ROLLED_BACK_VERIFIED_LOCAL')
        self.assertTrue(r['rollback_exact'])
        self.assertTrue(r['readback_equal_plan'])
        self.assertEqual(r['confirmation'],'CONFIRMO')
        a=self.read(folder,'ESTADO_INICIAL.json')
        b=self.read(folder,'ESTADO_APLICADO.json')
        c=self.read(folder,'ESTADO_RESTAURADO.json')
        self.assertEqual(a,c)
        self.assertEqual(b['NORMAL']['level'],2)
        self.assertEqual(a['NORMAL']['level'],1)
        self.assertEqual(b['TRANSFORM']['activation_state'],'INACTIVE_NEVER_LEGAL_BRONZE')
        self.assertEqual(r['notion_writes'],0)

    def test_cancelamento_antes_da_confirmação(self):
        p, folder=self.run_cli(['1','2','1','2','1','INT=2','FOR=3,CON=3','0'])
        self.assertEqual(p.returncode,0,p.stdout[-1500:])
        r=self.read(folder,'RECIBO_CANCELAMENTO.json')
        self.assertEqual(r['status'],'CANCELADO_SEM_APLICACAO')
        self.assertTrue(r['untouched'])
        self.assertFalse((folder/'ESTADO_APLICADO.json').exists())
        self.assertEqual(r['initial_state_digest'],r['readback_digest'])

    def test_prata_cap7_rolagens_recibo_e_rollback(self):
        p, folder=self.run_cli(['2','8','1','2','2','DES=2','FOR=3,CON=3','SAB=2','1','1','1'])
        self.assertEqual(p.returncode,0,p.stdout[-2200:])
        r=self.read(folder,'RECIBO_EVOLUCAO.json')
        receipts=self.read(folder,'RECIBOS_ROLAGENS.json')
        a=self.read(folder,'ESTADO_INICIAL.json')
        b=self.read(folder,'ESTADO_APLICADO.json')
        self.assertEqual(b['NORMAL']['level'],8)
        self.assertEqual(a['TRANSFORM']['spirit']['cap'],7)
        self.assertEqual(b['TRANSFORM']['effective_level'],7)
        self.assertEqual(len(receipts),6)
        self.assertEqual(r['rolled_receipts'],6)
        self.assertEqual(r['status'],'EVOLUIDO_E_RESTAURADO_LOCAL')
        self.assertTrue(r['rollback_exact'])
        self.assertIn('DADO AUDITÁVEL',p.stdout)
        self.assertEqual(r['notion_writes'],0)
        self.assertEqual(r['party_writes'],0)

    def test_manter_evolucao_na_copia(self):
        p, folder=self.run_cli(['1','2','1','2','1','INT=2','FOR=3,CON=3','1','2'])
        self.assertEqual(p.returncode,0,p.stdout[-2000:])
        r=self.read(folder,'RECIBO_EVOLUCAO.json')
        self.assertEqual(r['status'],'EVOLUIDO_MANTIDO_EM_COPIA_LOCAL')
        self.assertEqual(self.read(folder,'ESTADO_APLICADO.json')['NORMAL']['level'],2)
        self.assertFalse((folder/'ESTADO_RESTAURADO.json').exists())
        self.assertNotEqual(r['before_sha256'],r['after_sha256'])
        candidates = []
        for entry in sorted((ROOT/'execucoes').glob('*'), reverse=True):
            rf = entry/'RECIBO_EVOLUCAO.json'
            if rf.is_file() and json.loads(rf.read_text(encoding='utf-8')).get('status') in (
                    'EVOLUIDO_MANTIDO_EM_COPIA_LOCAL', 'COMMITTED_LOCAL_VERIFIED'):
                candidates.append(entry)
        index = candidates.index(folder) + 1
        restored, no_folder = self.run_cli(['3', str(index), '1'])
        self.assertEqual(restored.returncode, 0, restored.stdout[-1600:])
        self.assertIsNone(no_folder)
        final = self.read(folder, 'RECIBO_EVOLUCAO.json')
        self.assertEqual(final['status'], 'EVOLUIDO_E_RESTAURADO_LOCAL')
        self.assertTrue(final['rollback_exact'])
        self.assertEqual(self.read(folder, 'ESTADO_INICIAL.json'),
                         self.read(folder, 'ESTADO_RESTAURADO.json'))

    def test_taxa_divergente_entra_hold_sem_gravacao(self):
        p, folder=self.run_cli(['1','2','1','3'])
        self.assertEqual(p.returncode,0,p.stdout[-1700:])
        r=self.read(folder,'RECIBO_CANCELAMENTO.json')
        self.assertEqual(r['status'],'CANCELADO_SEM_APLICACAO')
        self.assertTrue(r['untouched'])
        self.assertFalse((folder/'ESTADO_APLICADO.json').exists())


if __name__=='__main__':
    unittest.main(verbosity=2)

import copy,hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from adaptador_copia_local import import_local,ImportHold,canonical_sha
ROOT=Path(__file__).resolve().parent
EXAMPLE=json.loads((ROOT/'fichas_locais'/'exemplo_ficticio.json').read_text())

class ImportedTests(unittest.TestCase):
    def run_entry(self, answers):
        p=subprocess.run([sys.executable,'-u',str(ROOT/'iniciar_levelup.py')],
         cwd=ROOT,input='\n'.join(answers)+'\n',capture_output=True,text=True,timeout=30)
        return p
    def test_imported_snapshot_e2e(self):
        old=set((ROOT/'execucoes').glob('*')) if (ROOT/'execucoes').exists() else set()
        p=self.run_entry(['4','exemplo_ficticio.json','2','1','2','1','INT=2','FOR=3,CON=3','1','1'])
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        new=set((ROOT/'execucoes').glob('*'))-old
        self.assertEqual(len(new),1)
        folder=new.pop()
        orig=(ROOT/'fichas_locais'/'exemplo_ficticio.json').read_bytes()
        self.assertEqual((folder/'SNAPSHOT_ORIGINAL_IMUTAVEL.json').read_bytes(),orig)
        source=json.loads((folder/'PROJECAO_SEM_REESCREVER_FICHA.json').read_text())
        self.assertEqual(source['snapshot_original'],EXAMPLE['snapshot'])
        self.assertEqual(source['engine_projection_after']['NORMAL']['level'],2)
        self.assertEqual(source['engine_projection_before']['NORMAL']['level'],1)
        r=json.loads((folder/'RECIBO_EVOLUCAO.json').read_text())
        self.assertTrue(r['rollback_exact'])
    def test_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as x:
            d=Path(x);(d/'fichas_locais').mkdir()
            e=copy.deepcopy(EXAMPLE);e['snapshot']['equipamentos'].append({'nome':'ALTERADO'})
            (d/'fichas_locais'/'a.json').write_text(json.dumps(e))
            with self.assertRaisesRegex(ImportHold,'SHA-256'):
                import_local('a.json',d)
    def test_real_hold(self):
        with tempfile.TemporaryDirectory() as x:
            d=Path(x);(d/'fichas_locais').mkdir()
            e=copy.deepcopy(EXAMPLE);e['kind']='FICHA_EXISTENTE_EXPORTADA'
            (d/'fichas_locais'/'r.json').write_text(json.dumps(e))
            with self.assertRaisesRegex(ImportHold,'HOLD REAL'):
                import_local('r.json',d)
    def test_real_quarantine_without_engine(self):
        d=ROOT/'fichas_locais';p=d/'exportacao_real_SIMULADA.json'
        e=copy.deepcopy(EXAMPLE);e['kind']='FICHA_EXISTENTE_EXPORTADA'
        p.write_text(json.dumps(e,ensure_ascii=False),encoding='utf8')
        q=ROOT/'importacoes_quarentena'
        old=set(q.glob('*')) if q.exists() else set()
        try:
            result=self.run_entry(['4',p.name])
            self.assertEqual(result.returncode,2,result.stdout+result.stderr)
            self.assertIn('IMPORTAÇÃO REAL EM QUARENTENA',result.stdout)
            new=set(q.glob('*'))-old
            self.assertEqual(len(new),1)
            folder=new.pop()
            self.assertEqual((folder/'COPIA_BRUTA_SEM_EVOLUCAO.json').read_bytes(),p.read_bytes())
            receipt=json.loads((folder/'RECIBO_HOLD.json').read_text())
            self.assertEqual(receipt['status'],'QUARENTENA_REAL_HOLD_SEM_MOTOR')
            self.assertFalse((folder/'ESTADO_APLICADO.json').exists())
        finally:
            p.unlink(missing_ok=True)
    def test_missing_blocks_hold(self):
        with tempfile.TemporaryDirectory() as x:
            d=Path(x);(d/'fichas_locais').mkdir()
            e=copy.deepcopy(EXAMPLE);e['snapshot']['blocos_originais']=[]
            e['snapshot_sha256']=canonical_sha(e['snapshot'])
            (d/'fichas_locais'/'r.json').write_text(json.dumps(e))
            with self.assertRaisesRegex(ImportHold,'sem blocos'):
                import_local('r.json',d)
    def test_outside_path_denied(self):
        with self.assertRaises(ImportHold):
            import_local('../../LEIA-ME.md',ROOT)

if __name__=='__main__': unittest.main(verbosity=2)

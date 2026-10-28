"""GUI real Tk sob display virtual Linux, NÃO equivale a teste Windows ou UAT."""
import tempfile,tkinter as tk,unittest
from unittest.mock import patch
from pathlib import Path
import iniciar_levelup_gui as gui
from mesa_levelup import LocalSession,list_runs

class GUIWorkflowTest(unittest.TestCase):
    def test_bronze_full_window_and_readback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=tk.Tk()
            try:
                with patch.object(gui,'LocalSession',side_effect=lambda *a,**k:LocalSession(*a,root=tmp,**k)),\
                    patch.object(gui,'list_runs',side_effect=lambda:list_runs(tmp)),\
                    patch.object(gui.messagebox,'askyesno',return_value=True),\
                    patch.object(gui.messagebox,'showinfo',return_value=None),\
                    patch.object(gui.messagebox,'showwarning',return_value=None):
                    app=gui.LevelUpWindow(root)
                    root.update()
                    app.set_character(1)
                    app.start_session()
                    self.assertEqual(app.session.phase,'TARGET')
                    app.answer('CONFIRMO_NIVEIS')
                    app.answer(2)
                    app.mode_answer('FIXO')
                    app.answer({'INT':2})
                    app.answer({'FOR':3,'CON':3})
                    self.assertEqual(app.session.phase,'CONFIRM')
                    text=app.preview_text.get('1.0','end')
                    self.assertIn('ANTES/DEPOIS',text)
                    self.assertIn('Bronze 1★ → Bronze 2★',text)
                    app.confirm()
                    self.assertEqual(app.session.phase,'READY')
                    app.apply()
                    self.assertIn('EVOLUIDO_MANTIDO',app.history.get('1.0','end'))
                    s=app.session
                    app.restore_current()
                    self.assertIsNone(app.session)
                    self.assertEqual(s.store.get_all(),s.initial)
                    app.inspect_selected()
                    self.assertIn('EVOLUÇÃO',app.preview_text.get('1.0','end'))
            finally:root.destroy()


    def test_prata_gui_rolled_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=tk.Tk()
            try:
                with patch.object(gui,'LocalSession',side_effect=lambda *a,**k:LocalSession(*a,root=tmp,**k)),\
                    patch.object(gui.messagebox,'askyesno',return_value=True),\
                    patch.object(gui.messagebox,'showwarning',return_value=None):
                    app=gui.LevelUpWindow(root)
                    app.set_character(2)
                    app.target_value.set('8')
                    app.start_session()
                    for v in ('CONFIRMO_NIVEIS',2,'ROLAR',{'DES':2},{'FOR':3,'CON':3},{'SAB':2},'ROLAR_AGORA'):
                        app.answer(v)
                    self.assertEqual(app.session.phase,'CONFIRM')
                    self.assertIn('Total recibos: 6',app.preview_text.get('1.0','end'))
                    app.confirm();app.apply()
                    self.assertIn('"rolled_receipts": 6',app.history.get('1.0','end'))
            finally:root.destroy()

    def test_file_selector_quarantine_no_engine(self):
        import json,copy
        from test_v03 import EXAMPLE
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'fichas_locais';folder.mkdir()
            rec=copy.deepcopy(EXAMPLE);rec['kind']='FICHA_EXISTENTE_EXPORTADA'
            path=folder/'FICHA_SIMULADA_DECLARADA_REAL.json'
            original=json.dumps(rec,ensure_ascii=False).encode('utf-8')
            path.write_bytes(original)
            root=tk.Tk()
            try:
                with patch.object(gui,'APP_ROOT',Path(tmp)),\
                    patch.object(gui.filedialog,'askopenfilename',return_value=str(path)),\
                    patch.object(gui.messagebox,'showwarning',return_value=None):
                    app=gui.LevelUpWindow(root)
                    app.import_character()
                    quarantine=list((Path(tmp)/'importacoes_quarentena').glob('*/COPIA_BRUTA_SEM_EVOLUCAO.json'))
                    self.assertEqual(len(quarantine),1)
                    self.assertEqual(quarantine[0].read_bytes(),original)
                    self.assertIsNone(app.session)
            finally:root.destroy()

if __name__=='__main__':unittest.main(verbosity=2)

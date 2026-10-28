import unittest
from audit_native_facade import active_fields, attr_value, state_from_engine

class ParserTests(unittest.TestCase):
    def test_extract_chunks(self):
        t='## ESTADO ATIVO INTEGRAL DO MOTOR — TEST\nSTATE_000: {"NORMAL":{},\nSTATE_001: "TRANSFORM":{},"LOCKS":{}}\n<details>archive'
        self.assertEqual(set(state_from_engine(t)),{'NORMAL','TRANSFORM','LOCKS'})
    def test_history_is_not_active(self):
        s='**NÍVEL:** 16\n---\n**NÍVEL:** 999'
        self.assertEqual(active_fields(s)['NÍVEL'],'16')
    def test_duplicate_active_rejected(self):
        with self.assertRaises(ValueError): active_fields('**NÍVEL:** 16\n**NÍVEL:** 17')
    def test_layer_extract(self):
        self.assertEqual(attr_value('FOR: 2 \\| DES: 13 \\| CON: 10','DES'),'13')
        self.assertIsNone(attr_value('FOR: 2','INT'))
    def test_missing_motor_rejected(self):
        with self.assertRaises(ValueError): state_from_engine('NO MOTOR')
if __name__=='__main__': unittest.main()

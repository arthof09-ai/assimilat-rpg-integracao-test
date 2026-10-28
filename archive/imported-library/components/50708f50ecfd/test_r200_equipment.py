"""Isolated prospective TEST fixtures; verifies physical-magic separation and no-history mutations."""
import unittest
from fractions import Fraction
from r200_equipment_and_profiles import RANKS,weapon,armor,build_profile,state

class PhysicalAndStateTests(unittest.TestCase):
    def test_rank_tables_all(self):
        for i,rank in enumerate(RANKS):
            self.assertEqual(weapon('espada',rank),(i+1,8))
            self.assertEqual(weapon('adaga',rank),(i+1,4))
            self.assertEqual(weapon('brutal',rank),(2*(i+1),6))
            self.assertEqual(armor('LEVE',rank)['physical_ca'],3+2*i)
            self.assertEqual(armor('MEDIA',rank)['physical_ca'],7+2*i)
            self.assertEqual(armor('PESADA',rank)['physical_ca'],10+4*i)
    def test_absolute_prospective(self):
        self.assertEqual(weapon('espada','OURO'),(4,8))
        self.assertEqual(weapon('brutal','LENDARIO'),(12,6))
        self.assertEqual(weapon('brutal','PRATA'),(6,6))
        self.assertEqual(armor('PESADA','OURO_NEGRO')['physical_ca'],26)
    def test_speeds_exact_no_rounding(self):
        for kind,frac in [('LEVE',Fraction(1)),('MEDIA',Fraction(3,4)),('PESADA',Fraction(1,2))]:
            st=armor(kind,'OURO')
            self.assertEqual(Fraction(st['speed_factor_num'],st['speed_factor_den']),frac)
            self.assertEqual(Fraction(10)*frac,{'LEVE':Fraction(10),'MEDIA':Fraction(15,2),'PESADA':Fraction(5)}[kind])
    def test_profiles_checksum_and_racial(self):
        for level in (1,2,3,4,5,6):
            p=build_profile(level)
            self.assertEqual(sum(p['natural_initial'].values()),37)
            self.assertEqual(sum(p['natural_current'].values()),37+(level-1)*5)
            self.assertEqual(p['ff'],10*sum(p['natural_current'][k] for k in ('FOR','DES','CON')))
            self.assertEqual(len(p['ff_milestones']),p['ff']//100)
            self.assertEqual(p['ff_damage_bonus'],sum(z['roll_d4'] for z in p['ff_milestones'].values()))
            self.assertEqual(p['transform'],'PROHIBITED' if level<=5 else 'ELIGIBLE_ONLY_NO_SPIRIT_IDENTIFIED')
        self.assertEqual(build_profile(1)['natural_hp_max'],26)
        self.assertEqual(build_profile(1)['natural_pa_max'],22)
        self.assertEqual(build_profile(6)['natural_hp_max'],129)
        self.assertEqual(build_profile(6)['natural_pa_max'],116)
        with self.assertRaises(ValueError):build_profile(7)
    def test_magic_off_keeps_physical_and_innate(self):
        for level in (1,6):
            p=build_profile(level); a=state(p,False);b=state(p,True)
            for prop in ['weapon_dice','armor_physical_ca','mobility','hp','base_pa','profile','level']:
                self.assertEqual(a[prop],b[prop],prop)
            self.assertEqual(Fraction(b['ca'])-Fraction(a['ca']),2)
            self.assertEqual(a['ring_PA_daily_debited_TEST'],0)
            self.assertEqual(b['ring_PA_daily_debited_TEST'],13)
            self.assertEqual(a['pa_free_at_entry']-b['pa_free_at_entry'],13)
            self.assertFalse(a['magic_source_rank_admitted'] or b['magic_source_rank_admitted'])
            self.assertEqual(p['ring_proxy']['rank'],'NOT_PUBLISHED')
    def test_no_mutation_between_variants(self):
        p=build_profile(1)
        before=(p['weapon']['physical_dice'],p['armor']['physical_ca'],p['ff_damage_bonus'])
        state(p,True);state(p,False);state(p,True)
        self.assertEqual(before,(p['weapon']['physical_dice'],p['armor']['physical_ca'],p['ff_damage_bonus']))
if __name__=='__main__':unittest.main()

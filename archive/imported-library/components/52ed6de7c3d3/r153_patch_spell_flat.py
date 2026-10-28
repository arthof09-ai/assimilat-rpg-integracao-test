from pathlib import Path
p=Path(__file__).resolve().parent/'native_v081_controlled/vlab_effects_v08.py'
s=p.read_text()
old="damage_rolls:tuple[int,...]|None=None,damage_faces:int|None=None):"
new="damage_rolls:tuple[int,...]|None=None,damage_faces:int|None=None,documented_flat_bonus:int=0):"
assert s.count(old)==1;s=s.replace(old,new)
old="or sum(damage_rolls)!=damage:"
new="or type(documented_flat_bonus)!=int or documented_flat_bonus<0 or sum(damage_rolls)+documented_flat_bonus!=damage:"
assert s.count(old)==1;s=s.replace(old,new)
old="'save_effect':explicit_save_effect,'save_exceeds_cd':target_save_exceeds_cd,'damage_rolls':damage_rolls,'damage_faces':damage_faces,"
new="'save_effect':explicit_save_effect,'save_exceeds_cd':target_save_exceeds_cd,'damage_rolls':damage_rolls,'damage_faces':damage_faces,'documented_flat_bonus':documented_flat_bonus,"
assert s.count(old)==1;s=s.replace(old,new)
p.write_text(s)

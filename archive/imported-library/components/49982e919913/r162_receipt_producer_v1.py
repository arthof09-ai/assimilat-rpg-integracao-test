"""Prospective source-native receipt classifier. No combat logic; uses committed ledger fields.
Only call after independent validation of row_sha/R18 chain, not as a substitute for it.
"""
from dataclasses import dataclass

class ReceiptError(ValueError):pass

def classify_committed_action(action:dict)->dict:
 if action.get('action') not in ('weapon_attack','spell'):raise ReceiptError('NOT_OFFENSIVE_NATIVE_EVENT')
 physical=action['action']=='weapon_attack'
 k_before='before_hp' if physical else 'hp_before';k_after='after_hp' if physical else 'hp_after'
 k_net='net' if physical else 'effective'
 required=('raw','rd_applied',k_before,k_after,k_net)
 if any(k not in action for k in required):raise ReceiptError('INCOMPLETE_NATIVE')
 if any(type(action[k]) is not int or action[k]<0 for k in required):raise ReceiptError('INVALID_NATIVE_NUMBERS')
 before,after,post=action[k_before],action[k_after],action[k_net]
 if post!=max(0,action['raw']-action['rd_applied']):raise ReceiptError('NATIVE_RD_ARITHMETIC_MISMATCH')
 actual=before-after;over=post-actual
 if not (after==max(0,before-post) and 0<=actual<=before and 0<=over and actual+over==post):raise ReceiptError('NATIVE_HP_DAMAGE_INCONSISTENT')
 if physical:
  if action.get('hp_loss_actual')!=actual or action.get('overkill')!=over:raise ReceiptError('WEAPON_NATIVE_RECEIPT_MISMATCH')
 spell_dice_pre_save=None
 if not physical and 'damage_rolls' in action:
  rolls=action['damage_rolls'];flat=action.get('documented_flat_bonus',0)
  if type(rolls) is not list or any(type(k) is not int or k<=0 for k in rolls) or type(flat) is not int:
   raise ReceiptError('INVALID_SPELL_DICE_TRANSCRIPT')
  spell_dice_pre_save=sum(rolls)+flat
  if action.get('save_effect')=='SAVE-HALF' and action.get('save_exceeds_cd') is True:
   if spell_dice_pre_save%2:raise ReceiptError('ODD_HALF_HOLD_NO_ROUNDING_RULE')
   expected=spell_dice_pre_save//2
  elif action.get('save_effect')=='SAVE-HALF' and action.get('save_exceeds_cd') is False:
   expected=spell_dice_pre_save
  else:expected=None
  if expected is not None and expected!=action['raw']:
   raise ReceiptError('SAVING_THROW_NATIVE_TRANSCRIPT_MISMATCH')
 return {'gross_spell_dice_pre_save':spell_dice_pre_save,'raw_damage':action['raw'],'rd_applied':action['rd_applied'],
   'net_post_RD':post,'hp_effectively_lost':actual,'overkill':over,
   'hp_before':before,'hp_after':after,
   'hit_condition':action.get('hit') if physical else 'SAVE_EFFECT',
   'action':action['action'],'classification':'HP_CAP_SOURCE_NATIVE_V1','raw_semantics':'POST_SAVE_PRE_RD_WHERE_APPLICABLE'}

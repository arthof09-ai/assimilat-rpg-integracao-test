"""IBX-17 / Level Down additive operation in existing R17 engine; sandbox ONLY.

Reuses R17 normal/transform derived functions and R14 DurableStore/Controller.
Strictly no Notion integration, production credentials, or player-side writing.
The synthetic history is explicit, reproducible, source-bound, with all rolls fixed
and an identified per-level progression allocation. Original engine is untouched.
"""
from __future__ import annotations
import copy, hashlib, json, re, unicodedata
from pathlib import Path

from engine_r13 import ATTRS, FIXED, addattrs, ff, milestone_stats, rank
from engine_r17 import validate_r17, _race_derived_normal, _race_derived_transform
from durable_r14 import DurableStore, DurableController
from r10_recovery import digest

class DownHold(ValueError):pass

ALIASES={'forca':'FOR','for':'FOR','destreza':'DES','des':'DES',
         'constituicao':'CON','con':'CON','inteligencia':'INT','int':'INT',
         'sabedoria':'SAB','sab':'SAB','carisma':'CAR','car':'CAR'}
PATTERN=re.compile(r'(?<!\w)(?:-\s*)?(\d+)\s*(?:(?:pontos?|atributos?)\s*)?(?:de|em|da|do)?\s*'
                   r'(forca|destreza|constituicao|inteligencia|sabedoria|carisma|for|des|con|int|sab|car)\b'
                   r'|\b(forca|destreza|constituicao|inteligencia|sabedoria|carisma|for|des|con|int|sab|car)\s*:\s*(\d+)\b')

def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))

def parse_down(text):
    """Natural language, but deny unrecognized mechanics/unknown layers/level changes."""
    if not isinstance(text,str) or not text.strip():raise DownHold('SOLICITACAO_VAZIA')
    t=normalize(text)
    if re.search(r'\b(perca|perder|reduza|reduzir|diminua|diminuir|baixar|baixe)\s+(?:o\s+)?(?:nivel|level|rank|classificacao|estrela)',t):
        raise DownHold('PERDA_DE_NIVEL_E_OUTRA_MODALIDADE')
    if re.search(r'\b(equipamento|titulo|temporario|espirito|demonio|tap|atributos?\s+iniciais?)\b',t):
        raise DownHold('CAMADA_NAO_AUTORIZADA')
    if not re.search(r'\b(retire|retira|retirar|tire|tirar|remova|remover|subtraia|subtrair|menos|corrija|corrigir|level\s*down|reduza|reduzir)\b',t) and not re.match(r'\s*-',t):
        raise DownHold('INTENCAO_DE_RETIRADA_NAO_CONFIRMADA')
    found=[]
    for m in PATTERN.finditer(t):
        val=int(m.group(1) or m.group(4));key=ALIASES[m.group(2) or m.group(3)]
        found.append((m.start(),m.end(),key,val))
    if not found:raise DownHold('ATRIBUTOS_NAO_RECONHECIDOS')
    remainder=t
    for a,b,_,_ in reversed(found):remainder=remainder[:a]+' '+remainder[b:]
    # Allow ONLY familiar conversational framing and the no-level-change clause.
    remainder=re.sub(r'\b(?:nao\s+altere\s+meu\s+nivel|sem\s+alterar\s+(?:o\s+)?nivel|mantenha\s+(?:o\s+)?nivel)\b',' ',remainder)
    remainder=re.sub(r'\b(?:quero|gostaria|por\s+favor|pode|voce|me|da|do|de|os|as|a|o|e|tambem|pontos?|atributos?|normais?|da\s+minha\s+ficha|na\s+ficha|level\s+down|retire|retira|retirar|tirar|tire|remova|remover|subtrair|menos|corrija|corrigir|reduza|reduzir|esses|valores|eu|preciso)\b',' ',remainder)
    remainder=re.sub(r'[\s.,;:!?\-]+','',remainder)
    if remainder:raise DownHold('TEXTO_NAO_RECONHECIDO:'+remainder[:65])
    out={}
    for _,_,key,val in found:
        if key in out:raise DownHold('ATRIBUTO_DUPLICADO:'+key)
        if val<=0 or val>1000:raise DownHold('PONTOS_INVALIDOS')
        out[key]=val
    return out

# Every level has a known synthetic allocation (+2). At level16, explicit
# classification rebase; no past dice are rerolled or retroactively fabricated.
DIST={1:{'DES':2},2:{'DES':2},3:{'DES':2},4:{'DES':2},5:{'DES':2},6:{'DES':2},
      7:{'DES':2},8:{'DES':1,'CON':1},9:{'CON':2},10:{'CON':2},
      11:{'CON':2},12:{'CON':2},13:{'CON':1,'INT':1},14:{'INT':2},
      15:{'SAB':2},16:{'CAR':2}}
BASE_INITIAL={'FOR':6,'DES':5,'CON':5,'INT':4,'SAB':3,'CAR':2}
EXTERNAL={kind:{k:amounts.get(k,0) for k in ATTRS} for kind,amounts in
          {'permanent_title':{'SAB':2},'equipment':{'DES':3},'temporary':{'INT':1}}.items()}
SPIRIT={'FOR':20,'DES':40,'CON':45,'INT':90,'SAB':12,'CAR':9} # 216 @ BAP27, L16

def zero():return {k:0 for k in ATTRS}

def added(*layers):
    x=zero()
    for layer in layers:x=addattrs(x,layer)
    return x

def synthetic_roll_receipt(values, id):
    return {'schema':'SYNTHETIC_ROLL_LEDGER_V1','id':id,
            'values_sha256':hashlib.sha256(json.dumps(values,sort_keys=True).encode()).hexdigest(),
            'actor':'SYNTHETIC_EXPLICIT_TEST'}

def require_synthetic_receipt(receipt, values):
    if not isinstance(receipt,dict) or receipt.get('schema')!='SYNTHETIC_ROLL_LEDGER_V1' or \
       not str(receipt.get('id','')).startswith('SIM-ROLL-') or \
       receipt.get('actor')!='SYNTHETIC_EXPLICIT_TEST' or \
       receipt.get('values_sha256')!=hashlib.sha256(json.dumps(values,sort_keys=True).encode()).hexdigest():
        raise DownHold('ROLAGEM_SEM_RECIBO_SINTETICO_VALIDO')

def growth_totals(history, initial, stat, rank_rebases):
    """Authoritative classification rebase at 6/11/16, frozen rolls otherwise.
    This EXAMPLE uses fixed-choice per level; no initial value is recounted.
    """
    points=copy.deepcopy(initial)
    hp=10+initial['CON'] if stat=='CON' else 10+initial['INT']
    for ev in history:
        lv=ev['level'];points=addattrs(points,ev['allocation'])
        if lv in (6,11,16):
            die={6:8,11:10,16:12}[lv]
            dice=rank_rebases[str(lv)]['values']
            hp=(10+initial['CON'] if stat=='CON' else 10+initial['INT'])+sum(dice)+lv*points[stat]
        else:
            die={0:6,1:8,2:10,3:12,4:20}[(lv-1)//5]
            hp+=ev['dice_value']+points[stat]
    return hp

def make_history():
    return [{'level':lv,'allocation':{k:DIST[lv].get(k,0) for k in ATTRS},
             'dice_mode':'FIXO_60_PERCENT_HISTORICO','dice_value':FIXED[{0:6,1:8,2:10,3:12,4:20}[(lv-1)//5]],
             'source':'SYNTHETIC_LEDGER_EXPLICIT','retracted':zero()} for lv in range(1,17)]

def _locks():
    data={}
    for mark in range(1,15):
        typ=('CA','DANO','VIDA')[(mark-1)%3]
        rolls=[(mark%4)+1] if typ!='VIDA' else [3,3]
        data[str(mark)]={'type':typ,'rolls':rolls,'first_source':'SIM-FIRST-REACHED-HISTORIC','historical':True}
    return data

def layer_intrinsic(n):return added(n['initial_attrs'],*(ev['allocation'] for ev in n['level_allocation_history']))

def verify_history(pages):
    n,t,l=(pages[x] for x in ('NORMAL','TRANSFORM','LOCKS'))
    if n.get('level')!=16 or n.get('id')!='SYNTH-IBX17-LEVELDOWN-ON16':
        raise DownHold('HISTORICO_SINTETICO_IDENTIDADE_OU_NIVEL_INVALIDO')
    if n.get('progression_confirmed')!='SYNTHETIC_EXPLICIT':raise DownHold('HISTORICO_NAO_SINTETICO')
    if n['initial_attrs']!=BASE_INITIAL or sum(n['initial_attrs'].values())!=25:
        raise DownHold('INICIAIS_HISTORICAS_INVALIDAS')
    if n['hp_initial']!=10+BASE_INITIAL['CON'] or n['pa_initial']!=10+BASE_INITIAL['INT']:
        raise DownHold('VALORES_INICIAIS_REESCRITOS')
    hist=n.get('level_allocation_history')
    if not isinstance(hist,list) or len(hist)!=16 or [x['level'] for x in hist]!=list(range(1,17)):
        raise DownHold('EPISODIOS_HISTORICOS_INCOMPLETOS')
    tally=zero()
    for ev in hist:
        lv=ev['level'];die={0:6,1:8,2:10,3:12,4:20}[(lv-1)//5]
        a,b=ev.get('allocation'),ev.get('retracted')
        if not isinstance(a,dict) or not isinstance(b,dict) or set(a)!=set(ATTRS) or set(b)!=set(ATTRS):
            raise DownHold('CAMADAS_HISTORICAS_DESCONHECIDAS')
        if any(type(v)!=int or v<0 for v in list(a.values())+list(b.values())) or sum(a.values())+sum(b.values())!=2:
            raise DownHold('ORCAMENTO_HISTORICO_CONTRADITORIO')
        if ev.get('source')!='SYNTHETIC_LEDGER_EXPLICIT':raise DownHold('ORIGEM_HISTORICA_NAO_VERIFICADA')
        if ev.get('dice_mode') not in ('FIXO_60_PERCENT_HISTORICO','ROLADO_COM_RECIBO'):
            raise DownHold('ESCOLHA_DE_DADOS_DESCONHECIDA')
        val=ev.get('dice_value')
        if type(val)!=int or not 1<=val<=die:
            raise DownHold('DADO_HISTORICO_IMPOSSIVEL')
        if ev['dice_mode']=='FIXO_60_PERCENT_HISTORICO' and val!=FIXED[die]:
            raise DownHold('DADO_FIXO_HISTORICO_DIVERGENTE')
        if ev['dice_mode']=='ROLADO_COM_RECIBO':
            require_synthetic_receipt(ev.get('dice_receipt'),[val])
        tally=addattrs(tally,b)
    if tally!=n.get('retraction_total'):raise DownHold('RETRACOES_NAO_RECONCILIADAS')
    rebases=n.get('rank_rebases')
    if not isinstance(rebases,dict) or set(rebases)!={'6','11','16'}:
        raise DownHold('REBASE_HISTORICO_AUSENTE')
    for lv,die in ((6,8),(11,10),(16,12)):
        rec=rebases[str(lv)]
        if rec.get('mode') not in ('FIXO_60_PERCENT_HISTORICO','ROLADO_COM_RECIBO'):
            raise DownHold('REBASE_SEM_ORIGEM')
        vals=rec.get('values')
        if not isinstance(vals,list) or len(vals)!=lv or any(type(v)!=int or not 1<=v<=die for v in vals):
            raise DownHold('REBASE_SEM_ROLAGENS_COMPLETAS')
        if rec['mode']=='FIXO_60_PERCENT_HISTORICO' and any(v!=FIXED[die] for v in vals):
            raise DownHold('REBASE_FIXO_DIVERGENTE')
        if rec['mode']=='ROLADO_COM_RECIBO':require_synthetic_receipt(rec.get('dice_receipt'),vals)
    layers=n.get('attribute_layers')
    if not isinstance(layers,dict) or set(layers)!=set(EXTERNAL):raise DownHold('CAMADAS_NAO_MAPEADAS')
    for layer in layers.values():
        if set(layer)!=set(layer_intrinsic(n)) or any(type(v)!=int or v<0 for v in layer.values()):
            raise DownHold('BONUS_EXTERNO_INVALIDO')
    actual=added(layer_intrinsic(n),*[layers[x] for x in ('permanent_title','equipment','temporary')])
    if n['attrs']!=actual:raise DownHold('ATRIBUTOS_GERAIS_NAO_CONCILIADOS')
    if n['hp_natural']!=growth_totals(hist,n['initial_attrs'],'CON',rebases):
        raise DownHold('VIDA_HISTORICA_DIVERGENTE')
    if n['pa_natural']!=growth_totals(hist,n['initial_attrs'],'INT',rebases):
        raise DownHold('ALMA_HISTORICA_DIVERGENTE')
    form_roll=t.get('form_rank_rebase')
    if not isinstance(form_roll,dict) or form_roll.get('mode') not in ('FIXO_60_PERCENT_HISTORICO','ROLADO_COM_RECIBO'):
        raise DownHold('TRANSFORM_DADO_DE_CRESCIMENTO_NAO_CERTIFICADO')
    rollvals=form_roll.get('values')
    if not isinstance(rollvals,list) or len(rollvals)!=16 or any(type(v)!=int or not 1<=v<=20 for v in rollvals):
        raise DownHold('TRANSFORM_ROLAGENS_AUSENTES')
    if form_roll['mode']=='FIXO_60_PERCENT_HISTORICO' and any(v!=12 for v in rollvals):
        raise DownHold('TRANSFORM_D20_FIXO_INVALIDO')
    if form_roll['mode']=='ROLADO_COM_RECIBO':require_synthetic_receipt(form_roll.get('dice_receipt'),rollvals)
    if t['hp_theoretical_natural']!=n['hp_initial']+sum(rollvals)+16*t['attrs']['CON']:
        raise DownHold('T6B_VIDA_TEORICA_DIVERGENTE')
    if t['pa_theoretical_natural']!=n['pa_initial']+sum(rollvals)+16*t['attrs']['INT']:
        raise DownHold('T6B_ALMA_TEORICA_DIVERGENTE')
    return True

def recompute(pages):
    """Call EXISTING R17/ R13 formula operators; T6-B theoretical diff."""
    n,t,l=(pages[x] for x in ('NORMAL','TRANSFORM','LOCKS'))
    natural=layer_intrinsic(n)
    n['attrs']=added(natural,*[n['attribute_layers'][k] for k in ('permanent_title','equipment','temporary')])
    n['hp_natural']=growth_totals(n['level_allocation_history'],n['initial_attrs'],'CON',n['rank_rebases'])
    n['pa_natural']=growth_totals(n['level_allocation_history'],n['initial_attrs'],'INT',n['rank_rebases'])
    t['attrs']=addattrs(n['attrs'],t['overlay'])
    # For the synthetic Ouro Negro16 character the transform uses a d20 fixed=12;
    # T6-B DIFFERENCE is calculated from both form maxima, not direct roll addition.
    lv=n['level']
    if lv!=16:raise DownHold('SYNTHETIC_HISTORY_SCOPE_ONLY_L16')
    t['hp_theoretical_natural']=n['hp_initial']+sum(t['form_rank_rebase']['values'])+lv*t['attrs']['CON']
    t['pa_theoretical_natural']=n['pa_initial']+sum(t['form_rank_rebase']['values'])+lv*t['attrs']['INT']
    _race_derived_normal(n,l['milestones'])
    _race_derived_transform(n,t,l['milestones'])
    validate_r17(pages)
    verify_history(pages)
    return pages

def create_fixture():
    history=make_history()
    n={'id':'SYNTH-IBX17-LEVELDOWN-ON16','fixture_only':True,'race':'Humano',
       'level':16,'normal_rate':2,'progression_confirmed':'SYNTHETIC_EXPLICIT',
       'initial_attrs':copy.deepcopy(BASE_INITIAL),'attrs':zero(),
       'attribute_layers':copy.deepcopy(EXTERNAL),'level_allocation_history':history,
       'retraction_total':zero(),'retraction_policy':'SYNTHETIC_EXPLICIT_PROGRESS_HISTORY',
       'hp_initial':15,'pa_initial':14,'hp_natural':0,'pa_natural':0,
       'rank_rebases':{str(lv):{'mode':'FIXO_60_PERCENT_HISTORICO','values':[FIXED[die]]*lv}
                       for lv,die in ((6,8),(11,10),(16,12))},
       'hp_permanent':5,'pa_permanent':20,'hp_current':240,'pa_current':150,
       'pa_committed':30,'hp_max':0,'pa_max':0,'pa_free':0,'pa_spendable_now':120,
       'armor':2,'magic_prof':3,'luta_prof':2,'magic_cd_other':2,
       'weapon_damage_base_fixture':4,'hp_growth_mode':'60_PERCENT_FIXED',
       'pa_growth_mode':'60_PERCENT_FIXED','titles':[],'title_credits':{},
       'history':['SYNTHETIC: sixteen known +2 allocations with fixed dice; no Party'],
       'untouched':{'inventario':['anel-experimental +3 DES'],'links':['synthetic://only']}}
    t={'id':n['id'],'fixture_only':True,'effective_level':16,
       'spirit':{'id':'SYNTHETIC-EMERF-NOT-REAL','bap':27,'cap':16,'allowed_attrs':list(ATTRS),'abilities':['Sombras simuladas']},
       'overlay':copy.deepcopy(SPIRIT),'attrs':zero(),'tap_carry_half_units':0,
       'hp_theoretical_natural':0,'pa_theoretical_natural':0,
       'form_rank_rebase':{'mode':'FIXO_60_PERCENT_HISTORICO','values':[12]*16},
       'hp_bonus_max':0,'pa_bonus_max':0,'hp_bonus_current':200,'pa_bonus_current':400,
       'abilities_active':['Sombras simuladas'],'activation_state':'INACTIVE_NO_T6B_REFRESH',
       'history':['SYNTHETIC fixed TAP 216 previously earned, no activation'],
       'untouched':{'synthetic_image_ref':'no-image'}}
    l={'id':n['id'],'fixture_only':True,'milestones':_locks(),
       'history':['all FF milestones 100..1400 earned/rolled before correction; locks permanent']}
    x={'NORMAL':n,'TRANSFORM':t,'LOCKS':l}
    return recompute(x)

def inspect_before(pages):
    n,t,l=(pages[k] for k in ('NORMAL','TRANSFORM','LOCKS'))
    natural=layer_intrinsic(n)
    return {'level':n['level'],'rank':rank(n['level'])[2],
            'natural':natural,'title':n['attribute_layers']['permanent_title'],
            'equipment':n['attribute_layers']['equipment'],
            'temporary':n['attribute_layers']['temporary'],
            'normal_general':n['attrs'],'spirit_tap':t['overlay'],
            'transformed_general':t['attrs'],
            'normal':{'hp_initial':n['hp_initial'],'hp_natural':n['hp_natural'],'hp_max':n['hp_max'],
                      'hp_current':n['hp_current'],'pa_initial':n['pa_initial'],'pa_natural':n['pa_natural'],
                      'pa_max':n['pa_max'],'pa_current':n['pa_current'],'pa_committed':n['pa_committed'],
                      'pa_free':n['pa_free'],'pa_spendable_now':n['pa_spendable_now'],
                      **n['derived']},
            'transform':{'hp_theoretical_natural':t['hp_theoretical_natural'],
                         'pa_theoretical_natural':t['pa_theoretical_natural'],
                         'hp_bonus_max':t['hp_bonus_max'],'hp_bonus_current':t['hp_bonus_current'],
                         'pa_bonus_max':t['pa_bonus_max'],'pa_bonus_current':t['pa_bonus_current'],
                         **t['derived']},
            'active_marks_normal':[int(i) for i in l['milestones'] if 100*int(i)<=ff(n['attrs'])],
            'active_marks_transform':[int(i) for i in l['milestones'] if 100*int(i)<=ff(t['attrs'])],
            'locks_total':len(l['milestones']),
            'budget':{'granted':25+2*n['level'],'current_natural':sum(natural.values()),
                      'invalid_retracted':sum(n['retraction_total'].values()),
                      'spirit_tap_earned':sum(t['overlay'].values()),
                      'spirit_tap_expected':(t['spirit']['bap']*t['effective_level'])//2}}

def calculate_down(source,requested):
    validate_r17(source)
    verify_history(source)
    p=copy.deepcopy(source)
    n=p['NORMAL']; t=p['TRANSFORM']
    if not isinstance(requested,dict) or not requested:raise DownHold('SEM_CORRECAO')
    if any(k not in ATTRS or type(v)!=int or v<1 for k,v in requested.items()):raise DownHold('CORRECAO_INVALIDA')
    available={k:sum(ev['allocation'].get(k,0) for ev in n['level_allocation_history']) for k in ATTRS}
    for key,val in requested.items():
        if val>available[key]:raise DownHold('PONTOS_DISTRIBUIDOS_INSUFICIENTES:'+key)
    # Exactly these level-sourced synthetic allocations are retracted. The choice
    # of epochs is explicit in the receipt; not a real-player history inference.
    removed={k:[] for k in requested}
    for key,desired in requested.items():
        pending=desired
        for ev in reversed(n['level_allocation_history']):
            if not pending:break
            take=min(pending,ev['allocation'][key])
            if take:
                ev['allocation'][key]-=take
                ev['retracted'][key]+=take
                removed[key].append({'level':ev['level'],'points':take})
                pending-=take
        if pending:raise DownHold('HISTORICO_INSUFICIENTE:'+key)
        n['retraction_total'][key]+=desired
    # Historical source and initial values remain immutable; no reroll.
    recompute(p)
    if p['NORMAL']['level']!=source['NORMAL']['level'] or p['TRANSFORM']['effective_level']!=t['effective_level']:
        raise DownHold('NIVEL_MUDOU')
    if p['TRANSFORM']['overlay']!=t['overlay'] or p['LOCKS']!=source['LOCKS']:
        raise DownHold('TAP_OU_MARCOS_MODIFICADOS')
    if p['NORMAL']['initial_attrs']!=source['NORMAL']['initial_attrs']:
        raise DownHold('INICIAL_MODIFICADO')
    # Reservations should NEVER be silently truncated/filled/healed.
    for key in ('hp_current','pa_current','pa_committed'):
        if p['NORMAL'][key]!=source['NORMAL'][key]:raise DownHold('RECURSO_NORMAL_ALTERADO:'+key)
    for key in ('hp_bonus_current','pa_bonus_current'):
        if p['TRANSFORM'][key]!=source['TRANSFORM'][key]:raise DownHold('RECURSO_ESPIRITUAL_RECARREGADO')
    initial_record={ev['level']:(ev['dice_mode'],ev['dice_value'],ev.get('dice_receipt')) for ev in source['NORMAL']['level_allocation_history']}
    final_record={ev['level']:(ev['dice_mode'],ev['dice_value'],ev.get('dice_receipt')) for ev in p['NORMAL']['level_allocation_history']}
    if initial_record!=final_record or source['NORMAL']['rank_rebases']!=p['NORMAL']['rank_rebases'] or source['TRANSFORM']['form_rank_rebase']!=p['TRANSFORM']['form_rank_rebase']:
        raise DownHold('DADOS_HISTORICOS_ALTERADOS')
    before=inspect_before(source);after=inspect_before(p)
    return {'updated':p,'before':before,'after':after,'removed_events':removed,
            'changed':{k:{'before':before['normal'][k],'after':after['normal'][k]}
                       for k in before['normal'] if before['normal'][k]!=after['normal'][k]},
            'marks_deactivated':{'normal':sorted(set(before['active_marks_normal'])-set(after['active_marks_normal'])),
                                 'transform':sorted(set(before['active_marks_transform'])-set(after['active_marks_transform']))},
            'direct_delta':{'FF':after['normal']['ff']-before['normal']['ff'],
                            'VIDA_MAX':after['normal']['hp_max']-before['normal']['hp_max'],
                            'ALMA_MAX':after['normal']['pa_max']-before['normal']['pa_max']}}

class LevelDownSession:
    """Uses SAME local R14 WAL and R17 derived formulas as Level Up.
    Session receives chat turns; no app, terminal or code needed from the Mestre.
    """
    def __init__(self,root):
        self.root=Path(root);self.metadata=self.root/'LEVELDOWN_SESSION.json'
        self.initial_path=self.root/'PREIMAGEM_SINTETICA.json'
        self.store_path=self.root/'COPIA_LOCAL_3_DOCS'
    def _read(self,p):return json.loads(Path(p).read_text(encoding='utf-8'))
    def _write(self,p,val):
        from durable_r14 import _atomic_json
        _atomic_json(p,val)
    def start(self):
        if self.metadata.exists():return self.view()
        if self.root.exists() and any(self.root.iterdir()):raise DownHold('SESSAO_EXISTENTE_DESCONHECIDA')
        self.root.mkdir(parents=True,exist_ok=True)
        fixture=create_fixture();validate_r17(fixture)
        self._write(self.initial_path,fixture)
        DurableStore(self.store_path,fixture)
        self._write(self.metadata,{'schema':'IBX17-LEVELDOWN-SERVICE-V1','actor':'SYNTHETIC_ONLY',
            'engine':'EXISTING_R17_PLUS_R14','phase':'READY_FOR_REQUEST',
            'initial_hash':digest(fixture),'current_event':None,'requested':None,
            'official_writes':0,'party_writes':0,'level_granted':False})
        return self.view()
    def view(self):
        if not self.metadata.exists():raise DownHold('SESSAO_INEXISTENTE')
        m=self._read(self.metadata);initial=self._read(self.initial_path)
        if digest(initial)!=m['initial_hash']:raise DownHold('PREIMAGEM_ALTERADA')
        validate_r17(initial)
        verify_history(initial)
        store=DurableStore(self.store_path)
        live=store.get_all();validate_r17(live);verify_history(live)
        phase=m['phase']
        if phase in ('READY_FOR_REQUEST','PREVIEW','CANCELLED') and live!=initial:
            raise DownHold('Efeito sem commit declarado')
        if phase=='COMMITTED_LOCAL':
            event=store.event(m['current_event'])
            if not event or event['state']!='COMMITTED' or digest(live)!=event['intent_hash']:
                raise DownHold('COMMIT_SEM_READBACK')
        if phase=='REVERTED_LOCAL':
            if live!=initial:raise DownHold('REVERSAO_INCOMPLETA')
            rec=self._read(self.root/'RECIBO_LEVELDOWN.json')
            rev=store.event(rec.get('reverse_event_id','')) if rec.get('reverse_event_id') else None
            if rev is None or rev.get('state')!='COMMITTED' or rev.get('intent_hash')!=digest(initial):
                raise DownHold('REVERSAO_SEM_RECIBO_WAL')
        result={'phase':phase,'character':'PERSONAGEM_SINTETICA_OURO_NEGRO_1',
                'source_sha256':m['initial_hash'],'current_sha256':digest(live),
                'level':live['NORMAL']['level'],'rank':rank(live['NORMAL']['level'])[2],
                'official_writes':0,'party_writes':0,'original_session_untouched':True,
                'question':{'READY_FOR_REQUEST':'Informe: Retire 10 de Destreza e 5 de Constituição. Não altere meu nível.',
                            'CANCELLED':'Cancelado sem efeitos. Nova solicitação pode iniciar outra prévia.',
                            'PREVIEW':'Prévia pronta. Responda CONFIRMO TESTE LOCAL ou CANCELAR.',
                            'COMMITTED_LOCAL':'Aplicação local verificada. Responda REVERTER TESTE LOCAL ou ESTADO.',
                            'REVERTED_LOCAL':'Reversão exata comprovada. Nenhum commit real.'}.get(phase,'HOLD')}
        if m['current_event']:
            result['event_id']=m['current_event']
            result['receipt_file']=str(self.root/'RECIBO_LEVELDOWN.json')
        if phase=='PREVIEW':
            preview=self._read(self.root/'PREVIA_LEVELDOWN.json')
            if preview['before_sha256']!=digest(live):raise DownHold('PREVIA_STALE')
            calc=calculate_down(live,preview['requested'])
            if digest(calc['updated'])!=preview['after_sha256']:raise DownHold('PREVIA_ADULTERADA')
            result['preview']=preview['display']
        if phase in ('COMMITTED_LOCAL','REVERTED_LOCAL'):
            receipt=self._read(self.root/'RECIBO_LEVELDOWN.json')
            expected=receipt['after_sha256'] if phase=='COMMITTED_LOCAL' else receipt['before_sha256']
            if digest(live)!=expected:raise DownHold('RECIBO/STORE_DIVERGEM')
            result['receipt']=receipt
        return result
    def interact(self,text,origin='MESTRE_CHAT_REQUEST_UNVERIFIED'):
        if origin not in ('MESTRE_CHAT_REQUEST_UNVERIFIED','AUTOMATED_TEST_INPUT'):
            raise DownHold('ORIGEM_NAO_PERMITIDA')
        if not self.metadata.exists():self.start()
        state=self.view();phase=state['phase'];m=self._read(self.metadata)
        t=normalize(text).strip()
        if phase=='PREVIEW' and t in ('cancelar','cancelo','nao confirmo','cancelar pre via'):
            m['phase']='CANCELLED';self._write(self.metadata,m)
            return self.view()
        if phase=='PREVIEW' and t=='confirmo teste local':
            preview=self._read(self.root/'PREVIA_LEVELDOWN.json')
            initial=self._read(self.initial_path);store=DurableStore(self.store_path)
            if store.get_all()!=initial or digest(initial)!=preview['before_sha256']:
                raise DownHold('PREIMAGEM_DIVERGIU_NAO_EXECUTAR')
            calc=calculate_down(initial,preview['requested'])
            if digest(calc['updated'])!=preview['after_sha256']:raise DownHold('PREVIA_INCOMPATIVEL')
            plan={'event_id':preview['event_id'],'before_digest':digest(initial),'updates':calc['updated']}
            # Do not repeat effect in case of unknown WAL state.
            if store.event(preview['event_id']) is not None:raise DownHold('EVENTO_EXISTENTE_HOLD_RECONCILIAR')
            e=DurableController(store).run(plan)
            reopened=DurableStore(self.store_path).get_all()
            if e['state']!='COMMITTED' or digest(reopened)!=preview['after_sha256']:
                raise DownHold('EFEITO_LOCAL_INDETERMINADO_READBACK')
            receipt={'event_id':preview['event_id'],'origin':origin,
                     'authorization':'LOCAL_SANDBOX_ONLY_CONFIRMADO_NESTA_SESSAO',
                     'character':'SYNTHETIC_ONLY','reason':preview['request_text'],
                     'removed':preview['requested'],'events_retracted':calc['removed_events'],
                     'before_sha256':preview['before_sha256'],'after_sha256':preview['after_sha256'],
                     'before':calc['before'],'after':calc['after'],
                     'readback':'MATCH_LOCAL_FILES','ff_locks_preserved':True,
                     'level_unchanged':True,'tap_preserved':True,
                     'notion_writes':0,'party_writes':0,'real_character_writes':0}
            self._write(self.root/'RECIBO_LEVELDOWN.json',receipt)
            m['phase']='COMMITTED_LOCAL';self._write(self.metadata,m)
            return self.view()
        if phase=='COMMITTED_LOCAL' and t not in ('confirmo teste local','estado','status','reverter teste local'):
            if parse_down(text)==m['requested']:
                v=self.view();v['idempotent']='REQUEST_ALREADY_APPLIED_NOOP';return v
            raise DownHold('JA_HA_COMMIT_OUTRA_SOLICITACAO_HOLD')
        if phase=='COMMITTED_LOCAL' and t in ('confirmo teste local','estado','status'):
            v=self.view();v['idempotent']='READBACK_NO_SECOND_COMMIT'
            return v
        if phase=='COMMITTED_LOCAL' and t=='reverter teste local':
            store=DurableStore(self.store_path)
            receipt=self._read(self.root/'RECIBO_LEVELDOWN.json')
            if digest(store.get_all())!=receipt['after_sha256']:
                raise DownHold('REVERTER_PREIMAGEM_DIVERGENTE')
            e=DurableController(store).explicit_rollback(m['current_event'])
            reopened=DurableStore(self.store_path).get_all()
            if e['state']!='COMMITTED' or digest(reopened)!=receipt['before_sha256']:
                raise DownHold('REVERSAO_NAO_EXATA')
            receipt['reverse_event_id']=e['event_id'];receipt['reversal']='REVERTED_EXACT_READBACK'
            self._write(self.root/'RECIBO_LEVELDOWN.json',receipt)
            m['phase']='REVERTED_LOCAL';self._write(self.metadata,m)
            return self.view()
        if phase=='REVERTED_LOCAL' and t=='reverter teste local':
            v=self.view();v['idempotent']='REVERSAL_ALREADY_VERIFIED'
            return v
        if phase in ('READY_FOR_REQUEST','CANCELLED'):
            wanted=parse_down(text)
            initial=self._read(self.initial_path)
            calc=calculate_down(initial,wanted)
            evt='SIM-LD-'+hashlib.sha256((digest(initial)+json.dumps(wanted,sort_keys=True)).encode()).hexdigest()[:24]
            if DurableStore(self.store_path).event(evt) is not None:
                raise DownHold('JA_TESTADO_EVENTO_NAO_REAPLICAR')
            preview={'event_id':evt,'before_sha256':digest(initial),
                     'after_sha256':digest(calc['updated']),'request_text':text,
                     'requested':wanted,'display':{
                         'antes':calc['before'],'depois':calc['after'],
                         'origens_retiradas':calc['removed_events'],
                         'marcos_desativados':calc['marks_deactivated'],
                         'delta_direto':calc['direct_delta'],
                         'nota':'Somente cópia fictícia; level, histórico inicial, itens, títulos, rolagens e TAP preservados.'}}
            self._write(self.root/'PREVIA_LEVELDOWN.json',preview)
            m['phase']='PREVIEW';m['current_event']=evt;m['requested']=wanted
            self._write(self.metadata,m)
            return self.view()
        raise DownHold('TRANSICAO_NAO_AUTORIZADA:'+phase)

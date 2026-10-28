"""R16 candidate human-choice dialogue -- never a Party chat sender.

Can be driven by a synthetic harness only. Player-facing lines are templates;
this module never uses Notion, messaging, email, O Primeiro, or real IDs.
Only decisions requiring a human are prompted; calculations stay with engine.
"""
from __future__ import annotations
import copy
from dataclasses import dataclass,field
from typing import Any
from engine_r13 import ATTRS,RulePending,rank,ff,addattrs
from r16_gate import FIRST_TRANSFORM_LEVEL,access,plan_prata

class DialogueHold(RulePending):pass


def _budget(state,level):
    n=state['NORMAL']; t=state['TRANSFORM']
    # Other sources require a separately verified case contract.
    if n['titles'] or n['title_credits']:
        raise DialogueHold('retroactive title choices not admitted without per-source authority')
    normal=n['normal_rate']
    spirit=(t['spirit']['bap']*min(level,t['spirit']['cap']))//2 - (t['spirit']['bap']*min(level-1,t['spirit']['cap']))//2
    return normal,spirit


def _alloc(a,expected,allowed):
    if not isinstance(a,dict):raise DialogueHold('Envie um mapa de atributos para a distribuição.')
    if set(a)-set(allowed):raise DialogueHold('Atributo não permitido nesta distribuição.')
    if any(type(v) is not int or v<0 for v in a.values()):raise DialogueHold('Use apenas inteiros não negativos.')
    if sum(a.values())!=expected:raise DialogueHold(f'A distribuição soma {sum(a.values())}, mas o orçamento é {expected}.')
    return dict(a)


@dataclass
class Dialogue:
    """State machine for one verified, *fictional* Prata level-up.

    Production flag is intentionally absent; no path for real characters.
    """
    state:dict
    target_level:int
    event_id:str='SIM-DIALOGUE-R16-001'
    cursor_level:int=0
    phase:str='RATE'
    answer_log:list=field(default_factory=list)
    choices:dict=field(default_factory=dict)
    result:dict|None=None
    blocker:str|None=None

    def __post_init__(self):
        n=self.state['NORMAL']
        if n['fixture_only'] is not True or n['id']!='SYNTH-R16-PRATA-ONLY':
            raise DialogueHold('only invented Prata fixtures supported')
        if n['level']<FIRST_TRANSFORM_LEVEL or self.target_level<=n['level'] or self.target_level>25:
            raise DialogueHold('unsupported level or missing legitimate goal')
        rank(self.target_level)
        self.cursor_level=n['level']+1
        self.choices={'target_level':self.target_level,'normal_allocations':{},
                      'spirit_allocations':{},'milestones':{},
                      'actor':'SIMULATED_TEST_AGENT','approval':'OFFLINE_SYNTHETIC_ONLY'}

    def _expected(self):return _budget(self.state,self.cursor_level)

    def prompt(self):
        """Portuguese proposed Party-safe wording. No secret sources in strings."""
        normal,spirit=self._expected()
        n=self.state['NORMAL'];tier0=rank(n['level'])[2];tier1=rank(self.target_level)[2]
        if self.phase=='RATE':
            return (f'Você vai do nível {n["level"]} ({tier0}) para {self.target_level} ({tier1}), conforme a evolução registrada. '
                    'Antes de continuar: quantos pontos de atributos NORMAIS você recebe por nível, contando os bônus permanentes já confirmados? '
                    'Responda com o número. Se sua ficha disser algo diferente, eu verificarei com o Mestre antes de alterar qualquer coisa.')
        if self.phase=='MODE':
            return ('Para o crescimento de Vida e Alma, você prefere os valores fixos de 60% dos dados ou rolagens? '
                    'Responda FIXO ou ROLAR. A opção ROLAR exige a integração de um registrador auditável de resultados.')
        if self.phase=='NORMAL':
            return (f'No nível {self.cursor_level}, você tem {normal} pontos de atributos normais. '
                    'Como quer distribuir entre Força, Destreza, Constituição, Inteligência, Sabedoria e Carisma? '
                    'A soma deve ser exata. Ex.: FOR=1, DES=1.')
        if self.phase=='SPIRIT':
            return (f'No nível {self.cursor_level}, para a forma espiritual há {spirit} pontos próprios disponíveis neste avanço. '
                    'Nesta ficha de TESTE, os atributos elegíveis são Força e Constituição. '
                    'Como quer distribuir? Esses pontos são separados dos normais.')
        if self.phase=='FF':
            choices=self._needed_ff()
            return (f'Você alcançará o marco novo de {choices[0]*100} de Força Física. '
                    'Escolha o benefício permanente desse marco: DANO, CA ou VIDA. '
                    'A rolagem do bônus será registrada uma única vez e vinculada ao marco.')
        if self.phase=='CONFIRM':
            p=self._preview()
            before=p['before']['NORMAL'];after=p['updates']['NORMAL']
            return (f'Prévia, sem alterar sua ficha: nível {before["level"]} → {after["level"]}; '
                    f'Vida máxima {before["hp_max"]} → {after["hp_max"]}, Vida atual {before["hp_current"]} (sem cura); '
                    f'Alma/PA máximo {before["pa_max"]} → {after["pa_max"]}, PA atual {before["pa_current"]} (sem recarga). '
                    'Os pontos normais, a forma espiritual, a FF e os derivados também serão conferidos. '
                    'Você confirma suas escolhas? Responda CONFIRMO ou CORRIGIR. '
                    'Esta é uma demonstração isolada, sem escrita no Notion.')
        if self.phase=='READY':return 'Suas decisões de TESTE estão confirmadas. A execução local pode gerar save e recibos.'
        if self.phase=='HOLD':return 'Encontrei uma divergência que exige verificação. Nenhuma alteração será feita.'
        return 'Etapa encerrada em ambiente sintético.'

    def _needed_ff(self):
        normal,spirit=self._expected()
        n=self.state['NORMAL'];t=self.state['TRANSFORM']
        total_normal={};total_spirit={}
        for lv in range(n['level']+1,self.cursor_level+1):
            a=self.choices.get('normal_allocations',{}).get(str(lv))
            b=self.choices.get('spirit_allocations',{}).get(str(lv))
            if a is None or b is None:raise DialogueHold('allocate each level before FF')
            for k,v in a.items():total_normal[k]=total_normal.get(k,0)+v
            for k,v in b.items():total_spirit[k]=total_spirit.get(k,0)+v
        updated_normal=addattrs(n['attrs'],total_normal)
        updated_transform=addattrs(addattrs(t['attrs'],total_normal),total_spirit)
        # Inactive form theoretical FF does NOT count as a reached permanent milestone.
        active_form=self.state['TRANSFORM'].get('activation_state')=='ACTIVE_VERIFIED'
        highest=max(ff(updated_normal),ff(updated_transform) if active_form else 0)//100
        existing=set(map(int,self.state['LOCKS']['milestones'])) | set(map(int,self.choices['milestones']))
        return [k for k in range(1,highest+1) if k not in existing]

    def _advance_level(self):
        if self.cursor_level<self.target_level:
            self.cursor_level+=1
            self.phase='NORMAL'
        else:
            self.phase='CONFIRM'

    def _preview(self):
        if not self.event_id.startswith('SIM-'):raise DialogueHold('real event refused')
        ch=copy.deepcopy(self.choices)
        ch['resource_choice']='60_PERCENT_FIXED'
        return plan_prata(self.state,ch,self.event_id)

    def respond(self, answer:Any)->dict:
        """Explicit typed input. Wrong answers do not auto-fill missing choices."""
        phase=self.phase
        if phase in ('READY','HOLD'):raise DialogueHold('terminal dialogue state')
        if phase=='RATE':
            if type(answer) is not int or answer<=0:raise DialogueHold('Informe a taxa de pontos em número inteiro.')
            expected,_=self._expected()
            if answer!=expected:
                self.phase='HOLD';self.blocker='PLAYER_RATE_DIFFERS_FROM_VERIFIED_SOURCE'
                return {'status':'HOLD_MESTRE','reason':'rate differs; do not silently replace verified rule'}
            self.phase='MODE'
        elif phase=='MODE':
            if answer not in ('FIXO','ROLAR'):raise DialogueHold('Opção deve ser FIXO ou ROLAR.')
            if answer=='ROLAR':
                self.phase='HOLD';self.blocker='AUDITABLE_ROLL_PROVIDER_NOT_INTEGRATED'
                return {'status':'HOLD_TECHNICAL','reason':'do not fabricate dice results'}
            self.choices['resource_choice']='60_PERCENT_FIXED';self.phase='NORMAL'
        elif phase=='NORMAL':
            normal,_=self._expected()
            x=_alloc(answer,normal,ATTRS)
            self.choices['normal_allocations'][str(self.cursor_level)]=x
            _,spirit=self._expected()
            if spirit:
                self.phase='SPIRIT'
            else:
                self.choices['spirit_allocations'][str(self.cursor_level)]={}
                if self._needed_ff():self.phase='FF'
                else:self._advance_level()
        elif phase=='SPIRIT':
            _,spirit=self._expected()
            x=_alloc(answer,spirit,self.state['TRANSFORM']['spirit']['allowed_attrs'])
            self.choices['spirit_allocations'][str(self.cursor_level)]=x
            if self._needed_ff():self.phase='FF'
            else:self._advance_level()
        elif phase=='FF':
            needed=self._needed_ff();k=needed[0]
            if not isinstance(answer,dict) or answer.get('type') not in ('CA','DANO','VIDA'):
                raise DialogueHold('Escolha CA, DANO ou VIDA.')
            if answer.get('source')!='SIMULATED_DICE_ONLY':
                raise DialogueHold('Test receipts require synthetic dice provenance; never accept unverified dice')
            rolls=answer.get('rolls')
            if not isinstance(rolls,list) or len(rolls)!=(2 if answer['type']=='VIDA' else 1):
                raise DialogueHold('missing correct number of simulated dice')
            sides=6 if answer['type']=='VIDA' else 4
            if any(type(v) is not int or not 1<=v<=sides for v in rolls):
                raise DialogueHold('simulated roll invalid')
            self.choices['milestones'][str(k)]={'type':answer['type'],'rolls':list(rolls)}
            if self._needed_ff():self.phase='FF'
            else:self._advance_level()
        elif phase=='CONFIRM':
            if answer=='CORRIGIR':
                self.cursor_level=self.state['NORMAL']['level']+1
                self.phase='NORMAL';self.choices['normal_allocations']={};self.choices['spirit_allocations']={};self.choices['milestones']={}
            elif answer=='CONFIRMO':
                self.result=self._preview()
                self.phase='READY'
            else:raise DialogueHold('Exige CONFIRMO ou CORRIGIR.')
        self.answer_log.append({'phase':phase,'answer':copy.deepcopy(answer)})
        return {'status':self.phase,'prompt':self.prompt()}

    def executable_plan(self):
        if self.phase!='READY' or self.result is None:raise DialogueHold('cannot execute before preview and confirmation')
        return copy.deepcopy(self.result)

    def summary(self):
        return {'phase':self.phase,'target_level':self.target_level,'cursor_level':self.cursor_level,
                'answer_count':len(self.answer_log),'blocker':self.blocker,
                'live_writes':False,'notion_writer_available':False,
                'production_released':False,'party_messages_sent':0}

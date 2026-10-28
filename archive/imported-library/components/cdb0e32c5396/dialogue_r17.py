"""R17 player-safe message candidate controller -- SYNTHETIC OFFLINE ONLY.

Requests every human choice, refuses ambiguous source, never calls Notion/Party.
Rolls are generated only by RollLedger; no answer may supply dice values.
"""
from __future__ import annotations
from dataclasses import dataclass,field
import copy
from pathlib import Path
from engine_r13 import ATTRS,rank,ff,addattrs
from engine_r17 import (R17Hold,RESOURCES,bronze5_fixture,validate_r17,dice_contracts,plan_r17)
from roll_ledger_r17 import RollLedger

class DialogueR17Hold(R17Hold):pass

@dataclass
class DialogueR17:
    state:dict
    target_level:int
    event_id:str
    roll_ledger:RollLedger
    phase:str='TARGET'
    cursor:int=0
    answers:list=field(default_factory=list)
    choices:dict=field(default_factory=dict)
    result:dict|None=None
    blocker:str|None=None
    _conditional_index:int=0
    _any_roll_done:bool=False

    def __post_init__(self):
        validate_r17(self.state);start=self.state['NORMAL']['level'];rank(self.target_level)
        if not start<self.target_level:raise DialogueR17Hold('must level up')
        if start<6 and self.state['TRANSFORM'].get('bronze_accounting')!='SYNTHETIC_HYPOTHESIS_NOT_CANON':
            raise DialogueR17Hold('Bronze normal level-up lacks isolated staging contract')
        # T2/T3: the normal actor is allowed to gain levels after the Spirit
        # reaches its verified synthetic cap; Spirit budget thereafter is 0.
        if not self.event_id.startswith('SIM-'):raise DialogueR17Hold('synthetic event only')
        self.cursor=start+1
        self.choices={'target_level':self.target_level,'actor':'SIMULATED_TEST_AGENT',
                      'approval':'OFFLINE_SYNTHETIC_ONLY','normal_allocations':{},
                      'spirit_allocations':{},'milestones':{},'roll_receipts':{},
                      'conditionals':{},'resource_modes':{}}
        self._verify_optional_contracts()

    def _verify_optional_contracts(self):
        for contract in self.state['NORMAL'].get('choice_contracts',[]):
            if (contract.get('source')!='SIMULATED_VERIFIED_CONTRACT' or
                contract.get('impact')!='RECORD_ONLY_TEST' or
                type(contract.get('level')) is not int or
                not isinstance(contract.get('options'),list) or
                len(contract['options'])<2 or any(not isinstance(o,str) for o in contract['options']) or
                contract['level']<=self.state['NORMAL']['level'] or
                contract['level']>self.target_level or
                not contract.get('id')):
                raise DialogueR17Hold('conditional racial/class/skill effect lacks verified handler')

    def _contracts(self,level):
        return [c for c in self.state['NORMAL'].get('choice_contracts',[]) if c['level']==level]

    def _needed_ff(self):
        n=self.state['NORMAL']
        total={k:0 for k in ATTRS}
        for level in range(n['level']+1,self.cursor+1):
            a=self.choices['normal_allocations'].get(str(level))
            if a is None:raise DialogueR17Hold('normal allocation missing before FF')
            for k,v in a.items():total[k]+=v
        ceiling=ff(addattrs(n['attrs'],total))//100
        existing={int(k) for k in self.state['LOCKS']['milestones']}
        existing|={int(k) for k in self.choices['milestones']}
        return [k for k in range(1,ceiling+1) if k not in existing]

    def _budget(self,lv):
        n=self.state['NORMAL'];t=self.state['TRANSFORM']
        a=t['spirit']['bap'];cap=t['spirit']['cap']
        return n['normal_rate'],(a*min(lv,cap))//2-(a*min(lv-1,cap))//2

    def prompt(self):
        n=self.state['NORMAL'];from_lv=n['level'];to_lv=self.target_level
        if self.phase=='TARGET':
            return (f'Sua ficha de TESTE indica nível {from_lv} ({rank(from_lv)[2]}) e o pedido é chegar ao '
                    f'nível {to_lv} ({rank(to_lv)[2]}). Você confirma a quantidade de níveis recebidos, '
                    'com o registro de concessão do Mestre? Responda CONFIRMO_NIVEIS ou REVISAR_NIVEIS.')
        if self.phase=='RATE':
            return ('Antes de evoluir: quantos pontos de atributos NORMAIS você recebe por nível, '
                    'incluindo bônus permanentes confirmados? Informe a quantidade. '
                    'Se divergir da regra verificada, farei uma conferência antes de continuar.')
        if self.phase=='MODE':
            return ('Como deseja calcular o crescimento de Vida e Alma: resultado FIXO de 60% '
                    'ou ROLAR os dados? Pode escolher separadamente, por exemplo '
                    '{"VIDA":"ROLAR","ALMA":"FIXO"}. Os resultados serão registrados; '
                    'se houver dúvida normativa, a evolução será suspensa.')
        if self.phase=='NORMAL':
            budget,_=self._budget(self.cursor)
            return (f'No nível {self.cursor} ({rank(self.cursor)[2]}), você possui {budget} '
                    'pontos normais. Onde deseja distribuir entre FOR, DES, CON, INT, SAB e CAR? '
                    'Informe cada valor, com soma exata. Nada será distribuído automaticamente.')
        if self.phase=='SPIRIT':
            _,budget=self._budget(self.cursor)
            allowed=', '.join(self.state['TRANSFORM']['spirit']['allowed_attrs'])
            return (f'Para o nível {self.cursor}, há {budget} pontos próprios do Espírito nesta '
                    f'configuração de TESTE. Você pode distribuí-los entre {allowed}. '
                    'Eles são separados dos pontos normais e seguem os limites do Espírito.')
        if self.phase=='FF':
            milestone=self._needed_ff()[0]
            return (f'Foi alcançado um novo marco de {milestone*100} de Força Física pela '
                    'ficha normal. Escolha DANO (+1d4), CA (+1d4) ou VIDA (+2d6). '
                    'O dado será rolado uma única vez, com resultado permanente.')
        if self.phase=='CONDITIONAL':
            c=self._contracts(self.cursor)[self._conditional_index]
            return (f'Esta evolução inclui uma escolha adicional de TESTE em {c["label"]}. '
                    f'Qual opção você escolhe: {", ".join(c["options"])}? '
                    'Não vou escolher por você.')
        if self.phase=='ROLLS':
            return ('Suas escolhas estão registradas. Para os benefícios que você escolheu rolar, '
                    'os dados terão compromisso, resultado e recibo auditável sem nova tentativa. '
                    'Deseja realizar as rolagens agora? Responda ROLAR_AGORA ou CORRIGIR.')
        if self.phase=='CONFIRM':
            p=self._preview();b=p['before'];a=p['updates'];n0=b['NORMAL'];n1=a['NORMAL']
            alloc=', '.join(f'{k} {n0["attrs"][k]}→{n1["attrs"][k]}' for k in ATTRS if n0['attrs'][k]!=n1['attrs'][k])
            summaries=[]
            for s in p['steps']:
                res=s['growth'];summaries.append(f'nível {s["level"]}: Vida +dados {res["NORMAL_HP"]["sum"]}; '
                                             f'Alma +dados {res["NORMAL_PA"]["sum"]}')
            spirit_note=('A Transformação ainda não foi ativada. A partir de Prata 1 pode ser elegível, '
                         'mas cada ativação exige suas condições.' if self.target_level>=6 else
                         'A Transformação permanece proibida em Bronze.')
            return (f'PRÉVIA SEM ALTERAR A FICHA: nível {n0["level"]}→{n1["level"]}; '
                    f'atributos: {alloc}; Vida máxima {n0["hp_max"]}→{n1["hp_max"]}, '
                    f'Vida atual permanece {n1["hp_current"]}; Alma/PA máximo '
                    f'{n0["pa_max"]}→{n1["pa_max"]}, PA atual permanece {n1["pa_current"]}; '
                    f'CA {n0["derived"]["ca"]}→{n1["derived"]["ca"]}; '
                    f'FF {n0["derived"]["ff"]}→{n1["derived"]["ff"]}; '
                    f'CD {n0["derived"]["magic_cd"]}→{n1["derived"]["magic_cd"]}. '
                    + '; '.join(summaries)+'. '+spirit_note+
                    ' Deseja confirmar estas escolhas? Responda CONFIRMO ou CORRIGIR. '
                    'A confirmação neste teste NÃO grava nenhuma ficha online.')
        if self.phase=='READY':return 'Confirmação recebida. O plano de TESTE está apto à gravação exclusivamente local.'
        if self.phase=='HOLD':return 'Foi identificada uma divergência. Nenhuma alteração será realizada.'
        return 'Atendimento sintético encerrado.'

    def _alloc(self,a,budget,allowed):
        if not isinstance(a,dict) or set(a)-set(allowed) or any(type(v) is not int or v<0 for v in a.values()):
            raise DialogueR17Hold('distribuição inválida; informe inteiros não negativos e atributos permitidos')
        if sum(a.values())!=budget:raise DialogueR17Hold(f'o total é {sum(a.values())}, deveria ser {budget}')
        return copy.deepcopy(a)

    def _advance_after_alloc(self):
        if self._needed_ff():self.phase='FF'
        elif self._contracts(self.cursor):self.phase='CONDITIONAL';self._conditional_index=0
        else:self._advance_level()

    def _advance_level(self):
        if self.cursor<self.target_level:
            self.cursor+=1;self.phase='NORMAL'
        else:
            self.phase='ROLLS' if any(v=='ROLAR' for v in self.choices['resource_modes'].values()) else 'CONFIRM'

    def _draw(self,purpose,sides,count,roll_id=None):
        rid=roll_id or f'{self.event_id}_{purpose}'
        _,r=self.roll_ledger.draw(rid,self.event_id,purpose,sides,count)
        self._any_roll_done=True
        self.choices['roll_receipts'][rid]=r
        return r

    def _draw_resources(self):
        for spec in dice_contracts(self.state,self.choices):
            if self.choices['resource_modes'][spec['component']]=='ROLAR':
                self._draw(spec['purpose'],spec['sides'],spec['count'])

    def _preview(self):return plan_r17(self.state,self.choices,self.event_id)

    def respond(self,answer):
        phase=self.phase
        if phase in ('HOLD','READY'):raise DialogueR17Hold('terminal')
        if phase=='TARGET':
            if answer=='REVISAR_NIVEIS':self.phase='HOLD';self.blocker='MESTRE_TARGET_RECONCILIATION'
            elif answer=='CONFIRMO_NIVEIS':self.phase='RATE'
            else:raise DialogueR17Hold('confirme apenas o nível registrado, ou solicite revisão')
        elif phase=='RATE':
            if type(answer) is not int or answer<=0:raise DialogueR17Hold('taxa deve ser número inteiro')
            if answer!=self.state['NORMAL']['normal_rate']:
                self.phase='HOLD';self.blocker='PLAYER_RATE_MISMATCH_SOURCE'
            else:self.phase='MODE'
        elif phase=='MODE':
            if answer in ('FIXO','ROLAR'):ans={'VIDA':answer,'ALMA':answer}
            elif isinstance(answer,dict):ans=answer
            else:raise DialogueR17Hold('escolha FIXO ou ROLAR')
            if set(ans)!={'VIDA','ALMA'} or any(x not in ('FIXO','ROLAR') for x in ans.values()):
                raise DialogueR17Hold('opção para Vida/Alma inválida')
            self.choices['resource_modes']={'NORMAL_HP':ans['VIDA'],'TRANSFORM_HP':ans['VIDA'],
                                            'NORMAL_PA':ans['ALMA'],'TRANSFORM_PA':ans['ALMA']}
            self.phase='NORMAL'
        elif phase=='NORMAL':
            budget,_=self._budget(self.cursor)
            self.choices['normal_allocations'][str(self.cursor)]=self._alloc(answer,budget,ATTRS)
            _,spirit=self._budget(self.cursor)
            if spirit:self.phase='SPIRIT'
            else:
                self.choices['spirit_allocations'][str(self.cursor)]={}
                self._advance_after_alloc()
        elif phase=='SPIRIT':
            _,budget=self._budget(self.cursor)
            self.choices['spirit_allocations'][str(self.cursor)]=self._alloc(answer,budget,self.state['TRANSFORM']['spirit']['allowed_attrs'])
            self._advance_after_alloc()
        elif phase=='FF':
            if answer not in ('DANO','CA','VIDA'):raise DialogueR17Hold('marco exige DANO, CA ou VIDA')
            milestone=self._needed_ff()[0]
            # Once a die is rolled for a permanent FF choice, a different choice
            # must not allocate a second roll for the same milestone.
            rid=f'{self.event_id}_FF_{milestone}'
            purpose=f'FF_MILESTONE_{milestone:03d}_{answer}'
            prev=self.choices['roll_receipts'].get(rid)
            if prev and prev['spec']['purpose']!=purpose:
                raise DialogueR17Hold('existing permanent milestone roll cannot be replaced')
            sides=6 if answer=='VIDA' else 4;count=2 if sides==6 else 1
            r=self._draw(purpose,sides,count,roll_id=rid)
            self.choices['milestones'][str(milestone)]={'type':answer}
            self._advance_after_alloc()
        elif phase=='CONDITIONAL':
            c=self._contracts(self.cursor)[self._conditional_index]
            if answer not in c['options']:raise DialogueR17Hold('escolha não existe no contrato confirmado')
            self.choices['conditionals'][c['id']]=answer
            self._conditional_index+=1
            if self._conditional_index>=len(self._contracts(self.cursor)):
                self._advance_level()
        elif phase=='ROLLS':
            if answer=='CORRIGIR':
                if self._any_roll_done:raise DialogueR17Hold('dice rolled; reroll prohibited')
                self._reset_choices()
            elif answer=='ROLAR_AGORA':
                self._draw_resources()
                self.phase='CONFIRM'
            else:raise DialogueR17Hold('confirme a rolagem ou corrija escolhas')
        elif phase=='CONFIRM':
            if answer=='CORRIGIR':
                # Preserve already rolled results. Revision can change allocations,
                # but never mode/type of dice contract with already committed IDs.
                self._reset_choices(preserve_rolls=True)
            elif answer=='CONFIRMO':
                self.result=self._preview();self.phase='READY'
            else:raise DialogueR17Hold('prévia exige CONFIRMO ou CORRIGIR')
        self.answers.append({'phase':phase,'answer':copy.deepcopy(answer),'state_after':self.phase})
        return {'status':self.phase,'prompt':self.prompt() if self.phase not in ('READY','HOLD') else self.prompt()}

    def _reset_choices(self,preserve_rolls=False):
        preserved=copy.deepcopy(self.choices['roll_receipts']) if preserve_rolls else {}
        # FF recorded dice keep immutable if reused, otherwise never reroll.
        self.choices['normal_allocations']={};self.choices['spirit_allocations']={}
        self.choices['milestones']={};self.choices['conditionals']={}
        if not preserve_rolls:self.choices['roll_receipts']={}
        else:self.choices['roll_receipts']=preserved
        self.cursor=self.state['NORMAL']['level']+1;self.phase='NORMAL';self._conditional_index=0

    def executable_plan(self):
        if self.phase!='READY' or self.result is None:raise DialogueR17Hold('not approved')
        return copy.deepcopy(self.result)
    def safe_summary(self):
        return {'phase':self.phase,'level':[self.state['NORMAL']['level'],self.target_level],
                'questions_answered':len(self.answers),'reason':self.blocker,
                'writes_to_player_or_notion':0,'available_in_production':False,
                'receipts_generated':len(self.choices['roll_receipts'])}

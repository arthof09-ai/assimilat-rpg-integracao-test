#!/usr/bin/env python3
"""Mesa gráfica local Windows/Linux/macOS; camada sobre R17/R27 EXISTENTE.

Sem servidor HTTP, internet, pip ou chamadas Notion. Tkinter da biblioteca padrão.
"""
from __future__ import annotations
import json
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

# Imports intencionalmente via CLI: injeta shim Windows antes de motor inalterado.
from iniciar_levelup import (APP_ROOT, ATTRS, rank, bronze1_fixture, prata_fixture,
                              validate_r17, RealSourceHold, ImportHold, quarantine_real)
from fonte_v03 import import_v03
from mesa_levelup import LocalSession, list_runs, read_run, restore_folder, LocalHold

NAVY='#17283d'; BLUE='#2a5076'; PAPER='#f5f7fa'; DARK='#1d2939'; GREEN='#147963'

class LevelUpWindow:
    def __init__(self, root):
        self.root=root
        self.root.title('LEVEL-UP | Mesa experimental do Mestre — v03')
        self.root.geometry('1140x790')
        self.root.minsize(900,660)
        self.root.configure(bg=PAPER)
        self.session=None
        self.character=None
        self.name=None
        self.targets=()
        self.evidence=None
        self.current=None
        self.entry_vars=[]
        self.mode_var=None
        self.option_var=None
        self.phase=None
        self._make_ui()
        self.home()

    def _make_ui(self):
        header=tk.Frame(self.root,bg=NAVY,height=70)
        header.pack(fill='x')
        tk.Label(header,text='LEVEL-UP   •   MESA DO MESTRE',bg=NAVY,fg='white',
                 font=('Segoe UI',18,'bold')).pack(anchor='w',padx=24,pady=(12,0))
        tk.Label(header,text='EXPERIMENTAL • FICTÍCIO • OFFLINE — nenhuma ficha real ou Notion é alterada',
                 bg=NAVY,fg='#cbd5e1',font=('Segoe UI',9)).pack(anchor='w',padx=25)
        body=tk.Frame(self.root,bg=PAPER)
        body.pack(fill='both',expand=True,padx=14,pady=12)
        left=tk.Frame(body,bg='white',width=342,highlightbackground='#e0e4e9',highlightthickness=1)
        left.pack(side='left',fill='y',padx=(0,12))
        left.pack_propagate(False)
        right=tk.Frame(body,bg='white',highlightbackground='#e0e4e9',highlightthickness=1)
        right.pack(side='left',fill='both',expand=True)
        self.left=left
        self.right=right
        self.control=tk.Frame(left,bg='white')
        self.control.pack(fill='x',padx=16,pady=14)
        ttk.Separator(left).pack(fill='x',padx=16,pady=4)
        self.choice=tk.Frame(left,bg='white')
        self.choice.pack(fill='both',expand=True,padx=16,pady=10)
        self.status=tk.StringVar(value='Escolha um personagem fictício para começar.')
        tk.Label(left,textvariable=self.status,bg='white',fg=BLUE,wraplength=305,
                 justify='left',font=('Segoe UI',10)).pack(fill='x',padx=16,pady=(3,15))
        self.tabs=ttk.Notebook(right)
        self.tabs.pack(fill='both',expand=True,padx=10,pady=10)
        self.info=ScrolledText(self.tabs,wrap='word',font=('Consolas',10),padx=10,pady=10)
        self.preview_text=ScrolledText(self.tabs,wrap='word',font=('Consolas',10),padx=10,pady=10)
        self.history=ScrolledText(self.tabs,wrap='word',font=('Consolas',10),padx=10,pady=10)
        self.tabs.add(self.info,text='Ficha / Perguntas')
        self.tabs.add(self.preview_text,text='Antes x Depois')
        self.tabs.add(self.history,text='Histórico / Recibos')
        self._set_text(self.info,'Selecione um personagem à esquerda.')
        self._set_text(self.preview_text,'A comparação integral aparece ANTES de confirmar.')
        self._set_text(self.history,'Aqui ficará o recibo e as sessões mantidas.')

    def _set_text(self,widget,value):
        widget.configure(state='normal')
        widget.delete('1.0','end')
        widget.insert('1.0',value)
        widget.configure(state='disabled')

    def _clear(self,frame):
        for x in frame.winfo_children():x.destroy()

    def _button(self, parent, text, action, *, strong=False):
        b=tk.Button(parent,text=text,command=action,bg=GREEN if strong else '#edf1f7',
                    fg='white' if strong else DARK,activebackground=BLUE if strong else '#dfe8f2',
                    font=('Segoe UI',10,'bold' if strong else 'normal'),relief='flat',
                    wraplength=290,anchor='center',padx=9,pady=9,cursor='hand2')
        b.pack(fill='x',pady=5)
        return b

    def _label(self,text,bold=False):
        tk.Label(self.choice,text=text,bg='white',fg=DARK,wraplength=300,
                 font=('Segoe UI',11,'bold' if bold else 'normal'),justify='left').pack(anchor='w',pady=6)

    def _top(self):
        self._clear(self.control)
        self._button(self.control,'Início / escolher personagem',self.home)
        self._button(self.control,'Sessões anteriores e restauração',self.show_sessions)

    def home(self):
        if self.session and not self.session.committed:
            try:
                self.session.cancel('SAIDA_PARA_MENU_INICIAL')
            except LocalHold as exc:
                messagebox.showwarning('HOLD',str(exc))
                return
        self._top()
        self._clear(self.choice)
        self.session=None;self.character=None;self.evidence=None
        self.status.set('Nada foi alterado no Notion. Todos os cenários são isolados.')
        self._label('1. ESCOLHA UM PERSONAGEM',True)
        self._button(self.choice,'Exemplo fictício — Bronze 1★',lambda:self.set_character(1),strong=True)
        self._button(self.choice,'Exemplo fictício — Prata 1★',lambda:self.set_character(2))
        self._button(self.choice,'Importar cópia JSON experimental',self.import_character)
        self._label('Importação de fonte declarada real = quarentena. Não há leitura REST Notion.')
        self._set_text(self.info,'MODO MESTRE-SIDE / OFFLINE\n\n'
              '1. Clique em Bronze ou Prata.\n2. Escolha o nível permitido.\n'
              '3. Responda aos botões e distribua os pontos.\n'
              '4. Leia a aba Antes x Depois ANTES de confirmar.\n'
              '5. Confirme, mantenha ou restaure a cópia.\n\n'
              'Bronze não pode ativar Transformação Demoníaca.\n'
              'Em Prata, apenas elegibilidade condicionada — não ativação.\n\n'
              'Nenhum dado fictício é promovido a cânone.')
        self._set_text(self.preview_text,'A comparação será feita pelo plano do motor histórico, sem commit.')
        self._set_text(self.history,'Sem sessão selecionada. Use Sessões anteriores para recuperar uma cópia.')
        self.tabs.select(self.info)

    def set_character(self,index):
        if index==1:
            state=bronze1_fixture(); targets=(2,6)
            label='EXEMPLO_FICTICIO_BRONZE_1'
        else:
            state=prata_fixture()
            state['TRANSFORM']['spirit']['cap']=7   # fixture histórica hipotética R25
            validate_r17(state)
            targets=(7,8)
            label='EXEMPLO_FICTICIO_PRATA_1_CAP7'
        self._select(label,state,targets)

    def import_character(self):
        directory=APP_ROOT/'fichas_locais'
        p=filedialog.askopenfilename(parent=self.root,title='Selecione um JSON de fichas_locais',
                        initialdir=str(directory),filetypes=[('Cópia JSON','*.json')])
        if not p:return
        try:
            state,evidence=import_v03(p, APP_ROOT)
        except RealSourceHold as exc:
            try:
                path=quarantine_real(exc.evidence,APP_ROOT)
            except Exception as cause:
                messagebox.showerror('HOLD sem arquivamento','Não foi possível salvar a quarentena: '+str(cause));return
            messagebox.showwarning('HOLD / FICHA REAL','Cópia declarada real preservada em quarentena.\n'
                                   'Nenhuma evolução permitida.\n\nLocal: '+str(path))
            self.status.set('Fonte real declarada: QUARENTENA SEM EVOLUÇÃO')
            return
        except (ImportHold,OSError,ValueError) as exc:
            messagebox.showwarning('Importação bloqueada',str(exc));return
        current=state['NORMAL']['level']
        from engine_r13 import RANKS
        if current+1>len(RANKS)*5:
            messagebox.showwarning('Sem evolução','Esta ficha não possui próximo nível suportado.')
            return
        self._select('CÓPIA FICTÍCIA — '+Path(p).name,state,(current+1,),evidence)

    def _select(self,label,state,targets,evidence=None):
        self._clear(self.choice)
        self.name=label;self.character=state;self.targets=targets;self.evidence=evidence
        n=state['NORMAL'];t=state['TRANSFORM']
        a=rank(n['level'])
        summary=[f'PERSONAGEM: {label}',f'Rank: {a[2]} {a[1]}★ | nível {n["level"]}',
                 f'Raça: {n["race"]}',
                 'Atributos: '+', '.join(f'{k}={v}' for k,v in n['attrs'].items()),
                 f'Vida: {n["hp_current"]}/{n["hp_max"]}   Alma: {n["pa_current"]}/{n["pa_max"]}',
                 f'CA: {n["derived"]["ca"]}   FF: {n["derived"]["ff"]}   CD: {n["derived"]["magic_cd"]}',
                 f'Espírito (hipotético): {t["activation_state"]}',
                 f'Pontos normais por nível: {n["normal_rate"]}',
                 'Transformação NÃO será ativada.',
                 '', 'Equipamentos, técnicas e títulos REAIS não são calculados nesta fixture.']
        if evidence:
            summary += ['','Origem: arquivo JSON fictício declarado — não autenticação independente.',
                        'SHA bruto: '+evidence['original_bytes_sha256'],
                        'Atributos extras originais preservados byte a byte.']
        self._set_text(self.info,'\n'.join(summary))
        self._set_text(self.preview_text,'Prévia ainda não calculada. Faça suas escolhas primeiro.')
        self._label('2. ESCOLHA O DESTINO',True)
        opt={str(x):f'{rank(x)[2]} {rank(x)[1]}★ — nível {x}' for x in targets}
        self.target_value=tk.StringVar(value=str(targets[0]))
        for value,label in opt.items():
            ttk.Radiobutton(self.choice,text=label,variable=self.target_value,value=value).pack(anchor='w',pady=7)
        self._button(self.choice,'Começar evolução experimental',self.start_session,strong=True)
        self.status.set('Personagem fictício escolhido. O próximo passo exige confirmação de níveis.')
        self.tabs.select(self.info)

    def start_session(self):
        try:
            self.session=LocalSession(self.name,self.character,int(self.target_value.get()),
                                       source_evidence=self.evidence)
        except Exception as exc:
            messagebox.showerror('HOLD / início',str(exc));return
        self._set_text(self.history,'Pasta de execução isolada:\n'+str(self.session.folder)+
                       '\n\nO estado inicial foi salvo, mas nenhuma evolução foi aplicada.')
        self.render_question()

    def render_question(self):
        s=self.session
        d=s.dialogue
        self._clear(self.choice)
        phase=d.phase
        self.phase=phase
        self._label('ETAPA: '+phase,True)
        if phase=='HOLD':
            self._label('HOLD do motor: '+str(d.blocker))
            self._button(self.choice,'Encerrar sem aplicar',self.cancel)
            return
        if phase=='READY':
            self._label('CONFIRMO recebido. A cópia ainda aguarda commit local.')
            self._button(self.choice,'Aplicar na CÓPIA LOCAL',self.apply,strong=True)
            self._button(self.choice,'Cancelar antes de aplicar',self.cancel)
            return
        self._label(d.prompt())
        if phase in ('TARGET','ROLLS'):
            buttons={'TARGET':[('Confirmar níveis apenas neste TESTE','CONFIRMO_NIVEIS'),
                               ('Níveis divergentes: bloquear','REVISAR_NIVEIS')],
                     'ROLLS':[('Rolar dados no motor R17','ROLAR_AGORA'),
                              ('Corrigir escolhas, se permitido','CORRIGIR')]}[phase]
            for label,value in buttons:
                self._button(self.choice,label,lambda v=value:self.answer(v),strong=value.endswith('NIVEIS') or value=='ROLAR_AGORA')
        elif phase=='RATE':
            self._label('Taxa encontrada na cópia: '+str(d.state['NORMAL']['normal_rate']))
            self._button(self.choice,'Confirmar taxa indicada na cópia',
                         lambda:self.answer(d.state['NORMAL']['normal_rate']),strong=True)
            self._label('Se a taxa da ficha estiver incorreta, cancele e reconcilie a fonte.')
        elif phase=='MODE':
            self._mode_list({
                'Fixo Vida e Alma (contrato R17)':'FIXO',
                'Rolar Vida e Alma (recibos)':'ROLAR',
                'Rolar Vida / Alma fixa':'HP_ROLL',
                'Vida fixa / rolar Alma':'PA_ROLL'})
        elif phase in ('NORMAL','SPIRIT'):
            normal,spirit=d._budget(d.cursor)
            budget=normal if phase=='NORMAL' else spirit
            allowed=ATTRS if phase=='NORMAL' else d.state['TRANSFORM']['spirit']['allowed_attrs']
            self._label(f'Pontos neste nível: {budget} | Nível {d.cursor}')
            if phase=='SPIRIT':self._label('Pontos espirituais hipotéticos. Bronze: forma NÃO ativável.')
            form=tk.Frame(self.choice,bg='white');form.pack(fill='x',pady=5)
            self.entry_vars=[]
            for i,k in enumerate(allowed):
                row=tk.Frame(form,bg='white');row.pack(fill='x',pady=1)
                tk.Label(row,text=k,width=9,anchor='w',bg='white').pack(side='left')
                v=tk.StringVar(value='0')
                ttk.Spinbox(row,from_=0,to=budget,textvariable=v,width=8).pack(side='left')
                self.entry_vars.append((k,v))
            self._button(self.choice,'Validar distribuição no motor',self.submit_allocation,strong=True)
        elif phase in ('FF','CONDITIONAL'):
            if phase=='FF':
                self._mode_list({'Bônus de dano (conforme motor)':'DANO',
                                 'Bônus de CA (conforme motor)':'CA',
                                 'Bônus de Vida (conforme motor)':'VIDA'})
            else:
                options=d._contracts(d.cursor)[d._conditional_index]['options']
                self._mode_list({x:x for x in options})
        elif phase=='CONFIRM':
            try:report=s.preview()
            except Exception as exc:
                messagebox.showerror('HOLD prévia',str(exc));self.cancel();return
            self._set_text(self.preview_text,report)
            self.tabs.select(self.preview_text)
            self._label('Leia a aba Antes x Depois. NADA FOI APLICADO.')
            self._button(self.choice,'CONFIRMO a evolução só na cópia',self.confirm,strong=True)
            self._button(self.choice,'Corrigir escolhas (motor decide se permite)',lambda:self.answer('CORRIGIR'))
        self._button(self.choice,'Cancelar sem aplicar',self.cancel)

    def _mode_list(self,options):
        self.option_var=tk.StringVar(value=list(options.values())[0])
        for text,value in options.items():
            ttk.Radiobutton(self.choice,text=text,variable=self.option_var,value=value).pack(anchor='w',pady=6)
        self._button(self.choice,'Continuar',lambda:self.mode_answer(self.option_var.get()),strong=True)

    def mode_answer(self,value):
        if self.phase=='MODE':
            if value=='HP_ROLL':value={'VIDA':'ROLAR','ALMA':'FIXO'}
            elif value=='PA_ROLL':value={'VIDA':'FIXO','ALMA':'ROLAR'}
        self.answer(value)

    def submit_allocation(self):
        try:
            vals={k:int(v.get()) for k,v in self.entry_vars}
            if any(x<0 for x in vals.values()):raise ValueError('Pontos devem ser não negativos')
            self.answer(vals)
        except ValueError as e:
            messagebox.showwarning('Valor inválido',str(e)+'\nNenhum ponto foi consumido.')

    def answer(self,value):
        try:
            new=self.session.respond(value)
        except Exception as e:
            messagebox.showwarning('Escolha não aceita pelo motor',str(e)+'\nNenhuma evolução aplicada.')
            self.status.set('Resposta bloqueada: '+str(e))
            self.render_question()
            return
        if new=='HOLD':
            messagebox.showwarning('HOLD',str(self.session.dialogue.blocker)+'\nSem aplicação.')
        self.status.set('Pergunta aceita pelo motor. Etapa seguinte: '+new)
        self.render_question()

    def confirm(self):
        if not messagebox.askyesno('Confirmar apenas cópia local',
                'Você conferiu a aba ANTES x DEPOIS?\n\n'
                'A alteração será SOMENTE na cópia fictícia local, nunca no Notion.\n\nConfirmar?'):
            return
        self.answer('CONFIRMO')

    def apply(self):
        if not messagebox.askyesno('Última confirmação','Aplicar o plano já confirmado somente no experimento local?'):
            return
        try:
            receipt=self.session.commit()
            view=read_run(self.session.folder)
            self._set_text(self.preview_text,view['comparison'])
            self._set_text(self.info,'APLICAÇÃO EXPERIMENTAL CONCLUÍDA E REABERTA DO DISCO\n\n'+
                           json.dumps(receipt,ensure_ascii=False,indent=2))
            self._set_text(self.history,'RECIBO\n'+json.dumps(receipt,ensure_ascii=False,indent=2)+
                           '\n\nPasta: '+str(self.session.folder))
            self._clear(self.choice)
            self._label('Evolução confirmada na CÓPIA. O que deseja fazer?',True)
            self._button(self.choice,'Manter e fechar (reabrir mais tarde)',self.home,strong=True)
            self._button(self.choice,'Restaurar estado anterior agora',self.restore_current)
            self.status.set('COMMIT local e READBACK validados. Nenhum Notion alterado.')
            self.tabs.select(self.preview_text)
        except Exception as exc:
            messagebox.showerror('HOLD — não repita o evento',str(exc)+'\nConfira a pasta da execução.')
            self.status.set('HOLD efeito desconhecido; não repetir.')

    def cancel(self):
        if self.session:
            try:self.session.cancel()
            except Exception as e:
                messagebox.showwarning('HOLD: verificar possível efeito',str(e));return
        self.home()
        self.status.set('Cancelado antes de aplicar. Recibo local preservado.')

    def restore_current(self):
        if not self.session:return
        self.restore_chosen(self.session.folder)

    def restore_chosen(self, folder):
        if not messagebox.askyesno('Restaurar cópia',
                                   'Restaurar o estado ANTERIOR somente nesta cópia local?'):
            return
        try:
            r=restore_folder(folder)
            messagebox.showinfo('Restauração verificada','Estado original recuperado, recibo atualizado.')
            self.show_sessions()
        except Exception as exc:
            messagebox.showerror('HOLD sem reexecução',str(exc))

    def show_sessions(self):
        if self.session and not self.session.committed:
            try:
                self.session.cancel('SAIDA_PARA_HISTORICO')
            except LocalHold as exc:
                messagebox.showwarning('HOLD',str(exc))
                return
        self._top()
        self._clear(self.choice)
        self.session=None
        runs=list_runs()
        self._label('SESSÕES SALVAS',True)
        if not runs:
            self._label('Ainda não há sessões confirmadas.')
            self._set_text(self.history,'Nenhuma sessão confirmada disponível.')
            return
        self.listbox=tk.Listbox(self.choice,height=min(11,len(runs)),font=('Segoe UI',9))
        self.listbox.pack(fill='x',pady=10)
        for folder,r in runs:
            self.listbox.insert('end',folder.name+' • '+r.get('character','sem personagem')[:22])
        self.listbox.selection_set(0)
        self.runs=runs
        self._button(self.choice,'Ver estado e recibo',self.inspect_selected,strong=True)
        self._button(self.choice,'Restaurar sessão selecionada',self.restore_selected)
        self._label('Recibo, plano e WAL são conferidos antes de exibir ou restaurar.')
        self._set_text(self.info,'Selecione uma sessão e clique VER ESTADO.')
        self._set_text(self.history,'Sessões: '+str(len(runs))+'\nNenhuma ficha oficial foi consultada.')

    def _selected(self):
        selection=self.listbox.curselection()
        return self.runs[selection[0]][0] if selection else None

    def inspect_selected(self):
        folder=self._selected()
        if not folder:return
        try:
            view=read_run(folder)
            self._set_text(self.preview_text,view['comparison'])
            self._set_text(self.history,json.dumps(view['receipt'],ensure_ascii=False,indent=2)+
                           '\n\nEstado atual persistido:\n'+
                           json.dumps(view['current'],ensure_ascii=False,indent=2))
            self.tabs.select(self.preview_text)
            self.status.set('Sessão recuperada do disco; recibo e WAL validados.')
        except Exception as exc:
            messagebox.showerror('HOLD / integridade',str(exc))

    def restore_selected(self):
        folder=self._selected()
        if folder:self.restore_chosen(folder)


def main():
    window=tk.Tk()
    try:
        style=ttk.Style(window)
        if 'clam' in style.theme_names():style.theme_use('clam')
        style.configure('TRadiobutton',font=('Segoe UI',10),background='white')
    except Exception:pass
    LevelUpWindow(window)
    window.mainloop()

if __name__=='__main__':
    try:main()
    except Exception as exc:
        # Fails closed; batch wrapper preserves diagnostics on console.
        print('HOLD: interface indisponível:',type(exc).__name__,str(exc),file=sys.stderr)
        raise

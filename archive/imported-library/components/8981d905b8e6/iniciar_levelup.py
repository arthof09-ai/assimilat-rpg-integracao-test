#!/usr/bin/env python3
"""Interface humana (terminal) para DialogueR17 existente. APENAS CÓPIA EXPERIMENTAL.

Não contém regras mecânicas, integração Notion, publicação Party ou autoaprovação.
O controlador, planejador, RNG e rollback são importados sem alterações do R27.
"""
from __future__ import annotations

import copy
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parent
ENGINE_ROOT = APP_ROOT / 'engine_r17_existing_r27'
if not ENGINE_ROOT.is_dir():
    raise SystemExit('Motor R27 não encontrado ao lado da interface. Reextraia o pacote integral.')
sys.path.insert(0, str(ENGINE_ROOT))

from win_filelock_compat import install_windows_flock  # compatibilidade SEM editar motor R17/R27
install_windows_flock()

from dialogue_r17 import DialogueR17, DialogueR17Hold  # noqa: E402
from engine_r13 import ATTRS, rank                        # noqa: E402
from engine_r17 import bronze1_fixture, validate_r17     # noqa: E402
from r16_gate import prata_fixture                        # noqa: E402
from roll_ledger_r17 import RollLedger                     # noqa: E402
from durable_r14 import DurableStore, DurableController, _atomic_json        # noqa: E402
from safe_runner_r17 import SafeLocalR17Runner            # noqa: E402
from r10_recovery import digest                           # noqa: E402
from adaptador_copia_local import import_local, ImportHold, RealSourceHold, quarantine_real  # noqa: E402


class CancelledByUser(Exception):
    pass


def say(msg=''):
    print(msg, flush=True)


def ask(label: str) -> str:
    try:
        return input(label).strip()
    except (EOFError, KeyboardInterrupt):
        say('\nEntrada interrompida.')
        raise CancelledByUser('entrada humana interrompida')


def pick(title: str, options: dict[str, str], *, allow_cancel=True) -> str:
    while True:
        say('\n' + title)
        for key, description in options.items():
            say(f'  {key}) {description}')
        if allow_cancel:
            say('  0) Cancelar sem evoluir')
        v = ask('Sua escolha: ').strip().upper()
        if allow_cancel and v in ('0', 'CANCELAR', 'SAIR'):
            raise CancelledByUser('cancelamento explícito')
        if v in options:
            return v
        say('Escolha inválida: use uma das opções exibidas.')


def menu_character():
    v = pick('QUAL PERSONAGEM EXPERIMENTAL?', {
        '1': 'Exemplo fictício Humano, Bronze 1 (sem transformação)',
        '2': 'Exemplo fictício Humano, Prata 1 (Espírito HIPOTÉTICO, inativo)',
        '3': 'Restaurar uma evolução experimental MANTIDA anteriormente',
        '4': 'Carregar cópia JSON local (somente fictícia validada; real = HOLD)',
    })
    if v == '3':
        return ('RESTAURAR_COPIA_EXISTENTE', None, None, None)
    if v == '4':
        file_name = ask('Nome do arquivo em fichas_locais (ex.: exemplo_ficticio.json): ')
        try:
            state, evidence = import_local(file_name, APP_ROOT)
        except RealSourceHold as e:
            saved = quarantine_real(e.evidence, APP_ROOT)
            say('IMPORTAÇÃO REAL EM QUARENTENA (SEM EVOLUIR): ' + str(saved))
            say('HOLD: falta conciliação da fonte real, R22 e autorização de uso.')
            return ('HOLD_IMPORTACAO', None, None, None)
        except ImportHold as e:
            say('IMPORTAÇÃO EM HOLD, nenhum commit: ' + str(e))
            return ('HOLD_IMPORTACAO', None, None, None)
        current = state['NORMAL']['level']
        # Nenhum grant automático. Um único nível adjacente, sempre escolhido e confirmado.
        from engine_r13 import RANKS
        next_level = current + 1
        if next_level > len(RANKS)*5:
            say('HOLD: não há nível posterior conhecido.')
            return ('HOLD_IMPORTACAO', None, None, None)
        return ('COPIA_FICTICIA_IMPORTADA_'+file_name, state, (next_level,), evidence)
    if v == '1':
        return ('EXEMPLO_FICTICIO_BRONZE_1', bronze1_fixture(), (2, 6), None)
    silver = prata_fixture()
    silver['TRANSFORM']['spirit']['cap'] = 7  # Mesmo cenário hipotético R25: cap7.
    validate_r17(silver)
    return ('EXEMPLO_FICTICIO_PRATA_1_CAP7', silver, (7, 8), None)


def show_character(label, state):
    n = state['NORMAL']; t = state['TRANSFORM']; normal_rank = rank(n['level'])[2]
    say('\n' + '=' * 63)
    say(f'FICHA ISOLADA: {label} — {normal_rank} {rank(n["level"])[1]}★ / nível ordinal {n["level"]}')
    say('RAÇA: ' + n['race'] + ' | ATRIBUTOS: ' + ', '.join(f'{k}={n["attrs"][k]}' for k in ATTRS))
    say(f'VIDA {n["hp_current"]}/{n["hp_max"]} | ALMA/PA {n["pa_current"]}/{n["pa_max"]} | '
        f'CA {n["derived"]["ca"]} | FF {n["derived"]["ff"]} | CD {n["derived"]["magic_cd"]}')
    say(f'ESPÍRITO: {t["activation_state"]} | ativação NÃO executada')
    say(f'Pontos normais por nível (contrato desta cópia): {n["normal_rate"]}')
    say('AVISO: fixture fictícia e versão local; nenhum dado foi lido do Notion.')
    if n['level'] < 6:
        say('Bronze 1–5: Transformação Demoníaca PROIBIDA. TAP pré-Prata é hipótese isolada.')
    else:
        say('Dados e BAP do Espírito são HIPOTÉTICOS; não valem para nenhuma player.')
    say('=' * 63)


def choose_target(level, available):
    opts = {str(v): (f'{rank(level)[2]} {rank(level)[1]}★ → '
                       f'{rank(v)[2]} {rank(v)[1]}★ (nível ordinal {v})') for v in available}
    k = pick('ESCOLHA A EVOLUÇÃO SUPORTADA:', opts)
    return int(k)


def parse_allocation(raw: str, allowed: list[str]):
    """Adapter textual only: no budget or game calculations; DialogueR17 validates."""
    raw = raw.strip().upper()
    if not raw:
        raise ValueError('Escreva ao menos um atributo, por exemplo: INT=2')
    result = {}
    for segment in raw.replace(';', ',').split(','):
        pieces = segment.strip().replace(':', '=').split('=')
        if len(pieces) != 2:
            raise ValueError('Formato inválido. Exemplo: FOR=1, DES=1')
        key, val = (p.strip() for p in pieces)
        if key not in allowed:
            raise ValueError(f'Atributo {key!r} não disponível; use {", ".join(allowed)}')
        if key in result:
            raise ValueError(f'Atributo {key} foi informado duas vezes.')
        if not val.isdecimal():
            raise ValueError('Informe apenas números inteiros não negativos.')
        result[key] = int(val)
    return result


def human_answer(d):
    ph = d.phase
    if ph == 'TARGET':
        return {'1': 'CONFIRMO_NIVEIS', '2': 'REVISAR_NIVEIS'}[
            pick(d.prompt(), {'1': 'Confirmar concessão apenas neste TESTE',
                              '2': 'Suspender para revisão de níveis'})]
    if ph == 'RATE':
        say('\n' + d.prompt())
        while True:
            raw = ask('Pontos por nível, conforme cópia: ')
            if raw.upper() in ('CANCELAR', 'SAIR'):
                raise CancelledByUser('cancelado na conferência da taxa')
            if raw.isdecimal() and int(raw) > 0:
                return int(raw)
            say('Use um número inteiro positivo, por exemplo 2.')
    if ph == 'MODE':
        return {'1': 'FIXO', '2': 'ROLAR',
                '3': {'VIDA': 'ROLAR', 'ALMA': 'FIXO'},
                '4': {'VIDA': 'FIXO', 'ALMA': 'ROLAR'}}[
            pick(d.prompt(), {
                '1': 'VIDA FIXO 60% / ALMA FIXO 60%',
                '2': 'VIDA ROLAR / ALMA ROLAR (recibos auditáveis)',
                '3': 'VIDA ROLAR / ALMA FIXO 60%',
                '4': 'VIDA FIXO 60% / ALMA ROLAR'})]
    if ph in ('NORMAL', 'SPIRIT'):
        allowed = list(ATTRS if ph == 'NORMAL' else d.state['TRANSFORM']['spirit']['allowed_attrs'])
        say('\n' + d.prompt())
        say('Formato: INT=2 ou FOR=1,DES=1 (atributos omitidos recebem 0).')
        while True:
            raw = ask('Distribuição (ou CANCELAR): ')
            if raw.upper() in ('CANCELAR', 'SAIR'):
                raise CancelledByUser('distribuição cancelada')
            try:
                return parse_allocation(raw, allowed)
            except ValueError as e:
                say(f'Entrada inválida: {e}')
    if ph == 'FF':
        return {'1': 'DANO', '2': 'CA', '3': 'VIDA'}[
            pick(d.prompt(), {'1': 'DANO +1d4', '2': 'CA +1d4', '3': 'VIDA +2d6'})]
    if ph == 'CONDITIONAL':
        c = d._contracts(d.cursor)[d._conditional_index]  # somente apresentação
        return c['options'][int(pick(d.prompt(), {
            str(i + 1): option for i, option in enumerate(c['options'])})) - 1]
    if ph == 'ROLLS':
        return {'1': 'ROLAR_AGORA', '2': 'CORRIGIR'}[
            pick(d.prompt(), {'1': 'Rolar com recibo DURÁVEL do motor existente',
                              '2': 'Voltar às escolhas, sem rolar'})]
    if ph == 'CONFIRM':
        say('\n' + d.prompt())
        show_preview(d._preview())  # calculado pelo planejador original (sem commit)
        return {'1': 'CONFIRMO', '2': 'CORRIGIR'}[
            pick('A PRÉVIA NÃO FOI APLICADA. Confirmar?',
                 {'1': 'CONFIRMO — aplicar apenas na cópia local',
                  '2': 'Revisar escolhas e refazer prévia'})]
    raise RuntimeError('Fase de diálogo desconhecida: ' + ph)


def show_preview(plan):
    old = plan['before']; new = plan['updates']
    a = old['NORMAL']; b = new['NORMAL']
    say('\n' + '-' * 63)
    say('PRÉVIA GERADA PELO MOTOR (nenhuma gravação local ainda)')
    say(f'NÍVEL: {a["level"]} → {b["level"]}')
    for k in ATTRS:
        if a['attrs'][k] != b['attrs'][k]:
            say(f'{k}: {a["attrs"][k]} → {b["attrs"][k]}')
    for label, key in [('VIDA máxima', 'hp_max'), ('VIDA atual', 'hp_current'),
                       ('ALMA máxima', 'pa_max'), ('ALMA atual', 'pa_current')]:
        say(f'{label}: {a[key]} → {b[key]}')
    for label, key in [('CA', 'ca'), ('FF', 'ff'), ('CD mágica', 'magic_cd')]:
        say(f'{label}: {a["derived"][key]} → {b["derived"][key]}')
    # Mostra diferenças espirituais em ficha MESTRE-SIDE apenas, como HIPÓTESE.
    old_t, new_t = old['TRANSFORM'], new['TRANSFORM']
    if old_t['overlay'] != new_t['overlay']:
        say('Espírito (HIPÓTESE local, forma inativa):')
        for k in ATTRS:
            if old_t['overlay'][k] != new_t['overlay'][k]:
                say(f'  {k}: {old_t["overlay"][k]} → {new_t["overlay"][k]}')
    for step in plan['steps']:
        growth = step['growth']
        say(f'Nível {step["level"]}: Vida +{growth["NORMAL_HP"]["sum"]}; '
            f'Alma +{growth["NORMAL_PA"]["sum"]}; '
            f'Espírito capped={step["spirit_capped"]} (hipótese).')
    say('Transformação: NÃO ativada; nenhuma cura automática por subir de nível.')
    say('-' * 63)


def save(path, value):
    _atomic_json(path, value)  # mesma escrita atômica local do R14; sem Notion


def audit_rolls(d):
    for rid, r in d.choices['roll_receipts'].items():
        RollLedger.verify(r)
        say(f'DADO AUDITÁVEL [{r["spec"]["purpose"]}]: {r["rolls"]} '
            f'= {r["sum"]} | SHA do recibo {r["receipt_sha256"][:16]}…')


def finish_cancel(directory, store, original, transcript, reason, d=None):
    # Não atribui "cancelamento sem gravação" se algum evento foi aplicado.
    current = store.get_all()
    if store.event(d.event_id) if d else False:
        status = 'HOLD_VERIFICAR_EFEITO_EXISTENTE'
    else:
        status = 'CANCELADO_SEM_APLICACAO'
    receipt = {'schema': 'LEVELUP-HUMAN-CLI-V1', 'status': status,
               'reason': reason, 'initial_state_digest': digest(original),
               'readback_digest': digest(current), 'untouched': current == original,
               'transcript': transcript, 'notion_writes': 0, 'party_writes': 0,
               'production_certified': False}
    save(directory / 'RECIBO_CANCELAMENTO.json', receipt)
    say(f'\n{status} | ficha local intacta = {current == original}')
    say('Recibo: ' + str(directory / 'RECIBO_CANCELAMENTO.json'))
    return 0 if current == original else 2



def restore_previous():
    """Reabre cópia local previamente aplicada; usa o rollback ORIGINAL do R14."""
    runs = APP_ROOT / 'execucoes'
    candidates = []
    for p in sorted(runs.glob('*'), reverse=True) if runs.exists() else []:
        f = p / 'RECIBO_EVOLUCAO.json'
        if not f.is_file():
            continue
        try:
            receipt = json.loads(f.read_text(encoding='utf-8'))
        except (ValueError, OSError):
            continue
        if receipt.get('status') in ('EVOLUIDO_MANTIDO_EM_COPIA_LOCAL', 'COMMITTED_LOCAL_VERIFIED'):
            candidates.append((p, receipt))
    if not candidates:
        say('Não existe cópia local MANTIDA disponível para restauração.')
        return 0
    choices = {str(i + 1): f'{p.name} | {r["character"]} → nível {r["target_level"]}'
               for i, (p, r) in enumerate(candidates)}
    try:
        selected = int(pick('ESCOLHA QUAL CÓPIA RESTAURAR (NUNCA NOTION):', choices)) - 1
        folder, receipt = candidates[selected]
        before = json.loads((folder / 'ESTADO_INICIAL.json').read_text(encoding='utf-8'))
        after = json.loads((folder / 'ESTADO_APLICADO.json').read_text(encoding='utf-8'))
        store = DurableStore(folder / 'COPIA_LOCAL_3_DOCS')
        event = store.event(receipt['event_id'])
        if (not event or event['state'] != 'COMMITTED'
                or digest(before) != receipt['before_sha256']
                or digest(after) != receipt['after_sha256']
                or digest(store.get_all()) != receipt['after_sha256']
                or event['intent_hash'] != receipt['after_sha256']):
            say('HOLD: recibo, WAL ou cópia atual não coincidem. Não alterar.')
            return 2
        answer = pick('O estado atual corresponde ao recibo. Deseja restaurar?',
                      {'1': 'SIM, RESTAURAR esta cópia local pelo rollback R14',
                       '2': 'NÃO, manter como está'}, allow_cancel=False)
        if answer == '2':
            say('Cópia mantida, nenhuma modificação.')
            return 0
        rollback = DurableController(store).explicit_rollback(receipt['event_id'])
        reopened = DurableStore(folder / 'COPIA_LOCAL_3_DOCS').get_all()
        if (rollback['state'] != 'COMMITTED' or digest(reopened) != receipt['before_sha256']
                or reopened != before):
            say('HOLD: restauração não passou no readback.')
            return 2
        save(folder / 'ESTADO_RESTAURADO.json', reopened)
        receipt.update(status='EVOLUIDO_E_RESTAURADO_LOCAL',
                       rollback='ROLLED_BACK_VERIFIED_LOCAL_BY_REOPEN',
                       rollback_sha256=digest(reopened), rollback_exact=True)
        save(folder / 'RECIBO_EVOLUCAO.json', receipt)
        say('ROLLBACK POSTERIOR VERIFICADO: estado original restaurado na mesma cópia.')
        say('Recibo: ' + str(folder / 'RECIBO_EVOLUCAO.json'))
        return 0
    except CancelledByUser:
        say('Nenhuma alteração realizada.')
        return 0
    except (KeyError, ValueError, OSError) as exc:
        say('HOLD: falha na conferência da cópia local. ' + str(exc))
        return 2


def run():
    say('\n=== LEVEL-UP INTERATIVO DO MESTRE — TESTE ISOLADO ===')
    say('O MOTOR É O R17 EXISTENTE. Não acessa Notion/Party; não evolui personagens reais.')
    try:
        name, fixture, target_options, source_evidence = menu_character()
        if name == 'HOLD_IMPORTACAO':
            return 2
        if name == 'RESTAURAR_COPIA_EXISTENTE':
            return restore_previous()
        validate_r17(fixture)
        show_character(name, fixture)
        target = choose_target(fixture['NORMAL']['level'], target_options)
    except CancelledByUser:
        say('Cancelado antes de criar qualquer cópia.')
        return 0

    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + secrets.token_hex(5)
    directory = APP_ROOT / 'execucoes' / run_id
    directory.mkdir(parents=True, exist_ok=False)
    event_id = 'SIM-UI-' + secrets.token_hex(12)
    original = copy.deepcopy(fixture)
    save(directory / 'ESTADO_INICIAL.json', original)
    if source_evidence:
        # Prova material: cópia byte-exata do arquivo de entrada original e
        # envelope independente dos campos não editados pelo motor R17.
        from hashlib import sha256
        source_path=directory/'SNAPSHOT_ORIGINAL_IMUTAVEL.json'
        source_path.write_bytes(source_evidence['original_raw_bytes'])
        if sha256(source_path.read_bytes()).hexdigest()!=source_evidence['original_bytes_sha256']:
            raise RuntimeError('HOLD: arquivo de origem não persistiu idêntico')
        save(directory/'PROVENIENCIA_COPIA.json', {k:v for k,v in source_evidence.items()
             if k not in ('original_raw_bytes','snapshot')})
    store = DurableStore(directory / 'COPIA_LOCAL_3_DOCS', original)
    ledger = RollLedger(directory / 'RECIBOS_DADOS')
    transcript = []
    d = None
    try:
        d = DialogueR17(copy.deepcopy(original), target, event_id, ledger)
        say('\nExecução experimental: ' + str(directory))
        say('Digite 0 nos menus ou CANCELAR na distribuição para desistir.')
        while d.phase not in ('READY', 'HOLD'):
            phase = d.phase
            question = d.prompt()
            response = human_answer(d)
            try:
                d.respond(response)
            except (DialogueR17Hold, ValueError) as e:
                transcript.append({'phase': phase, 'question': question,
                                   'response': response, 'accepted': False, 'error': str(e)})
                say('RESPOSTA REJEITADA PELO MOTOR: ' + str(e))
                if d.phase == 'HOLD':
                    break
                continue
            transcript.append({'phase': phase, 'question': question,
                               'response': response, 'accepted': True, 'phase_after': d.phase})
            if phase in ('FF', 'ROLLS'):
                audit_rolls(d)

        if d.phase == 'HOLD':
            return finish_cancel(directory, store, original, transcript,
                                 'HOLD do controlador: ' + str(d.blocker), d)
        # O diálogo chegou a READY somente por CONFIRMO explícito.
        plan = d.executable_plan()
        save(directory / 'PREVIA_MOTOR.json', plan)
        runner = SafeLocalR17Runner(store)
        before_hash = digest(original)
        result = runner.execute(d)
        after = store.get_all()
        # Reabrir do DISCO, não confiar apenas no retorno de execute().
        reopened = DurableStore(directory / 'COPIA_LOCAL_3_DOCS')
        validated = validate_r17(reopened.get_all())
        after_hash = digest(reopened.get_all())
        if (result['status'] != 'COMMITTED_LOCAL_VERIFIED' or not validated
                or after != plan['updates'] or after_hash != digest(plan['updates'])):
            raise RuntimeError('HOLD: readback/planos discordam. Não repetir execução.')
        save(directory / 'ESTADO_APLICADO.json', after)
        if source_evidence:
            # Conserva todo o conteúdo original, estruturado e bruto, e inclui
            # a projeção R17 isolada. NÃO aplica delta aos blocos da ficha.
            save(directory/'PROJECAO_SEM_REESCREVER_FICHA.json', {
                'schema':'LEVELUP-COPIA-PROJECAO-V1', 'snapshot_original':source_evidence['snapshot'],
                'snapshot_sha256':source_evidence['snapshot_sha256'],
                'engine_projection_before':original,'engine_projection_after':after,
                'notion_write':False,'requires_human_reconciliation':True})
        save(directory / 'TRANSCRICAO_ENTRADAS_EXPERIMENTAIS.json', transcript)
        save(directory / 'RECIBOS_ROLAGENS.json', d.choices['roll_receipts'])
        receipt = {'schema': 'LEVELUP-HUMAN-CLI-V1', 'character': name,
                   'scope': 'OFFLINE_FICTITIOUS_HUMAN_OPERABLE', 'status': result['status'],
                   'event_id': event_id, 'target_level': target,
                   'before_sha256': before_hash, 'after_sha256': after_hash,
                   'confirmation': 'CONFIRMO' if transcript[-1]['response'] == 'CONFIRMO' else 'FAIL',
                   'readback_equal_plan': True, 'rolled_receipts': len(d.choices['roll_receipts']),
                   'rollback': 'NAO_EXECUTADO', 'notion_writes': 0,
                   'party_writes': 0, 'production_certified': False}
        save(directory / 'RECIBO_EVOLUCAO.json', receipt)
        say('\n=== APLICAÇÃO EM CÓPIA LOCAL CONFIRMADA ===')
        say(f'COMMIT = {result["status"]} | READBACK = IDENTICO À PRÉVIA')
        say(f'SHA ANTES : {before_hash}\nSHA DEPOIS: {after_hash}')
        say('Recibo gravado: ' + str(directory / 'RECIBO_EVOLUCAO.json'))
        choice = pick('E AGORA?', {'1': 'RESTAURAR estado anterior (rollback verificável)',
                                   '2': 'MANTER a evolução na cópia experimental'},
                      allow_cancel=False)
        if choice == '1':
            rb = runner.rollback(d)
            again = DurableStore(directory / 'COPIA_LOCAL_3_DOCS').get_all()
            if rb['status'] != 'ROLLED_BACK_VERIFIED_LOCAL' or digest(again) != before_hash:
                raise RuntimeError('HOLD: rollback divergente; não repetir cegamente')
            save(directory / 'ESTADO_RESTAURADO.json', again)
            receipt.update(status='EVOLUIDO_E_RESTAURADO_LOCAL', rollback=rb['status'],
                           rollback_sha256=digest(again), rollback_exact=(again == original))
            say('\nROLLBACK CONFIRMADO — estado anterior recuperado byte-identicamente.')
        else:
            receipt.update(status='EVOLUIDO_MANTIDO_EM_COPIA_LOCAL',
                           rollback='DISPONIVEL_APENAS_NA_SESSAO_DE_CONFIRMACAO')
            say('\nEvolução MANTIDA somente nesta cópia local. Nenhum efeito no Notion.')
        save(directory / 'RECIBO_EVOLUCAO.json', receipt)
        say('Pasta: ' + str(directory))
        return 0
    except CancelledByUser as e:
        if d and d.phase == 'READY':
            # Se a pessoa interrompeu após CONFIRMO/commit, jamais mentir sobre o efeito.
            say('Interrupção após confirmação: confira RECIBO_EVOLUCAO e estado local; não repetir.')
            return 2
        return finish_cancel(directory, store, original, transcript, str(e), d)
    except Exception as e:
        save(directory / 'HOLD_VERIFICAR_ESTADO.json',
             {'error_type': type(e).__name__, 'description': str(e),
              'initial_digest': digest(original), 'current_digest': digest(store.get_all()),
              'event_id': event_id, 'automatic_retry': False, 'notion_writes': 0})
        say('\nHOLD — não refaça o mesmo evento. Verifique a pasta antes de recomeçar.')
        say(type(e).__name__ + ': ' + str(e))
        return 2


if __name__ == '__main__':
    sys.exit(run())

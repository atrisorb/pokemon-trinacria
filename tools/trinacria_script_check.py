#!/usr/bin/env python3
"""Pokemon Trinacria - controllo dei blocchi del Modulo 6 (script, banchi di testo, eventi, registro NPC).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia):
    python -I tools/trinacria_script_check.py check docs/MODULO_6/6.01_PROLOGO.json [--repo F:/Progetti/pokeheartgold]
    python -I tools/trinacria_script_check.py --selftest

Un blocco del Modulo 6 e' un JSON (indice, risorse, testi per il Glossario) piu' una cartella con i file
da copiare nel repository di pokeheartgold con lo stesso percorso relativo («cartella_file»). Il controllo
legge il JSON, la cartella, i registri del Modulo 2 e il repository di HeartGold (macro, costanti, linter).
Ultima riga stampata: SCRIPT_OK oppure SCRIPT_FAILED (con --selftest: SELFTEST_OK / SELFTEST_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>" (blocca) o "AVVISO <codice> ..." (non blocca).

Codici: J00 file illeggibile o mancante · J01 file dell'indice diverso dalla cartella (SHA-1) · J02 mappa o simboli
diversi dal registro 2.1-2.3 · J03 banco di testo malformato o gemello di altra lunghezza · J04 messaggio citato
dallo script ma assente · J05 messaggio mai usato · J06 macro sconosciuta o numero di argomenti sbagliato ·
J07 etichetta mancante, doppia o script senza fine · J08 ScrDef, header degli eventi e zone_event incoerenti ·
J09 flag, variabile o costante sconosciuta · J10 nome del giocatore senza BufferPlayersName (R-TXT-07) ·
J11 zone_event: sprite, casella, avvio o warp non validi · J12 riga del registro NPC diversa dall'evento ·
J13 intestazione o OnFrame dello script non coerente · J14 linter dei messaggi · J15 coppia campagna/gemello ·
J16 Glossario (parole siciliane) · J17 elenco «testi» diverso dai banchi.
"""
import argparse
import csv
import glob
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import trinacria_msg_lint as L          # noqa: E402
import trinacria_glossary_check as G    # noqa: E402

DEFAULT_REPOS = ['F:/Progetti/pokeheartgold', os.path.join(HERE, '..', '..', 'pokeheartgold')]
NPC_COLONNE = ['map_symbol', 'npc_id', 'x', 'y', 'sprite', 'msg_bank', 'msg_index', 'post_category', 'dialect_area',
               'ruolo', 'visibile', 'hide_flag', 'trainer_id', 'pokemon_species', 'accanto_a', 'codice_trama', 'note']
BRANCH_LAST = ('GoTo', 'GoToIfSet', 'GoToIfUnset', 'GoToIfEq', 'GoToIfNe', 'GoToIfLt', 'GoToIfGt', 'GoToIfLe', 'GoToIfGe',
               'GoToIfDefeated', 'GoToIfNotDefeated', 'GoToIfTrainerDefeated', 'Call')
TERMINATORI = ('End', 'GoTo', 'EndMovement')
PLAYER_NAME = '{STRVAR_1 3, 0, 0}'


class Report:
    def __init__(self, quiet=False):
        self.errors, self.warnings, self.quiet = [], [], quiet

    def err(self, code, where, msg):
        self.errors.append((code, where, msg))
        if not self.quiet:
            print('ERRORE %s %s: %s' % (code, where, msg))

    def warn(self, code, where, msg):
        self.warnings.append((code, where, msg))
        if not self.quiet:
            print('AVVISO %s %s: %s' % (code, where, msg))

    def codes(self):
        return sorted({e[0] for e in self.errors})


def load_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def find_repo(arg=None):
    for r in ([arg] if arg else []) + DEFAULT_REPOS:
        if r and os.path.isfile(os.path.join(r, 'include', 'constants', 'flags.h')):
            return os.path.normpath(r)
    return None


def defines(path, prefix=''):
    out = set()
    if os.path.isfile(path):
        for m in re.finditer(r'#define\s+(%s\w+)' % prefix, open(path, encoding='utf-8', errors='replace').read()):
            out.add(m.group(1))
    return out


# ----------------------------------------------------------------------------------------------
# Contesto: registri del Modulo 2 e costanti di HeartGold

class Ctx:
    def __init__(self, docs, repo):
        self.docs, self.repo = docs, repo
        self.maps = {}
        for f in sorted(glob.glob(os.path.join(docs, 'MODULO_2', '2.[123]_*.json'))):
            for m in load_json(f).get('mappe', []):
                self.maps[m['simbolo']] = m
        reg4 = load_json(glob.glob(os.path.join(docs, 'MODULO_2', '2.4_*.json'))[0])
        self.flags, self.vars = set(), set()
        for riga in reg4.get('file_trinacria_flags_h', {}).get('righe', []):
            self.flags.update(re.findall(r'#define\s+(FLAG_\w+)', riga))
        for riga in reg4.get('file_trinacria_vars_h', {}).get('righe', []):
            self.vars.update(re.findall(r'#define\s+(VAR_\w+)', riga))
        self.flags |= {e['simbolo'] for e in reg4['flag']['motore']} | {a['alias'] for a in reg4['flag']['alias_trama']}
        self.vars |= {e['simbolo'] for e in reg4['variabili']['motore']}
        reg5 = load_json(glob.glob(os.path.join(docs, 'MODULO_2', '2.5_*.json'))[0])
        self.sprites_trn = {s['simbolo'] for k in ('personaggi', 'classi') for s in reg5['sprite'].get(k, [])}
        self.badges = {d['alias'] for d in reg5['medaglie']['dossier']}
        self.hg = {}
        if repo:
            c = os.path.join(repo, 'include', 'constants')
            self.hg['flag'] = defines(os.path.join(c, 'flags.h'), 'FLAG_')
            self.hg['var'] = defines(os.path.join(c, 'vars.h'), 'VAR_')
            self.hg['species'] = defines(os.path.join(c, 'species.h'), 'SPECIES_')
            self.hg['sprite'] = defines(os.path.join(c, 'sprites.h'), 'SPRITE_')
            self.hg['seq'] = defines(os.path.join(c, 'sndseq.h'), 'SEQ_')
            self.hg['badge'] = defines(os.path.join(c, 'badge.h'), 'BADGE_')
            self.macros = parse_macros(repo)
        else:
            self.macros = None

    def known(self, sym):
        if sym.startswith('FLAG_'):
            return sym in self.flags or sym in self.hg.get('flag', ()) or (not self.repo and sym.startswith('FLAG_'))
        if sym.startswith('VAR_'):
            return sym in self.vars or sym in self.hg.get('var', ()) or (not self.repo and sym.startswith('VAR_'))
        if not self.repo:
            return True
        if sym.startswith('SPECIES_'):
            return sym in self.hg.get('species', ())
        if sym.startswith('BADGE_'):
            return sym in self.badges or sym in self.hg.get('badge', ())
        if sym.startswith('SEQ_'):
            return sym in self.hg.get('seq', ())
        return True

    def sprite_ok(self, sym):
        return sym in self.sprites_trn or sym in self.hg.get('sprite', ()) or not self.repo


def parse_macros(repo):
    out = {}
    for name in ('script.inc', 'movement.inc'):
        p = os.path.join(repo, 'asm', 'macros', name)
        if not os.path.isfile(p):
            continue
        for m in re.finditer(r'^\s*\.macro\s+(\w+)[ \t]*([^\n]*)$', open(p, encoding='utf-8', errors='replace').read(), re.M):
            params = [x.strip() for x in m.group(2).split(',') if x.strip()]
            req = sum(1 for x in params if '=' not in x and ':req' not in x or ':req' in x)
            out[m.group(1)] = (req, len(params), name == 'movement.inc')
    return out


# ----------------------------------------------------------------------------------------------
# Albero dei file del blocco

class Albero:
    def __init__(self, block, base, tmp):
        self.files = {}
        inline = block.get('file_inline')
        if inline:
            self.root = tmp
            for rel, text in inline.items():
                p = os.path.join(tmp, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'w', encoding='utf-8', newline='') as f:
                    f.write(text)
        else:
            self.root = os.path.join(base, block['cartella_file'])

    def path(self, rel):
        return os.path.join(self.root, rel)

    def read(self, rel):
        with open(self.path(rel), encoding='utf-8', newline='') as f:
            return f.read()

    def exists(self, rel):
        return os.path.isfile(self.path(rel))


# ----------------------------------------------------------------------------------------------
# Script .s

SYM_MSG = re.compile(r'\b(msg_\d{4}(?:_[A-Za-z0-9]+)?)_(\d{5})\b')


def parse_script(text):
    """Restituisce (istruzioni, etichette, chunks). Una istruzione = (riga, nome, [argomenti]); un chunk = (etichetta, [istruzioni])."""
    instrs, labels, chunks = [], {}, []
    cur = ['', []]
    for n, raw in enumerate(text.split('\n'), 1):
        line = raw.strip()
        if not line or line.startswith('#') or line.startswith('//'):
            continue
        m = re.match(r'^([A-Za-z_]\w*):$', line)
        if m:
            chunks.append(tuple(cur))
            cur = [m.group(1), []]
            labels.setdefault(m.group(1), []).append(n)
            continue
        if line.startswith('.'):
            continue
        name, _, rest = line.partition(' ')
        name = name.strip()
        if '\t' in name:
            name, _, rest = line.partition('\t')
        args = [a.strip() for a in rest.split(',')] if rest.strip() else []
        ins = (n, name, args)
        instrs.append(ins)
        cur[1].append(ins)
    chunks.append(tuple(cur))
    return instrs, labels, [c for c in chunks if c[1] or c[0]]


def check_script(rel, text, codice, banco, n_msg, ctx, rep, msgs_text, refs):
    where = rel
    instrs, labels, chunks = parse_script(text)
    m_inc = re.search(r'#include "msgdata/msg/(\w+)\.h"', text)
    if not m_inc or m_inc.group(1) != banco:
        rep.err('J02', where, '#include del banco: atteso %s, trovato %s' % (banco, m_inc.group(1) if m_inc else 'nessuno'))
    if '#include "fielddata/script/scr_seq/event_%s.h"' % codice not in text:
        rep.err('J02', where, 'manca #include di event_%s.h' % codice)
    for lab, lines in labels.items():
        if len(lines) > 1:
            rep.err('J07', where, 'etichetta %s definita %d volte' % (lab, len(lines)))
    scrdef = [a[0] for (_, nm, a) in instrs if nm == 'ScrDef' and a]
    script_labels = sorted(l for l in labels if re.match(r'^scr_seq_%s_\d{3}$' % codice, l))
    if scrdef != script_labels:
        rep.err('J08', where, 'ScrDef %s diverso dalle etichette degli script %s' % (scrdef, script_labels))
    if not any(nm == 'ScrDefEnd' for _, nm, _ in instrs):
        rep.err('J08', where, 'manca ScrDefEnd')
    # istruzioni
    for n, nm, args in instrs:
        if ctx.macros is not None:
            if nm not in ctx.macros:
                rep.err('J06', '%s:%d' % (where, n), 'istruzione sconosciuta «%s»' % nm)
                continue
            req, tot, _ = ctx.macros[nm]
            if not (req <= len(args) <= max(tot, req)):
                rep.err('J06', '%s:%d' % (where, n), '%s vuole %d-%d argomenti, ne ha %d' % (nm, req, tot, len(args)))
        for a in args:
            for sym in re.findall(r'\b(?:FLAG|VAR|SPECIES|BADGE|SEQ)_[A-Za-z0-9_]+', a):
                if not ctx.known(sym):
                    rep.err('J09', '%s:%d' % (where, n), 'simbolo sconosciuto %s' % sym)
        # destinazioni
        tgt = None
        if nm in BRANCH_LAST and args:
            tgt = args[-1]
        elif nm == 'Case' and len(args) == 2:
            tgt = args[1]
        elif nm == 'ApplyMovement' and len(args) == 2 and args[1].startswith('_'):
            tgt = args[1]
        if tgt is not None and tgt not in labels:
            rep.err('J07', '%s:%d' % (where, n), 'etichetta %s mancante' % tgt)
        if nm == 'MenuItemAdd' and args and args[0].isdigit():
            refs.add(int(args[0]))
    for m in SYM_MSG.finditer(text):
        b, i = m.group(1), int(m.group(2))
        if b != banco:
            rep.err('J04', where, 'messaggio %s_%s di un altro banco (atteso %s)' % (b, m.group(2), banco))
        elif i >= n_msg:
            rep.err('J04', where, 'messaggio %s_%05d: il banco ne ha %d' % (b, i, n_msg))
        else:
            refs.add(i)
    # catene: terminatori e nome del giocatore
    bymov = {c[0]: bool(c[1]) and c[1][-1][1] == 'EndMovement' for c in chunks}
    for k, (lab, ins) in enumerate(chunks):
        if not ins or not lab:
            continue
        ultimo = ins[-1][1]
        succ = chunks[k + 1] if k + 1 < len(chunks) else None
        is_mov = bymov.get(lab)
        if succ is None or bymov.get(succ[0]) or re.match(r'^scr_seq_%s_\d{3}$' % codice, succ[0] or ''):
            if ultimo not in TERMINATORI:
                rep.err('J07', where, 'lo script «%s» non finisce con End/GoTo/EndMovement (ultima istruzione %s)' % (lab or '(inizio)', ultimo))
        if not is_mov:
            buffered = False
            for n, nm, args in ins:
                if nm == 'BufferPlayersName':
                    buffered = True
                texts = []
                for a in args:
                    mm = SYM_MSG.fullmatch(a.strip())
                    if mm and mm.group(1) == banco and int(mm.group(2)) < n_msg:
                        texts.append(msgs_text[int(mm.group(2))])
                if any(PLAYER_NAME in t for t in texts) and not buffered:
                    rep.err('J10', '%s:%d' % (where, n), 'messaggio col nome del giocatore senza BufferPlayersName prima (R-TXT-07)')
    return labels, chunks


# ----------------------------------------------------------------------------------------------
# Controllo di un blocco

def check_block(block_path, repo, docs, rep, ctx=None):
    block = load_json(block_path)
    base = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(block_path)), '..', '..'))
    check_loaded(block, base, repo, docs, rep, block_path, ctx)


def check_loaded(block, base, repo, docs, rep, block_path=None, ctx=None):
    ctx = ctx or Ctx(docs, repo)
    if repo is None:
        rep.warn('J00', 'repository', 'pokeheartgold non trovato: macro, costanti e linter non controllati')
    tmp = tempfile.mkdtemp(prefix='trn_script_')
    try:
        alb = Albero(block, base, tmp)
        run(block, alb, ctx, rep, docs, repo, block_path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run(block, alb, ctx, rep, docs, repo, block_path):
    # J01: indice dei file
    for f in block.get('file_da_copiare', []):
        rel = f['percorso']
        if not alb.exists(rel):
            rep.err('J01', rel, 'file dell\'indice mancante nella cartella')
        elif f.get('sha1') and hashlib.sha1(open(alb.path(rel), 'rb').read().replace(b'\r\n', b'\n')).hexdigest() != f['sha1']:
            rep.err('J01', rel, 'SHA-1 (con fine riga LF) diverso da quello dell\'indice: rigenerare il blocco')
    charmap = L.load_charmap(repo) if repo else None
    widths = L.load_widths(repo) if repo else None
    testi_attesi = {}
    npc_rows = block.get('npc', [])
    for mp in block.get('mappe', []):
        sym = mp['simbolo']
        reg = ctx.maps.get(sym)
        where = sym
        if reg is None:
            rep.err('J02', where, 'mappa inesistente nei registri 2.1-2.3')
            continue
        banco, gem = reg['testi']['banco_campagna'], reg['testi']['gemello_post']
        codice = reg['codice_file_hg']
        sc = reg['script']
        att = {'banco_campagna': banco, 'gemello': gem, 'codice': codice,
               'script': os.path.basename(sc['file']), 'header_script': os.path.basename(sc['file_intestazione']),
               'eventi': os.path.basename(reg['eventi']['file'])}
        got = {'banco_campagna': mp['banco_campagna'], 'gemello': mp['gemello'], 'codice': mp['codice_file_hg'],
               'script': mp['file_script'].split('/')[-1], 'header_script': mp['file_header_script'].split('/')[-1],
               'eventi': mp['file_eventi'].split('/')[-1]}
        for k in att:
            if att[k] != got[k]:
                rep.err('J02', where, '%s: il registro dice %s, il blocco %s' % (k, att[k], got[k]))
        # banchi
        banks = {}
        for nome, rel in ((banco, mp['file_banco']), (gem, mp['file_gemello'])):
            if not alb.exists(rel):
                rep.err('J00', rel, 'banco mancante')
                banks[nome] = None
                continue
            try:
                d = json.loads(alb.read(rel))
            except ValueError as e:
                rep.err('J03', rel, 'JSON illeggibile: %s' % e)
                banks[nome] = None
                continue
            msgs = d.get('messages', [])
            for i, m in enumerate(msgs):
                if m.get('id') != '%s_%05d' % (nome, i):
                    rep.err('J03', rel, 'messaggio %d ha id %r invece di %s_%05d' % (i, m.get('id'), nome, i))
                    break
            if 'key' not in d:
                rep.err('J03', rel, 'manca "key"')
            banks[nome] = [L.message_text(m) for m in msgs]
            if charmap:
                prob = []
                L.lint_bank(alb.path(rel), charmap, widths, L.PROFILES['field'], prob)
                for p in prob:
                    rep.err('J14', rel, p.split(': ', 1)[-1])
        if banks.get(banco) is not None and banks.get(gem) is not None:
            if len(banks[banco]) != len(banks[gem]):
                rep.err('J15', where, '%s ha %d messaggi, %s ne ha %d' % (banco, len(banks[banco]), gem, len(banks[gem])))
            else:
                prob = []
                L.pair_check(alb.path(mp['file_banco']), alb.path(mp['file_gemello']), prob)
                for p in prob:
                    rep.err('J15', where, p)
            for i, t in enumerate(banks[banco]):
                testi_attesi['%s_%05d' % (banco, i)] = t
            for i, t in enumerate(banks[gem]):
                testi_attesi['%s_%05d' % (gem, i)] = t
        # script
        refs = set()
        n_msg = len(banks[banco]) if banks.get(banco) else 0
        for rel in (mp['file_script'], mp['file_header_script'], mp['file_event_h'], mp['file_eventi']):
            if not alb.exists(rel):
                rep.err('J00', rel, 'file mancante')
        if not alb.exists(mp['file_script']):
            continue
        txt = alb.read(mp['file_script'])
        labels, chunks = check_script(mp['file_script'], txt, codice, banco, n_msg, ctx, rep, banks.get(banco) or [], refs)
        if banks.get(banco):
            for i in range(n_msg):
                if i not in refs:
                    rep.err('J05', '%s_%05d' % (banco, i), 'messaggio mai usato dallo script')
        n_scr = len([l for l in labels if re.match(r'^scr_seq_%s_\d{3}$' % codice, l)])
        # intestazione (OnFrame)
        used_by_hdr = set()
        if alb.exists(mp['file_header_script']):
            h = alb.read(mp['file_header_script'])
            for _, nm, a in parse_script(h)[0]:
                if nm == 'InitScriptGoToIfEqual' and len(a) == 3:
                    if not ctx.known(a[0]):
                        rep.err('J09', mp['file_header_script'], 'variabile sconosciuta %s' % a[0])
                    mm = re.fullmatch(r'_EV_scr_seq_%s_(\d{3}) \+ 1' % codice, a[2])
                    if not mm or int(mm.group(1)) >= n_scr:
                        rep.err('J13', mp['file_header_script'], 'OnFrame verso uno script inesistente: %s' % a[2])
                    else:
                        used_by_hdr.add(int(mm.group(1)))
            if ctx.macros is not None:
                for n, nm, a in parse_script(h)[0]:
                    if nm not in ctx.macros:
                        rep.err('J06', mp['file_header_script'] + ':%d' % n, 'istruzione sconosciuta «%s»' % nm)
        # event_h e zone_event
        ev_ids = {}
        if alb.exists(mp['file_event_h']):
            eh = alb.read(mp['file_event_h'])
            evs = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'#define _EV_scr_seq_%s_(\d{3}) (\d+)' % codice, eh)}
            if sorted(evs) != list(range(n_scr)) or any(k != v for k, v in evs.items()):
                rep.err('J08', mp['file_event_h'], 'i _EV_ non sono 0..%d in ordine' % (n_scr - 1))
            objs_h = [(m.group(1), int(m.group(2))) for m in re.finditer(r'#define (obj_\w+) (\d+)', eh)]
            ev_ids = dict(objs_h)
        zone = None
        if alb.exists(mp['file_eventi']):
            zone = json.loads(alb.read(mp['file_eventi']))
        if zone is not None:
            check_zone(zone, mp, codice, n_scr, used_by_hdr, ev_ids, ctx, rep, reg, alb, txt, banco)
        # registro NPC
        rows = [r for r in npc_rows if r['map_symbol'] == sym]
        check_npc(rows, zone, mp, codice, banco, txt, rep)
    # J17: elenco «testi»
    testi = {t['id']: t for t in block.get('testi', [])}
    if set(testi) != set(testi_attesi):
        mancano = sorted(set(testi_attesi) - set(testi))[:4]
        troppi = sorted(set(testi) - set(testi_attesi))[:4]
        rep.err('J17', 'testi', 'elenco diverso dai banchi (mancano %s; in piu\' %s)' % (mancano, troppi))
    for i, t in testi.items():
        if i in testi_attesi and t.get('testo') != testi_attesi[i]:
            rep.err('J17', i, 'testo diverso dal banco')
    # J16: Glossario
    g3 = sorted(glob.glob(os.path.join(docs, 'MODULO_3', '3.*.json')))
    g3 = [p for p in g3 if os.path.basename(p) != '3.1_PIANO_INCONTRI.json']
    g6 = [p for p in sorted(glob.glob(os.path.join(docs, 'MODULO_6', '6.*.json')))
          if (block_path is None or os.path.abspath(p) != os.path.abspath(block_path)) and 'glossario_aggiunte' in load_json(p)
          and load_json(p).get('blocco') != block.get('blocco')]
    gr = G.Report(quiet=True)
    own = block_path if (block_path and 'file_inline' not in block) else None
    paths = g3 + g6
    tmpg = None
    if own is None:
        tmpg = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
        json.dump({'glossario_aggiunte': block.get('glossario_aggiunte', []), 'testi': block.get('testi', [])}, tmpg)
        tmpg.close()
        own = tmpg.name
    paths.append(own)
    entries, areas, _ = G.load_glossary(paths, gr)
    G.check_texts([own], entries, areas, gr, G.load_places(docs))
    if tmpg:
        os.unlink(tmpg.name)
    for c, w, m in gr.errors:
        rep.err('J16', w, '%s %s' % (c, m))


def check_zone(zone, mp, codice, n_scr, used_by_hdr, ev_ids, ctx, rep, reg, alb, script_text, banco):
    where = mp['file_eventi']
    used = set(used_by_hdr)

    def ref(sid, what):
        mm = re.fullmatch(r'_EV_scr_seq_%s_(\d{3}) \+ 1' % codice, str(sid))
        if not mm:
            rep.err('J08', where, '%s: scriptId %r non valido' % (what, sid))
            return
        if int(mm.group(1)) >= n_scr:
            rep.err('J08', where, '%s: script %s inesistente' % (what, mm.group(1)))
        used.add(int(mm.group(1)))

    if zone.get('header') != 'fielddata/script/scr_seq/event_%s.h' % codice:
        rep.err('J08', where, 'header %r' % zone.get('header'))
    ids = []
    pos = {}
    for o in zone.get('objects', []):
        ids.append(o['id'])
        if o.get('scriptId'):
            ref(o['scriptId'], o['id'])
        if not ctx.sprite_ok(o['spriteId']):
            rep.err('J11', where, '%s: sprite %s inesistente' % (o['id'], o['spriteId']))
        if o['eventFlag'] != 'FLAG_NOTHING' and not ctx.known(o['eventFlag']):
            rep.err('J09', where, '%s: eventFlag %s sconosciuto' % (o['id'], o['eventFlag']))
        key = (o['x'], o['z'])
        if key in pos and not (pos[key]['eventFlag'] != o['eventFlag']):
            rep.err('J11', where, '%s e %s sulla stessa casella %s' % (o['id'], pos[key]['id'], key))
        pos[key] = o
        if not 0 <= o['facingDirection'] <= 3:
            rep.err('J11', where, '%s: direzione %s' % (o['id'], o['facingDirection']))
    if [i for i in ev_ids] != ids:
        rep.err('J08', where, 'gli oggetti %s non sono quelli dell\'header %s' % (ids, list(ev_ids)))
    for b in zone.get('bgs', []):
        ref(b['scriptId'], 'bg (%d,%d)' % (b['x'], b['z']))
    for c in zone.get('coords', []):
        ref(c['scriptId'], 'coords (%d,%d)' % (c['x'], c['z']))
        if not ctx.known(c['var']):
            rep.err('J09', where, 'coords: variabile %s sconosciuta' % c['var'])
    for w in zone.get('warps', []):
        if w['header'] not in ctx.maps:
            rep.err('J11', where, 'warp verso la mappa inesistente %s' % w['header'])
    for n in range(n_scr):
        if n not in used:
            rep.err('J08', where, 'lo script %03d non e\' usato da nessun oggetto, bg, coords o OnFrame' % n)


def check_npc(rows, zone, mp, codice, banco, script_text, rep):
    where = mp['simbolo']
    if zone is None:
        return
    objs = {o['id']: o for o in zone.get('objects', [])}
    by = {r['npc_id']: r for r in rows}
    for oid in objs:
        if oid not in by:
            rep.err('J12', where, 'oggetto %s senza riga nel registro NPC' % oid)
    for rid in by:
        if rid not in objs:
            rep.err('J12', where, 'riga NPC %s senza oggetto nell\'evento' % rid)
    for oid, o in objs.items():
        r = by.get(oid)
        if not r:
            continue
        if (str(o['x']), str(o['z'])) != (str(r['x']), str(r['y'])):
            rep.err('J12', '%s %s' % (where, oid), 'casella (%s,%s) diversa dall\'evento (%s,%s)' % (r['x'], r['y'], o['x'], o['z']))
        if o['spriteId'] != r['sprite']:
            rep.err('J12', '%s %s' % (where, oid), 'sprite %s diverso da %s' % (r['sprite'], o['spriteId']))
        hf = '' if o['eventFlag'] == 'FLAG_NOTHING' else o['eventFlag']
        if hf != r['hide_flag']:
            rep.err('J12', '%s %s' % (where, oid), 'hide_flag %r diverso dall\'eventFlag %r' % (r['hide_flag'], hf))
        if r['msg_bank'] != banco:
            rep.err('J12', '%s %s' % (where, oid), 'banco %s invece di %s' % (r['msg_bank'], banco))
        mm = re.fullmatch(r'_EV_scr_seq_%s_(\d{3}) \+ 1' % codice, str(o.get('scriptId')))
        if mm:
            first = _first_msg_deep(script_text, int(mm.group(1)), codice, banco)
            if first is not None and '%05d' % first != r['msg_index']:
                rep.err('J12', '%s %s' % (where, oid), 'msg_index %s: lo script mostra per primo il %05d' % (r['msg_index'], first))


def _first_msg_deep(text, n, codice, banco):
    """Primo messaggio nel testo dello script n, anche dopo un salto: primo riferimento nel suo corpo e nelle etichette seguenti."""
    instrs, labels, chunks = parse_script(text)
    start = None
    for k, (lab, ins) in enumerate(chunks):
        if lab == 'scr_seq_%s_%03d' % (codice, n):
            start = k
            break
    if start is None:
        return None
    for lab, ins in chunks[start:]:
        if lab != chunks[start][0] and re.match(r'^scr_seq_%s_\d{3}$' % codice, lab or ''):
            break
        for _, nm, args in ins:
            for a in args:
                mm = SYM_MSG.fullmatch(a.strip())
                if mm and mm.group(1) == banco:
                    return int(mm.group(2))
    return None


# ----------------------------------------------------------------------------------------------

def find_docs(arg=None):
    for d in ([arg] if arg else []) + [os.path.join(HERE, '..', 'docs'), 'F:/Progetti/pokémon-sicilia/docs']:
        if d and os.path.isfile(os.path.join(d, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json')):
            return os.path.normpath(d)
    return None


# mutazioni del collaudo: (codice atteso, descrizione, funzione(block, files))
def _sost(files, rel_fine, vecchio, nuovo):
    for rel in files:
        if rel.endswith(rel_fine):
            assert vecchio in files[rel], (rel_fine, vecchio)
            files[rel] = files[rel].replace(vecchio, nuovo, 1)
            return
    raise AssertionError(rel_fine)


def mutazioni(blocco):
    m0 = blocco['mappe'][0]
    cam = next(m for m in blocco['mappe'] if m['simbolo'].endswith('2F'))
    scr, bank, gem = cam['file_script'], cam['file_banco'], cam['file_gemello']
    b2 = cam['banco_campagna']
    return [
        ('J00', 'file di script mancante', lambda b, f: f.pop(scr)),
        ('J01', 'SHA-1 sbagliato', lambda b, f: b['file_da_copiare'][0].__setitem__('sha1', '0' * 40)),
        ('J02', 'codice del file diverso dal registro', lambda b, f: b['mappe'][0].__setitem__('codice_file_hg', 'T99X')),
        ('J03', 'id di messaggio fuori ordine', lambda b, f: _sost(f, bank.split('/')[-1], '%s_00001' % b2, '%s_00007' % b2)),
        ('J04', 'messaggio inesistente', lambda b, f: _sost(f, scr.split('/')[-1], '%s_00001' % b2, '%s_00099' % b2)),
        ('J05', 'messaggio mai usato', lambda b, f: _sost(f, scr.split('/')[-1], '%s_00004' % b2, '%s_00003' % b2)),
        ('J06', 'istruzione sconosciuta', lambda b, f: _sost(f, scr.split('/')[-1], '\tLockAll\n\tNPCMsg %s_00005' % b2, '\tLockAll\n\tFooBar\n\tNPCMsg %s_00005' % b2)),
        ('J07', 'etichetta mancante', lambda b, f: _sost(f, scr.split('/')[-1], 'GoToIfEq _pc_nessuna_mail', 'GoToIfEq _pc_manca')),
        ('J08', 'ScrDef mancante', lambda b, f: _sost(f, scr.split('/')[-1], '\tScrDef scr_seq_T20R0202_005\n', '')),
        ('J09', 'flag sconosciuto', lambda b, f: _sost(f, scr.split('/')[-1], 'SetVar VAR_TR_SCENE_CT_01, 5', 'SetFlag FLAG_M_CT_99\n\tSetVar VAR_TR_SCENE_CT_01, 5')),
        ('J10', 'nome senza BufferPlayersName', lambda b, f: _sost(f, scr.split('/')[-1], 'ScrCmd_804 2\n\tBufferPlayersName 0\n', 'ScrCmd_804 2\n')),
        ('J11', 'sprite inesistente', lambda b, f: _sost(f, m0['file_eventi'].split('/')[-1], 'SPRITE_GORGGEOUSM', 'SPRITE_NON_ESISTE')),
        ('J12', 'riga NPC con casella diversa', lambda b, f: b['npc'][0].__setitem__('x', '99')),
        ('J13', 'OnFrame verso uno script inesistente', lambda b, f: _sost(f, cam['file_header_script'].split('/')[-1], '_EV_scr_seq_T20R0202_003 + 1', '_EV_scr_seq_T20R0202_099 + 1')),
        ('J14', 'riga troppo lunga', lambda b, f: _sost(f, bank.split('/')[-1], 'La testa pesa', 'La testa pesa ' + 'x' * 40)),
        ('J15', 'STRVAR diverso nel gemello', lambda b, f: _sost(f, gem.split('/')[-1], '{STRVAR_1 3, 0, 0}', 'Tu')),
        ('J16', 'parole non siciliane in un messaggio scn', lambda b, f: next(t for t in b['testi'] if t['id'] == '%s_00001' % b2).__setitem__('lingua', 'scn')),
        ('J17', 'elenco testi incompleto', lambda b, f: b['testi'].pop(0)),
    ]


def selftest(docs, repo):
    import copy
    good = True
    blocks = sorted(glob.glob(os.path.join(docs, 'MODULO_6', '6.[0-9]*_*.json')))
    ctx = Ctx(docs, repo)
    rep = Report(quiet=True)
    for b in blocks:
        check_block(b, repo, docs, rep, ctx)
    print('blocchi del Modulo 6 controllati: %d' % len(blocks))
    if rep.errors:
        good = False
        print('collaudo: i blocchi veri danno errori: %s' % rep.codes())
        for e in rep.errors[:10]:
            print('   ', *e)
    if not blocks:
        print('collaudo: nessun blocco del Modulo 6 in %s' % docs)
        print('SELFTEST_FAILED')
        return 1
    # mutazioni del primo blocco (in memoria: nessun file toccato)
    path = blocks[0]
    base0 = load_json(path)
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(path)), '..', '..'))
    files0 = {}
    for dp, _, fn in os.walk(os.path.join(root, base0['cartella_file'])):
        for n in fn:
            full = os.path.join(dp, n)
            files0[os.path.relpath(full, os.path.join(root, base0['cartella_file'])).replace(os.sep, '/')] = open(full, encoding='utf-8', newline='').read().replace('\r\n', '\n')
    for cod, descr, fn in mutazioni(base0):
        if not repo and cod in ('J06', 'J09', 'J14'):
            continue
        b, f = copy.deepcopy(base0), dict(files0)
        b['file_inline'] = f
        fn(b, f)
        r = Report(quiet=True)
        check_loaded(b, root, repo, docs, r, None, ctx)
        ok = cod in r.codes()
        print('  %s %s: %s' % ('ok ' if ok else 'KO ', cod, descr + ('' if ok else ' -> dà %s' % r.codes())))
        good = good and ok
    print('repository: %s' % (repo or 'nessuno (J06, J09 e J14 non si controllano)'))
    print('SELFTEST_OK' if good else 'SELFTEST_FAILED')
    return 0 if good else 1


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    ap = argparse.ArgumentParser(description='controllo dei blocchi del Modulo 6')
    ap.add_argument('comando', nargs='?', choices=['check'])
    ap.add_argument('file', nargs='*')
    ap.add_argument('--repo')
    ap.add_argument('--docs')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    docs = find_docs(a.docs)
    repo = find_repo(a.repo)
    if not docs:
        print('ERRORE J00 docs: cartella docs non trovata (usare --docs)')
        print('SCRIPT_FAILED')
        return 1
    if a.selftest:
        return selftest(docs, repo)
    if a.comando != 'check' or not a.file:
        ap.print_help()
        return 2
    rep = Report()
    for f in a.file:
        check_block(f, repo, docs, rep)
    print('blocchi: %d, errori: %d, avvisi: %d' % (len(a.file), len(rep.errors), len(rep.warnings)))
    print('SCRIPT_OK' if not rep.errors else 'SCRIPT_FAILED')
    return 0 if not rep.errors else 1


if __name__ == '__main__':
    sys.exit(main())

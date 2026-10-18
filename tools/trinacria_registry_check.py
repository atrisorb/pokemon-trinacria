#!/usr/bin/env python3
"""Pokemon Trinacria - controllo del registro di flag, variabili e NPC (Modulo 2, blocco 2.4)
e del registro di classi, allenatori, sprite, medaglie e musiche (blocco 2.5).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia oppure da F:\\Progetti\\pokeheartgold):
    python -I tools/trinacria_registry_check.py
    python -I tools/trinacria_registry_check.py --npc data/trinacria/npc_registry.csv
    python -I tools/trinacria_registry_check.py --npc data/trinacria/npc_registry.csv --finale
    python -I tools/trinacria_registry_check.py --repo F:/Progetti/pokeheartgold
    python -I tools/trinacria_registry_check.py --selftest

Ultima riga stampata: REGISTRY_OK / REGISTRY_FAILED (oppure SELFTEST_OK / SELFTEST_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>" (blocca) o "AVVISO <codice> ..." (non blocca).
"""
import argparse
import csv
import io
import json
import os
import re
import sys

DEFAULT_DOCS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs'),
    'F:/Progetti/pokémon-sicilia/docs',
]
REGISTRY_FILES = ['2.1_MAPS_CT_SR_RG.json', '2.2_MAPS_CL_AG_TP.json', '2.3_MAPS_ME_PA_EN_ROADS.json']
FLAGS_FILE = '2.4_FLAGS_VARS.json'
TRAINERS_FILE = '2.5_TRAINERS_SPRITES_FLY_SEQ.json'
TRAMA_FILE = '00_TRAMA_ESPANSA_E_SIDEQUEST.md'
CODE_RE = re.compile(r'\b(?:[MSDBECP])-[A-Z0-9]+(?:-[A-Z0-9]+)?\b')
NPC_HEADER = ['map_symbol', 'npc_id', 'x', 'y', 'sprite', 'msg_bank', 'msg_index', 'post_category',
              'dialect_area', 'ruolo', 'visibile', 'hide_flag', 'trainer_id', 'pokemon_species',
              'accanto_a', 'codice_trama', 'note']
RUOLI_6040 = ('POPOLO', 'ALLENATORE')
RUOLI = ('POPOLO', 'ALLENATORE', 'SISTEMA', 'COMPAGNO', 'PERSONAGGIO', 'SERVIZIO', 'MEMORIA', 'POKEMON')
VISIBILE = ('SEMPRE', 'CAMPAGNA', 'POST')

# ----------------------------------------------------------------------------------------------
# Report


class Report:
    def __init__(self, quiet=False):
        self.errors = []
        self.warnings = []
        self.quiet = quiet

    def err(self, code, where, msg):
        self.errors.append((code, where, msg))
        if not self.quiet:
            print('ERRORE %s %s: %s' % (code, where, msg))

    def warn(self, code, where, msg):
        self.warnings.append((code, where, msg))
        if not self.quiet:
            print('AVVISO %s %s: %s' % (code, where, msg))

    def codes(self):
        return sorted(set(c for c, _, _ in self.errors))


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def find_docs(arg):
    cands = [arg] if arg else DEFAULT_DOCS
    for c in cands:
        if c and os.path.isfile(os.path.join(c, 'MODULO_2', FLAGS_FILE)):
            return os.path.normpath(c)
    return None


def hexint(s):
    return int(s, 16) if isinstance(s, str) else int(s)

# ----------------------------------------------------------------------------------------------
# Scansione del repository pokeheartgold (flag e variabili storici liberati dalla riscrittura)


def _defs(path, prefix):
    out = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            m = re.match(r'#define\s+(%s[A-Za-z0-9_]+)\s+\(?(0x[0-9A-Fa-f]+|\d+)\)?\s*(//.*)?$' % prefix, line.strip())
            if m:
                out[m.group(1)] = int(m.group(2), 0)
    return out


def scan_repo(repo, maps_registry, excluded_ids, extra_engine_flags=(), extra_engine_vars=()):
    """Classifica ogni flag 0x040-0x54F e ogni variabile 0x4030-0x416F di HeartGold.

    Ritorna (flags, vars): {id: {'nomi': [...], 'classi': {classe: [file]}}}. Classi dei file:
    ENGINE (C/asm/include), GLOBAL (script non legato a una mappa), KEPT (script/eventi di uno slot escluso
    o condiviso con uno slot escluso), REPLACED (script/eventi di uno slot riscritto da Trinacria),
    UNREACHABLE (script/eventi solo di slot non usati da Trinacria). Un ID e' libero se compare solo in
    REPLACED/UNREACHABLE (o in nessun file) e non e' tra gli ID letti dal C per indice.
    """
    R = repo.rstrip('/\\') + '/'
    flags = _defs(R + 'include/constants/flags.h', 'FLAG_')
    vars_ = _defs(R + 'include/constants/vars.h', 'VAR_')
    maps = {}
    with open(R + 'include/constants/maps.h', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'#define\s+(MAP_[A-Z0-9_]+)\s+(\d+)', line)
            if m:
                maps[m.group(1)] = int(m.group(2))
    hdr = {}
    txt = open(R + 'src/data/map_headers.h', encoding='utf-8').read()
    for m in re.finditer(r'\[(MAP_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n\s*\},', txt, re.S):
        body = m.group(2)

        def g(k):
            return re.search(r'\.%s\s*=\s*([A-Za-z0-9_]+)' % k, body).group(1)
        if m.group(1) in maps:
            hdr[maps[m.group(1)]] = {'scripts': g('scriptsBank'), 'shdr': g('scriptHeaderBank'), 'events': g('eventsBank')}
    used = {mp['id']: mp for mp in maps_registry}
    status = {}

    def scr(b):
        return 'files/fielddata/script/scr_seq/' + re.sub(r'_bin$', '', b) + '.s'

    def ev(b):
        return 'files/fielddata/eventdata/zone_event/' + re.sub(r'_bin$', '', b).replace('NARC_zone_event_', '') + '.json'
    for mid, h in hdr.items():
        for key, fn in (('scripts', scr), ('shdr', scr), ('events', ev)):
            f = fn(h[key])
            if mid in used:
                mp = used[mid]
                newf = {'scripts': mp['script']['file'], 'shdr': mp['script']['file_intestazione'],
                        'events': mp['eventi']['file']}[key]
                role = 'REPLACED' if newf == f else 'LEFT'
            elif mid in excluded_ids:
                role = 'EXCLUDED'
            else:
                role = 'UNUSED'
            status.setdefault(f, set()).add(role)

    def fstatus(f):
        s = status.get(f)
        if s is None:
            return 'GLOBAL'
        if 'EXCLUDED' in s:
            return 'KEPT'
        if 'REPLACED' in s:
            return 'REPLACED'
        return 'UNREACHABLE'
    files = []
    skip_top = {'build', '.git', 'tools', 'subprojects', 'docs', '.cache', 'data'}
    for root, dirs, fs in os.walk(R):
        rel = os.path.relpath(root, R).replace(os.sep, '/')
        if rel == '.':
            dirs[:] = [x for x in dirs if x not in skip_top]
            rel = ''
        if rel.startswith(('files/msgdata', 'files/graphic', 'graphics')):
            continue
        for fn in fs:
            if fn.endswith(('.c', '.h', '.s', '.inc', '.json', '.txt', '.csv')):
                files.append((rel + '/' + fn) if rel else fn)
    word = re.compile(r'\b(FLAG_[A-Za-z0-9_]+|VAR_[A-Za-z0-9_]+)\b')
    refs = {}
    for f in files:
        if f in ('include/constants/flags.h', 'include/constants/vars.h') or f.startswith('include/trinacria/') \
                or f.endswith('_hg_compat.h'):
            continue
        try:
            t = open(R + f, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        for w in set(word.findall(t)):
            refs.setdefault(w, set()).add(f)

    def classify(f):
        if f.startswith('files/fielddata/script/scr_seq/') and f.endswith('.s'):
            return fstatus(f)
        if f.startswith('files/fielddata/eventdata/zone_event/'):
            return fstatus(f)
        if f.startswith('files/fielddata/script/scr_seq/') and f.endswith('.h'):
            return 'EVENT_H'
        return 'ENGINE'

    def analyze(defs, lo, hi, extra):
        res = {}
        for i in range(lo, hi + 1):
            names = sorted(n for n, v in defs.items() if v == i)
            cls = {}
            for n in names:
                for f in refs.get(n, ()):
                    cls.setdefault(classify(f), set()).add(f)
            if i in extra:
                cls.setdefault('ENGINE', set()).add('letto per indice dal C')
            res[i] = {'nomi': names, 'classi': {k: sorted(v) for k, v in cls.items()}}
        return res
    return analyze(flags, 0x40, 0x54F, set(extra_engine_flags)), analyze(vars_, 0x4030, 0x416F, set(extra_engine_vars))


def is_free(entry):
    return set(entry['classi']) <= {'REPLACED', 'UNREACHABLE'}

# ----------------------------------------------------------------------------------------------
# Registro


class Context:
    def __init__(self, docs):
        self.docs = docs
        m2 = os.path.join(docs, 'MODULO_2')
        self.reg = load_json(os.path.join(m2, FLAGS_FILE))
        self.maps = {}
        for fn in REGISTRY_FILES:
            d = load_json(os.path.join(m2, fn))
            for mp in d['mappe']:
                self.maps[mp['simbolo']] = mp
            if 'piano_globale' in d:
                self.excluded = set(x['id'] for x in d['piano_globale']['slot']['esclusi']['slot'])
        self.trama_path = os.path.join(docs, TRAMA_FILE)
        r = self.reg
        self.flags = {f['simbolo']: f for f in r['flag']['elenco']}
        self.flag_alias = {a['alias']: a['di'] for a in r['flag']['alias_trama']}
        self.engine_flags = {f['simbolo']: f for f in r['flag']['motore']}
        self.hist_flags = {}
        for pool in r['flag']['storico']['pool'].values():
            for grp in pool['gruppi'].values():
                for s in grp['simboli']:
                    self.hist_flags[s['simbolo']] = s
        self.vars = {v['simbolo']: v for v in r['variabili']['elenco']}
        self.hist_vars = {}
        for grp in r['variabili']['storico']['gruppi'].values():
            for s in grp['simboli']:
                self.hist_vars[s['simbolo']] = s
        self.codes = {f['codice'] for f in r['flag']['elenco'] if f.get('codice')}
        npc = r['npc_registry']
        self.dialects = {a['area']: a for a in npc['aree_dialettali']}
        self.memorial = {m['mappa']: m for m in npc['luoghi_della_memoria']}
        self.dims = r['dimensioni_mappe']
        # blocco 2.5 (facoltativo finche' non esiste)
        self.tr_reg = None
        self.trainers = {}
        self.sprite_alias = {}
        p25 = os.path.join(m2, TRAINERS_FILE)
        if os.path.isfile(p25):
            t = self.tr_reg = load_json(p25)
            self.trainers = {e['id']: e for e in t['allenatori']['elenco']}
            for s in t['sprite']['personaggi'] + t['sprite']['classi']:
                self.sprite_alias[s['simbolo']] = s['slot_hg']

    def all_flag_symbols(self):
        s = set(self.flags) | set(self.flag_alias) | set(self.engine_flags) | set(self.hist_flags)
        return s

    def map_province(self, mp):
        if mp['provincia'] != 'ROADS':
            return mp['provincia']
        return (mp.get('area_dialettale') or 'ROADS').split('_')[0]


def check_registry(ctx, rep, repo_scan=None):
    r = ctx.reg
    seen_ids = {}
    seen_sym = set()
    lo, hi = hexint(r['flag']['intervallo']['primo']), hexint(r['flag']['intervallo']['ultimo'])
    for f in r['flag']['elenco']:
        v = hexint(f['id'])
        if v != f['valore']:
            rep.err('R02', f['simbolo'], 'id %s diverso da valore %d' % (f['id'], f['valore']))
        if not lo <= v <= hi:
            rep.err('R02', f['simbolo'], 'id %s fuori da 0x%X-0x%X' % (f['id'], lo, hi))
        if v in seen_ids:
            rep.err('R01', f['simbolo'], 'id %s gia\' usato da %s' % (f['id'], seen_ids[v]))
        seen_ids[v] = f['simbolo']
        if f['simbolo'] in seen_sym or not re.match(r'^FLAG_[A-Z0-9_]+$', f['simbolo']):
            rep.err('R03', f['simbolo'], 'simbolo duplicato o non valido')
        seen_sym.add(f['simbolo'])
        for mp in f.get('mappe', []):
            if mp not in ctx.maps:
                rep.err('R10', f['simbolo'], 'mappa %s inesistente nei registri 2.1-2.3' % mp)
        if f.get('codice'):
            exp = 'FLAG_' + f['codice'].replace('-', '_')
            if f['simbolo'] != exp:
                rep.err('R03', f['simbolo'], 'nome meccanico atteso %s (trama R-08)' % exp)
    for e in r['flag']['motore']:
        v = hexint(e['id'])
        if v in seen_ids:
            rep.err('R01', e['simbolo'], 'id %s gia\' usato da %s' % (e['id'], seen_ids[v]))
        seen_ids[v] = e['simbolo']
    for a in r['flag']['alias_trama']:
        if a['di'] not in ctx.flags and a['di'] not in ctx.engine_flags:
            rep.err('R04', a['alias'], 'alias verso %s inesistente' % a['di'])
        if a['alias'] in seen_sym:
            rep.err('R03', a['alias'], 'alias con lo stesso nome di un flag')
    # storico
    reserved = {hexint(x['id']) for x in r['flag']['storico']['riservati_motore']}
    free_listed = set()
    for pname, pool in r['flag']['storico']['pool'].items():
        plo, phi = hexint(pool['da']), hexint(pool['a'])
        free_listed |= {hexint(x) for x in pool['liberi']}
        for gname, grp in pool['gruppi'].items():
            for s in grp['simboli']:
                v = hexint(s['id'])
                if v in seen_ids:
                    rep.err('R01', s['simbolo'], 'id %s gia\' usato da %s' % (s['id'], seen_ids[v]))
                seen_ids[v] = s['simbolo']
                if v in reserved or not plo <= v <= phi or s['id'] not in pool['liberi']:
                    rep.err('R08', s['simbolo'], 'id %s non libero nel pool %s' % (s['id'], pname))
                if s['simbolo'] in seen_sym:
                    rep.err('R03', s['simbolo'], 'simbolo duplicato')
                seen_sym.add(s['simbolo'])
    for v in reserved:
        if v < 0x40:
            rep.err('R08', '0x%X' % v, 'i flag 0x000-0x03F sono temporanei di mappa (azzerati a ogni cambio mappa)')
    # variabili
    vseen = {}
    ranges = [(hexint(a), hexint(b)) for a, b in r['variabili']['intervalli']]
    for v in r['variabili']['elenco'] + r['variabili']['motore']:
        n = hexint(v['id'])
        if n in vseen:
            rep.err('R01', v['simbolo'], 'id %s gia\' usato da %s' % (v['id'], vseen[n]))
        vseen[n] = v['simbolo']
        if v in r['variabili']['elenco']:
            if not any(a <= n <= b for a, b in ranges):
                rep.err('R02', v['simbolo'], 'id %s fuori dagli intervalli delle missioni' % v['id'])
            vals = [x['valore'] for x in v['valori']]
            if vals != list(range(len(vals))) or len(vals) < 3:
                rep.err('R07', v['simbolo'], 'valori non contigui da 0 o meno di 3 passi')
            if v.get('flag_completamento') and v['flag_completamento'] not in ctx.flags:
                rep.err('R04', v['simbolo'], 'flag di completamento %s inesistente' % v['flag_completamento'])
    vres = {hexint(x['id']) for x in r['variabili']['storico']['riservati_motore']}
    vfree = set(r['variabili']['storico']['liberi'])
    for grp in r['variabili']['storico']['gruppi'].values():
        for s in grp['simboli']:
            n = hexint(s['id'])
            if n in vseen:
                rep.err('R01', s['simbolo'], 'id %s gia\' usato da %s' % (s['id'], vseen[n]))
            vseen[n] = s['simbolo']
            if n in vres or s['id'] not in vfree:
                rep.err('R08', s['simbolo'], 'variabile %s non libera' % s['id'])
    # header generati
    for key, defs in (('file_trinacria_flags_h', None), ('file_trinacria_vars_h', None)):
        lines = r[key]['righe']
        got = {}
        for line in lines:
            m = re.match(r'#define\s+((?:FLAG|VAR)_[A-Z0-9_]+)\s+(\S+)', line)
            if m and not m.group(1).endswith('_H'):
                got[m.group(1)] = m.group(2)
        want = {}
        if key == 'file_trinacria_flags_h':
            for f in r['flag']['elenco']:
                want[f['simbolo']] = f['id']
            for a in r['flag']['alias_trama']:
                want[a['alias']] = a['di']
            for s in ctx.hist_flags.values():
                want[s['simbolo']] = s['id']
        else:
            for v in r['variabili']['elenco']:
                want[v['simbolo']] = v['id']
            for s in ctx.hist_vars.values():
                want[s['simbolo']] = s['id']
        if got != want:
            diff = sorted(set(got.items()) ^ set(want.items()))[:5]
            rep.err('R09', key, 'righe del file non coerenti con gli elenchi (es. %s)' % diff)
    # trama
    if os.path.isfile(ctx.trama_path):
        trama = open(ctx.trama_path, encoding='utf-8').read()
        tcodes = set(CODE_RE.findall(trama)) | {'E-ST-09'}
        for c in sorted(tcodes - ctx.codes):
            rep.err('R05', c, 'codice della trama senza flag di completamento')
        for c in sorted(ctx.codes - tcodes):
            rep.err('R06', c, 'flag per un codice che non esiste nella trama')
        for name in sorted(set(re.findall(r'\bFLAG_[A-Z0-9_]+', trama))):
            if name not in ctx.all_flag_symbols():
                rep.err('R04', name, 'flag nominato dalla trama ma assente dal registro')
        for name in sorted(set(re.findall(r'\bVAR_[A-Z0-9_]+', trama))):
            if name not in ctx.vars and name not in {v['simbolo'] for v in r['variabili']['motore']}:
                rep.err('R04', name, 'variabile nominata dalla trama ma assente dal registro')
    else:
        rep.warn('R05', ctx.trama_path, 'trama non trovata: controllo dei codici saltato')
    # repository
    if repo_scan is not None:
        fl, vr = repo_scan
        for s in ctx.hist_flags.values():
            e = fl[hexint(s['id'])]
            if not is_free(e):
                rep.err('G01', s['simbolo'], 'id %s usato da file che restano: %s' % (s['id'], {k: v[:2] for k, v in e['classi'].items() if k not in ('REPLACED', 'UNREACHABLE')}))
        for s in ctx.hist_vars.values():
            e = vr[hexint(s['id'])]
            if not is_free(e):
                rep.err('G01', s['simbolo'], 'id %s usato da file che restano: %s' % (s['id'], {k: v[:2] for k, v in e['classi'].items() if k not in ('REPLACED', 'UNREACHABLE')}))
        for v in r['variabili']['elenco']:
            e = vr[hexint(v['id'])]
            if e['classi']:
                rep.err('G02', v['simbolo'], 'la variabile %s e\' citata da %s' % (v['id'], sorted(e['classi'])))

# ----------------------------------------------------------------------------------------------
# Registro del blocco 2.5 (classi, allenatori, sprite, medaglie, musiche)

POOL_CLASS_CATS = ('COMUNE', 'SICILIANA', 'U_SISTEMA')


def _header_defs(lines, prefix):
    out = {}
    for line in lines:
        m = re.match(r'#define\s+(%s[A-Za-z0-9_]+)\s+(\S+)' % prefix, line)
        if m and not m.group(1).endswith('_H'):
            out[m.group(1)] = m.group(2)
    return out


def check_trainers(ctx, rep, repo=None):
    t = ctx.tr_reg
    if t is None:
        rep.warn('T00', TRAINERS_FILE, 'registro del blocco 2.5 assente: controlli T saltati')
        return
    # classi
    classes = t['classi_allenatore']['elenco']
    if [c['indice'] for c in classes] != list(range(129)):
        rep.err('T10', 'classi', 'servono le classi 0-128 in ordine')
    csym = {}
    for c in classes:
        if c['simbolo'] in csym:
            rep.err('T10', c['simbolo'], 'nome di classe ripetuto')
        csym[c['simbolo']] = c
        if c['rinominata'] != (c['simbolo'] != c['simbolo_hg']):
            rep.err('T10', c['simbolo'], 'campo rinominata incoerente')
    hg_names = {c['simbolo_hg'] for c in classes}
    for c in classes:
        if c['rinominata'] and c['simbolo'] in hg_names:
            rep.err('T10', c['simbolo'], 'il nome nuovo coincide con un nome HeartGold')
    # allenatori
    el = t['allenatori']['elenco']
    if [e['id'] for e in el] != list(range(738)):
        rep.err('T01', 'allenatori', 'servono gli id 0-737, ognuno una volta, in ordine')
    seen = set()
    for e in el:
        w = '%d %s' % (e['id'], e['simbolo'])
        if e['simbolo'] in seen:
            rep.err('T02', w, 'simbolo ripetuto')
        seen.add(e['simbolo'])
        if not re.match(r'^TRAINER_[A-Z0-9_]+$', e['simbolo']):
            rep.err('T02', w, 'simbolo non valido')
        tid, tipo = e['id'], e['tipo']
        ok_tipo = (tid == 0 and tipo == 'NESSUNO') or (1 <= tid <= 699 and tipo in ('FISSO', 'POOL')) or \
                  (700 <= tid <= 737 and tipo in ('FISSO', 'RISERVA'))
        if not ok_tipo:
            rep.err('T05', w, 'tipo %s non ammesso per questo id' % tipo)
        if tipo == 'FISSO':
            c = csym.get(e['classe'])
            if c is None:
                rep.err('T03', w, 'classe %s inesistente' % e['classe'])
            elif c['categoria'] in ('NON_USARE', 'FIERA', 'PROTAGONISTA'):
                rep.err('T03', w, 'classe %s di categoria %s' % (e['classe'], c['categoria']))
            if e['nome_in_lotta'] and len(e['nome_in_lotta']) > 7:
                rep.err('T04', w, 'nome in lotta oltre 7 caratteri')
            if not e['mappa'] or e['mappa'] not in ctx.maps:
                rep.err('T07', w, 'mappa %s inesistente' % e['mappa'])
            elif e['mappa'] in ctx.memorial:
                rep.err('T07', w, 'nessuna lotta nei luoghi della memoria')
            ct = e['codice_trama']
            if not ct or (ct not in ctx.codes and ct != 'ST-01'):
                rep.err('T06', w, 'codice della trama %s sconosciuto' % ct)
        elif e['classe'] is not None:
            rep.err('T03', w, 'solo gli allenatori fissi hanno la classe nel registro')
        if tipo == 'POOL' and not re.match(r'^TRAINER_TR_%s_\d{3}$' % e['gruppo'], e['simbolo']):
            rep.err('T05', w, 'simbolo del pool diverso dal gruppo %s' % e['gruppo'])
    for k in range(1, 9):
        for v in range(1, 4):
            tid = 700 + 3 * (k - 1) + (v - 1)
            e = ctx.trainers.get(tid)
            if e and e['tipo'] == 'FISSO' and not (e['simbolo'].startswith('TRAINER_RITROVO_') and e['simbolo'].endswith('_%d' % v)):
                rep.err('T05', '%d' % tid, 'formula dei Ritrovi (blocco 2.4): 700 + 3*(k-1) + (versione-1)')
    for tid, code in ((730, 'P-03'), (731, 'P-04'), (732, 'P-05'), (733, 'P-06')):
        if ctx.trainers.get(tid, {}).get('codice_trama') != code:
            rep.err('T05', '%d' % tid, 'il Fantasma %s usa l\'allenatore %d (trama)' % (code, tid))
    # gruppi
    for g in t['allenatori']['gruppi']:
        po = g['pool']
        if po:
            ids = [e['id'] for e in el if e['tipo'] == 'POOL' and e['gruppo'] == g['gruppo']]
            if ids != list(range(po['primo'], po['ultimo'] + 1)) or po['numero'] != len(ids):
                rep.err('T05', g['gruppo'], 'pool non contiguo o diverso da gruppi.pool')
    # header
    want = {e['simbolo']: str(e['id']) for e in el if e['id'] > 0}
    got = _header_defs(t['file_trinacria_trainers_h']['righe'], 'TRAINER_')
    if got != want:
        rep.err('T08', 'file_trinacria_trainers_h', 'righe diverse dall\'elenco (es. %s)' % sorted(set(got.items()) ^ set(want.items()))[:3])
    got = _header_defs(t['file_trainer_class_h']['righe'], 'TRAINERCLASS_')
    want = {c['simbolo']: str(c['indice']) for c in classes}
    if {k: v for k, v in got.items() if k in want or v.isdigit() and int(v) < 129} != want:
        rep.err('T08', 'file_trainer_class_h', 'definizioni delle classi diverse dall\'elenco')
    got = _header_defs(t['file_trainer_class_hg_compat_h']['righe'], 'TRAINERCLASS_')
    want = {c['simbolo_hg']: c['simbolo'] for c in classes if c['rinominata']}
    if got != want:
        rep.err('T08', 'file_trainer_class_hg_compat_h', 'alias diversi dalle classi rinominate')
    got = _header_defs(t['file_trinacria_sprites_h']['righe'], 'SPRITE_')
    if got != ctx.sprite_alias:
        rep.err('T08', 'file_trinacria_sprites_h', 'alias diversi dalla sezione sprite')
    got = _header_defs(t['file_trinacria_badges_h']['righe'], 'BADGE_')
    if got != {b['alias']: b['slot_hg'] for b in t['medaglie']['dossier']}:
        rep.err('T08', 'file_trinacria_badges_h', 'alias diversi dalla sezione medaglie')
    got = _header_defs(t['file_trinacria_seq_h']['righe'], 'SEQ_')
    want = {m['simbolo']: m['slot_hg_sostituito'] for m in t['musiche']['campo']}
    want.update({m['simbolo']: m['slot_hg'] for m in t['musiche']['lotta']})
    if got != want:
        rep.err('T08', 'file_trinacria_seq_h', 'alias diversi dalla sezione musiche')
    slots = [m['slot_hg_sostituito'] for m in t['musiche']['campo']] + [m['slot_hg'] for m in t['musiche']['lotta']]
    if len(slots) != len(set(slots)):
        rep.err('T08', 'musiche', 'uno slot SEQ usato da due nomi')
    # repository
    if repo:
        inc = os.path.join(repo, 'include', 'constants')
        tc = _defs(os.path.join(inc, 'trainer_class.h'), 'TRAINERCLASS_')
        cp = os.path.join(inc, 'trainer_class_hg_compat.h')
        compat = _header_defs(open(cp, encoding='utf-8').read().splitlines(), 'TRAINERCLASS_') if os.path.isfile(cp) else {}
        for c in classes:
            n = tc.get(c['simbolo'], tc.get(c['simbolo_hg']))
            if n is None and c['simbolo_hg'] in compat:
                n = c['indice']
            if n != c['indice']:
                rep.err('T09', c['simbolo'], 'classe %s/%s assente o con altro numero in trainer_class.h' % (c['simbolo'], c['simbolo_hg']))
        trh = _defs(os.path.join(inc, 'trainers.h'), 'TRAINER_')
        for e in el:
            if e['id'] > 0 and e['simbolo'] in trh and trh[e['simbolo']] != e['id']:
                rep.err('T09', e['simbolo'], 'nome gia\' usato in trainers.h con un altro numero')
        spr = _defs(os.path.join(inc, 'sprites.h'), 'SPRITE_')
        for s in t['sprite']['personaggi'] + t['sprite']['classi']:
            if spr.get(s['slot_hg']) != s['valore']:
                rep.err('T09', s['simbolo'], 'slot %s assente da sprites.h' % s['slot_hg'])
        for p in t['sprite']['pokemon']:
            if p['sprite'] not in spr:
                rep.err('T09', p['specie'], 'sprite %s assente da sprites.h' % p['sprite'])
        seq = _defs(os.path.join(inc, 'sndseq.h'), 'SEQ_')
        for m in t['musiche']['lotta']:
            if seq.get(m['slot_hg']) != m['valore'] or (m['gemello_gb_sounds'] and m['gemello_gb_sounds'] not in seq):
                rep.err('T09', m['simbolo'], 'slot %s o gemello assente da sndseq.h' % m['slot_hg'])
        bd = _defs(os.path.join(inc, 'badge.h'), 'BADGE_')
        for b in t['medaglie']['dossier']:
            if bd.get(b['slot_hg']) != b['valore']:
                rep.err('T09', b['alias'], 'medaglia %s assente da badge.h' % b['slot_hg'])
        for e in t['modifiche_codice']:
            p = os.path.join(repo, e['file'])
            txt = open(p, encoding='utf-8').read() if os.path.isfile(p) else ''
            if txt.count(e['cerca']) + txt.count(e['sostituisci']) != 1:
                rep.err('T09', e['id'], 'in %s non si trova una sola volta il testo da cercare (o quello gia\' sostituito)' % e['file'])

# ----------------------------------------------------------------------------------------------
# Registro degli NPC


def map_bounds(ctx, mp):
    """Ritorna la lista dei rettangoli validi (x0, y0, x1, y1) in caselle, o None se sconosciuta."""
    if mp['tipo'] == 'esterno' and 'celle' in mp['matrice'] and mp['matrice']['simbolo'].endswith('0000_EVERYWHERE_bin'):
        return [(32 * cx, 32 * cy, 32 * cx + 32, 32 * cy + 32) for cx, cy in mp['matrice']['celle']]
    dim = ctx.dims.get(mp['simbolo'])
    if dim:
        return [(0, 0, 32 * dim[0], 32 * dim[1])]
    return None


def sprite_species_match(sprite, species):
    m = re.match(r'^SPRITE_FOLLOWER_MON_(?:STATIC_)?([A-Z0-9_]+)$', sprite)
    if not m or not species.startswith('SPECIES_'):
        return False
    s = m.group(1)
    sp = species[len('SPECIES_'):]
    if s == sp:
        return True
    for suf in ('_F', '_SPIKY'):
        if s.endswith(suf) and s[:-len(suf)] == sp:
            return True
    return s.startswith(sp + '_')


def read_rows(path_or_text, rep, label):
    if '\n' in path_or_text:
        text = path_or_text
    else:
        raw = open(path_or_text, 'rb').read()
        if raw.startswith(b'\xef\xbb\xbf'):
            rep.err('N01', label, 'file con BOM: salvare in UTF-8 senza BOM')
            raw = raw[3:]
        if b'\r\n' in raw:
            rep.err('N01', label, 'fine riga CRLF: usare LF')
        text = raw.decode('utf-8')
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows or rows[0] != NPC_HEADER:
        rep.err('N01', label, 'intestazione diversa da: ' + ','.join(NPC_HEADER))
        return []
    out = []
    for i, r in enumerate(rows[1:], start=2):
        if not r:
            continue
        if len(r) != len(NPC_HEADER):
            rep.err('N02', '%s:%d' % (label, i), '%d colonne invece di %d' % (len(r), len(NPC_HEADER)))
            continue
        d = dict(zip(NPC_HEADER, r))
        d['_line'] = i
        out.append(d)
    return out


def check_npc(ctx, rep, source, label, finale=False, soglia=20, repo=None):
    rows = read_rows(source, rep, label)
    sprites = species = None
    if repo:
        sprites = set(_defs(os.path.join(repo, 'include/constants/sprites.h'), 'SPRITE_'))
        sprites |= {a for a, slot in ctx.sprite_alias.items() if slot in sprites}
        species = set(_defs(os.path.join(repo, 'include/constants/species.h'), 'SPECIES_'))
    static_species = set(ctx.reg['npc_registry']['sprite_pokemon_statici'])
    known_flags = ctx.all_flag_symbols()
    by_map = {}
    for d in rows:
        by_map.setdefault(d['map_symbol'], []).append(d)
    counts = {}
    for d in rows:
        where = '%s:%d %s/%s' % (label, d['_line'], d['map_symbol'], d['npc_id'])
        mp = ctx.maps.get(d['map_symbol'])
        if mp is None:
            rep.err('N03', where, 'mappa inesistente nei registri 2.1-2.3')
            continue
        if not re.match(r'^obj_[a-z0-9_]+$', d['npc_id']):
            rep.err('N04', where, 'npc_id deve essere obj_<minuscole/cifre/_>')
        ruolo = d['ruolo']
        if ruolo not in RUOLI:
            rep.err('N13', where, 'ruolo sconosciuto %r' % ruolo)
            continue
        # coordinate
        try:
            x, y = int(d['x']), int(d['y'])
            b = map_bounds(ctx, mp)
            if b is None:
                rep.warn('N05', where, 'dimensioni della mappa sconosciute: coordinate non controllate')
            elif not any(x0 <= x < x1 and y0 <= y < y1 for x0, y0, x1, y1 in b):
                rep.err('N05', where, 'casella (%d,%d) fuori dalla mappa %s' % (x, y, b))
        except ValueError:
            rep.err('N05', where, 'coordinate non intere')
        # testi
        bank = mp['testi'].get('banco_campagna')
        if bank in (None, 'msg_0003_EVERYWHERE'):
            rep.err('N21', where, 'la mappa non ha testi propri (Zona Safari o slot senza testi): niente NPC')
        elif d['msg_bank'] == 'STD':
            if ruolo != 'SERVIZIO' or d['msg_index'] != '-':
                rep.err('N08', where, 'msg_bank STD solo per ruolo SERVIZIO con msg_index -')
        elif d['msg_bank'] != bank:
            rep.err('N08', where, 'msg_bank %s diverso dal banco della mappa %s' % (d['msg_bank'], bank))
        elif not re.match(r'^\d{5}$', d['msg_index']):
            rep.err('N09', where, 'msg_index deve avere 5 cifre')
        elif repo and finale:
            jf = os.path.join(repo, 'files/msgdata/msg', bank + '.json')
            if os.path.isfile(jf):
                ids = {m['id'] for m in load_json(jf)['messages']}
                if '%s_%s' % (bank, d['msg_index']) not in ids:
                    rep.err('N09', where, 'messaggio %s_%s assente dal banco' % (bank, d['msg_index']))
        # sprite e Pokemon
        sp = d['sprite']
        if not re.match(r'^SPRITE_[A-Z0-9_]+$', sp) or (sprites is not None and sp not in sprites):
            rep.err('N07', where, 'sprite %s inesistente' % sp)
        is_mon_sprite = sp.startswith('SPRITE_FOLLOWER_MON_')
        if ruolo == 'POKEMON':
            if not is_mon_sprite or not sprite_species_match(sp, d['pokemon_species']):
                rep.err('N16', where, 'Pokemon: sprite SPRITE_FOLLOWER_MON_* coerente con %s' % d['pokemon_species'])
            elif species is not None and d['pokemon_species'] not in species:
                rep.err('N16', where, 'specie %s inesistente' % d['pokemon_species'])
            else:
                name = d['pokemon_species'][len('SPECIES_'):]
                if not sp.startswith('SPRITE_FOLLOWER_MON_STATIC_'):
                    if name in static_species:
                        rep.err('N16', where, 'esiste SPRITE_FOLLOWER_MON_STATIC_%s: usare quello' % name)
                    else:
                        rep.warn('N16', where, 'sprite dinamico del Pokemon a seguito: prova a schermo nel Modulo 7')
            acc = d['accanto_a']
            if acc == 'SELVATICO':
                if d['map_symbol'] in ctx.memorial:
                    rep.err('N17', where, 'nessun Pokemon selvatico nei luoghi della memoria')
            else:
                owner = [o for o in by_map[d['map_symbol']] if o['npc_id'] == acc and o['ruolo'] != 'POKEMON']
                if not owner:
                    rep.err('N16', where, 'accanto_a %r non e\' un NPC umano della stessa mappa' % acc)
                else:
                    try:
                        if max(abs(int(owner[0]['x']) - int(d['x'])), abs(int(owner[0]['y']) - int(d['y']))) > 2:
                            rep.err('N16', where, 'il Pokemon deve stare entro 2 caselle da %s' % acc)
                    except ValueError:
                        pass
            if d['dialect_area'] != 'ITALIANO':
                rep.err('N11', where, 'i testi dei Pokemon sono narrazione: dialect_area ITALIANO')
        else:
            if is_mon_sprite:
                rep.err('N07', where, 'sprite di Pokemon su un NPC umano: usare ruolo POKEMON')
            if d['pokemon_species'] or d['accanto_a']:
                rep.err('N16', where, 'pokemon_species e accanto_a solo per ruolo POKEMON')
            area = d['dialect_area']
            if area not in ctx.dialects:
                rep.err('N11', where, 'area dialettale sconosciuta %r' % area)
            elif area != 'ITALIANO':
                prov = ctx.map_province(mp)
                if ctx.dialects[area]['provincia'] != prov and not d['note'].startswith('FORESTIERO:'):
                    rep.err('N12', where, 'area %s di %s in una mappa di %s (note: FORESTIERO: <motivo>)' % (area, ctx.dialects[area]['provincia'], prov))
        # visibilita'
        vis, hf = d['visibile'], d['hide_flag']
        if vis not in VISIBILE:
            rep.err('N14', where, 'visibile deve essere SEMPRE, CAMPAGNA o POST')
        elif vis == 'CAMPAGNA' and hf != 'FLAG_POST_RESIGNATION':
            rep.err('N14', where, 'CAMPAGNA richiede hide_flag FLAG_POST_RESIGNATION')
        elif vis == 'POST' and hf != 'FLAG_TR_HIDE_POSTGAME':
            rep.err('N14', where, 'POST richiede hide_flag FLAG_TR_HIDE_POSTGAME')
        elif vis == 'SEMPRE' and hf in ('FLAG_POST_RESIGNATION', 'FLAG_TR_HIDE_POSTGAME'):
            rep.err('N14', where, 'SEMPRE non puo\' usare %s' % hf)
        if hf:
            if hf not in known_flags:
                rep.err('N19', where, 'hide_flag %s non registrato' % hf)
            elif hf in ctx.hist_flags:
                grp = ctx.hist_flags[hf]['gruppo']
                if ctx.hist_flags[hf]['pool'] != 'nascondi':
                    rep.err('N19', where, '%s e\' un flag di oggetto, non di visibilita\'' % hf)
                elif grp not in ('GLOBALE', mp['provincia']):
                    rep.err('N19', where, '%s appartiene al gruppo %s, la mappa a %s' % (hf, grp, mp['provincia']))
        # allenatori
        tid = d['trainer_id']
        if tid:
            if not tid.isdigit():
                rep.err('N15', where, 'trainer_id non numerico')
            else:
                t = int(tid)
                if ruolo in ('ALLENATORE', 'SISTEMA'):
                    if not 1 <= t <= 699:
                        rep.err('N15', where, 'allenatori della storia: 1-699')
                elif ruolo in ('COMPAGNO', 'PERSONAGGIO'):
                    if not 700 <= t <= 737 or vis != 'POST':
                        rep.err('N15', where, 'compagni e personaggi lottano solo nel post-game (700-737, visibile POST)')
                    if ruolo == 'COMPAGNO' and re.match(r'^C-0[1-8]$', d['codice_trama']):
                        k = int(d['codice_trama'][-1])
                        if t not in (700 + 3 * (k - 1), 701 + 3 * (k - 1), 702 + 3 * (k - 1)):
                            rep.err('N15', where, 'il Ritrovo di %s usa gli allenatori %d-%d' % (d['codice_trama'], 700 + 3 * (k - 1), 702 + 3 * (k - 1)))
                else:
                    rep.err('N15', where, 'trainer_id non ammesso per il ruolo %s' % ruolo)
                te = ctx.trainers.get(t)
                if ctx.tr_reg is not None and 0 <= t <= 737:
                    if te is None or te['tipo'] in ('NESSUNO', 'RISERVA'):
                        rep.err('N15', where, 'allenatore %d riservato o inesistente nel registro 2.5' % t)
                    elif te['tipo'] == 'POOL':
                        grp = mp['provincia']
                        if te['gruppo'] != grp:
                            rep.err('N15', where, '%s e\' del pool %s, la mappa del gruppo %s' % (te['simbolo'], te['gruppo'], grp))
                        if ruolo not in ('ALLENATORE', 'SISTEMA'):
                            rep.err('N15', where, 'un allenatore del pool ha ruolo ALLENATORE o SISTEMA')
                    else:
                        if te['ruolo_npc'] == 'COMPAGNO' and not te['simbolo'].startswith('TRAINER_RITROVO_'):
                            rep.err('N15', where, '%s e\' un alleato: la lotta parte da MultiBattle, niente trainer_id nel registro' % te['simbolo'])
                        elif te['ruolo_npc'] != ruolo:
                            rep.err('N15', where, '%s ha ruolo %s nel registro 2.5' % (te['simbolo'], te['ruolo_npc']))
                        if te['codice_trama'] and ruolo != 'COMPAGNO' and d['codice_trama'] != te['codice_trama']:
                            rep.err('N15', where, '%s richiede codice_trama %s' % (te['simbolo'], te['codice_trama']))
                        if te['mappa'] and te['mappa'] != d['map_symbol']:
                            rep.warn('N15', where, '%s lotta in %s secondo il registro 2.5' % (te['simbolo'], te['mappa']))
        elif ruolo == 'ALLENATORE':
            rep.err('N15', where, 'ALLENATORE senza trainer_id')
        # codici della trama
        ct = d['codice_trama']
        if ct and ct not in ctx.codes and not re.match(r'^ST-(0[1-9]|1[0-2])$', ct):
            rep.err('N18', where, 'codice_trama %s sconosciuto' % ct)
        if ruolo == 'COMPAGNO' and not re.match(r'^C-0[1-8]$', ct):
            rep.err('N18', where, 'COMPAGNO richiede codice_trama C-01..C-08')
        if ruolo == 'PERSONAGGIO' and not ct:
            rep.err('N18', where, 'PERSONAGGIO richiede il codice della missione in cui compare')
        # luoghi della memoria
        mem = ctx.memorial.get(d['map_symbol'])
        if mem:
            if ruolo not in mem['ruoli_ammessi']:
                rep.err('N17', where, 'ruolo %s non ammesso in un luogo della memoria (%s)' % (ruolo, ', '.join(mem['ruoli_ammessi'])))
            if tid:
                rep.err('N17', where, 'nessuna lotta nei luoghi della memoria')
        # note
        if re.search(r'[",{}\\]', d['note']):
            rep.err('N22', where, 'note: vietati virgole, virgolette, graffe e barre inverse (usare ;)')
        # categoria 60/40
        pc = d['post_category']
        counted = ruolo in RUOLI_6040 and vis in ('SEMPRE', 'POST')
        if counted:
            if pc not in ('CAPRO', 'ESTIMATORE'):
                rep.err('N10', where, '%s visibile dopo le dimissioni: post_category CAPRO o ESTIMATORE' % ruolo)
            else:
                c = counts.setdefault(ctx.map_province(mp), [0, 0])
                c[0 if pc == 'CAPRO' else 1] += 1
        elif pc != 'ESENTE':
            rep.err('N10', where, 'post_category ESENTE per ruolo %s / visibile %s' % (ruolo, vis))
    # duplicati
    for mapsym, lst in by_map.items():
        ids = {}
        tiles = {}
        for d in lst:
            if d['npc_id'] in ids:
                rep.err('N04', '%s:%d %s' % (label, d['_line'], mapsym), 'npc_id %s ripetuto (riga %d)' % (d['npc_id'], ids[d['npc_id']]))
            ids[d['npc_id']] = d['_line']
            key = (d['x'], d['y'])
            if key in tiles:
                o = tiles[key]
                if not (o['hide_flag'] and d['hide_flag'] and o['hide_flag'] != d['hide_flag']):
                    rep.err('N06', '%s:%d %s' % (label, d['_line'], mapsym), 'stessa casella di %s (servono due hide_flag diversi)' % o['npc_id'])
            tiles[key] = d
    # 60/40
    for prov in sorted(counts):
        c, e = counts[prov]
        n = c + e
        ok = 58 * n <= 100 * c <= 62 * n and 38 * n <= 100 * e <= 42 * n
        where = 'provincia %s' % prov
        msg = 'CAPRO %d (%.1f%%), ESTIMATORE %d (%.1f%%) su %d' % (c, 100.0 * c / n, e, 100.0 * e / n, n)
        if ok:
            if not rep.quiet:
                print('60/40 %s: %s' % (prov, msg))
        elif finale or n >= soglia:
            rep.err('N20', where, msg + ' (soglie 58-62%% e 38-42%%%s)' % ('' if any(58 * n <= 100 * k <= 62 * n for k in range(n + 1)) else '; con questo totale nessuna ripartizione e\' valida: aggiungere o togliere un NPC'))
        else:
            rep.warn('N20', where, msg + ' (meno di %d NPC: controllo rinviato, usare --finale a fine Modulo 6)' % soglia)
    return rows

# ----------------------------------------------------------------------------------------------


def selftest(ctx, here):
    tdir = os.path.join(here, 'testdata')
    ok = os.path.join(tdir, 'npc_registry_prova_ok.csv')
    ko = os.path.join(tdir, 'npc_registry_prova_ko.csv')
    expected = ctx.reg['strumento']['collaudo']['errori_attesi_ko']
    good = True
    r1 = Report(quiet=True)
    check_registry(ctx, r1)
    check_trainers(ctx, r1)
    rows = check_npc(ctx, r1, ok, 'prova_ok', finale=True)
    print('registro + prova_ok: %d righe, %d errori, %d avvisi' % (len(rows), len(r1.errors), len(r1.warnings)))
    for e in r1.errors:
        print('  inatteso:', e)
    good &= not r1.errors
    r2 = Report(quiet=True)
    rows = check_npc(ctx, r2, ko, 'prova_ko', finale=True)
    got = r2.codes()
    print('prova_ko: %d righe, codici trovati %s' % (len(rows), ' '.join(got)))
    if got != sorted(expected):
        print('  attesi:', ' '.join(sorted(expected)))
        good = False
    print('SELFTEST_OK' if good else 'SELFTEST_FAILED')
    return 0 if good else 1


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description='Controllo del registro di flag, variabili e NPC di Pokemon Trinacria')
    ap.add_argument('--docs', help='cartella docs di pokémon-sicilia (contiene MODULO_2/)')
    ap.add_argument('--repo', help='cartella di pokeheartgold: rifa la scansione dei flag storici e legge sprite/specie/banchi')
    ap.add_argument('--npc', help='data/trinacria/npc_registry.csv da controllare')
    ap.add_argument('--finale', action='store_true', help='60/40 obbligatorio in ogni provincia anche con pochi NPC; con --repo controlla anche che ogni msg_index esista nel banco')
    ap.add_argument('--soglia-minima', type=int, default=20, help='sotto questo numero di NPC il 60/40 e\' solo un avviso')
    ap.add_argument('--selftest', action='store_true', help='collaudo sui CSV di prova in tools/testdata')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    docs = find_docs(a.docs)
    if not docs:
        print('ERRORE R00 docs: MODULO_2/%s non trovato (usare --docs)' % FLAGS_FILE)
        print('REGISTRY_FAILED')
        return 1
    ctx = Context(docs)
    if a.selftest:
        return selftest(ctx, os.path.dirname(os.path.abspath(__file__)))
    rep = Report(quiet=a.quiet)
    scan = None
    if a.repo:
        r = ctx.reg
        scan = scan_repo(a.repo, list(ctx.maps.values()), ctx.excluded,
                         [hexint(x) for x in r['flag']['storico']['letti_per_indice']],
                         [hexint(x) for x in r['variabili']['storico']['letti_per_indice']])
    check_registry(ctx, rep, scan)
    check_trainers(ctx, rep, a.repo)
    if a.npc:
        rows = check_npc(ctx, rep, a.npc, os.path.basename(a.npc), a.finale, a.soglia_minima, a.repo)
        print('NPC controllati: %d' % len(rows))
    print('errori: %d, avvisi: %d' % (len(rep.errors), len(rep.warnings)))
    print('REGISTRY_OK' if not rep.errors else 'REGISTRY_FAILED')
    return 0 if not rep.errors else 1


if __name__ == '__main__':
    sys.exit(main())

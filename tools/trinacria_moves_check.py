#!/usr/bin/env python3
"""Pokemon Trinacria - controllo dei blocchi delle mosse (Modulo 3, blocchi 3.6-3.9).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia oppure da F:\\Progetti\\pokeheartgold):
    python -I tools/trinacria_moves_check.py --selftest
    python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json [blocchi 3.7-3.9]
           [--repo F:/Progetti/pokeheartgold] [--docs <docs>] [--completo]

Ultima riga stampata: MOSSE_OK / SELFTEST_OK (oppure *_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>".
Con --repo si controllano anche simboli, nomi inglesi e dati delle mosse (M05, M08) e si usa il font vero.
"""
import argparse
import collections
import glob
import json
import os
import re
import struct
import sys

# ----------------------------------------------------------------------------------------------
# Limiti del blocco 3.0 (L-08, D-02) e nomi della trama (blocco 3.6, R-MOS-02)

NAME_LIMIT = (15, 72)          # caratteri, px; anche il maiuscolo di msg_0751 sta in 72 px
DESC_PROFILE = (5, 23, 120)    # righe, caratteri per riga, px per riga
MOVES = 467
NAME_CHARS = re.compile(r"^[A-Za-z0-9àèéìòùâêîôûÀÈÉÌÒÙÂÊÎÔÛçëïüñ ’.\-]+$")  # R-GRA-11
SYSTEM_CATEGORIES = ('specie', 'mossa', 'strumento', 'classe', 'abilita', 'tipo', 'natura', 'soprannome', 'dossier')
# mosse che la trama cita col nome italiano ufficiale (R-NOM-01): numero -> nome
# (241: la trama scrive «Giorno di Sole», che sfora L-08 in maiuscolo: deviazione D-19 del blocco 3.8)
TRAMA_IT = {18: 'Turbine', 29: 'Bottintesta', 56: 'Idropompa', 76: 'Solarraggio', 114: 'Nube', 123: 'Smog',
            135: 'Covauova', 148: 'Flash', 157: 'Frana', 164: 'Sostituto', 215: 'Rintoccasana', 220: 'Malcomune', 226: 'Staffetta',
            241: 'Giornodisole', 252: 'Bruciapelo', 312: 'Aromaterapia', 366: 'Ventoincoda'}
TYPES = ['NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL', 'MYSTERY', 'FIRE', 'WATER',
         'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK']
CLASSES = ['fisica', 'speciale', 'stato']
CMD_RE = re.compile(r'\{[^{}]*\}')

# larghezze del membro 0 di files/graphic/font.narc (lette il 18/10/2026); con --repo si leggono dal font vero
WIDTHS = {c: 6 for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdeghkmnopqrstuvwxyz0123456789-!?…()“”àèéòùÀÈÉÌÒÙçëüñ\u2009'}
WIDTHS.update({'i': 3, 'l': 4, 'ì': 4, 'î': 4, ' ': 4, 'f': 5, 'j': 5, '’': 5, '.': 5, ',': 5, ':': 5, ';': 5})

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCS = [os.path.join(HERE, '..', 'docs'), 'F:/Progetti/pokémon-sicilia/docs']
DEFAULT_REPOS = [os.path.join(HERE, '..', '..', 'pokeheartgold'), 'F:/Progetti/pokeheartgold']

# ----------------------------------------------------------------------------------------------


class Report:
    def __init__(self, quiet=False):
        self.errors = []
        self.quiet = quiet

    def err(self, code, where, msg):
        self.errors.append((code, where, msg))
        if not self.quiet:
            print('ERRORE %s %s: %s' % (code, where, msg))

    def codes(self):
        return sorted(set(c for c, _, _ in self.errors))


class Font:
    def __init__(self, repo=None):
        self.widths = dict(WIDTHS)
        self.charmap = None
        if repo:
            cm = {}
            with open(os.path.join(repo, 'tools', 'msgenc', 'charmap.txt'), encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'\s*([0-9A-Fa-f]{4})=(.+)$', line.split('//')[0].rstrip('\n'))
                    if m and len(m.group(2)) == 1:
                        cm.setdefault(m.group(2), int(m.group(1), 16))
            data = open(os.path.join(repo, 'files', 'graphic', 'font', 'font_00000000.bin'), 'rb').read()
            _, wds, n = struct.unpack_from('<III', data, 0)
            table = data[wds:wds + n]
            self.charmap = cm
            self.widths = {c: table[code - 1] for c, code in cm.items() if 0 < code <= n}

    def px(self, s):
        return sum(self.widths.get(c, 6) for c in CMD_RE.sub('', s))

    def known(self, c):
        return c in self.charmap if self.charmap is not None else c in WIDTHS


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def find_docs(arg):
    for d in ([arg] if arg else []) + DEFAULT_DOCS:
        if d and os.path.isfile(os.path.join(d, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json')):
            return d
    return None


def load_glossary(docs, move_files):
    """Glossario 3.0 + aggiunte dei blocchi delle specie (3.1-3.5) + aggiunte dei blocchi delle mosse controllati."""
    out = []
    if docs:
        out += load_json(os.path.join(docs, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json'))['glossario']
        for f in sorted(glob.glob(os.path.join(docs, 'MODULO_3', '3.[1-5]_POKEMON_*.json'))):
            out += load_json(f).get('glossario_aggiunte', [])
    for p in move_files:
        try:
            out += load_json(p).get('glossario_aggiunte', [])
        except Exception:  # noqa: BLE001 - M00 lo segnala check_moves
            pass
    return out


def narc_members(path):
    d = open(path, 'rb').read()
    off = struct.unpack_from('<H', d, 12)[0]
    sz, n = struct.unpack_from('<IH', d, off + 4)
    fat = [struct.unpack_from('<II', d, off + 12 + 8 * i) for i in range(n)]
    o2 = off + sz
    o3 = o2 + struct.unpack_from('<I', d, o2 + 4)[0]
    return [d[o3 + 8 + a:o3 + 8 + b] for a, b in fat]


class Repo:
    """Simboli (include/constants/moves.h), nomi inglesi (msg_0750) e dati (files/poketool/waza/waza_tbl.narc)."""

    def __init__(self, repo):
        txt = open(os.path.join(repo, 'include', 'constants', 'moves.h'), encoding='utf-8').read()
        self.symbols = {s: int(n) for s, n in re.findall(r'#define\s+(MOVE_\w+)\s+(\d+)', txt)
                        if not s.startswith('MOVE_ATTRIBUTE_')}
        self.names = [m['en_US'] for m in load_json(os.path.join(repo, 'files', 'msgdata', 'msg', 'msg_0750.json'))['messages']]
        self.waza = narc_members(os.path.join(repo, 'files', 'poketool', 'waza', 'waza_tbl.narc'))

    def data(self, n):
        eff, cat, pw, ty, acc, pp, ch, _, pri, _ = struct.unpack_from('<HBBBBBBHbB', self.waza[n], 0)
        return {'tipo': 'TYPE_' + TYPES[ty], 'classe': CLASSES[cat], 'potenza': pw, 'precisione': acc, 'pp': pp,
                'effetto': eff, 'probabilita_effetto': ch, 'priorita': pri}

# ----------------------------------------------------------------------------------------------
# Blocchi delle mosse


def bank_0749(lines):
    """Come HeartGold: con 5 righe l'ultima non ha «\\n», con meno righe ce l'hanno tutte (R-MOS-03)."""
    return [x + '\n' for x in lines[:-1]] + [lines[-1] + ('\n' if len(lines) < DESC_PROFILE[0] else '')]


def check_moves(paths, glossary, rep, font, repo=None, entries=None):
    by_index = {}
    system = collections.defaultdict(set)
    for g in glossary:
        if g.get('categoria') == 'mossa' and isinstance(g.get('sostituisce'), dict):
            by_index[g['sostituisce'].get('indice')] = g
        if g.get('categoria') in SYSTEM_CATEGORIES:
            system[str(g.get('forma', '')).lower()].add((g.get('categoria'), g.get('id')))
    seen = {}
    for p in paths:
        try:
            block = load_json(p)['mosse']
        except Exception as ex:  # noqa: BLE001
            rep.err('M00', os.path.basename(p), 'file illeggibile o senza «mosse» (%s)' % ex)
            continue
        for m in block:
            n = m.get('n')
            nm = m.get('nome') or ''
            where = '%s n.%s %s' % (os.path.basename(p), n, nm)
            if not isinstance(n, int) or not 1 <= n <= MOVES or n in seen:
                rep.err('M05', where, 'numero fuori intervallo (1-%d) o ripetuto' % MOVES)
                continue
            seen[n] = p
            if entries is not None:
                entries.append((p, m))
            if repo is not None:
                if repo.symbols.get(m.get('simbolo')) != n:
                    rep.err('M05', where, 'il simbolo %s non vale %d in moves.h' % (m.get('simbolo'), n))
                if n < len(repo.names) and repo.names[n] != m.get('originale'):
                    rep.err('M05', where, '«originale» %s diverso da msg_0750 (%s)' % (m.get('originale'), repo.names[n]))
                if n < len(repo.waza) and repo.data(n) != m.get('dati'):
                    rep.err('M08', where, 'dati diversi da waza_tbl.narc: %s' % repo.data(n))
            up = nm.upper()
            if len(nm) > NAME_LIMIT[0] or font.px(nm) > NAME_LIMIT[1] or font.px(up) > NAME_LIMIT[1] or \
                    not NAME_CHARS.match(nm) or any(not font.known(c) for c in nm):
                rep.err('M01', where, '%d caratteri, %d px (maiuscolo %d px) oltre L-08 o caratteri non ammessi' % (
                    len(nm), font.px(nm), font.px(up)))
            if m.get('maiuscolo') != up:
                rep.err('M02', where, 'maiuscolo «%s» diverso da «%s»' % (m.get('maiuscolo'), up))
            lines = m.get('descrizione') or []
            ok = 1 <= len(lines) <= DESC_PROFILE[0]
            for L in lines:
                if '\n' in L or len(L) > DESC_PROFILE[1] or font.px(L) > DESC_PROFILE[2] or "'" in L or '"' in L or \
                        any(not font.known(c) for c in L):
                    ok = False
            if not ok or m.get('msg_0749') != bank_0749(lines or ['']):
                rep.err('M03', where, 'descrizione fuori dal profilo D-02: %s' % ' | '.join(lines))
            g = by_index.get(n)
            if m.get('lingua') == 'scn':
                if not g or g.get('forma') != nm or g.get('id') != m.get('glossario'):
                    rep.err('M04', where, 'nome assente dal Glossario o diverso (%s)' % (g.get('forma') if g else '—'))
            elif m.get('lingua') == 'it':
                if g or m.get('glossario') is not None:
                    rep.err('M04', where, 'nome italiano ma il Glossario ha una voce per questa mossa (%s)' % (g.get('forma') if g else m.get('glossario')))
            else:
                rep.err('M04', where, 'lingua «%s» non valida (scn, it)' % m.get('lingua'))
            if n in TRAMA_IT and (nm != TRAMA_IT[n] or m.get('lingua') != 'it'):
                rep.err('M10', where, 'la trama la cita col nome italiano ufficiale «%s» (R-MOS-02)' % TRAMA_IT[n])
            elif n not in TRAMA_IT and m.get('lingua') == 'it':
                rep.err('M10', where, 'nome italiano per una mossa che la trama non cita (R-MOS-01)')
            others = {x for x in system.get(nm.lower(), set()) if x[1] != m.get('glossario')}
            if others:
                rep.err('M07', where, 'stesso nome di %s' % ', '.join('%s %s' % x for x in sorted(others)))
            b = m.get('banchi') or {}
            if b.get('msg_0750') != nm or b.get('msg_0751') != m.get('maiuscolo') or b.get('msg_0749') != m.get('msg_0749'):
                rep.err('M06', where, 'banchi diversi dai campi della voce')
    return len(seen)


def check_complete(entries, rep):
    """M09 (dal 3.9, solo con --completo): i blocchi 3.6-3.9 insieme coprono le mosse 1-467 e nessun nome si ripete."""
    nums = {m.get('n') for _, m in entries}
    missing = [n for n in range(1, MOVES + 1) if n not in nums]
    if missing:
        rep.err('M09', 'mosse', '%d mosse assenti dai blocchi (%s%s)' % (
            len(missing), ', '.join(str(n) for n in missing[:10]), '…' if len(missing) > 10 else ''))
    names = collections.defaultdict(list)
    for _, m in entries:
        names[(m.get('nome') or '').lower()].append(m.get('n'))
    for nm, ns in sorted(names.items()):
        if len(ns) > 1:
            rep.err('M09', 'nome %s' % nm, 'usato da più mosse: %s' % ', '.join(str(n) for n in ns))


def run_check(args, rep):
    font = Font(args.repo)
    docs = find_docs(args.docs)
    glossary = load_glossary(docs, args.files)
    repo = Repo(args.repo) if args.repo else None
    entries = []
    n = check_moves(args.files, glossary, rep, font, repo, entries)
    print('mosse controllate: %d' % n)
    if getattr(args, 'completo', False):
        check_complete(entries, rep)


def selftest():
    docs = find_docs(None)
    ok_files = sorted(glob.glob(os.path.join(HERE, '..', 'docs', 'MODULO_3', '3.[6-9]_MOSSE_*.json')))
    ko = os.path.join(HERE, 'testdata', 'mosse_prova_ko.json')
    repo = next((r for r in DEFAULT_REPOS if os.path.isfile(os.path.join(r, 'include', 'constants', 'moves.h'))), None)
    print('repository per il collaudo: %s' % (repo or 'nessuno (M08 non si controlla)'))
    good = True

    class A:
        pass
    a = A()
    a.files, a.repo, a.docs, a.completo = ok_files, repo, docs, len(ok_files) == 4
    rep = Report(quiet=True)
    run_check(a, rep)
    if not ok_files or rep.errors:
        good = False
        print('collaudo: i blocchi %s danno errori: %s' % (', '.join(os.path.basename(f)[:3] for f in ok_files), rep.codes()))
        for e in rep.errors[:10]:
            print('   ', *e)
    rep2 = Report(quiet=True)
    a.files, a.completo = [ko], True
    run_check(a, rep2)
    expected = [c for c in load_json(ko)['errori_attesi'] if repo or c != 'M08']
    if rep2.codes() != sorted(expected):
        good = False
        print('collaudo: mosse_prova_ko.json dà %s invece di %s' % (rep2.codes(), sorted(expected)))
    print('SELFTEST_OK' if good else 'SELFTEST_FAILED')
    return 0 if good else 1


def main():
    # la console di Windows (cp1252) non ha ’ e simili: senza questo un messaggio d'errore fa crashare lo strumento
    sys.stdout.reconfigure(errors='backslashreplace')
    if '--selftest' in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('check')
    c.add_argument('files', nargs='+')
    c.add_argument('--repo')
    c.add_argument('--docs')
    c.add_argument('--completo', action='store_true', help='dal 3.9: M09, tutte le mosse 1-467 una volta sola')
    args = ap.parse_args()
    rep = Report()
    run_check(args, rep)
    print('MOSSE_OK' if not rep.errors else 'MOSSE_FAILED')
    return 1 if rep.errors else 0


if __name__ == '__main__':
    sys.exit(main())

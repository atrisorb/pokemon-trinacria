#!/usr/bin/env python3
"""Pokemon Trinacria - controllo dei blocchi degli strumenti (Modulo 3, blocchi 3.10-3.12).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia oppure da F:\\Progetti\\pokeheartgold):
    python -I tools/trinacria_items_check.py --selftest
    python -I tools/trinacria_items_check.py check docs/MODULO_3/3.10_STRUMENTI_1-180.json [blocchi 3.11-3.12]
           [--repo F:/Progetti/pokeheartgold] [--docs <docs>] [--completo]

Ultima riga stampata: STRUMENTI_OK / SELFTEST_OK (oppure *_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>".
Con --repo si controllano anche simboli, nomi inglesi, dati e negozi (S05, S11, S12) e si usa il font vero.
"""
import argparse
import collections
import csv
import glob
import json
import os
import re
import struct
import sys

# ----------------------------------------------------------------------------------------------
# Limiti del blocco 3.0 (L-03, L-04, L-05, D-03) e decisioni del blocco 3.10 (R-STR-01…10)

NAME_LIMIT = (15, 72)            # L-03: caratteri, px
ART_LIMIT = (20, 90)             # L-04
PLURAL_LIMIT = (20, 82)          # L-05
DESC_PROFILE = (3, 41, 215)      # D-03: righe, caratteri per riga, px per riga
ITEMS = 536
EMPTY_SLOTS = range(113, 135)    # ITEM_UNUSED_113…134: restano «???» (R-STR-02)
NAME_CHARS = re.compile(r"^[A-Za-z0-9àèéìòùâêîôûÀÈÉÌÒÙÂÊÎÔÛçëïüñ ’.\-]+$")  # R-GRA-11
SYSTEM_CATEGORIES = ('specie', 'mossa', 'strumento', 'classe', 'abilita', 'tipo', 'natura', 'soprannome', 'dossier')
# strumenti che la trama cita col nome italiano (R-STR-01): numero -> nome
TRAMA_IT = {43: 'Genovese'}
# strumenti della trama che hanno la stessa parola di un soprannome (R-NOM-02): numero
TRAMA_SOPRANNOMI = {33}
# livello del bancone dei Centri (src/scrcmd_mart.c, ScrCmd_MartBuy) -> Dossier necessari
TIER_DOSSIER = {1: 0, 2: 1, 3: 3, 4: 5, 5: 7, 6: 8}
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


def load_glossary(docs, item_files):
    """Glossario 3.0 + aggiunte dei blocchi delle specie e delle mosse (3.1-3.9) + aggiunte dei blocchi controllati."""
    out = []
    if docs:
        out += load_json(os.path.join(docs, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json'))['glossario']
        for f in sorted(glob.glob(os.path.join(docs, 'MODULO_3', '3.[1-9]_*.json'))):
            out += load_json(f).get('glossario_aggiunte', [])
    for p in item_files:
        try:
            out += load_json(p).get('glossario_aggiunte', [])
        except Exception:  # noqa: BLE001 - S00 lo segnala check_items
            pass
    return out

# ----------------------------------------------------------------------------------------------
# Forme dei banchi msg_0223 e msg_0224 (R-NOM-09, R-NOM-10, R-STR-03)


def with_article(name, gender):
    """Articolo indeterminativo italiano davanti al nome, coi colori di HeartGold (R-NOM-09)."""
    low = name.lower()
    vowel = low[:1] in 'aeiouàèéìòù'
    impure = (low[:1] == 's' and low[1:2] not in 'aeiouàèéìòù') or low[:1] in 'zxy' or low[:2] in ('gn', 'ps')
    if gender == 'f':
        art = 'un’' if vowel else 'una '
    else:
        art = 'uno ' if impure else 'un '
    return '%s{COLOR 255}%s{COLOR 0}' % (art, name)


def plural(name):
    """R-NOM-10 e R-STR-03: composti, nomi in -Ball e abbreviazioni invariabili; -u/-a -> -i
    (-iu/-ia -> -i, -cu/-ca -> -chi, -gu/-ga -> -ghi)."""
    if ' ' in name or '.' in name or any(c.isupper() for c in name[1:]) or name[-1:] not in 'ua':
        return name
    stem = name[:-1]
    if stem[-1:] == 'i':
        return stem
    return stem + ('hi' if stem[-1:] in 'cg' else 'i')

# ----------------------------------------------------------------------------------------------
# Repository


class Repo:
    """Simboli (include/constants/items.h), nomi inglesi (msg_0222) e dati (src/item.c + item_data.csv)."""

    def __init__(self, repo):
        txt = open(os.path.join(repo, 'include', 'constants', 'items.h'), encoding='utf-8').read()
        txt = txt[txt.index('#define ITEM_NONE'):]
        self.symbols = {}
        for s, n in re.findall(r'^#define\s+(ITEM_\w+)\s+(\d+)\s*$', txt, re.M):
            self.symbols.setdefault(int(n), s)
        self.by_symbol = {s: n for n, s in self.symbols.items()}
        self.names = [m['en_US'] for m in load_json(os.path.join(repo, 'files', 'msgdata', 'msg', 'msg_0222.json'))['messages']]
        src = open(os.path.join(repo, 'src', 'item.c'), encoding='utf-8').read()
        self.data_index = {s: int(i) for s, i in re.findall(r'\[(ITEM_\w+)\]\s*=\s*\{\s*NARC_item_data_(\d+)_bin', src)}
        with open(os.path.join(repo, 'files', 'itemtool', 'itemdata', 'item_data.csv'), encoding='utf-8') as f:
            self.rows = list(csv.DictReader(f))

    def data(self, n):
        r = self.rows[self.data_index.get(self.symbols.get(n), 0)]
        return {'prezzo': int(r['price']), 'tasca': r['fieldPocket'], 'effetto_tenuto': r['holdEffect'],
                'parametro_effetto': int(r['holdEffectParam'])}


class Marts:
    """Bancone dei Centri a livelli (_020FBF22) e banconi speciali (_0210FA3C) di src/scrcmd_mart.c."""

    def __init__(self, repo):
        src = open(os.path.join(repo, 'src', 'scrcmd_mart.c'), encoding='utf-8').read()
        badge = src[src.index('_020FBF22[]'):]
        badge = badge[:badge.index('};')]
        self.tiers = {s: int(t) for s, t in re.findall(r'\{\s*(ITEM_\w+),\s*(\d+)\s*\}', badge)}
        lists = {name: re.findall(r'ITEM_\w+', body) for name, body in re.findall(r'const u16 (_020FB\w+)\[\] = \{([^}]*)\}', src)}
        order = src[src.index('*_0210FA3C[]'):]
        order = re.findall(r'(_020FB\w+)', order[:order.index('};')])
        self.special = [lists[o] for o in order]

    def where(self, n, assignment, repo):
        sym = repo.symbols[n]
        out = []
        if sym in self.tiers:
            out.append({'bancone': 'tutti i Centri Pokémon', 'dal_dossier': TIER_DOSSIER[self.tiers[sym]],
                        'livello_scrcmd_mart': self.tiers[sym]})
        for i, items in enumerate(self.special):
            if sym in items:
                out.append({'bancone': 'speciale %d' % i, 'mappa': assignment[i]})
        return out

# ----------------------------------------------------------------------------------------------
# Blocchi degli strumenti


def bank_0221(lines):
    """D-03: righe separate da «\\n», nessun separatore finale."""
    return [x + '\n' for x in lines[:-1]] + [lines[-1]]


def check_items_list(items, fname, glossary, rep, font, repo=None, seen=None, marts=None, assignment=None):
    seen = {} if seen is None else seen
    by_index = {}
    system = collections.defaultdict(set)
    for g in glossary:
        if g.get('categoria') == 'strumento' and isinstance(g.get('sostituisce'), dict):
            by_index[g['sostituisce'].get('indice')] = g
        if g.get('categoria') in SYSTEM_CATEGORIES:
            system[str(g.get('forma', '')).lower()].add((g.get('categoria'), g.get('id')))
    for m in items:
        n = m.get('n')
        nm = m.get('nome') or ''
        where = '%s n.%s %s' % (fname, n, nm)
        if not isinstance(n, int) or not 1 <= n <= ITEMS or n in seen:
            rep.err('S05', where, 'numero fuori intervallo (1-%d) o ripetuto' % ITEMS)
            continue
        seen[n] = fname
        if repo is not None:
            if repo.symbols.get(n) != m.get('simbolo'):
                rep.err('S05', where, 'il simbolo %s non vale %d in items.h' % (m.get('simbolo'), n))
            if n < len(repo.names) and repo.names[n] != m.get('originale'):
                rep.err('S05', where, '«originale» %s diverso da msg_0222 (%s)' % (m.get('originale'), repo.names[n]))
        if (n in EMPTY_SLOTS) != bool(m.get('vuoto')):
            rep.err('S10', where, 'gli slot 113-134 sono vuoti e restano «???», gli altri hanno un nome (R-STR-02)')
            continue
        if m.get('vuoto'):
            if m.get('nome') is not None or m.get('glossario') is not None:
                rep.err('S10', where, 'slot vuoto con un nome')
            continue
        if repo is not None and repo.data(n) != m.get('dati'):
            rep.err('S11', where, 'dati diversi da item_data.csv: %s' % repo.data(n))
        if len(nm) > NAME_LIMIT[0] or font.px(nm) > NAME_LIMIT[1] or not NAME_CHARS.match(nm) or \
                any(not font.known(c) for c in nm):
            rep.err('S01', where, '%d caratteri, %d px oltre L-03 o caratteri non ammessi' % (len(nm), font.px(nm)))
        art = m.get('con_articolo') or ''
        if m.get('genere') not in ('m', 'f') or art != with_article(nm, m.get('genere')) or \
                len(CMD_RE.sub('', art)) > ART_LIMIT[0] or font.px(art) > ART_LIMIT[1]:
            rep.err('S02', where, 'forma con l’articolo «%s» (%d px) diversa da R-NOM-09 o oltre L-04' % (art, font.px(art)))
        pl = m.get('plurale') or ''
        if not pl or len(pl) > PLURAL_LIMIT[0] or font.px(pl) > PLURAL_LIMIT[1] or not NAME_CHARS.match(pl):
            rep.err('S03', where, 'plurale «%s» (%d px) oltre L-05' % (pl, font.px(pl)))
        lines = m.get('descrizione') or []
        ok = 1 <= len(lines) <= DESC_PROFILE[0]
        for L in lines:
            if '\n' in L or len(L) > DESC_PROFILE[1] or font.px(L) > DESC_PROFILE[2] or "'" in L or '"' in L or \
                    any(not font.known(c) for c in L):
                ok = False
        if not ok or (m.get('banchi') or {}).get('msg_0221') != bank_0221(lines or ['']):
            rep.err('S04', where, 'descrizione fuori dal profilo D-03: %s' % ' | '.join(lines))
        g = by_index.get(n)
        if m.get('lingua') == 'scn':
            if not g or g.get('forma') != nm or g.get('id') != m.get('glossario') or g.get('genere') != m.get('genere') or \
                    g.get('plurale') != pl or g.get('con_articolo') != art:
                rep.err('S07', where, 'nome assente dal Glossario o diverso (%s)' % (g.get('forma') if g else '—'))
        elif m.get('lingua') == 'it':
            if g or m.get('glossario') is not None or TRAMA_IT.get(n) != nm:
                rep.err('S07', where, 'nome italiano solo per gli strumenti che la trama cita così (R-STR-01)')
        else:
            rep.err('S07', where, 'lingua «%s» non valida (scn, it)' % m.get('lingua'))
        others = {x for x in system.get(nm.lower(), set()) if x[1] != m.get('glossario') and
                  not (n in TRAMA_SOPRANNOMI and x[0] == 'soprannome')}
        if others:
            rep.err('S08', where, 'stesso nome di %s' % ', '.join('%s %s' % x for x in sorted(others)))
        b = m.get('banchi') or {}
        if b.get('msg_0222') != nm or b.get('msg_0223') != art or b.get('msg_0224') != pl:
            rep.err('S06', where, 'banchi diversi dai campi della voce')
        ott = m.get('ottenimento') or {}
        if marts is not None and assignment is not None and repo is not None:
            if ott.get('negozi') != marts.where(n, assignment, repo):
                rep.err('S12', where, 'negozi diversi da src/scrcmd_mart.c e dal piano dei negozi')
        if not ott.get('negozi') and not ott.get('altro'):
            rep.err('S12', where, 'nessun modo di ottenerlo')
    return seen


def check_items(paths, glossary, rep, font, repo=None, marts=None):
    seen = {}
    entries = []
    assignment = None
    blocks = []
    for p in paths:
        try:
            b = load_json(p)
            blocks.append((p, b['strumenti']))
        except Exception as ex:  # noqa: BLE001
            rep.err('S00', os.path.basename(p), 'file illeggibile o senza «strumenti» (%s)' % ex)
            continue
        if b.get('piano_negozi'):
            assignment = {int(x['indice']): x['mappa'] for x in b['piano_negozi']['banconi_speciali']}
    for p, items in blocks:
        check_items_list(items, os.path.basename(p), glossary, rep, font, repo, seen, marts, assignment)
        entries += items
    return entries


def check_complete(entries, rep):
    """S09 (dal 3.12, solo con --completo): i blocchi 3.10-3.12 insieme coprono gli strumenti 1-536 e nessun nome si ripete."""
    nums = {m.get('n') for m in entries}
    missing = [n for n in range(1, ITEMS + 1) if n not in nums]
    if missing:
        rep.err('S09', 'strumenti', '%d strumenti assenti dai blocchi (%s%s)' % (
            len(missing), ', '.join(str(n) for n in missing[:10]), '…' if len(missing) > 10 else ''))
    names = collections.defaultdict(list)
    for m in entries:
        if m.get('nome'):
            names[m['nome'].lower()].append(m.get('n'))
    for nm, ns in sorted(names.items()):
        if len(ns) > 1:
            rep.err('S09', 'nome %s' % nm, 'usato da più strumenti: %s' % ', '.join(str(n) for n in ns))


def run_check(args, rep):
    font = Font(args.repo)
    docs = find_docs(args.docs)
    glossary = load_glossary(docs, args.files)
    repo = Repo(args.repo) if args.repo else None
    marts = Marts(args.repo) if args.repo else None
    entries = check_items(args.files, glossary, rep, font, repo, marts)
    print('strumenti controllati: %d' % len(entries))
    if getattr(args, 'completo', False):
        check_complete(entries, rep)


def selftest():
    docs = find_docs(None)
    ok_files = sorted(glob.glob(os.path.join(HERE, '..', 'docs', 'MODULO_3', '3.1[0-2]_STRUMENTI_*.json')))
    ko = os.path.join(HERE, 'testdata', 'strumenti_prova_ko.json')
    repo = next((r for r in DEFAULT_REPOS if os.path.isfile(os.path.join(r, 'include', 'constants', 'items.h'))), None)
    print('repository per il collaudo: %s' % (repo or 'nessuno (S05, S11, S12 non si controllano)'))
    good = True

    class A:
        pass
    a = A()
    a.files, a.repo, a.docs, a.completo = ok_files, repo, docs, len(ok_files) == 3
    rep = Report(quiet=True)
    run_check(a, rep)
    if not ok_files or rep.errors:
        good = False
        print('collaudo: i blocchi %s danno errori: %s' % (', '.join(os.path.basename(f)[:4] for f in ok_files), rep.codes()))
        for e in rep.errors[:10]:
            print('   ', *e)
    rep2 = Report(quiet=True)
    a.files, a.completo = [ko], True
    run_check(a, rep2)
    expected = [c for c in load_json(ko)['errori_attesi'] if repo or c not in ('S05', 'S11', 'S12')]
    if rep2.codes() != sorted(expected):
        good = False
        print('collaudo: strumenti_prova_ko.json dà %s invece di %s' % (rep2.codes(), sorted(expected)))
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
    c.add_argument('--completo', action='store_true', help='dal 3.12: S09, tutti gli strumenti 1-536 una volta sola')
    args = ap.parse_args()
    rep = Report()
    run_check(args, rep)
    print('STRUMENTI_OK' if not rep.errors else 'STRUMENTI_FAILED')
    return 1 if rep.errors else 0


if __name__ == '__main__':
    sys.exit(main())

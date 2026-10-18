#!/usr/bin/env python3
"""Pokemon Trinacria - controllo del Glossario bloccato e dei nomi (Modulo 3, blocco 3.0).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia oppure da F:\\Progetti\\pokeheartgold):
    python -I tools/trinacria_glossary_check.py --selftest
    python -I tools/trinacria_glossary_check.py glossary docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json [altri blocchi…]
    python -I tools/trinacria_glossary_check.py names --repo F:/Progetti/pokeheartgold [--glossary <json…> --applied]
    python -I tools/trinacria_glossary_check.py text --glossary <json…> [--docs <cartella docs>] <testi.json…>
    python -I tools/trinacria_glossary_check.py merge <json…> -o data/trinacria/GLOSSARIO_BLOCCATO.json

Ultima riga stampata: GLOSSARY_OK / NAMES_OK / TEXT_OK / MERGE_OK / SELFTEST_OK (oppure *_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>" (blocca) o "AVVISO <codice> ..." (non blocca).
I file del Glossario sono JSON con la chiave "glossario" (blocco 3.0, file unito) o "glossario_aggiunte"
(blocchi successivi); le aree dialettali vengono dalla chiave "aree" del blocco 3.0.
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
# Costanti del blocco 3.0 (sezione «limiti»): il comando glossary le confronta col file (codice G13).

LIMITS = {  # categoria del Glossario -> (id limite, caratteri, px, controlla anche il maiuscolo)
    'specie': ('L-01', 10, 60, False),
    'strumento': ('L-03', 15, 72, False),
    'classe': ('L-06', 15, 70, False),
    'mossa': ('L-08', 15, 72, True),
    'abilita': ('L-09', 15, 72, True),
    'tipo': ('L-10', 10, 60, False),
    'natura': ('L-11', 7, 42, False),
    'categoria_dex': ('L-12', 19, 110, False),
}
ART_LIMITS = {'specie': ('L-02', 20, 76), 'strumento': ('L-04', 20, 90), 'classe': ('L-07', 20, 80)}
PLURAL_LIMIT = ('L-05', 20, 82)
NAME_CATEGORIES = ('specie', 'mossa', 'strumento', 'classe', 'abilita', 'tipo', 'natura')
CATEGORIES = NAME_CATEGORIES + ('categoria_dex', 'dossier', 'soprannome', 'termine', 'nome_proprio', 'luogo')
LINGUE = ('scn', 'it', 'nome')
FONTI = ('MCP', 'architetto')
REQUIRED = ('id', 'forma', 'categoria', 'lingua', 'aree', 'vietata_in', 'forme', 'varianti_vietate', 'fonte', 'significato')

# banco HeartGold -> (id limite, caratteri visibili, px); copie in maiuscolo; numero di messaggi
BANK_LIMITS = {
    '0237': ('L-01', 10, 60), '0238': ('L-02', 20, 76), '0222': ('L-03', 15, 72), '0223': ('L-04', 20, 90),
    '0224': ('L-05', 20, 82), '0730': ('L-06', 15, 70), '0731': ('L-07', 20, 80), '0750': ('L-08', 15, 72),
    '0751': ('L-08', 15, 72), '0720': ('L-09', 15, 72), '0721': ('L-09', 15, 72), '0735': ('L-10', 10, 60),
    '0034': ('L-11', 7, 42), '0816': ('L-12', 19, 110), '0279': ('L-14', 16, 94),
}
BANK_COUNTS = {'0237': 496, '0238': 496, '0222': 537, '0223': 537, '0224': 537, '0730': 129, '0731': 129,
               '0750': 468, '0751': 468, '0720': 124, '0721': 124, '0735': 18, '0034': 25, '0816': 494,
               '0803': 494, '0749': 468, '0221': 537, '0722': 124}
UPPER_COPIES = {'0751': '0750', '0721': '0720'}
DESC_PROFILES = {  # banco -> (id, righe, caratteri per riga, px per riga)
    '0803': ('D-01', 3, 43, 222), '0749': ('D-02', 5, 23, 120), '0221': ('D-03', 3, 41, 215), '0722': ('D-04', 2, 26, 136),
}

# larghezze del membro 0 di files/graphic/font.narc (lette il 18/10/2026) per i caratteri ammessi nei nomi;
# con --repo si leggono dal font vero.
WIDTHS = {c: 6 for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdeghkmnopqrstuvwxyz0123456789-!?…àèéòùâêôûÀÈÉÌÒÙÂÊÎÔÛçëüñÇËÏÜÑ'}
WIDTHS.update({'i': 3, 'l': 4, 'ì': 4, 'î': 4, 'ï': 4, ' ': 4, 'f': 5, 'j': 5, '’': 5, '.': 5, ',': 5})
NAME_CHARS = set(WIDTHS) - set('!?…,')
CMD_RE = re.compile(r'\{[^{}]*\}')
TOKEN_RE = re.compile(r"’?[^\W\d_]+’?")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCS = [os.path.join(HERE, '..', 'docs'), 'F:/Progetti/pokémon-sicilia/docs']
BLOCK_30 = os.path.join('MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json')

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

# ----------------------------------------------------------------------------------------------
# Font e charmap


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


def visible(s):
    return len(CMD_RE.sub('', s))

# ----------------------------------------------------------------------------------------------
# Lettura del Glossario


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_glossary(paths, rep):
    """Restituisce (voci, aree, limiti_del_file) unendo i file nell'ordine dato."""
    entries, areas, file_limits = [], None, None
    for p in paths:
        try:
            j = load_json(p)
        except (OSError, ValueError) as e:
            rep.err('G00', os.path.basename(p), 'file illeggibile: %s' % e)
            continue
        part = j.get('glossario', j.get('glossario_aggiunte'))
        if part is None:
            rep.err('G00', os.path.basename(p), 'manca la chiave "glossario" o "glossario_aggiunte"')
            continue
        for e in part:
            e = dict(e)
            e['_file'] = os.path.basename(p)
            entries.append(e)
        if j.get('aree') and areas is None:
            areas = {a['codice']: a.get('padre') for a in j['aree']}
        if j.get('limiti') and file_limits is None:
            file_limits = j['limiti']
    if areas is None:
        rep.err('G05', 'aree', 'nessun file contiene la chiave "aree" (serve il blocco 3.0 o il file unito)')
        areas = {}
    return entries, areas, file_limits


def ancestors(areas, code):
    out = []
    while code:
        out.append(code)
        code = areas.get(code)
    return out


def check_glossary(entries, areas, rep, font, file_limits=None):
    if file_limits:
        by_id = {x['id']: x for x in file_limits}
        for cat, (lid, cc, pp, _) in LIMITS.items():
            x = by_id.get(lid)
            if x and (x['limite_vincolante']['caratteri'], x['limite_vincolante']['px']) != (cc, pp):
                rep.err('G13', lid, 'limite del file %s/%s diverso da quello dello strumento %s/%s'
                        % (x['limite_vincolante']['caratteri'], x['limite_vincolante']['px'], cc, pp))
    ids, keys = {}, {}
    names = collections.defaultdict(list)
    forms = collections.defaultdict(set)
    for e in entries:
        where = '%s %s' % (e.get('id', '?'), e.get('forma', '?'))
        missing = [k for k in REQUIRED if k not in e]
        if missing:
            rep.err('G01', where, 'campi mancanti: %s' % ', '.join(missing))
            continue
        if e['categoria'] not in CATEGORIES or e['lingua'] not in LINGUE or e['fonte'] not in FONTI \
                or not isinstance(e['forme'], list) or not e['forme']:
            rep.err('G01', where, 'categoria, lingua, fonte o forme non validi')
            continue
        if e['id'] in ids:
            rep.err('G12', where, 'id ripetuto (anche in %s)' % ids[e['id']])
        ids[e['id']] = e['_file']
        key = (e['forma'].lower(), e['categoria'])
        if key in keys:
            rep.err('G02', where, 'forma già presente nella stessa categoria (%s)' % keys[key])
        keys[key] = e['id']
        if e['categoria'] in NAME_CATEGORIES:
            names[e['forma'].lower()].append(e['id'])
        for f in e['forme']:
            forms[f.lower()].add(e['id'])
        for a in list(e['aree']) + list(e['vietata_in']):
            if a not in areas:
                rep.err('G05', where, 'area sconosciuta %s' % a)
        texts = [e['forma']] + list(e['forme']) + list(e['varianti_vietate'])
        if any("'" in t or '"' in t for t in texts[:len(e['forme']) + 1]):
            rep.err('G10', where, 'apostrofo o virgolette dritti (si usa ’)')
        for c in e['forma']:
            if not font.known(c) or (e['categoria'] in NAME_CATEGORIES and c not in NAME_CHARS):
                rep.err('G06', where, 'carattere non ammesso %r' % c)
                break
        if e['fonte'] == 'MCP' and not e.get('lemma_mcp'):
            rep.err('G11', where, 'fonte MCP senza lemma_mcp')
        cat = e['categoria']
        if cat in LIMITS:
            lid, cc, pp, up = LIMITS[cat]
            n, p = len(e['forma']), font.px(e['forma'])
            if n > cc or p > pp:
                rep.err('G07', where, '%d caratteri, %d px: oltre %s (%d caratteri, %d px)' % (n, p, lid, cc, pp))
            if up and font.px(e['forma'].upper()) > pp:
                rep.err('G08', where, 'il maiuscolo %s misura %d px > %d' % (e['forma'].upper(), font.px(e['forma'].upper()), pp))
        if cat in ART_LIMITS and e.get('con_articolo'):
            lid, cc, pp = ART_LIMITS[cat]
            a = e['con_articolo']
            if visible(a) > cc or font.px(a) > pp or e['forma'] not in a:
                rep.err('G09', where, 'forma con l’articolo «%s» (%d px) oltre %s (%d px) o senza il nome' % (CMD_RE.sub('', a), font.px(a), lid, pp))
        if cat == 'strumento' and e.get('plurale'):
            lid, cc, pp = PLURAL_LIMIT
            if visible(e['plurale']) > cc or font.px(e['plurale']) > pp:
                rep.err('G09', where, 'plurale «%s» (%d px) oltre %s (%d px)' % (e['plurale'], font.px(e['plurale']), lid, pp))
    for n, who in names.items():
        if len(who) > 1:
            rep.err('G03', n, 'stesso nome in più voci di nomi di sistema: %s' % ', '.join(who))
    for e in entries:
        for v in e.get('varianti_vietate', []):
            if v.lower() in forms:
                rep.err('G04', '%s %s' % (e.get('id'), e.get('forma')),
                        'la variante vietata «%s» è una forma ammessa (%s)' % (v, ', '.join(sorted(forms[v.lower()]))))
    return len(entries)

# ----------------------------------------------------------------------------------------------
# Banchi dei nomi nel repository


def bank_texts(repo, b):
    files = glob.glob(os.path.join(repo, 'files', 'msgdata', 'msg', 'msg_%s*.json' % b))
    if not files:
        return None
    out = []
    for m in load_json(files[0])['messages']:
        t = m.get('en_US', '')
        out.append(''.join(t) if isinstance(t, list) else t)
    return out


def check_names(repo, rep, font, entries=None, applied=False):
    banks = {}
    for b in sorted(set(BANK_LIMITS) | set(BANK_COUNTS)):
        t = bank_texts(repo, b)
        if t is None:
            rep.err('N00', 'msg_%s' % b, 'banco non trovato')
            continue
        banks[b] = t
        if b in BANK_COUNTS and len(t) != BANK_COUNTS[b]:
            rep.err('N04', 'msg_%s' % b, '%d messaggi invece di %d: i banchi dei nomi non si allungano né si accorciano' % (len(t), BANK_COUNTS[b]))
    for b, (lid, cc, pp) in BANK_LIMITS.items():
        for i, t in enumerate(banks.get(b, [])):
            n, p = visible(t), font.px(t)
            if n > cc or p > pp:
                rep.err('N01', 'msg_%s_%05d' % (b, i), '«%s»: %d caratteri, %d px oltre %s (%d, %d)' % (CMD_RE.sub('', t), n, p, lid, cc, pp))
            for c in CMD_RE.sub('', t):
                if font.charmap is not None and c not in font.charmap:
                    rep.err('N06', 'msg_%s_%05d' % (b, i), 'carattere %r assente dalla charmap' % c)
    for up, src in UPPER_COPIES.items():
        for i, (a, u) in enumerate(zip(banks.get(src, []), banks.get(up, []))):
            if a.upper() != u:
                rep.err('N02', 'msg_%s_%05d' % (up, i), '«%s» non è il maiuscolo di msg_%s («%s»)' % (u, src, a))
    for b, (did, nl, cc, pp) in DESC_PROFILES.items():
        for i, t in enumerate(banks.get(b, [])):
            if not t.strip('\n'):
                continue
            if '\r' in t or '\f' in t:
                rep.err('N03', 'msg_%s_%05d' % (b, i), '%s: solo «\\n» come separatore' % did)
            lines = t.split('\n')
            if lines[-1] == '':
                lines = lines[:-1]
            if len(lines) > nl:
                rep.err('N03', 'msg_%s_%05d' % (b, i), '%s: %d righe (massimo %d)' % (did, len(lines), nl))
            for L in lines:
                if visible(L) > cc or font.px(L) > pp:
                    rep.err('N03', 'msg_%s_%05d' % (b, i), '%s: riga «%s» %d caratteri, %d px (massimo %d, %d)' % (did, CMD_RE.sub('', L), visible(L), font.px(L), cc, pp))
    if entries:
        done = todo = 0
        for e in entries:
            s = e.get('sostituisce') or {}
            b, i = str(s.get('banco', '')).replace('msg_', ''), s.get('indice')
            if b in banks and isinstance(i, int):
                if 0 <= i < len(banks[b]) and banks[b][i] == e['forma']:
                    done += 1
                else:
                    todo += 1
                    if applied:
                        rep.err('N05', '%s %s' % (e['id'], e['forma']), 'msg_%s_%05d contiene «%s»' % (b, i, banks[b][i] if 0 <= i < len(banks[b]) else '?'))
        print('nomi del Glossario già nel repository: %d, ancora da applicare: %d' % (done, todo))
    return banks

# ----------------------------------------------------------------------------------------------
# Testi del Modulo 6


def load_places(docs):
    places = set()
    for f in glob.glob(os.path.join(docs, 'MODULO_2', '2.[123]_*.json')):
        for s in load_json(f).get('sezioni_pokegear', []):
            places.update(tok.lower() for tok in TOKEN_RE.findall(s.get('testo', '')))
    return places


def build_text_index(entries):
    single = collections.defaultdict(list)
    multi = []
    for e in entries:
        for f in e['forme']:
            f = f.lower()
            inner = f.strip('’')
            if re.search(r"[ .\-]", f) or '’' in inner:
                multi.append((f, e))
            else:
                single[f].append(e)
        forma = e['forma']
        if re.search(r'[a-zàèéìòù][A-Z]', forma) or re.search(r'[ .\-]', forma):
            multi.append((forma.lower(), e))
    multi.sort(key=lambda x: -len(x[0]))
    banned = collections.defaultdict(list)
    for e in entries:
        for v in e['varianti_vietate']:
            banned[v.lower()].append(e)
    return single, multi, banned


def entry_ok(e, area, areas):
    if 'IT' in e['aree']:
        return True
    anc = ancestors(areas, area)
    return any(a in anc for a in e['aree'])


def entry_banned(e, area, areas):
    anc = ancestors(areas, area)
    return any(a in anc for a in e['vietata_in'])


def check_texts(paths, entries, areas, rep, places=frozenset()):
    single, multi, banned = build_text_index(entries)
    n = 0
    for p in paths:
        try:
            items = load_json(p).get('testi', [])
        except (OSError, ValueError) as e:
            rep.err('T00', os.path.basename(p), 'file illeggibile: %s' % e)
            continue
        for it in items:
            n += 1
            where = '%s %s' % (os.path.basename(p), it.get('id', '?'))
            lingua, area = it.get('lingua'), it.get('area')
            if lingua not in ('scn', 'it') or area not in areas:
                rep.err('T01', where, 'lingua (scn/it) o area non valide: %r %r' % (lingua, area))
                continue
            txt = it.get('testo', '')
            txt = ''.join(txt) if isinstance(txt, list) else txt
            low = ' ' + re.sub(r'[\n\r\f]', ' ', CMD_RE.sub(' ', txt)).lower() + ' '
            for v, es in banned.items():
                if re.search(r'(?<![\w’])' + re.escape(v) + r'(?![\w’])', low):
                    rep.err('T03', where, 'variante vietata «%s»: si scrive «%s»' % (v, es[0]['forma']))
            for f, e in multi:
                pat = r'(?<![\w’])' + re.escape(f) + r'(?!\w)'
                if re.search(pat, low):
                    if entry_banned(e, area, areas):
                        rep.err('T04', where, '«%s» è vietata nell’area %s' % (e['forma'], area))
                    elif lingua == 'scn' and not entry_ok(e, area, areas):
                        rep.err('T02', where, '«%s» non è ammessa nell’area %s (aree %s)' % (e['forma'], area, ','.join(e['aree'])))
                    low = re.sub(pat, ' ', low)
            for tok in TOKEN_RE.findall(low):
                es = single.get(tok)
                if not es and tok.endswith('’') and single.get(tok[:-1]):
                    es = single.get(tok[:-1])
                if es and all(entry_banned(e, area, areas) for e in es):
                    rep.err('T04', where, '«%s» è vietata nell’area %s' % (tok, area))
                    continue
                if lingua != 'scn':
                    continue
                if es and any(entry_ok(e, area, areas) for e in es):
                    continue
                if tok in places:
                    continue
                if es:
                    rep.err('T02', where, '«%s» non è ammessa nell’area %s' % (tok, area))
                else:
                    rep.err('T02', where, '«%s» non è nel Glossario' % tok)
    return n

# ----------------------------------------------------------------------------------------------
# Unione


def merge(paths, out, rep, font):
    entries, areas, limits = load_glossary(paths, rep)
    check_glossary(entries, areas, rep, font, limits)
    if rep.errors:
        return 0
    first = load_json(paths[0])
    doc = {'file': 'GLOSSARIO_BLOCCATO.json', 'fonti': [os.path.basename(p) for p in paths],
           'aree': first.get('aree'), 'glossario': [{k: v for k, v in e.items() if k != '_file'} for e in entries]}
    d = os.path.dirname(os.path.abspath(out))
    os.makedirs(d, exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('voci unite: %d da %d file -> %s' % (len(entries), len(paths), out))
    return len(entries)

# ----------------------------------------------------------------------------------------------
# Collaudo


def find_docs(arg):
    for d in ([arg] if arg else DEFAULT_DOCS):
        if d and os.path.isfile(os.path.join(d, BLOCK_30)):
            return d
    return None


def selftest(docs):
    tdir = os.path.join(HERE, 'testdata')
    block = os.path.join(docs, BLOCK_30)
    expected = load_json(block)['strumento']['collaudo']
    font = Font()
    good = True

    r = Report(quiet=True)
    entries, areas, limits = load_glossary([block], r)
    check_glossary(entries, areas, r, font, limits)
    print('blocco 3.0: %d voci, %d errori' % (len(entries), len(r.errors)))
    for e in r.errors:
        print('  inatteso:', e)
    good &= not r.errors

    r = Report(quiet=True)
    e2, a2, _ = load_glossary([block, os.path.join(tdir, 'glossario_prova_ok.json')], r)
    check_glossary(e2, a2, r, font)
    print('blocco 3.0 + glossario_prova_ok: %d voci, %d errori' % (len(e2), len(r.errors)))
    for e in r.errors:
        print('  inatteso:', e)
    good &= not r.errors

    r = Report(quiet=True)
    e3, a3, _ = load_glossary([block, os.path.join(tdir, 'glossario_prova_ko.json')], r)
    check_glossary(e3, a3, r, font)
    got = r.codes()
    print('glossario_prova_ko: codici trovati %s' % ' '.join(got))
    if got != sorted(expected['errori_attesi_glossario_ko']):
        print('  attesi:', ' '.join(sorted(expected['errori_attesi_glossario_ko'])))
        good = False

    r = Report(quiet=True)
    check_texts([os.path.join(tdir, 'testi_prova_ok.json')], e2, a2, r, load_places(docs))
    print('testi_prova_ok: %d errori' % len(r.errors))
    for e in r.errors:
        print('  inatteso:', e)
    good &= not r.errors

    r = Report(quiet=True)
    check_texts([os.path.join(tdir, 'testi_prova_ko.json')], e2, a2, r, load_places(docs))
    got = r.codes()
    print('testi_prova_ko: codici trovati %s' % ' '.join(got))
    if got != sorted(expected['errori_attesi_testi_ko']):
        print('  attesi:', ' '.join(sorted(expected['errori_attesi_testi_ko'])))
        good = False

    print('SELFTEST_OK' if good else 'SELFTEST_FAILED')
    return 0 if good else 1


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description='Controllo del Glossario bloccato e dei nomi di Pokemon Trinacria')
    ap.add_argument('comando', nargs='?', choices=['glossary', 'names', 'text', 'merge'])
    ap.add_argument('file', nargs='*', help='file del Glossario (glossary, merge) o dei testi (text)')
    ap.add_argument('--glossary', nargs='+', default=[], help='file del Glossario per names e text')
    ap.add_argument('--repo', help='cartella di pokeheartgold (charmap e larghezze vere del font)')
    ap.add_argument('--docs', help='cartella docs di pokémon-sicilia (blocco 3.0 e nomi dei luoghi del Modulo 2)')
    ap.add_argument('--applied', action='store_true', help='names: ogni nome del Glossario deve essere già nel suo banco')
    ap.add_argument('-o', '--output', help='merge: file da scrivere')
    ap.add_argument('--selftest', action='store_true', help='collaudo sui file di prova in tools/testdata')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    docs = find_docs(a.docs)
    if a.selftest:
        if not docs:
            print('ERRORE G00 docs: %s non trovato (usare --docs)' % BLOCK_30)
            print('SELFTEST_FAILED')
            return 1
        return selftest(docs)
    rep = Report(quiet=a.quiet)
    font = Font(a.repo)
    if a.comando == 'glossary':
        entries, areas, limits = load_glossary(a.file, rep)
        n = check_glossary(entries, areas, rep, font, limits)
        print('voci: %d, errori: %d, avvisi: %d' % (n, len(rep.errors), len(rep.warnings)))
        tag = 'GLOSSARY'
    elif a.comando == 'names':
        if not a.repo:
            rep.err('N00', 'repo', 'serve --repo')
        else:
            entries = None
            if a.glossary:
                entries, areas, limits = load_glossary(a.glossary, rep)
            check_names(a.repo, rep, font, entries, a.applied)
        print('errori: %d' % len(rep.errors))
        tag = 'NAMES'
    elif a.comando == 'text':
        entries, areas, _ = load_glossary(a.glossary, rep)
        places = load_places(docs) if docs else set()
        n = check_texts(a.file, entries, areas, rep, places)
        print('testi: %d, errori: %d' % (n, len(rep.errors)))
        tag = 'TEXT'
    elif a.comando == 'merge':
        if not a.output:
            rep.err('G00', 'merge', 'serve -o <file>')
        else:
            merge(a.file, a.output, rep, font)
        tag = 'MERGE'
    else:
        ap.print_help()
        return 2
    print('%s_OK' % tag if not rep.errors else '%s_FAILED' % tag)
    return 0 if not rep.errors else 1


if __name__ == '__main__':
    sys.exit(main())

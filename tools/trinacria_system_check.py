#!/usr/bin/env python3
"""Pokemon Trinacria - controllo del blocco dei nomi di sistema (Modulo 3, blocco 3.13).

Uso (dalla cartella di F:\\Progetti\\pokémon-sicilia oppure da F:\\Progetti\\pokeheartgold):
    python -I tools/trinacria_system_check.py --selftest
    python -I tools/trinacria_system_check.py check docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json
           [--repo F:/Progetti/pokeheartgold] [--docs <docs>]

Ultima riga stampata: SISTEMA_OK / SELFTEST_OK (oppure *_FAILED).
Ogni problema e' una riga "ERRORE <codice> <dove>: <messaggio>".
Con --repo si controllano anche nomi inglesi e simboli (Y12) e si usa il font vero.
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
# Limiti del blocco 3.0 (L-06, L-07, L-09, L-10, L-11, D-04) e misure del blocco 3.13

ABILITY_LIMIT = (15, 72)        # L-09: caratteri, px; anche il maiuscolo di msg_0721 sta in 72 px
DESC_PROFILE = (2, 26, 136)     # D-04: righe, caratteri per riga, px per riga
TYPE_LIMIT = (10, 60)           # L-10
NATURE_LIMIT = (7, 42)          # L-11
CLASS_LIMIT = (15, 70)          # L-06
CLASS_ART_LIMIT = (20, 80)      # L-07
FORM_LIMIT = (16, 76)           # R-FOR-01: il più largo di HeartGold tra le forme di msg_0802 («Overcast Form»)
SEARCH_LIMIT = 43               # R-TIP-02: il più largo di HeartGold tra i tipi della ricerca («Electric»)
ABILITIES, TYPES, NATURES, CLASSES = 124, 18, 25, 129
NAME_CHARS = re.compile(r"^[A-Za-z0-9àèéìòùâêîôûÀÈÉÌÒÙÂÊÎÔÛçëïüñ ’.\-]+$")  # R-GRA-11
# i soprannomi no: R-NOM-02 ammette che un soprannome sia anche un nome di sistema (Siccità)
SYSTEM_CATEGORIES = ('specie', 'mossa', 'strumento', 'classe', 'abilita', 'tipo', 'natura', 'dossier')
CMD_RE = re.compile(r'\{[^{}]*\}')

# nomi italiani ufficiali (R-NOM-01; tabelle di PokeAPI, lingua it, lette il 27/10/2026)
ABILITA_IT = [
    None, 'Tanfo', 'Piovischio', 'Acceleratore', 'Lottascudo', 'Vigore', 'Umidità', 'Scioltezza', 'Sabbiavelo',
    'Statico', 'Assorbivolt', 'Assorbacqua', 'Indifferenza', 'Antimeteo', 'Insettocchi', 'Insonnia', 'Cambiacolore',
    'Immunità', 'Fuocardore', 'Polvoscudo', 'Mente Locale', 'Ventose', 'Prepotenza', 'Pedinombra', 'Cartavetro',
    'Magidifesa', 'Levitazione', 'Spargispora', 'Sincronismo', 'Corpochiaro', 'Alternacura', 'Parafulmine',
    'Leggiadro', 'Nuotovelox', 'Clorofilla', 'Risplendi', 'Traccia', 'Macroforza', 'Velenopunto', 'Forza Interiore',
    'Magmascudo', 'Idrovelo', 'Magnetismo', 'Antisuono', 'Copripioggia', 'Sabbiafiume', 'Pressione', 'Grassospesso',
    'Sveglialampo', 'Corpodifuoco', 'Fugafacile', 'Sguardofermo', 'Ipertaglio', 'Raccolta', 'Pigrone', 'Tuttafretta',
    'Incantevole', 'Più', 'Meno', 'Previsioni', 'Antifurto', 'Muta', 'Dentistretti', 'Pelledura', 'Melma', 'Erbaiuto',
    'Aiutofuoco', 'Acquaiuto', 'Aiutinsetto', 'Testadura', 'Siccità', 'Trappoarena', 'Spiritovivo', 'Fumochiaro',
    'Forzapura', 'Guscioscudo', 'Riparo', 'Intricopiedi', 'Elettrorapid', 'Antagonismo', 'Cuordeciso', 'Mantelneve',
    'Voracità', 'Grancollera', 'Agiltecnica', 'Antifuoco', 'Disinvoltura', 'Pellearsa', 'Download', 'Ferropugno',
    'Velencura', 'Adattabilità', 'Abillegame', 'Idratazione', 'Solarpotere', 'Piedisvelti', 'Normalità', 'Cecchino',
    'Magicscudo', 'Nullodifesa', 'Rallentatore', 'Tecnico', 'Fogliamanto', 'Impaccio', 'Rompiforma', 'Supersorte',
    'Scoppio', 'Presagio', 'Premonizione', 'Imprudenza', 'Lentifumé', 'Filtro', 'Lentoinizio', 'Nervisaldi',
    'Acquascolo', 'Corpogelo', 'Solidroccia', 'Scendineve', 'Mielincetta', 'Indagine', 'Temerarietà', 'Multitipo',
    'Regalfiore', 'Sogniamari']
TIPI_IT = ['Normale', 'Lotta', 'Volante', 'Veleno', 'Terra', 'Roccia', 'Coleottero', 'Spettro', 'Acciaio', '???',
           'Fuoco', 'Acqua', 'Erba', 'Elettro', 'Psico', 'Ghiaccio', 'Drago', 'Buio']
NATURE_IT = ['Ardita', 'Schiva', 'Audace', 'Decisa', 'Birbona', 'Sicura', 'Docile', 'Placida', 'Scaltra', 'Fiacca',
             'Timida', 'Lesta', 'Seria', 'Allegra', 'Ingenua', 'Modesta', 'Mite', 'Quieta', 'Ritrosa', 'Ardente',
             'Calma', 'Gentile', 'Vivace', 'Cauta', 'Furba']
# classi col nome italiano di un ruolo condiviso (R-CLA-03, deviazione D-24): possono ripetersi tra le classi
CLASSI_IT = {'Allenatore', 'Allenatrice', 'Rivale', 'Segretario', 'Presidente', 'Campione', 'Magistrata', 'Fantasma'}
FORM_INDICES = list(range(116, 122)) + list(range(145, 159)) + list(range(160, 167))
ROTOM = 479

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


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def find_docs(arg):
    for d in ([arg] if arg else []) + DEFAULT_DOCS:
        if d and os.path.isfile(os.path.join(d, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json')):
            return d
    return None


def load_names(docs, skip):
    """Glossario 3.0 + aggiunte dei blocchi 3.1-3.12, e i nomi italiani delle mosse e degli strumenti (Y08)."""
    gl, it = [], []
    if not docs:
        return gl, it
    gl += load_json(os.path.join(docs, 'MODULO_3', '3.0_REGOLE_E_GLOSSARIO.json'))['glossario']
    for f in sorted(glob.glob(os.path.join(docs, 'MODULO_3', '3.*_*.json'))):
        if os.path.basename(f).startswith(('3.0_', '3.13_')) or os.path.abspath(f) in skip:
            continue
        b = load_json(f)
        gl += b.get('glossario_aggiunte', [])
        for key, cat in (('mosse', 'mossa'), ('strumenti', 'strumento')):
            for e in b.get(key, []):
                if e.get('lingua') == 'it' and e.get('nome'):
                    it.append((e['nome'], '%s %s' % (cat, e['nome'])))
    return gl, it


def article(name, gender, number):
    """Articolo italiano davanti al nome della classe, senza colori (R-NOM-09; plurali: R-CLA-04)."""
    low = name.lower()
    vowel = low[:1] in 'aeiouàèéìòù'
    impure = (low[:1] == 's' and low[1:2] not in 'aeiouàèéìòù') or low[:1] in 'zxy' or low[:2] in ('gn', 'ps')
    if number == 'p':
        art = 'le ' if gender == 'f' else ('gli ' if vowel or impure else 'i ')
    elif gender == 'f':
        art = 'un’' if vowel else 'una '
    else:
        art = 'uno ' if impure else 'un '
    return art + name


def wrap(text, font):
    """Righe di D-04: parole intere, al massimo 26 caratteri e 136 px per riga."""
    lines, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w) if cur else w
        if len(t) <= DESC_PROFILE[1] and font.px(t) <= DESC_PROFILE[2]:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def bank_lines(lines):
    """D-04: righe separate da «\\n», nessun separatore finale."""
    return [x + '\n' for x in lines[:-1]] + [lines[-1]]

# ----------------------------------------------------------------------------------------------
# Repository (Y12)


class Repo:
    def __init__(self, path):
        def bank(n):
            out = []
            for m in load_json(os.path.join(path, 'files', 'msgdata', 'msg', 'msg_%s.json' % n))['messages']:
                t = m.get('en_US', '')
                out.append(''.join(t) if isinstance(t, list) else t)
            return out
        self.banks = {n: bank(n) for n in ('0720', '0721', '0722', '0730', '0731', '0735', '0034', '0802')}
        self.abilities = {}
        for line in open(os.path.join(path, 'include', 'constants', 'abilities.h'), encoding='utf-8'):
            m = re.match(r'#define (ABILITY_\w+)\s+(\d+)', line)
            if m:
                self.abilities[int(m.group(2))] = m.group(1)
        self.classes = {}
        for line in open(os.path.join(path, 'include', 'constants', 'trainer_class.h'), encoding='utf-8'):
            m = re.match(r'#define (TRAINERCLASS_\w+)\s+(\d+)\s*$', line)
            if m:
                self.classes.setdefault(int(m.group(2)), m.group(1))

# ----------------------------------------------------------------------------------------------


def check_name(rep, code, where, name, limit, font, upper=False):
    if not name or not NAME_CHARS.match(name):
        rep.err(code, where, 'nome vuoto o con caratteri non ammessi (R-GRA-11)')
        return
    cc, pp = limit
    if len(name) > cc or font.px(name) > pp:
        rep.err(code, where, '«%s» %d caratteri, %d px: oltre %d caratteri, %d px' % (name, len(name), font.px(name), cc, pp))
    if upper and font.px(name.upper()) > pp:
        rep.err(code, where, 'il maiuscolo «%s» misura %d px > %d' % (name.upper(), font.px(name.upper()), pp))


def check_block(b, glossary, it_names, rep, font, repo=None):
    for k in ('abilita', 'tipi', 'nature', 'classi', 'forme', 'ricerca_tipi', 'deviazioni_dalle_specifiche', 'glossario_aggiunte'):
        if not isinstance(b.get(k), list):
            rep.err('Y00', k, 'sezione mancante o non è un elenco')
            return
    devs = {d.get('id') for d in b['deviazioni_dalle_specifiche']}
    owners = collections.defaultdict(set)   # nome minuscolo -> {(categoria, chi)}
    for g in glossary:
        if g.get('categoria') in SYSTEM_CATEGORIES:
            owners[g['forma'].lower()].add((g['categoria'], g['id']))
    for nm, who in it_names:
        owners[nm.lower()].add(('it', who))
    mine = collections.defaultdict(set)

    # abilità
    ab = b['abilita']
    if [e.get('n') for e in ab] != list(range(ABILITIES)):
        rep.err('Y01', 'abilita', 'servono le voci 0-%d una volta, in ordine' % (ABILITIES - 1))
    for e in ab:
        n, where = e.get('n'), 'abilità %s' % e.get('n')
        if n == 0:
            if (e.get('banchi') or {}) != {'msg_0720': ' -', 'msg_0721': ' -', 'msg_0722': ' -'}:
                rep.err('Y01', where, 'lo slot 0 resta « -» nei tre banchi')
            continue
        nm = e.get('nome') or ''
        check_name(rep, 'Y01', where, nm, ABILITY_LIMIT, font, upper=True)
        if e.get('maiuscolo') != nm.upper():
            rep.err('Y01', where, 'maiuscolo diverso da «%s»' % nm.upper())
        if isinstance(n, int) and 0 < n < ABILITIES:
            if nm != ABILITA_IT[n] and e.get('deviazione') not in devs:
                rep.err('Y02', where, '«%s» non è il nome italiano ufficiale «%s» e non ha una deviazione' % (nm, ABILITA_IT[n]))
        lines = e.get('descrizione') or []
        if not lines or len(lines) > DESC_PROFILE[0] or any(
                not L or len(L) > DESC_PROFILE[1] or font.px(L) > DESC_PROFILE[2] for L in lines):
            rep.err('Y03', where, 'descrizione fuori da D-04 (%d righe, %d caratteri, %d px)' % DESC_PROFILE)
        bk = e.get('banchi') or {}
        if bk.get('msg_0720') != nm or bk.get('msg_0721') != nm.upper() or bk.get('msg_0722') != bank_lines(lines or ['']):
            rep.err('Y11', where, 'banchi diversi dai campi della voce')
        mine[nm.lower()].add(('abilita', where))
        if repo:
            if e.get('originale') != repo.banks['0720'][n] or e.get('simbolo') != repo.abilities.get(n):
                rep.err('Y12', where, 'nome inglese o simbolo diverso dal repository (%s, %s)' % (repo.banks['0720'][n], repo.abilities.get(n)))

    # tipi e nature
    for key, table, lim, cnt, bank in (('tipi', TIPI_IT, TYPE_LIMIT, TYPES, '0735'), ('nature', NATURE_IT, NATURE_LIMIT, NATURES, '0034')):
        lst = b[key]
        if [e.get('n') for e in lst] != list(range(cnt)):
            rep.err('Y04' if key == 'tipi' else 'Y05', key, 'servono le voci 0-%d una volta, in ordine' % (cnt - 1))
        for e in lst:
            n, nm, where = e.get('n'), e.get('nome') or '', '%s %s' % (key, e.get('n'))
            code = 'Y04' if key == 'tipi' else 'Y05'
            if isinstance(n, int) and 0 <= n < cnt and nm != table[n]:
                rep.err(code, where, '«%s» non è il nome italiano ufficiale «%s»' % (nm, table[n]))
            if nm != '???':
                check_name(rep, code, where, nm, lim, font)
                mine[nm.lower()].add((key, where))
            if (e.get('banchi') or {}) != {'msg_%s' % bank: nm}:
                rep.err('Y11', where, 'banchi diversi dai campi della voce')
            if repo and isinstance(n, int) and 0 <= n < cnt and e.get('originale') != repo.banks[bank][n]:
                rep.err('Y12', where, 'nome inglese diverso dal repository (%s)' % repo.banks[bank][n])

    # classi
    cl = b['classi']
    if [e.get('n') for e in cl] != list(range(CLASSES)):
        rep.err('Y06', 'classi', 'servono le voci 0-%d una volta, in ordine' % (CLASSES - 1))
    gl_class = {}
    for g in glossary + b['glossario_aggiunte']:
        if g.get('categoria') == 'classe':
            gl_class[(g.get('sostituisce') or {}).get('indice')] = g
    for e in cl:
        n, nm, where = e.get('n'), e.get('nome') or '', 'classe %s' % e.get('n')
        check_name(rep, 'Y06', where, nm, CLASS_LIMIT, font)
        art = article(nm, e.get('genere'), e.get('numero'))
        if e.get('con_articolo') != art:
            rep.err('Y06', where, 'forma con l’articolo «%s» invece di «%s» (R-NOM-09, R-CLA-04)' % (e.get('con_articolo'), art))
        if len(art) > CLASS_ART_LIMIT[0] or font.px(art) > CLASS_ART_LIMIT[1]:
            rep.err('Y06', where, '«%s» %d px oltre L-07 (%d px)' % (art, font.px(art), CLASS_ART_LIMIT[1]))
        g = gl_class.get(n)
        if e.get('lingua') == 'it' and not (g and g['forma'] == nm):
            if nm not in CLASSI_IT:
                rep.err('Y07', where, 'nome italiano «%s» fuori dai ruoli condivisi (R-CLA-03)' % nm)
            if g:
                rep.err('Y07', where, 'nome italiano ma il Glossario ha una voce per questa classe (%s)' % g['forma'])
        else:
            if not g or g['forma'] != nm or e.get('glossario') != g.get('id'):
                rep.err('Y07', where, 'nome assente dal Glossario o diverso (%s)' % (g.get('forma') if g else '—'))
            elif g.get('genere') and g['genere'] != e.get('genere'):
                rep.err('Y07', where, 'genere diverso dal Glossario')
            mine[nm.lower()].add(('classe', where))
        if (e.get('banchi') or {}) != {'msg_0730': nm, 'msg_0731': art}:
            rep.err('Y11', where, 'banchi diversi dai campi della voce')
        if repo and isinstance(n, int) and 0 <= n < CLASSES and (
                e.get('originale') != repo.banks['0730'][n] or e.get('simbolo_hg') != repo.classes.get(n)):
            rep.err('Y12', where, 'nome inglese o simbolo diverso dal repository (%s, %s)' % (repo.banks['0730'][n], repo.classes.get(n)))

    # Y08: un nome per oggetto tra abilità, tipi, nature e classi siciliane, e contro gli altri nomi di sistema
    for nm, who in mine.items():
        if len(who) > 1:
            rep.err('Y08', nm, 'stesso nome in più voci del blocco: %s' % ', '.join(sorted(w for _, w in who)))
        own = {e.get('glossario') for e in cl if (e.get('nome') or '').lower() == nm}
        others = sorted('%s %s' % x for x in owners.get(nm, set()) if x[1] not in own)
        if others:
            rep.err('Y08', nm, 'stesso nome di %s' % ', '.join(others))

    # forme (msg_0802)
    fo = b['forme']
    if [e.get('n') for e in fo] != FORM_INDICES:
        rep.err('Y09', 'forme', 'servono i messaggi 116-121, 145-158 e 160-166 di msg_0802, in ordine')
    rotom = next((g['forma'] for g in glossary if g.get('categoria') == 'specie'
                  and (g.get('sostituisce') or {}).get('indice') == ROTOM), None)
    for e in fo:
        n, nm, where = e.get('n'), e.get('nome') or '', 'forma %s' % e.get('n')
        check_name(rep, 'Y09', where, nm, FORM_LIMIT, font)
        if isinstance(n, int) and 153 <= n <= 158 and rotom and not nm.startswith(rotom):
            rep.err('Y09', where, 'le forme di Rotom cominciano col nome della specie «%s»' % rotom)
        if (e.get('banchi') or {}) != {'msg_0802': nm}:
            rep.err('Y11', where, 'banchi diversi dai campi della voce')
        if repo and isinstance(n, int) and e.get('originale') != repo.banks['0802'][n]:
            rep.err('Y12', where, 'testo inglese diverso dal repository (%s)' % repo.banks['0802'][n])

    # tipi nella ricerca del Pokédex (msg_0802 47-63)
    types = {e.get('n'): e.get('nome') for e in b['tipi']}
    rt = b['ricerca_tipi']
    if [e.get('n') for e in rt] != list(range(47, 64)):
        rep.err('Y10', 'ricerca_tipi', 'servono i messaggi 47-63 di msg_0802, in ordine')
    for e in rt:
        nm, full, where = e.get('nome') or '', types.get(e.get('tipo')) or '', 'ricerca %s' % e.get('n')
        ok = nm == full or (nm.endswith('.') and full.startswith(nm[:-1]) and font.px(full) > SEARCH_LIMIT)
        if not ok or font.px(nm) > SEARCH_LIMIT:
            rep.err('Y10', where, '«%s» (%d px): serve il nome del tipo «%s» entro %d px, abbreviato col punto solo se non entra (R-TIP-02)'
                    % (nm, font.px(nm), full, SEARCH_LIMIT))
        if (e.get('banchi') or {}) != {'msg_0802': nm}:
            rep.err('Y11', where, 'banchi diversi dai campi della voce')
        if repo and isinstance(e.get('n'), int) and e.get('originale') != repo.banks['0802'][e['n']]:
            rep.err('Y12', where, 'testo inglese diverso dal repository (%s)' % repo.banks['0802'][e['n']])

    # glossario_aggiunte: numerazione G313-NNNN
    for i, g in enumerate(b['glossario_aggiunte'], 1):
        if g.get('id') != 'G313-%04d' % i or g.get('categoria') != 'classe' or g.get('limite') != 'L-06':
            rep.err('Y00', g.get('id', '?'), 'voce del Glossario fuori numerazione G313-NNNN o non di categoria «classe»')
    return len(ab) + len(b['tipi']) + len(b['nature']) + len(cl) + len(fo) + len(rt)


def run_check(args, rep):
    font = Font(args.repo)
    docs = find_docs(args.docs)
    repo = Repo(args.repo) if args.repo else None
    total = 0
    for p in args.files:
        try:
            b = load_json(p)
        except Exception as ex:  # noqa: BLE001
            rep.err('Y00', p, 'file illeggibile: %s' % ex)
            continue
        glossary, it_names = load_names(docs, {os.path.abspath(p)})
        total += check_block(b, glossary, it_names, rep, font, repo)
    print('voci controllate: %d' % total)


def selftest():
    docs = find_docs(None)
    ok_files = sorted(glob.glob(os.path.join(HERE, '..', 'docs', 'MODULO_3', '3.13_*.json')))
    ko = os.path.join(HERE, 'testdata', 'sistema_prova_ko.json')
    repo = next((r for r in DEFAULT_REPOS if os.path.isfile(os.path.join(r, 'include', 'constants', 'abilities.h'))), None)
    print('repository per il collaudo: %s' % (repo or 'nessuno (Y12 non si controlla)'))
    good = True

    class A:
        pass
    a = A()
    a.files, a.repo, a.docs = ok_files, repo, docs
    rep = Report(quiet=True)
    run_check(a, rep)
    if not ok_files or rep.errors:
        good = False
        print('collaudo: il blocco 3.13 dà errori: %s' % rep.codes())
        for e in rep.errors[:10]:
            print('   ', *e)
    rep2 = Report(quiet=True)
    a.files = [ko]
    run_check(a, rep2)
    expected = [c for c in load_json(ko)['errori_attesi'] if repo or c != 'Y12']
    if rep2.codes() != sorted(expected):
        good = False
        print('collaudo: sistema_prova_ko.json dà %s invece di %s' % (rep2.codes(), sorted(expected)))
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
    args = ap.parse_args()
    rep = Report()
    run_check(args, rep)
    print('SISTEMA_OK' if not rep.errors else 'SISTEMA_FAILED')
    return 1 if rep.errors else 0


if __name__ == '__main__':
    sys.exit(main())

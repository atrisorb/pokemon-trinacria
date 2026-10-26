"""Generatore del blocco 3.10 (strumenti 1-180). Uso: python -I tools/generatori/3.10/gen310.py

Scrive docs/MODULO_3/3.10_STRUMENTI_1-180.json. Contenuti in content310.py, parti fisse del blocco in text310.py.
Il repository pokeheartgold deve stare accanto al progetto (F:/Progetti/pokeheartgold).
"""
import csv, glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
sys.stdout.reconfigure(errors='backslashreplace')  # console cp1252: la riga finale ha «→»
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
import trinacria_dex_check as dex  # noqa: E402
import trinacria_items_check as chk  # noqa: E402
from content310 import STRUMENTI, DEVIAZIONI, NEGOZI_SPECIALI  # noqa: E402
from text310 import TESTI  # noqa: E402

LO, HI = 1, 180
BLOCK = '3.10'
OUT = PROJ + '/docs/MODULO_3/3.10_STRUMENTI_1-180.json'
font = dex.Font(REPO)

repo = chk.Repo(REPO)
mart = chk.Marts(REPO)


def wrap(text):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w) if cur else w
        if len(t) <= chk.DESC_PROFILE[1] and font.px(t) <= chk.DESC_PROFILE[2]:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


G = json.load(open(PROJ + '/docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json', encoding='utf-8'))['glossario']
for f in sorted(glob.glob(PROJ + '/docs/MODULO_3/3.[1-9]_*.json')) + sorted(glob.glob(PROJ + '/docs/MODULO_3/3.1[0-9]_*.json')):
    if os.path.normpath(f) != os.path.normpath(OUT):
        G += json.load(open(f, encoding='utf-8')).get('glossario_aggiunte', [])
g30 = {g['sostituisce']['indice']: g for g in G if g['categoria'] == 'strumento' and g['id'].startswith('G30')}
specie_n = {g['forma']: g['sostituisce']['indice'] for g in G if g['categoria'] == 'specie'}
taken = {}
for g in G:
    if g['categoria'] in chk.SYSTEM_CATEGORIES:
        taken.setdefault(g['forma'].lower(), []).append('%s %s' % (g['categoria'], g['forma']))


def nota_specie(t):
    return re.sub(r'\{([^{}]+)\}', lambda m: str(specie_n[m.group(1)]), t) if t else t


errors = []
by_n = {s[0]: s for s in STRUMENTI}
strumenti, aggiunte = [], []
k = 0
for n in range(LO, HI + 1):
    entry = {'n': n, 'simbolo': repo.symbols[n], 'originale': repo.names[n]}
    if n in chk.EMPTY_SLOTS:
        entry.update({'vuoto': True, 'nome': None, 'lingua': None, 'glossario': None,
                      'banchi': 'invariati: «???» in msg_0222, msg_0223 e msg_0224, voce vuota in msg_0221 (R-STR-02)'})
        strumenti.append(entry)
        continue
    if n not in by_n:
        errors.append('strumento %d mancante in content310.py' % n)
        continue
    _, nome, gen, plur, lemma, sig, nota, desc, altro = by_n[n]
    nota = nota_specie(nota)
    if nome == 'G30':
        g = g30[n]
        nm, lingua, gid, gen, plur = g['forma'], 'scn', g['id'], g['genere'], g['plurale']
    elif isinstance(nome, tuple):
        nm, lingua, gid = nome[1], 'it', None
        if chk.TRAMA_IT.get(n) != nm:
            errors.append('nome della trama %d' % n)
    else:
        nm, lingua = nome, 'scn'
        if plur is None:
            plur = chk.plural(nm)
        k += 1
        gid = 'G310-%04d' % k
        others = [t for t in taken.get(nm.lower(), []) if not (n in chk.TRAMA_SOPRANNOMI and t.startswith('soprannome'))]
        if others:
            errors.append('collisione %s con %s' % (nm, others))
        forme = [nm.lower()] + ([plur.lower()] if plur.lower() != nm.lower() else [])
        ge = {'id': gid, 'forma': nm, 'categoria': 'strumento', 'lingua': 'scn', 'aree': ['SIC'], 'vietata_in': [],
              'forme': forme, 'varianti_vietate': [],
              'sostituisce': {'banco': 'msg_0222', 'indice': n, 'originale': repo.names[n]},
              'genere': gen, 'con_articolo': chk.with_article(nm, gen), 'plurale': plur,
              'significato': sig, 'origine': 'architetto 3.10', 'nota': nota,
              'caratteri': len(nm), 'px': font.px(nm), 'fonte': 'MCP' if lemma else 'architetto', 'lemma_mcp': lemma,
              'limite': 'L-03', 'con_articolo_px': font.px(chk.with_article(nm, gen)), 'plurale_px': font.px(plur)}
        aggiunte.append(ge)
    art = chk.with_article(nm, gen)
    lines = wrap(desc)
    msg = [L + '\n' for L in lines[:-1]] + [lines[-1]]
    entry.update({'nome': nm, 'lingua': lingua, 'glossario': gid, 'genere': gen, 'con_articolo': art, 'plurale': plur,
                  'caratteri': len(nm), 'px': font.px(nm), 'con_articolo_px': font.px(art), 'plurale_px': font.px(plur)})
    if lingua == 'it':
        entry['nome_della_trama'] = nota
    for d in DEVIAZIONI:
        if ('n. %d)' % n) in d['oggetto'] or ('n. %d ' % n) in d['oggetto']:
            entry['deviazione'] = d['id']
    entry.update({'dati': repo.data(n), 'descrizione': lines, 'descrizione_righe_px': [font.px(L) for L in lines],
                  'ottenimento': {'negozi': mart.where(n, NEGOZI_SPECIALI, repo), 'altro': altro},
                  'banchi': {'msg_0222': nm, 'msg_0223': art, 'msg_0224': plur, 'msg_0221': msg}})
    strumenti.append(entry)

# controllo con lo strumento del blocco (stesse regole dell'esecutore)
rep = chk.Report(quiet=True)
chk.check_items_list(strumenti, 'gen310', G + aggiunte, rep, font, repo)
errors += ['%s %s: %s' % e for e in rep.errors]
for e in strumenti:
    if e.get('vuoto'):
        continue
    if not e['ottenimento']['negozi'] and not e['ottenimento']['altro']:
        errors.append('strumento %d %s: nessun modo di ottenerlo' % (e['n'], e['nome']))
if errors:
    print('\n'.join(errors))
    sys.exit(1)

veri = [e for e in strumenti if not e.get('vuoto')]
mcp = sum(1 for a in aggiunte if a['fonte'] == 'MCP')
counts = dict(strumenti=len(veri), vuoti=len(strumenti) - len(veri), nuovi=len(aggiunte), mcp=mcp, arch=len(aggiunte) - mcp,
              g30=sum(1 for e in veri if e['glossario'] and e['glossario'].startswith('G30')),
              it=sum(1 for e in veri if e['lingua'] == 'it'),
              righe=sum(len(e['descrizione']) for e in veri),
              maxpx=max(px for e in veri for px in e['descrizione_righe_px']),
              maxnome=max(e['px'] for e in veri), maxart=max(e['con_articolo_px'] for e in veri),
              maxplur=max(e['plurale_px'] for e in veri),
              venduti=sum(1 for e in veri if e['ottenimento']['negozi']))
TESTI(counts, strumenti, aggiunte, DEVIAZIONI, NEGOZI_SPECIALI, mart, OUT)

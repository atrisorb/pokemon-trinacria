"""Generatore del blocco 3.11 (strumenti 181-360). Uso: python -I tools/generatori/3.11/gen311.py

Scrive docs/MODULO_3/3.11_STRUMENTI_181-360.json. Contenuti in content311.py, parti fisse del blocco in text311.py.
Il repository pokeheartgold deve stare accanto al progetto (F:/Progetti/pokeheartgold).
"""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
DOCS = PROJ + '/docs'
sys.stdout.reconfigure(errors='backslashreplace')  # console cp1252: la riga finale ha «→»
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
import trinacria_dex_check as dex  # noqa: E402
import trinacria_items_check as chk  # noqa: E402
from content311 import STRUMENTI, DEVIAZIONI, MT_ALTRO  # noqa: E402
from text311 import TESTI  # noqa: E402

LO, HI = 181, 360
BLOCK = '3.11'
OUT = PROJ + '/docs/MODULO_3/3.11_STRUMENTI_181-360.json'
font = dex.Font(REPO)

repo = chk.Repo(REPO)
mart = chk.Marts(REPO)
wild = chk.Wild(REPO, DOCS)
tms = chk.TMMoves(REPO, DOCS)
first = json.load(open(glob.glob(DOCS + '/MODULO_3/3.10_STRUMENTI_*.json')[0], encoding='utf-8'))
NEGOZI_SPECIALI = chk.plan_assignment(first['piano_negozi'])

G = json.load(open(DOCS + '/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json', encoding='utf-8'))['glossario']
for f in sorted(glob.glob(DOCS + '/MODULO_3/3.[1-9]_*.json')) + sorted(glob.glob(DOCS + '/MODULO_3/3.1[0-9]_*.json')):
    if os.path.normpath(f) != os.path.normpath(OUT):
        G += json.load(open(f, encoding='utf-8')).get('glossario_aggiunte', [])
g30 = {g['sostituisce']['indice']: g for g in G if g['categoria'] == 'strumento' and g['id'].startswith('G30')}
specie_n = {g['forma']: g['sostituisce']['indice'] for g in G if g['categoria'] == 'specie'}
taken = {}
for g in G:
    if g['categoria'] in chk.SYSTEM_CATEGORIES:
        taken.setdefault(g['forma'].lower(), []).append('%s %s' % (g['categoria'], g['forma']))

# nomi delle specie (per simbolo e per nome inglese in maiuscolo) e delle mosse (per nome inglese)
SPECIE = {}
for f in sorted(glob.glob(DOCS + '/MODULO_3/3.[1-5]_POKEMON_*.json')):
    b = json.load(open(f, encoding='utf-8'))
    key = next(k for k, v in b.items() if isinstance(v, list) and v and isinstance(v[0], dict) and 'originale' in v[0])
    for e in b[key]:
        SPECIE[e['originale']] = e['nome']
        if e.get('simbolo'):
            SPECIE[e['simbolo'][len('SPECIES_'):]] = e['nome']
MOSSE = {e['originale']: e['nome'] for e in tms.blocks.values()}

# mappe dei registri 2.1-2.3 (le mappe scritte in «altro» devono esistere, R-STR-07)
MAPPE = set()
for f in glob.glob(DOCS + '/MODULO_2/2.[1-3]_*.json'):
    MAPPE |= set(re.findall(r'\bMAP_[A-Z0-9_]+', open(f, encoding='utf-8').read()))


def nota_specie(t):
    return re.sub(r'\{([^{}]+)\}', lambda m: str(specie_n[m.group(1)]), t) if t else t


def segnaposti(t):
    t = re.sub(r'\[SP:([^\]]+)\]', lambda m: SPECIE[m.group(1)], t)
    return re.sub(r'\[MV:([^\]]+)\]', lambda m: MOSSE[m.group(1)], t)


errors = []
by_n = {s[0]: s for s in STRUMENTI}
strumenti, aggiunte = [], []
k = 0
for n in range(LO, HI + 1):
    entry = {'n': n, 'simbolo': repo.symbols[n], 'originale': repo.names[n]}
    if n in tms.move:  # MT: sigla della trama e descrizione della mossa insegnata (R-STR-11)
        mv = tms.blocks[tms.move[n]]
        nm, gen, plur, lingua, gid = chk.TRAMA_IT[n], 'f', chk.TRAMA_IT[n], 'it', None
        desc = ' '.join(mv['descrizione'])
        nota = ('Sigla italiana della trama («MT», R-STR-11): insegna la mossa %d %s (%s). La descrizione è quella '
                'della mossa nel blocco %s, riscritta nel profilo D-03.' % (
                    mv['n'], mv['nome'], tms.move[n], '3.6' if mv['n'] <= 120 else '3.7' if mv['n'] <= 240 else
                    '3.8' if mv['n'] <= 360 else '3.9'))
        altro = MT_ALTRO[n - chk.TM01 + 1]
        entry['mossa'] = {'n': mv['n'], 'simbolo': tms.move[n], 'nome': mv['nome']}
    elif n not in by_n:
        errors.append('strumento %d mancante in content311.py' % n)
        continue
    else:
        _, nome, gen, plur, lemma, sig, nota, desc, altro = by_n[n]
        nota = nota_specie(nota)
        desc = segnaposti(desc)
        if nome == 'G30':
            g = g30[n]
            nm, lingua, gid, gen, plur = g['forma'], 'scn', g['id'], g['genere'], g['plurale']
        else:
            nm, lingua = nome, 'scn'
            if plur is None:
                plur = chk.plural(nm)
            k += 1
            gid = 'G311-%04d' % k
            others = taken.get(nm.lower(), []) + (taken.get(plur.lower(), []) if plur.lower() != nm.lower() else [])
            if others:
                errors.append('collisione %s con %s' % (nm, others))
            forme = [nm.lower()] + ([plur.lower()] if plur.lower() != nm.lower() else [])
            ge = {'id': gid, 'forma': nm, 'categoria': 'strumento', 'lingua': 'scn', 'aree': ['SIC'], 'vietata_in': [],
                  'forme': forme, 'varianti_vietate': [],
                  'sostituisce': {'banco': 'msg_0222', 'indice': n, 'originale': repo.names[n]},
                  'genere': gen, 'con_articolo': chk.with_article(nm, gen), 'plurale': plur,
                  'significato': sig, 'origine': 'architetto 3.11', 'nota': nota,
                  'caratteri': len(nm), 'px': font.px(nm), 'fonte': 'MCP' if lemma else 'architetto', 'lemma_mcp': lemma,
                  'limite': 'L-03', 'con_articolo_px': font.px(chk.with_article(nm, gen)), 'plurale_px': font.px(plur)}
            aggiunte.append(ge)
    for m in re.findall(r'\bMAP_[A-Z0-9_]+', altro or ''):
        if m not in MAPPE:
            errors.append('strumento %d: la mappa %s non è nei registri 2.1-2.3' % (n, m))
    art = chk.with_article(nm, gen)
    lines = chk.wrap(desc, font)
    msg = chk.bank_0221(lines)
    entry.update({'nome': nm, 'lingua': lingua, 'glossario': gid, 'genere': gen, 'con_articolo': art, 'plurale': plur,
                  'caratteri': len(nm), 'px': font.px(nm), 'con_articolo_px': font.px(art), 'plurale_px': font.px(plur)})
    if lingua == 'it':
        entry['nome_della_trama'] = nota
    for d in DEVIAZIONI:
        if ('n. %d)' % n) in d['oggetto'] or ('n. %d ' % n) in d['oggetto']:
            entry['deviazione'] = d['id']
    selv = [dict(x, nome=SPECIE[x['specie'][len('SPECIES_'):]]) for x in wild.where(n, repo)]
    entry.update({'dati': repo.data(n), 'descrizione': lines, 'descrizione_righe_px': [font.px(L) for L in lines],
                  'ottenimento': {'negozi': mart.where(n, NEGOZI_SPECIALI, repo), 'selvatici': selv, 'altro': altro},
                  'banchi': {'msg_0222': nm, 'msg_0223': art, 'msg_0224': plur, 'msg_0221': msg}})
    strumenti.append(entry)

# controllo con lo strumento del blocco (stesse regole dell'esecutore)
rep = chk.Report(quiet=True)
chk.check_items_list(strumenti, 'gen311', G + aggiunte, rep, font, repo, None, mart, NEGOZI_SPECIALI, wild, tms)
errors += ['%s %s: %s' % e for e in rep.errors]
if errors:
    print('\n'.join(errors))
    sys.exit(1)

mcp = sum(1 for a in aggiunte if a['fonte'] == 'MCP')
counts = dict(strumenti=len(strumenti), nuovi=len(aggiunte), mcp=mcp, arch=len(aggiunte) - mcp,
              g30=sum(1 for e in strumenti if e['glossario'] and e['glossario'].startswith('G30')),
              mt=sum(1 for e in strumenti if 'mossa' in e),
              righe=sum(len(e['descrizione']) for e in strumenti),
              maxpx=max(px for e in strumenti for px in e['descrizione_righe_px']),
              maxnome=max(e['px'] for e in strumenti), maxart=max(e['con_articolo_px'] for e in strumenti),
              maxplur=max(e['plurale_px'] for e in strumenti),
              venduti=sum(1 for e in strumenti if e['ottenimento']['negozi']),
              selvatici=sum(1 for e in strumenti if e['ottenimento']['selvatici']),
              premi_mt=sum(1 for v in MT_ALTRO.values() if v and v.startswith('Premio')))
TESTI(counts, strumenti, aggiunte, DEVIAZIONI, OUT)

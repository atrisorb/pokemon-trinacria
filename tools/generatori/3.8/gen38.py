"""Generatore del blocco 3.8 (mosse 241-360). Uso: python -I tools/generatori/3.8/gen38.py

Scrive docs/MODULO_3/3.8_MOSSE_241-360.json. Contenuti in content38.py, parti fisse del blocco in text38.py.
Il repository pokeheartgold deve stare accanto al progetto (F:/Progetti/pokeheartgold).
"""
import glob, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
sys.stdout.reconfigure(errors='backslashreplace')  # console cp1252: la riga finale ha «→»
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
import trinacria_dex_check as dex  # noqa: E402
from content38 import MOSSE, DEVIAZIONI  # noqa: E402
from text38 import TESTI  # noqa: E402

LO, HI = 241, 360
BLOCK = '3.8'
OUT = PROJ + '/docs/MODULO_3/3.8_MOSSE_241-360.json'
NAME = (15, 72)
DESC = (5, 23, 120)
font = dex.Font(REPO)

TRAMA_IT = {18: 'Turbine', 29: 'Bottintesta', 56: 'Idropompa', 76: 'Solarraggio', 114: 'Nube', 123: 'Smog', 135: 'Covauova', 148: 'Flash',
            157: 'Frana', 164: 'Sostituto', 215: 'Rintoccasana', 220: 'Malcomune', 226: 'Staffetta', 241: 'Giornodisole',
            252: 'Bruciapelo', 312: 'Aromaterapia', 366: 'Ventoincoda'}


def narc_members(path):
    d = open(path, 'rb').read()
    off = struct.unpack_from('<H', d, 12)[0]
    sz, n = struct.unpack_from('<IH', d, off + 4)
    fat = [struct.unpack_from('<II', d, off + 12 + 8 * i) for i in range(n)]
    o2 = off + sz
    o3 = o2 + struct.unpack_from('<I', d, o2 + 4)[0]
    base = o3 + 8
    return [d[base + a:base + b] for a, b in fat]


TYPES = ['NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL', 'MYSTERY', 'FIRE', 'WATER',
         'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK']
CAT = ['fisica', 'speciale', 'stato']
waza = narc_members(REPO + '/files/poketool/waza/waza_tbl.narc')
moves_h = open(REPO + '/include/constants/moves.h', encoding='utf-8').read()
sym = {int(n): s for s, n in re.findall(r'#define\s+(MOVE_\w+)\s+(\d+)', moves_h) if not s.startswith('MOVE_ATTRIBUTE_')}
en = [m['en_US'] for m in json.load(open(REPO + '/files/msgdata/msg/msg_0750.json', encoding='utf-8'))['messages']]


def dati(n):
    eff, cat, pw, ty, acc, pp, ch, rng, pri, flg = struct.unpack_from('<HBBBBBBHbB', waza[n], 0)
    return {'tipo': 'TYPE_' + TYPES[ty], 'classe': CAT[cat], 'potenza': pw, 'precisione': acc, 'pp': pp,
            'effetto': eff, 'probabilita_effetto': ch, 'priorita': pri}


def wrap(text):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w) if cur else w
        if len(t) <= DESC[1] and font.px(t) <= DESC[2]:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


G = json.load(open(PROJ + '/docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json', encoding='utf-8'))['glossario']
for f in sorted(glob.glob(PROJ + '/docs/MODULO_3/3.[1-5]_POKEMON*.json')):
    G += json.load(open(f, encoding='utf-8'))['glossario_aggiunte']
# blocchi delle mosse gia' consegnati (dal 3.7): i loro nomi non si ripetono; il blocco che si sta generando no
for f in sorted(glob.glob(PROJ + '/docs/MODULO_3/3.[6-9]_MOSSE*.json')):
    if os.path.normpath(f) != os.path.normpath(OUT):
        G += json.load(open(f, encoding='utf-8'))['glossario_aggiunte']
g30 = {g['sostituisce']['indice']: g for g in G if g['categoria'] == 'mossa'}
taken = {}
# numeri delle specie per le note: «{Nome}» -> numero della specie che si chiama così
specie_n = {g['forma']: g['sostituisce']['indice'] for g in G if g['categoria'] == 'specie'}
dev_n = {d['mossa']: d['id'] for d in DEVIAZIONI}


def nota_specie(t):
    return re.sub(r'\{([^{}]+)\}', lambda m: str(specie_n[m.group(1)]), t) if t else t


for g in G:
    if g['categoria'] in ('specie', 'mossa', 'strumento', 'classe', 'abilita', 'tipo', 'natura', 'soprannome', 'dossier'):
        taken.setdefault(g['forma'].lower(), []).append('%s %s' % (g['categoria'], g['forma']))

errors = []
mosse, aggiunte = [], []
seen_names = {}
k = 0
for (n, nome, lemma, sig, nota, desc) in MOSSE:
    nota = nota_specie(nota)
    assert LO <= n <= HI
    d = dati(n)
    entry = {'n': n, 'simbolo': sym[n], 'originale': en[n]}
    if nome == 'G30':
        g = g30[n]
        nm, lingua, gid = g['forma'], 'scn', g['id']
    elif isinstance(nome, tuple):
        nm, lingua, gid = nome[1], 'it', None
        if TRAMA_IT.get(n) != nm:
            errors.append('nome della trama %d' % n)
    else:
        nm, lingua = nome, 'scn'
        k += 1
        gid = 'G38-%04d' % k
        if nm.lower() in taken:
            errors.append('collisione %s con %s' % (nm, taken[nm.lower()]))
        if n in TRAMA_IT:
            errors.append('mossa %d citata dalla trama con nome siciliano' % n)
        ge = {'id': gid, 'forma': nm, 'categoria': 'mossa', 'lingua': 'scn', 'aree': ['SIC'], 'vietata_in': [],
              'forme': [nm.lower()], 'varianti_vietate': [],
              'sostituisce': {'banco': 'msg_0750', 'indice': n, 'originale': en[n], 'copia_maiuscola': 'msg_0751'},
              'significato': sig, 'origine': 'architetto 3.8', 'nota': nota,
              'caratteri': len(nm), 'px': font.px(nm), 'fonte': 'MCP' if lemma else 'architetto', 'lemma_mcp': lemma,
              'limite': 'L-08', 'maiuscolo': nm.upper(), 'maiuscolo_px': font.px(nm.upper())}
        aggiunte.append(ge)
    if nm.lower() in seen_names:
        errors.append('nome ripetuto %s' % nm)
    seen_names[nm.lower()] = n
    if len(nm) > NAME[0] or font.px(nm) > NAME[1] or font.px(nm.upper()) > NAME[1]:
        errors.append('L-08 %s %d %d' % (nm, font.px(nm), font.px(nm.upper())))
    lines = wrap(desc)
    if len(lines) > DESC[0]:
        errors.append('D-02 %d righe: %s' % (len(lines), lines))
    for L in lines:
        if "'" in L or '"' in L or any(not font.known(c) for c in L):
            errors.append('carattere in %s' % L)
    msg = [L + '\n' for L in lines[:-1]] + [lines[-1] + ('\n' if len(lines) < DESC[0] else '')]
    entry.update({'nome': nm, 'lingua': lingua, 'glossario': gid})
    if lingua == 'it':
        entry['nome_della_trama'] = nota
    if n in dev_n:
        entry['deviazione'] = dev_n[n]
    entry.update({'caratteri': len(nm), 'px': font.px(nm), 'maiuscolo': nm.upper(), 'maiuscolo_px': font.px(nm.upper()),
                  'dati': d, 'descrizione': lines, 'descrizione_righe_px': [font.px(L) for L in lines], 'msg_0749': msg,
                  'banchi': {'msg_0750': nm, 'msg_0751': nm.upper(), 'msg_0749': msg}})
    mosse.append(entry)

assert [m['n'] for m in mosse] == list(range(LO, HI + 1)), 'mosse mancanti'
if errors:
    print('\n'.join(errors))
    sys.exit(1)

mcp = sum(1 for a in aggiunte if a['fonte'] == 'MCP')
n_g30 = sum(1 for m in mosse if m['glossario'] and m['glossario'].startswith('G30'))
n_it = sum(1 for m in mosse if m['lingua'] == 'it')
righe = sum(len(m['descrizione']) for m in mosse)
r5 = sum(1 for m in mosse if len(m['descrizione']) == 5)
maxpx = max(px for m in mosse for px in m['descrizione_righe_px'])
maxup = max(m['maiuscolo_px'] for m in mosse)
counts = dict(mosse=len(mosse), nuovi=len(aggiunte), mcp=mcp, arch=len(aggiunte) - mcp, g30=n_g30, it=n_it,
              righe=righe, r5=r5, r4=len(mosse) - r5, maxpx=maxpx, maxup=maxup, spec=specie_n)
TESTI(counts, mosse, aggiunte, DEVIAZIONI, OUT)

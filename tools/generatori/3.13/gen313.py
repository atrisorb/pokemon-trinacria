"""Generatore del blocco 3.13 (abilità, tipi, nature, classi allenatore, forme e lessico di sistema).
Uso: python -I tools/generatori/3.13/gen313.py

Scrive docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json. Contenuti in content313.py, parti fisse del blocco in text313.py.
Il repository pokeheartgold deve stare accanto al progetto (F:/Progetti/pokeheartgold), il dizionario siciliano in
F:/Progetti/sicilian-dialect-mcp.
"""
import glob, json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
VOCAB = os.path.normpath(os.path.join(PROJ, '..', 'sicilian-dialect-mcp', 'vocabolario.json'))
DOCS = PROJ + '/docs'
sys.stdout.reconfigure(errors='backslashreplace')  # console cp1252: la riga finale ha «→»
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
import trinacria_system_check as chk  # noqa: E402
from content313 import ABILITA, ABILITA_UFFICIALI_DIVERSE, TIPI, NATURE, CLASSI, FORME, RICERCA_TIPI, LESSICO  # noqa: E402
from text313 import TESTI, DEVIAZIONI  # noqa: E402

BLOCK = '3.13'
OUT = PROJ + '/docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json'
font = chk.Font(REPO)
repo = chk.Repo(REPO)
errors = []

G, IT = chk.load_names(DOCS, {os.path.abspath(OUT)})
g30 = {g['sostituisce']['indice']: g for g in G if g['categoria'] == 'classe' and g['id'].startswith('G30')}
rotom = next(g['forma'] for g in G if g['categoria'] == 'specie' and g['sostituisce']['indice'] == chk.ROTOM)
reg = {e['indice']: e for e in json.load(open(glob.glob(DOCS + '/MODULO_2/2.5_*.json')[0], encoding='utf-8'))
       ['classi_allenatore']['elenco']}


def plain(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


vocab = {t['lemma']: t for t in json.load(open(VOCAB, encoding='utf-8'))['termini']}


def dev_of(text):
    return next((d['id'] for d in DEVIAZIONI if text in d['oggetto']), None)


# abilità (msg_0720, msg_0721, msg_0722)
abilita = [{'n': 0, 'simbolo': repo.abilities[0], 'originale': repo.banks['0720'][0], 'nome': None,
            'nota': 'Nessuna abilità: resta « -» nei tre banchi.',
            'banchi': {'msg_0720': ' -', 'msg_0721': ' -', 'msg_0722': ' -'}}]
for n in range(1, chk.ABILITIES):
    nm, desc = ABILITA[n]
    lines = chk.wrap(desc, font)
    e = {'n': n, 'simbolo': repo.abilities[n], 'originale': repo.banks['0720'][n], 'nome': nm, 'maiuscolo': nm.upper(),
         'lingua': 'it', 'caratteri': len(nm), 'px': font.px(nm), 'maiuscolo_px': font.px(nm.upper())}
    if n in ABILITA_UFFICIALI_DIVERSE:
        e['nome_ufficiale'] = ABILITA_UFFICIALI_DIVERSE[n]
        e['deviazione'] = dev_of('abilità n. %d ' % n)
    e.update({'descrizione': lines, 'descrizione_righe_px': [font.px(L) for L in lines],
              'banchi': {'msg_0720': nm, 'msg_0721': nm.upper(), 'msg_0722': chk.bank_lines(lines)}})
    abilita.append(e)

tipi = [{'n': n, 'originale': repo.banks['0735'][n], 'nome': nm, 'lingua': 'it' if nm != '???' else None,
         'caratteri': len(nm), 'px': font.px(nm), 'banchi': {'msg_0735': nm}} for n, nm in enumerate(TIPI)]
nature = [{'n': n, 'originale': repo.banks['0034'][n], 'nome': nm, 'lingua': 'it', 'caratteri': len(nm),
           'px': font.px(nm), 'banchi': {'msg_0034': nm}} for n, nm in enumerate(NATURE)]

# classi (msg_0730, msg_0731) e voci nuove del Glossario
classi, aggiunte, k = [], [], 0
for n in range(chk.CLASSES):
    nm, gen, num, lingua, lemma, sig = CLASSI[n]
    r = reg[n]
    gid = None
    if nm == 'G30':
        g = g30[n]
        nm, gen, lingua, gid = g['forma'], g['genere'], g['lingua'], g['id']
    elif lingua == 'scn':
        k += 1
        gid = 'G313-%04d' % k
        if lemma:
            t = vocab.get(lemma)
            if not t:
                errors.append('classe %d: lemma «%s» assente dal dizionario' % (n, lemma))
            elif plain(nm) not in {plain(v) for v in [t['lemma']] + t['varianti']} and num != 'p':
                errors.append('classe %d: «%s» non è il lemma «%s» né una sua variante' % (n, nm, lemma))
        art = chk.article(nm, gen, num)
        ge = {'id': gid, 'forma': nm, 'categoria': 'classe', 'lingua': 'scn', 'aree': ['SIC'], 'vietata_in': [],
              'forme': [nm.lower()], 'varianti_vietate': [],
              'sostituisce': {'banco': 'msg_0730', 'indice': n, 'simbolo': r['simbolo'], 'originale': repo.banks['0730'][n]},
              'genere': gen, 'con_articolo': art, 'significato': sig, 'origine': 'architetto 3.13',
              'nota': ('Plurale: la classe è una coppia (R-CLA-04).' if num == 'p' else None),
              'caratteri': len(nm), 'px': font.px(nm), 'fonte': 'MCP' if lemma else 'architetto', 'lemma_mcp': lemma,
              'limite': 'L-06', 'con_articolo_px': font.px(art)}
        if num == 'p':
            ge['numero'] = 'p'
        aggiunte.append(ge)
    art = chk.article(nm, gen, num)
    e = {'n': n, 'simbolo_hg': r['simbolo_hg'], 'simbolo': r['simbolo'], 'categoria': r['categoria'],
         'originale': repo.banks['0730'][n], 'nome': nm, 'lingua': lingua, 'glossario': gid, 'genere': gen,
         'numero': num, 'con_articolo': art, 'caratteri': len(nm), 'px': font.px(nm), 'con_articolo_px': font.px(art),
         'ruolo': r['ruolo'], 'banchi': {'msg_0730': nm, 'msg_0731': art}}
    if lingua == 'it' and not gid:
        e['nota'] = sig
    classi.append(e)

# forme (msg_0802) e tipi nella ricerca del Pokédex
forme = []
for n in chk.FORM_INDICES:
    nm, nota = FORME[n]
    nm = nm.replace('{ROTOM}', rotom)
    e = {'n': n, 'originale': repo.banks['0802'][n], 'nome': nm, 'lingua': 'it', 'nota': nota,
         'caratteri': len(nm), 'px': font.px(nm), 'banchi': {'msg_0802': nm}}
    d = dev_of('msg_0802_%05d' % n)
    if d:
        e['deviazione'] = d
    forme.append(e)
ricerca = []
for n, t in RICERCA_TIPI.items():
    nm = TIPI[t]
    if font.px(nm) > chk.SEARCH_LIMIT:  # R-TIP-02: abbreviato col punto, la parte più lunga che entra
        nm = next(nm[:i] + '.' for i in range(len(nm) - 1, 0, -1) if font.px(nm[:i] + '.') <= chk.SEARCH_LIMIT)
    ricerca.append({'n': n, 'originale': repo.banks['0802'][n], 'tipo': t, 'nome': nm, 'px': font.px(nm),
                    'banchi': {'msg_0802': nm}})

# lessico di sistema: messaggi di HeartGold che sono esattamente l'etichetta inglese
banks = {}
for f in sorted(glob.glob(REPO + '/files/msgdata/msg/msg_*.json')):
    for m in json.load(open(f, encoding='utf-8'))['messages']:
        t = m.get('en_US')
        if t is not None:
            banks[m['id']] = ''.join(t) if isinstance(t, list) else t
lessico = []
for gruppo, parola, labels, nota in LESSICO:
    occ = sorted(i for i, t in banks.items() if t.strip() in labels)
    lessico.append({'gruppo': gruppo, 'parola': parola, 'etichette_heartgold': labels, 'messaggi_heartgold': occ,
                    'nota': nota})

# controllo con lo strumento del blocco (stesse regole dell'esecutore)
blocco_prova = {'abilita': abilita, 'tipi': tipi, 'nature': nature, 'classi': classi, 'forme': forme,
                'ricerca_tipi': ricerca, 'deviazioni_dalle_specifiche': DEVIAZIONI, 'glossario_aggiunte': aggiunte}
rep = chk.Report(quiet=True)
chk.check_block(blocco_prova, G, IT, rep, font, repo)
errors += ['%s %s: %s' % e for e in rep.errors]
if errors:
    print('\n'.join(errors))
    sys.exit(1)

mcp = sum(1 for a in aggiunte if a['fonte'] == 'MCP')
c = dict(nuovi=len(aggiunte), mcp=mcp, arch=len(aggiunte) - mcp,
         righe=sum(len(e.get('descrizione', [])) for e in abilita),
         maxpx=max(px for e in abilita for px in e.get('descrizione_righe_px', [])),
         maxab=max(e.get('px', 0) for e in abilita), maxabu=max(e.get('maiuscolo_px', 0) for e in abilita),
         maxtipo=max(e['px'] for e in tipi), maxnat=max(e['px'] for e in nature),
         maxcl=max(e['px'] for e in classi), maxart=max(e['con_articolo_px'] for e in classi),
         maxforma=max(e['px'] for e in forme), maxric=max(e['px'] for e in ricerca),
         g30=sum(1 for e in classi if (e['glossario'] or '').startswith('G30')),
         cl_it=sum(1 for e in classi if e['lingua'] == 'it' and not e['glossario']),
         cl_scn=sum(1 for e in classi if (e['glossario'] or '').startswith('G313')))
TESTI(c, abilita, tipi, nature, classi, forme, ricerca, lessico, aggiunte, OUT)

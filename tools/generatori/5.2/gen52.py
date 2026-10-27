"""Generatore del blocco 5.2 (partiture del Prologo e dell'Atto I).
Uso: python -I tools/generatori/5.2/gen52.py

Rifà il collaudo delle partiture tools/music/5.2/ (tools/music/collauda.py: componi, applica a una
copia dell'originale di HeartGold, controlla) e scrive docs/MODULO_5/5.2_ATTO_I.md coi numeri di ogni
brano, la SCHEDA delle partiture e il registro 2.5. Testi fissi in text52.py. Serve l'archivio originale
nel repository pokeheartgold accanto al progetto (F:/Progetti/pokeheartgold).
"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
DOCS = PROJ + '/docs'
OUT_MD = DOCS + '/MODULO_5/5.2_ATTO_I.md'
OUT_DIR = PROJ + '/build/collaudo/5.2'
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
sys.path.insert(0, PROJ + '/tools/music')
import trinacria_audio as A  # noqa: E402
import collauda as K  # noqa: E402
import notazione as N  # noqa: E402
import text52 as T  # noqa: E402

errors = []


def err(msg):
    errors.append(msg)
    print('ERRORE', msg)


os.makedirs(OUT_DIR, exist_ok=True)
new, righe, errs = K.collauda(['5.2'], OUT_DIR, REPO)
if errs:
    A.print_errs(errs)
    sys.exit('collaudo fallito: AUDIO_FAILED')
hg, _ = A.hg_original(REPO)
sd = A.Sdat(hg)
A.add_aliases(sd, REPO)
reg = json.load(open(glob.glob(DOCS + '/MODULO_2/2.5_*.json')[0], encoding='utf-8'))['musiche']
uso = {r['simbolo']: ('mappe', r['mappe']) for r in reg['campo']}
uso.update({r['simbolo']: ('uso', r['uso']) for r in reg['lotta']})
attesi = [r['simbolo'] for r in reg['campo'] + reg['lotta'] if r['blocco_modulo_5'] == '5.2']
fatti = [r['simbolo'] for r in righe]
if sorted(attesi) != sorted(fatti):
    err('partiture diverse dagli slot 5.2 del registro: mancano %s, in più %s' % (
        sorted(set(attesi) - set(fatti)), sorted(set(fatti) - set(attesi))))
campo = {r['simbolo'] for r in reg['campo']}
stesso = {r['simbolo']: r['scheda']['stesso_brano'] for r in righe if r['scheda'].get('stesso_brano')}
per_sim = {r['simbolo']: r for r in righe}
for s, base in stesso.items():
    if per_sim[s]['byte'] != per_sim[base]['byte'] or per_sim[s]['banco'] != per_sim[base]['banco']:
        err('%s non è identico a %s' % (s, base))
for r in righe:
    for k in ('titolo', 'carattere', 'tonalita', 'forma'):
        if not r['scheda'].get(k):
            err('%s: SCHEDA senza %s' % (r['simbolo'], k))

# --- uso dei tasti della batteria 39 nelle musiche di HeartGold
uso_tasti = collections.Counter()
for i, nm in enumerate(sd.names['SEQ']):
    if not nm or not A.is_music_slot(nm) or '_P_' in nm or not sd.seq_info(i):
        continue
    try:
        tracks = A.simulate(sd.seq_data(i))
    except A.AudioError:
        continue
    for tr in tracks:
        for n in tr.notes:
            if n[4] == 39:
                uso_tasti[n[1]] += 1


def num(n):
    return '{:,}'.format(n).replace(',', ' ')


def secondi(r):
    no = r['notazione']
    da, a = no['ritornello']
    q = (a - da) * no['battuta'] / 48
    s = q * 60 / no['bpm']
    return ('%.1f' % s).replace('.', ',')


def metro(r):
    m = r['notazione']['metro']
    return '%d/%d' % (m[0], m[1])


def estranee(r):
    return [(v['nome'], e) for v in r['notazione']['voci'] if v['estranee'] for e in v['estranee']]


def nome_nota(k):
    return N._nome(k)


scritti = [r for r in righe if r['simbolo'] not in stesso]
poly_max = max(r['polifonia']['totale'] for r in righe)
psg_max = max(r['polifonia'].get('psg', 0) for r in righe)
byte_max = max(r['byte'] for r in righe)
byte_max_field = max(r['byte'] for r in righe if r['lettore'] == 'PLAYER_FIELD')
n_estranee = sum(len(estranee(r)) for r in scritti)
V = dict(versione=T.VERSIONE, data=T.DATA, sha1=A.HG_SHA1, n_file=len(righe), n_distinti=len(scritti),
         n_stesso=len(stesso), n_campo=sum(1 for r in righe if r['simbolo'] in campo),
         n_lotta=sum(1 for r in righe if r['simbolo'] not in campo), poly_max=poly_max, psg_max=psg_max,
         byte_max=num(byte_max), byte_max_field=num(byte_max_field), sdat_byte=num(len(new)),
         n_estranee=n_estranee, qualita=', '.join('`%s`' % (q or '«»') for q in N.QUALITA))

out = [T.INTESTAZIONE.format(**V), '', T.IN_BREVE.format(**V), '', T.NOTAZIONE.format(**V), '',
       T.COLLAUDO.format(**V), '']

# 2.1 numeri
out.append('| # | Alias | Slot HeartGold | Lettore | Banco | Vol. | Tempo | Metro | Rit. | Tracce | Note | Byte | Insieme | Carico |')
out.append('|---:|---|---|---|---|---:|---:|:-:|---|---:|---:|---|---:|---:|')
for n, r in enumerate(righe, 1):
    no = r['notazione']
    da, a = no['ritornello']
    out.append('| %d | `%s` | `%s` | %s | `%s` | %d | %d | %s | %d + %d (%s s) | %d | %d | %s (%s) | %d | %s |' % (
        n, r['simbolo'], r['slot'], r['lettore'].replace('PLAYER_', ''), r['banco'], r['volume'], no['bpm'],
        metro(r), da, a - da, secondi(r), r['tracce'], r['note'], num(r['byte']), num(r['byte_hg']),
        r['polifonia']['totale'], num(r['carico'])))
out.append('')
out.append('Totale: %s byte di sequenze (HeartGold negli stessi slot: %s); nessun brano supera %d note insieme; '
           'una sola voce PSG (`SEQ_CT_CUBBAR_TECHNO`), nessun rumore.' % (
               num(sum(r['byte'] for r in righe)), num(sum(r['byte_hg'] for r in righe)), poly_max))
out.append('')

# 2.2 deviazioni
dev = []
for r in righe:
    inf = sd.seq_info(sd.seq_index(r['slot']))
    b0, v0 = sd.name('BANK', inf['banco']), inf['volume']
    if r['banco'] != b0 or r['volume'] != v0:
        dev.append((r, b0, v0))
out.append(T.DEVIAZIONI_INTRO.format(n_uguali=len(righe) - len(dev)))
out.append('')
out.append('| Alias | Slot | Banco HeartGold → Trinacria | Volume HeartGold → Trinacria | Perché |')
out.append('|---|---|---|---|---|')
for r, b0, v0 in dev:
    if r['simbolo'] in stesso:
        why = 'stesso brano di `%s` (R-AUD-17): stesso banco e volume, così suona identico' % stesso[r['simbolo']]
    else:
        why = r['scheda'].get('perche_volume', '')
        if not why:
            err('%s: banco o volume diverso da HeartGold senza ragione (SCHEDA perche_volume)' % r['simbolo'])
    out.append('| `%s` | `%s` | %s | %s | %s |' % (
        r['simbolo'], r['slot'], '`%s` → `%s`' % (b0, r['banco']) if b0 != r['banco'] else 'invariato',
        '%d → %d' % (v0, r['volume']) if v0 != r['volume'] else 'invariato', why))
out.append('')

# 3 timbri
usati = collections.defaultdict(list)
for r in scritti:
    for v in r['notazione']['voci']:
        for p in v['programmi']:
            if r['simbolo'] not in usati[p]:
                usati[p].append(r['simbolo'])
out.append(T.TIMBRI_INTRO)
out.append('')
out.append('| Prg | Ruolo nelle partiture | Perché (dati del banco, uso in HeartGold) | Brani | Esempio |')
out.append('|---:|---|---|---:|---|')
for p in sorted(usati):
    if p not in T.TIMBRI:
        err('programma %d senza ruolo in text52.TIMBRI' % p)
        continue
    ruolo, perche = T.TIMBRI[p]
    out.append('| %d | %s | %s | %d | `%s` |' % (p, ruolo, perche, len(usati[p]), usati[p][0]))
for p in T.TIMBRI:
    if p not in usati:
        err('programma %d in text52.TIMBRI ma in nessuna partitura' % p)
out.append('')
out.append(T.BATTERIA_INTRO)
out.append('')
tasti_usati = collections.Counter()
for r in scritti:
    sseq, _ = A.midi_to_sseq(A.read(os.path.join(OUT_DIR, r['simbolo'] + '.mid')))
    for tr in A.simulate(sseq):
        for n in tr.notes:
            if n[4] == 39:
                tasti_usati[n[1]] += 1
out.append('| Nome | Tasto | Nota | Colpi nel 5.2 | Usi in HeartGold |')
out.append('|---|---:|---|---:|---:|')
for nome, k in sorted(N.BATTERIA.items(), key=lambda x: x[1]):
    out.append('| `%s` | %d | %s | %s | %s |' % (nome, k, A.note_name(k), num(tasti_usati[k]), num(uso_tasti[k])))
out.append('')

# 4 brani
out.append('## 4. I brani')
out.append('')
out.append('Per ogni slot: dati dello slot, mappe o uso dal registro 2.5, la `SCHEDA` della partitura e le voci '
           '(nome della voce e programma; «eco» e «ottava» sono copie di un\'altra voce, R-AUD-15). «Estranee» '
           '= note su un movimento fuori dall\'accordo (R-AUD-19), come `battuta.movimento:nota/accordo`, con le '
           'battute contate da 0 come nel parametro `da=` della partitura.')
out.append('')
for n, r in enumerate(righe, 1):
    sch = r['scheda']
    no = r['notazione']
    out.append('### 4.%d `%s` — %s' % (n, r['simbolo'], sch['titolo']))
    out.append('')
    tw = (' e gemello `%s`' % r['gemello']) if r['gemello'] else ' (nessun gemello GB)'
    out.append('- **Slot:** `%s`%s · %s · `%s` · volume %d · partitura `%s`' % (
        r['slot'], tw, r['lettore'], r['banco'], r['volume'], r['partitura']))
    kind, val = uso[r['simbolo']]
    if kind == 'mappe':
        m = ', '.join('`%s`' % x for x in val[:6]) + (' … (%d mappe)' % len(val) if len(val) > 6 else '')
        out.append('- **Mappe:** %s' % m)
    else:
        out.append('- **Uso:** %s' % val)
    if r['simbolo'] in stesso:
        out.append('- **Stesso brano di `%s`** (R-AUD-17): la partitura carica quella e ne prende banco e volume.'
                   % stesso[r['simbolo']])
        out.append('')
        continue
    out.append('- **Carattere:** %s.' % sch['carattere'])
    da, a = no['ritornello']
    out.append('- **Tonalità, metro, tempo:** %s · %s · %d semiminime al minuto' % (sch['tonalita'], metro(r), no['bpm']))
    out.append('- **Forma:** %s; ritornello dalla battuta %d alla %d (%d battute, %s secondi).' % (
        sch['forma'], da, a, a - da, secondi(r)))
    voci = []
    for v in no['voci']:
        tag = ''
        if v['copia_di']:
            tag = ', copia di «%s»' % v['copia_di']
        elif v['pedale']:
            tag = ', pedale'
        voci.append('%s (%d%s)' % (v['nome'], v['programma'], tag))
    out.append('- **Voci:** %s.' % ' · '.join(voci))
    est = estranee(r)
    out.append('- **Estranee:** %s' % ('nessuna' if not est else '%d — %s' % (len(est), ', '.join(
        '%s %d.%d:%s/%s' % (nm, e[0], e[1], e[2], e[3]) for nm, e in est))))
    out.append('')

# 5 regole
out.append('## 5. Regole')
out.append('')
out.append('Le regole R-AUD-01…14 del blocco 5.1 restano valide; il blocco 5.2 aggiunge:')
out.append('')
out.append('| Codice | Regola | Testo |')
out.append('|---|---|---|')
for code, title, text in T.REGOLE:
    out.append('| %s | %s | %s |' % (code, title, text))
out.append('')
out.append(T.NOTE_BLOCCHI)
out.append('')
riga = ('BLOCCO COMPLETO: 5.2 — %d partiture in tools/music/5.2/ (%d brani scritti + %d slot «_EST» con lo stesso '
        'brano; %d di campo, %d di lotta, incontro e vittoria, coi 3 temi di «U Sistema»), notazione comune '
        'tools/music/notazione.py e collaudo tools/music/collauda.py; al massimo %d note insieme, %d voce PSG, '
        'sequenza più lunga %s byte; %d note estranee rilette; %d banchi o volumi diversi dallo slot HeartGold; '
        '%d regole R-AUD-15…21 → AUDIO_OK') % (
    len(righe), len(scritti), len(stesso), V['n_campo'], V['n_lotta'], poly_max, psg_max, num(byte_max),
    n_estranee, len(dev), len(T.REGOLE))
out.append('## 7. Riga di controllo')
out.append('')
out.append('`%s`' % riga)
out.append('')

if errors:
    sys.exit('%d errori: documento non scritto' % len(errors))
with open(OUT_MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(out))
print('scritto %s (%d byte)' % (OUT_MD, os.path.getsize(OUT_MD)))
print(riga)

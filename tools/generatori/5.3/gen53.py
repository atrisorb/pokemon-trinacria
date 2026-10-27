"""Generatore del blocco 5.3 (partiture degli Atti II-IV).
Uso: python -I tools/generatori/5.3/gen53.py

Rifà il collaudo delle partiture tools/music/5.3/ (tools/music/collauda.py: componi, applica a una
copia dell'originale di HeartGold, controlla) e scrive docs/MODULO_5/5.3_ATTI_II-IV.md coi numeri di
ogni brano, la SCHEDA delle partiture e il registro 2.5. Testi fissi in text53.py. Serve l'archivio
originale nel repository pokeheartgold accanto al progetto (F:/Progetti/pokeheartgold).
Copiato da tools/generatori/5.2/gen52.py; in più gestisce il brano che non si ripete (A10).
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
OUT_MD = DOCS + '/MODULO_5/5.3_ATTI_II-IV.md'
OUT_DIR = PROJ + '/build/collaudo/5.3'
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
sys.path.insert(0, PROJ + '/tools/music')
import trinacria_audio as A  # noqa: E402
import collauda as K  # noqa: E402
import notazione as N  # noqa: E402
import text53 as T  # noqa: E402

BLOCCO = '5.3'
errors = []


def err(msg):
    errors.append(msg)
    print('ERRORE', msg)


os.makedirs(OUT_DIR, exist_ok=True)
new, righe, errs = K.collauda([BLOCCO], OUT_DIR, REPO)
if errs:
    A.print_errs(errs)
    sys.exit('collaudo fallito: AUDIO_FAILED')
hg, _ = A.hg_original(REPO)
sd = A.Sdat(hg)
A.add_aliases(sd, REPO)
reg = json.load(open(glob.glob(DOCS + '/MODULO_2/2.5_*.json')[0], encoding='utf-8'))['musiche']
uso = {r['simbolo']: ('mappe', r['mappe']) for r in reg['campo']}
uso.update({r['simbolo']: ('uso', r['uso']) for r in reg['lotta']})
attesi = [r['simbolo'] for r in reg['campo'] + reg['lotta'] if r['blocco_modulo_5'] == BLOCCO]
fatti = [r['simbolo'] for r in righe]
if sorted(attesi) != sorted(fatti):
    err('partiture diverse dagli slot %s del registro: mancano %s, in più %s' % (
        BLOCCO, sorted(set(attesi) - set(fatti)), sorted(set(fatti) - set(attesi))))
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
    if (r['notazione']['ritornello'] is None) != (r['ritornello'] is None):
        err('%s: ritornello della notazione diverso da quello della sequenza' % r['simbolo'])
    if r['notazione']['ritornello'] is None and not r['notazione']['durata']:
        err('%s: brano senza ritornello e senza fine_a()' % r['simbolo'])

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


def battute(r):
    """(prima battuta, battute) del ritornello, o (0, durata) del brano che finisce."""
    no = r['notazione']
    if no['ritornello']:
        da, a = no['ritornello']
        return da, a - da
    return 0, no['durata']


def secondi(r):
    no = r['notazione']
    q = battute(r)[1] * no['battuta'] / 48
    s = q * 60 / no['bpm']
    return ('%.1f' % s).replace('.', ',')


def metro(r):
    m = r['notazione']['metro']
    return '%d/%d' % (m[0], m[1])


def estranee(r):
    return [(v['nome'], e) for v in r['notazione']['voci'] if v['estranee'] for e in v['estranee']]


def voci_di(tipo):
    """Brani con voci PSG o di rumore (programmi della tavolozza comune, §9.2 del 5.1)."""
    prg = {'psg': {43, 48, 49, 50, 51, 52, 58, 59}, 'rumore': {53, 54}}[tipo]
    return [r['simbolo'] for r in righe if any(p in prg for v in r['notazione']['voci'] for p in v['programmi'])]


scritti = [r for r in righe if r['simbolo'] not in stesso]
finiti = [r for r in righe if not r['notazione']['ritornello']]
poly_max = max(r['polifonia']['totale'] for r in righe)
psg_max = max(r['polifonia'].get('psg', 0) for r in righe)
rumore_max = max(r['polifonia'].get('rumore', 0) for r in righe)
byte_max = max(r['byte'] for r in righe)
byte_max_field = max(r['byte'] for r in righe if r['lettore'] == 'PLAYER_FIELD')
n_estranee = sum(len(estranee(r)) for r in scritti)
V = dict(versione=T.VERSIONE, data=T.DATA, sha1=A.HG_SHA1, n_file=len(righe), n_distinti=len(scritti),
         n_campo=sum(1 for r in righe if r['simbolo'] in campo),
         n_lotta=sum(1 for r in righe if r['simbolo'] not in campo), poly_max=poly_max, psg_max=psg_max,
         rumore_max=rumore_max, byte_max=num(byte_max), byte_max_field=num(byte_max_field),
         sdat_byte=num(len(new)), n_estranee=n_estranee or 'nessuna',
         finito=finiti[0]['simbolo'] if finiti else '—', finito_s=secondi(finiti[0]) if finiti else '—',
         psg=', '.join('`%s`' % s for s in voci_di('psg')), rumore=', '.join('`%s`' % s for s in voci_di('rumore')))
if len(finiti) != 1:
    err('attesi 1 brano senza ritornello (SEQ_TRN_TRAGHETTO), trovati %d' % len(finiti))

out = [T.INTESTAZIONE.format(**V), '', T.IN_BREVE.format(**V), '', T.NOTAZIONE.format(**V), '',
       T.COLLAUDO.format(**V), '']

# 2.1 numeri
out.append('| # | Alias | Slot HeartGold | Lettore | Banco | Vol. | Tempo | Metro | Rit. | Tracce | Note | Byte | Insieme | Carico |')
out.append('|---:|---|---|---|---|---:|---:|:-:|---|---:|---:|---|---:|---:|')
for n, r in enumerate(righe, 1):
    no = r['notazione']
    if no['ritornello']:
        da, lung = battute(r)
        rit = '%d + %d (%s s)' % (da, lung, secondi(r))
    else:
        rit = 'finisce a %d (%s s)' % (no['durata'], secondi(r))
    out.append('| %d | `%s` | `%s` | %s | `%s` | %d | %d | %s | %s | %d | %d | %s (%s) | %d | %s |' % (
        n, r['simbolo'], r['slot'], r['lettore'].replace('PLAYER_', ''), r['banco'], r['volume'], no['bpm'],
        metro(r), rit, r['tracce'], r['note'], num(r['byte']), num(r['byte_hg']),
        r['polifonia']['totale'], num(r['carico'])))
out.append('')
out.append('Totale: %s byte di sequenze (HeartGold negli stessi slot: %s); nessun brano supera %d note insieme; '
           'voci PSG solo in %s (al massimo %d insieme), rumore solo in %s (%d).' % (
               num(sum(r['byte'] for r in righe)), num(sum(r['byte_hg'] for r in righe)), poly_max,
               V['psg'], psg_max, V['rumore'], rumore_max))
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
    if r['banco'] == b0 and not (v0 < 60 and r['volume'] == 64):
        err('%s: volume %d → %d fuori da R-AUD-24' % (r['simbolo'], v0, r['volume']))
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
        err('programma %d senza ruolo in text53.TIMBRI' % p)
        continue
    ruolo, perche = T.TIMBRI[p]
    out.append('| %d | %s | %s | %d | `%s` |' % (p, ruolo, perche, len(usati[p]), usati[p][0]))
for p in T.TIMBRI:
    if p not in usati:
        err('programma %d in text53.TIMBRI ma in nessuna partitura' % p)
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
out.append('| Nome | Tasto | Nota | Colpi nel %s | Usi in HeartGold |' % BLOCCO)
out.append('|---|---:|---|---:|---:|')
for nome, k in sorted(N.BATTERIA.items(), key=lambda x: x[1]):
    out.append('| `%s` | %d | %s | %s | %s |' % (nome, k, A.note_name(k), num(tasti_usati[k]), num(uso_tasti[k])))
out.append('')

# 4 brani
out.append('## 4. I brani')
out.append('')
out.append('Per ogni slot: dati dello slot, mappe dal registro 2.5, la `SCHEDA` della partitura e le voci '
           '(nome della voce e programma; «eco», «ottava» e i raddoppi sono copie di un\'altra voce, R-AUD-15). '
           '«Estranee» = note su un movimento fuori dall\'accordo (R-AUD-19), come `battuta.movimento:nota/accordo`, '
           'con le battute contate da 0 come nel parametro `da=` della partitura.')
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
    out.append('- **Carattere:** %s.' % sch['carattere'])
    out.append('- **Tonalità, metro, tempo:** %s · %s · %d semiminime al minuto' % (sch['tonalita'], metro(r), no['bpm']))
    if no['ritornello']:
        da, a = no['ritornello']
        out.append('- **Forma:** %s; ritornello dalla battuta %d alla %d (%d battute, %s secondi).' % (
            sch['forma'], da, a, a - da, secondi(r)))
    else:
        out.append('- **Forma:** %s; il brano dura %d battute (%s secondi) e finisce, come lo slot HeartGold (A10).' % (
            sch['forma'], no['durata'], secondi(r)))
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
out.append('Le regole R-AUD-01…14 del blocco 5.1 e R-AUD-15…21 del blocco 5.2 restano valide; il blocco 5.3 aggiunge:')
out.append('')
out.append('| Codice | Regola | Testo |')
out.append('|---|---|---|')
for code, title, text in T.REGOLE:
    out.append('| %s | %s | %s |' % (code, title, text))
out.append('')
out.append(T.NOTE_BLOCCHI.format(**V))
out.append('')
riga = ('BLOCCO COMPLETO: 5.3 — %d partiture in tools/music/5.3/ (tutte musiche di campo delle province di '
        'Siracusa, Ragusa, Caltanissetta, Agrigento, Trapani e Messina, più il viaggio in traghetto, che '
        'finisce come lo slot HeartGold); al massimo %d note insieme, %d voci PSG, %d di rumore (il vento del '
        'Cretto), sequenza più lunga %s byte; %d note estranee; %d volumi diversi dallo slot HeartGold; '
        '%d regole R-AUD-22…24 → AUDIO_OK') % (
    len(righe), poly_max, psg_max, rumore_max, num(byte_max), n_estranee, len(dev), len(T.REGOLE))
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

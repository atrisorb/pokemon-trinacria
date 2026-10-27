"""Generatore del blocco 5.1 (pipeline MIDI→SSEQ, banchi SBNK e suoni da mantenere).
Uso: python -I tools/generatori/5.1/gen51.py

Scrive docs/MODULO_5/5.1_PIPELINE_E_SFX.md e docs/MODULO_5/5.1_BANCHI_SBNK.json leggendo
l'archivio audio e i sorgenti di pokeheartgold (accanto al progetto, F:/Progetti/pokeheartgold)
e il registro 2.5. Testi fissi in text51.py; le tabelle si calcolano con tools/trinacria_audio.py.
"""
import collections
import glob
import hashlib
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
DOCS = PROJ + '/docs'
OUT_MD = DOCS + '/MODULO_5/5.1_PIPELINE_E_SFX.md'
OUT_JSON = DOCS + '/MODULO_5/5.1_BANCHI_SBNK.json'
sys.stdout.reconfigure(errors='backslashreplace')
sys.path.insert(0, HERE)
sys.path.insert(0, PROJ + '/tools')
import trinacria_audio as A  # noqa: E402
import text51 as T  # noqa: E402

# Risultati del collaudo (python -I tools/trinacria_audio.py --selftest, 27/10/2026): il generatore
# non lo rifà (dura circa 3 minuti), ricalcola solo i dati delle tabelle.
COLLAUDO = {'n_rt': 1371, 'rapporto': 87, 'rapporto_max': 103, 'campo_max': 12304, 'n_codici': 13,
            'prova': '612 byte, 4 tracce, 229 note, ritornello di 8 battute nello slot `SEQ_GS_T_WAKABA`; '
                      'archivio di 8 652 832 byte, `controlla` superato, `AUDIO_OK`.'}

errors = []


def err(msg):
    errors.append(msg)
    print('ERRORE', msg)


raw = A.read(A.sdat_path(REPO))
sha1 = hashlib.sha1(raw).hexdigest()
if sha1 != A.HG_SHA1:
    sys.exit('archivio del repository diverso dall\'originale di HeartGold')
sd = A.Sdat(raw)
aliases = A.add_aliases(sd, REPO)
vals = A.sndseq_values(REPO)
pairs = A.gb_twins(REPO)
reg = json.load(open(glob.glob(DOCS + '/MODULO_2/2.5_*.json')[0], encoding='utf-8'))['musiche']
lim = A.player_limits(sd)
ch = lim['PLAYER_FIELD']['canali']
if ch != lim['PLAYER_BGM']['canali']:
    err('i due lettori delle musiche hanno canali diversi')
basic = A.parse_sbnk(sd.bank_data(sd.bank_index('BANK_BASIC')))
banks = [n for n in sd.names['BANK'] if n and A.MUSIC_BANK.match(n)]
insts = {b: A.parse_sbnk(sd.bank_data(sd.bank_index(b))) for b in banks}


def same(a, b):
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


for b in banks:
    for p in range(60):
        if b != 'BANK_BGM_ARCEUS' and not same(insts[b][p], basic[p]):
            err('%s: programma %d diverso da BANK_BASIC' % (b, p))

# --- uso dei programmi nelle musiche di HeartGold
uso = {}
uso_comune = collections.defaultdict(lambda: {'brani': set(), 'tasti': [], 'ruoli': collections.Counter()})
song_cache = {}
for i, nm in enumerate(sd.names['SEQ']):
    if not nm or not A.is_music_slot(nm) or not sd.seq_info(i):
        continue
    bank = sd.name('BANK', sd.seq_info(i)['banco'])
    tracks = A.simulate(sd.seq_data(i))
    song_cache[nm] = tracks
    meds = []
    for tr in tracks:
        ks = [k for _, k, v, _, _, _ in tr.notes if v]
        if ks:
            meds.append((statistics.median(ks), tr.n, tr))
    meds.sort(key=lambda x: (x[0], x[1]))
    for r, (m, n, tr) in enumerate(meds):
        ruolo = 'basso' if r == 0 and len(meds) > 1 else ('melodia' if r == len(meds) - 1 else 'mezzo')
        for t, k, v, d, p, _ in tr.notes:
            if not v:
                continue
            u = uso.setdefault((bank, p), {'brani': set(), 'min': 127, 'max': 0, 'note': 0})
            u['brani'].add(nm)
            u['min'], u['max'] = min(u['min'], k), max(u['max'], k)
            u['note'] += 1
            if p < 60 and (bank != 'BANK_BGM_ARCEUS' or p != 30):
                c = uso_comune[p]
                c['brani'].add(nm)
                c['tasti'].append(k)
                c['ruoli'][ruolo] += 1


def regioni(inst):
    out = []
    for lo, hi, r in inst['regioni']:
        e = {'tasti': [A.note_name(lo), A.note_name(hi)] if lo != hi else A.note_name(lo), 'tipo': r['tipo']}
        if r['tipo'] == 'psg':
            e['duty'] = r['swav']
        elif r['tipo'] == 'pcm':
            e['onda'] = [r['swar'], r['swav']]
        e['nota_base'] = A.note_name(r['nota_base'])
        e['adsr'] = r['adsr']
        out.append(e)
    return out


def descr_zone(inst):
    regs = inst['regioni']
    if inst['tipo'] == 'batteria':
        return 'batteria %s–%s (%d tasti)' % (A.note_name(regs[0][0]), A.note_name(regs[-1][1]), len(regs))
    if inst['tipo'] == 'divisione':
        return '%d zone' % len(regs)
    return '1 zona'


# --- slot del registro
slots = []
for r in reg['campo']:
    slots.append({'simbolo': r['simbolo'], 'slot': r['slot_hg_sostituito'], 'gemello': r['gemello_gb_sounds'],
                  'blocco': r['blocco_modulo_5'], 'uso': ', '.join(r['mappe'][:3]) + (' …' if len(r['mappe']) > 3 else ''),
                  'tipo': 'campo'})
for r in reg['lotta']:
    slots.append({'simbolo': r['simbolo'], 'slot': r['slot_hg'], 'gemello': r['gemello_gb_sounds'],
                  'blocco': r['blocco_modulo_5'], 'uso': r['uso'], 'tipo': 'lotta'})
file_users = collections.defaultdict(list)
for i, nm in enumerate(sd.names['SEQ']):
    if nm and sd.seq_info(i):
        file_users[sd.seq_info(i)['file']].append(nm)
reg_slots = {s['slot'] for s in slots}
for s in slots:
    i = sd.seq_index(s['slot'])
    if vals.get(s['slot']) != i:
        err('%s: valore diverso fra sndseq.h e archivio' % s['slot'])
    tw = A.twin_of(sd, s['slot'])
    if tw != s['gemello']:
        err('%s: gemello %s, registro %s' % (s['slot'], tw, s['gemello']))
    inf = sd.seq_info(i)
    tracks = song_cache[s['slot']]
    lp = A.song_loop(tracks)
    bank = sd.name('BANK', inf['banco'])
    poly = A.polyphony(tracks, A.kind_func(insts[bank]), until=lp[1] if lp and lp != 'diversi' else None)
    others = [u for u in file_users[inf['file']] if u != s['slot']]
    s.update({'valore': i, 'lettore': sd.name('PLAYER', inf['lettore']), 'banco': bank, 'volume': inf['volume'],
              'byte': len(sd.seq_data(i)), 'ritornello': lp is not None, 'polifonia': poly['totale'],
              'tracce': len(tracks), 'condivide_file_con': others})
n_condivisi = sum(1 for s in slots if s['condivide_file_con'])
n_gemelli_slot = sum(1 for s in slots if s['gemello'])

# --- suoni
fs = A.field_sounds(REPO, sd)
se_campo = sorted(((n, c) for n, c in fs['PlaySE'].items() if n.startswith('SEQ_')), key=lambda x: (-x[1], x[0]))
fanfare = sorted(((n, c) for n, c in fs['PlayFanfare'].items() if n.startswith('SEQ_')), key=lambda x: (-x[1], x[0]))
cry_uses = sum(fs['PlayCry'].values())
stopse = 0
for fn in glob.glob(REPO + '/files/fielddata/script/scr_seq/*.s'):
    with open(fn, encoding='utf-8', errors='replace') as f:
        stopse += sum(1 for line in f if re.match(r'\s*StopSE SEQ_SE_GS_N_', line))


def seq_row(nm):
    i = sd.index[nm][1]
    inf = sd.seq_info(i)
    lp = A.song_loop(A.simulate(sd.seq_data(i)))
    return i, sd.name('BANK', inf['banco']), sd.name('PLAYER', inf['lettore']), lp is not None


me_names = [n for n in sd.names['SEQ'] if n and n.startswith('SEQ_ME_') and sd.seq_info(sd.index[n][1])]
n_se = sum(1 for n in sd.names['SEQ'] if n and n.startswith('SEQ_SE_') and sd.seq_info(sd.index[n][1]))
n_pv_arc = sum(1 for n in sd.names['WAVEARC'] if n and n.startswith('WAVE_ARC_PV'))
n_pv_bank = sum(1 for n in sd.names['BANK'] if n and n.startswith('BANK_PV'))
src = open(REPO + '/src/field/field_control.c', encoding='utf-8').read()
piastre = re.findall(r'\[SOUNDPLATE_SOUND_(\w+)\] = \{ (SEQ_\w+),\s*(TRUE|FALSE)\s*\}', src)
species_h = open(REPO + '/include/constants/species.h', encoding='utf-8').read()
for sp in ('SPECIES_ZUBAT', 'SPECIES_WHISMUR'):
    if not re.search(r'#define %s\b' % sp, species_h):
        err('%s non esiste' % sp)
for nm in ('SEQ_SE_DP_KON', 'SEQ_SE_DP_PINPON'):
    if nm not in fs['PlaySE'] or seq_row(nm)[3]:
        err('%s non è un effetto di campo che non si ripete' % nm)
for nm in T.SIGNIFICATO_SE:
    if nm not in fs['PlaySE'] and nm not in fs['PlayFanfare']:
        err('significato di %s, che gli script di campo non suonano' % nm)
for k in T.PIASTRE_USO:
    if k not in [p[0] for p in piastre]:
        err('piastra sconosciuta %s' % k)

# --- valori per i testi
V = dict(versione=T.VERSIONE, data=T.DATA, sha1=sha1, sdat_byte='{:,}'.format(len(raw)).replace(',', ' '),
         n_banchi=len(banks), n_slot=len(slots), n_gemelli=len(pairs), n_nomi=len(vals) - 1, n_alias=len(aliases),
         n_gemelli_slot=n_gemelli_slot, n_senza_gemello=len(slots) - n_gemelli_slot, n_condivisi=n_condivisi,
         canali=ch['totale'], psg=ch['psg'], rumore=ch['rumore'], heap_field=lim['PLAYER_FIELD']['heap_lettore'],
         carico_field=lim['PLAYER_FIELD']['carico_max'], carico_bgm=lim['PLAYER_BGM']['carico_max'],
         n_se_campo=len(se_campo), n_fanfare=len(fanfare), n_piastre=len(piastre), n_stopse=stopse, **COLLAUDO)
for k in ('heap_field', 'carico_field', 'carico_bgm', 'campo_max'):
    V[k] = '{:,}'.format(V[k]).replace(',', ' ')
V['poly_hg_max'] = max(s['polifonia'] for s in slots)
V['n_pv_arc'] = n_pv_arc


def fmt(s):
    return s.format(**V)


def num(n):
    return '{:,}'.format(n).replace(',', ' ')


md = [fmt(T.INTESTAZIONE), '', fmt(T.IN_BREVE), '', fmt(T.STRUMENTO), '', fmt(T.COLLAUDO), '', fmt(T.PIPELINE), '']
md += ['## 4. Regole', '', '| Codice | Regola | Testo |', '|---|---|---|']
for code, title, text in T.REGOLE:
    md.append('| %s | %s | %s |' % (code, title, fmt(text)))
md += ['', T.CONVENZIONE, '']

# 6. lettori
md += ['## 6. Lettori e limiti', '',
       'Un lettore (`PLAYER_*`) è il canale logico su cui suona una sequenza. I canali sono i 16 canali hardware del DS: '
       '0–7 solo PCM, 8–13 PCM o PSG (onda quadra), 14–15 PCM o rumore. Il lettore usa solo quelli della sua maschera.', '',
       '| Lettore | Sequenze insieme | Canali (maschera) | Di cui PSG / rumore | Heap del lettore | Usato da |',
       '|---|---:|---|---:|---:|---|']
fam_by_player = collections.defaultdict(collections.Counter)
for i, nm in enumerate(sd.names['SEQ']):
    if nm and sd.seq_info(i):
        f = 'musiche' if A.is_music_slot(nm) else ('gemelli GB' if '_P_' in nm[:9] else (
            'effetti' if nm.startswith('SEQ_SE') else ('jingle' if nm.startswith('SEQ_ME') else (
                'versi' if nm.startswith('SEQ_PV') else 'altro'))))
        fam_by_player[sd.name('PLAYER', sd.seq_info(i)['lettore'])][f] += 1
for p in range(len(sd.entries['PLAYER'])):
    nm = sd.name('PLAYER', p)
    pi = sd.player_info(p)
    c = A.player_channels(sd, p)
    chans = ','.join(str(k) for k in range(16) if pi['canali'] >> k & 1)
    used = ', '.join('%s %d' % (k, v) for k, v in fam_by_player[nm].most_common())
    md.append('| `%s` | %d | %d (%s) | %d / %d | %s | %s |' % (nm, pi['max_seq'], c['totale'], chans, c['psg'], c['rumore'],
                                                             num(pi['heap']) if pi['heap'] else '— (heap comune)', used or '—'))
md += ['', 'Carico massimo che HeartGold già usa (sequenza + banco + onde), il limite di A09:', '',
       '| Lettore | Carico massimo | Brano | Sequenza più lunga | Brano |', '|---|---:|---|---:|---|']
for p in ('PLAYER_FIELD', 'PLAYER_BGM'):
    l = lim[p]
    md.append('| `%s` | %s | `%s` | %s | `%s` |' % (p, num(l['carico_max']), l['carico_max_da'], num(l['sseq_max']), l['sseq_max_da']))
md += ['', 'L’heap generale del suono è `SND_HEAP_SIZE` = 0xBEAE0 (%s byte, `include/sound.h`). Le musiche di HeartGold '
       'usano fino a 16 tracce, quindi il limite di 16 tracce SSEQ non è stretto.' % num(0xBEAE0), '']

# 7. slot
md += ['## 7. I %d slot delle musiche' % len(slots), '',
       'Dal registro 2.5 (`musiche.campo` e `musiche.lotta`), coi dati dello slot HeartGold letti dall’archivio. «Byte» e '
       '«Note insieme» sono del brano HeartGold e danno l’ordine di grandezza; i limiti veri sono quelli di R-AUD-06. '
       '«Rit.» = lo slot si ripete, quindi la partitura deve avere `loopStart`/`loopEnd`.', '',
       '| # | Alias di Trinacria | Slot HeartGold | Valore | Gemello GB | Lettore | Banco | Vol. | Byte | Rit. | Note insieme | Blocco | Mappe o uso |',
       '|---:|---|---|---:|---|---|---|---:|---:|:-:|---:|---|---|']
for k, s in enumerate(slots, 1):
    md.append('| %d | `%s` | `%s` | %d | %s | %s | `%s` | %d | %s | %s | %d | %s | %s |' % (
        k, s['simbolo'], s['slot'], s['valore'], '`%s`' % s['gemello'] if s['gemello'] else '—',
        s['lettore'].replace('PLAYER_', ''), s['banco'], s['volume'], num(s['byte']), 'sì' if s['ritornello'] else 'no',
        s['polifonia'], s['blocco'], s['uso'].replace('|', '/')))
nr = sum(1 for s in slots if s['ritornello'])
md += ['', 'Si ripetono %d slot su %d; non si ripetono: %s.' % (
    nr, len(slots), ', '.join('`%s` (`%s`)' % (s['simbolo'], s['slot']) for s in slots if not s['ritornello']) or 'nessuno'), '']

# 8. file condivisi
md += ['## 8. Slot che condividono il file dei dati', '',
       'In HeartGold più voci di sequenza possono puntare allo stesso file (stessa musica con un altro banco o un altro nome). '
       'Per questi %d slot del registro `applica` crea un file proprio (R-AUD-03); le voci della colonna «Restano HeartGold» '
       'non cambiano. Le voci in grassetto sono anche loro slot del registro, con un brano diverso.' % n_condivisi, '',
       '| Slot del registro | Alias | Stesso file di | Restano HeartGold |', '|---|---|---|---|']
alias_of = {s['slot']: s['simbolo'] for s in slots}
for s in slots:
    if s['condivide_file_con']:
        o = s['condivide_file_con']
        md.append('| `%s` | `%s` | %s | %s |' % (s['slot'], s['simbolo'],
                                              ', '.join('**`%s`**' % x if x in reg_slots else '`%s`' % x for x in o),
                                              ', '.join('`%s`' % x for x in o if x not in reg_slots) or '—'))
md += ['', 'Da notare: `SEQ_GS_R_1_29` (strade orientali) divide il file con `SEQ_GS_TITLE01`, `SEQ_GS_OPENING_TITLE_G/S`, '
       '`SEQ_DUMMY` e `SEQ_TEST_TITLE`; `SEQ_GS_SENKYO` con la radio del Team Rocket `SEQ_GS_SENKYO_R` (§12). Anche i gemelli '
       'GB condividono file fra loro: lo strumento li tratta allo stesso modo.', '']

# 9. banchi
md += ['## 9. Banchi SBNK', '', '### 9.1 Com’è fatto un banco', '',
       'Ogni banco musicale usa due archivi d’onda: `WAVE_ARC_BASIC` (%s byte, lo stesso per tutti) e uno proprio. '
       'I programmi 0–59 vengono tutti da `WAVE_ARC_BASIC` e sono **identici in tutti i %d banchi** (l’unica eccezione è il '
       'programma 30 di `BANK_BGM_ARCEUS`); i programmi propri (dal 60 in su) usano l’archivio del banco. Tipi: «zone» = '
       'strumento a zone di tasti (campioni diversi per registro), «pcm» = un solo campione, «batteria» = un campione per '
       'tasto, «psg» = onda quadra (canali 8–13), «rumore» = rumore bianco (canali 14–15).' % (
           num(len(sd.files[sd.wavearc_info(sd.bank_info(sd.bank_index('BANK_BASIC'))['wavearc'][0])['file']])), len(banks)), '',
       '### 9.2 La tavolozza comune (programmi 0–59)', '',
       'Uso nelle %d musiche di HeartGold: brani che lo usano, note suonate, registro (nota più bassa, mediana, più alta) e '
       'ruolo della traccia (traccia più grave del brano = basso, più acuta = melodia). I nomi degli strumenti non sono nei '
       'dati: per sentirli `onde BANK_BASIC --out <cartella>` scrive le onde in WAV.' % len(song_cache), '',
       '| Prg | Tipo | Zone | Brani HG | Note | Registro | Basso | Melodia |', '|---:|---|---|---:|---:|---|---:|---:|']
TIPO_IT = {'divisione': 'zone', 'pcm': 'pcm', 'batteria': 'batteria', 'psg': 'psg', 'rumore': 'rumore'}
palette = []
for p in range(60):
    inst = basic[p]
    c = uso_comune.get(p)
    if c and c['tasti']:
        ks = c['tasti']
        tot = sum(c['ruoli'].values())
        reg_txt = '%s · %s · %s' % (A.note_name(min(ks)), A.note_name(int(statistics.median(ks))), A.note_name(max(ks)))
        row = (len(c['brani']), len(ks), reg_txt, round(100 * c['ruoli']['basso'] / tot), round(100 * c['ruoli']['melodia'] / tot))
        md.append('| %d | %s | %s | %d | %s | %s | %d%% | %d%% |' % ((p, TIPO_IT[inst['tipo']], descr_zone(inst), row[0], num(row[1])) + row[2:]))
    else:
        row = None
        md.append('| %d | %s | %s | 0 | 0 | mai usato | — | — |' % (p, TIPO_IT[inst['tipo']], descr_zone(inst)))
    palette.append({'programma': p, 'tipo': TIPO_IT[inst['tipo']], 'regioni': regioni(inst),
                    'uso_heartgold': None if not row else {
                        'brani': row[0], 'elenco_brani': sorted(c['brani']), 'note': row[1], 'nota_min': A.note_name(min(c['tasti'])),
                        'nota_mediana': A.note_name(int(statistics.median(c['tasti']))),
                        'nota_max': A.note_name(max(c['tasti'])), 'basso_pct': row[3], 'melodia_pct': row[4]}})
drum = basic[39]['regioni']
md += ['', 'La batteria 39 (%s–%s) segue la disposizione General MIDI nei brani di HeartGold: i tasti più usati sono 38 '
       '(D2, rullante), 42 (F#2, charleston chiuso), 36 (C2) e 35 (B1, casse), 46 (A#2, charleston aperto), 40 (E2).' % (
           A.note_name(drum[0][0]), A.note_name(drum[-1][1])), '',
       '### 9.3 I %d banchi musicali' % len(banks), '',
       '| Banco | Indice | Carico (byte) | Programmi | Propri (60+) | Brani HG | Slot del registro |',
       '|---|---:|---:|---:|---|---:|---|']
banchi_json = []
for b in banks:
    bi = sd.bank_index(b)
    ins = insts[b]
    own = [p for p in range(len(ins)) if ins[p] and (p >= 60 or not same(ins[p], basic[p]))]
    users = [n for n in song_cache if sd.name('BANK', sd.seq_info(sd.index[n][1])['banco']) == b]
    rs = [s['simbolo'] for s in slots if s['banco'] == b]
    md.append('| `%s` | %d | %s | %d | %s | %d | %s |' % (
        b, bi, num(sd.bank_load_size(bi)), sum(1 for x in ins if x),
        ', '.join('%d %s' % (p, TIPO_IT[ins[p]['tipo']]) for p in own) or '—', len(users),
        ', '.join('`%s`' % x for x in rs) or '—'))
    progs = []
    for p in own:
        u = uso.get((b, p))
        progs.append({'programma': p, 'tipo': TIPO_IT[ins[p]['tipo']], 'regioni': regioni(ins[p]),
                      'uso_heartgold': None if not u else {'brani': sorted(u['brani']), 'note': u['note'],
                                                           'nota_min': A.note_name(u['min']), 'nota_max': A.note_name(u['max'])}})
    banchi_json.append({'banco': b, 'indice': bi, 'byte_carico': sd.bank_load_size(bi),
                        'archivi_onda': [sd.name('WAVEARC', w) for w in sd.bank_info(bi)['wavearc'] if w != 0xFFFF],
                        'programmi': sum(1 for x in ins if x), 'programmi_propri': progs,
                        'brani_heartgold': sorted(users), 'slot_del_registro': rs})
md.append('')

# 10. suoni
md += ['## 10. Suoni da mantenere al 100%', '', '### 10.1 Cosa resta identico', '',
       '| Famiglia | Voci | Come si usa | Controllo |', '|---|---:|---|---|',
       '| Effetti `SEQ_SE_*` | %d | `PlaySE`, `StopSE`, `WaitSE`; lotta e menu dal codice | A20 |' % n_se,
       '| Jingle `SEQ_ME_*` | %d | `PlayFanfare`, `WaitFanfare` | A20 |' % len(me_names),
       '| Versi dei Pokémon | %d banchi `BANK_PV*`, %d archivi `WAVE_ARC_PV*`, sequenze `SEQ_PV*` | `PlayCry SPECIES_X, 0`, `WaitCry` (%d chiamate negli script di HeartGold) | A20 |' % (n_pv_bank, n_pv_arc, cry_uses),
       '| Banchi e archivi d’onda | %d e %d | — | A20 |' % (len([x for x in sd.entries['BANK'] if x]), len([x for x in sd.entries['WAVEARC'] if x])),
       '| Musiche HeartGold fuori dal registro | %d | titolo, bicicletta, Surf, Pokéathlon, radio… | A20 |' % (
           len(song_cache) - len(slots)),
       '', 'Il codice di HeartGold che suona effetti e jingle non cambia: i nomi `SEQ_*` restano quelli di `sndseq.h`.', '',
       '### 10.2 Jingle', '',
       '| Jingle | Valore | Usi negli script di campo | Significato (dal nome) |', '|---|---:|---:|---|']
fan_count = dict(fanfare)
for n in me_names:
    md.append('| `%s` | %d | %d | %s |' % (n, sd.index[n][1], fan_count.get(n, 0), T.SIGNIFICATO_ME.get(n, '—')))
md += ['', 'Gli script di campo di HeartGold suonano con `PlayFanfare` %d sequenze: i jingle con usi > 0 qui sopra e '
       '`SEQ_SE_PL_KIRAKIRA` (%d volte).' % (len(fanfare), fan_count.get('SEQ_SE_PL_KIRAKIRA', 0)), '',
       '### 10.3 Effetti collaudati sul campo (R-AUD-09)', '',
       'I %d effetti che gli script di campo di HeartGold (`files/fielddata/script/scr_seq/`) suonano con `PlaySE`, '
       'in ordine di uso. «Si ripete» = l’effetto continua finché uno `StopSE` non lo ferma.' % len(se_campo), '',
       '| Effetto | Valore | Usi | Banco | Lettore | Si ripete | Significato (dal nome) |', '|---|---:|---:|---|---|:-:|---|']
se_json = []
for n, c in se_campo:
    i, b, p, lp = seq_row(n)
    md.append('| `%s` | %d | %d | `%s` | %s | %s | %s |' % (n, i, c, b, p.replace('PLAYER_', ''), 'sì' if lp else 'no',
                                                          T.SIGNIFICATO_SE.get(n, '—')))
    se_json.append({'effetto': n, 'valore': i, 'usi_heartgold': c, 'banco': b, 'lettore': p, 'si_ripete': lp,
                    'significato': T.SIGNIFICATO_SE.get(n)})
md += ['', '### 10.4 Versi', '',
       'Ogni specie ha il suo verso (`PlayCry SPECIES_X, 0`): i nomi delle specie restano i simboli `SPECIES_*` di HeartGold '
       'anche dove il Glossario dà il nome siciliano. Gli script di HeartGold chiamano `PlayCry` %d volte, con la specie scritta '
       'o in una variabile.' % cry_uses, '',
       '### 10.5 Tavolozza dell’Orecchio di Dionisio (S-SR-02, R-AUD-10)', '',
       '| Scelta | Suono | Comandi |', '|---:|---|---|']
for a, b, c in T.TAVOLOZZA_ECO:
    md.append('| %s | %s | %s |' % (a, b, c))
md += ['', 'Due versi della colonia e due effetti brevi del §10.3 che non si ripetono, tutti suonati già sul campo da HeartGold.', '',
       '### 10.6 Suoni d’ambiente: le piastre sonore (R-AUD-11)', '',
       'Tabella `sSoundplateSounds` di `src/field/field_control.c`: il suono parte quando il giocatore entra nella zona della piastra.', '',
       '| Piastra | Effetto | Si ripete | Uso proposto in Trinacria |', '|---|---|:-:|---|']
pi_json = []
for k, seqn, flag in piastre:
    lp = seq_row(seqn)[3]
    md.append('| `SOUNDPLATE_SOUND_%s` | `%s` | %s | %s |' % (k, seqn, 'sì' if lp else 'no', T.PIASTRE_USO.get(k, '—')))
    pi_json.append({'piastra': 'SOUNDPLATE_SOUND_' + k, 'effetto': seqn, 'si_ripete': lp, 'uso_proposto': T.PIASTRE_USO.get(k)})
md.append('')

# 11. codici
md += ['## 11. Codici d’errore', '',
       '| Codice | Comando | Significato |', '|---|---|---|',
       '| A00 | tutti | file mancante, argomenti sbagliati, archivio illeggibile |',
       '| A01 | applica | lo slot non è una musica `SEQ_GS_*` di HeartGold (né gemello `SEQ_GS_P_*`, né effetto) |',
       '| A02 | applica | file del brano mancante, né MIDI né SSEQ, o sequenza che non si esegue |',
       '| A03 | applica | banco che non è `BANK_BASIC` o `BANK_BGM_*` |',
       '| A04 | applica | volume fuori da 0–127 |',
       '| A05 | applica | nota su un programma vuoto o fuori dalle zone di tasti dello strumento |',
       '| A06 | applica | più note insieme dei canali del lettore (%d) |' % ch['totale'],
       '| A07 | applica | più note PSG (%d) o di rumore (%d) insieme dei canali adatti |' % (ch['psg'], ch['rumore']),
       '| A08 | applica | sequenza più grande dell’heap del lettore (%s byte su `PLAYER_FIELD`) |' % V['heap_field'],
       '| A09 | applica | sequenza + banco + onde oltre il carico massimo di HeartGold sul lettore |',
       '| A10 | applica | ritornello mancante, di troppo o diverso fra le tracce |',
       '| A11 | applica | slot usato da due brani |',
       '| A12 | applica, mid2sseq | MIDI fuori convenzione: controller sconosciuto, nota senza fine o fine senza nota |',
       '| A20 | controlla | voce o file cambiato fuori dagli slot del manifesto |',
       '| A21 | controlla | lo slot non contiene il brano, il banco o il volume del manifesto |',
       '| A22 | applica, controlla | l’archivio di partenza non è l’originale (SHA-1) |',
       '| C01–C04 | componi | partitura che non si esegue, simbolo diverso dal nome del file, simbolo fuori dal registro, simbolo doppio |',
       '', T.NOTE_BLOCCHI, '']

n_own = sum(len(b['programmi_propri']) for b in banchi_json)
riga = ('BLOCCO COMPLETO: 5.1 — strumento tools/trinacria_audio.py (A00–A22) collaudato: archivio ricostruito identico, '
        '%d sequenze in andata e ritorno identiche, %d gemelli e %d nomi verificati; %d slot del registro (%d con gemello GB, '
        '%d col file condiviso resi propri); %d banchi musicali (60 programmi comuni, %d propri); limiti %d canali (%d PSG, '
        '%d rumore), %s byte di sequenza su PLAYER_FIELD; suoni mantenuti: %d effetti, %d jingle, versi (%d archivi d’onda), '
        'con %d effetti e %d fanfare di campo, %d suoni d’ambiente e la tavolozza di S-SR-02; %d regole R-AUD; '
        'componi.py e prova_5_1.py → AUDIO_OK') % (
    COLLAUDO['n_rt'], len(pairs), len(vals) - 1, len(slots), n_gemelli_slot, n_condivisi, len(banks), n_own,
    ch['totale'], ch['psg'], ch['rumore'], V['heap_field'], n_se, len(me_names), n_pv_arc, len(se_campo), len(fanfare),
    len(piastre), len(T.REGOLE))
md += ['## 13. Riga di controllo', '', '`%s`' % riga, '']

catalogo = {'modulo': 5, 'blocco': '5.1', 'titolo': 'Banchi SBNK, slot delle musiche e suoni da mantenere',
            'versione': T.VERSIONE, 'data': T.DATA, 'fonte': {'archivio': 'files/data/sound/gs_sound_data.sdat', 'sha1': sha1,
                                                              'byte': len(raw)},
            'note': ['Generato da tools/generatori/5.1/gen51.py; il documento è docs/MODULO_5/5.1_PIPELINE_E_SFX.md.',
                     'Tasti in notazione scientifica (C4 = 60). «onda» = [indice dell’archivio nel banco, indice dell’onda].',
                     'adsr = attacco, decadimento, sostegno, rilascio grezzi (0–127).'],
            'lettori': {p: lim[p] for p in sorted(lim)},
            'tavolozza_comune': {'banco_di_riferimento': 'BANK_BASIC', 'programmi': palette},
            'banchi': banchi_json, 'slot': slots,
            'suoni': {'jingle': [{'jingle': n, 'valore': sd.index[n][1], 'usi_campo': fan_count.get(n, 0),
                                  'significato': T.SIGNIFICATO_ME.get(n)} for n in me_names],
                      'effetti_campo': se_json, 'fanfare_campo': [n for n, c in fanfare],
                      'piastre_sonore': pi_json,
                      'orecchio_di_dionisio': [{'scelta': a, 'suono': b, 'comandi': c} for a, b, c in T.TAVOLOZZA_ECO]},
            'riga_finale': riga}

if errors:
    sys.exit('%d errori: blocco non scritto' % len(errors))
os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
with open(OUT_MD, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))
with open(OUT_JSON, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(catalogo, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('%s: %d byte' % (OUT_MD, os.path.getsize(OUT_MD)))
print('%s: %d byte' % (OUT_JSON, os.path.getsize(OUT_JSON)))
print(riga)

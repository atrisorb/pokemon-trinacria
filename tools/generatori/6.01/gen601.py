"""Generatore del blocco 6.01 (Prologo: il Cubbar e la casa di Corso Italia).

Uso: python -I tools/generatori/6.01/gen601.py

Scrive i 18 file da copiare in docs/MODULO_6/6.01_FILE/, il registro degli NPC (6.01_NPC.csv),
l'indice docs/MODULO_6/6.01_PROLOGO.json e il documento 6.01_PROLOGO.md, poi lancia i controlli
(trinacria_script_check.py, registro NPC) e scrive il risultato nei due documenti. I testi stanno in
content601.py (messaggi), scripts601.py (script ed eventi) e text601.py (prosa). Serve il repository
pokeheartgold accanto al progetto (F:/Progetti/pokeheartgold): ne legge le chiavi dei banchi, il font
e le macro.
"""
import csv
import hashlib
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
REPO = os.path.normpath(os.path.join(PROJ, '..', 'pokeheartgold'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PROJ, 'tools'))
sys.stdout.reconfigure(errors='backslashreplace')

import content601 as C      # noqa: E402
import scripts601 as S      # noqa: E402
import text601 as T         # noqa: E402

DOCS = os.path.join(PROJ, 'docs')
OUT = os.path.join(DOCS, 'MODULO_6')
TREE = os.path.join(OUT, '6.01_FILE')
OUT_MD = os.path.join(OUT, '6.01_PROLOGO.md')
OUT_JSON = os.path.join(OUT, '6.01_PROLOGO.json')
OUT_CSV = os.path.join(OUT, '6.01_NPC.csv')
BLOCCO = '6.01'
PY = [sys.executable, '-X', 'utf8', '-I']

MAPPE = {
    'MAP_CT_MISTERBIANCO_CUBBAR': dict(codice='T25SP0101', script_n=910, hdr_n=683, ev_n='488_T25SP0101', fn=S.cubbar),
    'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F': dict(codice='T20R0202', script_n=846, hdr_n=619, ev_n='061_T20R0202', fn=S.camera),
    'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F': dict(codice='T20R0201', script_n=845, hdr_n=618, ev_n='060_T20R0201', fn=S.casa),
}

# attributi del registro NPC per ogni oggetto (R-SCR-10)
NPC = {
    'obj_t25sp0101_christian': dict(ruolo='COMPAGNO', cat='ESENTE', area='CT_GALERMO', codice='C-03',
                                    note='Prologo: all’ingresso VIP; si unisce nel capitolo 2 (Galermo); sparisce con FLAG_M_CT_00'),
    'obj_t25sp0101_subwoofer': dict(ruolo='POKEMON', cat='ESENTE', area='ITALIANO', specie='SPECIES_EXPLOUD',
                                    accanto='obj_t25sp0101_christian', note='Subwoofer è il nome della specie (Glossario G30-0024)'),
    'obj_t25sp0101_figlio_avvocato': dict(ruolo='POPOLO', cat='CAPRO', area='CT_CORSO_ITALIA', note='figlio d’avvocato; ha il Gattupardu'),
    'obj_t25sp0101_gattupardu': dict(ruolo='POKEMON', cat='ESENTE', area='ITALIANO', specie='SPECIES_PERSIAN',
                                     accanto='obj_t25sp0101_figlio_avvocato', note='Pokémon da salotto'),
    'obj_t25sp0101_figlia_magistrato': dict(ruolo='POPOLO', cat='ESTIMATORE', area='CT_CORSO_ITALIA', note='figlia di magistrato; ha il Novicudi'),
    'obj_t25sp0101_novicudi': dict(ruolo='POKEMON', cat='ESENTE', area='ITALIANO', specie='SPECIES_NINETALES',
                                   accanto='obj_t25sp0101_figlia_magistrato', note='Pokémon da salotto'),
    'obj_t25sp0101_praticante': dict(ruolo='POPOLO', cat='CAPRO', area='CT_CORSO_ITALIA', note='praticante di uno studio legale'),
    'obj_t25sp0101_pr_locale': dict(ruolo='POPOLO', cat='ESTIMATORE', area='CT_CORSO_ITALIA', note='PR del locale'),
    'obj_t25sp0101_figlia_magistrato_2': dict(ruolo='POPOLO', cat='CAPRO', area='CT_CORSO_ITALIA', note='figlia di magistrato'),
    'obj_t25sp0101_figlio_imprenditore': dict(ruolo='POPOLO', cat='CAPRO', area='CT_CORSO_ITALIA', note='figlio di un imprenditore; ha il Diavulazzu'),
    'obj_t25sp0101_diavulazzu': dict(ruolo='POKEMON', cat='ESENTE', area='ITALIANO', specie='SPECIES_HOUNDOOM',
                                     accanto='obj_t25sp0101_figlio_imprenditore', note='collare con una targhetta senza nome'),
    'obj_t20r0201_graziella': dict(ruolo='PERSONAGGIO', cat='ESENTE', area='CT_CORSO_ITALIA', codice='M-CT-01',
                                   note='la madre del protagonista; custodisce i risparmi'),
    'obj_t20r0201_puparu': dict(ruolo='POKEMON', cat='ESENTE', area='ITALIANO', specie='SPECIES_MR_MIME',
                                accanto='obj_t20r0201_graziella', note='domestico di casa'),
    'obj_t20r0201_leccu': dict(ruolo='POKEMON', cat='ESENTE', area='ITALIANO', specie='SPECIES_DELCATTY',
                               accanto='obj_t20r0201_graziella', note='Pokémon da divano'),
}

RISORSE = {
    'flag_impostati': [
        {'simbolo': 'FLAG_M_CT_00', 'dove': 'T25SP0101_013', 'nota': 'alias FLAG_INTRO_CUBBAR; fine del flashback; nasconde Christian e il Subwoofer'},
        {'simbolo': 'FLAG_M_CT_01', 'dove': 'T20R0201_000', 'nota': 'M-CT-01 completata (nessun Consenso)'},
        {'simbolo': 'FLAG_GOT_BAG', 'dove': 'T20R0201_000', 'nota': 'flag del motore (menu): lo zaino'},
        {'simbolo': 'FLAG_GOT_TRAINER_CARD', 'dove': 'T20R0201_000', 'nota': 'flag del motore (menu): la tessera'},
        {'simbolo': 'FLAG_GOT_SAVE_BUTTON', 'dove': 'T20R0201_000', 'nota': 'flag del motore (menu): il salvataggio'},
        {'simbolo': 'FLAG_GOT_OPTIONS_BUTTON', 'dove': 'T20R0201_000', 'nota': 'flag del motore (menu): le opzioni'},
        {'simbolo': 'FLAG_GOT_POKEGEAR', 'dove': 'T20R0201_000', 'nota': 'registro 2.4: il telefono del protagonista'},
        {'simbolo': 'FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL', 'dove': 'T20R0201_001', 'nota': 'nome di HeartGold: prima proposta dei risparmi'},
        {'simbolo': 'FLAG_SYS_MOMS_SAVINGS', 'dove': 'T20R0201_001', 'nota': 'letto dal C: parte del premio in denaro va alla madre'},
    ],
    'flag_letti': ['FLAG_GOT_STARTER'],
    'variabili': [
        {'simbolo': 'VAR_TR_SCENE_CT_01', 'valori': '0-6 (§3 del documento)', 'nota': 'una sola variabile di scena per M-CT-00 e M-CT-01'},
        {'simbolo': 'VAR_TRINACRIA_ATTO', 'valori': '0 → 1', 'nota': 'impostata a 1 da T20R0201_000 (Atto I)'},
    ],
    'comandi_speciali': ['ScrCmd_804 2 (T20R0202_003): livello 2 della mappa del Pokégear (4.4, R-GFX-33)'],
    'prossimi_liberi': {'variabile_di_scena_CT': 'VAR_TR_SCENE_CT_02', 'flag_nascondi_CT': 'FLAG_TR_HIDE_CT_001 (nessuno consumato)'},
}

ANCORE = [
    {'da': 'MAP_CT_MISTERBIANCO_CUBBAR', 'x': 16, 'z': 24, 'verso': 'MAP_CT_MISTERBIANCO', 'indice': 0, 'blocco': '6.07'},
    {'da': 'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F', 'x': 3, 'z': 10, 'verso': 'MAP_CT_CATANIA_CORSO_ITALIA', 'indice': 1, 'blocco': '6.05'},
    {'da': 'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F', 'x': 3, 'z': 3, 'verso': 'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F', 'indice': 0, 'blocco': '6.01'},
    {'da': 'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F', 'x': 3, 'z': 4, 'verso': 'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F', 'indice': 1, 'blocco': '6.01'},
]


def sha1(b):
    return hashlib.sha1(b).hexdigest()


def scrivi(rel, testo, files, mappa, tipo, azione):
    p = os.path.join(TREE, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    b = testo.encode('utf-8')
    with open(p, 'wb') as f:
        f.write(b)
    files.append({'percorso': rel.replace('\\', '/'), 'tipo': tipo, 'mappa': mappa, 'azione': azione, 'sha1': sha1(b)})


def banco_json(nome, key, testi):
    msgs = []
    for i, t in enumerate(testi):
        parti, cur = [], ''
        for ch in t:
            cur += ch
            if ch in '\n\r\f':
                parti.append(cur)
                cur = ''
        if cur or not parti:
            parti.append(cur)
        msgs.append({'id': '%s_%05d' % (nome, i), 'en_US': parti if len(parti) > 1 else parti[0]})
    return json.dumps({'key': key, 'messages': msgs}, ensure_ascii=False, indent=2) + '\n'


def key_hg(banco):
    p = os.path.join(REPO, 'files', 'msgdata', 'msg', banco + '.json')
    return json.load(open(p, encoding='utf-8'))['key']


def esegui(cmd, cwd=PROJ):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    if os.path.isdir(TREE):
        import shutil
        shutil.rmtree(TREE)
    os.makedirs(TREE)
    files, mappe, testi, npc_rows = [], [], [], []
    eventi = S.eventi()
    tot = dict(messaggi=0, script=0, oggetti=0)
    for sym, m in MAPPE.items():
        codice = m['codice']
        b = C.BANCHI[sym]
        testo_s, hdr_s, n_scr = m['fn']()
        ev = eventi[sym]
        mp = dict(simbolo=sym, codice_file_hg=codice, banco_campagna=b['banco'], gemello=b['gemello'],
                  n_messaggi=len(b['messaggi']), n_script=n_scr, n_oggetti=len(ev['objects']))
        rel = {
            'banco': 'files/msgdata/msg/%s.json' % b['banco'],
            'gemello': 'files/msgdata/msg/%s.json' % b['gemello'],
            'script': 'files/fielddata/script/scr_seq/scr_seq_%04d_%s.s' % (m['script_n'], codice),
            'hdr': 'files/fielddata/script/scr_seq/scr_seq_%04d_%s_hdr.s' % (m['hdr_n'], codice),
            'event_h': 'files/fielddata/script/scr_seq/event_%s.h' % codice,
            'eventi': 'files/fielddata/eventdata/zone_event/%s.json' % m['ev_n'],
        }
        key = key_hg(b['banco'])
        scrivi(rel['banco'], banco_json(b['banco'], key, [x['testo'] for x in b['messaggi']]), files, sym, 'banco di campagna', 'sostituisci')
        scrivi(rel['gemello'], banco_json(b['gemello'], key, [x['twin'] for x in b['messaggi']]), files, sym, 'banco gemello post-dimissioni', 'nuovo')
        scrivi(rel['script'], testo_s, files, sym, 'script', 'sostituisci')
        scrivi(rel['hdr'], hdr_s, files, sym, 'intestazione degli script (OnFrame)', 'sostituisci')
        scrivi(rel['event_h'], S.header_eventi(codice, n_scr, ev['objects']), files, sym, 'header degli eventi', 'sostituisci')
        scrivi(rel['eventi'], json.dumps(ev, ensure_ascii=False, indent=2), files, sym, 'zone_event', 'sostituisci')
        mp.update(file_banco=rel['banco'], file_gemello=rel['gemello'], file_script=rel['script'],
                  file_header_script=rel['hdr'], file_event_h=rel['event_h'], file_eventi=rel['eventi'])
        mappe.append(mp)
        for i, x in enumerate(b['messaggi']):
            testi.append({'id': '%s_%05d' % (b['banco'], i), 'lingua': x['lingua'], 'area': x['area'], 'testo': x['testo']})
            testi.append({'id': '%s_%05d' % (b['gemello'], i), 'lingua': x['lingua'], 'area': x['area'], 'testo': x['twin']})
        tot['messaggi'] += len(b['messaggi'])
        tot['script'] += n_scr
        tot['oggetti'] += len(ev['objects'])
        # righe NPC
        import trinacria_script_check as K
        for o in ev['objects']:
            a = NPC[o['id']]
            first = K._first_msg_deep(testo_s, int(o['scriptId'].split('_')[-1].split(' ')[0]), codice, b['banco'])
            npc_rows.append({
                'map_symbol': sym, 'npc_id': o['id'], 'x': o['x'], 'y': o['z'], 'sprite': o['spriteId'],
                'msg_bank': b['banco'], 'msg_index': '%05d' % first, 'post_category': a['cat'], 'dialect_area': a['area'],
                'ruolo': a['ruolo'], 'visibile': 'SEMPRE', 'hide_flag': '' if o['eventFlag'] == 'FLAG_NOTHING' else o['eventFlag'],
                'trainer_id': '', 'pokemon_species': a.get('specie', ''), 'accanto_a': a.get('accanto', ''),
                'codice_trama': a.get('codice', ''), 'note': a['note']})
    # CSV
    buf = io.StringIO(newline='')
    w = csv.DictWriter(buf, fieldnames=['map_symbol', 'npc_id', 'x', 'y', 'sprite', 'msg_bank', 'msg_index', 'post_category',
                                         'dialect_area', 'ruolo', 'visibile', 'hide_flag', 'trainer_id', 'pokemon_species',
                                         'accanto_a', 'codice_trama', 'note'], lineterminator='\n', quoting=csv.QUOTE_NONE, escapechar='\\')
    w.writeheader()
    w.writerows(npc_rows)
    with open(OUT_CSV, 'w', encoding='utf-8', newline='') as f:
        f.write(buf.getvalue())

    doc = {
        'modulo': 'MODULO 6 - MASTER_SCRIPT_AND_DIALOGUE_BIBLE', 'blocco': BLOCCO,
        'titolo': 'Prologo: il Cubbar (M-CT-00) e la casa di Corso Italia (M-CT-01)', 'versione': T.VERSIONE, 'data': '2026-11-08',
        'progetto': 'Pokémon Trinacria - autore e copyright: atrisorb',
        'file': 'F:\\Progetti\\pokémon-sicilia\\docs\\MODULO_6\\6.01_PROLOGO.json',
        'lettore': 'LLM esecutore: i file di 6.01_FILE si copiano nel repository (Modulo 7, blocco 7.5); nessuna decisione.',
        'fonti': ['trama v1.9 (M-CT-00, M-CT-01)', 'registri 2.1, 2.4, 2.5', 'blocchi 3.x (Glossario)', '4.2 (stanza del Cubbar)', '4.4 (R-GFX-33)',
                  'pokeheartgold: asm/macros, scr_seq, zone_event, msg_0545/0546/0603'],
        'cartella_file': 'docs/MODULO_6/6.01_FILE',
        'mappe': mappe, 'npc': npc_rows, 'testi': testi, 'glossario_aggiunte': [],
        'risorse': RISORSE, 'ancore_attese': ANCORE,
        'aperti': ['msg_0219 (discorso iniziale di HeartGold) e tutta l\'interfaccia sono in inglese fino alla richiesta 6.00 (scaletta v2.24, da fare per prima)',
                   '60/40 provvisorio di CT: 4 CAPRO e 2 ESTIMATORE',
                   'sprite dinamici dei Pokémon in scena (Exploud, Ninetales, Houndoom, Mr. Mime, Delcatty): prova a schermo nel 7.4'],
        'controllo': {},
    }
    doc['file_da_copiare'] = files  # elenco dei file (percorso, sha1, azione): l'indice del blocco
    json.dump(doc, open(OUT_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    open(OUT_JSON, 'a', encoding='utf-8', newline='\n').write('\n')

    # --- controlli
    risultati = []
    rc, out = esegui(PY + ['tools/trinacria_script_check.py', 'check', 'docs/MODULO_6/6.01_PROLOGO.json', '--repo', REPO])
    risultati.append(('python -I tools/trinacria_script_check.py check docs/MODULO_6/6.01_PROLOGO.json', out.splitlines()[-1] if out else '?', out))
    if rc != 0:
        print(out)
        print('SCRIPT_CHECK_FALLITO: il documento non si scrive')
        return 1
    rc, out = esegui(PY + ['tools/trinacria_registry_check.py', '--npc', 'docs/MODULO_6/6.01_NPC.csv', '--repo', REPO])
    risultati.append(('python -I tools/trinacria_registry_check.py --npc docs/MODULO_6/6.01_NPC.csv --repo <pokeheartgold>', out.splitlines()[-1] if out else '?', out))
    if 'REGISTRY_OK' not in out:
        print(out)
        print('REGISTRO_NPC_FALLITO: il documento non si scrive')
        return 1
    righe = []
    for sym, m in MAPPE.items():
        b = C.BANCHI[sym]
        rc, out = esegui(PY + ['tools/trinacria_msg_lint.py', '--root', REPO, '--pair',
                               'docs/MODULO_6/6.01_FILE/files/msgdata/msg/%s.json' % b['banco'],
                               'docs/MODULO_6/6.01_FILE/files/msgdata/msg/%s.json' % b['gemello']])
        righe.append((b['banco'], b['gemello'], out.splitlines()[-1] if out else '?'))
        if rc != 0:
            print(out)
            return 1
    avvisi = [l for l in risultati[1][2].splitlines() if l.startswith('AVVISO')]

    import gen601_md
    gen601_md.scrivi(OUT_MD, doc, files, risultati, righe, avvisi, MAPPE, C, S, T, NPC, tot, PROJ)
    doc['controllo'] = {'script_check': risultati[0][1], 'registro_npc': risultati[1][1],
                        'linter': {'%s / %s' % (a, b_): c for a, b_, c in righe}, 'avvisi_registro': len(avvisi)}
    doc['riga_finale'] = gen601_md.riga_finale(doc, tot)
    json.dump(doc, open(OUT_JSON, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    open(OUT_JSON, 'a', encoding='utf-8', newline='\n').write('\n')
    print(doc['riga_finale'])
    return 0


if __name__ == '__main__':
    sys.exit(main())

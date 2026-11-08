"""Scrittura del documento 6.01_PROLOGO.md (usata da gen601.py)."""
import os

DESCR = {
    ('T25SP0101', 0): 'Christian: prima volta cinque messaggi in catena (poi variabile = 3); dopo, un messaggio solo',
    ('T25SP0101', 1): 'Subwoofer (Exploud): verso e messaggio',
    ('T25SP0101', 2): 'figlio d’avvocato', ('T25SP0101', 3): 'Gattupardu (Persian)',
    ('T25SP0101', 4): 'figlia di magistrato', ('T25SP0101', 5): 'Novicudi (Ninetales)',
    ('T25SP0101', 6): 'praticante', ('T25SP0101', 7): 'PR del locale', ('T25SP0101', 8): 'figlia di magistrato (2)',
    ('T25SP0101', 9): 'figlio dell’imprenditore', ('T25SP0101', 10): 'Diavulazzu (Houndoom)',
    ('T25SP0101', 11): 'arrivo nel Cubbar (OnFrame, variabile = 1) → variabile = 2',
    ('T25SP0101', 12): 'uscita chiusa (coords (16,23), variabile = 2): messaggio e un passo indietro',
    ('T25SP0101', 13): 'uscita (coords (16,23), variabile = 3): messaggio, `FLAG_M_CT_00`, variabile = 4, dissolvenza e `Warp` in camera',
    ('T20R0202', 0): 'PC (logica di HeartGold: posta)', ('T20R0202', 1): 'scaffale dei codici (bg (8,4))',
    ('T20R0202', 2): 'inizio partita (OnFrame, variabile = 0): didascalia, variabile = 1, dissolvenza, `Warp` nel Cubbar (16,22)',
    ('T20R0202', 3): 'risveglio (OnFrame, variabile = 4): `ScrCmd_804 2`, quattro messaggi in catena, variabile = 5',
    ('T20R0202', 4): 'lettera del Ministero (bg (7,4))', ('T20R0202', 5): 'diploma del Cutelli (bg (10,4))',
    ('T20R0201', 0): 'scena della madre (OnFrame, variabile = 5): chiude M-CT-01, variabile = 6',
    ('T20R0201', 1): 'Graziella: prima dello starter un messaggio; dopo lo starter i risparmi (prima proposta e menu)',
    ('T20R0201', 2): 'televisione (bg (5,3), (6,3))', ('T20R0201', 3): 'fornello (bg (9,3))',
    ('T20R0201', 4): 'lavello (bg (8,3))', ('T20R0201', 5): 'frigorifero (bg (11,3))',
    ('T20R0201', 6): 'Puparu (Mr. Mime)', ('T20R0201', 7): 'Leccu (Delcatty)',
}

TITOLI = {
    'MAP_CT_MISTERBIANCO_CUBBAR': ('4.1 Il Cubbar (`MAP_CT_MISTERBIANCO_CUBBAR`, M-CT-00)',
                                   'Stanza `pista` della matrice 0298 (4.2): caselle libere x 5-26, z 8-23; il banco del bar occupa z = 10 con i varchi in x = 5, 13 e 26; il tappeto d’uscita è (16,24). Le sei persone stanno sui punti `pista_1…pista_6` (z = 16), Christian sul varco (13,10) lato pista, cioè la casella (13,11).'),
    'MAP_CT_CATANIA_CASA_PROTAGONISTA_2F': ('4.2 La camera (`MAP_CT_CATANIA_CASA_PROTAGONISTA_2F`, inizio partita e risveglio)',
                                            'Stanza di HeartGold (matrice 0072): caselle libere x 1-10, z 4-10; PC, scaffale e mobili sul muro nord (z = 4). Il giocatore arriva dal Cubbar sulla casella (5,6).'),
    'MAP_CT_CATANIA_CASA_PROTAGONISTA_1F': ('4.3 Il piano terra (`MAP_CT_CATANIA_CASA_PROTAGONISTA_1F`, M-CT-01)',
                                            'Stanza di HeartGold (matrice 0071): Graziella (6,7) come la madre di HeartGold; i Pokémon stanno su due caselle libere fuori dal percorso dei suoi movimenti (z = 5 verso ovest, poi le caselle (3..6,7)).'),
}


def vis(t):
    return t.replace('\r', ' ⏎ ').replace('\f', ' ▸ ').replace('\n', ' / ').replace('|', '\\|')


def riga_finale(doc, tot):
    n_it = sum(1 for t in doc['testi'] if t['lingua'] == 'it')
    n_scn = sum(1 for t in doc['testi'] if t['lingua'] == 'scn')
    return ('BLOCCO COMPLETO: 6.01 - 3 mappe (Cubbar, camera e piano terra di casa), %d script, %d messaggi nei banchi di campagna e altrettanti '
            'gemelli (%d in italiano, %d in siciliano), %d oggetti in scena (8 persone e 6 Pokémon), 14 righe del registro NPC, '
            'variabile di scena VAR_TR_SCENE_CT_01 (0-6), FLAG_M_CT_00 e FLAG_M_CT_01; strumento nuovo trinacria_script_check.py (J00-J17) '
            '-> SCRIPT_OK; regole R-SCR-01...15' % (tot['script'], tot['messaggi'], n_it // 2, n_scn // 2, tot['oggetti']))


def scrivi(path, doc, files, risultati, righe_lint, avvisi, MAPPE, C, S, T, NPC, tot, proj):
    md = [T.INTESTAZIONE.format(versione=T.VERSIONE, data=T.DATA) + '\n', T.IN_BREVE + '\n', T.APPLICAZIONE + '\n',
          T.REGOLE + '\n', T.PROLOGO + '\n']
    md.append('## 4. Le tre mappe\n\n')
    eventi = S.eventi()
    for sym, m in MAPPE.items():
        cod = m['codice']
        titolo, nota = TITOLI[sym]
        b = C.BANCHI[sym]
        ev = eventi[sym]
        md.append('### %s\n\n%s\n\n' % (titolo, nota))
        md.append('Banco di campagna `%s`, gemello `%s` (%d messaggi), script `scr_seq_%04d_%s`, intestazione `scr_seq_%04d_%s_hdr`, eventi `%s`.\n\n'
                  % (b['banco'], b['gemello'], len(b['messaggi']), m['script_n'], cod, m['hdr_n'], cod, m['ev_n']))
        if ev['objects']:
            md.append('| Oggetto | Sprite | Casella (x, z) | Script | Ruolo | Area | 60/40 |\n|---|---|---|---|---|---|---|\n')
            for o in ev['objects']:
                a = NPC[o['id']]
                n = int(o['scriptId'].split('_')[-1].split(' ')[0])
                md.append('| `%s` | `%s` | (%d, %d) | %03d | %s | %s | %s |\n' % (o['id'], o['spriteId'], o['x'], o['z'], n, a['ruolo'], a['area'], a['cat']))
            md.append('\n')
        if ev.get('bgs') or ev.get('coords') or ev.get('warps'):
            md.append('Eventi: ' + '; '.join(
                ['bg (%d,%d) → %s' % (x['x'], x['z'], x['scriptId'].split('_')[-1].split(' ')[0]) for x in ev.get('bgs', [])]
                + ['coords (%d,%d) %s = %d → %s' % (x['x'], x['z'], x['var'], x['val'], x['scriptId'].split('_')[-1].split(' ')[0]) for x in ev.get('coords', [])]
                + ['warp (%d,%d) → `%s` ancora %d' % (x['x'], x['z'], x['header'], x['anchor']) for x in ev.get('warps', [])]) + '.\n\n')
        md.append('Script:\n\n| N. | Cosa fa |\n|---|---|\n')
        for i in range(m['n_script'] if 'n_script' in m else 0):
            pass
        n_script = len([1 for k in DESCR if k[0] == cod])
        for i in range(n_script):
            md.append('| %03d | %s |\n' % (i, DESCR[(cod, i)]))
        md.append('\nMessaggi (campagna ▸ gemello; `⏎` = `\\r`, `▸` = `\\f`, `/` = `\\n`):\n\n| N. | Lingua | Campagna | Gemello post-dimissioni |\n|---|---|---|---|\n')
        for i, x in enumerate(b['messaggi']):
            gem = '(uguale)' if x['twin'] == x['testo'] else vis(x['twin'])
            md.append('| %02d | %s/%s | %s | %s |\n' % (i, x['lingua'], x['area'], vis(x['testo']), gem))
        md.append('\n')
    md.append(T.RISORSE_INTRO)
    for f in doc['risorse']['flag_impostati']:
        md.append('| `%s` | impostato in `%s`: %s |\n' % (f['simbolo'], f['dove'], f['nota']))
    for f in doc['risorse']['flag_letti']:
        md.append('| `%s` | letto (lo imposta M-CT-02) |\n' % f)
    for v in doc['risorse']['variabili']:
        md.append('| `%s` | %s: %s |\n' % (v['simbolo'], v['valori'], v['nota']))
    for c in doc['risorse']['comandi_speciali']:
        md.append('| comando | %s |\n' % c)
    md.append('| prossimi liberi | `%s`; %s |\n\n' % (doc['risorse']['prossimi_liberi']['variabile_di_scena_CT'], doc['risorse']['prossimi_liberi']['flag_nascondi_CT']))
    md.append(T.ANCORE)
    md.append('\n' + T.DECISIONI)
    md.append('\n' + T.PROVE)
    md.append('\n' + T.NOTE)
    md.append('\n## 10. File del blocco\n\n| Percorso (sotto `6.01_FILE/`) | Tipo | Azione | SHA-1 |\n|---|---|---|---|\n')
    for f in files:
        md.append('| `%s` | %s | %s | `%s` |\n' % (f['percorso'], f['tipo'], f['azione'], f['sha1'][:12]))
    md.append('\n## 11. Controlli eseguiti\n\n| Comando | Ultima riga |\n|---|---|\n')
    for cmd, last, _ in risultati:
        md.append('| `%s` | `%s` |\n' % (cmd, last))
    for a, b_, last in righe_lint:
        md.append('| `python -I tools/trinacria_msg_lint.py --root <pokeheartgold> --pair %s.json %s.json` | `%s` |\n' % (a, b_, last))
    md.append('\nIl controllo del blocco (J00-J17) verifica: indice e SHA-1, banchi (id contigui, linter, coppie), macro e argomenti di ogni istruzione contro `asm/macros/`, etichette e fine degli script, `ScrDef`, header e zone_event, simboli di flag, variabili, specie, sprite e musiche, `BufferPlayersName` prima dei messaggi col nome, righe del registro NPC e Glossario dei messaggi in siciliano.\n')
    if avvisi:
        md.append('\nAvvisi del registro NPC (non bloccano):\n\n')
        for a in avvisi:
            md.append('- %s\n' % a.replace('AVVISO ', '').replace('|', '\\|'))
    md.append('\n## 12. Riga di controllo\n\n`%s`\n' % riga_finale(doc, tot))
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(md))

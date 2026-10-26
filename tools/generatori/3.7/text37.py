import json


def TESTI(c, mosse, agg, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    blocco = {
        'modulo': 3,
        'blocco': '3.7',
        'titolo': 'Mosse da #121 a #240',
        'versione': '1.0',
        'data': '26/10/2026',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.7_MOSSE_121-240.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.8–3.13, 6.x (squadre, insegnanti di mosse, dialoghi) e 7.x '
                   '(applicazione nel repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/moves.h (simboli), '
            'files/msgdata/msg/msg_0749.json (descrizioni), msg_0750.json (nomi), msg_0751.json (maiuscolo), '
            'files/poketool/waza/waza_tbl.narc (dati: 16 byte per mossa con effetto, classe, potenza, tipo, precisione, '
            'PP, probabilità dell’effetto, bersaglio, priorità), files/graphic/font/font_00000000.bin e '
            'tools/msgenc/charmap.txt (larghezze e caratteri).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.1: L-08, D-02, R-GRA, R-NOM, R-GLO e le 15 mosse del Glossario '
            '(3 in questo intervallo).',
            'docs/MODULO_3/3.6_MOSSE_1-120.json v1.1: regole R-MOS-01…08, che valgono anche qui, e i 108 nomi del 3.6 '
            '(nessuno si ripete).',
            'docs/MODULO_3/3.1–3.5: «glossario_aggiunte» delle 493 specie (i nomi delle mosse non le ripetono).',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (625 lemmi, versione 2.0.0): attestazione delle forme '
            '(campo «lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.6 (R-03, R-10, M-SR-02, M-CL-01, M-EN-04, S-RG-01): mosse citate '
            'col nome italiano ufficiale e usi fuori dalla lotta.',
        ],
        'come_si_usa': [
            'Ogni voce di «mosse» dà il nome (msg_0750), il maiuscolo per le parole rapide (msg_0751) e la descrizione '
            '(msg_0749) della mossa con lo stesso indice: l’esecutore copia i tre campi di «banchi» nei tre banchi, '
            'all’indice «n» (Modulo 7).',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G37-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02) e valgono per i testi del Modulo 6.',
            'Il campo «dati» riporta i dati di HeartGold (tipo, classe, potenza, precisione, PP, effetto, priorità): '
            'serve a chi sceglie le mosse delle squadre nel Modulo 6 e non si modifica.',
            'Controllo: python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
            'docs/MODULO_3/3.7_MOSSE_121-240.json --repo F:/Progetti/pokeheartgold → MOSSE_OK; poi '
            'python -I tools/trinacria_glossary_check.py glossary docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json '
            'docs/MODULO_3/3.1_POKEMON_1-100.json … docs/MODULO_3/3.7_MOSSE_121-240.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.7/gen37.py (contenuti in content37.py, parti fisse in '
            'text37.py), copia di tools/generatori/3.6/: python -I tools/generatori/3.7/gen37.py lo riscrive. Il 3.8 '
            'parte da una copia di questa cartella.',
        ],
        'regole': {
            'R-MOS-01…08': 'Valgono come le scrive il blocco 3.6 v1.1 (nomi, nomi della trama, descrizioni D-02, usi '
                           'fuori dalla lotta, collisioni, famiglie di nomi, fonte, banchi). Le voci che seguono dicono '
                           'solo come si applicano a questo intervallo e cosa cambia.',
            'R-MOS-01': 'In questo intervallo si ricopiano 3 mosse del Glossario 3.0: Ciumara (127, MN 7), Cuntrora (156) '
                        'e RinaDiL’Etna (201). I nomi siciliani più lunghi hanno 12 lettere (Panzatammuru, Forzasigreta): '
                        'il maiuscolo di msg_0751 misura %d px al massimo (L-08, 72 px).' % c['maxup'],
            'R-MOS-02': 'Aggiornata dal 3.7: le mosse che la trama cita in italiano sono 17, non 16. Il 3.6 non aveva '
                        'contato Flash (148), che la trama cita in S-RG-01 («il fotografo e il suo Smeargle/Flash») e '
                        'che per R-NOM-01 tiene il nome italiano ufficiale. Il 3.6 v1.1 e lo strumento '
                        '(TRAMA_IT, codice M10) sono allineati. In questo intervallo: Smog (123), Covauova (135), Flash '
                        '(148), Frana (157), Sostituto (164), Rintoccasana (215), Malcomune (220), Staffetta (226). '
                        'Twister (239) non è «Turbine»: si chiama Dracunara.',
            'R-MOS-04': 'Usi fuori dalla lotta in questo intervallo: Ciumara risale le cascate (MN 7; trama R-03, la '
                        'Cascata delle Due Rocche a Corleone), Covauova e Vivilatti (Milk Drink) cedono PS a un compagno, '
                        'Flash illumina le grotte buie, Zàgara (Sweet Scent) attira i Pokémon selvatici. Sono gli usi '
                        'del motore di HeartGold (src/field_move.c; Covauova e Vivilatti dal menu della squadra): la descrizione li dice e non ne aggiunge altri.',
            'R-MOS-05': 'Sei forme naturali erano già nomi di specie e sono state sostituite: Sucasangu (n. 169) → '
                        'Zinzulata (141), Vasuni (n. 238) → Vasazza (142), Zannuni (n. 365) → Zannazza (162), Rèpitu '
                        '(n. 200) → Trivulu (195), Strina (n. 175) → Rialu (217), Virdura (n. 470) → Fogghiasuli (235). '
                        'Restano distinte le forme vicine a una specie: Ovubumma, Bummata e Murcabumma dalla specie '
                        'Bumma (n. 100), Dispettu da Spettu (n. 274), Ammucciuni da Ammucciatu (n. 302), Scippu da '
                        'Scippaturi (n. 461), Malataliata da Taliatura (n. 405). Iron Tail si chiama Cudaferru e non '
                        '«Cudazzaru», che si leggerebbe come la specie Cudazza (n. 8).',
            'R-MOS-06': 'Famiglie di nomi di questo intervallo: pugni Stunapugnu (146), Lestupugnu (183), Scassapugnu '
                        '(223); calci Autucauciu (136) e Tricauci (167); ossa Ossumazza (125), Ossuturnu (155), '
                        'Ossucorpi (198); baci Vasazza (142) e Vasatedda (186); Canciu e Canciu2 (160, 176, come '
                        'Conversione e Conversione2); Murca e Murcabumma (124, 188); Zannata e Zannazza (158, 162); '
                        'ferro Alaferru, Cudaferru, Granfaferru (211, 231, 232); Sucatuna (202) con Sucatedda e Sucata '
                        '(71, 72); Ballacqua (240) con Ballaspati e Ballaciuri; Rotafocu (172) con Rotacauciu (27); '
                        'Dracuciatu (225) e Dracunara (239) con Dracuraggia (82); Amuri e Siddiu (216, 218); Riparu e '
                        'Addunata (182, 197, stesso effetto); Agghiurnata, Fogghiasuli, Chiaruluna (234–236, la stessa '
                        'descrizione come in HeartGold).',
            'R-MOS-07': 'Fonte (R-GLO-03). «MCP» solo quando il nome è lemma o variante del dizionario: %s (%d). '
                        'Vasatedda è una variante di «vasa», Firriata di «firriari», Agghiurnata di «agghiurnari», '
                        'Zàgara di «zagara». I nomi derivati da una voce del dizionario (Ncagghiata da ncagghiari, '
                        'Assicutata da assicutari, Allisciata da allisciari, Sbafantata da sbafanti, Scutulata da '
                        'scutulari, Siddiu da siddiari…) sono «architetto» e la «nota» dice da dove vengono.'
                        % (', '.join(mcp), len(mcp)),
            'R-MOS-09': 'Nuova. Nelle descrizioni i tipi e le parole del gioco hanno il nome italiano ufficiale, come le '
                        'statistiche di R-MOS-03: Spettro (Jastima 174, Smascarata 193), Roccia, Terra e Acciaio '
                        '(RinaDiL’Etna 201), Acqua (Ballacqua 240), Allenatore (Amuri 216, Siddiu 218). Se il 3.13 '
                        'rinomina un tipo, deve dare anche queste descrizioni riscritte.',
            'R-MOS-10': 'Nuova. Quando una descrizione nomina un’altra mossa, usa il nome di Trinacria (quello di '
                        'msg_0750): Firriata (229) libera da Lazzu (20), Nfasciata (35), Sanguetta (73) e Chiova (191). '
                        'Se quel nome cambia, cambia anche la descrizione.',
        },
        'mosse': mosse,
        'glossario_aggiunte': agg,
        'note_per_blocchi_successivi': [
            '3.8 (241–360): Glossario 3.0 da ricopiare: Martiddata (249), Garòfalu (250), Curtigghiu (269), Sorbacqua '
            '(330). Nomi della trama (R-MOS-02): Giorno di Sole (241), Bruciapelo (252), Aromaterapia (312). «GIORNO DI '
            'SOLE» misura 80 px in maiuscolo e sfora L-08: il 3.8 lo risolve con una deviazione registrata (R-NOM-03), '
            'come dicono le note del 3.6.',
            '3.8–3.9, famiglie (R-MOS-06): Focus Punch (264), Shadow Punch (325), '
            'Drain Punch (409), Bullet Punch (418) con «pugnu» dove il nome inglese ha Punch; Blaze Kick (299) con '
            '«cauciu»; Iron Defense (334) e Iron Head (442) con «ferru»; Gunk Shot (441) con «murca»; Dragon Claw (337), '
            'Dragon Dance (349), Dragon Pulse (406), Dragon Rush (407) con «dracu»; Leaf Blade (348) e Leaf Storm (437) '
            'con «fogghia».',
            '3.9 (361–467): Glossario 3.0: Acchianata (431). Nome della trama: Ventoincoda (366). Controllo con '
            '--completo (M09).',
            '3.13: oltre alle statistiche di R-MOS-03, le descrizioni del 3.7 usano i tipi Spettro, Roccia, Terra, '
            'Acciaio, Acqua e la parola «Allenatore» (R-MOS-09).',
            'Modulo 6: Flash (148) è la mossa dello Smeargle del fotografo in S-RG-01; Covauova e Rintoccasana sono '
            'le mosse di cura accaparrate dalle cliniche (R-10); Staffetta, Sostituto e Malcomune sono la squadra del '
            'politico di M-EN-04. Nei messaggi in siciliano le mosse si nominano con la forma del Glossario (R-GLO-05).',
            'Modulo 7: applicazione dei tre banchi per indice, come per il 3.6; poi trinacria_glossary_check.py names '
            '--applied → NAMES_OK e trinacria_moves_check.py check … --repo . → MOSSE_OK.',
        ],
        'strumento': {
            'file': 'tools/trinacria_moves_check.py (nel repository: tools/trinacria/trinacria_moves_check.py, Modulo 7.2)',
            'novita': 'TRAMA_IT ha 17 mosse: aggiunta Flash (148) per R-MOS-02. Nessun codice nuovo; il collaudo '
                      'controlla insieme i blocchi 3.6 e 3.7.',
            'comandi': {
                'collaudo': 'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'controllo': 'python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
                             'docs/MODULO_3/3.7_MOSSE_121-240.json [blocchi 3.8–3.9] [--repo <pokeheartgold>] '
                             '[--completo] → MOSSE_OK',
            },
        },
        'controllo': {
            'mosse': c['mosse'],
            'nomi_dal_glossario_3_0': c['g30'],
            'nomi_italiani_della_trama': c['it'],
            'nomi_nuovi': c['nuovi'],
            'nomi_nuovi_per_fonte': {'MCP': c['mcp'], 'architetto': c['arch']},
            'descrizioni': c['mosse'],
            'righe_delle_descrizioni': c['righe'],
            'descrizioni_per_righe': {'5': c['r5'], 'meno di 5': c['r4']},
            'riga_piu_larga_px': c['maxpx'],
            'maiuscolo_piu_largo_px': c['maxup'],
            'collisioni_con_le_specie_risolte': 6,
            'verifiche_superate': [
                'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'python -I tools/trinacria_moves_check.py check 3.6 + 3.7 --repo F:/Progetti/pokeheartgold → MOSSE_OK',
                'python -I tools/trinacria_glossary_check.py glossary 3.0 + 3.1–3.5 + 3.6 + 3.7 --repo '
                'F:/Progetti/pokeheartgold → GLOSSARY_OK',
                'python -I tools/trinacria_glossary_check.py --selftest → SELFTEST_OK',
            ],
        },
        'riga_finale': ('BLOCCO COMPLETO: 3.7 — 120 mosse (%d nomi nuovi: MCP %d, architetto %d; %d dal Glossario 3.0; '
                        '%d nomi italiani della trama, con Flash aggiunta a R-MOS-02), 120 descrizioni D-02 (%d righe, '
                        'la più larga %d px), maiuscoli entro 72 px, dati di waza_tbl ricopiati; 3.6 v1.1 e strumento '
                        'allineati (17 mosse della trama)'
                        % (c['nuovi'], c['mcp'], c['arch'], c['g30'], c['it'], c['righe'], c['maxpx'])),
    }
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(blocco['riga_finale'])

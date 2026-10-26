import json


def TESTI(c, mosse, agg, dev, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    blocco = {
        'modulo': 3,
        'blocco': '3.8',
        'titolo': 'Mosse da #241 a #360',
        'versione': '1.0',
        'data': '26/10/2026',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.8_MOSSE_241-360.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.9–3.13, 6.x (squadre, insegnanti di mosse, dialoghi) e 7.x '
                   '(applicazione nel repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/moves.h (simboli), '
            'files/msgdata/msg/msg_0749.json (descrizioni), msg_0750.json (nomi), msg_0751.json (maiuscolo), '
            'files/poketool/waza/waza_tbl.narc (dati: 16 byte per mossa con effetto, classe, potenza, tipo, precisione, '
            'PP, probabilità dell’effetto, bersaglio, priorità), files/graphic/font/font_00000000.bin e '
            'tools/msgenc/charmap.txt (larghezze e caratteri), src/party_menu.c (sFieldMoves, mosse usabili fuori '
            'dalla lotta) e src/item.c (sTMHMMoves, MN 05 = Whirlpool, MN 06 = Rock Smash).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.1: L-08, D-02, R-GRA, R-NOM (R-NOM-03 per la deviazione D-19), '
            'R-GLO, le 15 mosse del Glossario (4 in questo intervallo) e le deviazioni D-01…D-18.',
            'docs/MODULO_3/3.6_MOSSE_1-120.json v1.2 e docs/MODULO_3/3.7_MOSSE_121-240.json v1.0: regole R-MOS-01…10, '
            'che valgono anche qui, e i 217 nomi siciliani nuovi dei due blocchi (nessuno si ripete).',
            'docs/MODULO_3/3.1–3.5: «glossario_aggiunte» delle 493 specie (i nomi delle mosse non le ripetono; i numeri '
            'delle specie citati nelle note vengono da lì).',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (625 lemmi, versione 2.0.0): attestazione delle forme '
            '(campo «lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.7 (R-03, R-10, E-SR-01, M-EN-06): mosse citate col nome italiano '
            'ufficiale e usi fuori dalla lotta.',
        ],
        'come_si_usa': [
            'Ogni voce di «mosse» dà il nome (msg_0750), il maiuscolo per le parole rapide (msg_0751) e la descrizione '
            '(msg_0749) della mossa con lo stesso indice: l’esecutore copia i tre campi di «banchi» nei tre banchi, '
            'all’indice «n» (Modulo 7).',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G38-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02) e valgono per i testi del Modulo 6.',
            'La sezione «deviazioni_dalle_specifiche» continua la numerazione del blocco 3.0 (D-19): vale come le '
            'deviazioni D-01…D-18, cioè la forma bloccata sostituisce quella della specifica in ogni testo.',
            'Il campo «dati» riporta i dati di HeartGold (tipo, classe, potenza, precisione, PP, effetto, priorità): '
            'serve a chi sceglie le mosse delle squadre nel Modulo 6 e non si modifica.',
            'Controllo: python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
            'docs/MODULO_3/3.7_MOSSE_121-240.json docs/MODULO_3/3.8_MOSSE_241-360.json --repo F:/Progetti/pokeheartgold '
            '→ MOSSE_OK; poi python -I tools/trinacria_glossary_check.py glossary docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json '
            'docs/MODULO_3/3.1_POKEMON_1-100.json … docs/MODULO_3/3.8_MOSSE_241-360.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.8/gen38.py (contenuti e deviazione in content38.py, parti fisse '
            'in text38.py), copia di tools/generatori/3.7/: python -I tools/generatori/3.8/gen38.py lo riscrive. Il 3.9 '
            'parte da una copia di questa cartella.',
        ],
        'regole': {
            'R-MOS-01…10': 'Valgono come le scrivono i blocchi 3.6 v1.2 (R-MOS-01…08) e 3.7 (R-MOS-09, R-MOS-10). Le '
                           'voci che seguono dicono solo come si applicano a questo intervallo e cosa cambia.',
            'R-MOS-01': 'In questo intervallo si ricopiano 4 mosse del Glossario 3.0: Martiddata (249), Garòfalu (250), '
                        'Curtigghiu (269) e Sorbacqua (330). I nomi siciliani più lunghi hanno 12 lettere (Negghiabadda, '
                        'Ballambriacu, Chiantufintu, Tagghiaventu, Ventuargentu, Tronuscuntru, Fogghiaspata): il '
                        'maiuscolo di msg_0751 misura %d px al massimo (L-08, 72 px).' % c['maxup'],
            'R-MOS-02': 'Nomi della trama in questo intervallo: Giornodisole (241), Bruciapelo (252), Aromaterapia (312). '
                        'La trama scriveva «Giorno di Sole»: il nome resta quello italiano ufficiale, ma nella grafia '
                        'attaccata di HeartGold e SoulSilver, per la deviazione D-19 (R-MOS-11). TRAMA_IT dello '
                        'strumento (codice M10) e l’elenco del 3.6 v1.2 sono allineati.',
            'R-MOS-04': 'Usi fuori dalla lotta in questo intervallo: Martiddata frantuma le rocce incrinate e Garòfalu '
                        'attraversa i vortici (src/party_menu.c, sFieldMoves). Nessun’altra mossa di questo intervallo '
                        'ha un uso sul campo in HeartGold (Dive e Secret Power no): le descrizioni non ne aggiungono. '
                        'I blocchi di calcestruzzo dei clan (trama M-SR-01, D-SR-01, M-CL-01) sono rocce di Martiddata '
                        'nel Modulo 6; la descrizione dice solo l’uso del motore.',
            'R-MOS-05': 'Tre forme naturali erano già nomi di specie e sono state sostituite: Mbrugghiu (n. %d) → '
                        'Trucchettu (271), Ncarzaratu (n. %d) → Catinazzu (286), Sintimentu (n. %d) → Sestusensu (326). '
                        'Restano distinte le forme vicine a una specie, che la «nota» segnala: Specchiata (Specchiu), '
                        'Prufizzia (Prufeta), Sciroccata (Scirocco), Lagnusìa (Lagnusu, Lagnusazzu), Scantu (Scantazzu), '
                        'Tempubadda (Tempu), Lannata (Lanna), Simenzata (Simenza), Fulmineddu (Furmini), Ciriveddata '
                        '(Ciriveddu), Strummulata (Strummula). Blaze Kick si chiama Focucauciu e non «Vampacauciu», che '
                        'si leggerebbe come la specie Vampa.' % (c['spec']['Mbrugghiu'], c['spec']['Ncarzaratu'],
                                                               c['spec']['Sintimentu']),
            'R-MOS-06': 'Famiglie di nomi di questo intervallo: pugni Mirapugnu (264), Stiddapugnu (309), Ummirapugnu '
                        '(325), Muntapugnu (327, Sky Uppercut); calci Focucauciu (299, come Focupugnu); ferro Pelliferru '
                        '(334); draghi Dracugranfa (337) e Dracuballu (349); foglie Fogghiamaga (345) e Fogghiaspata '
                        '(348); balli Ballapinni (297) e Ballambriacu (298) con Ballaspati, Ballaciuri e Ballacqua; palle '
                        '«-badda» Ummirabadda (247), Negghiabadda (296), Jacciubadda (301), Tempubadda (311); mosse '
                        'supreme degli starter «-ranni» Focuranni (307), Acquaranni (308), Arburanni (338); fosse '
                        'Fossapetra (317) e Fossarina (328); braccia Vrazzuspini (302) e Vrazzumazza (359); code '
                        'Cudaluci (294) e Cudavilenu (342) con Cudaferru; Sparagnu, Sputazzata, Ammuccata (254–256) '
                        'si citano a vicenda nelle descrizioni (R-MOS-10); Specchiata (243) fa coppia con Vinnitta (68). '
                        'Overheat e Psycho Boost (315, 354), Foresight e Odor Sleuth (193, 316) hanno la stessa '
                        'descrizione come in HeartGold, Miracle Eye (357) la stessa col tipo Buio.',
            'R-MOS-07': 'Fonte (R-GLO-03). «MCP» solo quando il nome è lemma o variante del dizionario: %s (%d). Cursa '
                        'è una variante di «curriri», Sparagnu di «sparagnari» («sparàgnu»), Sciroccata di «sciroccu», '
                        'Lagnusìa di «lagnusu», Scantu di «scantazzu». I nomi derivati da una voce del dizionario '
                        '(Alliffata da alliffari, Sbacantata da sbacantari, Arricriata da arricriàrisi, Nzingata da '
                        'nzingari, Arruspicata da arruspicari, Strummulata da strùmmulu, Scanciu da scanciari…) sono '
                        '«architetto» e la «nota» dice da dove vengono.' % (', '.join(mcp), len(mcp)),
            'R-MOS-09': 'Tipi e parole del gioco nelle descrizioni di questo intervallo, col nome italiano ufficiale: '
                        'Fuoco (Giornodisole 241, Vagnata 346), Ghiaccio (Grannulata 258), Elettro (Carrica 268, '
                        'Nfangata 300), Spettro (Annasata 316), Buio (Ucchiusantu 357), «lotta in doppio» (Manuzza 270), '
                        '«abilità» (Pupiata 272, Scanciu 285), Levitazione (Pisantizza 356, nome dell’abilità).',
            'R-MOS-10': 'Descrizioni che nominano altre mosse col nome di Trinacria: Sputazzata e Ammuccata (255, 256) '
                        'nominano Sparagnu (254), Rimannata (277) nomina Sanguetta (73), Spaccamuru (280) nomina '
                        'Paraluci e Paracorpi (113, 115).',
            'R-MOS-11': 'Nuova. Quando un nome della trama (R-MOS-02) sfora L-08, si usa la grafia del nome italiano '
                        'ufficiale che entra, o un’altra forma intera, e la scelta si registra nella sezione '
                        '«deviazioni_dalle_specifiche» del blocco, numerata dopo l’ultima deviazione già data (D-19 qui; '
                        'il 3.9 parte da D-20). La mossa resta «lingua» it senza voce nel Glossario; la voce ha il campo '
                        '«deviazione»; nello stesso blocco si allineano la trama, l’elenco di R-MOS-02 del 3.6, '
                        'TRAMA_IT dello strumento e dei generatori, e la scaletta.',
        },
        'deviazioni_dalle_specifiche': dev,
        'mosse': mosse,
        'glossario_aggiunte': agg,
        'note_per_blocchi_successivi': [
            '3.9 (361–467): Glossario 3.0 da ricopiare: Acchianata (431). Nome della trama: Ventoincoda (366: 11 lettere, '
            'maiuscolo 66 px, entra in L-08). Controllo con --completo (M09). Le eventuali deviazioni partono da D-20.',
            '3.9, famiglie (R-MOS-06): Drain Punch (409) e Bullet Punch (418) con «pugnu»; Iron Head (442) con «ferru»; '
            'Gunk Shot (441) con «murca»; Dragon Pulse (406) e Dragon Rush (407) con «dracu»; Leaf Storm (437) con '
            '«fogghia»; le palle (Energy Ball 412, Focus Blast 411, Aura Sphere 396…) possono continuare «-badda».',
            'Blocchi degli strumenti (MN): in HeartGold ITEM_HM05 insegna Whirlpool (Garòfalu) e ITEM_HM06 Rock Smash '
            '(Martiddata) (src/item.c:128–129), mentre le note del Glossario 3.0 chiamano Martiddata «MN 5» e '
            'Garòfalu «MN 6» (ordine della trama, R-03). Questo blocco non tocca le MN: il blocco che nomina le MN '
            'deve decidere se segue i numeri del motore o rinumera, e allineare il Glossario.',
            '3.13: oltre a statistiche e tipi di R-MOS-03 e R-MOS-09, le descrizioni del 3.8 usano i tipi Fuoco, '
            'Ghiaccio, Elettro, Spettro, Buio e il nome dell’abilità Levitazione (Pisantizza, 356).',
            'Modulo 6: Giornodisole e Solarraggio sono le mosse degli specchi ustori di E-SR-01 (nella battuta si '
            'scrive «Giornodisole», D-19); Bruciapelo è la mossa del Gattupardu di Mistretta (M-EN-06, con Pizzu); '
            'Aromaterapia è una delle mosse di cura delle cliniche (R-10); Martiddata apre i blocchi di calcestruzzo '
            '(M-SR-01, D-SR-01, M-CL-01) e Garòfalu i gorghi di Cariddi; Sorbacqua è la mossa del furto idrico negli '
            'Ipogei (M-AG-03).',
            'Modulo 7: applicazione dei tre banchi per indice, come per il 3.6 e il 3.7; poi trinacria_glossary_check.py '
            'names --applied → NAMES_OK e trinacria_moves_check.py check … --repo . → MOSSE_OK.',
        ],
        'strumento': {
            'file': 'tools/trinacria_moves_check.py (nel repository: tools/trinacria/trinacria_moves_check.py, Modulo 7.2)',
            'novita': 'TRAMA_IT: la mossa 241 è «Giornodisole» (deviazione D-19). Nessun codice nuovo; il collaudo '
                      'controlla insieme i blocchi 3.6, 3.7 e 3.8.',
            'comandi': {
                'collaudo': 'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'controllo': 'python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
                             'docs/MODULO_3/3.7_MOSSE_121-240.json docs/MODULO_3/3.8_MOSSE_241-360.json [blocco 3.9] '
                             '[--repo <pokeheartgold>] [--completo] → MOSSE_OK',
            },
        },
        'controllo': {
            'mosse': c['mosse'],
            'nomi_dal_glossario_3_0': c['g30'],
            'nomi_italiani_della_trama': c['it'],
            'deviazioni': [d['id'] for d in dev],
            'nomi_nuovi': c['nuovi'],
            'nomi_nuovi_per_fonte': {'MCP': c['mcp'], 'architetto': c['arch']},
            'descrizioni': c['mosse'],
            'righe_delle_descrizioni': c['righe'],
            'descrizioni_per_righe': {'5': c['r5'], 'meno di 5': c['r4']},
            'riga_piu_larga_px': c['maxpx'],
            'maiuscolo_piu_largo_px': c['maxup'],
            'collisioni_con_le_specie_risolte': 3,
            'verifiche_superate': [
                'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'python -I tools/trinacria_moves_check.py check 3.6 + 3.7 + 3.8 --repo F:/Progetti/pokeheartgold → MOSSE_OK',
                'python -I tools/trinacria_glossary_check.py glossary 3.0 + 3.1–3.5 + 3.6 + 3.7 + 3.8 --repo '
                'F:/Progetti/pokeheartgold → GLOSSARY_OK',
                'python -I tools/trinacria_glossary_check.py --selftest → SELFTEST_OK',
            ],
        },
        'riga_finale': ('BLOCCO COMPLETO: 3.8 — 120 mosse (%d nomi nuovi: MCP %d, architetto %d; %d dal Glossario 3.0; '
                        '%d nomi italiani della trama), 120 descrizioni D-02 (%d righe, la più larga %d px), maiuscoli '
                        'entro 72 px, dati di waza_tbl ricopiati; deviazione D-19 «Giorno di Sole» → «Giornodisole» '
                        '(maiuscolo da 80 a 72 px) con trama v1.7, 3.6 v1.2 e strumento allineati'
                        % (c['nuovi'], c['mcp'], c['arch'], c['g30'], c['it'], c['righe'], c['maxpx'])),
    }
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(blocco['riga_finale'])

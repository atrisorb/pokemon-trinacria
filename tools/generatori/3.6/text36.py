import json


def TESTI(c, mosse, agg, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    blocco = {
        'modulo': 3,
        'blocco': '3.6',
        'titolo': 'Mosse da #1 a #120',
        'versione': '1.2',
        'data': '26/10/2026',
        'novita_1_2': 'Nell’elenco di R-MOS-02 la mossa 241 si chiama «Giornodisole», grafia attaccata del nome italiano '
                      'ufficiale: «Giorno di Sole» sforava L-08 in maiuscolo (80 px), deviazione D-19 del blocco 3.8. '
                      'Le 120 voci di questo blocco non cambiano.',
        'novita_1_1': 'R-MOS-02 conta 17 mosse della trama: aggiunta Flash (148), citata in S-RG-01 e trovata dal blocco 3.7. '
                      'Le 120 voci di questo blocco non cambiano.',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.6_MOSSE_1-120.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.7–3.13, 6.x (squadre, insegnanti di mosse, dialoghi) e 7.x '
                   '(applicazione nel repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/moves.h (simboli), '
            'files/msgdata/msg/msg_0749.json (descrizioni), msg_0750.json (nomi), msg_0751.json (maiuscolo), '
            'files/poketool/waza/waza_tbl.narc (dati: 16 byte per mossa con effetto, classe, potenza, tipo, precisione, '
            'PP, probabilità dell’effetto, bersaglio, priorità), files/graphic/font/font_00000000.bin e '
            'tools/msgenc/charmap.txt (larghezze e caratteri), files/msgdata/msg/msg_0802.json (forme alternative, per il 3.13).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.1: L-08, D-02, R-GRA, R-NOM, R-GLO e le 15 mosse del Glossario '
            '(7 in questo intervallo).',
            'docs/MODULO_3/3.1–3.5: «glossario_aggiunte» delle 493 specie (i nomi delle mosse non le ripetono).',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (625 lemmi, versione 2.0.0): attestazione delle forme '
            '(campo «lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.6 (R-03, R-10.3, R-10.7, M-SR, M-AG, M-TP, E-SR-01): mosse citate '
            'col nome italiano ufficiale e usi fuori dalla lotta.',
        ],
        'come_si_usa': [
            'Ogni voce di «mosse» dà il nome (msg_0750), il maiuscolo per le parole rapide (msg_0751) e la descrizione '
            '(msg_0749) della mossa con lo stesso indice: l’esecutore copia i tre campi di «banchi» nei tre banchi, '
            'all’indice «n» (Modulo 7).',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G36-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02) e valgono per i testi del Modulo 6.',
            'Il campo «dati» riporta i dati di HeartGold (tipo, classe, potenza, precisione, PP, effetto, priorità): '
            'serve a chi sceglie le mosse delle squadre nel Modulo 6 e non si modifica.',
            'Controllo: python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
            '--repo F:/Progetti/pokeheartgold → MOSSE_OK; poi python -I tools/trinacria_glossary_check.py glossary '
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json docs/MODULO_3/3.1_POKEMON_1-100.json … '
            'docs/MODULO_3/3.6_MOSSE_1-120.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.6/gen36.py (contenuti in content36.py, parti fisse in '
            'text36.py): python -I tools/generatori/3.6/gen36.py lo riscrive. I blocchi 3.7–3.9 partono da una copia '
            'di questa cartella (regola dei generatori nella scaletta).',
        ],
        'regole': {
            'R-MOS-01': 'Nomi. Ogni mossa ha un nome siciliano del Glossario (specifica PLOT §5: «le 467 Mosse»), tranne '
                        'quelle che la trama cita col nome italiano ufficiale (R-MOS-02). Le 15 mosse del Glossario 3.0 '
                        'si ricopiano: in questo intervallo Pizzu (6), Roncigghiu (15), Passaggiu (19), Aliscafu (57), '
                        'Scoppola (63), Spallata (70), Scussuni (89). Le altre entrano nella «glossario_aggiunte» del '
                        'blocco della mossa. Limite L-08: 15 caratteri e 72 px, e anche il maiuscolo di msg_0751 entro '
                        '72 px: con le maiuscole tutte da 6 px un nome senza spazi ha al massimo 12 lettere (qui il più '
                        'largo è Tagghiatesta, 72 px in maiuscolo).',
            'R-MOS-02': 'Nomi della trama. Le mosse che la trama cita in italiano tengono il nome italiano ufficiale '
                        '(R-NOM-01, nota del 3.0 per i blocchi 3.6–3.9), con «lingua» it, «glossario» null e nessuna '
                        'voce nel Glossario. Elenco completo, 17 mosse (lo strumento lo controlla come M10): Turbine (18), '
                        'Bottintesta (29), Idropompa (56), Solarraggio (76), Nube (114), Smog (123), Covauova (135), '
                        'Flash (148, S-RG-01: il fotografo col suo Smeargle; aggiunta dal 3.7), Frana (157), Sostituto (164), Rintoccasana (215), Malcomune (220), Staffetta (226), Giornodisole '
                        '(241; la trama scriveva «Giorno di Sole», deviazione D-19 del blocco 3.8), Bruciapelo (252), Aromaterapia (312), Ventoincoda (366). «Turbine» è Whirlwind (18), '
                        'non Twister (239, «Tornado»): nella trama la usano Pidgeot e Fearow contro le pale eoliche. '
                        '«Bottintesta» è entrata nella trama v1.6 (R-10.7, l’insegnante dei Monti Rossi) dopo la nota '
                        'del 3.0 e segue la stessa regola. Nessun’altra mossa tiene il nome italiano.',
            'R-MOS-03': 'Descrizioni (msg_0749, profilo D-02). In italiano, come le voci dell’Atlante (R-SPE-05): sono '
                        'testi di sistema che in lotta devono dire con esattezza cosa fa la mossa, quindi seguono il '
                        'campo «dati» e non aggiungono ambientazione. Al massimo 5 righe, ognuna entro 23 caratteri e '
                        '120 px (membro 0 del font); nel banco come HeartGold: con 5 righe l’ultima non ha «\\n» (359 '
                        'voci di HeartGold), con meno righe ce l’hanno tutte (104 voci). Nomi fissi dentro le '
                        'descrizioni, quelli italiani ufficiali: PS, Attacco, Difesa, Attacco Speciale, Difesa '
                        'Speciale, Velocità, precisione, elusione, «brutto colpo» (colpo critico), «tentennare», '
                        'scottare, congelare, paralizzare, avvelenare, addormentare, confondere, KO, Centro Pokémon.',
            'R-MOS-04': 'Usi fuori dalla lotta. Le descrizioni delle mosse con un uso sul campo dicono l’uso di '
                        'Trinacria (trama R-03): Roncigghiu recide i rovi, Passaggiu porta in una città già visitata, '
                        'Aliscafu naviga sull’acqua, Spallata sposta i massi, Pirtusu (Dig) fa uscire dalle grotte, '
                        'Squagghiata (Teleport) riporta all’ultimo Centro Pokémon, Bottintesta trova Pokémon negli '
                        'alberi. I messaggi del campo (Passaggiu bloccato nell’area etnea da FLAG_ETNA_ASH_ACTIVE) sono '
                        'del Modulo 6.',
            'R-MOS-05': 'Collisioni. Nessun nome di mossa coincide con un nome di specie, strumento, classe, abilità, '
                        'tipo, natura, Dossier o soprannome (R-NOM-02, codici G03 e M07). Nove forme naturali erano già '
                        'nomi di specie e sono state sostituite: Tinagghia (n. 127) → Strinciuta (11), Vrascia (n. 5) → '
                        'Carbunedda (52), Sbruffu (n. 223) → Jittacqua (55), Pruvulazzu (n. 449) → Cinnirazza (77), '
                        'Faidda (n. 172) e Scintidda (n. 4) → Lampu (84), Saitta (n. 26) → Fulminata (85), Specchiu '
                        '(n. 436) → Paracorpi (115), Pacenzia (n. 202) → Agghiuttuta (117). Le forme vicine a un nome '
                        'di specie restano distinte (Spingulata e la specie Spingula, Lampu e Lampuzzu, Tronu e '
                        'Pinnatronu).',
            'R-MOS-06': 'Famiglie di nomi. Le mosse in coppia o in serie hanno nomi della stessa forma, perché il '
                        'giocatore le riconosca: Focupugnu, Jacciupugnu, Tronupugnu (7–9, come Fuocopugno e i suoi '
                        'fratelli); Pugniceddi e Pugnuni (4, 5); Duicauci, Cauciuni, Sautacauciu, Rotacauciu (24–27); '
                        'Ballaspati e Ballaciuri (14, 80); Sucatedda e Sucata (71, 72); Paraluci e Paracorpi (113, 115); '
                        'Punciuta e Duipunciuti (40, 41). I pugni e i calci dei blocchi successivi (Hi Jump Kick 136, '
                        'Mach Punch 183, DynamicPunch 223, Focus Punch 264, Blaze Kick 299…) usano «pugnu» e «cauciu».',
            'R-MOS-07': 'Fonte (R-GLO-03). «MCP» solo quando il nome è lemma o variante del dizionario: %s (%d). '
                        'I nomi derivati da un verbo del dizionario (Arrimazzata da arrimazzari, Alluccata da alluccari, '
                        'Squagghiata da squagghiari, Scattata da scattari…) sono «architetto» e la «nota» dice da dove '
                        'vengono. Zotta vale «frusta» (Vine Whip): il senso di «sberla» del dizionario non si usa per '
                        'la mossa.' % (', '.join(mcp), len(mcp)),
            'R-MOS-08': 'Banchi (R-NOM-08). msg_0750, msg_0751 e msg_0749 restano di 468 messaggi; l’indice 0 («-» e '
                        'la descrizione vuota) non cambia. Il maiuscolo di msg_0751 è quello esatto del nome '
                        '(R-GRA-08: Garòfalu → GARÒFALU, RinaDiL’Etna → RINADIL’ETNA). Le parole rapide non sono più in '
                        'ordine alfabetico: accettato (R-NOM-12).',
        },
        'mosse': mosse,
        'glossario_aggiunte': agg,
        'note_per_blocchi_successivi': [
            '3.7 (121–240): Glossario 3.0 da ricopiare: Ciumara (127), Cuntrora (156), RinaDiL’Etna (201). Nomi della '
            'trama (R-MOS-02): Smog (123), Covauova (135), Flash (148), Frana (157), Sostituto (164), Rintoccasana (215), Malcomune '
            '(220), Staffetta (226).',
            '3.8 (241–360): Glossario 3.0: Martiddata (249), Garòfalu (250), Curtigghiu (269), Sorbacqua (330). Nomi '
            'della trama: Giorno di Sole (241), Bruciapelo (252), Aromaterapia (312). Attenzione: «Giorno di Sole» sta '
            'in L-08 (72 px) ma il maiuscolo «GIORNO DI SOLE» misura 80 px e sfora L-08: il 3.8 lo risolve con una '
            'deviazione registrata (R-NOM-03), per esempio «GiornoDiSole» (maiuscolo 72 px), e allinea la trama '
            '(E-SR-01) e la tabella TRAMA_IT dello strumento.',
            '3.9 (361–467): Glossario 3.0: Acchianata (431). Nome della trama: Ventoincoda (366). Il 3.9 chiude le mosse: '
            'il controllo si lancia con --completo (M09: mosse 1–467 una volta sola, nomi tutti diversi) e la riga '
            'finale dà il riepilogo delle 467 mosse.',
            '3.7–3.9: stesse regole R-MOS-01…08; nessun nome riprende un nome di 3.6 (M07 lo segnala già senza '
            '--completo, perché le «glossario_aggiunte» di tutti i blocchi controllati entrano nel confronto).',
            '3.13: nelle descrizioni delle mosse le statistiche e gli stati hanno i nomi italiani ufficiali di R-MOS-03; '
            'se il 3.13 rinomina una statistica o uno stato nei banchi di sistema, deve dare anche le descrizioni delle '
            'mosse da riscrivere. Le forme alternative delle specie sono in msg_0802 (banco dell’interfaccia del '
            'Pokédex, 176 messaggi): mari di Shellos e Gastrodon 116–117, mantelli di Burmy e Wormadam 118–120, forme '
            'di Deoxys 145–148, di Shaymin 149–150, di Giratina 151–152, di Castform 161–165; le nomina il 3.13.',
            'Modulo 6: le squadre e gli insegnanti di mosse usano questi nomi; Bottintesta è l’insegnante dei Monti Rossi '
            '(trama R-10.7); nei messaggi in siciliano le mosse si nominano con la forma del Glossario (R-GLO-05).',
            'Modulo 7: applicazione dei tre banchi per indice; poi trinacria_glossary_check.py names --repo . --glossary '
            '<file del Glossario> --applied → NAMES_OK (N01 limiti, N02 maiuscolo, N03 profilo D-02, N05 nomi '
            'applicati) e trinacria_moves_check.py check … --repo . → MOSSE_OK.',
        ],
        'strumento': {
            'file': 'tools/trinacria_moves_check.py (nel repository: tools/trinacria/trinacria_moves_check.py, Modulo 7.2)',
            'file_di_prova': ['tools/testdata/mosse_prova_ko.json'],
            'comandi': {
                'collaudo': 'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'controllo': 'python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
                             '[blocchi 3.7–3.9] [--repo <pokeheartgold>] [--docs <docs>] [--completo] → MOSSE_OK',
            },
            'codici': {
                'M00': 'file illeggibile o senza «mosse»',
                'M01': 'nome oltre L-08 (caratteri, px, px del maiuscolo) o con caratteri non ammessi (R-GRA-11)',
                'M02': 'maiuscolo diverso dal maiuscolo esatto del nome (R-GRA-08)',
                'M03': 'descrizione fuori dal profilo D-02 (righe, caratteri, px, apostrofi dritti, «\\n» del banco)',
                'M04': 'nome assente dal Glossario o diverso, nome italiano con una voce nel Glossario, lingua non valida',
                'M05': 'mossa ripetuta o fuori da 1–467; con --repo: simbolo diverso da moves.h o «originale» diverso da msg_0750',
                'M06': 'banchi incoerenti coi campi (msg_0750, msg_0751, msg_0749)',
                'M07': 'nome uguale a un altro nome di sistema o a un soprannome (R-MOS-05)',
                'M08': 'con --repo: «dati» diversi da waza_tbl.narc',
                'M09': 'con --completo: mosse 1–467 non coperte una volta sola o nome ripetuto tra i blocchi',
                'M10': 'mossa citata dalla trama senza il nome italiano ufficiale, o nome italiano su una mossa che la '
                       'trama non cita (R-MOS-02)',
            },
            'collaudo': {
                'descrizione': 'i blocchi 3.6–3.9 presenti in docs/MODULO_3 non danno errori (con --completo solo quando '
                               'ci sono tutti e quattro); mosse_prova_ko.json, controllato con --completo, produce '
                               'esattamente i codici attesi (M08 solo se il repository è presente).',
                'errori_attesi': ['M01', 'M02', 'M03', 'M04', 'M05', 'M06', 'M07', 'M08', 'M09', 'M10'],
            },
            'novita': 'strumento nuovo del blocco 3.6; trinacria_glossary_check.py e trinacria_dex_check.py non cambiano.',
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
            'collisioni_con_le_specie_risolte': 9,
            'verifiche_superate': [
                'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json --repo F:/Progetti/pokeheartgold → MOSSE_OK',
                'python -I tools/trinacria_glossary_check.py glossary 3.0 + 3.1–3.5 + 3.6 --repo F:/Progetti/pokeheartgold → GLOSSARY_OK',
                'python -I tools/trinacria_glossary_check.py --selftest → SELFTEST_OK',
                'python -I tools/trinacria_dex_check.py --selftest → SELFTEST_OK',
            ],
        },
        'riga_finale': ('BLOCCO COMPLETO: 3.6 — 120 mosse (%d nomi nuovi: MCP %d, architetto %d; %d dal Glossario 3.0; '
                        '%d nomi italiani della trama), 120 descrizioni D-02 (%d righe, la più larga %d px), maiuscoli '
                        'entro 72 px, dati di waza_tbl ricopiati; strumento nuovo trinacria_moves_check.py (M00–M10) '
                        'collaudato' % (c['nuovi'], c['mcp'], c['arch'], c['g30'], c['it'], c['righe'], c['maxpx'])),
    }
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(blocco['riga_finale'])

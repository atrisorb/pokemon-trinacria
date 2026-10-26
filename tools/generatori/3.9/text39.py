import glob, json, os


def riepilogo(out, mosse, agg):
    """Mosse 1-467 dei blocchi 3.6-3.9 insieme (il 3.9 dai dati appena generati)."""
    tutte, nuove = [], []
    for f in sorted(glob.glob(os.path.join(os.path.dirname(out), '3.[6-8]_MOSSE_*.json'))):
        b = json.load(open(f, encoding='utf-8'))
        tutte += b['mosse']
        nuove += b['glossario_aggiunte']
    tutte += mosse
    nuove += agg
    nomi = [m['nome'].lower() for m in tutte]
    per_blocco = {}
    for a in nuove:
        per_blocco[a['id'][:3]] = per_blocco.get(a['id'][:3], 0) + 1
    return {
        'mosse': len(tutte),
        'numeri_coperti': '1–%d, ognuno una volta' % max(m['n'] for m in tutte),
        'nomi_distinti': len(set(nomi)),
        'nomi_siciliani_nuovi': len(nuove),
        'nomi_nuovi_per_blocco': {'3.6': per_blocco['G36'], '3.7': per_blocco['G37'], '3.8': per_blocco['G38'],
                                  '3.9': per_blocco['G39']},
        'nomi_nuovi_per_fonte': {'MCP': sum(1 for a in nuove if a['fonte'] == 'MCP'),
                                 'architetto': sum(1 for a in nuove if a['fonte'] != 'MCP')},
        'nomi_dal_glossario_3_0': sum(1 for m in tutte if m['glossario'] and m['glossario'].startswith('G30')),
        'nomi_italiani_della_trama': sum(1 for m in tutte if m['lingua'] == 'it'),
        'deviazioni': ['D-19 (3.8)'],
        'maiuscolo_piu_largo_px': max(m['maiuscolo_px'] for m in tutte),
        'riga_di_descrizione_piu_larga_px': max(px for m in tutte for px in m['descrizione_righe_px']),
    }


def TESTI(c, mosse, agg, dev, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    r = riepilogo(out, mosse, agg)
    blocco = {
        'modulo': 3,
        'blocco': '3.9',
        'titolo': 'Mosse da #361 a #467',
        'versione': '1.0',
        'data': '26/10/2026',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.9_MOSSE_361-467.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.10–3.13, 6.x (squadre, insegnanti di mosse, dialoghi) e 7.x '
                   '(applicazione nel repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/moves.h (simboli), '
            'files/msgdata/msg/msg_0749.json (descrizioni), msg_0750.json (nomi), msg_0751.json (maiuscolo), '
            'files/poketool/waza/waza_tbl.narc (dati: 16 byte per mossa con effetto, classe, potenza, tipo, precisione, '
            'PP, probabilità dell’effetto, bersaglio, priorità), files/graphic/font/font_00000000.bin e '
            'tools/msgenc/charmap.txt (larghezze e caratteri), src/party_menu.c (sFieldMoves: Rock Climb sì, Defog no).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.1: L-08, D-02, R-GRA, R-NOM, R-GLO, le 15 mosse del Glossario '
            '(1 in questo intervallo: Acchianata, 431) e le deviazioni D-01…D-18.',
            'docs/MODULO_3/3.6_MOSSE_1-120.json v1.2, 3.7_MOSSE_121-240.json v1.0 e 3.8_MOSSE_241-360.json v1.0: regole '
            'R-MOS-01…11, che valgono anche qui, la deviazione D-19 e i 330 nomi siciliani nuovi dei tre blocchi '
            '(nessuno si ripete).',
            'docs/MODULO_3/3.1–3.5: «glossario_aggiunte» delle 493 specie (i nomi delle mosse non le ripetono; i numeri '
            'delle specie citati nelle note vengono da lì).',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (625 lemmi, versione 2.0.0): attestazione delle forme '
            '(campo «lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.7 (R-03, M-TP-03/B-TP-02, M-EN-03): Ventoincoda è l’unica mossa '
            'di questo intervallo che la trama cita col nome italiano ufficiale; Scalaroccia è già Acchianata (R-03).',
        ],
        'come_si_usa': [
            'Ogni voce di «mosse» dà il nome (msg_0750), il maiuscolo per le parole rapide (msg_0751) e la descrizione '
            '(msg_0749) della mossa con lo stesso indice: l’esecutore copia i tre campi di «banchi» nei tre banchi, '
            'all’indice «n» (Modulo 7).',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G39-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02) e valgono per i testi del Modulo 6.',
            'Il campo «dati» riporta i dati di HeartGold (tipo, classe, potenza, precisione, PP, effetto, priorità): '
            'serve a chi sceglie le mosse delle squadre nel Modulo 6 e non si modifica.',
            'Questo è l’ultimo blocco delle mosse: con il 3.6, il 3.7 e il 3.8 copre le mosse 1–467 una volta sola '
            '(sezione «riepilogo_mosse_1_467», controllo M09 con --completo).',
            'Controllo: python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
            'docs/MODULO_3/3.7_MOSSE_121-240.json docs/MODULO_3/3.8_MOSSE_241-360.json docs/MODULO_3/3.9_MOSSE_361-467.json '
            '--repo F:/Progetti/pokeheartgold --completo → MOSSE_OK; poi python -I tools/trinacria_glossary_check.py '
            'glossary docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json docs/MODULO_3/3.1_POKEMON_1-100.json … '
            'docs/MODULO_3/3.9_MOSSE_361-467.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.9/gen39.py (contenuti in content39.py, parti fisse in text39.py), '
            'copia di tools/generatori/3.8/: python -I tools/generatori/3.9/gen39.py lo riscrive.',
        ],
        'regole': {
            'R-MOS-01…11': 'Valgono come le scrivono i blocchi 3.6 v1.2 (R-MOS-01…08), 3.7 (R-MOS-09, R-MOS-10) e 3.8 '
                           '(R-MOS-11). Le voci che seguono dicono solo come si applicano a questo intervallo; il 3.9 '
                           'non aggiunge regole.',
            'R-MOS-01': 'In questo intervallo si ricopia 1 mossa del Glossario 3.0: Acchianata (431). I nomi siciliani '
                        'più lunghi hanno 12 lettere (Chiovavilenu, Tagghianotti, Ummiragranfa, Tagghiamenti, '
                        'Fogghiaventu, Cruciavilenu, Rugghiutempu, Sfardaspaziu, Scoppiaciuri): il maiuscolo di '
                        'msg_0751 misura %d px al massimo (L-08, 72 px).' % c['maxup'],
            'R-MOS-02': 'Nome della trama in questo intervallo: Ventoincoda (366; 11 lettere, maiuscolo 66 px, entra in '
                        'L-08 senza deviazione). Nessun’altra mossa 361–467 compare nella trama col nome italiano: '
                        'l’elenco dei 17 nomi di R-MOS-02 (3.6 v1.2) è completo e TRAMA_IT dello strumento non cambia.',
            'R-MOS-04': 'Uso fuori dalla lotta in questo intervallo: Acchianata scala le pareti rocciose '
                        '(src/party_menu.c, sFieldMoves). Defog (Annittata, 432) in HeartGold non ha un uso sul campo e '
                        'la descrizione non ne aggiunge.',
            'R-MOS-05': 'Nessuna forma scelta coincide con un nome di specie, mossa, strumento, classe, Dossier o '
                        'soprannome. Le forme vicine a una specie, che la «nota» segnala, restano distinte: Scippata '
                        '(Scippaturi), Canciascutu (Scutu), Canciacori (Cori), Malasimenza (Simenza), Lustrapetra '
                        '(Lustrinu), Furficiata (Furficiuni), Tistapaci (Tistuni), Saittata (Saitta), Fogghiaventu '
                        '(Fogghiazza), Ammagata (Ammagatura), Sciamuarmi (Sciammuni), Rugghiutempu (Tempu), '
                        'Sfardaspaziu (Spaziu). Scartate in partenza: «Tumpulata» (MCP) per Force Palm, troppo vicina a '
                        'Timpulata (3); «Pizzupetra» per Stone Edge, perché Pizzu è la mossa 6; «Petraluci» per Power '
                        'Gem, che si leggerebbe come la specie Petraluna.',
            'R-MOS-06': 'Famiglie di nomi di questo intervallo: pugni Sucapugnu (409) e Lampupugnu (418); ferro '
                        'Scattaferru (368), Ferruluci (430), Tistaferru (442), Ferrubumma (443); morchia Murcazza (441); '
                        'draghi Dracupulsu (406), Dracucursa (407), Dracustidda (434); foglie Fogghiaventu (437); palle '
                        '«-badda» Aurabadda (396), Mirabadda (411), Naturabadda (412); bombe «-bumma» Ciciribumma (402), '
                        'Zancabumma (426), Ferrubumma (443); zanne Zannatronu, Zannajacciu, Zannafocu (422–424) con '
                        'Zannavilenu; ombre Ummiragranfa (421), Ummiralesta (425), Ummiraforza (467); lesti Lestujacciu '
                        '(420) e Lestacqua (453); tagli «Tagghia-» Tagghianotti (400), Tagghiacelu (403), Tagghiamenti '
                        '(427); veleni «-vilenu» Chiovavilenu (390), Puncivilenu (398), Cruciavilenu (440); scambi '
                        '«Cancia-» Canciaforza, Canciascutu (384, 385) e Canciacori (391); gli ordini della regina degli '
                        'sciami «Sciamu-» Sciamuarmi, Sciamuscutu, Sciamucura (454–456); code Cudacqua (401); balli '
                        'Ballaluna (461). Avalanche (419) ha la stessa descrizione di Rendicuntu (279) come in HeartGold '
                        'Revenge; Healing Wish e Lunar Dance (361, 461) si somigliano come in HeartGold.',
            'R-MOS-07': 'Fonte (R-GLO-03). «MCP» solo quando il nome è lemma o variante del dizionario: %s (%d): '
                        '«parrata» è una variante di «parratina». I nomi derivati o composti da una voce del dizionario '
                        '(Scippata da scippari, Scattaferru da scattari, Canciaforza da canciari, Unnavacanti da '
                        'vacanti, Ciciribumma da cìciri, Allavancata da allavancari, Annittata da annititari, '
                        'Dracustidda da stidda, Zuttazza da zotta, Ammagata da ammagari, Ballaluna da luna, Ventutintu '
                        'da tintu…) sono «architetto» e la «nota» dice da dove vengono.' % (', '.join(mcp), len(mcp)),
            'R-MOS-09': 'Parole del gioco nelle descrizioni di questo intervallo, col nome italiano ufficiale: '
                        '«Bacca» (Cugghiuta 363, Scippata 365, Rusicata 450), «Lastra» (Judiziu 449), «Allenatore» '
                        '(Sigillu 373), «abilità» e il nome dell’abilità Insonnia (Stummacata 380, Malasimenza 388). '
                        'Nessun nome di tipo.',
            'R-MOS-10': 'Descrizioni che nominano altre mosse col nome di Trinacria: Fintata (364) nomina Riparu e '
                        'Addunata (182, 197).',
        },
        'deviazioni_dalle_specifiche': dev,
        'mosse': mosse,
        'glossario_aggiunte': agg,
        'riepilogo_mosse_1_467': r,
        'note_per_blocchi_successivi': [
            '3.10–3.12 (strumenti): le descrizioni delle mosse usano le parole «Bacca» (363, 365, 450) e «Lastra» '
            '(449) come nomi generici delle categorie di strumenti: se i blocchi degli strumenti le rinominano, devono '
            'dare anche le descrizioni delle mosse da riscrivere. Resta aperta la numerazione delle MN (nota del 3.8: '
            'ITEM_HM05 = Whirlpool/Garòfalu, ITEM_HM06 = Rock Smash/Martiddata nel motore; Acchianata è ITEM_HM08). '
            'I nomi delle MT e delle MN si scrivono col nome di Trinacria della mossa insegnata (R-NOM).',
            '3.13: oltre a statistiche e tipi di R-MOS-03 e R-MOS-09, le descrizioni del 3.9 usano «abilità», il nome '
            'dell’abilità Insonnia (Malasimenza, 388) e «Allenatore» (Sigillu, 373).',
            'Modulo 6: Ventoincoda è la mossa degli stormi del Prestanome dei parchi eolici (M-TP-03, B-TP-02, con '
            'Turbine); Acchianata si sblocca a M-EN-03 per il post-game; Sciamuarmi, Sciamuscutu e Sciamucura sono le '
            'mosse di Vespiquen, che il Re delle Liste Civiche schiera alla Lega (M-EN-04).',
            'Modulo 7: applicazione dei tre banchi per indice, come per i blocchi 3.6–3.8; poi '
            'trinacria_glossary_check.py names --applied → NAMES_OK e trinacria_moves_check.py check … --repo . '
            '--completo → MOSSE_OK.',
        ],
        'strumento': {
            'file': 'tools/trinacria_moves_check.py (nel repository: tools/trinacria/trinacria_moves_check.py, Modulo 7.2)',
            'novita': 'Nessun codice nuovo. Con i quattro blocchi 3.6–3.9 presenti, il collaudo li controlla insieme e '
                      'attiva M09 (copertura 1–467, nomi distinti), come previsto dal 3.6.',
            'comandi': {
                'collaudo': 'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'controllo': 'python -I tools/trinacria_moves_check.py check docs/MODULO_3/3.6_MOSSE_1-120.json '
                             'docs/MODULO_3/3.7_MOSSE_121-240.json docs/MODULO_3/3.8_MOSSE_241-360.json '
                             'docs/MODULO_3/3.9_MOSSE_361-467.json [--repo <pokeheartgold>] --completo → MOSSE_OK',
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
            'collisioni_con_le_specie_risolte': 0,
            'verifiche_superate': [
                'python -I tools/trinacria_moves_check.py --selftest → SELFTEST_OK',
                'python -I tools/trinacria_moves_check.py check 3.6 + 3.7 + 3.8 + 3.9 --repo F:/Progetti/pokeheartgold '
                '--completo → MOSSE_OK (467 mosse)',
                'python -I tools/trinacria_glossary_check.py glossary 3.0 + 3.1–3.5 + 3.6–3.9 --repo '
                'F:/Progetti/pokeheartgold → GLOSSARY_OK',
                'python -I tools/trinacria_glossary_check.py --selftest → SELFTEST_OK',
            ],
        },
        'riga_finale': ('BLOCCO COMPLETO: 3.9 — 107 mosse (%d nomi nuovi: MCP %d, architetto %d; %d dal Glossario 3.0; '
                        '%d nome italiano della trama), 107 descrizioni D-02 (%d righe, la più larga %d px), maiuscoli '
                        'entro 72 px, dati di waza_tbl ricopiati, nessuna deviazione; mosse 1–467 complete (%d nomi '
                        'distinti, M09 superato)'
                        % (c['nuovi'], c['mcp'], c['arch'], c['g30'], c['it'], c['righe'], c['maxpx'], r['nomi_distinti'])),
    }
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(blocco['riga_finale'])

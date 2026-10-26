import json, re

# Parole di sistema che le descrizioni usano col nome italiano ufficiale (per il 3.13 e per i blocchi 3.11-3.12)
PAROLE = [
    ('Bacca', r'\bBacc[ah]e?\b'), ('PS', r'\bPS\b'), ('PP', r'\bPP\b'), ('Attacco', r'\bAttacco\b(?! Speciale)'),
    ('Difesa', r'\bDifesa\b(?! Speciale)'), ('Velocità', r'\bVelocità\b'), ('Attacco Speciale', r'\bAttacco Speciale\b'),
    ('Difesa Speciale', r'\bDifesa Speciale\b'), ('precisione', r'\bprecisione\b'), ('brutti colpi', r'\bbrutti colpi\b'),
    ('statistiche', r'\bstatistiche\b'), ('tipo Acqua', r'\btipo\b[^.]*\bAcqua\b'), ('tipo Coleottero', r'\bColeottero\b'),
    ('tipo Drago', r'\bDrago\b'), ('tipo Spettro', r'\bSpettro\b'), ('tipo Acciaio', r'\bAcciaio\b'),
    ('paralisi', r'\bparalisi\b'), ('avvelenamento', r'\bavvelenamento\b'), ('scottatura', r'\bscottatur[ae]\b'),
    ('congelato', r'\bcongela(to|mento)?\b|\bscongela\b'), ('confusione', r'\bconfusione\b'), ('infatuazione', r'\binfatuazione\b'),
    ('Allenatore', r'\bAllenatore\b'), ('abilità', r'\babilità\b'),
]


def parole(strumenti):
    out = {}
    for label, rx in PAROLE:
        ns = [e['n'] for e in strumenti if not e.get('vuoto') and re.search(rx, ' '.join(e['descrizione']))]
        if ns:
            out[label] = ns
    return out


def piano(mart, assegnati):
    livelli = sorted(mart.tiers.items(), key=lambda x: (x[1], x[0]))
    from trinacria_items_check import TIER_DOSSIER
    return {
        'spiegazione': 'Ogni Centro Pokémon ha il bancone del negozio (trama R-09.5). Il commesso del bancone usa '
                       'ScrCmd_MartBuy: la merce dipende dai Dossier ottenuti (i 9 Dossier stanno sugli slot medaglia, '
                       'registro 2.5), con i livelli di _020FBF22 in src/scrcmd_mart.c, che non si modifica. Alcuni Centri '
                       'hanno un secondo commesso con una lista speciale (ScrCmd_SpecialMartBuy, indice della lista in '
                       '_0210FA3C): l’indice e il Centro sono fissati qui e valgono anche per le MT e le carte da lettere '
                       'dei blocchi 3.11 e 3.12. Le liste non cambiano: cambia solo il Centro che le usa (script del Modulo 6).',
        'livelli_dei_dossier': [{'livello': t, 'dossier_ottenuti': ('%d o più' % d) if t == 6 else
                                 {1: '0', 2: '1–2', 3: '3–4', 4: '5–6', 5: '7'}[t], 'dal_dossier': d}
                                for t, d in sorted(TIER_DOSSIER.items())],
        'bancone_dei_centri': [{'simbolo': s, 'livello': t, 'dal_dossier': TIER_DOSSIER[t]} for s, t in livelli],
        'banconi_speciali': [{'indice': i, 'mappa': assegnati[i], 'strumenti': items}
                             for i, items in enumerate(mart.special)],
        'prezzi': 'Quelli di item_data.csv, copiati nel campo «dati» di ogni strumento: nessun prezzo cambia. L’unica '
                  'eccezione è una vendita a script, non un negozio: l’AcquaFuntana a 2000 al bar del Terminal A (E-CT-06).',
    }


def TESTI(c, strumenti, agg, dev, assegnati, mart, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    blocco = {
        'modulo': 3,
        'blocco': '3.10',
        'titolo': 'Strumenti da #1 a #180',
        'versione': '1.1',
        'data': '26/10/2026',
        'novita_1_1': 'Allineamento con la trama v1.9: i premi che la trama lasciava al Modulo 3 hanno ora uno strumento '
                      'preciso, scritto in «ottenimento.altro»: GranitaCafè (S-CT-03), Cannolu (S-PA-07), Cassata (S-AG-07), '
                      'PetraFocu (S-CT-02, al posto di quella a terra a Nicolosi), PetraAcqua (S-ME-08, al posto di quella a '
                      'terra in ME), PetraArba (S-SR-07, al posto di quella a terra a Pachino), FossiliCupula (premio di '
                      'S-RG-05), OssuLifanti (S-TP-04 e S-EN-05, che la trama premiava con un «Fossile» che il piano 3.1 non '
                      'prevede), le Bacche Pirsica (S-EN-04), Aranciu (S-SR-03) e Racina (S-AG-05). '
                      'Nomi, descrizioni, dati e negozi non cambiano.',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.10_STRUMENTI_1-180.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.11–3.13, 6.x (negozi, oggetti a terra e nascosti, regali, '
                   'dialoghi) e 7.x (applicazione nel repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/items.h (simboli), '
            'files/msgdata/msg/msg_0221.json (descrizioni), msg_0222.json (nomi), msg_0223.json (con l’articolo), '
            'msg_0224.json (plurali), src/item.c e files/itemtool/itemdata/item_data.csv (dati: prezzo, tasca, effetto '
            'tenuto), src/scrcmd_mart.c (banconi dei negozi), src/overlay_03/shop_menu.c:976 (FestaBall in regalo), '
            'src/field/rock_smash_item.c (strumenti sotto le rocce), files/graphic/font/font_00000000.bin e '
            'tools/msgenc/charmap.txt (larghezze e caratteri).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.1: L-03, L-04, L-05, D-03, R-GRA, R-NOM (R-NOM-09 articoli, '
            'R-NOM-10 plurali), R-GLO, i 15 strumenti del Glossario (13 in questo intervallo) e le deviazioni D-01…D-18.',
            'docs/MODULO_3/3.1–3.9: «glossario_aggiunte» delle 493 specie e delle 467 mosse (i nomi degli strumenti non '
            'le ripetono); 3.1_PIANO_INCONTRI.json: mappe dei fossili, dei leggendari e di Armisanti; 3.8 (D-19) e 3.9: '
            'le descrizioni delle mosse 363, 365 e 450 usano «Bacca», la 449 «Lastra».',
            'docs/MODULO_2/2.1–2.4: simboli dei Centri Pokémon (R-09.5: ogni Centro ha il negozio; a Modica il '
            'laboratorio), delle mappe citate e dei pool di flag degli oggetti FLAG_TR_ITEM_<P>_* e FLAG_TR_HIDDEN_<P>_*.',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (625 lemmi, versione 2.0.0): attestazione delle forme '
            '(campo «lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.7: gli strumenti che la trama lascia al Modulo 3 in questo '
            'intervallo (PaniCaMeusa S-PA-02, Sfinciuni S-PA-04, Genovesi S-TP-03, Cassateddi S-EN-03, Sali S-TP-02, '
            'la Pietra di E-SR-01 e le altre Pietre e gli «strumenti rari» dei premi), E-CT-06 e E-PA-01.',
        ],
        'come_si_usa': [
            'Ogni voce di «strumenti» dà nome (msg_0222), forma con l’articolo (msg_0223), plurale (msg_0224) e '
            'descrizione (msg_0221) dello strumento con lo stesso indice: l’esecutore copia i quattro campi di «banchi» '
            'nei quattro banchi, all’indice «n» (Modulo 7). Le voci con «vuoto» (113–134) non si toccano.',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G310-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02) e valgono per i testi del Modulo 6.',
            '«ottenimento» dice dove si compra (calcolato da src/scrcmd_mart.c e dalla sezione «piano_negozi») e come '
            'altro si ottiene: premi della trama, oggetti a terra e nascosti con la provincia del pool di flag (il '
            'Modulo 6 sceglie la mappa nella provincia, tranne dove la mappa è scritta), regali. Il campo «dati» '
            'riporta prezzo, tasca ed effetto di HeartGold e non si modifica.',
            'Controllo: python -I tools/trinacria_items_check.py check docs/MODULO_3/3.10_STRUMENTI_1-180.json '
            '--repo F:/Progetti/pokeheartgold → STRUMENTI_OK; poi python -I tools/trinacria_glossary_check.py glossary '
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json docs/MODULO_3/3.1_POKEMON_1-100.json … '
            'docs/MODULO_3/3.10_STRUMENTI_1-180.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.10/gen310.py (contenuti in content310.py, parti fisse in '
            'text310.py), che usa le stesse funzioni dello strumento di controllo. I blocchi 3.11 e 3.12 partono da una '
            'copia di questa cartella.',
        ],
        'regole': {
            'R-STR-01': 'Nomi. Ogni strumento ha un nome siciliano (specifica PLOT §5: «rinominare … gli Strumenti»), '
                        'tranne quelli che la trama cita in italiano, che tengono la forma della trama con lingua «it» e '
                        'senza voce nel Glossario: in questo intervallo solo Genovese (43, S-TP-03). I 13 strumenti del '
                        'Glossario 3.0 in questo intervallo si ricopiano. Gli strumenti della trama col nome siciliano '
                        '(PaniCaMeusa, Sfinciuni, Cassatedda, Sali, la Pietra di E-SR-01 = PetraSulari) stanno sugli slot '
                        'che hanno lo stesso effetto: cibi curativi sui dolci regionali di HeartGold (Lava Cookie, Old '
                        'Gateau, Berry Juice) e su Moomoo Milk, il sale sullo Shoal Salt.',
            'R-STR-02': 'Slot vuoti. Gli strumenti 113–134 (ITEM_UNUSED_113…134) non esistono in HeartGold: puntano a '
                        'item_data_0000 e hanno «???» nei banchi. Restano così (nessun nome, nessun dato): il blocco li '
                        'elenca con «vuoto» solo perché i blocchi 3.10–3.12 coprano 1–536. Gli strumenti chiave della '
                        'trama che mancano (Amuleto, 9 Atti, 9 Faldoni) vanno su slot che esistono già, nei blocchi 3.11–3.12.',
            'R-STR-03': 'Articolo e plurale. Forma con l’articolo di R-NOM-09 (genere nel campo «genere»; «un’» '
                        'attaccato al colore). Plurale di R-NOM-10: composti attaccati, nomi in -Ball e abbreviazioni '
                        'invariabili; parole semplici -u/-a → -i, con -iu/-ia → -i (Curaggiu → Curaggi), -cu/-ca → -chi e '
                        '-gu/-ga → -ghi (Pirsica → '
                        'Pirsichi, Marengu → Marenghi); invariabili anche i nomi di massa e quelli già in -i o in vocale '
                        'accentata (Ogghiu, Riganu, Meli, Ciciri, Zammù…), scritti nel campo «plurale».',
            'R-STR-04': 'Descrizioni. In italiano, col profilo D-03 (3 righe, 41 caratteri e 215 px, nessun «\\n» '
                        'finale), come le descrizioni delle mosse (R-MOS-03 del 3.6). Statistiche, stati, tipi, «brutti '
                        'colpi» e «Bacca» hanno il nome italiano ufficiale: l’elenco degli strumenti che li usano è nella '
                        'sezione «parole_di_sistema_nelle_descrizioni». I luoghi di HeartGold nelle descrizioni (Lavaridge, '
                        'Old Chateau, Shoal Cave, Great Marsh, Sinnoh) diventano luoghi siciliani o spariscono.',
            'R-STR-05': 'Bacche. Le 64 Bacche prendono il nome del frutto siciliano, senza prefisso (Cirasa, Pumu, '
                        'Aranciu…; le cinque dei gusti hanno un frutto di quel sapore: Pipi piccante, Nucidda secca, Ficu '
                        'dolce, Aliva amara, Limuni aspra). «Bacca» e «Bacche» restano la parola italiana generica della '
                        'categoria (tasca della borsa, descrizioni): per questo le descrizioni delle mosse 363, 365 e 450 '
                        'dei blocchi 3.9 non cambiano. Il nome della tasca è del 3.13, che deve tenerlo «Bacche» o dare '
                        'anche le descrizioni da riscrivere (mosse 363, 365, 450 e gli strumenti elencati sotto «Bacca»).',
            'R-STR-06': 'Negozi. Sezione «piano_negozi»: il bancone dei Centri a livelli di Dossier e i 30 banconi '
                        'speciali assegnati ai Centri. Vale per tutti i blocchi degli strumenti: il 3.11 e il 3.12 '
                        'ricalcolano «ottenimento.negozi» con lo stesso piano (le MT delle liste 7 e 20 si comprano alla '
                        'Fiera del Mediterraneo). Nessuna lista e nessun prezzo cambia.',
            'R-STR-07': 'Oggetti a terra, nascosti e regali. «ottenimento.altro» fissa quantità e provincia; dove scrive '
                        'una mappa (MAP_…) vale quella, altrimenti il Modulo 6 la sceglie tra le mappe della provincia e '
                        'usa un flag del pool del registro 2.4 (FLAG_TR_ITEM_<P>_* a terra, FLAG_TR_HIDDEN_<P>_* nascosti). '
                        '«<P>» è ognuna delle 9 province (CT, SR, RG, CL, AG, TP, ME, PA, EN); ROADS sono le strade. Le Bacche '
                        'vengono dalle piante del Modulo 6 nelle province scritte.',
            'R-STR-08': 'Famiglie di nomi. «-Ball» (Glossario 3.0), «Petra-» (pietre dell’evoluzione), «Zufulu-» (gli '
                        'zufoli: Friscalettu è una mossa), «Cocciu-» (i cocci), «Fossili-» (i fossili; Scutu e Crozza come '
                        'le specie che rinascono), «Sfera-» (le sfere dei leggendari), «Carta-» (le carte da lettere: '
                        'Littra è una specie), gli spaventi Scanticeddu/Scantuni/Terruri (repellenti), i cibi nutrienti '
                        '(integratori), le bevande dei chioschi (cure). Nei composti attaccati l’accento interno si omette '
                        '(R-GRA-03). I blocchi 3.11–3.12 continuano queste famiglie.',
            'R-STR-09': 'Nomi delle specie nelle descrizioni. Le sfere nominano il leggendario col nome del Glossario '
                        '(Ribbelli, Seculu, Spaziu), come le descrizioni delle mosse nominano le mosse (R-MOS-10).',
            'R-STR-10': 'Dati. Il campo «dati» è ricopiato da item_data.csv (prezzo, tasca, effetto tenuto e suo '
                        'parametro) e lo strumento di controllo lo confronta col repository (S11): il Modulo 3 non cambia '
                        'gli effetti degli strumenti.',
        },
        'deviazioni_dalle_specifiche': dev,
        'strumenti': strumenti,
        'glossario_aggiunte': agg,
        'piano_negozi': piano(mart, assegnati),
        'parole_di_sistema_nelle_descrizioni': {
            'spiegazione': 'Numeri degli strumenti di questo blocco la cui descrizione usa la parola. Se il 3.13 cambia '
                           'una di queste parole, dà anche le descrizioni da riscrivere (come per le mosse, R-MOS-09).',
            'parole': parole(strumenti),
        },
        'note_per_blocchi_successivi': [
            '3.11–3.12: copiano tools/generatori/3.10/ (gen311.py…) e usano lo stesso strumento di controllo; il 3.12 '
            'aggiunge --completo (S09: 1–536 una volta sola). I prossimi id del Glossario sono G311-0001… e G312-0001….',
            '3.11: le Lastre (298–313) sono la categoria che la descrizione della mossa 449 chiama «Lastra»: se il 3.11 '
            'dà alle Lastre un nome di famiglia diverso, dà anche la descrizione della mossa 449 da riscrivere. Le Bacche '
            '181–212 continuano R-STR-05 (frutti siciliani; le Bacche che dimezzano i danni hanno il frutto e il tipo '
            'nella descrizione).',
            '3.12: decide le MN (ITEM_HM01…08). In HeartGold ITEM_HM05 insegna Whirlpool (Garòfalu) e ITEM_HM06 Rock '
            'Smash (Martiddata), e ITEM_HM08 Rock Climb (Acchianata); le note del Glossario 3.0 dicono «MN 5» per '
            'Martiddata e «MN 6» per Garòfalu: il 3.12 sceglie e, se serve, corregge il Glossario con una nuova versione '
            'del 3.0. Il 3.12 mette anche gli strumenti chiave della trama (Amuleto ST-12, 9 Atti ST-02, 9 Faldoni ST-07) '
            'su slot di strumenti chiave che esistono già (R-STR-02).',
            '3.13: il nome della tasca delle Bacche resta «Bacche» (R-STR-05) o il 3.13 riscrive le descrizioni delle '
            'mosse 363, 365, 450 e degli strumenti elencati sotto «Bacca»; lo stesso per statistiche, stati e tipi '
            'elencati in «parole_di_sistema_nelle_descrizioni».',
            'Modulo 6: le vendite a script (AcquaFuntana a 2000 al Terminal A, E-CT-06), i regali e i premi scritti in '
            '«ottenimento.altro», gli oggetti a terra e nascosti con i flag dei pool provinciali, le piante delle Bacche.',
        ],
        'strumento': {
            'file': 'tools/trinacria_items_check.py',
            'file_di_prova': 'tools/testdata/strumenti_prova_ko.json',
            'comandi': ['--selftest → SELFTEST_OK', 'check <blocchi> [--repo <pokeheartgold>] [--docs <docs>] [--completo] → STRUMENTI_OK'],
            'codici': {
                'S00': 'file illeggibile o senza «strumenti»',
                'S01': 'nome oltre L-03 (15 caratteri, 72 px) o con caratteri non ammessi (R-GRA-11)',
                'S02': 'forma con l’articolo diversa da R-NOM-09 o oltre L-04 (90 px)',
                'S03': 'plurale oltre L-05 (82 px)',
                'S04': 'descrizione fuori dal profilo D-03 o msg_0221 diverso dalle righe',
                'S05': 'numero, simbolo o nome inglese diversi da items.h e msg_0222 (con --repo)',
                'S06': 'banchi diversi dai campi della voce',
                'S07': 'nome siciliano assente dal Glossario o diverso; nome italiano non della trama',
                'S08': 'stesso nome di un altro nome di sistema (specie, mossa, strumento, classe, soprannome…)',
                'S09': 'con --completo: strumenti 1–536 non coperti una volta sola o nome ripetuto',
                'S10': 'slot 113–134 non vuoto o slot vero segnato vuoto',
                'S11': 'dati diversi da item_data.csv (con --repo)',
                'S12': 'negozi diversi da src/scrcmd_mart.c e dal piano (con --repo) o strumento senza modo di ottenerlo',
            },
            'collaudo': 'il blocco 3.10 (e i successivi presenti) senza errori; strumenti_prova_ko.json con gli errori '
                        'attesi del suo campo «errori_attesi».',
        },
        'controllo': {
            'strumenti': c['strumenti'],
            'slot_vuoti': c['vuoti'],
            'nomi_siciliani_nuovi': c['nuovi'],
            'nomi_nuovi_per_fonte': {'MCP': c['mcp'], 'architetto': c['arch']},
            'nomi_mcp': mcp,
            'nomi_dal_glossario_3_0': c['g30'],
            'nomi_italiani_della_trama': c['it'],
            'nome_piu_largo_px': c['maxnome'],
            'con_articolo_piu_largo_px': c['maxart'],
            'plurale_piu_largo_px': c['maxplur'],
            'righe_di_descrizione': c['righe'],
            'riga_di_descrizione_piu_larga_px': c['maxpx'],
            'strumenti_che_si_comprano': c['venduti'],
            'deviazioni': [d['id'] for d in dev],
            'verifiche_superate': ['trinacria_items_check.py check --repo → STRUMENTI_OK',
                                   'trinacria_glossary_check.py glossary (3.0 + 3.1–3.10) → GLOSSARY_OK',
                                   'trinacria_items_check.py --selftest → SELFTEST_OK'],
        },
    }
    riga = ('BLOCCO COMPLETO: 3.10 — %d strumenti (%d nomi nuovi: MCP %d, architetto %d; %d dal Glossario 3.0; '
            '%d nome italiano della trama) e %d slot vuoti invariati, %d descrizioni D-03 (%d righe, la più larga %d px), '
            'nomi entro 72 px, con l’articolo entro 90 px, plurali entro 82 px, dati di item_data.csv ricopiati; piano dei '
            'negozi (bancone a livelli di Dossier e 30 banconi speciali sui Centri: %d strumenti in vendita); deviazione '
            'D-20; strumento nuovo trinacria_items_check.py (S00–S12) collaudato') % (
        c['strumenti'], c['nuovi'], c['mcp'], c['arch'], c['g30'], c['it'], c['vuoti'], c['strumenti'], c['righe'],
        c['maxpx'], c['venduti'])
    blocco['riga_finale'] = riga
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(riga)

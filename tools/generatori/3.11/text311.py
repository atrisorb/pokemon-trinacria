import json, re

TIPI = ['Normale', 'Fuoco', 'Acqua', 'Elettro', 'Erba', 'Ghiaccio', 'Lotta', 'Veleno', 'Terra', 'Volante', 'Psico',
        'Coleottero', 'Roccia', 'Spettro', 'Drago', 'Buio', 'Acciaio']
# Parole di sistema che le descrizioni usano col nome italiano ufficiale (per il 3.13), come nel 3.10
PAROLE = [
    ('Bacca', r'\bBacc[ah]e?\b'), ('Lastra', r'\bLastr[ae]\b'), ('PS', r'\bPS\b'), ('PP', r'\bPP\b'),
    ('Attacco', r'\bAttacco\b(?! Speciale)'), ('Difesa', r'\bDifesa\b(?! Speciale)'), ('Velocità', r'\bVelocità\b'),
    ('Attacco Speciale', r'\bAttacco Speciale\b'), ('Difesa Speciale', r'\bDifesa Speciale\b'),
    ('precisione', r'\bprecis[ia]'), ('elusione', r'\belusione\b'), ('brutti colpi', r'\bbrutti colpi\b'),
    ('statistiche', r'\bstatistic[ah]e?\b'), ('superefficace', r'\bsuperefficac[ei]\b'),
    ('tentennare', r'\btentenn'), ('KO', r'\bKO\b'), ('Punti Esperienza', r'\bPunti Esperienza\b'),
    ('mosse fisiche / attacco fisico', r'\bfisic[oh]e?\b'), ('mosse speciali / attacco speciale', r'\b(mosse|attacco) special[ei]\b'),
    ('paralisi / paralizzare', r'\bparali'), ('avvelenamento / avvelenare', r'\bavvelen|\bveleno\b'),
    ('scottatura', r'\bscottatur[ae]\b'), ('congelare', r'\bcongel'), ('confusione / confondere', r'\bconfu|\bconfond'),
    ('infatuazione / infatuarsi', r'\binfatua'), ('Allenatore', r'\bAllenatore\b'), ('abilità', r'\babilità\b'),
] + [('tipo %s' % t, r'\btipo %s\b' % t) for t in TIPI]


def parole(strumenti):
    out = {}
    for label, rx in PAROLE:
        ns = [e['n'] for e in strumenti if re.search(rx, ' '.join(e['descrizione']))]
        if ns:
            out[label] = ns
    return out


def TESTI(c, strumenti, agg, dev, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    mt = [e for e in strumenti if 'mossa' in e]
    blocco = {
        'modulo': 3,
        'blocco': '3.11',
        'titolo': 'Strumenti da #181 a #360',
        'versione': '1.0',
        'data': '26/10/2026',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.11_STRUMENTI_181-360.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.12–3.13, 6.x (premi, oggetti a terra e nascosti, regali, '
                   'piante delle Bacche, dialoghi) e 7.x (applicazione nel repository). Ogni valore è deciso: non si '
                   'sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/items.h (simboli), '
            'files/msgdata/msg/msg_0221.json (descrizioni), msg_0222.json (nomi), msg_0223.json, msg_0224.json, '
            'src/item.c (dati e sTMHMMoves: la mossa di ogni MT), files/itemtool/itemdata/item_data.csv, '
            'src/scrcmd_mart.c (banconi), files/poketool/personal/personal.json e include/constants/species.h (strumenti '
            'tenuti dai selvatici), src/pokemon.c:3736 (WildMonSetRandomHeldItem: 50, 5 e 100 per cento), '
            'files/graphic/font/font_00000000.bin e tools/msgenc/charmap.txt (larghezze).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.1: L-03, L-04, L-05, D-03, R-GRA, R-NOM, R-GLO; il Glossario non '
            'ha strumenti in questo intervallo (i suoi ultimi due, SH Scassatu 450 e Ciucculatta 504, sono del 3.12).',
            'docs/MODULO_3/3.10_STRUMENTI_1-180.json v1.1: regole R-STR-01…10, piano dei negozi (R-STR-06), famiglie di '
            'nomi (R-STR-08), «glossario_aggiunte» G310 per le collisioni.',
            'docs/MODULO_3/3.1–3.5: nomi delle specie (descrizioni e collisioni); 3.1_PIANO_INCONTRI.json: tabelle dei '
            'selvatici (gs_enc_data, Safari, bottintesta, sciami), «evoluzioni» (EVO_ITEM_DAY con gli strumenti 221, '
            '226, 227, 233, 235, 246, 252, 321–325), leggendari (Isulidda a Taormina) e mitici non ottenibili '
            '(Patreternu).',
            'docs/MODULO_3/3.6–3.9: nomi e descrizioni delle mosse (le MT, R-STR-11; Paraluci, Paracorpi, Grannulata, '
            'RinaDiL’Etna, Giornodisole, Ballacqua, Lazzu, Nfasciata nelle descrizioni); la mossa 449 Judiziu usa «Lastra».',
            'docs/MODULO_2/2.1–2.4: simboli delle mappe citate (controllati dal generatore) e pool di flag '
            'FLAG_TR_ITEM_<P>_* e FLAG_TR_HIDDEN_<P>_*.',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (versione 2.0.0): attestazione delle forme («lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.9: premi della trama in questo intervallo (ITEM_AMULET_COIN S-CT-01, '
            'ITEM_LEFTOVERS S-CT-07, ITEM_SCOPE_LENS S-SR-04, ITEM_LUCKY_EGG S-RG-07, ITEM_EXP__SHARE S-CL-05, '
            'ITEM_SILK_SCARF S-AG-06, ITEM_SOOTHE_BELL S-ME-05) e le 10 «MT» senza numero (M-CT-06, S-CT-05, S-SR-02, '
            'S-CL-02, S-AG-04, S-TP-05, S-TP-07, S-ME-04, S-PA-03, S-EN-02).',
        ],
        'come_si_usa': [
            'Come nel 3.10: ogni voce di «strumenti» dà nome (msg_0222), forma con l’articolo (msg_0223), plurale '
            '(msg_0224) e descrizione (msg_0221) dello strumento con lo stesso indice; l’esecutore copia i quattro campi '
            'di «banchi» all’indice «n» (Modulo 7).',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G311-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02). Le MT (328–360) non hanno voce nel Glossario: tengono la sigla italiana (R-STR-11).',
            '«ottenimento» ha tre campi: «negozi» (calcolato da src/scrcmd_mart.c col piano del 3.10), «selvatici» '
            '(calcolato, R-STR-13: non si scrive nulla nel repository, è già in personal.json) e «altro» (premi della '
            'trama, oggetti a terra e nascosti coi pool provinciali, regali, piante: lavoro del Modulo 6, R-STR-07).',
            'Controllo: python -I tools/trinacria_items_check.py check docs/MODULO_3/3.10_STRUMENTI_1-180.json '
            'docs/MODULO_3/3.11_STRUMENTI_181-360.json --repo F:/Progetti/pokeheartgold → STRUMENTI_OK; poi '
            'python -I tools/trinacria_glossary_check.py glossary docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json '
            'docs/MODULO_3/3.1_POKEMON_1-100.json … docs/MODULO_3/3.11_STRUMENTI_181-360.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.11/gen311.py (contenuti in content311.py, parti fisse in '
            'text311.py), copia del generatore del 3.10. Il 3.12 parte da una copia di questa cartella.',
        ],
        'regole': {
            'R-STR-01…10': 'Valgono come nel blocco 3.10 (nomi siciliani, slot vuoti, articolo e plurale, descrizioni '
                           'D-03, Bacche, negozi, oggetti a terra e nascosti, famiglie di nomi, specie nelle descrizioni, '
                           'dati di item_data.csv). In questo intervallo nessuno strumento ha un nome italiano della '
                           'trama (R-STR-01) tranne le sigle delle MT (R-STR-11) e nessuno slot è vuoto (R-STR-02).',
            'R-STR-11': 'MT. Le MT si chiamano «MT01»…«MT92» e le MN «MN01»…«MN08» (sigle italiane che la trama usa, '
                        '«MT»; il Glossario 3.0 scrive «MN 5» ecc.): lingua «it», nessuna voce nel Glossario, femminili '
                        '(«una MT01»), plurale invariabile. Lo strumento di controllo le ha nel suo elenco TRAMA_IT. La '
                        'mossa insegnata è quella di sTMHMMoves in src/item.c (campo «mossa»): non cambia. La '
                        'descrizione, come in HeartGold, è quella della mossa: il testo del blocco 3.6–3.9, a parole '
                        'intere, riscritto nel profilo D-03 (codice S14). Se il 3.13 o un’altra versione di un blocco '
                        'delle mosse cambia una di queste descrizioni, la descrizione della MT si rigenera.',
            'R-STR-12': 'Premi «MT» della trama. Le 10 «MT» che la trama dà senza numero sono MT di questo intervallo: '
                        'M-CT-06 → MT18 (Ballacqua, la pioggia sull’incendio), S-CT-05 → MT10, S-SR-02 → MT05 '
                        '(Alluccata, l’eco), S-CL-02 → MT30 (Ummirabadda, i fantasmi), S-AG-04 → MT04 (Abbentu, il '
                        'libro), S-TP-05 → MT03 (Acquapulsu), S-TP-07 → MT26 (Scussuni, le cave), S-ME-04 → MT06 '
                        '(Tossicu, le fumarole), S-PA-03 → MT29 (Sfirniciata, il mosaico), S-EN-02 → MT31 (Spaccamuru, '
                        'il castello nella roccia). Sono MT che non si comprano; le altre MT 01–33 che non si comprano '
                        'alla Fiera del Mediterraneo (banconi 7 e 20) sono a terra in una provincia.',
            'R-STR-13': 'Selvatici. «ottenimento.selvatici» elenca le specie delle tabelle del piano 3.1 (gs_enc_data, '
                        'Safari di Vendicari, bottintesta, sciami) che tengono lo strumento in personal.json, con la '
                        'probabilità di WildMonSetRandomHeldItem: 50 per il primo strumento, 5 per il secondo, 100 se '
                        'sono uguali (senza l’abilità che le alza). È un dato calcolato e informativo: nessun file '
                        'cambia. Lo strumento di controllo lo ricalcola (S13). Uno strumento che si ottiene solo così non '
                        'ha «altro».',
            'R-STR-14': 'Strumenti dell’evoluzione. Le descrizioni dicono come si evolve in Trinacria (piano 3.1, '
                        'R-INC-05): gli strumenti degli scambi di HeartGold fanno evolvere salendo di livello di giorno '
                        '(EVO_ITEM_DAY), GranfaFina e Sanna di notte come in HeartGold. Ognuno si trova a terra o nascosto '
                        'prima della Lega, oltre che dai selvatici dove ci sono.',
            'R-STR-15': 'Famiglie nuove (continuano R-STR-08). «Lastra-» + la parola siciliana del tipo per le 16 Lastre: '
                        '«Lastra» resta anche la parola della categoria, quindi la descrizione della mossa 449 (Judiziu, '
                        'blocco 3.9) non cambia; «Erba-» (erbe da tenere), «Badda-» (palle: Ummirabadda è una mossa), '
                        '«Sfera-» (le sfere, come nel 3.10), «Cuti-» (ciottoli e pietre del tempo), «Ncenzu-» (incensi), '
                        '«Pisu-» (pesi), «Fularu-» (foulard, senza effetto: in Trinacria non ci sono gare), «Lenti-», '
                        '«Cascia-», «Granfa-» (artigli, come FossiliGranfa). Le Bacche 181–212 continuano R-STR-05: quelle '
                        'che indeboliscono un tipo hanno il frutto e il tipo nella descrizione.',
        },
        'deviazioni_dalle_specifiche': dev,
        'strumenti': strumenti,
        'glossario_aggiunte': agg,
        'mt': {
            'spiegazione': 'Le 33 MT del blocco con la mossa insegnata e come si ottengono (R-STR-11, R-STR-12).',
            'elenco': [{'n': e['n'], 'nome': e['nome'], 'mossa': e['mossa'], 'negozi': [x.get('mappa') for x in
                        e['ottenimento']['negozi']], 'altro': e['ottenimento']['altro']} for e in mt],
        },
        'parole_di_sistema_nelle_descrizioni': {
            'spiegazione': 'Numeri degli strumenti di questo blocco la cui descrizione usa la parola. Se il 3.13 cambia '
                           'una di queste parole, dà anche le descrizioni da riscrivere (R-MOS-09, R-STR-04). Per le MT '
                           'la descrizione viene dalla mossa: si riscrive la mossa e la MT si rigenera (R-STR-11).',
            'parole': parole(strumenti),
        },
        'note_per_blocchi_successivi': [
            '3.12: copia tools/generatori/3.11/ (gen312.py…), usa lo stesso strumento di controllo e aggiunge --completo '
            '(S09: 1–536 una volta sola). I prossimi id del Glossario sono G312-0001…. Le MT 34–92 e le MN seguono '
            'R-STR-11 (le sigle sono già nell’elenco TRAMA_IT dello strumento); le MT 34–92 che non si comprano vanno a '
            'terra o nascoste come qui. I premi «MT» della trama sono tutti assegnati (R-STR-12).',
            '3.12: decide ancora le MN (ITEM_HM05 = Whirlpool/Garòfalu, ITEM_HM06 = Rock Smash/Martiddata in HeartGold, '
            'al contrario delle note del Glossario 3.0), gli slot degli strumenti chiave della trama (Amuleto ST-12, 9 '
            'Atti ST-02, 9 Faldoni ST-07), le canne (ITEM_OLD_ROD S-CT-04, ITEM_GOOD_ROD M-SR-03, ITEM_SUPER_ROD M-TP-03) '
            'e copia i due strumenti del Glossario 3.0 del suo intervallo (SH Scassatu 450, Ciucculatta 504 di S-RG-02).',
            '3.12: «ottenimento.selvatici» come qui (R-STR-13). Il 3.10 non ha questo campo (lo strumento lo controlla '
            'solo dove c’è): i suoi strumenti tenuti dai selvatici restano descritti da «negozi» e «altro».',
            '3.13: le parole di «parole_di_sistema_nelle_descrizioni» (tipi, statistiche, stati, «Punti Esperienza», '
            '«tentennare», «KO», «Bacca», «Lastra») restano coi nomi italiani ufficiali o il 3.13 dà le descrizioni da '
            'riscrivere.',
            'Modulo 6: premi della trama scritti in «altro» (sette strumenti tenuti e dieci MT), oggetti a terra e '
            'nascosti coi pool provinciali (le Lastre e gli strumenti segnati «post-game» si mettono in mappe del '
            'post-game o dietro FLAG_POST_RESIGNATION), le piante delle Bacche 181–212, i cinque foulard regalati dalle '
            'sarte.',
        ],
        'strumento': {
            'file': 'tools/trinacria_items_check.py',
            'file_di_prova': 'tools/testdata/strumenti_prova_ko.json',
            'comandi': ['--selftest → SELFTEST_OK', 'check <blocchi> [--repo <pokeheartgold>] [--docs <docs>] [--completo] → STRUMENTI_OK'],
            'codici_nuovi': {
                'S12': 'come nel 3.10; «selvatici» conta come modo di ottenere lo strumento. Il piano dei negozi si legge '
                       'dal 3.10 anche quando si controlla un blocco successivo da solo.',
                'S13': 'selvatici diversi da personal.json e dalle tabelle del piano 3.1 (con --repo)',
                'S14': 'MT o MN con la mossa diversa da sTMHMMoves o la descrizione diversa da quella della mossa '
                       'riscritta in D-03 (con --repo)',
            },
            'collaudo': 'i blocchi 3.10 e 3.11 senza errori; strumenti_prova_ko.json con gli errori attesi del suo campo '
                        '«errori_attesi» (ora anche S13 e S14).',
        },
        'controllo': {
            'strumenti': c['strumenti'],
            'nomi_siciliani_nuovi': c['nuovi'],
            'nomi_nuovi_per_fonte': {'MCP': c['mcp'], 'architetto': c['arch']},
            'nomi_mcp': mcp,
            'nomi_dal_glossario_3_0': c['g30'],
            'mt_con_sigla': c['mt'],
            'nome_piu_largo_px': c['maxnome'],
            'con_articolo_piu_largo_px': c['maxart'],
            'plurale_piu_largo_px': c['maxplur'],
            'righe_di_descrizione': c['righe'],
            'riga_di_descrizione_piu_larga_px': c['maxpx'],
            'strumenti_che_si_comprano': c['venduti'],
            'strumenti_tenuti_dai_selvatici': c['selvatici'],
            'premi_mt_della_trama': c['premi_mt'],
            'deviazioni': [d['id'] for d in dev],
            'verifiche_superate': ['trinacria_items_check.py check 3.10 3.11 --repo → STRUMENTI_OK',
                                   'trinacria_glossary_check.py glossary (3.0 + 3.1–3.11) → GLOSSARY_OK',
                                   'trinacria_items_check.py --selftest → SELFTEST_OK'],
        },
    }
    riga = ('BLOCCO COMPLETO: 3.11 — %d strumenti (%d nomi siciliani nuovi: MCP %d, architetto %d; %d MT con la sigla '
            'italiana e la descrizione della mossa), %d descrizioni D-03 (%d righe, la più larga %d px), nomi entro 72 '
            'px, con l’articolo entro 90 px, plurali entro 82 px, dati di item_data.csv ricopiati; %d strumenti in '
            'vendita col piano del 3.10, %d tenuti dai selvatici, %d premi «MT» della trama assegnati; nessuna '
            'deviazione; trinacria_items_check.py esteso (S13, S14)') % (
        c['strumenti'], c['nuovi'], c['mcp'], c['arch'], c['mt'], c['strumenti'], c['righe'], c['maxpx'],
        c['venduti'], c['selvatici'], c['premi_mt'])
    blocco['riga_finale'] = riga
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(riga)

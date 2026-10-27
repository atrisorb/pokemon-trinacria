import json, re
import trinacria_items_check as chk

TIPI = ['Normale', 'Fuoco', 'Acqua', 'Elettro', 'Erba', 'Ghiaccio', 'Lotta', 'Veleno', 'Terra', 'Volante', 'Psico',
        'Coleottero', 'Roccia', 'Spettro', 'Drago', 'Buio', 'Acciaio']
# Parole di sistema che le descrizioni usano col nome italiano ufficiale (per il 3.13), come nel 3.10 e nel 3.11
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
    ('infatuazione / infatuarsi', r'\binfatua'), ('Allenatore', r'\bAllenator[ei]\b'), ('abilità', r'\babilità\b'),
    ('Punti Lotta', r'\bPunti Lotta\b'), ('Poké Ball', r'\bPoké Ball\b'), ('Codici Amico', r'\bCodici Amico\b'),
    ('Pokédex', r'\bPokédex\b'), ('Scheda Allenatore', r'\bScheda Allenatore\b'),
] + [('tipo %s' % t, r'\b(tipo|Pokémon) %s\b' % t) for t in TIPI]


def parole(strumenti):
    out = {}
    for label, rx in PAROLE:
        ns = [e['n'] for e in strumenti if re.search(rx, ' '.join(e.get('descrizione', [])))]
        if ns:
            out[label] = ns
    return out


def TESTI(c, strumenti, agg, dev, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    mt = [e for e in strumenti if 'mossa' in e]
    per_n = {e['n']: e for e in strumenti}
    chiave = [
        ('Amuleto', [439], 'ST-12'),
        ('Atti del Fascicolo Trinacria', sorted(chk.ATTI), 'ST-02, VAR_ST_02'),
        ('Faldoni di Totò', sorted(chk.FALDONI), 'ST-07, VAR_ST_07, FLAG_ST_07_FALDONE_*'),
        ('Canne', [445, 446, 447], 'S-CT-04, M-SR-03, M-TP-03 (R-10.7)'),
        ('Scooter', [450], 'M-CT-03'),
        ('Fiutatore dei faldoni', [471], 'M-CT-09, FLAG_C_06'),
        ('Vasi e spruzzino delle Bacche', [470, 477], 'Modulo 6, CT'),
        ('Ball artigianali', [468] + list(range(485, 499)), 'S-CT-07, R-STR-19'),
        ('Censimento dei Littra', [469], 'S-RG-05'),
        ('Connessioni e Fiera', [437, 465], 'Centro Pokémon di Catania, P-09'),
        ('Ricordi dei leggendari', [453, 458, 482, 483, 532, 534, 535, 536], 'post-game, piano 3.1'),
        ('Ciucculatta', [504], 'S-RG-02'),
    ]
    blocco = {
        'modulo': 3,
        'blocco': '3.12',
        'titolo': 'Strumenti da #361 a #536',
        'versione': '1.0',
        'data': '26/10/2026',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.12_STRUMENTI_361-536.json',
        'lettore': 'LLM esecutore e autore dei blocchi 3.13, 4.x (icone degli strumenti chiave), 6.x (premi, oggetti a '
                   'terra e nascosti, regali, piante dei Pirazzi, Ball artigianali, dialoghi) e 7.x (applicazione nel '
                   'repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 26/10/2026: include/constants/items.h (simboli), '
            'files/msgdata/msg/msg_0221.json (descrizioni), msg_0222.json (nomi), msg_0223.json, msg_0224.json, '
            'src/item.c (dati e sTMHMMoves: la mossa di ogni MT e MN; ITEM_EXPLORER_KIT punta a item_data_0000), '
            'files/itemtool/itemdata/item_data.csv (prezzo, tasca, fieldUseFunc: gli slot degli Atti e dei faldoni '
            'hanno fieldUseFunc 0 e nessuno script), src/scrcmd_mart.c (banconi), files/poketool/personal/personal.json '
            'e include/constants/species.h (strumenti tenuti dai selvatici), files/graphic/font/font_00000000.bin e '
            'tools/msgenc/charmap.txt (larghezze).',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.2: L-03, L-04, L-05, D-03, R-GRA, R-NOM, R-GLO; i due strumenti '
            'del Glossario in questo intervallo (SH Scassatu 450, Ciucculatta 504) e le MN della trama (R-03).',
            'docs/MODULO_3/3.10_STRUMENTI_1-180.json v1.1 e 3.11_STRUMENTI_181-360.json: regole R-STR-01…15, piano dei '
            'negozi (R-STR-06), famiglie di nomi (R-STR-08, R-STR-15), «glossario_aggiunte» G310 e G311 per le '
            'collisioni e per il controllo --completo.',
            'docs/MODULO_3/3.1–3.5: nomi delle specie; 3.1_PIANO_INCONTRI.json: tabelle dei selvatici, leggendari del '
            'post-game (le mappe dei ricordi dei leggendari), mitici non ottenibili (Patreternu, Ciurita).',
            'docs/MODULO_3/3.6–3.9: nomi e descrizioni delle mosse delle MT 34–92 e delle MN 01–08 (R-STR-11).',
            'docs/MODULO_2/2.1–2.4: mappe citate (controllate dal generatore), slot esclusi e mappe riassegnate '
            '(Gara Coleotteri, Parco Amici, sale giochi, Pokéathlon), pool FLAG_TR_ITEM_<P>_* e FLAG_TR_HIDDEN_<P>_*, '
            'sezione «sottotrame» (missioni degli Atti di ST-02, mappe e flag dei faldoni di ST-07), '
            'FLAG_ST_12_AMULETO_CONSEGNATO, FLAG_C_02, FLAG_C_06.',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (versione 2.0.0): attestazione delle forme («lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.9: R-03 (Dossier e MN), R-10.7 (canne, Littra, regali), ST-02, '
            'ST-07, ST-12, M-CT-03 (SH Scassatu), S-CT-04, M-SR-03, M-TP-03 (canne), S-CT-07 (il maestro ceramista di '
            'Caltagirone), S-RG-02 (Ciucculatta), S-RG-05, P-02, P-03, P-04, P-08, P-09.',
        ],
        'come_si_usa': [
            'Come nel 3.10 e nel 3.11: ogni voce di «strumenti» dà nome (msg_0222), forma con l’articolo (msg_0223), '
            'plurale (msg_0224) e descrizione (msg_0221) dello strumento con lo stesso indice; l’esecutore copia i '
            'quattro campi di «banchi» all’indice «n» (Modulo 7). Lo slot 428 è vuoto e resta com’è (R-STR-02).',
            'I nomi siciliani nuovi sono nella «glossario_aggiunte» (G312-0001…): entrano nel Glossario bloccato con '
            '«merge» (R-GLO-02). Non hanno voce nel Glossario le MT e le MN (R-STR-11) e i nomi italiani della trama: '
            'Amuleto, i 9 Atti e i 9 Faldoni (R-STR-18).',
            '«ottenimento» ha i tre campi del 3.11: «negozi» (calcolato col piano del 3.10), «selvatici» (calcolato, '
            'R-STR-13) e «altro» (premi, oggetti a terra e nascosti, regali: lavoro del Modulo 6, R-STR-07). Gli '
            'strumenti che non si ottengono lo dicono in «altro» (R-STR-17).',
            'Controllo: python -I tools/trinacria_items_check.py check docs/MODULO_3/3.10_STRUMENTI_1-180.json '
            'docs/MODULO_3/3.11_STRUMENTI_181-360.json docs/MODULO_3/3.12_STRUMENTI_361-536.json --repo '
            'F:/Progetti/pokeheartgold --completo → STRUMENTI_OK; poi python -I tools/trinacria_glossary_check.py '
            'glossary docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json docs/MODULO_3/3.1_POKEMON_1-100.json … '
            'docs/MODULO_3/3.12_STRUMENTI_361-536.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.12/gen312.py (contenuti in content312.py, parti fisse in '
            'text312.py), copia del generatore del 3.11.',
        ],
        'regole': {
            'R-STR-01…15': 'Valgono come nei blocchi 3.10 e 3.11. In questo intervallo hanno un nome italiano della '
                           'trama (R-STR-01) l’Amuleto, i 9 Atti e i 9 Faldoni (R-STR-18), oltre alle sigle delle MT e '
                           'delle MN (R-STR-11).',
            'R-STR-02': 'Slot vuoti (estende quella del 3.10). Anche lo strumento 428 (ITEM_EXPLORER_KIT) punta a '
                        'item_data_0000 e ha «???» nei banchi: resta vuoto come gli slot 113–134. Lo strumento di '
                        'controllo lo tiene in EMPTY_SLOTS.',
            'R-STR-16': 'MN. Le MN seguono l’ordine di HeartGold (sTMHMMoves): MN01 Roncigghiu, MN02 Passaggiu, MN03 '
                        'Aliscafu, MN04 Spallata, MN05 Garòfalu, MN06 Martiddata, MN07 Ciumara, MN08 Acchianata '
                        '(deviazione D-22: le note del Glossario 3.0 v1.1 dicevano «MN 5» Martiddata e «MN 6» '
                        'Garòfalu; il 3.0 v1.2 le corregge). Ogni MN si riceve col Dossier che ne sblocca l’uso fuori '
                        'dalla lotta (tabella R-03 della trama); il Dossier 6 non dà MN.',
            'R-STR-17': 'Strumenti che non si ottengono. Gli strumenti chiave di Sinnoh e di HeartGold che la trama non '
                        'usa (missioni, chiavi, consegne, programmi radio, sale giochi, gare, Pokéathlon, Parco Amici) '
                        'hanno nome e descrizione ma nessuno script li dà: «altro» comincia con «Non si ottiene in '
                        'Trinacria (R-STR-17)» e dice perché. Il Modulo 6 non li mette in nessuna mappa.',
            'R-STR-18': 'Strumenti chiave della trama. L’Amuleto (ST-12) sta sullo slot dell’Old Charm (439). Gli Atti '
                        '(ST-02) e i faldoni (ST-07) sono uno per provincia, col nome italiano della trama e la sigla '
                        'della provincia («Atto CT», «Faldone CT»; plurali «Atti CT», «Faldoni CT»), su slot di '
                        'strumenti chiave di Sinnoh con fieldUseFunc 0, senza script né codice in HeartGold: Atti '
                        '429, 430, 436, 438, 440, 441, 451, 452, 454 (CT, SR, RG, CL, AG, TP, ME, PA, EN), faldoni 457, '
                        '459, 460, 461, 462, 463, 467, 473, 533. Lo strumento di controllo li ha in ATTI, FALDONI e '
                        'TRAMA_IT. Lo script che dà un Atto o un faldone fa anche VAR_ST_02 o VAR_ST_07 +1 (registro '
                        '2.4). Le icone sono quelle degli slot di Sinnoh: il Modulo 4 può ridisegnarle.',
            'R-STR-19': 'Pirazzi e Ball artigianali. Le Ghicocche di HeartGold diventano i «Pirazzi» (perastri) coi '
                        'colori delle famiglie Zufulu- e Cocciu- del 3.10; la Cascitta (468) li tiene. Il maestro '
                        'ceramista di Caltagirone, quello che aspetta in cima alla Scalinata di S-CT-07, fa la parte '
                        'di Kurt: alla fine di S-CT-07 dà la Cascitta e un PirazzuRussu, poi trasforma un Pirazzu in '
                        'una Ball al giorno (Russu → ScaluniBall, Giarnu → LunaBall, Blu → IscaBall, Virdi → '
                        'CumpariBall, Rosa → ZitaBall, Jancu → CurriBall, Niuru → PisantiBall). Le piante dei Pirazzi '
                        'sono nelle province scritte in «altro». È un’aggiunta alla trama come quelle di R-10.7.',
            'R-STR-20': 'Famiglie nuove (continuano R-STR-08 e R-STR-15). «Canna-» per le canne (Cannuzza, CannaBona, '
                        'Cannazza: diminutivo e accrescitivo, deviazione D-21), «Pirazzu-» per le Ghicocche, '
                        '«Campana-» per le campane, «Pinna-» per le piume dei leggendari, «Scatula-» per le scatole, '
                        '«Chiavi-» per le chiavi, «Cartedda01…27» per le 27 schede del Pokéathlon (non si ottengono). '
                        'Le Ball artigianali continuano «-Ball»; le sfere di Hoenn continuano «Sfera-».',
        },
        'deviazioni_dalle_specifiche': dev,
        'strumenti': strumenti,
        'glossario_aggiunte': agg,
        'mt_e_mn': {
            'spiegazione': 'Le 59 MT e le 8 MN del blocco con la mossa insegnata e come si ottengono (R-STR-11, '
                           'R-STR-16).',
            'elenco': [{'n': e['n'], 'nome': e['nome'], 'mossa': e['mossa'], 'negozi': [x.get('mappa') for x in
                        e['ottenimento']['negozi']], 'altro': e['ottenimento']['altro']} for e in mt],
        },
        'strumenti_chiave_della_trama': {
            'spiegazione': 'Gli strumenti di questo blocco che la trama o le sue aggiunte usano, con la sottotrama o la '
                           'missione che li dà (dettagli in «ottenimento.altro»).',
            'elenco': [{'gruppo': g, 'strumenti': [{'n': n, 'nome': per_n[n]['nome']} for n in ns], 'trama': t}
                       for g, ns, t in chiave],
        },
        'parole_di_sistema_nelle_descrizioni': {
            'spiegazione': 'Numeri degli strumenti di questo blocco la cui descrizione usa la parola. Se il 3.13 cambia '
                           'una di queste parole, dà anche le descrizioni da riscrivere (R-MOS-09, R-STR-04). Per le MT '
                           'e le MN la descrizione viene dalla mossa: si riscrive la mossa e la MT si rigenera '
                           '(R-STR-11).',
            'parole': parole(strumenti),
        },
        'riepilogo_strumenti_1_536': dict(c['riepilogo'], spiegazione=(
            'I blocchi 3.10–3.12 insieme: ogni slot 1–536 una volta sola, nomi tutti diversi (S09 con --completo).')),
        'note_per_blocchi_successivi': [
            '3.0 v1.2: le note di Martiddata (G30-0041) e Garòfalu (G30-0042) dicono ora MN06 e MN05 (D-22).',
            '3.13: le parole di «parole_di_sistema_nelle_descrizioni» dei blocchi 3.10–3.12 restano coi nomi italiani '
            'ufficiali o il 3.13 dà le descrizioni da riscrivere; qui si aggiungono «Punti Lotta», «Poké Ball», '
            '«Codici Amico», «Pokédex» e «Scheda Allenatore».',
            'Modulo 4: le icone degli slot di Sinnoh usati da Atti, faldoni e Amuleto (R-STR-18) si possono '
            'ridisegnare; il Ciauraturi (471) è il fiutatore che la trama chiama «Pokégear» in ST-07.',
            'Modulo 6: premi e regali scritti in «altro» (canne, SH Scassatu, Atti, faldoni, Amuleto, Ciauraturi, '
            'Grasta e Sbrizzaturi, Taccuinu, Rigistraturi, Scartafazzu, Ciucculatta ×5), le MN coi Dossier (R-STR-16), '
            'le MT a terra e nascoste coi pool provinciali, le piante dei Pirazzi e il maestro ceramista di '
            'Caltagirone (R-STR-19), i ricordi dei leggendari accanto agli statici del post-game. Nessuno script dà '
            'gli strumenti di R-STR-17.',
            'Trama: R-STR-19 (Pirazzi e Ball artigianali dal maestro ceramista di Caltagirone) è un’aggiunta alla '
            'trama; la tabella di R-10.7 la può riportare in una versione successiva.',
        ],
        'strumento': {
            'file': 'tools/trinacria_items_check.py',
            'file_di_prova': 'tools/testdata/strumenti_prova_ko.json',
            'comandi': ['--selftest → SELFTEST_OK', 'check <blocchi> [--repo <pokeheartgold>] [--docs <docs>] [--completo] → STRUMENTI_OK'],
            'cambiamenti': {
                'EMPTY_SLOTS': 'gli slot 113–134 e 428 (R-STR-02)',
                'ATTI, FALDONI, TRAMA_IT': 'gli slot degli Atti e dei faldoni e i nomi italiani della trama (R-STR-18)',
                'S09': 'con --completo: i blocchi 3.10–3.12 coprono 1–536 una volta sola, nomi tutti diversi',
            },
            'collaudo': 'i blocchi 3.10, 3.11 e 3.12 insieme senza errori, anche con --completo (il selftest lo attiva '
                        'quando ci sono tutti e tre); strumenti_prova_ko.json con gli errori attesi del suo campo '
                        '«errori_attesi».',
        },
        'controllo': {
            'strumenti': c['strumenti'],
            'slot_vuoti': c['vuoti'],
            'nomi_siciliani_nuovi': c['nuovi'],
            'nomi_nuovi_per_fonte': {'MCP': c['mcp'], 'architetto': c['arch']},
            'nomi_mcp': mcp,
            'nomi_dal_glossario_3_0': c['g30'],
            'nomi_italiani_della_trama': c['it'],
            'mt_con_sigla': c['mt'],
            'mn_con_sigla': c['mn'],
            'nome_piu_largo_px': c['maxnome'],
            'con_articolo_piu_largo_px': c['maxart'],
            'plurale_piu_largo_px': c['maxplur'],
            'righe_di_descrizione': c['righe'],
            'riga_di_descrizione_piu_larga_px': c['maxpx'],
            'strumenti_che_si_comprano': c['venduti'],
            'strumenti_tenuti_dai_selvatici': c['selvatici'],
            'strumenti_che_non_si_ottengono': c['non_ottenibili'],
            'deviazioni': [d['id'] for d in dev],
            'verifiche_superate': ['trinacria_items_check.py check 3.10 3.11 3.12 --repo --completo → STRUMENTI_OK',
                                   'trinacria_glossary_check.py glossary (3.0 + 3.1–3.12) → GLOSSARY_OK',
                                   'trinacria_items_check.py --selftest → SELFTEST_OK'],
        },
    }
    r = c['riepilogo']
    riga = ('BLOCCO COMPLETO: 3.12 — %d strumenti (%d nomi siciliani nuovi: MCP %d, architetto %d; %d MT e %d MN con '
            'la sigla italiana; %d nomi italiani della trama: Amuleto, 9 Atti, 9 Faldoni; 1 slot vuoto), %d '
            'descrizioni D-03 (%d righe, la più larga %d px), nomi entro 72 px, con l’articolo entro 90 px, plurali '
            'entro 82 px; %d strumenti in vendita, %d che non si ottengono (R-STR-17); deviazioni D-21 (canne) e D-22 '
            '(MN05/MN06); strumenti 1–536 completi (%d nomi distinti, %d nomi siciliani nuovi nei blocchi 3.10–3.12) '
            '→ STRUMENTI_OK con --completo') % (
        c['strumenti'], c['nuovi'], c['mcp'], c['arch'], c['mt'], c['mn'], c['it'], c['strumenti'] - c['vuoti'],
        c['righe'], c['maxpx'], c['venduti'], c['non_ottenibili'], r['nomi_distinti'], r['nomi_siciliani_nuovi'])
    blocco['riga_finale'] = riga
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(riga)

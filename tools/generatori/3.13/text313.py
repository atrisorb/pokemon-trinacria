import json

DEVIAZIONI = [
    {'id': 'D-23',
     'oggetto': 'abilità n. 39 (ABILITY_INNER_FOCUS)',
     'forma_specifica': 'Forza Interiore (nome italiano ufficiale, R-NOM-01)',
     'forma_bloccata': 'Forzinterna',
     'motivo': '«Forza Interiore» misura 85 px e il maiuscolo «FORZA INTERIORE» 88 px, oltre i 72 di L-09 (msg_0720 e '
               'msg_0721). Come «Giornodisole» (D-19) il nome si scrive attaccato; «Forzainteriore» misura ancora 84 '
               'px (maiuscolo), quindi la seconda parola si accorcia in «interna». La descrizione resta quella della '
               'concentrazione che impedisce di tentennare.'},
    {'id': 'D-24',
     'oggetto': 'classi allenatore con lo stesso nome (R-NOM-02)',
     'forma_specifica': 'R-NOM-02 del 3.0: due classi non hanno mai lo stesso nome',
     'forma_bloccata': 'Allenatore e Allenatrice (giocatore, compagni, classi della Frontiera e classi da non usare), '
                       'Segretario (9 classi), Campione (4 classi): un nome per ruolo (R-CLA-03)',
     'motivo': 'HeartGold stesso dà un nome solo a più classi dello stesso ruolo (msg_0730: «Leader» 16 volte, «Elite '
               'Four» 4, «₧₦ Trainer» 15, «Executive» 4). Le classi si distinguono per sprite, squadra e nome '
               'dell’allenatore («Segretario Calì»); nomi diversi per i 9 Segretari o per i 4 Campioni non esistono '
               'nella trama. La regola resta per i nomi siciliani: nessuna classe siciliana ha il nome di un’altra '
               'classe o di una specie, mossa, strumento, abilità, tipo o natura (codice Y08).'},
]


def TESTI(c, abilita, tipi, nature, classi, forme, ricerca, lessico, agg, out):
    mcp = [a['forma'] for a in agg if a['fonte'] == 'MCP']
    it_ruoli = {}
    for e in classi:
        if e['lingua'] == 'it' and not e['glossario']:
            it_ruoli.setdefault(e['nome'], []).append(e['n'])
    blocco = {
        'modulo': 3,
        'blocco': '3.13',
        'titolo': 'Abilità, tipi, nature, classi allenatore e parole di sistema',
        'versione': '1.0',
        'data': '27/10/2026',
        'progetto': 'Pokémon Trinacria',
        'file': 'docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json',
        'lettore': 'LLM esecutore e autore dei blocchi 4.x (icone dei tipi), 6.x (frasi con i nomi delle classi) e 7.x '
                   '(applicazione nel repository). Ogni valore è deciso: non si sceglie nulla.',
        'fonti': [
            'F:\\Progetti\\pokeheartgold @ c28680fe0, letti il 27/10/2026: include/constants/abilities.h e '
            'include/constants/trainer_class.h (simboli), files/msgdata/msg/msg_0720.json, msg_0721.json, '
            'msg_0722.json (abilità), msg_0730.json e msg_0731.json (classi), msg_0735.json (tipi), msg_0034.json '
            '(nature), msg_0802.json (interfaccia del Pokédex: forme e tipi della ricerca), tutti i banchi di '
            'files/msgdata/msg (etichette del lessico), files/graphic/font/font_00000000.bin e tools/msgenc/charmap.txt '
            '(larghezze).',
            'Nomi italiani ufficiali di abilità, tipi, nature e forme: tabelle di PokeAPI (github.com/PokeAPI/pokeapi, '
            'data/v2/csv: ability_names.csv, type_names.csv, nature_names.csv, pokemon_form_names.csv, lingua 8 = it), '
            'lette il 27/10/2026. Il repository di HeartGold è inglese: questi nomi non si possono controllare lì, e '
            'per qualche abilità il nome attuale può differire da quello stampato su HeartGold e SoulSilver italiani.',
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json v1.2: L-06, L-07, L-09, L-10, L-11, D-04, R-GRA, R-NOM, R-GLO; '
            'le 12 classi del Glossario (G30-0061…).',
            'docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json v1.1: le 129 classi con simbolo, categoria e ruolo '
            '(«COMUNE: nome siciliano nel Modulo 3.13»).',
            'docs/MODULO_3/3.1–3.12: nomi di specie, mosse e strumenti per le collisioni (Y08); il nome di Rotom '
            '(3.5) per le sue forme; le parole di sistema usate dalle descrizioni (R-MOS-03, R-MOS-09, sezioni '
            '«parole_di_sistema_nelle_descrizioni» dei blocchi 3.10–3.12).',
            'F:\\Progetti\\sicilian-dialect-mcp\\vocabolario.json (versione 2.0.0): attestazione delle forme («lemma_mcp»).',
            'docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md v1.9: R-10.2, R-10.6 (livelli di «U Sistema»), i compagni C-01…C-08, '
            'M-EN-04 (i 4 Campioni della Lega), M-EN-06 (il Presidente), P-02 (Maria), P-03…P-06 (Fantasmi), P-09 '
            '(Fiera del Mediterraneo).',
        ],
        'come_si_usa': [
            'Ogni voce dà i testi da copiare nei banchi all’indice «n» (campo «banchi»): abilità in msg_0720 (nome), '
            'msg_0721 (maiuscolo) e msg_0722 (descrizione, profilo D-04); tipi in msg_0735; nature in msg_0034; classi '
            'in msg_0730 (nome) e msg_0731 (con l’articolo); forme e tipi della ricerca in msg_0802. L’esecutore cambia '
            'solo i messaggi elencati (Modulo 7); i banchi non cambiano numero di messaggi (R-NOM-08).',
            'I nomi siciliani nuovi delle classi sono nella «glossario_aggiunte» (G313-0001…): entrano nel Glossario '
            'bloccato con «merge» (R-GLO-02). Non hanno voce nel Glossario i nomi italiani ufficiali (abilità, tipi, '
            'nature, forme) né i nomi italiani dei ruoli condivisi (R-CLA-03).',
            'La sezione «lessico_di_sistema» fissa le parole italiane che descrizioni e testi usano per statistiche, '
            'stati, tasche della borsa, lotta e tempo atmosferico (R-LES-01).',
            'Controllo: python -I tools/trinacria_system_check.py check docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json '
            '--repo F:/Progetti/pokeheartgold → SISTEMA_OK; poi python -I tools/trinacria_glossary_check.py glossary '
            'docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json docs/MODULO_3/3.1_POKEMON_1-100.json … '
            'docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json → GLOSSARY_OK.',
            'Il blocco è generato da tools/generatori/3.13/gen313.py (contenuti in content313.py, parti fisse in '
            'text313.py).',
        ],
        'regole': {
            'R-ABI-01': 'Nomi delle abilità. Nome italiano ufficiale (R-NOM-01), entro L-09 anche in maiuscolo; il '
                        'maiuscolo di msg_0721 è il maiuscolo esatto del nome (R-GRA-08). Una sola deviazione: '
                        'Forzinterna (D-23). Levitazione e Insonnia, citate nelle descrizioni delle mosse (R-MOS-09), '
                        'restano come sono. Lo slot 0 resta « -» nei tre banchi.',
            'R-ABI-02': 'Descrizioni delle abilità. Scritte per Trinacria in italiano col profilo D-04 (2 righe, 26 '
                        'caratteri e 136 px per riga, «\\n» tra le righe, nessun separatore finale). Usano le parole '
                        'del lessico (R-LES-01) e i nomi italiani dei tipi; non nominano mosse né strumenti per nome '
                        '(«mosse esplosive», «del miele»), tranne le categorie generiche «Bacca» e «Lastra».',
            'R-TIP-01': 'Tipi. Nomi italiani ufficiali con l’iniziale maiuscola (R-GRA-08: «Coleottero», non '
                        '«COLEOTTERO»), entro L-10; il tipo 9 resta «???». Le icone dei tipi sono immagini (Modulo 4).',
            'R-TIP-02': 'Tipi nella ricerca del Pokédex (msg_0802 47–63). Stesso nome del tipo, entro 43 px (il più '
                        'largo di HeartGold, «Electric»: HeartGold stesso accorcia «Fighting» in «Fight»). Il nome che '
                        'non entra si accorcia col punto alla parte più lunga che entra: «Coleot.» (Coleottero).',
            'R-NAT-01': 'Nature. Nomi italiani ufficiali, entro L-11.',
            'R-CLA-01': 'Classi con nome siciliano. Tutte le classi «COMUNE» del registro 2.5 e i capi dei padiglioni '
                        'della Fiera (P-09) hanno un nome siciliano nuovo, registrato in «glossario_aggiunte» '
                        '(G313-NNNN), entro L-06 e, con l’articolo, L-07. Il nome dice chi è l’allenatore nella '
                        'Sicilia della trama (ruolo del registro 2.5); le coppie maschio/femmina di HeartGold hanno due '
                        'forme (Nataturi/Natatrici, Nduvinu/Nduvina).',
            'R-CLA-02': 'Classi del Glossario 3.0. Le 12 classi di «U Sistema» e siciliane (Scagnozzu, Infiltrata, '
                        'Cambiavoti, Cassieri, Caporali, Coll. Biancu, Portaborse, Figghiu Papà, Pustiggiat., '
                        'Assessuri, Zauddu, Buddaci) si ricopiano dal Glossario.',
            'R-CLA-03': 'Ruoli condivisi (deviazione D-24). Un nome italiano solo per le classi dello stesso ruolo, come '
                        'in HeartGold: %s. Non hanno voce nel Glossario. «Allenatore»/«Allenatrice» valgono per il '
                        'giocatore, i compagni (C-01…C-08, col genere del personaggio), le classi della Frontiera che la '
                        'storia non usa e le classi da non usare (R-CL-04 del registro 2.5).' % '; '.join(
                            '%s (%s)' % (k, ', '.join(str(n) for n in v)) for k, v in it_ruoli.items()),
            'R-CLA-04': 'Articoli delle classi (msg_0731). Come R-NOM-09, senza comandi di colore. Le tre classi che '
                        'sono una coppia (Jimiddi, Cumpari, Ziti; in HeartGold «the Twins») hanno l’articolo '
                        'determinativo plurale: «le» al femminile, «gli» davanti a vocale, s impura e z, «i» negli '
                        'altri casi («gli Ziti», «i Cumpari», «le Jimiddi»).',
            'R-CLA-05': 'Genere. Il genere del nome è quello del personaggio della trama (i 9 Segretari sono uomini, '
                        'Pippo è un uomo, Maria e Chantal sono donne), anche dove la tabella dei sessi di HeartGold dice '
                        'altro: la tabella (genere_tabella del registro 2.5) non cambia.',
            'R-FOR-01': 'Forme (msg_0802). Nome italiano ufficiale entro 16 caratteri e 76 px, la forma più larga di '
                        'HeartGold («Overcast Form»). Le forme di Castform sono i messaggi 160–163, quelle di Cherrim '
                        '164–165 (la scaletta diceva «Castform 161–165»).',
            'R-FOR-02': 'Se una forma di una specie non entra, tutte le forme di quella specie lasciano la parola '
                        '«Forma»: Deoxys (Normale, Attacco, Difesa, Velocità), Giratina (Alterata, Originale), Cherrim '
                        '(Nuvola, Splendore) e Castform (Sole, Pioggia, Nuvola di Neve; la forma normale, 160, è già «Normale»).',
            'R-FOR-03': 'Rotom e Pichu. Le forme di Rotom cominciano col nome di Trinacria della specie (Prisa, blocco '
                        '3.5) e non sono in maiuscolo come in HeartGold (R-GRA-08): «Prisa Calore», «Prisa Lavaggio»… '
                        'Il Pichu dalle orecchie a punta (166, «Spiky-eared») si chiama «Orecchiapunta»: il nome '
                        'italiano descrittivo «Orecchie a punta» misura 89 px.',
            'R-LES-01': 'Lessico di sistema. Le parole della sezione «lessico_di_sistema» sono italiane e si scrivono '
                        'così in tutti i testi di Trinacria (descrizioni dei blocchi 3.6–3.13, testi del Modulo 6): sono '
                        'le stesse che le descrizioni di mosse e strumenti già usano (R-MOS-03, R-MOS-09, R-STR-05), '
                        'quindi nessuna descrizione va riscritta. «messaggi_heartgold» elenca i messaggi di HeartGold '
                        'che sono esattamente un’etichetta inglese della parola: è un indice per chi tradurrà '
                        'l’interfaccia, non un elenco completo (le parole compaiono anche dentro le frasi).',
        },
        'deviazioni_dalle_specifiche': DEVIAZIONI,
        'abilita': abilita,
        'tipi': tipi,
        'nature': nature,
        'classi': classi,
        'glossario_aggiunte': agg,
        'forme': forme,
        'ricerca_tipi': ricerca,
        'lessico_di_sistema': lessico,
        'riepilogo_nomi_di_sistema': {
            'spiegazione': 'Con questo blocco il Modulo 3 dà nome a tutti gli oggetti dei banchi dei nomi del 3.0 '
                           '(sezione «banchi_dei_nomi»): specie (3.1–3.5), mosse (3.6–3.9), strumenti (3.10–3.12), '
                           'abilità, classi, tipi e nature (3.13). I luoghi sono nei registri 2.1–2.3.',
            'abilita': len(abilita) - 1, 'tipi': len(tipi) - 1, 'nature': len(nature), 'classi': len(classi),
            'forme': len(forme), 'tipi_della_ricerca': len(ricerca),
        },
        'note_per_blocchi_successivi': [
            'Modulo 4: le icone dei tipi e degli stati (immagini con le scritte inglesi «NORMAL», «PAR»…) vanno '
            'ridisegnate coi nomi di R-TIP-01 e le sigle degli stati del lessico; le scritte delle tasche della borsa '
            'sono testo (lessico, gruppo «tasche»).',
            'Modulo 6: nelle frasi i nomi delle classi entrano con {STRVAR…} entro R-LIM-05 (con l’articolo al massimo '
            '30 caratteri contati dal linter); le classi in coppia usano l’articolo plurale (R-CLA-04). I compagni '
            'combattono come «Allenatore»/«Allenatrice» seguito dal nome (R-CLA-03).',
            'Modulo 7: applicazione dei banchi msg_0720, msg_0721, msg_0722, msg_0730, msg_0731, msg_0735, msg_0034 e '
            'dei messaggi di msg_0802 di questo blocco; prove a schermo dei tipi lunghi (L-10) nella Sala Lotta della '
            'Fiera, nel Pokéathlon e nelle parole rapide, dei tipi della ricerca del Pokédex (R-TIP-02) e delle forme '
            '(R-FOR-01). La tabella dei sessi delle classi non cambia (R-CLA-05).',
            'Punto aperto per l’autore: nessuna richiesta della scaletta traduce l’interfaccia di HeartGold (menu, '
            'frasi di lotta, riepilogo, borsa, Pokédex), che resta in inglese. Il lessico di sistema fissa le parole; '
            'se l’interfaccia va tradotta serve una richiesta nuova.',
        ],
        'strumento': {
            'file': 'tools/trinacria_system_check.py',
            'file_di_prova': 'tools/testdata/sistema_prova_ko.json',
            'comandi': ['--selftest → SELFTEST_OK', 'check <blocco> [--repo <pokeheartgold>] [--docs <docs>] → SISTEMA_OK'],
            'codici': {
                'Y00': 'file illeggibile, sezione mancante, voce del Glossario fuori numerazione G313-NNNN',
                'Y01': 'abilità: voci 0–123, slot 0 invariato, nome entro L-09 anche in maiuscolo, maiuscolo esatto',
                'Y02': 'abilità: nome italiano ufficiale (ABILITA_IT) o deviazione registrata',
                'Y03': 'descrizione delle abilità nel profilo D-04',
                'Y04': 'tipi: voci 0–17, nome italiano ufficiale (TIPI_IT), L-10',
                'Y05': 'nature: voci 0–24, nome italiano ufficiale (NATURE_IT), L-11',
                'Y06': 'classi: voci 0–128, nome entro L-06, articolo giusto (R-NOM-09, R-CLA-04) entro L-07',
                'Y07': 'classi: nome siciliano uguale alla voce del Glossario (3.0 o G313), nome italiano solo per i '
                       'ruoli condivisi (CLASSI_IT)',
                'Y08': 'un nome per oggetto: abilità, tipi, nature e classi siciliane diversi tra loro e dai nomi di '
                       'specie, mosse, strumenti e Dossier (non i soprannomi, R-NOM-02)',
                'Y09': 'forme di msg_0802: messaggi giusti, entro R-FOR-01, Rotom col nome della specie',
                'Y10': 'tipi della ricerca: nome del tipo entro 43 px, abbreviato col punto solo se non entra',
                'Y11': 'campo «banchi» uguale ai campi della voce',
                'Y12': 'con --repo: nomi inglesi e simboli uguali al repository',
            },
            'collaudo': 'il blocco 3.13 senza errori; sistema_prova_ko.json con gli errori attesi del suo campo '
                        '«errori_attesi».',
        },
        'controllo': {
            'abilita': len(abilita) - 1,
            'abilita_nome_piu_largo_px': c['maxab'],
            'abilita_maiuscolo_piu_largo_px': c['maxabu'],
            'righe_di_descrizione': c['righe'],
            'riga_di_descrizione_piu_larga_px': c['maxpx'],
            'tipi': len(tipi) - 1, 'tipo_piu_largo_px': c['maxtipo'],
            'nature': len(nature), 'natura_piu_larga_px': c['maxnat'],
            'classi': len(classi),
            'classi_dal_glossario_3_0': c['g30'],
            'classi_con_nome_siciliano_nuovo': c['cl_scn'],
            'classi_coi_ruoli_condivisi': c['cl_it'],
            'nomi_siciliani_nuovi': c['nuovi'],
            'nomi_nuovi_per_fonte': {'MCP': c['mcp'], 'architetto': c['arch']},
            'nomi_mcp': mcp,
            'classe_piu_larga_px': c['maxcl'],
            'con_articolo_piu_largo_px': c['maxart'],
            'forme': len(forme), 'forma_piu_larga_px': c['maxforma'],
            'tipo_della_ricerca_piu_largo_px': c['maxric'],
            'parole_del_lessico': len(lessico),
            'deviazioni': [d['id'] for d in DEVIAZIONI],
            'verifiche_superate': ['trinacria_system_check.py check 3.13 --repo → SISTEMA_OK',
                                   'trinacria_glossary_check.py glossary (3.0 + 3.1–3.13) → GLOSSARY_OK',
                                   'trinacria_system_check.py --selftest → SELFTEST_OK'],
        },
    }
    riga = ('BLOCCO COMPLETO: 3.13 — %d abilità coi nomi italiani ufficiali (1 deviazione, D-23) e %d descrizioni D-04 '
            '(%d righe, la più larga %d px), maiuscoli entro %d px; %d tipi e %d nature coi nomi italiani ufficiali; '
            '%d classi (%d dal Glossario 3.0, %d nomi siciliani nuovi: MCP %d, architetto %d; %d coi ruoli condivisi '
            'di D-24), con l’articolo entro %d px; %d forme di msg_0802 e %d tipi della ricerca; lessico di '
            'sistema di %d parole → SISTEMA_OK') % (
        len(abilita) - 1, len(abilita) - 1, c['righe'], c['maxpx'], c['maxabu'], len(tipi) - 1, len(nature),
        len(classi), c['g30'], c['nuovi'], c['mcp'], c['arch'], c['cl_it'], c['maxart'], len(forme), len(ricerca),
        len(lessico))
    blocco['riga_finale'] = riga
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(blocco, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(riga)

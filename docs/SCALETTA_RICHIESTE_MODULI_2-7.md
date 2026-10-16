# Scaletta delle richieste per i Moduli 2–7

**Versione:** 1.2 · 16/10/2026
**Come si usa:** invia le richieste **una alla volta, nell'ordine**. Ogni richiesta produce **un file** (o un blocco di un file) in `F:\Progetti\pokémon-sicilia\docs\` e finisce con una riga di controllo `BLOCCO COMPLETO: <id> — <conteggi>`. Se la riga manca, il blocco è stato troncato: invia `Continua il blocco <id> dal punto esatto in cui si è interrotto, senza ripetere nulla.`

Ogni blocco scritto a mano è dimensionato per stare in una sola risposta senza riassumere (circa 60–90 KB di testo). Il testo da incollare è nella colonna «Richiesta». I registri del Modulo 2 si possono **generare con uno script** che legge il repository e controlla la coerenza: in quel caso il limite non vale (il blocco 2.1 pesa circa 540 KB perché ogni mappa contiene l'intestazione completa) e la riga `BLOCCO COMPLETO` resta obbligatoria.

## Stato

| Blocco | Stato | Riga di controllo |
|---|---|---|
| 2.1 | consegnato il 15/10/2026 (allineato a v1.1 il 16/10/2026 per R-10) | `BLOCCO COMPLETO: 2.1 — 119 mappe (CT 53, SR 42, RG 24; 46 esterne, 73 interne), 104 gemelli msg_0830–msg_0933, 34 matrici nuove 0288–0321, 64 MAPSEC, 10 punti di volo, 33 musiche` |
| 2.2 | prossima richiesta | — |

Il blocco 2.1 e la versione 1.2 della trama (`00_TRAMA_ESPANSA_E_SIDEQUEST.md`) hanno fissato decisioni vincolanti per tutti i blocchi successivi: sezione `piano_globale` del registro 2.1, decisione **R-09** (come i luoghi diventano mappe) e decisione **R-10** (centralità biopolitica dei Pokémon e architettura di **«U Sistema»**, la mafia siciliana a 4 livelli che sostituisce il Team Rocket compiendo 10 operazioni inedite coi Pokémon). Sono riassunte nelle righe delle tabelle qui sotto.

## Ordine e dipendenze

```
Modulo 2 (ID) ──► Modulo 3 (nomi) ──► Modulo 5 (audio) ──► Modulo 4 (grafica) ──► Modulo 6 (script e dialoghi) ──► Modulo 7 (runbook)
     │                                                                                                         ▲
     └──────────────── i ticket del Modulo 1 (M1-01…M1-16) si possono già eseguire ────────────────────────────┘
```

Il Modulo 1 (`MODULO_1_INFRASTRUCTURE_AND_ENGINE_SPEC.md`) è già eseguibile: puoi far partire l'esecutore sui passi M1-01…M1-16 mentre produciamo i moduli successivi.

---

## Modulo 2 — `GLOBAL_CONSTANTS_REGISTRY.json` (5 richieste)

| ID | Richiesta da incollare | File prodotto | Contenuto e controllo |
|---|---|---|---|
| 2.1 ✅ | `Genera il blocco 2.1 del Modulo 2: registro delle mappe di CT, SR e RG.` | `docs/MODULO_2/2.1_MAPS_CT_SR_RG.json` | Per ogni mappa: simbolo `MAP_*`, ID numerico (riuso di uno slot di `include/constants/maps.h` di HeartGold, con il simbolo HG sostituito), matrice, banco script, banco testi + gemello post, meteo, musica `SEQ_*`, sezione del Pokégear, punto di volo, missioni della trama (allineate a R-10), confini percorribili, intestazione completa (28 campi). Interni ed esterni. Più il `piano_globale` per i blocchi successivi. **Consegnato e aggiornato a v1.1.** |
| 2.2 | `Genera il blocco 2.2 del Modulo 2: registro delle mappe di CL, AG e TP.` | `docs/MODULO_2/2.2_MAPS_CL_AG_TP.json` | come 2.1, dentro il `piano_globale` del 2.1: solo gli slot di `slot.riservati_2_2` (al massimo 148), solo le celle `l`, `a`, `t` della matrice 0; numerazione da `msg_0934`, `map_matrix_0322`, MAPSEC 66, `scr_seq_0965`, `zone_event` 491; punti di volo, righe di volo e righe di spawn solo tra quelli liberi; regole R-MAP-01…21 del 2.1 e R-09/R-10 della trama (incluso `followMode` per il Pokémon a seguito e le note sulle operazioni di «U Sistema» in `contenuti_trama`). Regione del Pokégear: `MAP_REGION_JOHTO` per le celle in colonna < 24. |
| 2.3 | `Genera il blocco 2.3 del Modulo 2: registro delle mappe di ME, PA, EN, strade, dungeon trasversali e post-game.` | `docs/MODULO_2/2.3_MAPS_ME_PA_EN_ROADS.json` | come 2.2, con gli slot di `slot.riservati_2_3` (al massimo 207; gli slot con un «ruolo» si usano per quel ruolo), le celle `m`, `p`, `e` e la numerazione che riprende dopo il 2.2. Completa le 10 strade già prenotate con simbolo e celle (`MAP_STRADA_*` in `strade_riservate`) e aggiunge i tratti ancora mancanti di A18, A19, A20, A29, SS114, SS115, SS121, SS640, SS284, i dungeon trasversali e Pantelleria. Totale: 66 esclusi + 119 + 148 + 207 = 540 slot (limite di HeartGold). |
| 2.4 | `Genera il blocco 2.4 del Modulo 2: FLAG, VAR, registro NPC e strumento di controllo.` | `docs/MODULO_2/2.4_FLAGS_VARS.json` + `tools/trinacria_registry_check.py` | Tutti i flag (0x840–0x95F, poi intervallo storico) e le variabili (0x405B–0x406F, 0x4152–0x416F) dei codici M/S/D/B/E/C/P della trama; schema e regole di `npc_registry.csv` (inclusi gli sprite overworld dei Pokémon di presidio o di lavoro accanto agli NPC); controllo 60/40. Lo strumento è collaudato su un CSV di prova. |
| 2.5 | `Genera il blocco 2.5 del Modulo 2: classi allenatore, ID allenatori, sprite, punti di volo, medaglie e sequenze musicali.` | `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json` | `TRAINER_CLASS_*`: riuso degli slot HG con i nomi siciliani delle specifiche (`FigghiuDiPapà`, `Parcheggiaturi`, `Assessuri`, `Zauddu`, `Buddaci`…) e rimappatura integrale degli slot del Team Rocket (`TEAM_ROCKET`, `TEAM_ROCKET_F`, `EXECUTIVE_ARCHER/ARIANA/PETREL/PROTON`) sui **4 livelli di «U Sistema»** (`Scagnozzu`, `Cambiavoti`, `Caporali`, `CollettuBian.`, `Cassieri`, `Infiltrata` — decisione R-10.6); mappa ID allenatori 1–737 per provincia, `SPRITE_*` degli NPC e dei Pokémon overworld, `FLYPOINT_*` riusati, slot medaglie dei 9 Dossier, elenco `SEQ_*` (inclusi i 3 slot musicali Rocket rimappati su «U Sistema»). I punti di volo, le musiche `SEQ_*` e le righe delle tabelle di volo e spawn già assegnati dai blocchi 2.1–2.3 si ricopiano senza cambiarli. |

## Modulo 3 — `SICILIAN_DEX_MOVES_ITEMS_DB.json` (14 richieste)

| ID | Richiesta | File | Contenuto |
|---|---|---|---|
| 3.0 | `Genera il blocco 3.0 del Modulo 3: limiti dei buffer, regole di nomenclatura e Glossario bloccato (prima parte).` | `docs/MODULO_3/3.0_REGOLE_E_GLOSSARIO.json` + `tools/trinacria_glossary_check.py` | Limiti di caratteri misurati nel sorgente (nomi Pokémon, mosse, strumenti, abilità, classi), regole di grafia, Glossario bloccato con forma unica e area per ogni parola siciliana usata nei nomi (inclusi i termini di R-10). |
| 3.1–3.5 | `Genera il blocco 3.N del Modulo 3: Pokémon da #A a #B.` con 3.1 = 1–100, 3.2 = 101–200, 3.3 = 201–300, 3.4 = 301–400, 3.5 = 401–493 | `docs/MODULO_3/3.N_POKEMON_A-B.json` | Per ogni specie: ID, nome originale, nome siciliano (entro il limite o con l'estensione del buffer indicata), categoria, **descrizione del Pokédex scritta nella voce del Prof. Alfio Strano («Atlante Biopolitico della Trinacria», R-10.5: ecologia siciliana + come la specie interagisce con il territorio o viene sfruttata da «U Sistema»)** già formattata, distribuzione comune per comune (mappa, metodo, livelli, rarità, ora del giorno). |
| 3.6–3.9 | `Genera il blocco 3.N del Modulo 3: mosse da #A a #B.` con 3.6 = 1–120, 3.7 = 121–240, 3.8 = 241–360, 3.9 = 361–467 | `docs/MODULO_3/3.N_MOSSE_A-B.json` | ID, nome originale, nome siciliano, descrizione formattata; le MN civiche con i nomi delle specifiche (`Martiddata`, `Roncigghiu`, `Spallata`, `Aliscafu`, `Passaggiu`… R-03 e R-10.4), le mosse chiave del Sistema (`Pizzu`, `Curtigghiu`, `Scussuni`, `Sorbacqua`…) e `RinaDiL’Etna`. |
| 3.10–3.12 | `Genera il blocco 3.N del Modulo 3: strumenti da #A a #B.` con 3.10 = 1–180, 3.11 = 181–360, 3.12 = 361–536 | `docs/MODULO_3/3.N_STRUMENTI_A-B.json` | ID, nome originale, nome siciliano (`SeltzLimoneESale`, `ArancinuSavia`, `CoppulaBall`, `CuffaBall`, `BummuluBall`, `UrnaElettor.`, i 9 `Atti` di ST-02, i 9 `Faldoni` di ST-07…), descrizione, dove si trova o si compra. |
| 3.13 | `Genera il blocco 3.13 del Modulo 3: abilità, tipi, nature, classi allenatore e parole di sistema.` | `docs/MODULO_3/3.13_ABILITA_TIPI_SISTEMA.json` | tutto ciò che resta dei nomi di sistema, incluse le classi di «U Sistema» (R-10.6). |

## Modulo 5 — `AUDIO_SCORE_BLUEPRINTS.md` (4 richieste)

| ID | Richiesta | File | Contenuto |
|---|---|---|---|
| 5.1 | `Genera il blocco 5.1 del Modulo 5: pipeline MIDI→SSEQ, banchi SBNK di HeartGold e SFX da mantenere.` | `docs/MODULO_5/5.1_PIPELINE_E_SFX.md` + script di prova | Strumento di conversione scelto e provato, elenco degli SBNK e degli strumenti usabili, elenco SFX/versi dei Pokémon da mantenere al 100% (usati anche nel minigioco dell'Orecchio di Dionisio `S-SR-02` e negli eventi overworld). L'aggancio `SEQ_*` ↔ mappa è già nei registri del Modulo 2 (sezione `musiche`): ogni brano nuovo **sostituisce i dati di uno slot HeartGold** e del suo gemello `SEQ_GS_P_*`, nessuna sequenza in più. |
| 5.2 | `Genera il blocco 5.2 del Modulo 5: partiture del Prologo e dell'Atto I.` | `docs/MODULO_5/5.2_ATTO_I.md` + `tools/music/*.py` | Script `midiutil` completi (Cubbar techno, Vermut, via Etnea, San Cristoforo, Librino, Etna, Fontanarossa in crisi, Segreteria, lotta allenatore, più i **3 temi di «U Sistema»** che sostituiscono gli slot del Team Rocket: incontro scagnozzo/cambiavoti `SEQ_GS_EYE_ROCKET`, covo/racket `SEQ_GS_R_AJITO`, battaglia contro «U Sistema» `SEQ_GS_BA_ROCKET` — R-10.6). |
| 5.3 | `Genera il blocco 5.3 del Modulo 5: partiture degli Atti II–IV.` | `docs/MODULO_5/5.3_ATTI_II-IV.md` + script | barocco ibleo, Comiso, zolfare, Valle dei Templi, Cretto (vento), Stretto, Nebrodi… |
| 5.4 | `Genera il blocco 5.4 del Modulo 5: partiture dell'Atto V, finale, crediti e post-game.` | `docs/MODULO_5/5.4_ATTO_V_FINALE.md` + script | Capaci (vento e auto), Palermo, Lega, Mistretta, palco, pianoforte e violino in Do minore, post-game (Maria e Fantasmi della Prima Repubblica). |

## Modulo 4 — `GRAPHICS_AND_TILESET_MANIFEST.md` (4 richieste)

| ID | Richiesta | File | Contenuto |
|---|---|---|---|
| 4.1 | `Genera il blocco 4.1 del Modulo 4: inventario degli asset HeartGold, riusi e pipeline grafica.` | `docs/MODULO_4/4.1_INVENTARIO_PIPELINE.md` | percorsi, formati, comandi `nitrogfx`/IMD/`g3dcvtr` provati, regole di palette 555-BGR, inventario degli sprite Pokémon overworld usati per il Follower e per le scene di «U Sistema» nelle mappe. |
| 4.2 | `Genera il blocco 4.2 del Modulo 4: tileset e modelli 3D di CT, SR, RG, CL.` | `docs/MODULO_4/4.2_TILESET_EST.md` + script Pillow | ogni tile in griglia 8×8/16×16 con palette esatta (sacchi di spazzatura attorno ai `Munnizza`, cassonetti bruciati, insegna Cubbar, tavolini di via Gemmellaro, braci di via Plebiscito, Palazzo di Cemento coi cavi d'allaccio abusivo, cenere nera, terminal di Comiso, serbatoi del polo petrolchimico, parabole del MUOS…). Dai registri del Modulo 2: un modello per ogni cella usata della matrice 0 e per ogni stanza delle matrici nuove (2.1: `map_matrix_0288`–`0321`), le voci `AREA-<simbolo>`, la porta del Centro Pokémon alla casella locale (16,19) di ogni città con punto di volo, gli ostacoli lungo i confini non percorribili, le anteprime d'ingresso da sostituire e, se il meteo 9 non mostra nebbia, la tinta gialla di Augusta, Priolo e del polo. |
| 4.3 | `Genera il blocco 4.3 del Modulo 4: tileset e modelli 3D di AG, TP, ME, PA, EN.` | `docs/MODULO_4/4.3_TILESET_OVEST.md` + script | Faraglioni, tubi e saracinesche dell'acquedotto, autobotti abusive, pale eoliche scollegate, Cretto di Burri, steli di Capaci (palette sobria), caselli, pilone dello Stretto, Villa Romana… |
| 4.4 | `Genera il blocco 4.4 del Modulo 4: titolo, copyright atrisorb, Pokégear, sondaggio, sprite nuovi dei personaggi.` | `docs/MODULO_4/4.4_UI_TITOLO_SPRITE.md` + script | `GFX-COPYRIGHT`, `GFX-TITLE-*`, mappa della Sicilia nel Pokégear divisa in due regioni sui due lati del motore (Sicilia orientale = Kanto, colonna ≥ 24; occidentale = Johto: **da confermare qui**), nomi delle due regioni, campi `unk_05`/`unk170*` della tabella del Volo, barra del Consenso, sprite di protagonista, compagni, Mistretta e delle classi di «U Sistema» (al posto delle reclute/esecutivi Rocket, R-10.6). |

## Modulo 6 — `MASTER_SCRIPT_AND_DIALOGUE_BIBLE` (38 richieste)

Ogni blocco: per ogni mappa, coordinate degli NPC (umani e Pokémon overworld presenti nella scena per le operazioni di «U Sistema» o per l'ecologia locale, R-10), script `scr_seq` con le macro reali, banco di campagna e banco gemello post-dimissioni già formattati (36 caratteri, `LINT_OK` garantito con il linter del Modulo 1), squadre complete (specie, soprannome/nome siciliano, livello, 4 mosse coerenti con il racket o il ruolo tematico di R-10.3, strumento, IV), categoria 60/40 di ogni NPC, e testi di interazione col Pokémon a seguito nei luoghi chiave e nei luoghi della memoria (R-10.4). Richiesta tipo: `Genera il blocco 6.NN del Modulo 6.`

Mappe, stanze, file e banchi sono quelli dei registri del Modulo 2: le missioni vanno nella mappa indicata dal campo `contenuti_trama`, i piani e le sale dei dungeon sono stanze della stessa mappa (trama R-09.1), le località «seconda cella» non hanno una mappa propria (R-09.2), le aree della Zona Safari di Vendicari non hanno testi propri, la scala del piano interrato dei Centri Pokémon è un oggetto con il cartello «fuori servizio».

| Blocchi | Contenuto |
|---|---|
| 6.01 | Prologo: Cubbar (Misterbianco) e casa di Corso Italia |
| 6.02 | Catania: via Etnea, via Gemmellaro (Vermut: starter, Atlante del Prof. Strano, primo scagnozzo del Sistema), Piazza Teatro Massimo, Piazza Università |
| 6.03 | Catania: Pescheria, Duomo (comizi col Pokémon sul palco), Castello Ursino, Palazzo degli Elefanti (Segreteria 1: monopolio dei Pokémon curatori) |
| 6.04 | Catania: San Cristoforo e via Plebiscito (pizzo biologico nell'officina); San Giovanni Galermo |
| 6.05 | Catania: Librino e Palazzo di Cemento (allaccio abusivo coi Pokémon Elettro/Acqua); Corso Italia, Lungomare, Ognina |
| 6.06 | Catania: Plaia (Privè Zagara) e Aeroporto di Fontanarossa (crisi della cenere e Pokémon spazzatori bloccati dalla SAC) |
| 6.07 | Misterbianco, Acireale, Aci Castello/Aci Trezza |
| 6.08 | Nicolosi/Etna Sud (biotruffa piromane sui Monti Rossi), Paternò, Adrano |
| 6.09 | Bronte (cartello dell'Oro Verde e sciami Coleottero), Randazzo, Caltagirone |
| 6.10 | SS114, Augusta, Priolo Gargallo, Melilli (inceneritori viventi del polo petrolchimico) |
| 6.11 | Lentini (magazzini occupati), Carlentini, Siracusa (Ortigia, Neapolis, Segreteria 2: blocco portuale) |
| 6.12 | Noto e Vendicari (Zona Safari), Avola, Pachino/Marzamemi (tonnara VIP), Portopalo |
| 6.13 | Ragusa (Superiore, Ibla, Segreteria 3: catena del freddo), Marina di Ragusa |
| 6.14 | Modica (laboratorio-Centro), Scicli, Santa Croce Camerina/Punta Secca |
| 6.15 | Vittoria (mercato all'alba: Pokémon Ghiaccio e spore), Comiso (jamming radar coi Pokémon Elettro/Acciaio), Pozzallo, Ispica |
| 6.16 | SS626 e valloni (frane a comando), Caltanissetta (Segreteria 4: Viadotto Salso 2), San Cataldo (zolfara) |
| 6.17 | Gela, Niscemi (MUOS e pozzi chimici scavati dai `Dugtrio`), Mazzarino, Riesi |
| 6.18 | Mussomeli, Sutera |
| 6.19 | Licata (Calogero e le autobotti), Palma di Montechiaro, Canicattì |
| 6.20 | Agrigento (Ipogei prosciugati dai `Gastrodon`/`Octillery`, Villaseta e il cemento notturno, Segreteria 5), Favara |
| 6.21 | Porto Empedocle, Realmonte, Sciacca (saracinesche notturne e terme) |
| 6.22 | Lampedusa e Linosa (frode del carburante e Porta d'Europa in tono sobrio) |
| 6.23 | Castelvetrano/Selinunte (covi smantellati), Gibellina e Cretto (silenzio col Pokémon a seguito), Mazara del Vallo |
| 6.24 | Marsala (pale eoliche girate a vuoto dagli stormi Volante), Trapani, Erice (Segreteria 6: Loggia del Vento) |
| 6.25 | Alcamo, Castellammare/Scopello/Zingaro, San Vito Lo Capo, Favignana, pullman delle 5:40 |
| 6.26 | Nebrodi: Sant'Agata, San Fratello, Mistretta (mafia dei pascoli di carta e `Rapidash` sanfratellani), Capo d'Orlando |
| 6.27 | Patti/Tindari, Barcellona Pozzo di Gotto, Milazzo |
| 6.28 | Eolie: Lipari (dissalatore bloccato), Vulcano, Stromboli (Sciara del Fuoco) |
| 6.29 | Messina (Torre Faro e l'elicottero del 2006, Ganzirri, Giostra, Duomo, Segreteria 7 e gli archivi magnetici dal 1971) |
| 6.30 | Taormina (galà e riciclaggio d'élite) e Giardini Naxos; attraversamento dello Stretto |
| 6.31 | Cinisi (Punta Raisi, Casa Memoria) e Capaci/Isola delle Femmine — tono sobrio, silenzio del Pokémon a seguito |
| 6.32 | Palermo: Politeama/Libertà, Massimo, Quattro Canti, Palazzo delle Aquile (Segreteria 8: l'On. Scaduto) |
| 6.33 | Palermo: Ballarò, Vucciria, Kalsa, Borgo Vecchio, ZEN 2 (`UrnaElettor.`), Mondello (`U Cassiere` e il Parcheggiatore Capo) |
| 6.34 | Monreale, Bagheria, Corleone/Ficuzza (le voliere dei «pizzini alati» e il CIDMA sobrio), Piana degli Albanesi, Partinico, Termini, Cefalù |
| 6.35 | Enna, Pergusa, Nicosia, Sperlinga, Agira, Leonforte, Aidone, Centuripe (Segreteria 9: la Commissione Elettorale) |
| 6.36 | Via della Lega e i 4 Campioni dell'ARS; Piazza Armerina e i 6 Pokémon-pilastro di Mistretta nella Villa Romana |
| 6.37 | Palco (col Pokémon starter al fianco), dissolvenza, titoli di coda (`msg_0440`, 301 messaggi) |
| 6.38 | Post-game: Ritrovi, Maria sul tetto del tribunale, i 4 Fantasmi della Prima Repubblica, Ho-Oh sull'Etna, Lugia a Cariddi, i Tre Venti vaganti, Fiera del Mediterraneo, Pantelleria, missioni P |

## Modulo 7 — `EXECUTOR_ATOMIC_RUNBOOK.md` (7 richieste)

| ID | Richiesta | File | Contenuto |
|---|---|---|---|
| 7.1 | `Genera il blocco 7.1 del Modulo 7: TASK del Modulo 1 e impianto di prova (emulatore e salvataggi).` | `docs/MODULO_7/7.1_TASK_MOTORE.md` | TASK-0001… dai passi M1, `emu.sh` per `pokeheartgold`, salvataggi di prova. |
| 7.2 | `Genera il blocco 7.2 del Modulo 7: TASK delle costanti e dei nomi (Moduli 2 e 3).` | `docs/MODULO_7/7.2_TASK_COSTANTI_NOMI.md` | Rinomina dei simboli `MAP_*`, `MAPSEC_*`, `FLYPOINT_*`, `FLAG_SYS_FLYPOINT_*`, `SPAWN_*`, `TRAINER_CLASS_*` (inclusi gli slot Rocket → «U Sistema») e file di alias `*_hg_compat.h` (R-MAP-01/02, R-10.6), `include/trinacria/trinacria_seq.h`, nomi dei luoghi in `msg_0279`. |
| 7.3 | `Genera il blocco 7.3 del Modulo 7: TASK dell'audio (Modulo 5).` | `docs/MODULO_7/7.3_TASK_AUDIO.md` | |
| 7.4 | `Genera il blocco 7.4 del Modulo 7: TASK della grafica (Modulo 4).` | `docs/MODULO_7/7.4_TASK_GRAFICA.md` | |
| 7.5 | `Genera il blocco 7.5 del Modulo 7: TASK delle mappe e degli script di CT, SR, RG.` | `docs/MODULO_7/7.5_TASK_ATTI_I-II.md` | Intestazioni in `map_headers.h`, matrice 0 e matrici nuove, tabelle di volo e spawn, gemelli `msg_0830`–`0933`, zona della cenere definitiva. Prove a schermo: il meteo 9 mostra nebbia ad Augusta? (altrimenti `WEATHER_SUNNY` + tinta gialla); le due regioni del Pokégear funzionano? |
| 7.6 | `Genera il blocco 7.6 del Modulo 7: TASK delle mappe e degli script di CL, AG, TP, ME.` | `docs/MODULO_7/7.6_TASK_ATTI_III-IV.md` | |
| 7.7 | `Genera il blocco 7.7 del Modulo 7: TASK di PA, EN, finale, post-game e verifica completa.` | `docs/MODULO_7/7.7_TASK_ATTO_V_E_VERIFICA.md` | |

Ogni TASK: file da aprire in `F:\Progetti\pokeheartgold`, blocco esatto da inserire o sostituire, comando di verifica (`build_trinacria.ps1`, `trinacria_msg_lint.py`, `nitrogfx`, controlli del Modulo 2/3), criterio PASS/FAIL binario.

---

**Totale: 72 richieste** (5 + 14 + 4 + 4 + 38 + 7). Il Modulo 1, questo documento e il blocco 2.1 sono già consegnati: restano **71 richieste**, a partire dalla 2.2.

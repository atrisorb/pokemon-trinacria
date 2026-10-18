# Pokémon Trinacria — Trama espansa, sottotrame e missioni secondarie

**Versione:** 1.4 · 18/10/2026 · autore del progetto: **atrisorb**
**Fonte:** `F:\Progetti\pokeheartgold\docs\trinacria_spec\` (PLOT_TO_BE_ENRICHED.md, STORY_STATE_MACHINE.json, LLM_MASTER_INSTRUCTIONS.md, SCRIPT_GENERATION_TEMPLATE.md). Questo documento le **estende**: dove le specifiche sono vaghe o in contraddizione, la decisione presa qui è vincolante per i Moduli 2–7 (registro §0).

Il documento è il «canone narrativo». Non contiene ancora le battute: le scrive il Modulo 6, comune per comune, a partire da qui. I nomi siciliani di Pokémon, mosse e strumenti citati sono quelli delle specifiche; quelli mancanti li fissa il Modulo 3.

**Novità della versione 1.1:** decisione R-09 (come i luoghi della trama diventano mappe, dal registro `docs/MODULO_2/2.1_MAPS_CT_SR_RG.json`) e tabelle dei dungeon di CT, SR e RG allineate al registro. Per sapere **in quale mappa** si svolge una missione fa fede il campo `contenuti_trama` del registro del Modulo 2.
**Novità della versione 1.2:** decisione **R-10** (centralità biopolitica dei Pokémon nel mondo di gioco e architettura di **«U Sistema»**, la mafia siciliana contemporanea che sostituisce il Team Rocket compiendo operazioni sui Pokémon inedite nella storia della serie) e integrazione capillare del ruolo dei Pokémon e di «U Sistema» in tutte le sottotrame (§1), nelle 9 province (§2–§10) e nel post-game (§11), mantenendo invariati codici, mappe, flag, variabili e regole di sicurezza narrativa (R-05).
**Novità della versione 1.3:** completamento della decisione **R-09** con il registro `docs/MODULO_2/2.3_MAPS_ME_PA_EN_ROADS.json` (Messina, Palermo, Enna, 40 arterie `MAP_STRADA_*`, Lega dell'ARS, Fiera del Mediterraneo e post-game: tutte le **354 mappe** del gioco e tutte le **345 celle giocabili** della Matrice 0 sono ora assegnate e collegate al 100%).
**Novità della versione 1.4:** R-10.6 allineata al registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json`: nomi reali delle classi (`TRAINERCLASS_*`, 7 slot del Team Rocket) e degli slot musicali di «U Sistema». Il registro fissa anche gli ID allenatore dei personaggi della trama (Segretari, boss, Cambiavoti, Guastafeste dei comizi, Campioni, Mistretta, alleati e pretoriani di M-EN-05, Ritrovi, Maria, Fantasmi). Punto aperto: Maria (C-05) non ha un Ritrovo (P-01 elenca sette giorni per sette compagni); i suoi ID 712–714 restano riservati.

---

## 0. Registro delle decisioni di riconciliazione

### R-01 — Elenco definitivo dei comuni (85 comuni + località)

Le specifiche elencano alcune frazioni come comuni (Aci Trezza, Marzamemi, Marina di Ragusa, Punta Secca, Pergusa, Vulcano, Stromboli, Tindari). Restano nel gioco come **località** del loro comune. Per arrivare al conteggio pieno senza inventare luoghi, si aggiungono Randazzo (CT), Santa Croce Camerina (RG, comune di Punta Secca) e Pantelleria (TP, solo post-game).

| Prov. | Comuni (mappe esterne proprie) | Località dentro un comune | N. |
|---|---|---|---|
| CT | Catania, Misterbianco, Acireale, Aci Castello, Nicolosi, Paternò, Adrano, Bronte, Randazzo, Caltagirone | Aci Trezza (Aci Castello), Etna Sud/Rifugio Sapienza/Crateri Silvestri (Nicolosi), Plaia e Fontanarossa (Catania), Santa Maria la Scala (Acireale) | 10 |
| SR | Siracusa, Augusta, Priolo Gargallo, Melilli, Lentini, Carlentini, Noto, Avola, Pachino, Portopalo di Capo Passero | Ortigia e Neapolis (Siracusa), Marzamemi (Pachino), Vendicari (Noto), Isola delle Correnti (Portopalo) | 10 |
| RG | Ragusa, Modica, Scicli, Vittoria, Comiso, Pozzallo, Santa Croce Camerina, Ispica | Ibla e Marina di Ragusa (Ragusa), Punta Secca (Santa Croce Camerina), Cava d'Ispica (Ispica) | 8 |
| CL | Caltanissetta, Gela, Mussomeli, Niscemi, San Cataldo, Riesi, Mazzarino, Sutera | Gabbara (San Cataldo), Sughereta e MUOS (Niscemi), Rabato (Sutera) | 8 |
| AG | Agrigento, Licata, Sciacca, Porto Empedocle, Realmonte, Canicattì, Favara, Palma di Montechiaro, Lampedusa e Linosa | Valle dei Templi e Villaseta (Agrigento), Scala dei Turchi (Realmonte) | 9 |
| TP | Trapani, Erice, Marsala, Mazara del Vallo, Castelvetrano, Alcamo, Castellammare del Golfo, San Vito Lo Capo, Gibellina, Favignana, Pantelleria (post-game) | Selinunte (Castelvetrano), Mozia e Stagnone (Marsala), Scopello e Zingaro (Castellammare) | 11 |
| ME | Messina, Taormina, Giardini Naxos, Milazzo, Lipari, Barcellona Pozzo di Gotto, Patti, Capo d'Orlando, Sant'Agata di Militello, San Fratello, Mistretta | Ganzirri e Torre Faro (Messina), Vulcano e Stromboli (Lipari), Tindari e Marinello (Patti), Isola Bella (Taormina) | 11 |
| PA | Palermo, Capaci, Isola delle Femmine, Cinisi, Monreale, Bagheria, Corleone, Piana degli Albanesi, Termini Imerese, Cefalù, Partinico | Mondello e ZEN (Palermo), Punta Raisi (Cinisi), Ficuzza (Corleone), Portella della Ginestra (Piana degli Albanesi) | 11 |
| EN | Enna, Piazza Armerina, Nicosia, Sperlinga, Agira, Leonforte, Aidone, Centuripe | Pergusa (Enna), Villa Romana del Casale (Piazza Armerina), Morgantina (Aidone) | 8 |
| | | **Totale** | **86** (85 in storia + Pantelleria post-game) |

Una «località» non ha per forza una mappa propria: può essere una cella in più della mappa del suo comune (R-09.2).

### R-02 — Percorso di gioco (ordine geografico vincolante)

1. **CT** → a piedi lungo la SS114 dopo la crisi di Fontanarossa → **SR** → **RG** → SS115 verso ovest → **CL** → **AG** → SS115 → **TP**.
2. Da TP a ME: Palermo è chiusa dalla «Zona rossa» del Grande Comizio del Presidente Mistretta (cordone di polizia e Pokémon da blocco stradale: gag ricorrente). Si attraversa con la **scena del pullman regionale delle 5:40** (sequenza scriptata Trapani → Sant'Agata di Militello, fermate soppresse, aria condizionata rotta): si arriva nei **Nebrodi** → **ME**.
3. Da ME a PA: Pippo ti porta col traghetto dello Stretto a Villa San Giovanni e all'aeroporto di Reggio Calabria (fuori mappa, scena), da lì volo per **Punta Raisi** (Cinisi, Aeroporto Falcone e Borsellino). Così l'Atto V entra in Palermo **da ovest**, come chiedono le specifiche: Cinisi → A29 a Capaci → Isola delle Femmine → Palermo.
4. **PA** → A19 (deviazioni sulle trazzere) → **EN** (Dossier 9) → Volo a Palermo per la **Lega** → **Piazza Armerina** (finale).

### R-03 — I 9 Dossier e le MN (slot delle medaglie verificati in `src/field_move.c`)

| N. | Dossier | Segreteria (luogo) | Slot medaglia | Sblocca (MN, nome delle specifiche) | Uso civico fuori lotta (R-10.4) |
|---|---|---|---|---|---|
| 1 | Dossier Liotru | Catania, Palazzo degli Elefanti | `BADGE_ZEPHYR` | Spaccaroccia → `Martiddata` | Frantuma i blocchi di calcestruzzo abusivi dei clan e i massi delle micro-frane stradali |
| 2 | Dossier Aretusa | Siracusa, Ortigia (Castello Maniace) | `BADGE_HIVE` | Taglio → `Roncigghiu` | Recide i rovi del demanio abbandonato, le reti abusive delle tonnare e le casse dei mercati |
| 3 | Dossier Carrubba | Ragusa Ibla | `BADGE_PLAIN` | Forza → `Spallata` | Sposta i massi delle frane eterne (SS626/A19) e i container/carrelli dei monopoli logistici |
| 4 | Dossier Pirrera | Caltanissetta | `BADGE_FOG` | Surf → `Aliscafu` | Naviga tratti costieri, lagune, canali allagati degli Ipogei e isole senza dipendere dai traghetti |
| 5 | Dossier Telamuni | Agrigento | `BADGE_STORM` | Volo → `Passaggiu` | Sorvola le autostrade interrotte (bloccato nell'area etnea da `FLAG_ETNA_ASH_ACTIVE` fino a `FLAG_ELICOTTERO_PRIVATO`) |
| 6 | Dossier Mulinu | Erice, Castello di Venere | `BADGE_MINERAL` | — (obbedienza) | Autorità carismatica sui Pokémon ad alto livello prima della traversata dei Nebrodi |
| 7 | Dossier Pilunu | Messina | `BADGE_GLACIER` | Mulinello (nome nel Modulo 3) | Domina i gorghi di Cariddi nello Stretto di Messina per raggiungere le fosse abissali |
| 8 | Dossier Geniu | Palermo, Palazzo delle Aquile | `BADGE_RISING` | Cascata (nome nel Modulo 3) | Risale la Cascata delle Due Rocche a Corleone e i salti d'acqua dell'entroterra |
| 9 | Dossier Cerere | Enna Alta | `BADGE_EARTH` | Scalaroccia (nome nel Modulo 3) | Scala le pareti verticali di Rocca Busambra, del Cratere Centrale dell'Etna, di Sperlinga e del Castello Ursino (post-game) |

I nomi dei Dossier sono decisi dall'architetto (il dizionario non ha queste voci) e vanno nel Glossario bloccato del Modulo 3.

### R-04 — Curva dei livelli

| Tappa | Asso della Segreteria | Selvatici della provincia |
|---|---|---|
| Dossier 1 CT | 18 | 3–17 |
| Dossier 2 SR | 25 | 15–24 |
| Dossier 3 RG | 31 | 22–30 |
| Dossier 4 CL | 37 | 28–36 |
| Dossier 5 AG | 43 | 34–42 |
| Dossier 6 TP | 49 | 40–48 |
| Dossier 7 ME | 55 | 46–54 |
| Dossier 8 PA | 61 | 52–60 |
| Dossier 9 EN | 66 | 58–65 |
| Lega (4 Campioni) | 70 / 72 / 74 / 76 | Via della Lega 62–68 |
| Mistretta | 82–88 | — |
| Post-game | compagni 75–85, Fantasmi 85–90, Maria 95–100 | 60–80 |

### R-05 — Regole di sicurezza narrativa (vincolanti)

1. **Reati e malaffare solo a persone e società inventate.** I luoghi reali (Cubbar, Vermut, Savia, Caffè Sicilia, Farm Cultural Park, alberghi, lidi) compaiono come **ambientazione**, senza attribuire loro reati. Il riciclaggio della movida (sottotrama di Christian) avviene in un locale inventato, il «Privè Zagara», alla Plaia.
2. **Enti pubblici reali** (SAC, Regione, ARS, Comuni, consorzi): si criticano i disservizi pubblici e noti (cenere a Fontanarossa, Comiso sottoutilizzato, buche, acqua) come **opinioni dei personaggi**. I dirigenti, i documenti «segreti» e le prove della trama sono inventati.
3. **Nessuna persona reale vivente** come personaggio, nemmeno caricaturata. Le persone reali scomparse si nominano solo nei luoghi della memoria e con rispetto (Peppino Impastato a Cinisi, le vittime di Capaci). Il boss che abitava a cento passi da Casa Memoria **non si nomina**: «la casa del boss».
4. **Luoghi della memoria in tono sobrio** (niente lotte, niente battute, musica dedicata): Capaci e Isola delle Femmine (A29, steli e Giardino della Memoria Quarto Savona Quindici), Casa Memoria a Cinisi, il Grande Cretto di Gibellina, Portella della Ginestra, il CIDMA di Corleone, la Porta d'Europa a Lampedusa, l'hotspot di Pozzallo. In questi luoghi anche il Pokémon a seguito del protagonista cammina in silenzio, senza gag o versi festosi (R-10.4).
5. **Le persone migranti non sono mai oggetto di satira.** Nella sottotrama di Lampedusa i bersagli sono gli appaltatori inventati, non chi arriva.
6. Satira **iper-caricaturale ma mai squallida**: nessuna battuta su malattie, disabilità, aspetto fisico di persone reali, violenza sessuale.

### R-06 — Il Consenso (`VAR_TRINACRIA_CONSENSO`, 0–100)

- Si parte dall'**1%** («ti vota solo Turi, e forse tua madre»).
- Missione principale completata: **+3**. Missione secondaria completata: **+1**. Boss secondario sconfitto: **+1**. Comizio di provincia (§1, ST-01): **+2**.
- Cancelli: Palermo centro (Atto V) richiede **≥ 40**; la Sala d'Ercole (Lega) richiede **≥ 49**. Con 27 punti dalle principali, 18 dai comizi e 1 di partenza, per arrivare a 49 servono **almeno 3 punti** da missioni secondarie o boss secondari; per vedere le scene opzionali dei compagni nel finale servono **≥ 60** (cioè circa 14 secondarie). È il motore che porta il giocatore a fare il contenuto secondario.
- Il valore compare nel Pokégear come «Sondaggio» (Modulo 4) e nelle battute degli NPC (il Modulo 6 scrive tre varianti per i comizi: <20, 20–48, ≥49).

### R-07 — Budget delle ore

| Blocco | Principale | Secondario | Totale | Ore cumulative |
|---|---|---|---|---|
| Prologo + CT | 8 | 7 | 15 | 0–15 |
| SR | 4 | 3 | 7 | 15–22 |
| RG | 4,5 | 3,5 | 8 | 22–30 |
| CL | 4 | 3 | 7 | 30–37 |
| AG | 5 | 4 | 9 | 37–46 |
| TP | 4 | 3 | 7 | 46–53 |
| ME | 4 | 3 | 7 | 53–60 |
| PA | 4 | 3 | 7 | 60–67 |
| EN + Lega + finale | 4 | 1 | 5 | 67–72 |
| **Storia** | **41,5** | **30,5** | **72** | |
| Post-game (Atto VI) | 12 | 18 | 30 | 72–102 |

### R-08 — Nomi delle missioni → flag e variabili

Ogni elemento di questo documento ha un codice: `M-` principale, `S-` secondaria, `D-` dungeon, `B-` boss secondario, `E-` easter egg, `C-` compagno, `P-` post-game. Il Modulo 2 crea per ognuno un flag di completamento con nome meccanico: `FLAG_` + codice con `-` → `_` (es. `S-CT-03` → `FLAG_S_CT_03`). Le missioni con più di due passi hanno anche una variabile di avanzamento `VAR_` + codice (assegnate da 0x405B in poi).
Il registro è `docs/MODULO_2/2.4_FLAGS_VARS.json` (18/10/2026): 262 flag di completamento, 48 variabili coi passi, i flag con nome di questo documento (`FLAG_DOSSIER_CT`, `FLAG_RECRUIT_ORAZIO`…) come alias dello stesso numero. Due punti della trama sono fissati lì: **ST-02** — l'Atto di Catania è quello che Maria raccoglie a Fontanarossa e consegna come «primo Atto» a Ortigia (M-SR-04); gli altri 8 li danno le Segreterie, tranne Palermo (M-PA-04); **ST-06** — i 9 Cambiavoti sono le 8 secondarie «Cambiavoti di …» più quello del pontile di Gela in M-CL-02 (diverso da quello del seggio di S-CL-08).

### R-09 — Dai luoghi alle mappe (registro del Modulo 2)

HeartGold ha **540 slot di mappa** e la matrice del mondo esterno ha al massimo **47×17 = 799 celle**. Per far stare tutta la Sicilia, i registri delle mappe (blocco 2.1 del 15/10/2026 per CT/SR/RG; blocco 2.2 del 16/10/2026 per CL/AG/TP; blocco 2.3 del 17/10/2026 per ME/PA/EN/ROADS) seguono queste regole.

**R-09.1 — Piani e sale diventano stanze.** Quando la trama dice «N mappe» o «N piani», nel gioco sono **stanze** di una stessa mappa, collegate da warp (di solito due o tre per mappa). Piani, allenatori ed eventi restano quelli della trama: cambia solo il numero di slot usati.

| Dungeon o luogo | Trama | Registro 2.1 / 2.2 / 2.3 |
|---|---|---|
| D-CT-01 Crateri Silvestri e Monti Rossi | 3 mappe | 2 mappe: Monti Rossi (pineta in fiamme + colata del 2001), Crateri Silvestri (bocca spenta) |
| D-CT-02 Palazzo di Cemento | 10 piani | 5 mappe da 2 piani (`…_P01_P02` … `…_P09_P10`) con una sola matrice nuova |
| D-CT-03 Sciara dei pistacchi | 2 mappe | 1 mappa da 2 stanze (terrazze basse, terrazze alte e masseria) |
| D-CT-04 Terminal A | 3 mappe | 2 mappe: atrio + controlli di sicurezza; gate + sala VIP |
| D-CT-06 Grotta del Gelo | 2 piani | 1 mappa da 2 stanze |
| D-CT-07 Sotterranei del Castello Ursino | 3 piani | 1 mappa da 3 stanze |
| M-CT-08 Palazzo degli Elefanti | dungeon-ufficio | 2 mappe: atrio + corridoi con le code; sala del boss |
| D-SR-01 Polo petrolchimico | 4 mappe | 2 mappe: pontili + serbatoi; sala controllo + torcia |
| D-SR-02 Latomie del Paradiso | 2 mappe | 1 mappa da 2 stanze (Latomia del Paradiso, Orecchio di Dionisio) |
| D-SR-03 Tonnara di Marzamemi | 2 mappe | 1 mappa da 2 stanze |
| D-SR-04 Castello Maniace | 3 mappe | 2 mappe: ingresso + cortile a marea; sala della Segreteria |
| S-SR-01 e S-SR-03 | 4 radio, 3 magazzini | 1 mappa per gruppo, una stanza per radio o magazzino |
| D-RG-01 Mercato di Vittoria | 3 padiglioni + piazzale | 2 mappe: padiglioni (3 stanze); piazzale dei TIR |
| M-RG-04 Segreteria 3 | magazzini refrigerati | 2 mappe: magazzini (2 stanze); ufficio del boss |
| D-RG-02 Ex base NATO | 4 mappe | 2 mappe: hangar + bunker; sala radar + pista |
| D-RG-03 Cava d'Ispica | 3 mappe | 1 mappa da 3 stanze (necropoli, Larderia, grotte alte) |
| D-CL-01 Castello Manfredonico | 3 piani sulla rupe | 1 mappa da 3 stanze (`MAP_CL_CASTELLO_MANFREDONICO`) |
| D-CL-02 MUOS (Niscemi) | 3 mappe | 1 mappa esterna (`MAP_CL_NISCEMI_SUGHERETA`, 2 celle) + 2 mappe interne da 2 stanze (`MAP_CL_NISCEMI_MUOS_RECINZIONE`, `MAP_CL_NISCEMI_MUOS_PARABOLE`) |
| D-CL-03 Zolfara di Gabbara | 3 livelli di gallerie | 2 mappe: gallerie superiori da 2 stanze (`MAP_CL_GABBARA_ZOLFARA_GALLERIE`) + camera di fondo (`MAP_CL_GABBARA_ZOLFARA_FONDO`) |
| D-CL-04 Viadotto Salso 2 (Segreteria 4) | 4 piloni + cabina | 2 mappe: piloni da 3 stanze (`MAP_CL_VIADOTTO_SALSO_PILONI`) + cabina sospesa del boss (`MAP_CL_VIADOTTO_SALSO_CABINA`) |
| D-AG-01 Ipogei della Valle dei Templi | 3 livelli di cunicoli | 2 mappe: gallerie da 2 stanze (`MAP_AG_IPOGEI_GALLERIE`) + grande cisterna (`MAP_AG_IPOGEI_CISTERNA`) |
| D-AG-02 Grotta della Scala dei Turchi | 2 mappe di marna | 1 mappa da 2 stanze (`MAP_AG_GROTTA_SCALA_DEI_TURCHI`) |
| D-AG-03 Stufe del Monte Kronio | 3 piani di grotte | 1 mappa da 3 stanze (`MAP_AG_SCIACCA_STUFE_KRONIO`) |
| D-AG-04 Palazzine di Villaseta (Segreteria 5) | 3 edifici + attico | 2 mappe: cantieri da 3 stanze (`MAP_AG_VILLASETA_CANTIERI`) + attico con piscina del boss (`MAP_AG_VILLASETA_ATTICO_IACONO`) |
| D-TP-01 Cave di Cusa | 2 mappe | 1 mappa da 2 stanze (`MAP_TP_CAVE_DI_CUSA`) |
| D-TP-02 Laguna dello Stagnone | 3 mappe | 1 mappa esterna (`MAP_TP_MARSALA_STAGNONE`) + 1 mappa da 3 stanze (`MAP_TP_STAGNONE_LAGUNA`: saline, strada fenicia sommersa, Mozia) |
| D-TP-03 Cave di tufo di Cala Rossa | 2 mappe | 1 mappa da 2 stanze (`MAP_TP_FAVIGNANA_CALA_ROSSA`) |
| D-TP-04 Castello di Venere (Segreteria 6) | 3 mappe | 2 mappe: cortili nella nebbia da 2 stanze (`MAP_TP_CASTELLO_VENERE_CORTILI`) + loggia del boss (`MAP_TP_CASTELLO_VENERE_LOGGIA`) |
| D-TP-05 Grande Cretto di Gibellina | 1 mappa labirinto | 1 mappa da 2 stanze (`MAP_TP_GRANDE_CRETTO`) |
| D-ME-01 Bosco dei Nebrodi | 3 mappe di faggeta e pascoli | 1 mappa esterna da 3 celle (`MAP_ME_BOSCO_DEI_NEBRODI`) + 1 mappa interna da 2 stanze (`MAP_ME_NEBRODI_PASCOLI_FANTASMA`) |
| D-ME-02 Archivi della Società Stretto Eterna | 5 piani di faldoni dal 1971 | 1 mappa da 3 stanze (`MAP_ME_ARCHIVI_STRETTO_ETERNA`: piani 1–2, 3–4, 5) |
| M-ME-06 Palazzo delle Partecipate (Segreteria 7) | salone ingranaggi + CdA | 2 mappe: atrio e corridoio da 2 stanze (`MAP_ME_PALAZZO_PARTECIPATE_ATRIO`) + sala del boss (`MAP_ME_PALAZZO_PARTECIPATE_SALA`) |
| D-ME-03 Sciara del Fuoco (Stromboli) | 2 mappe vulcaniche | 1 mappa da 2 stanze (`MAP_ME_STROMBOLI_SCIARA_DEL_FUOCO`) |
| D-ME-04 Gorghi di Cariddi + P-08 | 2 mappe di mare vorticoso | 1 mappa da 2 stanze (`MAP_ME_GORGHI_DI_CARIDDI`) + 1 mappa abissale post-game (`MAP_ME_ABISSO_CARIDDI`) |
| D-PA-01 Monte Pellegrino e Grotta dell'Addaura | 3 mappe carsiche | 1 mappa esterna da 3 celle (`MAP_PA_MONTE_PELLEGRINO`) + 1 mappa interna da 3 stanze (`MAP_PA_MONTE_PELLEGRINO_GROTTE`) |
| D-PA-02 Bosco di Ficuzza e Cascata delle Due Rocche | 3 mappe | cella est di Corleone (`[15,6]`) + 1 mappa esterna da 3 celle (`MAP_PA_BOSCO_DI_FICUZZA`) + 1 mappa interna da 2 stanze (`MAP_PA_FICUZZA_VOLIERE_PIZZINI`) + vetta post-game (`MAP_PA_ROCCA_BUSAMBRA_VETTA`) |
| D-PA-03 Villa Palagonia | 2 mappe tra le statue | 1 mappa da 2 stanze (`MAP_PA_BAGHERIA_VILLA_PALAGONIA`) |
| D-PA-04 Ex stabilimento di Termini Imerese | 4 mappe | 1 mappa da 3 stanze (`MAP_PA_TERMINI_EX_STABILIMENTO`) |
| D-PA-05 Palazzo delle Aquile (Segreteria 8) | 3 piani comunali | 2 mappe: corridoi e commissioni da 2 stanze (`MAP_PA_PALAZZO_AQUILE_CORRIDOI`) + sala del boss (`MAP_PA_PALAZZO_AQUILE_SALA_SCADUTO`) |
| D-PA-06 Via della Lega (corridoi dell'ARS) | 5 piani (2 saltabili con ST-07) | 1 mappa da 3 stanze (`MAP_PA_PALERMO_VIA_DELLA_LEGA`: piani 1–2, 3–4, 5) tra `MAP_PA_PALERMO_LEGA_INGRESSO` e `MAP_PA_PALERMO_LEGA_ATRIO` |
| D-EN-01 Trazzere dell'A19 | 4 mappe esterne tra piloni | 1 mappa stradale da 5 celle sulla matrice 0 (`MAP_EN_A19_TRAZZERE`) |
| D-EN-02 Castello di Sperlinga | 2 piani scavati nella roccia | 1 mappa da 2 stanze (`MAP_EN_CASTELLO_DI_SPERLINGA`) |
| D-EN-03 Rocca di Cerere (Segreteria 9) | 2 mappe nella nebbia | 1 mappa da 2 stanze (`MAP_EN_ROCCA_DI_CERERE_NEBBIA`) + sala della Commissione Elettorale (`MAP_EN_COMMISSIONE_ELETTORALE`) |
| D-EN-04 Villa Romana del Casale | 3 sale a mosaico + Grande Caccia | 1 mappa da 3 stanze (`MAP_EN_VILLA_ROMANA_CASALE_GALLERIE`) + Sala della Grande Caccia (`MAP_EN_SALA_DELLA_GRANDE_CACCIA`) |

**R-09.2 — Località come seconda cella del comune.** Queste località non hanno una mappa propria: sono una cella in più della mappa esterna del comune.

| Località | Mappa e cella |
|---|---|
| Salinelle | Paternò, cella est |
| Ponte dei Saraceni | Adrano, cella ovest |
| Timpa e Santa Maria la Scala | Acireale, cella sud |
| Versante nord dell'Etna (ingresso della Grotta del Gelo) | Randazzo, cella est |
| Scalinata di Santa Maria del Monte | Caltagirone, cella sud: le **7 rampe sono 7 terrazze** della stessa mappa, un allenatore per terrazza |
| Biviere di Lentini | Lentini, cella ovest |
| Isola delle Correnti | Portopalo, cella sud (raggiungibile solo con la bassa marea, per script) |
| Contrada Gabbara (ingresso zolfara) | San Cataldo, cella nord `[22,7]` |
| Quartiere Rabato e Monte San Paolino | Sutera, cella sud `[20,9]` |
| Rupe del Castello Manfredonico | Mussomeli, cella nord `[20,6]` |
| Quartiere Villaseta (ingresso cantieri) | Agrigento, cella ovest `[17,9]` |
| Marinella di Porto Empedocle | Porto Empedocle, cella ovest `[16,10]` |
| Belvedere della Scala dei Turchi | Realmonte, cella ovest `[14,9]` |
| Saline di Trapani e stazione di valle della funivia | Trapani, cella est `[3,4]` |
| Baglio e faraglioni di Scopello | Castellammare del Golfo, cella ovest `[6,3]` |
| Spiaggia dei Conigli e Cavallo Bianco | Lampedusa, cella est (matrice propria 2×1 `map_matrix_0335_AG_LAMPEDUSA.bin`) |
| Promontorio di Tindari e Laghetti di Marinello | Patti, cella est `[33,0]` (`MAP_ME_PATTI_TINDARI`, con interno `MAP_ME_TINDARI_SANTUARIO`) |
| Isola Bella | Taormina, cella est `[43,1]` (`MAP_ME_TAORMINA`) |
| Lipari, Vulcano e Stromboli | Isole Eolie, 3 celle in matrice propria 3×1 `map_matrix_0354_ME_ISOLE_EOLIE.bin` (`MAP_ME_ISOLE_EOLIE`) |
| Aeroporto di Punta Raisi | Cinisi, cella nord `[10,2]` (`MAP_PA_CINISI`) |
| Isola delle Femmine | Capaci e Isola delle Femmine, cella nord `[11,2]` (`MAP_PA_CAPACI_ISOLA_DELLE_FEMMINE`) |
| Cascata delle Due Rocche | Corleone, cella est `[15,6]` (`MAP_PA_CORLEONE`) |
| Sicilia Outlet Village | Agira, cella sud `[32,5]` (`MAP_EN_AGIRA_OUTLET`) |
| Parco archeologico di Morgantina | Aidone, celle est `[31,7]` e `[31,8]` (`MAP_EN_AIDONE_MORGANTINA`) |

Hanno invece una mappa esterna propria: Ognina, Plaia, Fontanarossa, Aci Trezza, Etna Sud, Neapolis, Ortigia, Vendicari (ingresso), Marzamemi, Ibla, Marina di Ragusa, aeroporto di Comiso, Punta Secca (blocco 2.1); Sughereta di Niscemi, Valloni della SS626, Valle dei Templi, Acquedotto Costiero, Lampedusa, Selinunte, Stagnone di Marsala, Riserva dello Zingaro, Favignana (blocco 2.2); Bosco dei Nebrodi, Isole Eolie, Ganzirri/Torre Faro, Giostra, Diga Jato, Mondello, ZEN 2, Monte Pellegrino, Borgo Vecchio/Porto, Politeama/Libertà, Massimo/Maqueda, Vucciria/Kalsa, Ballarò, Palazzo dei Normanni, Bosco di Ficuzza, Alte Madonie, Enna Bassa, Lago di Pergusa, Pantelleria e le 40 arterie stradali `MAP_STRADA_*` più `MAP_EN_A19_TRAZZERE` (blocco 2.3).

**R-09.3 — Interni tolti: la scena si svolge all'aperto.**

| Interno della trama | Dove si svolge ora |
|---|---|
| Rifugio Sapienza | solo esterno, nella mappa Etna Sud |
| Stazione di Randazzo (S-CT-08) | binario e capostazione all'aperto; il viaggio è una mappa di scena (il treno) da cui si scende a Bronte |
| Palazzo del Barone della Timpa (B-CT-05) | lotta all'aperto sulla Timpa (cella sud di Acireale) |
| Bottega del ceramista (S-CT-07) | il ceramista aspetta in cima alla Scalinata |

**R-09.4 — Vendicari è la Zona Safari di HeartGold.** Il motore attiva la modalità Safari solo su quegli slot: casa del guardiaparco (slot 173), snodo della riserva (357) e 14 aree (343–356) che prendono il nome dai luoghi della riserva (Pantano Grande, Pantano Piccolo, Pantano Roveto, Torre Sveva, Tonnara di Vendicari, Cittadella dei Maccari, Spiaggia di Calamosche, Eloro, Pantano Sichilli, Saline, Macchia mediterranea, Dune, Scogliera, Pantano Gorgo). Le aree non hanno testi propri, quindi non hanno banco gemello.

**R-09.5 — Centri Pokémon con negozio.** Ogni Centro ha anche il bancone del negozio: non esistono mappe separate per i negozi. A Modica il laboratorio di cioccolato fa da Centro e da negozio (M-RG-01).

**R-09.6 — Due regioni nel Pokégear.** La mappa del Pokégear è divisa in **Sicilia orientale** (mappe con cella principale in colonna ≥ 24 della matrice; lato «Kanto» del motore) e **Sicilia occidentale** (colonna ≤ 23; lato «Johto»). Tutte le province di CT, SR, RG, ME ed EN più la fascia orientale di CL (Gela, Niscemi, Sughereta, MUOS, Mazzarino, Riesi, Valloni SS626, Viadotto Salso 2) e le 23 arterie stradali orientali/centrali sono in `MAP_REGION_KANTO`; Caltanissetta città, San Cataldo, Sutera, Mussomeli, AG, TP, PA e le 17 arterie stradali occidentali sono in `MAP_REGION_JOHTO`. Le 4 isole minori (`MAP_AG_LAMPEDUSA`, `MAP_TP_FAVIGNANA`, `MAP_ME_ISOLE_EOLIE`, `MAP_TP_PANTELLERIA`) hanno matrici proprie e usano gli slot speciali `S.S. Aqua` (`308`, `309`) e `Sinjoh` (`522`, `523`).

**R-09.7 — Nebbia gialla del polo petrolchimico e nebbie termali/montane.** Augusta, Priolo e le mappe del polo usano il valore meteo **9** (`WEATHER_UNKNOWN_9`, probabilmente nebbia, mai usato da HeartGold). Va verificato a schermo nel Modulo 7: se non mostra nebbia, quelle mappe tornano a `WEATHER_SUNNY` e il Modulo 4 dà la tinta gialla al tileset. Erice (`MAP_TP_ERICE`, `MAP_TP_CASTELLO_VENERE_CORTILI`), le Stufe di San Calogero (`MAP_AG_SCIACCA_STUFE_KRONIO`), il casolare dei Nebrodi (`MAP_ME_NEBRODI_PASCOLI_FANTASMA`), l'Abisso di Cariddi (`MAP_ME_ABISSO_CARIDDI`), la Vetta di Rocca Busambra (`MAP_PA_ROCCA_BUSAMBRA_VETTA`), Enna Alta (`MAP_EN_ENNA_ALTA`) e la Rocca di Cerere (`MAP_EN_ROCCA_DI_CERERE_NEBBIA`) usano il meteo nativo `WEATHER_FOG` (`6`); Piazza Armerina (`MAP_EN_PIAZZA_ARMERINA`) usa `WEATHER_RAIN` (`1`).

---

### R-10 — Centralità biopolitica dei Pokémon e architettura di «U Sistema» (La Mafia Pokémon come nuovo Team Rocket)

Per evitare che i Pokémon appaiano come un semplice pretesto di gameplay sovrapposto a una trama politica umana, in *Pokémon Trinacria* **i Pokémon sono l'infrastruttura fisica, economica, ecologica e coercitiva della Sicilia**, e **la Mafia («U Sistema») sostituisce il Team Rocket compiendo sui Pokémon e tramite i Pokémon operazioni criminali, clientelari e infrastrutturali totalmente inedite nella storia del brand**. Questa regola è vincolante per tutti i Moduli 2–7.

#### R-10.1 — Perché in Sicilia tutto passa dai Pokémon (Infrastruttura Vivente)

In *Pokémon Trinacria* la cronica incompiutezza delle infrastrutture pubbliche siciliane ha una causa precisa: **al posto delle reti moderne, l'isola si regge sul lavoro biologico dei Pokémon**, e chi controlla i Pokémon controlla i rubinetti, i trasporti, i raccolti, gli ospedali, i rifiuti e le urne.
- **Acqua e Sottosuolo:** gli antichi *qanat* arabi e gli *Ipogei* greci sono alimentati e regolati da Pokémon Acqua/Terra (`Gastrodon`, `Quagsire`, `Octillery`, `Poliwrath`). Chi li sequestra o li dirotta lascia a secco intere città per vendere l'acqua con le autobotti private.
- **Rifiuti e Ambiente:** l'accumulo di `munnizza` nei vicoli e il fumo chimico dei poli industriali dipendono dall'uso distorto di Pokémon Veleno/Buio (`Munnizza`/Grimer, `Sacconiru`/Muk, `Ciminièra`/Koffing, `Priolu`/Weezing), usati dalle ecomafie come inceneritori viventi a costo zero o liberati ad arte nelle periferie prima delle elezioni per ottenere ordinanze d'emergenza in deroga agli appalti.
- **Sanità, Logistica ed Energia:** i Pokémon curatori (`Chansey`, `Blissey`, `Clefable`) sono requisiti dalle cliniche private convenzionate svuotando i pronto soccorso pubblici; i Pokémon Ghiaccio (`Piloswine`, `Sneasel`, `Cloyster`) refrigerano i TIR dei cartelli ortofrutticoli; i Pokémon Volante (`Staraptor`, `Pidgeot`, `Skarmory`) vengono usati per far girare a comando le pale eoliche scollegate dalla rete durante i collaudi per incassare i sussidi energetici.
- **Perché si vota chi vince le lotte Pokémon:** un candidato che cita solo i codici della LUISS non ha alcuna presa perché ogni «cacicco» di quartiere o di provincia governa tramite un presidio fisico di Pokémon che bloccano cantieri, banchine, mercati e uffici. Sconfiggere in piazza la squadra di un boss o di un Segretario significa **spezzare materialmente il suo monopolio sul servizio pubblico locale** (riaprire le saracinesche dell'acqua, liberare i banchi del mercato, sbloccare i terminali aeroportuali).

#### R-10.2 — «U Sistema» (La Mafia Bicefala) al posto del Team Rocket

In *Pokémon Trinacria* non esiste un «Team Rocket» fumettistico in divisa uguale che taglia le code agli Slowpoke o vuole conquistare il mondo con un raggio spaziale. Al suo posto c'è **«U Sistema» (Il Cartello Grigio-Mafioso)**, il cui obiettivo è l'opposto di quello dei team malvagi classici: **non vuole distruggere o cambiare il mondo, ma conservarlo in uno stato di emergenza perpetua per incassare fondi pubblici, gestire subappalti e muovere pacchetti di voti**.
«U Sistema» disprezza la vecchia estetica della coppola e della lupara (derisa dai suoi stessi dirigenti come *«roba per i film coi turisti»*) e si articola in una **piramide bicefala a 4 livelli operativi** che rimappa tutti gli slot tecnici del Team Rocket in `pokeheartgold`:

1. **Livello 1 — Il Braccio di Strada («A Manovalanza» / Reclute del Sistema):**
   - Sostituisce le reclute del Team Rocket (`TRAINERCLASS_TEAM_ROCKET` / `_F` → `TRAINERCLASS_SCAGNOZZU` / `TRAINERCLASS_INFILTRATA` e classi affini, registro 2.5).
   - Non indossano un'uniforme unica, ma la divisa del loro racket quotidiano: **Parcheggiatori e Strozzini di rione** (con borsello a tracolla, sedia di plastica e fischietto), **Buttafuori della movida** (auricolare e camicia nera), **Caporali dei magazzini e dei TIR**, **Custodi infedeli degli acquedotti**, **Pascolatori abusivi dei Nebrodi**, **Portaborse e Funzionari di sbarramento**.
   - Trattano i propri Pokémon come *manovalanza in nero* o *strumenti di pizzo biologico*, tenuti in `CoppulaBall` o `CuffaBall` non registrate e pompati con stimolanti da mercato nero per intimidire commercianti, contadini e viaggiatori.
2. **Livello 2 — I Quadri Mobili del Racket, della Notte e del Voto (Esecutivi del Sistema):**
   - Sostituisce i 4 Esecutivi del Team Rocket (Archer, Ariana, Petrel, Proton) con le figure trasversali che il giocatore affronta lungo più province:
     - **`U Cassiere` (`ST-04`, B-PA-04):** il ragioniere itinerante del pizzo che si sposta tra Catania, Ragusa, Agrigento e Palermo riscuotendo le buste e usando Pokémon Buio/Veleno (`Houndoom`, `Weezing`, `Honchkrow`, `Drapion`) per fiutare il contante nascosto e punire chi denuncia (come Nunzio, il fratello di Orazio).
     - **`I 9 Cambiavoti Provinciali` (`ST-06`):** i capibastone piazzati davanti alle scuole-seggio di ciascuna provincia che comprano il voto a 50 euro verificando la scheda in cabina tramite Pokémon spia.
     - **`I Gestori della Notte e dei Club VIP` (`ST-05`):** i referenti del riciclaggio nei locali esclusivi (Privè Zagara alla Plaia, Tonnara di Marzamemi, Galà di Taormina, Lido di Mondello).
     - **`I Caporali e Subappaltatori delle Incompiute`:** i capi-cantiere e capi-trasporto che presidiano i nodi logistici (Fontanarossa, Vittoria, Comiso, Viadotto Salso 2, MUOS).
3. **Livello 3 — «A Cupula Grigia»: I 9 Cacicchi delle Segreterie Provinciali (Capipalestra):**
   - I 9 boss provinciali che detengono i **9 Dossier** necessari per candidarsi. Sono professionisti, primari, commissari, geometri, avvocati massoni e amministratori delegati perfettamente integrati nelle istituzioni, ciascuno a capo di un monopolio biopolitico basato su uno specifico tipo di Pokémon (§2–§10).
4. **Livello 4 — Il Vertice Politico e gli Intoccabili: I 4 Campioni dell'ARS, l'On. Mistretta e i Fantasmi della Prima Repubblica:**
   - I **4 Campioni della «Lega»** a Palazzo dei Normanni (i pilastri del trasformismo regionale), il Presidente **On. Raffaele «Don Lollò» Mistretta** a Piazza Armerina (*«u tappu ca teni chiusa la buttigghia»*) e, nel post-game, i **4 Fantasmi della Prima Repubblica** (`P-03`–`P-06`), antichi burattinai occulti ritiratisi sulle vette e nei sotterranei dell'isola a guardia dei Pokémon Leggendari.

#### R-10.3 — Le 10 Operazioni Inedite di «U Sistema» coi Pokémon (Tabella di riferimento)

Nessuna di queste operazioni esiste nei giochi Pokémon tradizionali; ciascuna è cucita su una missione reale della trama di *Pokémon Trinacria*:

| N. | Operazione di «U Sistema» | Province e Missioni | Specie Pokémon impiegate dal Sistema | Meccanica criminale / clientelare nel mondo di gioco |
|---|---|---|---|---|
| 1 | **Il Pizzo Biologico e il Sabotaggio d'Esercizio** | CT (`M-CT-02`, `M-CT-03`), SR (`S-SR-03`), PA (`ST-04`, `B-PA-04`) | `Ciminièra` (Koffing), `Slugma`, `Scippaturi` (Weavile/Sneasel), `Manzuni` (Snorlax), `Houndour` | Gli strozzini non chiedono solo denaro: piazzano Pokémon Veleno/Fuoco dentro le officine e i negozi per rendere l'aria irrespirabile o surriscaldare i macchinari, o usano `Manzuni` in doppia fila per murare l'ingresso finché il titolare non paga la «protezione ambientale» o cede le quote al clan. |
| 2 | **L'Allaccio Abusivo Elettro-Idrico e il Ricatto Condominiale** | CT (`M-CT-05`, `D-CT-02` Librino) | `Magnemite`, `Magneton`, `Voltorb`, `Grimer`, `Goldeen` | Nel Palazzo di Cemento il Capo-Condominio usa Pokémon Elettro per allacciare abusivamente i 10 piani alla cabina pubblica e Pokémon Acqua/Veleno per controllare l'unica cisterna sul tetto: chi non accetta il pacco alimentare col santino elettorale subisce il distacco immediato di corrente e acqua. |
| 3 | **La Biotruffa Piromane e il Parassitismo Agro-Mafioso** | CT (`M-CT-06` Etna, `M-CT-07` Bronte), AG (`S-AG-05` Canicattì) | `Magmar`, `Slugma`, `Houndoom` (Etna); `Pinsir`, `Scyther`, `Yanma`, `Graveler` (Bronte) | Sull'Etna l'Incendiario usa Pokémon Fuoco per bruciare parcelle mirate di pineta, agitando i Pokémon vulcanici selvatici per incassare sia l'appalto di contenimento sia quello di rimboschimento coi Pokémon Erba; a Bronte il cartello dell'Oro Verde sguinzaglia di notte sciami di Pokémon Coleottero per divorare i pistacchi dei piccoli produttori che non vendono al prezzo imposto dal clan. |
| 4 | **Il Monopolio dei Pokémon Curatori (Sanità Convenzionata)** | CT (`M-CT-08` Segreteria 1 — Dott. Calì) | `Chansey`, `Blissey`, `Clefable`, `Lickitung`, `Miltank` | Negli ospedali pubblici le liste d'attesa durano 18 mesi perché le cliniche private convenzionate del Dott. Calì hanno accaparrato tutti i Pokémon con mosse di cura (`Covauova`, `Rintoccasana`, `Aromaterapia`), costringendo i cittadini a pagare prestazioni private rimborsate a peso d'oro dalla Regione. |
| 5 | **Lo Scandalo Cenere-SAC e il Jamming Radar dello Scalo Fantasma** | CT (`M-CT-09` Fontanarossa), RG (`M-RG-03`, `D-RG-02` Comiso) | `Donphan`, `Skarmory`, `Forretress` (chiusi a CT); `Magneton`, `Electrode`, `Bronzong` (jamming a Comiso) | Quando il parossismo dei Pokémon di fuoco nel Cratere Centrale scatena la `RinaDiL’Etna`, la dirigenza dello scalo catanese tiene fermi negli hangar VIP i Pokémon spazzatori Terra/Acciaio per fatturare «emergenze straordinarie»; in parallelo, nell'ex base NATO di Comiso i caporali dei TIR usano Pokémon Elettro/Acciaio per disturbare i radiofari del terminal civile, impedendo i dirottamenti su Comiso e salvando il monopolio del trasporto su gomma! |
| 6 | **Gli Inceneritori Viventi e il Feudo Marittimo** | SR (`M-SR-02`, `D-SR-01` Polo; `M-SR-03` Marzamemi; `M-SR-05` Segreteria 2) | `Ciminièra` (Koffing), `Priolu` (Weezing), `Sacconiru` (Muk); `Lanturn`, `Tentacruel`, `Gyarados` | Nel polo petrolchimico di Augusta–Priolo i dirigenti smaltiscono gratis gli scarti tossici dandoli in pasto a colonie di `Priolu` e `Sacconiru` dentro i serbatoi, che li rigettano di notte come nebbia gialla (`Smog`/`Nube`) spacciata per «fenomeno ottico»; a Marzamemi e Ortigia i Pokémon Acqua/Elettro dei concessionari recintano il mare pubblico per i club VIP e bloccano le navi che non pagano il dazio portuale. |
| 7 | **Il Racket della Catena del Freddo e della Maturazione** | RG (`M-RG-02`, `D-RG-01` Vittoria; `M-RG-04` Segreteria 3) | `Piloswine`, `Sneasel`, `Dewgong` (freddo); `Victreebel`, `Vileplume`, `Tangrowth` (spore) | Nei padiglioni del Mercato di Vittoria e nei magazzini di Occhipinti, i Pokémon Ghiaccio refrigerano a costo zero i TIR della ditta imposta dal clan, mentre i Pokémon Erba/Veleno spargono spore acide sulle casse degli agricoltori ribelli, facendo marcire pomodori e zucchine prima dell'asta delle 4:00. |
| 8 | **Le Frane a Comando per la Perizia di Variante e i Pozzi del MUOS** | CL (`M-CL-01` SS626, `M-CL-03` Niscemi, `M-CL-04` Segreteria 4) | `Rhydon`, `Graveler`, `Dugtrio`, `Machamp` (frane); `Magnemite`, `Kadabra`, `Sandslash`, `Muk` (MUOS) | L'Ing. Lo Monaco resta commissario del Viadotto Salso 2 da 22 anni perché alla vigilia di ogni collaudo i suoi `Rhydon` e `Dugtrio` usano `Scussuni` (Terremoto) e `Frana` sui piloni per generare una nuova «variante in corso d'opera»; a Niscemi, coperti dalle onde dei Pokémon Elettro/Psico sulle parabole del MUOS, i `Dugtrio` scavano cunicoli per seppellire fusti tossici sotto la base. |
| 9 | **Il Furto Idrico negli Ipogei, il Cemento Notturno e il Vento/Pascolo di Carta** | AG (`M-AG-01`–`05`), TP (`M-TP-03`–`04`), ME (`M-ME-01`) | `Gastrodon`, `Quagsire`, `Octillery`, `Steelix` (AG); `Staraptor`, `Pidgeot`, `Skarmory` (TP); `Tauros`, `Houndoom`, `Ursaring` (ME) | Negli Ipogei di Agrigento i Pokémon Acqua/Terra aspirano con `Sorbacqua` l'acqua pubblica verso le autobotti da 150 € mentre gli `Steelix` ostruiscono le condotte; a Villaseta i `Machamp` e `Golem` alzano piani abusivi in una notte; a Trapani stormi di Pokémon Volante fanno girare con `Ventoincoda` le pale eoliche finte davanti agli ispettori; sui Nebrodi Pokémon feroci scacciano gli allevatori dai terreni su cui il clan incassa i fondi europei per mandrie inesistenti. |
| 10 | **Lo Spionaggio in Cabina, la Burocrazia Magnetica, i Pizzini Alati e l'Emergenza Munnizza** | Tutte (`ST-06`), ME (`M-ME-04`/`06`), PA (`M-PA-04`/`05`), EN (`M-EN-03`–`06`) | `Natu`, `Murkrow`, `Sableye`, `Rotom` (`ST-06`); `Magnezone`, `Porygon2`, `Bronzong` (ME); `Honchkrow`, `Drapion` (PA); `Slowking`, `Grimer`/`Muk` (EN/Lega) | Davanti ai seggi i 9 Cambiavoti usano Pokémon Spettro/Psico/Volante sui davanzali per verificare il voto in cabina prima di pagare i 50 €; a Messina i `Magnezone` e `Porygon2` smagnetizzano i protocolli dal 1971 per perpetuare i gettoni del Ponte; a Palermo gli `Honchkrow` di Ficuzza portano i pizzini coi pacchetti di voti senza usare telefoni intercettabili; a Palazzo dei Normanni il Cardinale dei Rifiuti scatena `Munnizza` e `Sacconiru` nelle strade per governare a colpi di ordinanze d'urgenza. |

#### R-10.4 — Il Pokémon a Seguito (Follower), le MN Civiche e i Luoghi della Memoria

1. **Il Pokémon a Seguito (`followMode` nativo di HeartGold):**
   - Il primo Pokémon della squadra cammina sempre dietro al protagonista in tutte le mappe esterne e nei dungeon (`MAP_FOLLOWMODE_ALLOW` / `HEIGHT_RESTRICT`, disattivato solo nelle mappe `SCENA` come il treno della Circumetnea).
   - Narrativamente è l'**antitesi dell'auto blu**: mentre i politici di «U Sistema» si muovono scortati o chiusi nei palazzi, il protagonista cammina tra la gente col proprio Pokémon a fianco.
   - Durante i **Comizi di Provincia (`ST-01`)**, il Pokémon a seguito sale sul palco accanto al protagonista: gli NPC commentano la sua presenza e il disturbatore mandato dal Sistema tenta di spaventarlo o zittirlo.
   - Nei **Luoghi della Memoria (`R-05.4`)** — Capaci e Isola delle Femmine (`M-PA-02`), Casa Memoria a Cinisi (`M-PA-01`), Grande Cretto di Gibellina (`M-TP-02`), covi smantellati di Castelvetrano (`M-TP-01`), Portella della Ginestra (`S-PA-07`), CIDMA di Corleone (`M-PA-04`), Porta d'Europa (`M-AG-04`) e hotspot di Pozzallo — non c'è mai alcuna lotta né incontro selvatico: se il giocatore interagisce col proprio Pokémon a seguito in quelle mappe, il testo di reazione mostra il Pokémon silenzioso e raccolto accanto all'allenatore.
2. **Le MN come Autodifesa Civica:**
   - Ogni MN sbloccata dai 9 Dossier (tabella `R-03`) rappresenta l'intervento diretto dei Pokémon del cittadino là dove la Regione o il Comune hanno abbandonato il territorio o dove «U Sistema» ha eretto barriere fisiche.

#### R-10.5 — L'Atlante Biopolitico del Prof. Alfio Strano (`ST-12`)

- Il Pokédex consegnato al Vermut (`M-CT-02`) dal **Prof. Alfio Strano** (zoologo in pensione dell'Università di Catania, isolato dai baroni accademici legati a Mistretta) non è un semplice catalogo naturalistico: è il **«Censimento Biopolitico della Fauna di Trinacria»**.
- Ogni voce del Pokédex (scritta nel Modulo 3, blocchi `3.1`–`3.5`) documenta come la specie viva nei micro-ecosistemi siciliani (sciare laviche, saline, zolfare, pantani, mercati rionali, tunnel autostradali incompiuti) e come venga sfruttata da «U Sistema» o difenda il territorio. Completare il Pokédex significa consegnare a Strano la prova scientifica di come l'ecologia dell'isola e la sua questione morale siano una cosa sola.

#### R-10.6 — Mappatura Tecnica su `pokeheartgold` (Slot Team Rocket → «U Sistema»)

- Nel Modulo 2 (blocco `2.5`, registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json`), gli slot di `include/constants/trainer_class.h` appartenenti al Team Rocket vengono rinominati (con alias di compatibilità in `trainer_class_hg_compat.h`) nelle classi operative di **«U Sistema»**: `TRAINERCLASS_TEAM_ROCKET` → `TRAINERCLASS_SCAGNOZZU`, `TRAINERCLASS_TEAM_ROCKET_F` → `TRAINERCLASS_INFILTRATA`, `TRAINERCLASS_EXECUTIVE_ARIANA` → `TRAINERCLASS_CAMBIAVOTI`, `TRAINERCLASS_EXECUTIVE_ARCHER` → `TRAINERCLASS_CASSIERI`, `TRAINERCLASS_EXECUTIVE_PROTON` → `TRAINERCLASS_CAPORALI`, `TRAINERCLASS_EXECUTIVE_PETREL` → `TRAINERCLASS_COLLETTU_BIANCU`, più il settimo slot del Team Rocket, `TRAINERCLASS_SCIENTIST_GS` → `TRAINERCLASS_PORTABORSE` (i «Portaborse e Funzionari di sbarramento» del livello 1). Sono affiancate dalle altre classi siciliane (`FigghiuDiPapà`, `Parcheggiaturi`, `Assessuri`, `Zauddu`, `Buddaci`). Nel repository il prefisso è `TRAINERCLASS_`, non `TRAINER_CLASS_`.
- Nel Modulo 5, gli slot musicali del Team Rocket (e i rispettivi gemelli `SEQ_GS_P_*`) diventano i temi di **«U Sistema»**: incontro `SEQ_GS_EYE_ROCKET`, lotta `SEQ_GS_VS_ROCKET`, covi e uffici del cartello `SEQ_GS_E_RIVAL1` (il covo del Team Rocket, `SEQ_GS_D_AJITO`, è già la crisi di Fontanarossa del blocco 2.1; `SEQ_GS_R_AJITO` e `SEQ_GS_BA_ROCKET` non esistono).
- Nel post-game (`FLAG_POST_RESIGNATION`, Modulo 1 §7.4), il reset automatico degli allenatori 1–699 con il bonus di **+25 livelli** ha una giustificazione narrativa perfetta: sei mesi dopo le dimissioni del protagonista, **«U Sistema» ha ripreso il controllo di ogni quartiere, cantiere, porto e segreteria cambiando semplicemente sigla di partito**, con squadre ancora più forti e agguerrite.

---

## 1. Sottotrame trasversali

| Codice | Sottotrama | Ruolo dei Pokémon e di «U Sistema» attraverso il gioco | Chiusura |
|---|---|---|---|
| ST-01 | **I comizi di provincia** | In ogni capoluogo, dopo il Dossier, un comizio in piazza con palco, folla di sprite e il **Pokémon a seguito del protagonista sul palco**. «U Sistema» invia un «Guastafeste» con Pokémon sonori o molesti (`Subwoofer`/Exploud, `Chatot`, `Priolu`/Weezing, `Crobat`) per coprire l'audio del microfono o disperdere la piazza. +2 di Consenso. Il discorso del protagonista cambia tono man mano (da italiano accademico a lingua di strada). | Comizio finale a Piazza Duomo di Catania (scena del palco col Pokémon starter al fianco). |
| ST-02 | **Il Fascicolo Trinacria** (Maria) | Maria raccoglie atti non coperti da segreto sulle **biotruffe e sugli appalti Pokémon della Cupola Grigia**: in ogni provincia il giocatore sequestra un «Atto» (strumento chiave, 9 in tutto, custodito dai Pokémon contabili/archivio dei boss) che smaschera un pezzo della rete di Mistretta. Maria ripete: «il palazzo non si cambia da dentro». | Gli Atti non bastano per un processo perché i reati vengono prescritti o coperti da immunità: Maria lo dice nel finale. Nel post-game diventano la chiave della sfida segreta sul tetto del Palazzo di Giustizia. |
| ST-03 | **La comunicazione di Turi** | In ogni provincia Turi lancia una campagna social disastrosa coinvolgendo goffamente i Pokémon locali (il santino stampato dai `Smeargle` col nome sbagliato, il jingle neomelodico registrato coi `Chatot`, il video coi `Rapidash` sul viadotto, il filtro coi `Meowth`). Una gaffe per provincia = una missione di «riparazione» (`S-xx-01`). | Nel finale Turi piange abbracciando Orazio e il suo `Foculavicu` sul palco; nel post-game scrive un libro che non legge nessuno. |
| ST-04 | **Il fratello di Orazio e il Pizzo Biologico** | Il fratello di Orazio, Nunzio, ha chiuso l'officina perché il racket gli ha avvelenato i locali coi `Ciminièra` (Koffing) e bruciato i banchi coi `Slugma`. Orazio cerca il ragioniere itinerante del racket, **«U Cassiere»**, che sposta le buste del pizzo da una provincia all'altra scortato da Pokémon Buio/Veleno (`Houndoom`, `Honchkrow`, `Drapion`). Indizi in CT, RG, AG, PA. | Lo si affronta e smantella a Palermo (`B-PA-04`). Nunzio riapre l'officina in via Plebiscito nel post-game coi Pokémon meccanici finalmente liberi (`P-10`). |
| ST-05 | **I soldi della notte** (Christian) | Il «Privè Zagara» della Plaia (inventato) e i club gemelli riciclano contanti tramite i buttafuori e lotte/esibizioni clandestine di Pokémon di lusso (`Gattupardu`/Persian con `Pizzu`, `Sharpedo`, `Exploud`, `Luxray`). Christian infiltrato passa al giocatore liste e codici. Tappe: CT, SR (Marzamemi), ME (Taormina), PA (Mondello). | Il Privè chiude e i Pokémon sequestrati vengono liberati; Christian apre un canale di musica coi suoi `Subwoofer` (Exploud) e organizza i Ritrovi al Cubbar nel post-game. |
| ST-06 | **Il voto a 50 euro e i Pokémon Spia** (Chantal) | In ogni provincia c'è un «Cambiavoti» di «U Sistema» che compra voti a 50 euro fuori dal seggio-scuola, usando piccoli Pokémon Spettro/Psico/Volante (`Natu`, `Murkrow`, `Sableye`, `Haunter`, `Rotom`) nascosti vicino alle finestre delle cabine per verificare il voto in tempo reale! Chantal insegna a individuarli (trovare l'NPC col telefono e il Pokémon spia davanti alla scuola). 9 Cambiavoti = 9 boss minori. | Con 9 Cambiavoti sconfitti Chantal regala la `UrnaElettor.` (Master Ball, sviluppata per «catturare il consenso assoluto senza scampo») prima della Lega. |
| ST-07 | **I faldoni di Totò** | Totò conosce i nascondigli dell'ARS in cui i portaborse occultano i registri delle «quote Pokémon» regionali. Dal primo contatto (telefonata a Fontanarossa) lascia 9 «faldoni» nascosti nelle province, sorvegliati o fiutabili col Pokégear. | Con 9 faldoni il `Cappottu` (Gengar) e il `Vucciria` (Honchkrow) di Totò aprono la scorciatoia segreta della Via della Lega (salta due piani del dungeon). |
| ST-08 | **La guerra dell'acqua** (Calogero) | La mafia dell'acqua usa Pokémon Acqua/Terra (`Gastrodon`, `Quagsire`, `Octillery`) per prosciugare le condotte pubbliche e `Steelix` per ostruire gli acquedotti: inizia a Licata/Agrigento (ipogei e autobotti), riprende a Trapani (saline e mulini), a Lipari (dissalatore bloccato dai Pokémon Elettro/Acqua del custode) e a Enna (lago di Pergusa prosciugato). | Nel post-game le saracinesche e le sorgenti presidiate dai Pokémon d'acqua restano aperte solo dove il giocatore ha completato le missioni: le battute cambiano. |
| ST-09 | **La Prima Pietra** (Pippo) | In ogni provincia c'è un cartello «Ponte sullo Stretto — Posa della prima pietra (Cantiere Pokémon Autorizzato)». A ogni atto la data cambia (1971, 1985, 2003, 2012, 2026, «prossimamente»). Leggere i 9 cartelli è un collezionabile (`E-ST-09`). | Nel post-game il cartello di Torre Faro, accanto al `Piloni` (Steelix) di Pippo, dice «Posa della prima pietra: dopo le dimissioni del Presidente». |
| ST-10 | **I tagli del nastro** (Mistretta) | Mistretta appare **di persona** una volta per provincia, sempre irraggiungibile dietro il cordone di sicurezza e il suo `Gattupardu` (Persian) da compagnia: inaugura un ospedale senza Pokémon curatori, una strada interrotta dai `Graveler`, un depuratore senz'acqua. Il giocatore non può sfidarlo; può solo parlarci. | Piazza Armerina (`M-EN-06`). |
| ST-11 | **La cenere (`RinaDiL’Etna`)** | Dal Fontanarossa in poi i Pokémon vulcanici del Cratere Centrale (agitati dai roghi dolosi e dall'incuria) mantengono l'Etna in parossismo ricorrente (`FLAG_ETNA_ASH_ACTIVE`): meteo `RinaDiL’Etna` nell'area etnea e spazio aereo bloccato perché la SAC tiene chiusi negli hangar i Pokémon spazzatori. | `FLAG_ELICOTTERO_PRIVATO` a Messina (`M-ME-07`); la cenere resta per sempre come gag e condizione meteo. |
| ST-12 | **L'Atlante Biopolitico del Prof. Strano** | Il «vecchio professore disilluso» del Vermut è il **Prof. Alfio Strano**, zoologo in pensione dell'Università di Catania boicottato dai baroni perché studiava lo sfruttamento dei Pokémon da parte di «U Sistema». Consegna il Pokédex al Capitolo 1 e valuta il censimento per telefono. | Pokédex regionale completo → `Amuleto` (oggetto, Modulo 3) e diploma «ad honorem» di Ecologia Civica. |

### I compagni: arco, squadra iconica e missione personale

| Codice | Compagno | Si unisce | Squadra iconica e legame coi Pokémon | Missione personale (oltre alla sottotrama) | Ruolo nel post-game |
|---|---|---|---|---|---|
| C-01 | Turi | Capitolo 1 (Vermut) | `Foculavicu` (Typhlosion), `Faragghiuni` (Golem), `Gazzusa` (Ludicolo). Custodisce i 3 starter in una scatola di paste di mandorla dell'agrumeto paterno. | «Il cavallo di Santa Venera» (`S-CT-02`): recuperare il `Cavaddruzzu` (Ponyta/Rapidash) del padre ceduto per debiti a un allevatore del Carnevale di Acireale. | Ritrovo al Vermut (lunedì) |
| C-02 | Orazio | Capitolo 2 (San Cristoforo) | `Muturinu` (Yanmega), `Cavaddruzzu` (Rapidash), `Scippaturi` (Weavile). Addestra Pokémon veloci da corsa urbana e da officina. | `ST-04`: liberare i Pokémon meccanici e l'officina del fratello Nunzio dal «Pizzo Biologico» di `U Cassiere`. | Ritrovo in via Plebiscito (martedì) |
| C-03 | Christian | Capitolo 2 (Galermo) | `Borsellu` (Croagunk/Toxicroak), `Piranha` (Sharpedo), `Subwoofer` (Exploud). Usa Pokémon sonori per i sound-system dei lidi e della movida. | `ST-05`: smascherare il riciclaggio e le lotte-esibizione truccate del Privè Zagara e dei club VIP. | Ritrovo al Cubbar (sabato notte, 22:00–04:00 dell'orologio del DS) |
| C-04 | Chantal | Capitolo 2 (Librino) | `Unghiafinta` (Sneasel/Glameow), `Labbroni` (Jynx), `Regina` (Nidoqueen). I suoi Pokémon sono star di TikTok ma presidiano i ballatoi di Librino. | `ST-06`: dare la caccia ai 9 Cambiavoti e ai loro Pokémon spia fuori dai seggi elettorali. | Ritrovo al Palazzo di Cemento (mercoledì) |
| C-05 | Maria | Capitolo 1 (Vermut), poi Atto II | `Bilancia` (Alakazam), `Carruba` (Tropius), `Giustizia` (Lucario). Usa Pokémon Psico/Lotta per ricostruire le scene del crimine e decrittare i registri dei clan. | `ST-02`: raccogliere i 9 Atti sulle biotruffe del Sistema, pur sapendo che la politica li insabbierà. | Super-boss sul tetto del Palazzo di Giustizia di Catania (`P-02`) |
| C-06 | Totò | telefonata a fine Atto I; di persona a Palermo | `PaniCaMeusa` (Snorlax), `Vucciria` (Honchkrow), `Cappottu` (Gengar). I suoi Pokémon conoscono ogni vicolo di Ballarò e ogni passaggio segreto di Palazzo dei Normanni. | `ST-07`: recuperare i 9 faldoni sulle «quote Pokémon» dell'ARS nascosti nelle province. | Ritrovo a Ballarò (giovedì) |
| C-07 | Calogero | Capitolo 7 (Licata) | `Tratturi` (Donphan), `Siccità` (Hippowdon), `Spatula` (Gyarados). Lavora la terra arida e il mare col supporto dei suoi Pokémon da fatica. | `ST-08`: spezzare il racket dei Pokémon idrovori che prosciugano gli acquedotti per le autobotti. | Ritrovo al porto di Licata (venerdì) |
| C-08 | Pippo | Capitolo 9 (Torre Faro) | `Piloni` (Steelix), `Piscispata` (Lanturn/Empoleon), `Cariddi` (Cloyster). I suoi Pokémon presidiano da 35 anni il pilone e i traghetti dello Stretto. | `ST-09`: svelare l'archivio magnetico della Società Stretto Eterna e rimettere in volo l'elicottero del 2006. | Ritrovo a Ganzirri (domenica) |

---

## 2. Provincia di Catania (CT) — Atto I · ore 0–15 · Dossier 1

**Area dialettale:** orientale non metafonetica (catanese-etneo). Quartieri con registro proprio: Corso Italia (Catania «bene»), San Cristoforo/Tondicello (popolare stretto, rotacismo), San Giovanni Galermo (periferia + gergo giovanile), Librino (iper-popolare), Acireale/Timpa (acese). Gallo-italico: nessuno in provincia.
**Musiche guida (Modulo 5):** techno del Cubbar, «chill» del Vermut, caos di via Etnea, mercato della Pescheria, allarme della cenere.
**Operazioni di «U Sistema» nella provincia (R-10.3):** pizzo biologico nelle officine di San Cristoforo, riciclaggio con Pokémon da esibizione al Privè Zagara, monopolio elettrico/idrico nei condomini di Librino, incendi dolosi con Pokémon Fuoco sull'Etna, parassitismo agro-mafioso coi Pokémon Coleottero a Bronte, accaparramento dei Pokémon curatori nelle cliniche private (Segreteria 1) e blocco dei Pokémon spazzatori della cenere a Fontanarossa.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito / ricompensa |
|---|---|---|---|---|
| M-CT-00 | Prologo: la notte al Cubbar | Misterbianco, Cubbar | Flashback giocabile alle 3:30. Christian all'ingresso VIP col suo `Subwoofer` (Exploud) vicino alla console; tavoli con bottiglie, candele scintillanti e rampolli della Catania bene che sfoggiano Pokémon rari da salotto (`Gattupardu`/Persian, `Ninetales`) accanto ai figli dei boss coi loro `Houndoom`. Il giocatore parla con 6 NPC della movida (figli di avvocati, di magistrati, un PR), nessuna lotta. Uscita = dissolvenza. | `FLAG_INTRO_CUBBAR` |
| M-CT-01 | Il risveglio in Corso Italia | Catania, casa del protagonista | Ore 14:00. Camera con codici LUISS, diploma del Cutelli, lettera di non idoneità. La madre (Graziella), assistita in casa da un domestico `Mr. Mime` / `Delcatty`, urla dal salone che il figlio dell'avvocato Lombardo ha già aperto lo studio a Milano. Scelta del nome. | Inizio partita, `VAR_TRINACRIA_ATTO` = 1 |
| M-CT-02 | Il Vermut e la scintilla | Via Etnea → Via Gemmellaro | Attraversare via Etnea (promoter coi `Chatot` strilloni, `Munnizza`/Grimer che escono dai cassonetti stracolmi nei vicoli). Al Vermut: Turi, Maria, il Prof. Alfio Strano. L'auto blu dell'assessore blocca via Santa Filomena per gli arancini da Savia, mentre i suoi scagnozzi di «U Sistema» usano un `Koffing` (`Ciminièra`) e un `Rattata`/`Houndour` per intimidire un commerciante che si lamenta. Maria spiega come le inchieste sulle biotruffe vengano insabbiate; il Prof. Strano spiega che senza un Pokémon al proprio fianco nessuno in Sicilia ti riconosce autorità sul territorio. Turi regala lo **Starter** (`Focudda`/Cyndaquil, `Caimanu`/Totodile o `Ficurinia`/Chikorita) custodito in una scatola di paste di mandorla; il Prof. Strano consegna il **Pokédex** (Atlante Biopolitico). Prima lotta contro lo scagnozzo dell'assessore: il Pokémon starter cammina da ora a fianco del protagonista (R-10.4). | Starter, Pokédex, `FLAG_VERMUT_EPIPHANY`, Consenso 1 |
| M-CT-03 | San Cristoforo: l'officina e il pizzo biologico | San Cristoforo, via Plebiscito | Tra il fumo delle braci di carne di cavallo, Orazio è assediato nell'officina del fratello Nunzio: gli strozzini del clan locale (Livello 1 di «U Sistema») hanno piazzato dei `Ciminièra` (Koffing) e `Slugma` dentro il locale per intossicare l'aria e surriscaldare i motori («pizzo biologico», R-10.3), bloccando l'uscita coi `Machop`. Tre lotte contro gli strozzini nei vicoli + boss `B-CT-01` (Nino «U Strozzinu») per liberare l'officina e i Pokémon meccanici di Orazio. | Orazio nel gruppo, `SH 300 Scassatu` (bicicletta), `FLAG_RECRUIT_ORAZIO` |
| M-CT-04 | San Giovanni Galermo: la notte che paga | Galermo, case popolari → Plaia | Christian porta il giocatore dietro le quinte della movida: al «Privè Zagara» (inventato) i buttafuori di «U Sistema» usano `Persian` con la mossa `Pizzu` (Giornopaga) e lotte clandestine di `Sharpedo`/`Croagunk` nei retrobottega per ripulire montagne di contante sporco in fatture da tavoli VIP. Lotta con 3 buttafuori per recuperare i primi registri contabili. | `FLAG_RECRUIT_CHRISTIAN`, primo indizio ST-05 |
| M-CT-05 | Librino: i dieci piani dell'allaccio | Librino, Palazzo di Cemento | Ascensore rotto dal 1998 (i `Magnemite` del motore sono stati rubati anni fa): dungeon verticale `D-CT-02`. Chantal, al 7° piano nel suo salone di unghie abusivo (dove una `Sneasel`/`Unghiafinta` lima i gel coi propri artigli), spiega che il Capo-Condominio (`B-CT-02`), affiliato a «U Sistema», usa Pokémon Elettro per controllare l'allaccio abusivo alla rete e Pokémon Acqua/Veleno al 10° piano per chiudere l'acqua della cisterna alle famiglie che non firmano per il candidato di Mistretta. Sconfiggerlo riapre l'acqua a tutto il palazzo. | `FLAG_RECRUIT_CHANTAL`, Consenso +3 |
| M-CT-06 | L'Etna che brucia (La biotruffa boschiva) | Nicolosi, Pineta dei Monti Rossi → Crateri Silvestri | Un incendio doloso divampa sulla pineta lavica: non è autocombustione, ma un'operazione di «U Sistema» (R-10.3). L'Incendiario della Forestale (`B-CT-03`, inventato) usa `Slugma` e `Magmar` addestrati per bruciare parcelle catastali precise e far impazzire i Pokémon selvatici dell'Etna, così che la ditta amica incassi prima l'appalto d'urgenza di «contenimento fauna vulcanica» e poi i fondi di rimboschimento coi Pokémon Erba. Dungeon `D-CT-01`; sconfiggere l'Incendiario calma i Pokémon della montagna. | Consenso +3, MT (Modulo 3) |
| M-CT-07 | L'Oro Verde e gli sciami del clan | Bronte | Il cartello agro-mafioso (inventato) del pistacchio taglieggia i piccoli coltivatori sulla sciara lavica: chi rifiuta di conferire il raccolto a metà prezzo ai magazzini di Don Saro (`B-CT-04`) si ritrova di notte il pistacchieto divorato dagli sciami di `Yanma`, `Pinsir` e `Scyther` addestrati dal clan, mentre i `Graveler` sbarrano i cancelli delle masserie. Dungeon `D-CT-03`; sconfitta del cartello e liberazione dei terreni. | Consenso +3 |
| M-CT-08 | Segreteria 1: il Ras dei Pokémon Curatori | Catania, Palazzo degli Elefanti | Dungeon-ufficio: corridoi con code infinite di pazienti e sportelli «torna domani». Mentre i Centri pubblici sono al collasso, i 4 allenatori della Segreteria (Primario, Convenzionato, Informatore, Centralinista) e il boss **Dott. Ignazio Calì** (Ras delle cliniche convenzionate, Livello 3 di «U Sistema») hanno monopolizzato tutti i Pokémon terapeutici (`Chansey`, `Clefable`, `Miltank`) per fatturare rimborsi regionali d'oro sulle liste d'attesa. Tipo **Normale**, asso Chansey L18. Sconfiggerlo sblocca il servizio pubblico e la MN `Martiddata`. | **Dossier Liotru**, `FLAG_DOSSIER_CT`, comizio ST-01 a Piazza Duomo |
| M-CT-09 | L'incubo di Fontanarossa e i Pokémon spazzatori | Aeroporto di Catania-Fontanarossa, Terminal A | Telefonata di Totò: il cavillo della Commissione Elettorale impone il deposito del pre-contrassegno entro 3 ore. A19 spezzata dai cantieri, unica via il volo delle 12:30. Alla rotonda dell'aeroporto i Pokémon vulcanici del Cratere Centrale (disturbati dai roghi di `M-CT-06`) entrano in parossismo: parte la pioggia di cenere nera (`FLAG_ETNA_ASH_ACTIVE`, primo `Warp` di aggiornamento, meteo `RinaDiL’Etna`). Terminal A: tabelloni «CANCELLATO», migliaia di passeggeri a terra, acqua a 5 euro, nessuna navetta. Nel dungeon `D-CT-04` (rivolta dei passeggeri contro la SAC) si scopre che il **Direttore Operativo dello Scalo** (inventato) tiene chiusi negli hangar VIP i Pokémon spazzatori Terra/Acciaio (`Donphan`, `Skarmory`, `Forretress`) per fatturare alla Regione «sgomberi straordinari d'emergenza» e si rifiuta di dirottare i voli su Comiso. Sconfitto il Direttore, il suo `Porygon2`/`Magneton` libera i terminali telematici della Sala VIP: Maria invia la PEC con firma digitale. | `FLAG_FONTANAROSSA_ASH_CRISIS`, `FLAG_SAC_VIP_LOUNGE_PEC_SENT`, Consenso +3, fine Atto I: si prosegue a piedi verso Siracusa |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo e passi (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-CT-01 | Il santino sbagliato (ST-03) | Turi, Piazza Università | Turi ha fatto stampare da una tipografia economica (che usa `Smeargle` sottopagati) 10.000 santini col nome del protagonista sbagliato. Ritrovare i 5 pacchi distribuiti per errore (via Etnea, Villa Bellini, Pescheria, Castello Ursino, Ognina) prima che i `Murkrow` dei giornalisti li vedano. | Consenso +1, `ITEM_AMULET_COIN` |
| S-CT-02 | Il cavallo di Santa Venera (C-01) | Turi, Acireale, discesa della Timpa | Il `Cavaddruzzu` (Ponyta/Rapidash) del padre di Turi è finito a un allevatore legato ai salotti acesi che vuole sfruttarlo per le parate del Carnevale. Gara di corsa in scooter (`SH 300 Scassatu`) lungo la Timpa (minigioco a tempo) e lotta col nobile decaduto `B-CT-05`, all'aperto sulla Timpa (R-09.3). | Consenso +1, Pokémon di tipo Fuoco (Modulo 3) |
| S-CT-03 | La granita di mezzanotte | Gelataio, Acireale, Piazza Duomo | Il Pokémon Ghiaccio del bar è stremato dal caldo: portare 3 granite a 3 NPC sparsi prima che si sciolgano (timer di 60 secondi tra le mappe). | `GranitaConzu` ×5 |
| S-CT-04 | Ciclopi | Pescatore anziano, Aci Trezza | Il pescatore racconta che i Faraglioni «sono rocce lanciate da un antico Pokémon gigante con un occhio solo contro le navi». Lotta in barca tra i Faraglioni contro 4 pescatori e i loro Pokémon marini (`Tentacool`, `Krabby`, `Corsola`). | Consenso +1, `ITEM_SUPER_ROD` |
| S-CT-05 | Le Salinelle | Geologo, Paternò | I vulcanetti di fango delle Salinelle (habitat naturale di `Wooper`, `Grimer` e `Slugma`) sono stati venduti dal comune per farci un parcheggio privato: raccogliere 4 campioni biologici di fango (punti di ispezione) per bloccare il cantiere con un vincolo faunistico. | Consenso +1, MT |
| S-CT-06 | Il Ponte dei Saraceni | Anziana, Adrano | Il ponte medievale sul Simeto è chiuso per «verifiche statiche dal 2009», presidiato dai `Geodude` del geometra comunale (inventato) che ha perso il fascicolo per incassare l'indennità di monitoraggio: batterlo per riaprire il passaggio. | Consenso +1, Pietra (Modulo 3) |
| S-CT-07 | I 142 gradini | Ceramista, Caltagirone, Scalinata di Santa Maria del Monte | Sfida a piani: 142 gradini divisi in 7 rampe (7 terrazze della stessa mappa, R-09.2), un allenatore artigiano per rampa coi suoi Pokémon Roccia/Fuoco da fornace (`Baltoy`, `Numel`, `Magby`), senza curarsi (`D-CT-05`). Il maestro ceramista aspetta in cima. | Consenso +1, `ITEM_LEFTOVERS` |
| S-CT-08 | La Circumetnea | Capostazione, Randazzo (binario all'aperto, R-09.3) | La littorina della Circumetnea si ferma ovunque perché branchi di Pokémon lavici e scagnozzi del cartello occupano i binari. Viaggio scriptato Randazzo–Bronte con 3 soste impreviste (una lotta per sosta) nella mappa di scena del treno. | Consenso +1, apre la Grotta del Gelo (`D-CT-06`) |
| S-CT-09 | Sant'Agata (evento a calendario) | Devoto, Cattedrale | Dal 3 al 5 febbraio (orologio del DS): processione con le candelore; il giocatore e il suo Pokémon a seguito aiutano i portatori a tenere in equilibrio una candelora lungo la salita (minigioco di equilibrio). | Strumento raro (Modulo 3) |
| S-CT-10 | Cambiavoti di Catania (ST-06) | Chantal, scuola-seggio di Librino | Trovare il Cambiavoti di «U Sistema» tra 8 NPC davanti al seggio (indizio: telefono in mano, busta di contanti e un `Murkrow`/`Natu` appollaiato che spia dentro le finestre della cabina elettorale). Lotta per cacciarlo dal seggio. | Consenso +1 |

### Dungeon

| Codice | Nome | Piani / struttura | MN richieste | Selvatici ed ecologia (tema) | Boss finale |
|---|---|---|---|---|---|
| D-CT-01 | Crateri Silvestri e Monti Rossi | 3 aree: pineta in fiamme, colata del 2001, bocca spenta (2 mappe, R-09.1) | — | Fuoco, Roccia, Volante (`Taddarita`/Zubat nei tubi di lava, `Slugma` e `Houndour` agitati dai roghi dolosi) | B-CT-03 |
| D-CT-02 | Palazzo di Cemento di Librino | 10 piani a scale in 5 mappe da 2 piani (R-09.1); ballatoi con cavi tenuti da `Magnemite` abusivi; panni stesi che bloccano i corridoi (si spostano parlando con chi li ha stesi) | — | nessun selvatico; 9 allenatori del condominio e scagnozzi del racket degli allacci (uno per piano) | B-CT-02 al 10° |
| D-CT-03 | Sciara dei pistacchi (Bronte) | 2 aree di campagna lavica a terrazze, cancelli del cartello sbarrati da Pokémon Roccia (1 mappa) | — | Erba, Coleottero, Terra (sciami che infestano i pistacchieti) | B-CT-04 |
| D-CT-04 | Terminal A di Fontanarossa | 4 aree in 2 mappe: atrio + controlli di sicurezza, gate + sala VIP | — | nessun selvatico; 8 allenatori («Bagaglisti Esauriti», «Funzionari SAC» inventati coi Pokémon spazzatori tenuti fermi, «Turisti Accaldati») | Direttore Operativo dello Scalo |
| D-CT-05 | Scalinata di Santa Maria del Monte | 7 rampe = 7 terrazze consecutive della cella sud di Caltagirone (R-09.2) | — | — | Ceramista (S-CT-07) |
| D-CT-06 | Grotta del Gelo (Randazzo, versante nord) | 2 piani di ghiaccio perenne dentro la lava (1 mappa), dove sopravvivono gli unici Pokémon Ghiaccio dell'Etna | `Martiddata` | Ghiaccio, Roccia (`Swinub`, `Sneasel`, `Zubat`) | B-CT-06 (opzionale) |
| D-CT-07 | Sotterranei del Castello Ursino | 3 piani scavati sotto il fossato lavico del 1669 (1 mappa) | `Scalaroccia` | Spettro, Roccia (`Gastly`, `Misdreavus`, `Geodude`) | post-game P-05 |

### Boss secondari

| Codice | Nome (inventato) | Ruolo in «U Sistema» o nel territorio | Tipo | Livello asso |
|---|---|---|---|---|
| B-CT-01 | Nino «U Strozzinu» | capozona del «pizzo biologico» di San Cristoforo (affumica le officine coi `Koffing` e sabota gli scooter coi `Weavile`/`Sneasel`) | Buio | 12 |
| B-CT-02 | Il Capo-Condominio | gestisce gli allacci abusivi coi Pokémon Elettro, la cisterna d'acqua sul tetto e i pacchi elettorali a Librino | Normale/Veleno | 14 |
| B-CT-03 | L'Incendiario della Forestale | appicca roghi mirati coi `Slugma`/`Magmar` per incassare gli appalti di contenimento e rimboschimento | Fuoco | 15 |
| B-CT-04 | Don Saro del Pistacchio | capo del cartello dell'Oro Verde (usa sciami di Pokémon Coleottero per punire i contadini che non cedono il raccolto) | Erba/Terra | 16 |
| B-CT-05 | Il Barone della Timpa | nobile decaduto di Acireale che requisisce i `Ponyta`/`Rapidash` per le sfilate del Carnevale | Fuoco/Normale | 17 |
| B-CT-06 | Il Custode del Gelo | eremita-speculatore che estrae coi suoi Pokémon Ghiaccio il ghiaccio perenne dell'Etna per venderlo «DOP» ai club VIP | Ghiaccio | 20 |

### Meme ed easter egg

| Codice | Contenuto |
|---|---|
| E-CT-01 | Il Liotru di Piazza Duomo (antico idolo di lava scolpito a forma di `Donphan`/`Phanpy`): parlandoci 10 volte di fila dice «…» poi «Ancora qui sei?». |
| E-CT-02 | «Arancinu» vs «arancina»: a Catania ogni NPC che vende arancini (accompagnato da un Pokémon di fuoco che tiene caldo l'olio) corregge il giocatore se usa la parola palermitana (scelta Sì/No). Ricompensa diversa a Palermo (`E-PA-01`). |
| E-CT-03 | Il cartello della Circumetnea con l'orario «indicativo (salvo attraversamento Tauros sui binari)». |
| E-CT-04 | Il motorino parcheggiato sul marciapiede di via Etnea (sorvegliato da un `Meowth` col borsello) che sposta posizione a ogni visita. |
| E-CT-05 | ST-09: primo cartello della «Posa della prima pietra» davanti alla stazione centrale. |
| E-CT-06 | Una bottiglietta d'acqua a 5 € al bar del Terminal A (strumento comprabile: identico all'`AcquaFuntana`, costa 10 volte tanto perché «filtrata da Pokémon d'élite»). |

---

## 3. Provincia di Siracusa (SR) — Atto II · ore 15–22 · Dossier 2

**Area dialettale:** siracusano settentrionale non metafonetico (Augusta, Priolo, Melilli, Lentini, Siracusa città); siracusano meridionale verso Noto, Avola, Pachino (tratti sud-orientali). Musica: «cortina di fumo» industriale, barocco di Noto, mare di Ortigia.
**Meteo speciale:** nebbia giallastra ad Augusta, a Priolo e nel polo petrolchimico (valore meteo 9, da verificare a schermo; in alternativa sole e tinta gialla del Modulo 4: R-09.7), generata dalle emissioni di `Smog` dei Pokémon Veleno usati come inceneritori viventi dal polo!
**Operazioni di «U Sistema» nella provincia (R-10.3):** smaltimento illecito di fanghi chimici tramite colonie di `Ciminièra`/`Priolu` e `Sacconiru` nei serbatoi di Augusta-Priolo, occupazione dei magazzini agrumari di Lentini, privatizzazione VIP del mare di Marzamemi con barriere di Pokémon Acqua, e racket delle concessioni e delle catene portuali a Ortigia (Segreteria 2).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-SR-01 | La SS114 a piedi | SS114 Catania–Augusta | Lunga strada costiera oltre la foce del Simeto (con blocchi di cemento dei clan da frantumare con `Martiddata`); prima comparsa del Cambiavoti di Siracusa/Lentini (`ST-06`) col suo Pokémon spia. | — |
| M-SR-02 | La cortina di fumo e gli inceneritori viventi | Augusta → Priolo → Melilli | Operai e pescatori mostrano i Pokémon marini intossicati nella rada megarese. I dirigenti del petrolchimico (inventati, finanziatori di Mistretta) usano colonie di `Ciminièra` (Koffing), `Priolu` (Weezing) e `Sacconiru` (Muk) chiuse nei serbatoi come **inceneritori biologici gratuiti**: danno loro in pasto i fanghi industriali e li costringono a espellerli di notte come nebbia gialla (`Smog`/`Nube`). Il giocatore entra nel polo (`D-SR-01`), abbatte le barriere con `Martiddata`, sconfigge `B-SR-01` e fotografa lo scarico chimico. | Consenso +3, `FLAG_AUGUSTA_REFINERY_CLEARED` |
| M-SR-03 | La Mafia dei VIP in tonnara | Marzamemi e Noto | Tonnara di Marzamemi trasformata in club esclusivo con concessione demaniale a 200 € l'anno (inventato); invasione di turisti milanesi radical-chic in piazza Regina Margherita. I gestori legati a «U Sistema» (`ST-05`) usano `Gyarados`, `Corsola` e `Lanturn` illuminati al neon per sbarrare il mare ai pescatori locali e organizzare scommesse VIP nella «camera della morte» della tonnara (`D-SR-03`). Galà in tonnara, 4 lotte con i «Concessionari» e boss `B-SR-03`. | Consenso +3, `FLAG_MARZAMEMI_VIP_BUSTED` |
| M-SR-04 | Maria a Ortigia | Siracusa, Fonte Aretusa | Davanti ai papiri della Fonte Aretusa (dove nuotano `Goldeen` e `Dewgong` d'acqua dolce), Maria arriva da Ragusa col suo `Bilancia` (Alakazam) e consegna il primo Atto (`ST-02`), illustrando come la Cupola Grigia controlli le boccature dei porti tramite i Pokémon marini. | — |
| M-SR-05 | Segreteria 2: il Barone delle Concessioni Portuali | Ortigia, Castello Maniace | Dungeon nel castello (`D-SR-04`) dove i Pokémon Acqua della Segreteria alzano e abbassano il livello delle maree allagando le passerelle a orari fissi. Boss: **Comm. Corrado Spataro**, «U Baruni dû Portu» (Livello 3 di «U Sistema»), che usa `Tentacruel` e `Lanturn` per bloccare le eliche di qualsiasi peschereccio o nave mercantile che non paghi il dazio alla sua cooperativa portuale. Tipo **Acqua**, asso Lanturn L25. Sconfiggerlo sblocca la MN `Roncigghiu` (Taglio). | **Dossier Aretusa**, `FLAG_DOSSIER_SR`, comizio in piazza Duomo di Ortigia |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-SR-01 | Il jingle neomelodico (ST-03) | Turi, Siracusa, Corso Matteotti | Turi ha inciso un jingle elettorale imbarazzante facendolo cantare a un coro di `Chatot` e `Jigglypuff`. Ritirare i nastri dalle 4 radio di quartiere (lotta con ogni DJ e i suoi Pokémon sonori/Elettro). | Consenso +1 |
| S-SR-02 | L'Orecchio di Dionisio | Guida turistica, Neapolis | Nella grotta dall'acustica perfetta, un branco di `Zubat` (`Taddarita`) e `Whismur` ripete ogni suono: minigioco dell'eco (ripetere sequenze di versi/SFX di HeartGold) per calmare la colonia. | MT |
| S-SR-03 | Le arance di Lentini | Agrumicoltore, Lentini | I vecchi magazzini dell'arancia rossa sono occupati dai caporali di «U Sistema» che usano `Machoke` e `Arbok` per impedire agli agricoltori di caricare le cassette se non pagano la mediazione del clan: liberare i 3 magazzini. | Consenso +1, bacche (Modulo 3) |
| S-SR-04 | Il Biviere | Birdwatcher, Lentini (cella ovest, R-09.2) | Censire per l'Atlante del Prof. Strano (`ST-12`) 5 specie di Pokémon Volante/Acqua migratori sul lago del Biviere (5 punti di osservazione). | `ITEM_SOOTHE_BELL` |
| S-SR-05 | Vendicari (zona Safari) | Guardiaparco, Noto | Oasi faunistica libera dallo sfruttamento di «U Sistema», con fenicotteri/Pokémon acquatici e biglietto d'ingresso: è la **Zona Safari di HeartGold** (cattura ecologica con strumenti a numero limitato), divisa in 14 habitat reali della riserva (R-09.4). | accesso permanente |
| S-SR-06 | La granita del Caffè | Cameriere, Noto, Corso Vittorio Emanuele | Consegna della granita di mandorla (tenuta fresca dal Pokémon del giocatore) a un anziano in cima alla scalinata della Cattedrale che non può più scendere. | Consenso +1 |
| S-SR-07 | Isola delle Correnti | Pescatore, Portopalo | L'estremo sud dove si scontrano i Pokémon dello Ionio e del Canale di Sicilia (cella sud di Portopalo, R-09.2): raggiungere l'isolotto con la bassa marea (orario del DS 6:00–9:00) e battere il Guardiano del Faro (`Ampharos`/`Starmie`). | Consenso +1, pietra rara |
| S-SR-08 | Il Nero d'Avola | Vignaiola, Avola | Gli scagnozzi dei mediatori vinicoli hanno nascosto coi loro `Murkrow` 6 casse di mosto pregiato nei cortili della pianta esagonale della città (indizi sui muri). | Consenso +1 |
| S-SR-09 | Cambiavoti di Siracusa (ST-06) | Chantal (telefono), Avola, scuola | Individuare e sconfiggere il Cambiavoti di Siracusa e il suo Pokémon spia (`Natu`/`Sableye`) appostato fuori dal seggio scolastico. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-SR-01 | Polo petrolchimico (Augusta–Priolo) | 4 aree in 2 mappe: pontili + serbatoi, sala controllo + torcia (R-09.1) | `Martiddata` (barriere di calcestruzzo del polo) | Veleno (`Ciminièra`, `Priolu`, `Sacconiru`), Acciaio (`Magnemite`), Elettro (`Voltorb`) | B-SR-01 |
| D-SR-02 | Latomie del Paradiso | 2 aree in cava (1 mappa: Latomia del Paradiso, Orecchio di Dionisio) | — | Roccia, Spettro, Buio (antichi Pokémon rimasti nelle prigioni di pietra) | B-SR-02 |
| D-SR-03 | Tonnara di Marzamemi | 2 aree in 1 mappa (camera della morte, magazzini del club con reti da tagliare) | `Roncigghiu` | Acqua (`Tentacool`, `Chinchou`, `Remoraid`) | M-SR-03 / B-SR-03 |
| D-SR-04 | Castello Maniace | 3 aree a marea in 2 mappe: ingresso + cortile a marea regolata dai Pokémon d'acqua, sala della Segreteria | — | Acqua | Segreteria 2 |

### Boss secondari

| Codice | Nome (inventato) | Ruolo in «U Sistema» o nel territorio | Tipo | Liv. |
|---|---|---|---|---|
| B-SR-01 | L'Ing. della Torcia | dirigente del polo che usa i `Priolu` (Weezing) per bruciare scarti tossici di notte sostenendo che «la fiamma della torcia è solo l'aura naturale dei Pokémon» | Veleno/Acciaio | 23 |
| B-SR-02 | Il Tiranno delle Latomie | guida abusiva affiliata al racket turistico che usa Pokémon Spettro per spaventare i visitatori e far pagare il «pizzo dell'eco» | Spettro | 22 |
| B-SR-03 | La Concessionaria di Marzamemi | referente di `ST-05` che recinta il mare demaniale coi `Gyarados` e `Lanturn` per i tavoli VIP da 500 € | Acqua/Volante | 24 |

### Meme ed easter egg

E-SR-01 La statua di Archimede a Ortigia: un NPC spiega che gli «specchi ustori» erano in realtà una schiera di `Alakazam` e `Magmar` con `Giorno di Sole` + `Solarraggio`, chiede «Eureka?» e regala una `Pietra` se si risponde «Sì». · E-SR-02 Il cartello del Ponte (`ST-09`) in piazza Pancali. · E-SR-03 Il turista milanese a Marzamemi col suo `Snubbull` con la pettorina firmata che ordina «una granita al pistacchio di Bronte, ma senza zucchero, senza pistacchio e cruelty-free per il mio Pokémon». · E-SR-04 L'`Ampharos` in cima al faro di Capo Passero che lampeggia in codice Morse «MUNNIZZA».

---

## 4. Provincia di Ragusa (RG) — Atto II · ore 22–30 · Dossier 3

**Area dialettale:** sud-orientale ibleo (ragusano, modicano, vittoriese), metafonetico. Maria passa dall'italiano giuridico all'ibleo intimo.
**Musica:** barocco ibleo, mercato all'alba, «cattedrale nel deserto» di Comiso (eco, luci a risparmio).
**Operazioni di «U Sistema» nella provincia (R-10.3):** racket della catena del freddo (Pokémon Ghiaccio) e del marciume indotto (Pokémon Erba/Veleno) al Mercato Ortofrutticolo di Vittoria, sabotaggio elettromagnetico dei radiofari dell'Aeroporto di Comiso tramite Pokémon Elettro/Acciaio per proteggere il monopolio dei TIR su gomma, e cartello dei magazzini refrigerati a Ragusa Ibla (Segreteria 3).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-RG-01 | Ibla e Modica | Ragusa Superiore → scale → Ibla; Modica Bassa/Alta | Ritrovo con Maria e il suo `Carruba` (Tropius): indaga sul racket logistico di Vittoria. A Modica l'antico laboratorio di cioccolato (dove i Pokémon Fuoco/Roccia scaldano la pietra metate a bassa temperatura senza sciogliere i cristalli di zucchero) funge da rifugio e Centro Pokémon locale (R-09.5). | — |
| M-RG-02 | Il mercato all'alba e il racket del freddo | Vittoria, Mercato Ortofrutticolo | Infiltrazione alle 4:00 (`D-RG-01`): i caporali di «U Sistema» (inventati) impongono i prezzi alla cassa usando **Pokémon Ghiaccio** (`Piloswine`, `Sneasel`, `Cloyster`) per refrigerare gratis solo i TIR della propria ditta e **Pokémon Erba/Veleno** (`Victreebel`, `Vileplume`) per spargere spore che fanno marcire in un'ora le cassette dei contadini che viaggiano in proprio. Tagliare le reti abusive con `Roncigghiu` e battere `B-RG-01` libera le aste. | Consenso +3, `FLAG_VITTORIA_MARKET_LIBERATED` |
| M-RG-03 | La cattedrale nel deserto e il jamming radar | Comiso, Aeroporto «Pio La Torre» | Terminal civile nuovo e deserto: luci a risparmio, un bar chiuso, nastri fermi, nessun Pokémon d'assistenza a terra. I pochi lavoratori raccontano (come opinione) che Comiso è tenuto al minimo come «ruota di scorta sgonfia» per non togliere voli e parcheggi a Catania. Il giocatore trova le carte (inventate) del «Piano Scalo Unico» e scopre il sabotaggio fisico: nei bunker e nella sala radar dell'ex base NATO (`D-RG-02`), i caporali del trasporto su gomma usano `Magneton`, `Electrode` e `Bronzong` per **disturbare con onde elettromagnetiche i radiofari di atterraggio**, così nessun cargo ortofrutticolo o volo dirottato può atterrare a Comiso e tutto deve viaggiare sui TIR del cartello! Sconfitta dei caporali e di `B-RG-02`: la pista è libera. | Consenso +3, `FLAG_COMISO_SAC_GHOST_AIRPORT` |
| M-RG-04 | Segreteria 3: il Monopolista della Logistica | Ragusa Ibla, Palazzo (inventato) di via del Mercato | Dungeon a magazzini refrigerati (pavimento ghiacciato dai `Dewgong`/`Piloswine` della logistica, puzzle di scivolamento). Boss: **Cav. Biagio Occhipinti**, re dei TIR dell'ortofrutta e della catena del freddo (Livello 3 di «U Sistema»). Tipo **Erba**, asso Victreebel L31 (affiancato da Pokémon che sfruttano clima e spore). Sconfiggerlo consegna il Dossier e sblocca la MN `Spallata` (Forza). | **Dossier Carrubba**, `FLAG_DOSSIER_RG`, comizio al Giardino Ibleo |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-RG-01 | Il video coi cavalli (ST-03) | Turi, Modica | Turi ha girato uno spot elettorale facendo galoppare dei `Ponyta` sul viadotto Guerrieri e bloccando il traffico. Rimuovere il cartellone abusivo (lotta col fotografo e il suo `Smeargle`/`Flash`). | Consenso +1 |
| S-RG-02 | Cioccolato azteco | Cioccolataia, Modica Alta | La ricetta tradizionale per i Pokémon: recuperare 3 ingredienti in 3 comuni (cacao sbarcato coi `Pelipper` al porto di Pozzallo, zucchero nei magazzini di Vittoria, spezie macinate coi Pokémon Erba a Scicli). | `CiucculataModica` ×5 (Modulo 3) |
| S-RG-03 | Il commissariato della TV | Comparsa, Scicli, via Mormino Penna | I pullman di turisti cercano i luoghi del commissario televisivo ma gli scagnozzi dei tour operator abusivi li spennano: guidare un gruppo con l'aiuto del proprio Pokémon a seguito nei 4 luoghi giusti. | Consenso +1 |
| S-RG-04 | La terrazza di Punta Secca | Bagnante, Santa Croce Camerina | Ritrovare l'asciugamano «del commissario» rubato da un `Krabby`/`Wingull` selvatico sulla spiaggia sotto il faro. | Strumento (Modulo 3) |
| S-RG-05 | Cava d'Ispica | Archeologo, Ispica | Dungeon rupestre `D-RG-03` abitato da antichi Pokémon Roccia/Spettro; 5 tombe sicule con iscrizioni (puzzle di sequenza). | Fossile (Modulo 3) |
| S-RG-06 | Torre Cabrera | Guardiano, Pozzallo | Aiutare il `Magmar`/`Focudda` del guardiano a riaccendere il braciere della torre costiera per la sagra del pesce (consegnare legna secca). | Consenso +1 |
| S-RG-07 | Il Loggiato del Sinatra | Ristoratore, Ispica | Sfida culinaria per umani e Pokémon: indovinare 3 piatti tipici iblei dagli indizi degli ingredienti e delle bacche. | `ITEM_LUCKY_EGG` |
| S-RG-08 | Cambiavoti di Ragusa (ST-06) | Chantal (telefono), Vittoria, scuola | Scovare il Cambiavoti di Vittoria e il suo Pokémon spia (`Murkrow`/`Haunter`) che controlla le schede dalle grate della scuola. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-RG-01 | Mercato di Vittoria | 3 padiglioni (1 mappa da 3 stanze) + piazzale dei TIR (TIR in movimento a tempo refrigerati dai Pokémon Ghiaccio del clan) | `Roncigghiu` (casse e reti) | Erba, Coleottero, Veleno (spore nei padiglioni) | B-RG-01 |
| D-RG-02 | Ex base NATO di Comiso | 4 aree in 2 mappe: hangar + bunker, sala radar + pista (disturbata dai Pokémon Elettro/Acciaio dei sabotatori) | `Martiddata` | Acciaio, Elettro, Volante (`Magnemite`, `Voltorb`, `Zubat`) | B-RG-02 |
| D-RG-03 | Cava d'Ispica | 3 aree rupestri in 1 mappa (necropoli, Larderia, grotte alte) | `Spallata` (sblocco massi al ritorno) | Roccia, Spettro (`Geodude`, `Gastly`, `Cubone`) | — |

### Boss secondari

B-RG-01 **Il Caporale dei TIR** (usa Pokémon Normale/Acciaio e Ghiaccio per bloccare le banchine di carico e refrigerare solo i camion del clan; 28) · B-RG-02 **Il Generale in Congedo** che vive nel bunker NATO «per abitudine» e presta i suoi Pokémon Acciaio/Volante ai sabotatori del radar di Comiso (30) · B-RG-03 **La Marchesa di Ibla**, che usa Pokémon Psico (`Espeon`, `Mr. Mime`) per decidere chi ha il sangue abbastanza blu da entrare nei palazzi barocchi (29).

### Meme ed easter egg

E-RG-01 Il bar chiuso del terminal di Comiso: dietro il bancone c'è solo uno `Slakoth` addormentato; parlandoci, «Riapriamo quando arriva un volo». · E-RG-02 Le scale di Ibla contate a schermo (340, numero mostrato da un cartello: gag «Il comune dice 340, i turisti 3.400, il mio Pokémon si è rifiutato al gradino 12»). · E-RG-03 Cartello ST-09 a Pozzallo. · E-RG-04 Il gigantesco serbatoio refrigerato di carrubbe del Monopolista (fatturato alla UE per 10.000 tonnellate) che contiene… un solo `Bellsprout` e un solo carrubo.

---

## 5. Provincia di Caltanissetta (CL) — Atto III · ore 30–37 · Dossier 4

**Area dialettale:** centrale metafonetica (nisseno); Gela con tratti propri; Niscemi e Mazzarino verso il sud-orientale. Riesi con la comunità valdese (italiano).
**Ambiente:** valloni, frane mai riparate (puzzle `Spallata` e `Martiddata`), zolfare dismesse.
**Operazioni di «U Sistema» nella provincia (R-10.3):** **frane programmate coi Pokémon Roccia/Terra** (`Rhydon`, `Graveler`, `Dugtrio`) la notte prima di ogni collaudo stradale per ottenere perizie di variante infinite e prorogare i commissariamenti per decenni (Segreteria 4); **scavo di pozzi segreti coi Pokémon Terra sotto lo scudo elettromagnetico del MUOS** di Niscemi per seppellire rifiuti industriali tossici.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-CL-01 | La strada che non c'è e le frane a comando | SS626 / trazzere | Frane «provvisorie dal 2005»: il giocatore usa i propri Pokémon con `Spallata` e `Martiddata` per aprire tre varchi tra i valloni e sorprende i manovali di una ditta in subappalto che stanno ordinando ai loro `Graveler` e `Dugtrio` di usare `Frana` sulla carreggiata appena riparata («Mbare, se la strada regge ci tolgono la cassa in deroga!»). | — |
| M-CL-02 | Gela: l'acropoli e il pontile | Gela | Contrasto tra le mura greche di Timoleonte (dove nidificano Pokémon Roccia/Volante) e le ciminiere spente dell'ex petrolchimico invase da `Grimer` e `Magnemite` selvatici; sul lunghissimo pontile sbarcatoio spazzato dal vento si affronta il Cambiavoti di Caltanissetta/Gela (`ST-06`). | Consenso +3 |
| M-CL-03 | Le parabole del MUOS e i pozzi chimici | Niscemi, Sughereta → stazione | Dungeon sci-fi a onde (`D-CL-02`): i Pokémon Elettro/Psico (`Magneton`, `Kadabra`, `Electabuzz`) piazzati attorno alle gigantesche parabole amplificano i «campi» che invertono i comandi a tempo per tenere lontani i curiosi. Sotto la copertura radar, una ditta dell'ecomafia (inventata) usa `Dugtrio`, `Sandslash` e `Muk` per scavare pozzi nella sughereta e interrare fusti di rifiuti speciali sotto il perimetro della base. Nessuna battuta sulle famiglie sgomberate dalla frana (R-05). | Consenso +3, `FLAG_NISCEMI_MUOS_QUEST` |
| M-CL-04 | Segreteria 4: il Commissario delle Opere Incompiute | Caltanissetta, viadotto (inventato) «Salso 2» | Dungeon sul viadotto di 400 m mai finito (`D-CL-04`): piloni a quote diverse collegati da passerelle provvisorie, dove i capi-cantiere usano `Machoke` e `Graveler` per montare e smontare gli stessi ponteggi da vent'anni. Boss: **Ing. Calogero Lo Monaco**, commissario straordinario da 22 anni (Livello 3 di «U Sistema»), che usa il suo **Rhydon L37** con `Scussuni` (Terremoto) per lesionare scientificamente il pilone numero 3 prima di ogni collaudo finale e incassare una nuova perizia di variante milionaria. Sconfiggerlo consegna il Dossier e sblocca `Aliscafu` (Surf). | **Dossier Pirrera**, `FLAG_DOSSIER_CL`, comizio in Corso Umberto |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-CL-01 | Il santino in dialetto (ST-03) | Turi, Caltanissetta | Turi ha scritto il santino «in nisseno» usando parole catanesi e ha disegnato il Pokémon simbolo della città al contrario: correggerlo parlando con 4 anziani in Corso Umberto (scelte multiple). | Consenso +1 |
| S-CL-02 | Il Castello di Mussomeli | Custode, Mussomeli | Dungeon medievale `D-CL-01` sulla rupe calcarea, infestato dai Pokémon Spettro legati alla leggenda delle tre dame murate vive. | MT |
| S-CL-03 | Le case a 1 euro | Coppia di stranieri, Mussomeli | Hanno comprato un rudere a 1 euro per ristrutturarlo coi loro Pokémon, ma sono bloccati dalla burocrazia comunale: 5 uffici, 5 timbri (giro tra NPC e funzionari pigri coi loro `Slowpoke`). | Consenso +1 |
| S-CL-04 | La zolfara di Gabbara | Ex minatore, San Cataldo | Dungeon `D-CL-03` nelle gallerie di zolfo abbandonate, dove vivono ancora i vecchi `Koffing`, `Geodude` e `Sandshrew` che un tempo estraevano il minerale; il minatore racconta la storia dei carusi delle zolfare (tono sobrio, R-05). | Pietra (Modulo 3) |
| S-CL-05 | Monte degli Ulivi | Pastore valdese, Riesi | Consegna di provviste al centro fondato negli anni '60; lotta d'allenamento leale e amichevole con i ragazzi del centro e i loro Pokémon Erba/Normale degli uliveti. | `ITEM_EXP__SHARE` (costante reale, doppio trattino basso) |
| S-CL-06 | U Cannuni | Barone decaduto, Mazzarino | Usare `Martiddata` e `Spallata` coi propri Pokémon per ritrovare 4 antiche pietre cadute dai bastioni cilindrici del castello «U Cannuni». | Consenso +1 |
| S-CL-07 | Il Rabato | Anziana, Sutera, Monte San Paolino | Salita al santuario sulla rocca di gesso (percorso a scalini coi Pokémon montani) e presepe vivente nel quartiere arabo con `Mareep` e `Miltank` (dicembre, orologio del DS). | Strumento raro |
| S-CL-08 | Cambiavoti di Caltanissetta (ST-06) | Chantal (telefono), Gela | Individuare e battere il Cambiavoti di Gela e il suo Pokémon spia (`Sableye`/`Natu`) davanti al seggio scolastico. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-CL-01 | Castello Manfredonico (Mussomeli) | 3 piani sulla rupe | `Spallata` | Spettro, Roccia (`Gastly`, `Haunter`, `Misdreavus`, `Zubat`) | B-CL-01 |
| D-CL-02 | MUOS (Niscemi) | 3 mappe: sughereta scavata dai Pokémon Terra dell'ecomafia, recinzione, piazzale delle parabole ad alta frequenza | `Roncigghiu` | Elettro, Acciaio, Terra, Veleno (`Magnemite`, `Dugtrio`, `Grimer`) | B-CL-02 |
| D-CL-03 | Zolfara di Gabbara | 3 livelli di gallerie gialle di zolfo | `Martiddata`, `Spallata` | Roccia, Terra, Veleno (`Graveler`, `Sandslash`, `Koffing`) | B-CL-03 |
| D-CL-04 | Viadotto Salso 2 | 4 piloni incompiuti scossi dai Pokémon dei subappaltatori | — | Volante, Roccia | Segreteria 4 |

### Boss secondari

B-CL-01 **La Dama del Castello** (medium che controlla i Pokémon Spettro della rupe di Mussomeli, 34) · B-CL-02 **Il Subappaltatore delle Parabole** (usa Pokémon Elettro/Acciaio per schermare il radar mentre i `Dugtrio` interrano i fusti tossici, 35) · B-CL-03 **U Capumastru** della zolfara (usa Pokémon Roccia/Terra nelle gallerie profonde di Gabbara, 35).

### Meme ed easter egg

E-CL-01 Le antenne Rai di Sant'Anna: un NPC col cappello di stagnola giura che «usano gli `Alakazam` per trasmettere i pensieri del Presidente». · E-CL-02 Cartello ST-09 a Caltanissetta. · E-CL-03 Il cartello «Lavori in corso — fine lavori 2006» con sotto un adesivo «2026» e un `Machop` che dorme appoggiato alla pala. · E-CL-04 L'amaro alle erbe di Caltanissetta distillato coi Pokémon Erba e offerto da ogni nonno (nome generico, nessun marchio).

---

## 6. Provincia di Agrigento (AG) — Atto III · ore 37–46 · Dossier 5

**Area dialettale:** agrigentino; Licata costiera (Calogero), Sciacca (marinaro di San Michele), Lampedusa (pelagio). Metafonia centrale.
**Tema:** sete, autobotti, abusivismo, la Valle dei Templi.
**Operazioni di «U Sistema» nella provincia (R-10.3):** **furto idrico biologico negli Ipogei** (i custodi infedeli usano `Gastrodon`, `Quagsire` e `Octillery` con `Sorbacqua`/`Idropompa` per aspirare l'acqua pubblica dalle condotte verso le cisterne private delle autobotti da 150 €, mentre gli `Steelix` tappano i tubi comunali); **frode del carburante fantasma a Lampedusa** (Pokémon Veleno/Acciaio usati per gonfiare chimicamente le cisterne d'acqua salmastra spacciandola per gasolio consegnato); **cemento abusivo notturno a Villaseta** (squadre di `Machamp`, `Golem` e `Hippowdon` del Geom. Iacono che alzano interi piani abusivi in una sola notte in cambio di pacchetti di voti e promesse di condono).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-AG-01 | Calogero e la sete di Licata | Licata, porto | Rubinetti a secco da 3 settimane mentre le autobotti del consorzio legato a «U Sistema» vendono acqua torbida a 150 € a carico, scortate da scagnozzi coi `Quagsire`. Calogero, col suo `Tratturi` (Donphan) e `Siccità` (Hippowdon), guida la rivolta degli agricoltori e blocca la SS115 coi trattori per far passare il giocatore contro il blocco del cartello. | `FLAG_RECRUIT_CALOGERO`, Consenso +3 |
| M-AG-02 | Il tubo bucato e i custodi della notte | Sciacca → Agrigento | Seguire l'acquedotto provinciale lungo la costa (mappe con i grossi tubi esterni): 5 saracinesche pubbliche vengono chiuse e ostruite ogni notte (tra le 20:00 e le 6:00 dell'orologio del DS) da 5 «Custodi Infedeli» di «U Sistema» (inventati) che usano `Onix`, `Steelix` e `Poliwrath` per bloccare le valvole e deviare la pressione idrica. Sconfiggerli di notte riapre il flusso. | Consenso +3, `FLAG_WATER_MAFIA_DEFEATED` |
| M-AG-03 | Gli Ipogei e le idrovore viventi | Valle dei Templi | Sotto le colonne doriche della Valle dei Templi si scende nel dungeon `D-AG-01` (gli antichi acquedotti sotterranei greci, navigabili con `Aliscafu`): nel cuore degli Ipogei si scopre la cisterna segreta (inventata) dove il Fontaniere Infedele (`B-AG-01`) usa una batteria di `Gastrodon`, `Quagsire` e `Octillery` con `Sorbacqua` e `Idropompa` per risucchiare le sorgenti pubbliche e pomparle direttamente nelle autobotti abusive in superficie! | — |
| M-AG-04 | Lampedusa: il carburante fantasma | Porto Empedocle → traghetto → Lampedusa | Sottotrama sugli appalti milionari (inventati) per la fornitura energetica e il trasporto carburante dell'isola: l'Appaltatore (`B-AG-04`) usa `Muk` e `Weezing` nei depositi portuali per miscelare scarti chimici e acqua di mare, fatturando alla Regione navi cisterna di gasolio mai consegnate. Tono sobrio e silenzioso alla Porta d'Europa col proprio Pokémon a seguito (R-05.4/5, R-10.4); nessuna satira su chi arriva. | `FLAG_LAMPEDUSA_ARC`, Consenso +3 |
| M-AG-05 | Segreteria 5: il Signore delle Acque e del Cemento | Agrigento, via Atenea → Villaseta | Dungeon `D-AG-04` tra i tetti e le impalcature delle palazzine abusive di Villaseta, dove squadre di `Machamp`, `Graveler` e `Golem` del racket edilizio tirano su quarti e quinti piani abusivi in una sola notte («cemento elettorale»: un piano in più = 50 voti garantiti per il condono). Boss: **Geom. Gerlando Iacono**, re del cemento e del consorzio delle autobotti (Livello 3 di «U Sistema»). Tipo **Terra**, asso Gastrodon L43 (con `Acquascolo`/`Sorbacqua` che si potenzia con l'acqua rubata). Sconfiggerlo consegna il Dossier e sblocca l'uso di `Passaggiu` (Volo). | **Dossier Telamuni**, `FLAG_DOSSIER_AG`, `Passaggiu` (Volo) disponibile, comizio in piazza Marconi |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-AG-01 | Il comizio sbagliato (ST-03) | Turi, Agrigento | Turi ha mandato i `Noctowl` dei volantini nella piazza sbagliata (Agrigento invece di Licata). Portare i 20 sostenitori da un comune all'altro (scena col pullman). | Consenso +1 |
| S-AG-02 | Le Terme di Sciacca | Ex bagnino, Sciacca | Le terme storiche (dove i Pokémon Fuoco/Acqua alimentavano le vasche sulfuree) sono chiuse per scaricabarile burocratico tra 4 uffici (Comune, Regione, ASP, Soprintendenza). Si riaprono vincendo 4 lotte contro i «funzionari» e i loro Pokémon pigri. | Consenso +1, apre le stufe del Monte Kronio (`D-AG-03`) |
| S-AG-03 | La Scala dei Turchi | Bagnina, Realmonte | Fermare i vandali e i venditori abusivi di souvenir che usano Pokémon Roccia/Acciaio (`Sandshrew`, `Aron`) per grattare blocchi di marna bianca dalla scogliera (4 lotte). | Consenso +1 |
| S-AG-04 | La Torre di Carlo V | Pescatore, Porto Empedocle | Il cartello con il nome letterario della città: trovare il vecchio libraio (accompagnato da un `Noctowl` occhialuto) che regala un libro (oggetto da leggere: brano scritto nel Modulo 6). | MT |
| S-AG-05 | L'uva Italia | Agricoltore, Canicattì | I mediatori del racket dell'uva hanno aizzato uno stormo di `Murkrow` e `Staravia` affamati contro il vigneto di un produttore indipendente: proteggere il raccolto (lotta a 3 ondate). | Bacche |
| S-AG-06 | I Sette Cortili | Artista, Favara | Farm Cultural Park come modello positivo di rigenerazione: caccia a 6 installazioni d'arte contemporanea realizzate dagli artisti insieme ai loro Pokémon (`Smeargle`, `Mr. Mime`, `Porygon`) tra i vicoli recuperati. | `ITEM_SOOTHE_BELL` |
| S-AG-07 | Il Gattopardo e la rosolia | Monaca, Palma di Montechiaro | Monastero delle Benedettine: consegnare le mandorle e il miele raccolto dai `Combee` per i dolci conventuali; lettura del passo del romanzo citato nel luogo (testo nel Modulo 6, parafrasi). | `Cassata` ×3 |
| S-AG-08 | La Spiaggia dei Conigli | Volontaria, Lampedusa | Proteggere la schiusa delle uova di tartaruga e di `Squirtle`/`Lapras` selvatici: usare il proprio Pokémon per rimuovere 5 file di ombrelloni e sdraio piazzati dagli abusivi sopra i nidi. | Consenso +1 |
| S-AG-09 | Cambiavoti di Agrigento (ST-06) | Chantal (telefono), Favara | Scovare e battere il Cambiavoti di Agrigento e il suo Pokémon spia (`Haunter`/`Murkrow`) fuori dal seggio scolastico. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-AG-01 | Ipogei della Valle dei Templi | 3 livelli di cunicoli d'acqua greci prosciugati o deviati dai Pokémon del consorzio | `Aliscafu` (canali), `Spallata` | Acqua, Terra, Roccia (`Wooper`, `Quagsire`, `Gastrodon`, `Onix`) | B-AG-01 |
| D-AG-02 | Grotta della Scala dei Turchi | 2 mappe di marna bianca e mare cristallino | `Aliscafu` | Acqua, Roccia (`Corsola`, `Shellder`, `Wingull`) | B-AG-02 |
| D-AG-03 | Stufe del Monte Kronio (Sciacca) | 3 piani di grotte di vapore termale ad altissima temperatura | `Martiddata` | Fuoco, Psico (`Torkoal`, `Slugma`, `Meditite`) | B-AG-03 |
| D-AG-04 | Palazzine di Villaseta | 3 edifici abusivi con piani extra in costruzione notturna coi Pokémon Lotta/Roccia, collegati da passerelle di cantiere | — | — | Segreteria 5 |

### Boss secondari

B-AG-01 **Il Fontaniere Infedele** (coordina i `Gastrodon` e `Octillery` che aspirano l'acqua pubblica negli Ipogei per le autobotti; Acqua, 40) · B-AG-02 **Il Raschiatore** della marna (scava la Scala dei Turchi coi Pokémon Roccia per rivendere la polvere bianca ai lidi VIP; Roccia, 39) · B-AG-03 **Il Santone del Vapore** (occupa abusivamente le stufe di San Calogero coi suoi Pokémon Psico/Fuoco; 41) · B-AG-04 **L'Appaltatore del Carburante** (Lampedusa, usa Pokémon Veleno/Acciaio per sofisticare le cisterne; 42).

### Meme ed easter egg

E-AG-01 L'autobotte abusiva trainata da un `Donphan` che passa a ogni visita con l'altoparlante di un ambulante. · E-AG-02 Il Telamone sdraiato nella Valle dei Templi (attorno a cui dormono tre `Slakoth`): «Sono stanco, riposo da 2.500 anni, come i lavori della statale Agrigento–Caltanissetta». · E-AG-03 Cartello ST-09 a Porto Empedocle. · E-AG-04 Il rubinetto di casa a Licata che, aperto, fa uscire solo il verso asciutto di un `Diglett` e dà un messaggio diverso ogni giorno della settimana.

---

## 7. Provincia di Trapani (TP) — Atto IV · ore 46–53 · Dossier 6

**Area dialettale:** occidentale (trapanese, marsalese, mazarese); Erice; Favignana egadina. Mai `mbare`/`carusu`.
**Tema:** vento, sale, vino, fantasmi, parchi eolici sui terreni espropriati con prestanome (inventati).
**Operazioni di «U Sistema» nella provincia (R-10.3):** **la truffa del vento artificiale nei parchi eolici** (la loggia dell'Avv. Asaro espropria vigneti e uliveti tramite prestanome per piantare pale eoliche mai collegate alla rete elettrica, e quando arrivano gli ispettori GSE schiera stormi di Pokémon Volante con `Ventoincoda` e `Turbine` per far girare le eliche a vuoto e incassare milioni di incentivi verdi!); racket delle quote pesca e delle cantine nello Stagnone.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-TP-01 | Selinunte e i covi | Castelvetrano, Parco di Selinunte, Cave di Cusa | Il parco archeologico sul mare; in paese, i covi del superlatitante sono stati smantellati e trasformati in un piccolo presidio civico: tono sobrio, nessuna lotta, il Pokémon a seguito cammina in silenzio (R-05.4, R-10.4). Dalle carte sequestrate emerge il primo indizio sulla «Loggia del Vento» che ha riciclato i vecchi capitali nei parchi eolici. | — |
| M-TP-02 | Il silenzio del Cretto | Gibellina | Il Grande Cretto di Burri: labirinto di cemento bianco, **nessun Pokémon selvatico, nessuna lotta, nessuna musica allegra**, solo il suono del vento e il Pokémon a seguito silenzioso al fianco del protagonista. Tre anziani raccontano i fondi della ricostruzione post-terremoto del Belice divorati dagli speculatori del cemento. Gibellina Nuova: architetture utopiche in rovina. | `FLAG_CRETTO_DI_BURRI_EVENT` |
| M-TP-03 | Il vento a pagamento e le pale truccate | Mazara del Vallo → Marsala | Dalla Kasbah e dal porto peschereccio di Mazara fino alle cantine di Marsala e alla Laguna dello Stagnone (`D-TP-02`): i contadini mostrano le colline espropriate da società prestanome (inventate) di «U Sistema» per innalzare torri eoliche coi cavi tranciati. Il giocatore sorprende il Prestanome (`B-TP-02`) mentre ordina a uno stormo di `Pidgeot`, `Fearow` e `Skarmory` di usare `Ventoincoda` e `Turbine` contro le pale ferme per falsificare i contatori durante l'ispezione e intascare i contributi europei! | Consenso +3, `FLAG_WIND_FARM_SYNDICATE` |
| M-TP-04 | Segreteria 6: il Gran Maestro dei Parchi Eolici | Trapani → funivia → Erice, Castello di Venere | La funivia si blocca a metà («guasto per raffiche anomale provocate dai Pokémon della Loggia», scena): si sale a piedi nel borgo medievale avvolto dalla nebbia. Dungeon nel Castello di Venere (`D-TP-04`, visibilità ridotta dalla nebbia generata dai `Noctowl`/`Altaria`). Boss: **Avv. Vito Asaro**, «Gran Maestro» della loggia (inventata) dei parchi eolici e dei prestanome (Livello 3 di «U Sistema»). Tipo **Volante**, asso Staraptor L49. | **Dossier Mulinu**, `FLAG_DOSSIER_TP`, comizio a Trapani |
| M-TP-05 | Il pullman delle 5:40 | Trapani, autostazione | Scena: l'accesso diretto a Palermo è sbarrato dalla «Zona rossa» del Grande Comizio di Mistretta (cordone di sicurezza coi `Growlithe`/`Arcanine` e `Bastiodon`); il pullman regionale delle 5:40 attraversa l'entroterra fino a Sant'Agata di Militello col protagonista e il suo Pokémon seduti tra i pendolari (R-02). | inizio della parte messinese |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-TP-01 | Il cous cous elettorale (ST-03) | Turi, San Vito Lo Capo | Turi ha promesso «cous cous di pesce gratis per tutti, Pokémon compresi» in un comizio: aiutare i cuochi e i loro `Octillery`/`Mr. Mime` a servirne 10 piatti a tempo (minigioco di consegna). | Consenso +1 |
| S-TP-02 | Le saline | Salinaro, Trapani | Ripristinare il ricambio d'acqua delle vasche di sale (habitat dei `Corsola` e `Krabby`) riparando 3 mulini a vento storici con l'aiuto dei propri Pokémon (puzzle di orientamento delle pale col vento del giorno). Riprende `ST-08`. | Consenso +1, `Sali` (Modulo 3) |
| S-TP-03 | Le genovesi ericine | Pasticcera, Erice | Consegnare le genovesi alla crema appena sfornate (tenute al caldo da un Pokémon Fuoco) a 3 NPC in cima e in fondo alla funivia prima che la nebbia le raffreddi. | `Genovesi` ×5 (Modulo 3) |
| S-TP-04 | Mozia | Archeologa, Marsala | Raggiungere l'isola di Mozia a piedi lungo l'antica strada fenicia sommersa (con bassa marea, orario del DS, tra i `Chinchou` e `Staryu`) e trovare la statua del Giovinetto (gag del museo chiuso il lunedì). | Fossile |
| S-TP-05 | Il Satiro Danzante | Pescatore, Mazara | Il vecchio capitano che pescò la statua bronzea nella rete (storia vera, raccontata con rispetto) chiede di recuperare la sua rete storica rimasta impigliata in un banco di `Tentacruel` e `Sharpedo`. | `ITEM_SUPER_ROD` se non ancora ottenuta, altrimenti MT |
| S-TP-06 | Lo Zingaro | Guardiaparco, Castellammare/Scopello | La prima riserva naturale siciliana: percorrere il sentiero costiero di 3 mappe aiutando i Pokémon selvatici (`Bellossom`, `Wingull`, `Phanpy`) a liberarsi dai rifiuti lasciati dai motoscafi abusivi. | Consenso +1 |
| S-TP-07 | La tonnara Florio | Ex tonnaroto, Favignana | Racconto sobrio dell'antica mattanza; esplorazione delle spettacolari cave di tufo bianco e mare turchese di Cala Rossa (`D-TP-03`), dove nidificano Pokémon Roccia/Acqua. | MT |
| S-TP-08 | Cambiavoti di Trapani (ST-06) | Chantal (telefono), Alcamo | Individuare e battere il Cambiavoti di Alcamo e il suo Pokémon spia (`Rotom`/`Murkrow`) davanti al seggio scolastico. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-TP-01 | Cave di Cusa | 2 mappe con i rocchi di colonna abbandonati nel V sec. a.C. e presidiati dai Pokémon Roccia | `Spallata` | Roccia, Terra (`Onix`, `Rhyhorn`, `Baltoy`) | B-TP-01 |
| D-TP-02 | Laguna dello Stagnone | mare basso tra saline e pale eoliche abusive, 3 mappe | `Aliscafu` | Acqua, Volante (`Mantine`, `Pelipper`, `Skarmory`) | B-TP-02 |
| D-TP-03 | Cave di tufo di Cala Rossa | 2 mappe di gallerie di calcarenite sul mare di Favignana | `Martiddata` | Roccia, Acqua (`Omanyte`/selvatici marini, `Graveler`) | — |
| D-TP-04 | Castello di Venere | 3 mappe avvolte nella nebbia fitta dei Pokémon Volante della Loggia | — | — | Segreteria 6 |
| D-TP-05 | Grande Cretto | 1 mappa labirinto, nessun incontro (luogo della memoria, R-05.4) | — | — | — |

### Boss secondari

B-TP-01 **Lo Scalpellino delle Cave** (vende blocchi archeologici di Cusa scavati coi suoi Pokémon Roccia alle ville abusive; Roccia, 46) · B-TP-02 **Il Prestanome** del parco eolico (nullatenente sulla carta, comanda gli stormi Volante/Elettro che falsificano i contatori GSE allo Stagnone; 47) · B-TP-03 **Il Massaro della Kasbah** (inventato, capozona del racket dei pescherecci coi suoi Pokémon Buio; 46).

### Meme ed easter egg

E-TP-01 Il vento di Trapani: ogni NPC all'aperto (e il verso dei Pokémon Volante) ha la frase che vola via a metà (testo troncato con «…» e poi «aspetta, rifaccio»). · E-TP-02 Cartello ST-09 a Trapani. · E-TP-03 La funivia di Erice «chiusa per vento» anche nei giorni di bonaccia perché il `Drifblim` dell'addetto dorme sui cavi. · E-TP-04 Il piatto di cous cous di San Vito che diventa più grande a ogni visita mentre uno `Snorlax` lo fissa estasiato.

---

## 8. Provincia di Messina (ME) — Atto IV · ore 53–60 · Dossier 7

**Area dialettale:** messinese non metafonetico (Giostra, Torre Faro/Ganzirri marinaro); San Fratello e Mistretta: gallo-italico nei Nebrodi (con variante sicilianizzata dichiarata); Eolie: eoliano.
**Tema:** lo Stretto, il Ponte eterno, la mafia dei pascoli, il lusso di Taormina.
**Operazioni di «U Sistema» nella provincia (R-10.3):** **la mafia dei pascoli di carta sui Nebrodi** (il clan incassa milioni di contributi europei AGEA dichiarando mandrie di Pokémon da pascolo inesistenti e usa `Tauros`, `Houndoom` e `Ursaring` feroci per cacciare gli allevatori onesti di cavalli sanfratellani `Rapidash` dai terreni demaniali); **la burocrazia magnetica della Società Stretto Eterna** (negli archivi dal 1971 i dirigenti usano `Magnezone`, `Bronzong` e `Porygon2` per spostare le pareti di faldoni, smagnetizzare i timbri di scadenza e rigenerare all'infinito il progetto preliminare del Ponte per non perdere i gettoni di presenza: Segreteria 7); **il patto del lusso a Taormina** (`ST-05`).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-ME-01 | La mafia dei pascoli e le mandrie fantasma | Nebrodi: San Fratello, Sant'Agata, Mistretta | Scendendo dal pullman delle 5:40 nei boschi dei Nebrodi (`D-ME-01`), un allevatore onesto di cavalli sanfratellani (`Ponyta`/`Rapidash`) spiega la truffa di «U Sistema»: il Pascolatore di Carta (`B-ME-01`, inventato) incassa i fondi europei su migliaia di ettari demaniali dichiarando nei registri greggi di `Mareep` e `Miltank` che non esistono, e sguinzaglia `Houndoom`, `Ursaring` e `Tauros` aggressivi per sbranare o scacciare i Pokémon degli allevatori veri che provano a usare il pascolo! Sconfitta del clan nel bosco. | Consenso +3, `FLAG_NEBRODI_PASTURE_MAFIA` |
| M-ME-02 | La costa tirrenica | Capo d'Orlando → Patti/Tindari → Barcellona → Milazzo | Lungo la costa tirrenica: a Tindari i laghetti di Marinello modellati dalle correnti e dai Pokémon marini; a Milazzo il castello, le ciminiere della raffineria presidiate da `Koffing`/`Magnemite` e l'imbarco per le Eolie. | — |
| M-ME-03 | Pippo a Torre Faro | Messina, Torre Faro | Davanti al pilone d'acciaio dello Stretto (attorno a cui è avvolto il suo gigantesco `Piloni`/Steelix), Pippo mangia un pidone e beve una birra coi cristalli di sale. Racconta 35 anni di studi di fattibilità e si unisce al gruppo. | `FLAG_RECRUIT_PIPPO` |
| M-ME-04 | La Società Stretto Eterna e i faldoni magnetici | Messina, archivi (inventati) | Pippo apre le porte del labirinto burocratico di 5 piani (`D-ME-02`): i 10 funzionari e il Dirigente dei Gettoni (`B-ME-02`) usano `Magneton`, `Bronzong` e `Porygon2` per **spostare magneticamente gli scaffali metallici dei faldoni dal 1971 e resettare i numeri di protocollo**, rendendo impossibile chiudere l'istruttoria del Ponte e garantendosi indennità di rischio perpetue. | Consenso +3 |
| M-ME-05 | Il galà del Teatro Antico | Taormina | Galà del cinema al Teatro Antico (tappa di `ST-05`): tra red carpet e Pokémon da pelliccia d'alta moda (`Persian`, `Ninetales`, `Glameow`), Christian e il giocatore smascherano in diretta il patto tra il consorzio degli albergatori del lusso (`B-ME-03`, inventato) e l'entourage di Mistretta, che usano le suite e le esibizioni Pokémon per lavare i fondi neri della campagna. 4 lotte in abito da sera. | Consenso +3 |
| M-ME-06 | Segreteria 7: l'AD delle Partecipate | Messina, Palazzo (inventato) delle Partecipate, vicino al Duomo | Il campanile astronomico del Duomo suona a mezzogiorno (col leone/`Entei` meccanico e il gallo): gli ingranaggi magnetici dei Pokémon Acciaio aprono e chiudono le porte del dungeon a ritmo delle statue. Boss: **Dott. Natale Sturiale**, AD di tutte le società partecipate regionali (Livello 3 di «U Sistema»), che governa trenta consigli d'amministrazione in contemporanea grazie al calcolo del suo **Magnezone L55**. Tipo **Acciaio**. Sconfiggerlo consegna il Dossier e sblocca la MN Mulinello. | **Dossier Pilunu**, `FLAG_DOSSIER_ME`, comizio in piazza Duomo |
| M-ME-07 | L'elicottero di Torre Faro | Torre Faro, hangar della Società Stretto Eterna | Nell'hangar sotto il pilone c'è un elicottero comprato nel 2006 «per i sopralluoghi aerei del Ponte» e mai acceso. Pippo e il suo `Piloni` (Steelix), insieme a un `Ampharos`/`Electabuzz` che ricarica le turbine, lo rimettono in moto. | `FLAG_ELICOTTERO_PRIVATO`: `Passaggiu` (Volo) funziona anche con la cenere dell'Etna |
| M-ME-08 | Attraversare lo Stretto | Messina, traghetto | Scena: attraversamento dello Stretto sul traghetto sindacale di Pippo (scortato dai `Piscispata` in mare) fino a Villa San Giovanni, aeroporto di Reggio Calabria e volo per Punta Raisi (R-02). | inizio Atto V |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-ME-01 | La diretta col filtro (ST-03) | Turi, Taormina | Turi ha trasmesso in diretta il comizio di Messina lasciando attivo un filtro social che trasforma il protagonista e il suo Pokémon in due `Meowth` con le orecchie rosa. Convincere 5 influencer coi loro Pokémon vanitosi a non ricondividerlo. | Consenso +1 |
| S-ME-02 | La Sciara del Fuoco | Guida vulcanologica, Stromboli | Salita notturna (orologio del DS 20:00–4:00) lungo il cratere attivo (`D-ME-03`), dove i `Magcargo` e `Torkoal` selvatici lanciano lapilli incandescenti verso il mare. | Pietra (Modulo 3) |
| S-ME-03 | Il dissalatore di Lipari | Calogero (telefono), Lipari | Tappa di `ST-08`: il dissalatore dell'isola è tenuto fermo dal Custode delle Pompe (`B-ME-04`, affiliato al racket delle navi cisterna) che usa `Lanturn` e `Electrode` per mandare in corto le turbine. Batterlo riavvia l'impianto. | Consenso +1 |
| S-ME-04 | Il cratere di Vulcano | Pescatore, Vulcano | Tra i bagni di fango sulfureo e le fumarole: trovare e censire per il Prof. Strano 3 Pokémon rari di tipo Fuoco/Veleno nascosti nei vapori. | MT |
| S-ME-05 | La Madonna Nera | Sacrestano, Tindari | Visita rispettosa al santuario sul promontorio e discesa ai laghetti di Marinello: raccogliere 5 conchiglie levigate dai `Shellder`/`Cloyster` sulla lingua di sabbia per il presepe della parrocchia. | `ITEM_SOOTHE_BELL` se non ottenuto, altrimenti bacche |
| S-ME-06 | Il Longano | Ex vivaista, Barcellona Pozzo di Gotto | Il torrente che divide la città è ostruito da detriti abbandonati da un appalto fantasma: usare i propri Pokémon con `Spallata` per riattivare la passerella storica. | Consenso +1 |
| S-ME-07 | Isola Bella | Bagnante, Taormina | Raggiungere Isola Bella sulla lingua di sabbia e battere il proprietario (inventato) del lido «più esclusivo d'Europa» che usa `Kingler` e `Cloyster` per riscuotere 100 € anche da chi appoggia solo l'asciugamano sugli scogli. | Consenso +1 |
| S-ME-08 | Cariddi | Pescatore di pescespada, Ganzirri | A bordo di una feluca tradizionale, usare la MN Mulinello col proprio Pokémon d'acqua per domare i vortici dello Stretto (`D-ME-04`) dove cacciano i `Gyarados` e i `Kingdra`. | Pokémon Acqua (Modulo 3) |
| S-ME-09 | Cambiavoti di Messina (ST-06) | Chantal (telefono), Giostra | Scovare e battere il Cambiavoti del rione Giostra e il suo Pokémon spia (`Sableye`/`Murkrow`) fuori dal seggio. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-ME-01 | Bosco dei Nebrodi | 3 mappe di faggeta e pascoli montani occupati dai Pokémon feroci del racket AGEA | `Roncigghiu` | Erba, Normale (`Ponyta`/`Rapidash` sanfratellani, `Tauros`, `Stantler`), Coleottero | B-ME-01 |
| D-ME-02 | Archivi della Società Stretto Eterna | 5 piani di faldoni dal 1971 (pareti metalliche che si spostano a tempo grazie ai `Magneton`/`Bronzong` dell'ente) | — | nessuno; 10 allenatori «Funzionari» coi loro Pokémon Acciaio/Psico | B-ME-02 |
| D-ME-03 | Sciara del Fuoco (Stromboli) | 2 mappe vulcaniche notturne a picco sul Tirreno | `Aliscafu` | Fuoco, Roccia (`Slugma`, `Magcargo`, `Numel`, `Koffing`) | — |
| D-ME-04 | Gorghi di Cariddi | 2 mappe di mare vorticoso nello Stretto | `Aliscafu`, Mulinello | Acqua, Drago (`Horsea`, `Seadra`, `Gyarados`, `Tentacruel`) | — (post-game: leggendario P-08) |

### Boss secondari

B-ME-01 **Il Pascolatore di Carta** (usa `Tauros` e `Houndoom` per cacciare gli allevatori dai terreni su cui incassa i fondi UE per greggi Pokémon fantasma; Normale/Terra, 52) · B-ME-02 **Il Dirigente dei Gettoni** (usa `Bronzong` e `Porygon2` per rimescolare i faldoni del Ponte dal 1971; Acciaio/Psico, 53) · B-ME-03 **L'Albergatore del Galà** (ricicla i fondi elettorali a Taormina con esibizioni di Pokémon d'élite; Normale/Volante, 53) · B-ME-04 **Il Custode delle Pompe** di Lipari (blocca il dissalatore coi Pokémon Acqua/Elettro per favorire le navi cisterna; 50).

### Meme ed easter egg

E-ME-01 Il cartello ST-09 a Torre Faro, aggiornato a ogni atto. · E-ME-02 Il «buddace»: un NPC catanese a Messina chiama così il `Magikarp`/`Feebas` di un pescatore messinese e nasce una disputa filologica (scambio scritto nel Modulo 6, nessuna volgarità). · E-ME-03 La statua del leone che ruggisce dal campanile astronomico a mezzogiorno col verso di un `Entei`/`Arcanine`: se il giocatore è in piazza, un evento unico al giorno. · E-ME-04 La focaccia messinese che Pippo divide col suo `Piloni` (Steelix) a ogni Ritrovo.

---

## 9. Provincia di Palermo (PA) — Atto V · ore 60–67 · Dossier 8

**Area dialettale:** palermitano urbano (Ballarò/Albergheria, Vucciria, Kalsa, Borgo Vecchio, ZEN), borgate marinare (Mondello, Isola delle Femmine); Piana degli Albanesi arbëreshë (cartelli bilingui; dialoghi arbëreshë solo come saluti, il resto in italiano/siciliano con dichiarazione nel Modulo 6). Mai `mbare`/`carusu`.
**Tono:** il cuore del potere e della memoria. Rallentamento voluto all'ingresso.
**Operazioni di «U Sistema» nella provincia (R-10.3):** **la rete dei «pizzini alati» e dei pacchetti di voti** (dalle masserie di Ficuzza fino a Palazzo delle Aquile, i collettori dell'On. Scaduto usano stormi di `Honchkrow`/`Vucciria`, `Murkrow` e `Drapion` per recapitare i registri cartacei del voto di scambio nei quartieri senza usare telefoni intercettabili dalla Procura di Maria: Segreteria 8); **il quartier generale di `U Cassiere`** (`ST-04`, `B-PA-04`); **il racket dei parcheggi e dei lidi a Mondello** (`B-PA-01`) e **lo smantellamento industriale a Termini Imerese** (`B-PA-03`).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-PA-01 | Cento passi | Cinisi (arrivo a Punta Raisi) | Casa Memoria Peppino Impastato: visita sobria, **nessuna lotta, nessun incontro**, una sola musica lenta. Maria e Totò accompagnano il protagonista; il Pokémon a seguito cammina in silenzio accanto a lui (R-05.4, R-10.4). | — |
| M-PA-02 | Le steli di Capaci | A29, Capaci e Isola delle Femmine | Il protagonista percorre a piedi il tratto con le steli e il Giardino della Memoria Quarto Savona Quindici. **Nessuna lotta, nessun selvatico, nessun NPC che parla tranne Maria e Totò.** Sonoro: solo vento e auto sull'asfalto. Il Pokémon a seguito resta silenzioso a capo chino al fianco del protagonista, che ripensa al concorso in magistratura fallito e giura di andare fino in fondo. | `FLAG_CAPACI_MEMORIAL_SILENCE` |
| M-PA-03 | Palermo a due velocità | Politeama/Libertà, Massimo/Maqueda/Quattro Canti, Ballarò, Vucciria, Kalsa, Borgo Vecchio, ZEN 2, Mondello | Con Totò e il suo `PaniCaMeusa` (Snorlax): i salotti di via Libertà (dove la borghesia passeggia coi `Persian` e `Arcanine` da pedigree) contro il caos vitale dei mercati di Ballarò e Vucciria e l'abbandono dello ZEN 2 (dove i `Munnizza`/Grimer proliferano vicino ai cumuli non raccolti e i ragazzi improvvisano lotte Pokémon tra i padiglioni). Cancello del Consenso ≥ 40 per aprire il cordone della Zona rossa in centro. | Consenso +3 |
| M-PA-04 | Le carte di Ficuzza e i pizzini alati | Corleone, Ficuzza | Maria spiega perché le intercettazioni telefoniche sul voto di scambio nella Conca d'Oro sono mute: il collettore elettorale di «U Sistema» non usa telefoni, ma una **rete biologica di `Honchkrow` (`Vucciria`), `Murkrow` e `Houndoom`** addestrati in una masseria nel Bosco di Ficuzza (`D-PA-02`, oltre la Cascata delle Due Rocche) per trasportare di notte i pizzini coi conteggi delle sezioni elettorali! Il giocatore espugna la masseria di `B-PA-02` e sequestra i registri. Il CIDMA di Corleone è un luogo di memoria visitabile, in tono sobrio e senza lotte (R-05.4). | `Atto` di ST-02, Consenso +3 |
| M-PA-05 | Segreteria 8: il Collettore della Conca d'Oro | Palermo, Palazzo delle Aquile | Dungeon fra sale di commissione e corridoi presidiati dai «Portatori di Voti» e dai loro Pokémon Buio/Veleno (`D-PA-05`). Boss: **On. Totò Scaduto** (omonimo del compagno: gag «chiamatemi Onorevole, il Totò senza portafoglio è lui»), il grande collettore elettorale della Conca d'Oro (Livello 3 di «U Sistema»). Tipo **Buio**, asso Drapion L61. Sconfiggerlo consegna il Dossier e sblocca la MN Cascata. | **Dossier Geniu**, `FLAG_DOSSIER_PA`, comizio al Politeama |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-PA-01 | Il manifesto abusivo (ST-03) | Turi, Palermo, via Maqueda | Turi ha mandato dei `Mankey`/`Aipom` ad attaccare i manifesti del protagonista sopra quelli di tutti gli altri candidati: staccarli in 6 punti prima che arrivino i vigili. | Consenso +1 |
| S-PA-02 | Pani ca' meusa | Ambulante, Vucciria | Il meusaio della Vucciria (aiutato da un `Magby` che tiene bollente la sugna nella caldaia) prepara il panino come strumento curativo e sfida il giocatore al minigioco «schietto o maritato». | `PaniCaMeusa` ×5 (Modulo 3) |
| S-PA-03 | Il Cristo Pantocratore | Sacrestano, Monreale | Un `Murkrow` entrato dal chiostro ha spostato le tessere di un bozzetto musivo: rimettere in ordine il mosaico dorato (puzzle a griglia 3×3). | MT |
| S-PA-04 | Villa dei Mostri | Custode, Bagheria, Villa Palagonia | Nel giardino barocco assediato dai palazzoni del sacco edilizio degli anni '60–'70, i Pokémon Spettro animano le ombre delle statue grottesche (`D-PA-03`): riconoscere 8 statue dei mostri dalle descrizioni. | `Sfinciuni` (Modulo 3) |
| S-PA-05 | La FIAT che non c'è | Ex operaio, Termini Imerese | Dungeon industriale spettrale `D-PA-04` nei capannoni abbandonati, dove i vecchi Pokémon Acciaio/Elettro (`Magnemite`, `Klink`/equivalenti HG `Magneton`, `Electabuzz`) lasciati dalle ditte fantasma vagano ancora lungo la catena di montaggio ferma; l'operaio racconta le dieci finte riconversioni industriali. | Consenso +1 |
| S-PA-06 | La Rocca di Cefalù | Turista, Cefalù | Salita lungo i bastioni fino al Tempio di Diana e lotta sulla cima contro il Guardiano della Rocca (`Aerodactyl`/`Golem`). | Consenso +1 |
| S-PA-07 | Lingue di Piana | Papàs, Piana degli Albanesi | Cartelli bilingui: trovare 5 parole arbëreshë sui cartelli e dirle a 5 NPC (dizionario nel Modulo 3). Portella della Ginestra è visitabile come luogo di memoria sobria, senza lotte né selvatici (R-05.4). Cannolo gigante finale. | `Cannolu` ×5 |
| S-PA-08 | La Diga Jato | Contadino, Partinico | Tappa di `ST-08`: le campagne sono a secco con l'invaso pieno accanto perché gli scagnozzi del consorzio bloccano le paratoie coi loro `Poliwrath` e `Quagsire`. Aprire le chiuse vincendo 3 lotte. | Consenso +1 |
| S-PA-09 | Il Festino (evento a calendario) | Devota, Cattedrale | 14–15 luglio (orologio del DS): il carro trionfale di Santa Rosalia attraversa il Cassaro; il giocatore e i suoi Pokémon aiutano a trainare il carro fino a Porta Felice (minigioco). | Strumento raro |
| S-PA-10 | Cambiavoti di Palermo (ST-06) | Chantal (di persona), ZEN 2 | Sconfiggere l'ultimo dei 9 Cambiavoti e il suo `Rotom`/`Gengar` spia davanti alla scuola dello ZEN 2; se tutti i 9 Cambiavoti sono stati sconfitti, Chantal consegna la `UrnaElettor.` (Master Ball). | Consenso +1, `UrnaElettor.` (se 9/9) |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici ed ecologia | Boss |
|---|---|---|---|---|---|
| D-PA-01 | Monte Pellegrino e Grotta dell'Addaura | 3 mappe carsiche sopra Palermo (`MAP_PA_MONTE_PELLEGRINO_GROTTE`) | `Martiddata`, `Spallata` | Roccia, Spettro (`Graveler`, `Golbat`, `Misdreavus`) | — |
| D-PA-02 | Bosco di Ficuzza e Cascata delle Due Rocche | 3 mappe: bosco reale, cascata, masseria delle voliere di `Honchkrow` del voto di scambio | `Roncigghiu`, Cascata | Erba, Acqua, Buio (`Murkrow`, `Honchkrow`, `Houndour`, `Lombre`) | B-PA-02 (post-game: P-03 sulla vetta di Rocca Busambra) |
| D-PA-03 | Villa Palagonia | 2 mappe tra le statue dei mostri | — | Spettro (`Gastly`, `Haunter`, `Shuppet`) | — |
| D-PA-04 | Ex stabilimento di Termini Imerese | 4 mappe: catena di montaggio, verniciatura, uffici dei liquidatori, piazzale | `Spallata` | Acciaio, Elettro, Spettro (`Magneton`, `Voltorb`, `Koffing`, `Banette`) | B-PA-03 |
| D-PA-05 | Palazzo delle Aquile | 3 piani di corridoi comunali e sale dei collettori | — | — | Segreteria 8 |
| D-PA-06 | Via della Lega (Palazzo dei Normanni, corridoi dell'ARS) | 5 piani di saloni burocratici, commessi e portaborse d'élite (2 piani saltabili con i 9 faldoni di Totò, `ST-07`) | `Spallata`, Cascata | Psico, Buio, Spettro L62–68 (i Pokémon segretari dell'Assemblea) | — |

### Boss secondari

B-PA-01 **Il Parcheggiatore Capo** di Mondello (controlla ogni centimetro di striscia blu e spiaggia libera usando `Manzuni`/Snorlax e `Scrafty`/`Primeape` per bloccare le auto di chi non paga «a piacere»; Normale/Buio, 58) · B-PA-02 **Il Massaro di Ficuzza** (addestra gli `Honchkrow` e `Houndoom` che portano i pizzini elettorali nella Conca d'Oro; Erba/Buio, 59) · B-PA-03 **Il Liquidatore** dello stabilimento (incassa fondi di riconversione da 15 anni tenendo i Pokémon Acciaio fermi nei capannoni di Termini; Acciaio, 59) · B-PA-04 **U Cassiere**, capo del racket interprovinciale del «pizzo biologico» che ha rovinato il fratello di Orazio (`ST-04`, affrontato nel suo covo coi registri di tutte le province; Buio/Veleno, 60).

### Meme ed easter egg

E-PA-01 «Arancina»: a Palermo gli NPC (e persino i cartelli delle rosticcerie) correggono «arancinu» (simmetrico a `E-CT-02`); chi ha risposto in modo «coerente» o «diplomatico» in entrambe le città riceve un oggetto. · E-PA-02 Il coccodrillo della Vucciria (leggenda metropolitana del fiume Papireto): un anziano giura che sia un `Feraligatr` (`Papiretu`) appeso al soffitto; con `Caimanu`/`Uzzuni`/`Papiretu` in squadra come Pokémon a seguito, battuta speciale e regalo. · E-PA-03 Cartello ST-09 al porto. · E-PA-04 Il traffico di via Roma: un NPC col suo `Slowpoke` aspetta l'autobus 101 dal primo atto. · E-PA-05 Il Genio di Palermo (statua col serpente `Ekans`/`Arbok` al petto): parlandoci, risponde con un indovinello diverso per ogni giorno della settimana.

---

## 10. Provincia di Enna (EN), Lega e finale — Atto V · ore 67–72 · Dossier 9

**Area dialettale:** centrale (ennese); **gallo-italico** a Piazza Armerina, Aidone, Nicosia, Sperlinga (Mistretta senza maschera parla un gallo-italico ennese sicilianizzato: il Modulo 6 dichiara il registro, R-08 della skill).
**Tema:** l'ombelico della Sicilia, nebbia, la resa dei conti.
**Operazioni di «U Sistema» nella provincia e alla Lega (R-10.3):** **il filtro psico-burocratico della Commissione Elettorale** (Segreteria 9 a Enna Alta, dove i Pokémon Psico generano cavilli retroattivi e nebbia cognitiva per escludere le liste non allineate); **i 4 Pilastri del Trasformismo all'ARS** (i 4 Campioni della Lega a Palazzo dei Normanni, ciascuno a capo di una branca biopolitica del Sistema, dall'emergenza `Munnizza` agli algoritmi taglia-ospedali); **il Vertice di Piazza Armerina** (dove i 6 Pokémon dell'On. Mistretta incarnano i 6 pilastri che tengono in equilibrio la Sicilia clientelare).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento (con ruolo centrale dei Pokémon e di «U Sistema») | Esito |
|---|---|---|---|---|
| M-EN-01 | La A19 a pezzi | A19 Termini → Enna | Piloni inclinati e deviazioni obbligatorie sulle trazzere provinciali (dungeon esterno `D-EN-01` con massi da spostare con `Spallata`); la domenica (orologio del DS) il traffico è bloccato dalla coda chilometrica di auto e `Manzuni` (Snorlax) diretti al Sicilia Outlet Village di Agira. | — |
| M-EN-02 | Il lago che non c'è | Pergusa | Ultima tappa di `ST-08`: il mitico lago di Proserpina è ridotto a una pozza fangosa perché gli scarichi sono stati deviati e i Pokémon d'acqua sono fuggiti; attorno al bacino corre l'autodromo abbandonato, usato dagli scagnozzi motorizzati del Sistema per corse clandestine coi `Rapidash` e `Yanmega` (sfida a giri di pista in sequenza a tempo). | Consenso +3 |
| M-EN-03 | Segreteria 9: la Commissione Elettorale | Enna Alta, Castello di Lombardia → Rocca di Cerere | Nebbia perenne mantenuta dai Pokémon Psico/Spettro sulla rocca più alta dell'isola (`D-EN-03`). Il boss è il **Presidente della Commissione Elettorale Regionale, Dott. Filippo La Rosa** (inventato, Livello 3 di «U Sistema»), autore del cavillo di Fontanarossa del Capitolo 3 (chiude il cerchio dell'Atto I): usa `Alakazam`, `Xatu` e il suo asso **Slowking L66** per smarrire i timbri, annullare le firme autenticate e confondere i ricorsi. Sconfiggerlo obbliga la Commissione a vidimare l'ultimo visto elettorale e sblocca `Scalaroccia` per il post-game. | **Dossier Cerere**, `FLAG_DOSSIER_EN`, ultimo visto elettorale |
| M-EN-04 | La notte dello spoglio: i 4 Campioni della Lega | Palermo, Palazzo dei Normanni, Sala d'Ercole | Cancello Consenso ≥ 49. Superata la Via della Lega (`D-PA-06`), nella Sala d'Ercole si affrontano i **4 Campioni della «Lega»** (Livello 4 di «U Sistema»):<br>1. **Don Tanino, il Gattopardo della Prima Repubblica** — Tipo **Roccia/Terra** (`Golem`, `Rhyperior`, `Cradily`, `Armaldo`, `Hippowdon`, asso L70): usa Pokémon-fossile inamovibili dal 1982 che resistono a ogni inchiesta.<br>2. **L'Assessora Tecnica venuta dal Nord (ma già comprata dal Sistema)** — Tipo **Acciaio/Elettro** (`Skarmory`, `Magnezone`, `Porygon-Z`, `Bronzong`, `Electivire`, asso L72): usa Pokémon cibernetici per calcolare il taglio lineare dei reparti ospedalieri e delle scuole di provincia.<br>3. **Il Re delle Liste Civiche e dei Trasformisti** — Tipo **Veleno/Spettro** (`Crobat`, `Gengar`, `Ninjask`/`Drapion`, `Vespiquen`, `Mismagius`, asso L74): cambia casacca e partito a metà battaglia abusando di `Staffetta` (Baton Pass), `Sostituto` e ` Malcomune`.<br>4. **Il Cardinale delle Opere Pubbliche e dei Rifiuti** — Tipo **Buio/Fuoco** (`Sacconiru`/Muk, `Houndoom`, `Honchkrow`, `Magmortar`, `Weavile`, asso L76): il signore delle discariche sature e degli inceneritori che libera i Pokémon Veleno/Buio in città per governare coi poteri d'emergenza. | `FLAG_LEGA_DEFEATED` |
| M-EN-05 | Sotto il temporale a Piazza Armerina | Piazza Armerina | Vinta la Lega, la Sala d'Ercole è vuota: l'On. Mistretta non è a Palermo, ma si è ritirato nel suo feudo al centro esatto dell'isola, nella **Villa Romana del Casale**. Temporale battente (meteo pioggia). Attraversando i quattro quartieri del Palio dei Normanni e il Duomo fino all'ingresso della Villa, i pretoriani della Cupola cercano di fermare il protagonista: gli **8 compagni** (Turi, Orazio, Christian, Chantal, Totò, Calogero, Pippo e Maria) schierano i propri Pokémon iconici e combattono al fianco del giocatore per aprirgli il varco. | — |
| M-EN-06 | La Sala della Grande Caccia: «U Tappu dâ Buttigghia» | Villa Romana del Casale | Tra i mosaici millenari (`D-EN-04`, dove gli antichi romani raffigurarono la cattura delle belve esattamente come Mistretta cattura i clienti e gli elettori), l'**On. Raffaele «Don Lollò» Mistretta** attende col suo `Gattupardu` (Persian) ai piedi. Non urla come un supercattivo: parla sottovoce, con dolcezza paterna e poi in gallo-italico ennese gelido (*«Iu sugnu sulu u tappu ca teni chiusa la buttigghia…»*). I suoi **6 Pokémon** sono i 6 vertici del Sistema siciliano:<br>• `Gattupardu` (Persian L82, con `Pizzu`/Giornopaga e `Bruciapelo`): il trasformismo aristocratico;<br>• `Poltrona` (Slaking L84): l'apparato clientelare immobile che dorme un turno e poi schiaccia ogni riforma;<br>• `Inciuciu` (Spiritomb L84): il patto trasversale di 108 dossier incrociati senza debolezze;<br>• `Cupula` (Tyranitar L86): il monopolio del cemento e delle cave che scatena `RinaDiL’Etna` in lotta;<br>• `Miliardariu` (Metagross L86): la macchina perfetta dei fondi pubblici e delle quote sanitarie;<br>• `Trinacria` (Dragonite L88): la forza primordiale e ferita dell'isola stessa, che Mistretta sostiene possa essere domata solo dal suo paternalismo. | `FLAG_PRESIDENT_MISTRETTA_DEFEATED` |
| M-EN-07 | Il palco | Catania, Piazza Duomo (comizio finale) | Folla di sprite che saltano sotto il Liotru, bandiere della Trinacria, coriandoli; il **Pokémon starter/a seguito** è sul palco accanto al protagonista che alza le braccia da nuovo Presidente della Regione; Turi piange abbracciando Orazio; Christian fa le storie col `Subwoofer`; Maria guarda da lontano col suo `Giustizia` (Lucario) senza applaudire. | — |
| M-EN-08 | Dissolvenza | schermo nero | La fanfara si spegne di colpo; pianoforte solo, poi violino struggente in Do minore. Le cinque frasi bianche sul nero raccontano i sei mesi a Palazzo d'Orléans: gli uffici svuotati, i ricorsi al TAR, gli scioperi dei Pokémon dei consorzi orchestrati dai vecchi cacicchi, gli stessi elettori venuti a chiedere il posto alla Forestale o il condono, e infine le **dimissioni irrevocabili**. Titoli di coda (`atrisorb`) sul nero. | `FLAG_POST_RESIGNATION`, `VAR_TRINACRIA_ATTO` = 6, salvataggio |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo (con integrazione Pokémon) | Ricompensa |
|---|---|---|---|---|
| S-EN-01 | Le due cattedrali | Sacrestani rivali, Nicosia | Santa Maria Maggiore contro San Nicolò: i due quartieri rivali si sfidano da secoli anche coi Pokémon dei rispettivi patroni; fare da paciere (dialoghi in gallo-italico). | Consenso +1 |
| S-EN-02 | Sperlinga negavit | Custode, Sperlinga | Castello scavato interamente nella roccia arenaria (`D-EN-02`), abitato da Pokémon Roccia/Volante; il motto del 1282 inciso sull'ingresso. | MT |
| S-EN-03 | L'outlet della domenica | Commessa, Agira | Parodia del consumismo domenicale: trovare un parcheggio nel labirinto di SUV e `Manzuni` (Snorlax) in doppia fila coi sacchetti firmati. Cassatelle di Agira. | `Cassateddi` (Modulo 3) |
| S-EN-04 | La Granfonte | Contadino, Leonforte | Nei pescheti di Leonforte i contadini insacchettano le pesche una a una sull'albero per proteggerle dai Pokémon Coleottero senza usare pesticidi: aiutare nel minigioco di insacchettamento; sosta alla Granfonte a 24 cannoli. | Bacche |
| S-EN-05 | La Dea di Morgantina | Museo, Aidone | La statua restituita dai musei stranieri: ritrovare la guida e il suo `Xatu`/`Noctowl` smarriti tra le rovine dell'agorà di Morgantina. | Fossile |
| S-EN-06 | La stella di Centuripe | Anziano, Centuripe | Dal «balcone della Sicilia» di fronte all'Etna fumante di cenere, consegnare una lettera urgente a Catania usando `Passaggiu` col proprio Pokémon Volante (possibile grazie a `FLAG_ELICOTTERO_PRIVATO`). | Consenso +1 |

### Dungeon

D-EN-01 **Trazzere dell'A19** (4 mappe esterne tra piloni spezzati, `Spallata`, selvatici Normale/Terra) · D-EN-02 **Castello di Sperlinga** (2 piani scavati nella roccia, `Scalaroccia` per la torre alta nel post-game) · D-EN-03 **Rocca di Cerere** (nebbia psichica, 2 mappe, Pokémon Psico/Spettro) · D-EN-04 **Villa Romana del Casale** (3 sale a mosaico della Grande Caccia: ogni mosaico raffigura antichi Pokémon catturati per i giochi imperiali e indica la via verso la sala di Mistretta).

### Meme ed easter egg

E-EN-01 Cartello ST-09 a Enna («la Sicilia ha un centro geografico, il Ponte neanche un pilone»). · E-EN-02 La nebbia di Enna Alta mantenuta dagli `Haunter` e `Slowking` che fa sparire gli NPC a metà frase. · E-EN-03 La pista di Pergusa: il record sul giro dell'autodromo non appartiene a un `Rapidash` ma a un nonno in Ape 50 spinta da uno `Slugma`. · E-EN-04 Lo studente dell'Università Kore col suo `Slowpoke` che riscrive la stessa tesi di laurea da 9 anni.

---

## 11. Atto VI — Il post-game della disillusione · ore 72–102

Si ricarica la partita: camera di Corso Italia, **sei mesi dopo le dimissioni**. `FLAG_POST_RESIGNATION` è acceso: il motore carica i banchi gemelli (Modulo 1 §7) e riattiva tutti gli allenatori 1–699 con **+25 livelli**.
Perché gli allenatori di «U Sistema» sono di nuovo tutti al loro posto e più forti di prima? Perché, come aveva profetizzato Mistretta a Piazza Armerina, **dopo le dimissioni del protagonista «U Sistema» si è riorganizzato in ventiquattr'ore cambiando semplicemente nome alle liste e alle cooperative**: i sacchi di spazzatura (sprite e `Munnizza` selvatici) sono ancora per strada, la cenere dell'Etna cade ancora, i cantieri sono ancora fermi, e il nuovo governo di salute pubblica ha già riaffidato cliniche, porti, mercati, acquedotti e parchi eolici agli stessi cacicchi. Il Volo funziona ovunque grazie all'elicottero di Pippo.

### Proporzione delle reazioni (vincolante, provincia per provincia)

- **60% Capro espiatorio (`CAPRO`):** danno la colpa al protagonista, ai suoi Pokémon e ai suoi studi in Bocconi/LUISS per la munnizza sotto casa, la chiusura di Fontanarossa per cenere, l'inutilità di Comiso, le buche dell'A19, la siccità e il mancato posto alla Forestale.
- **40% Estimatori (`ESTIMATORE`):** studenti del Cutelli, commercianti che non hanno più piegato la testa al pizzo biologico, vecchi pescatori e operai; riconoscono il sacrificio di chi ha combattuto da solo contro il Sistema.
- Il controllo è meccanico (registro degli NPC, Modulo 1 §7.8).

### Contenuti del post-game (Compagni, Maria, Fantasmi della Prima Repubblica e Leggendari di Trinacria)

| Codice | Contenuto | Dove | Dettagli (con ruolo dei Pokémon Leggendari e dei Fantasmi) |
|---|---|---|---|
| P-01 | Ritrovi con gli 8 compagni | luoghi di `C-01`…`C-08` | Una sfida a settimana per compagno, nel giorno indicato (orologio del DS). Gli 8 compagni sono rimasti gli unici presidi liberi nei rispettivi quartieri e province; le loro squadre L75→85 crescono dopo ogni vittoria (3 versioni, ID allenatori 700–723). |
| P-02 | Maria sul tetto del tribunale | Catania, Palazzo di Giustizia (piazza Verga), tetto | **Super-boss finale** (in stile Rosso sul Monte Argento). Si sblocca avendo raccolto i 9 Atti sulle biotruffe di `ST-02` e vinto tutti i Ritrovi almeno una volta. Maria ti aspetta all'alba sul tetto del tribunale sotto la cenere dell'Etna: ha continuato a istruire i processi usando le carte che hai raccolto durante la campagna. Squadra L95–100: Alakazam (`Bilancia`), Tropius (`Carruba`), Lucario (`Giustizia`), Togekiss (`Verità`), Gardevoir (`Codice`), Absol (`Sentenza`) (dettagli mosse/IV nel Modulo 6.38). Nessuna fanfara di vittoria dopo: solo il vento e un dialogo. |
| P-03 | Fantasma di Rocca Busambra | Ficuzza (Corleone), cima (con `Scalaroccia` e Cascata) | Primo dei **4 «Fantasmi della Prima Repubblica»** (allenatore 730, L85–90): i vecchi padrini-statisti invisibili degli anni '70–'80 che crearono «U Sistema» prima ancora di Mistretta. Usa Pokémon Buio/Terra/Roccia leggendari e antichi che incarnano il feudo inespugnabile della montagna. |
| P-04 | Fantasma del Cratere Centrale + **Ho-Oh (`FeniceEtnea`)** | Etna, sommità (dopo `D-CT-01` e `Scalaroccia`) | Secondo Fantasma della Prima Repubblica (allenatore 731, il vecchio signore delle eruzioni e delle ricostruzioni etnee). Sconfitto il Fantasma, sulla bocca del Cratere Centrale scende **Ho-Oh** (rinominato nel Modulo 3, es. `FeniceEtnea` / `Mongibeddu` sacro, L85), l'antico Pokémon leggendario del fuoco vulcanico la cui collera per i roghi dolosi e gli abusi edilizi alimentava la cenere eterna dell'Etna: catturarlo o placarlo rappresenta la riconciliazione con la montagna. |
| P-05 | Fantasma del Castello Ursino | Catania, sotterranei lavici (`D-CT-07`, con `Scalaroccia`) | Terzo Fantasma della Prima Repubblica (allenatore 732): l'architetto occulto dei salotti e delle concessioni catanesi, nascosto nelle camere sepolte dalla colata del 1669 coi suoi Pokémon Spettro/Acciaio/Fuoco L85–90. |
| P-06 | Fantasma di Pantelleria | Pantelleria (traghetto da Trapani, solo post-game): Lago Specchio di Venere, dammusi (mappa nuova) | Quarto Fantasma della Prima Repubblica (allenatore 733): l'esiliato d'oro ritiratosi tra i dammusi di pietra lavica e i vapori termali dello Specchio di Venere, custode dei segreti dei traffici mediterranei (L88–90). |
| P-07 | I Tre Venti di Sicilia | vaganti nell'isola | Sbloccati dopo il primo incontro coi Fantasmi: i tre Pokémon leggendari vaganti **Entei, Raikou e Suicune** percorrono le strade della Sicilia come i **Tre Venti dell'Isola** — **Scirocco** (Entei, il vento africano infuocato), **Tramontana** (Raikou, la tempesta elettrica dei monti) e **Maestrale** (Suicune, la corrente purificatrice dei mari e delle sorgenti, antitesi della mafia dell'acqua). |
| P-08 | **Lugia (`ScillaCariddi`)** nei gorghi dello Stretto | `D-ME-04` (Gorghi di Cariddi, fondo abissale) | Si sblocca dopo aver battuto Maria (`P-02`): nel punto più profondo della fossa dello Stretto di Messina, là dove nessuna «Società Stretto Eterna» potrà mai gettare un pilone, riposa **Lugia** (rinominato nel Modulo 3, L85), il guardiano abissale delle correnti tra Ionio e Tirreno. |
| P-09 | Fiera del Mediterraneo | Palermo | L'ex polo fieristico abbandonato di Palermo viene riaperto dagli Estimatori come cittadella sportiva: ospita le 5 strutture della **Frontiera Lotta di HeartGold** (come padiglioni della Fiera) dove sfidare gli allenatori più tecnici dell'isola senza corruzione né raccomandazioni. |
| P-10 | Nunzio riapre l'officina | San Cristoforo (`MAP_CT_CATANIA_OFFICINA`) | Chiusura di `ST-04`: dopo la caduta di `U Cassiere`, Nunzio riapre l'officina libera dal pizzo biologico; missione di consegna dei ricambi meccanici ed elettrici portati dai Pokémon di 4 province. |
| P-11 | Il libro di Turi | Acireale | Distribuire 9 copie del memoriale politico di Turi (*«Come abbiamo quasi salvato la Sicilia coi Pokémon»*, che nessuno vuole leggere) — una battuta per provincia che riflette la proporzione 60/40. |
| P-12 | Pokédex nazionale: l'Opera Omnia di Strano | Prof. Strano, Catania (`MAP_CT_CATANIA_VERMUT`) | Completamento dell'Atlante Biopolitico oltre il Pokédex regionale con le specie rare e post-game: il Prof. Strano pubblica finalmente il volume indipendente contro il parere del Senato Accademico. |

### Ore del post-game

Ritrovi (8 × 4 sfide) 8 h · Maria 2 h (più preparazione) · Fantasmi e leggendari 8 h · Fiera 6 h · missioni P-10/P-11 e ri-sfide degli allenatori 6 h. **Totale ≈ 30 h.**

---

## 12. Riepilogo numerico (per il controllo dei Moduli 2 e 6)

| Prov. | Principali | Secondarie | Dungeon | Boss secondari | Easter egg | Segreteria (Cacicco di «U Sistema») |
|---|---|---|---|---|---|---|
| CT | 10 | 10 | 7 | 6 | 6 | Normale, Chansey 18 (Monopolio Pokémon curatori) |
| SR | 5 | 9 | 4 | 3 | 4 | Acqua, Lanturn 25 (Racket portuale e inceneritori chimici) |
| RG | 4 | 8 | 3 | 3 | 4 | Erba, Victreebel 31 (Catena del freddo e jamming Comiso) |
| CL | 4 | 8 | 4 | 3 | 4 | Roccia, Rhydon 37 (Frane a comando e pozzi MUOS) |
| AG | 5 | 9 | 4 | 4 | 4 | Terra, Gastrodon 43 (Furto idrico negli Ipogei e cemento notturno) |
| TP | 5 | 8 | 5 | 3 | 4 | Volante, Staraptor 49 (Vento truccato nei parchi eolici) |
| ME | 8 | 9 | 4 | 4 | 4 | Acciaio, Magnezone 55 (Burocrazia magnetica dello Stretto e pascoli fantasma) |
| PA | 5 | 10 | 6 | 4 | 5 | Buio, Drapion 61 (Pizzini alati di Ficuzza e pacchetti di voti) |
| EN + finale | 8 | 6 | 4 | — | 4 | Psico, Slowking 66 (Cavilli elettorali) + Lega (70–76) + Mistretta (82–88) |
| **Totale** | **54** | **77** | **41** | **30** | **39** | 9 Segreterie + 4 Campioni + Presidente |
| Post-game | 12 voci P | | | | | Maria (95–100), 4 Fantasmi (85–90), Leggendari di Trinacria |

Flag necessari (R-08): 262 di completamento (54 M + 77 S + 41 D + 30 B + 40 E, compreso E-ST-09, + 8 C + 12 P) e 22 di sottotrame e stato, in 0x840–0x95B; la visibilità degli NPC e gli oggetti usano l'intervallo storico liberato (registro `docs/MODULO_2/2.4_FLAGS_VARS.json`).

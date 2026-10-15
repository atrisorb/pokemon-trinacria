# Pokémon Trinacria — Trama espansa, sottotrame e missioni secondarie

**Versione:** 1.1 · 15/10/2026 · autore del progetto: **atrisorb**
**Fonte:** `F:\Progetti\pokeheartgold\docs\trinacria_spec\` (PLOT_TO_BE_ENRICHED.md, STORY_STATE_MACHINE.json, LLM_MASTER_INSTRUCTIONS.md, SCRIPT_GENERATION_TEMPLATE.md). Questo documento le **estende**: dove le specifiche sono vaghe o in contraddizione, la decisione presa qui è vincolante per i Moduli 2–7 (registro §0).

Il documento è il «canone narrativo». Non contiene ancora le battute: le scrive il Modulo 6, comune per comune, a partire da qui. I nomi siciliani di Pokémon, mosse e strumenti citati sono quelli delle specifiche; quelli mancanti li fissa il Modulo 3.

**Novità della versione 1.1:** decisione R-09 (come i luoghi della trama diventano mappe, dal registro `docs/MODULO_2/2.1_MAPS_CT_SR_RG.json`) e tabelle dei dungeon di CT, SR e RG allineate al registro. Per sapere **in quale mappa** si svolge una missione fa fede il campo `contenuti_trama` del registro del Modulo 2.

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
2. Da TP a ME: Palermo è chiusa dalla «Zona rossa» del Grande Comizio del Presidente Mistretta (cordone di polizia: gag ricorrente). Si attraversa con la **scena del pullman regionale delle 5:40** (sequenza scriptata Trapani → Sant'Agata di Militello, fermate soppresse, aria condizionata rotta): si arriva nei **Nebrodi** → **ME**.
3. Da ME a PA: Pippo ti porta col traghetto dello Stretto a Villa San Giovanni e all'aeroporto di Reggio Calabria (fuori mappa, scena), da lì volo per **Punta Raisi** (Cinisi, Aeroporto Falcone e Borsellino). Così l'Atto V entra in Palermo **da ovest**, come chiedono le specifiche: Cinisi → A29 a Capaci → Isola delle Femmine → Palermo.
4. **PA** → A19 (deviazioni sulle trazzere) → **EN** (Dossier 9) → Volo a Palermo per la **Lega** → **Piazza Armerina** (finale).

### R-03 — I 9 Dossier e le MN (slot delle medaglie verificati in `src/field_move.c`)

| N. | Dossier | Segreteria (luogo) | Slot medaglia | Sblocca (MN, nome delle specifiche) |
|---|---|---|---|---|
| 1 | Dossier Liotru | Catania, Palazzo degli Elefanti | `BADGE_ZEPHYR` | Spaccaroccia → `Martiddata` |
| 2 | Dossier Aretusa | Siracusa, Ortigia (Castello Maniace) | `BADGE_HIVE` | Taglio → `Roncigghiu` |
| 3 | Dossier Carrubba | Ragusa Ibla | `BADGE_PLAIN` | Forza → `Spallata` |
| 4 | Dossier Pirrera | Caltanissetta | `BADGE_FOG` | Surf → `Aliscafu` |
| 5 | Dossier Telamuni | Agrigento | `BADGE_STORM` | Volo → `Passaggiu` |
| 6 | Dossier Mulinu | Erice, Castello di Venere | `BADGE_MINERAL` | — (obbedienza) |
| 7 | Dossier Pilunu | Messina | `BADGE_GLACIER` | Mulinello (nome nel Modulo 3): i gorghi di Cariddi nello Stretto |
| 8 | Dossier Geniu | Palermo, Palazzo delle Aquile | `BADGE_RISING` | Cascata (nome nel Modulo 3): Cascata delle Due Rocche |
| 9 | Dossier Cerere | Enna Alta | `BADGE_EARTH` | Scalaroccia (nome nel Modulo 3): post-game |

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
4. **Luoghi della memoria in tono sobrio** (niente lotte, niente battute, musica dedicata): Capaci e Isola delle Femmine (A29, steli e Giardino della Memoria Quarto Savona Quindici), Casa Memoria a Cinisi, il Grande Cretto di Gibellina, Portella della Ginestra, il CIDMA di Corleone, la Porta d'Europa a Lampedusa, l'hotspot di Pozzallo.
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

### R-09 — Dai luoghi alle mappe (registro del Modulo 2)

HeartGold ha **540 slot di mappa** e la matrice del mondo esterno ha al massimo **47×17 = 799 celle**. Per far stare tutta la Sicilia, il registro delle mappe (blocco 2.1, 15/10/2026) segue queste regole. Valgono anche per i blocchi 2.2 e 2.3.

**R-09.1 — Piani e sale diventano stanze.** Quando la trama dice «N mappe» o «N piani», nel gioco sono **stanze** di una stessa mappa, collegate da warp (di solito due per mappa). Piani, allenatori ed eventi restano quelli della trama: cambia solo il numero di slot usati.

| Dungeon o luogo | Trama | Registro 2.1 |
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

Hanno invece una mappa esterna propria: Ognina, Plaia, Fontanarossa, Aci Trezza, Etna Sud, Neapolis, Ortigia, Vendicari (ingresso), Marzamemi, Ibla, Marina di Ragusa, aeroporto di Comiso, Punta Secca.

**R-09.3 — Interni tolti: la scena si svolge all'aperto.**

| Interno della trama | Dove si svolge ora |
|---|---|
| Rifugio Sapienza | solo esterno, nella mappa Etna Sud |
| Stazione di Randazzo (S-CT-08) | binario e capostazione all'aperto; il viaggio è una mappa di scena (il treno) da cui si scende a Bronte |
| Palazzo del Barone della Timpa (B-CT-05) | lotta all'aperto sulla Timpa (cella sud di Acireale) |
| Bottega del ceramista (S-CT-07) | il ceramista aspetta in cima alla Scalinata |

**R-09.4 — Vendicari è la Zona Safari di HeartGold.** Il motore attiva la modalità Safari solo su quegli slot: casa del guardiaparco (slot 173), snodo della riserva (357) e 14 aree (343–356) che prendono il nome dai luoghi della riserva (Pantano Grande, Pantano Piccolo, Pantano Roveto, Torre Sveva, Tonnara di Vendicari, Cittadella dei Maccari, Spiaggia di Calamosche, Eloro, Pantano Sichilli, Saline, Macchia mediterranea, Dune, Scogliera, Pantano Gorgo). Le aree non hanno testi propri, quindi non hanno banco gemello.

**R-09.5 — Centri Pokémon con negozio.** Ogni Centro ha anche il bancone del negozio: non esistono mappe separate per i negozi. A Modica il laboratorio di cioccolato fa da Centro e da negozio (M-RG-01).

**R-09.6 — Due regioni nel Pokégear.** La mappa del Pokégear è divisa in **Sicilia orientale** (mappe con cella principale in colonna ≥ 24 della matrice; lato «Kanto» del motore) e **Sicilia occidentale** (lato «Johto»). Tutte le province di CT, SR e RG sono orientali. Da confermare nel Modulo 4.4.

**R-09.7 — Nebbia gialla del polo petrolchimico.** Augusta, Priolo e le mappe del polo usano il valore meteo **9** (`WEATHER_UNKNOWN_9`, probabilmente nebbia, mai usato da HeartGold). Va verificato a schermo nel Modulo 7: se non mostra nebbia, quelle mappe tornano a `WEATHER_SUNNY` e il Modulo 4 dà la tinta gialla al tileset.

---

## 1. Sottotrame trasversali

| Codice | Sottotrama | Come attraversa il gioco | Chiusura |
|---|---|---|---|
| ST-01 | **I comizi di provincia** | In ogni capoluogo, dopo il Dossier, un comizio in piazza con palco, folla di sprite e un «disturbatore» del Sistema da battere. +2 di Consenso. Il discorso del protagonista cambia tono man mano (da italiano accademico a lingua di strada). | Comizio finale a Piazza Duomo di Catania (scena del palco). |
| ST-02 | **Il Fascicolo Trinacria** (Maria) | Maria raccoglie atti non coperti da segreto: in ogni provincia il giocatore trova un «Atto» (strumento chiave, 9 in tutto) che smaschera un pezzo della rete di Mistretta. Maria ripete: «il palazzo non si cambia da dentro». | Gli Atti non bastano per un processo: Maria lo dice nel finale. Nel post-game diventano la chiave della sfida segreta sul tetto del Palazzo di Giustizia. |
| ST-03 | **La comunicazione di Turi** | In ogni provincia Turi lancia una campagna social disastrosa (gaffe: il santino col nome sbagliato, il jingle neomelodico, il video coi cavalli). Una gaffe per provincia = una piccola missione di «riparazione» (S-xx-01 di ogni provincia). | Nel finale Turi piange abbracciando Orazio sul palco; nel post-game scrive un libro che non legge nessuno. |
| ST-04 | **Il fratello di Orazio** | Il fratello di Orazio, Nunzio, ha chiuso l'officina per il pizzo. Orazio cerca il capo del racket, «U Cassiere», che si sposta da una provincia all'altra. Indizi in CT, RG, AG, PA. | Lo si affronta a Palermo (B-PA-04). Nunzio riapre l'officina in via Plebiscito nel post-game. |
| ST-05 | **I soldi della notte** (Christian) | Il «Privè Zagara» della Plaia (inventato) ricicla contanti con i buttafuori. Christian infiltrato passa al giocatore liste e codici. Tappe: CT, SR (Marzamemi), ME (Taormina), PA (Mondello). | Il Privè chiude; Christian apre un canale di musica e organizza i Ritrovi al Cubbar nel post-game. |
| ST-06 | **Il voto a 50 euro** (Chantal) | In ogni provincia c'è un «Cambiavoti» (compra voti con la foto in cabina). Chantal insegna a riconoscerli: un minigioco di osservazione (trovare l'NPC con il telefono in mano davanti al seggio-scuola). 9 Cambiavoti = 9 boss minori. | Con 9 Cambiavoti sconfitti Chantal regala la `UrnaElettor.` (Master Ball) prima della Lega. |
| ST-07 | **I faldoni di Totò** | Totò conosce i segreti dell'ARS. Dal primo contatto (telefonata a Fontanarossa) lascia «faldoni» nascosti nelle province (9 oggetti nascosti, uno per provincia). | Con 9 faldoni si apre la scorciatoia della Via della Lega (salta due piani del dungeon). |
| ST-08 | **La guerra dell'acqua** (Calogero) | Inizia a Licata (AG), riprende a Trapani (saline e pozzi), a Lipari (dissalatore) e a Enna (Pergusa prosciugato). | Nel post-game le saracinesche dell'acquedotto restano aperte solo dove il giocatore ha completato le missioni: le battute cambiano. |
| ST-09 | **La Prima Pietra** (Pippo) | In ogni provincia c'è un cartello «Ponte sullo Stretto — Posa della prima pietra». A ogni atto la data cambia (1971, 1985, 2003, 2012, 2026, «prossimamente»). Leggere i 9 cartelli è un collezionabile (E-ST-09). | Nel post-game il cartello di Torre Faro dice «Posa della prima pietra: dopo le dimissioni del Presidente». |
| ST-10 | **I tagli del nastro** (Mistretta) | Mistretta appare **di persona** una volta per provincia, sempre irraggiungibile: inaugura un ospedale senza reparti, una strada che finisce in un campo, un depuratore senza tubi. Il giocatore non può sfidarlo; può solo parlarci. | Piazza Armerina. |
| ST-11 | **La cenere** | Dal Fontanarossa in poi l'Etna è in parossismo ricorrente (`FLAG_ETNA_ASH_ACTIVE`): meteo `RinaDiL’Etna` nell'area etnea, volo bloccato. | `FLAG_ELICOTTERO_PRIVATO` a Messina (M-ME-07); la cenere resta per sempre (gag). |
| ST-12 | **Il Pokédex del Prof. Strano** | Il «vecchio professore disilluso» del Vermut è il **Prof. Alfio Strano**, zoologo in pensione dell'Università di Catania. Consegna il Pokédex al Capitolo 1 e valuta il completamento per telefono. | Pokédex regionale completo → `Amuleto` (oggetto, Modulo 3) e diploma «ad honorem». |

### I compagni: arco e missione personale

| Codice | Compagno | Si unisce | Missione personale (oltre alla sottotrama) | Ruolo nel post-game |
|---|---|---|---|---|
| C-01 | Turi | Capitolo 1 (Vermut) | «Il cavallo di Santa Venera»: recuperare il cavallo del padre venduto a un allevatore del Carnevale (Acireale). | Ritrovo al Vermut (lunedì) |
| C-02 | Orazio | Capitolo 2 (San Cristoforo) | ST-04 | Ritrovo in via Plebiscito (martedì) |
| C-03 | Christian | Capitolo 2 (Galermo) | ST-05 | Ritrovo al Cubbar (sabato notte, 22:00–04:00 dell'orologio del DS) |
| C-04 | Chantal | Capitolo 2 (Librino) | ST-06 | Ritrovo al Palazzo di Cemento (mercoledì) |
| C-05 | Maria | Capitolo 1 (Vermut), poi Atto II | ST-02 | Super-boss sul tetto del Palazzo di Giustizia di Catania |
| C-06 | Totò | telefonata a fine Atto I; di persona a Palermo | ST-07 | Ritrovo a Ballarò (giovedì) |
| C-07 | Calogero | Capitolo 7 (Licata) | ST-08 | Ritrovo al porto di Licata (venerdì) |
| C-08 | Pippo | Capitolo 9 (Torre Faro) | ST-09 | Ritrovo a Ganzirri (domenica) |

---

## 2. Provincia di Catania (CT) — Atto I · ore 0–15 · Dossier 1

**Area dialettale:** orientale non metafonetica (catanese-etneo). Quartieri con registro proprio: Corso Italia (Catania «bene»), San Cristoforo/Tondicello (popolare stretto, rotacismo), San Giovanni Galermo (periferia + gergo giovanile), Librino (iper-popolare), Acireale/Timpa (acese). Gallo-italico: nessuno in provincia.
**Musiche guida (Modulo 5):** techno del Cubbar, «chill» del Vermut, caos di via Etnea, mercato della Pescheria, allarme della cenere.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito / ricompensa |
|---|---|---|---|---|
| M-CT-00 | Prologo: la notte al Cubbar | Misterbianco, Cubbar | Flashback giocabile alle 3:30. Christian all'ingresso VIP; tavoli con bottiglie e candele scintillanti; il giocatore cammina nel privè, parla con 6 NPC della movida (figli di avvocati, di magistrati, un PR), nessuna lotta. Uscita = dissolvenza. | `FLAG_INTRO_CUBBAR` |
| M-CT-01 | Il risveglio in Corso Italia | Catania, casa del protagonista | Ore 14:00. Camera con codici LUISS, diploma del Cutelli, lettera di non idoneità. La madre (Graziella) urla dal salone del figlio dell'avvocato Lombardo. Scelta del nome. | Inizio partita, VAR_TRINACRIA_ATTO = 1 |
| M-CT-02 | Il Vermut e la scintilla | Via Etnea → Via Gemmellaro | Attraversare via Etnea (promoter, munnizza nei vicoli). Al Vermut: Turi, Maria, il Prof. Strano. L'auto blu dell'assessore blocca via Santa Filomena per gli arancini da Savia; i suoi scagnozzi intimidiscono un commerciante. Maria spiega gli insabbiamenti. Decisione: candidarsi. Turi regala lo starter dalla scatola di paste di mandorla; il Prof. Strano dà il Pokédex. Prima lotta contro uno scagnozzo dell'assessore. | Starter, Pokédex, `FLAG_VERMUT_EPIPHANY`, Consenso 1 |
| M-CT-03 | San Cristoforo: l'officina | San Cristoforo, via Plebiscito | Braci di carne di cavallo; Orazio assediato dagli strozzini nell'officina del fratello. Tre lotte contro gli strozzini nei vicoli + boss B-CT-01. | Orazio nel gruppo, `SH 300 Scassatu` (bicicletta), `FLAG_RECRUIT_ORAZIO` |
| M-CT-04 | San Giovanni Galermo: la notte che paga | Galermo, case popolari | Christian porta il giocatore dentro le dinamiche della movida: scopre il Privè Zagara (inventato) e il ruolo dei buttafuori nel giro del contante. Lotta con 3 buttafuori. | `FLAG_RECRUIT_CHRISTIAN`, primo indizio ST-05 |
| M-CT-05 | Librino: i dieci piani | Librino, Palazzo di Cemento | Ascensore rotto dal 1998: dungeon verticale D-CT-02. Chantal, al 7° piano nel suo salone di unghie abusivo, chiede di battere il Capo-Condominio (B-CT-02) che gestisce l'allaccio abusivo dell'acqua e i pacchi alimentari elettorali. | `FLAG_RECRUIT_CHANTAL`, Consenso +3 |
| M-CT-06 | L'Etna che brucia | Nicolosi, Pineta dei Monti Rossi → Crateri Silvestri | Un incendio doloso per incassare gli appalti di rimboschimento. Dungeon D-CT-01; boss B-CT-03 (l'Incendiario della Forestale, inventato). | Consenso +3, MT (Modulo 3) |
| M-CT-07 | L'Oro Verde | Bronte | Il cartello agro-mafioso (inventato) del pistacchio taglieggia i piccoli coltivatori. Dungeon D-CT-03 tra i pistacchieti sulla sciara; boss B-CT-04. | Consenso +3 |
| M-CT-08 | Segreteria 1: il Ras della Sanità Privata | Catania, Palazzo degli Elefanti | Dungeon-ufficio: corridoi con code di pazienti, sportelli «torna domani». 4 allenatori (Primario, Convenzionato, Informatore, Centralinista). Boss: **Dott. Ignazio Calì**, il Ras delle cliniche convenzionate. Tipo **Normale**, asso Chansey L18. | **Dossier Liotru**, `FLAG_DOSSIER_CT`, comizio ST-01 a Piazza Duomo |
| M-CT-09 | L'incubo di Fontanarossa | Aeroporto di Catania-Fontanarossa, Terminal A | Telefonata di Totò: il cavillo della Commissione Elettorale impone il deposito del pre-contrassegno entro 3 ore. A19 interrotta, unica via il volo delle 12:30. Alla rotonda dell'aeroporto parte la cenere (`FLAG_ETNA_ASH_ACTIVE`, primo `Warp` di aggiornamento). Terminal A: tabelloni «CANCELLATO», migliaia di passeggeri a terra, acqua a 5 euro, nessuna navetta. Dungeon D-CT-04 (rivolta). Boss: il **Direttore Operativo dello Scalo** (inventato). Sala VIP: Maria invia la PEC con firma digitale. | `FLAG_FONTANAROSSA_ASH_CRISIS`, `FLAG_SAC_VIP_LOUNGE_PEC_SENT`, Consenso +3, fine Atto I: si prosegue a piedi verso Siracusa |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo e passi | Ricompensa |
|---|---|---|---|---|
| S-CT-01 | Il santino sbagliato (ST-03) | Turi, Piazza Università | Turi ha stampato 10.000 santini col nome del protagonista sbagliato. Ritrovare i 5 pacchi distribuiti per errore (via Etnea, Villa Bellini, Pescheria, Castello Ursino, Ognina) prima che li veda la stampa. | Consenso +1, `ITEM_AMULET_COIN` |
| S-CT-02 | Il cavallo di Santa Venera (C-01) | Turi, Acireale, discesa della Timpa | Il cavallo del padre di Turi è finito a un allevatore che lo vuole far sfilare al Carnevale. Gara di corsa in bicicletta lungo la Timpa (minigioco a tempo) e lotta col nobile decaduto B-CT-05, all'aperto sulla Timpa (R-09.3). | Consenso +1, Pokémon di tipo Fuoco (Modulo 3) |
| S-CT-03 | La granita di mezzanotte | Gelataio, Acireale, Piazza Duomo | Portare 3 granite a 3 NPC sparsi prima che si sciolgano (timer di 60 secondi tra le mappe). | `GranitaConzu` ×5 |
| S-CT-04 | Ciclopi | Pescatore anziano, Aci Trezza | Il pescatore racconta che i Faraglioni «sono pietre tirate da un gigante con un occhio solo». Lotta in barca tra i Faraglioni contro 4 pescatori. | Consenso +1, `ITEM_SUPER_ROD` |
| S-CT-05 | Le Salinelle | Geologo, Paternò | Raccogliere 4 campioni di fango dalle Salinelle (punti di ispezione) per dimostrare che il comune ha venduto il terreno a un parcheggio. | Consenso +1, MT |
| S-CT-06 | Il Ponte dei Saraceni | Anziana, Adrano | Il ponte medievale è chiuso per «verifiche dal 2009». Battere il geometra comunale (inventato) che ha perso il fascicolo. | Consenso +1, Pietra (Modulo 3) |
| S-CT-07 | I 142 gradini | Ceramista, Caltagirone, Scalinata di Santa Maria del Monte | Sfida a piani: 142 gradini divisi in 7 rampe (7 terrazze della stessa mappa, R-09.2), un allenatore per rampa, senza curarsi (D-CT-05). Il ceramista aspetta in cima. | Consenso +1, `ITEM_LEFTOVERS` |
| S-CT-08 | La Circumetnea | Capostazione, Randazzo (binario all'aperto, R-09.3) | Il trenino si ferma ovunque tranne che alle fermate. Viaggio scriptato Randazzo–Bronte con 3 soste impreviste (una lotta per sosta) in una mappa di scena (il treno). | Consenso +1, apre la Grotta del Gelo (D-CT-06) |
| S-CT-09 | Sant'Agata (evento a calendario) | Devoto, Cattedrale | Dal 3 al 5 febbraio (orologio del DS): processione con le candelore, il giocatore aiuta a portare una candelora (minigioco di equilibrio). | Strumento raro (Modulo 3) |
| S-CT-10 | Cambiavoti di Catania (ST-06) | Chantal, scuola-seggio di Librino | Trovare il Cambiavoti tra 8 NPC davanti al seggio (indizio: telefono in mano e busta). Lotta. | Consenso +1 |

### Dungeon

| Codice | Nome | Piani / struttura | MN richieste | Selvatici (tema) | Boss finale |
|---|---|---|---|---|---|
| D-CT-01 | Crateri Silvestri e Monti Rossi | 3 aree: pineta in fiamme, colata del 2001, bocca spenta (2 mappe, R-09.1) | — | Fuoco, Roccia, Volante (Taddarita nei tubi di lava) | B-CT-03 |
| D-CT-02 | Palazzo di Cemento di Librino | 10 piani a scale in 5 mappe da 2 piani (R-09.1); ballatoi con allacci abusivi; panni stesi che bloccano i corridoi (si spostano parlando con chi li ha stesi) | — | nessun selvatico; 9 allenatori (uno per piano) | B-CT-02 al 10° |
| D-CT-03 | Sciara dei pistacchi (Bronte) | 2 aree di campagna lavica a terrazze, cancelli del cartello (1 mappa) | — | Erba, Coleottero, Terra | B-CT-04 |
| D-CT-04 | Terminal A di Fontanarossa | 4 aree in 2 mappe: atrio + controlli di sicurezza, gate + sala VIP | — | nessun selvatico; 8 allenatori («Bagaglisti Esauriti», «Funzionari SAC» inventati, «Turisti Accaldati») | Direttore Operativo dello Scalo |
| D-CT-05 | Scalinata di Santa Maria del Monte | 7 rampe = 7 terrazze consecutive della cella sud di Caltagirone (R-09.2) | — | — | Ceramista (S-CT-07) |
| D-CT-06 | Grotta del Gelo (Randazzo, versante nord) | 2 piani di ghiaccio perenne dentro la lava (1 mappa) | `Martiddata` | Ghiaccio, Roccia | B-CT-06 (opzionale) |
| D-CT-07 | Sotterranei del Castello Ursino | 3 piani (1 mappa) | `Scalaroccia` | Spettro, Roccia | post-game P-05 |

### Boss secondari

| Codice | Nome (inventato) | Ruolo | Tipo | Livello asso |
|---|---|---|---|---|
| B-CT-01 | Nino «U Strozzinu» | capo degli strozzini di San Cristoforo | Buio | 12 |
| B-CT-02 | Il Capo-Condominio | gestisce allacci abusivi e pacchi elettorali a Librino | Normale/Veleno | 14 |
| B-CT-03 | L'Incendiario della Forestale | appicca incendi per gli appalti di rimboschimento | Fuoco | 15 |
| B-CT-04 | Don Saro del Pistacchio | capo del cartello dell'Oro Verde | Erba/Terra | 16 |
| B-CT-05 | Il Barone della Timpa | nobile decaduto di Acireale, coi cavalli del Carnevale | Fuoco/Normale | 17 |
| B-CT-06 | Il Custode del Gelo | eremita che vende ghiaccio dell'Etna «DOP» | Ghiaccio | 20 |

### Meme ed easter egg

| Codice | Contenuto |
|---|---|
| E-CT-01 | Il Liotru di Piazza Duomo: parlandoci 10 volte di fila dice «…» poi «Ancora qui sei?». |
| E-CT-02 | «Arancinu» vs «arancina»: a Catania ogni NPC che vende arancini corregge il giocatore se usa la parola palermitana (scelta Sì/No). Ricompensa diversa a Palermo (E-PA-01). |
| E-CT-03 | Il cartello della Circumetnea con l'orario «indicativo». |
| E-CT-04 | Il motorino parcheggiato sul marciapiede di via Etnea che sposta posizione a ogni visita. |
| E-CT-05 | ST-09: primo cartello della «Posa della prima pietra» davanti alla stazione centrale. |
| E-CT-06 | Una bottiglietta d'acqua a 5 € al bar del Terminal A (strumento comprabile: identico all'`AcquaFuntana`, costa 10 volte tanto). |

---

## 3. Provincia di Siracusa (SR) — Atto II · ore 15–22 · Dossier 2

**Area dialettale:** siracusano settentrionale non metafonetico (Augusta, Priolo, Melilli, Lentini, Siracusa città); siracusano meridionale verso Noto, Avola, Pachino (tratti sud-orientali). Musica: «cortina di fumo» industriale, barocco di Noto, mare di Ortigia.
**Meteo speciale:** nebbia giallastra ad Augusta, a Priolo e nel polo petrolchimico (valore meteo 9, da verificare a schermo; in alternativa sole e tinta gialla del Modulo 4: R-09.7).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-SR-01 | La SS114 a piedi | SS114 Catania–Augusta | Lunga strada costiera con il Simeto e i ponti; prima comparsa del Cambiavoti di Lentini (ST-06). | — |
| M-SR-02 | La cortina di fumo | Augusta → Priolo → Melilli | Operai e pescatori mostrano il mare. I dirigenti del petrolchimico (inventati) finanziano Mistretta: il giocatore entra nel polo (D-SR-01) per fotografare uno scarico. | Consenso +3, `FLAG_AUGUSTA_REFINERY_CLEARED` |
| M-SR-03 | La Mafia dei VIP | Marzamemi e Noto | Tonnara di Marzamemi trasformata in club esclusivo con concessione demaniale a 200 € l'anno (inventato); invasione di turisti milanesi radical-chic in piazza Regina Margherita. Galà in tonnara, 4 lotte con «Concessionari». | Consenso +3, `FLAG_MARZAMEMI_VIP_BUSTED` |
| M-SR-04 | Maria a Ortigia | Siracusa, Fonte Aretusa | Maria arriva da Ragusa con il primo Atto (ST-02). Spiega le concessioni portuali. | — |
| M-SR-05 | Segreteria 2: il Barone delle Concessioni Portuali | Ortigia, Castello Maniace | Dungeon nel castello con le maree (passerelle che si allagano a orari fissi). Boss: **Comm. Corrado Spataro**, «U Baruni dû Portu». Tipo **Acqua**, asso Lanturn L25. | **Dossier Aretusa**, `FLAG_DOSSIER_SR`, comizio in piazza Duomo di Ortigia |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-SR-01 | Il jingle neomelodico (ST-03) | Turi, Siracusa, Corso Matteotti | Turi ha fatto un jingle elettorale imbarazzante. Ritirare le copie dalle 4 radio di quartiere (lotta con ogni DJ). | Consenso +1 |
| S-SR-02 | L'Orecchio di Dionisio | Guida turistica, Neapolis | Minigioco dell'eco: ripetere sequenze di suoni (SFX di HeartGold) nella grotta. | MT |
| S-SR-03 | Le arance di Lentini | Agrumicoltore, Lentini | I vecchi magazzini agrumari sono occupati dai trasportatori del clan: liberarne 3. | Consenso +1, bacche (Modulo 3) |
| S-SR-04 | Il Biviere | Birdwatcher, Lentini (cella ovest, R-09.2) | Fotografare 5 Pokémon Volante sul lago (punti di osservazione). | `ITEM_SOOTHE_BELL` |
| S-SR-05 | Vendicari (zona Safari) | Guardiaparco, Noto | Riserva con fenicotteri e biglietto d'ingresso: è la Zona Safari di HeartGold (cattura con strumenti a numero limitato), con 14 aree che prendono il nome dai luoghi della riserva (R-09.4). | accesso permanente |
| S-SR-06 | La granita del Caffè | Cameriere, Noto, Corso Vittorio Emanuele | Consegna della granita di mandorla a un anziano della Cattedrale che non può più scendere le scale. | Consenso +1 |
| S-SR-07 | Isola delle Correnti | Pescatore, Portopalo | L'estremo sud (cella sud di Portopalo, R-09.2): raggiungere l'isolotto con la bassa marea (orario del DS 6:00–9:00) e battere il Guardiano del Faro. | Consenso +1, pietra rara |
| S-SR-08 | Il Nero d'Avola | Vignaiola, Avola | Ritrovare 6 casse rubate nella pianta esagonale della città (indizi sui muri). | Consenso +1 |
| S-SR-09 | Cambiavoti di Siracusa (ST-06) | Chantal (telefono), Avola, scuola | Come S-CT-10. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-SR-01 | Polo petrolchimico (Augusta–Priolo) | 4 aree in 2 mappe: pontili + serbatoi, sala controllo + torcia (R-09.1) | `Martiddata` (barriere di calcestruzzo) | Veleno (`Ciminièra`, `Priolu`), Acciaio, Elettro | B-SR-01 |
| D-SR-02 | Latomie del Paradiso | 2 aree in cava (1 mappa: Latomia del Paradiso, Orecchio di Dionisio) | — | Roccia, Spettro, Buio | B-SR-02 |
| D-SR-03 | Tonnara di Marzamemi | 2 aree in 1 mappa (camera della morte, magazzini del club) | `Roncigghiu` | Acqua | M-SR-03 |
| D-SR-04 | Castello Maniace | 3 aree a marea in 2 mappe: ingresso + cortile a marea, sala della Segreteria | — | Acqua | Segreteria 2 |

### Boss secondari

| Codice | Nome (inventato) | Ruolo | Tipo | Liv. |
|---|---|---|---|---|
| B-SR-01 | L'Ing. della Torcia | dirigente del polo che dice «la torcia è un fenomeno ottico» | Veleno/Acciaio | 23 |
| B-SR-02 | Il Tiranno delle Latomie | guida abusiva che fa pagare l'eco | Spettro | 22 |
| B-SR-03 | La Concessionaria di Marzamemi | gestrice del club in tonnara | Acqua/Volante | 24 |

### Meme ed easter egg

E-SR-01 La statua di Archimede a Ortigia: un NPC chiede «Eureka?» e regala una `Pietra` se si risponde «Sì». · E-SR-02 Il cartello del Ponte (ST-09) in piazza Pancali. · E-SR-03 Il turista milanese a Marzamemi che ordina «una granita al pistacchio di Bronte, ma senza zucchero, senza pistacchio». · E-SR-04 La luce del faro di Capo Passero che lampeggia in codice Morse «MUNNIZZA».

---

## 4. Provincia di Ragusa (RG) — Atto II · ore 22–30 · Dossier 3

**Area dialettale:** sud-orientale ibleo (ragusano, modicano, vittoriese), metafonetico. Maria passa dall'italiano giuridico all'ibleo intimo.
**Musica:** barocco ibleo, mercato all'alba, «cattedrale nel deserto» di Comiso (eco, luci a risparmio).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-RG-01 | Ibla e Modica | Ragusa Superiore → scale → Ibla; Modica Bassa/Alta | Ritrovo con Maria: indaga sul Mercato di Vittoria. Laboratorio di cioccolato a Modica come rifugio (Centro Pokémon locale). | — |
| M-RG-02 | Il mercato all'alba | Vittoria, Mercato Ortofrutticolo | Infiltrazione alle 4:00: padiglioni, camion, prezzi decisi «alla cassa» dai trasportatori imposti (inventati). Dungeon D-RG-01. | Consenso +3, `FLAG_VITTORIA_MARKET_LIBERATED` |
| M-RG-03 | La cattedrale nel deserto | Comiso, Aeroporto «Pio La Torre» | Terminal civile nuovo e deserto: luci a risparmio, un bar chiuso, nastri fermi. I pochi lavoratori raccontano (come opinione) che Comiso è tenuto al minimo come «ruota di scorta sgonfia». Il giocatore trova le carte (inventate) del «Piano Scalo Unico». Lotta contro i caporali del trasporto su gomma che festeggiano ogni volta che Comiso non decolla. Poi la pista: D-RG-02 nell'ex base NATO. | Consenso +3, `FLAG_COMISO_SAC_GHOST_AIRPORT` |
| M-RG-04 | Segreteria 3: il Monopolista della Logistica | Ragusa Ibla, Palazzo (inventato) di via del Mercato | Dungeon a magazzini refrigerati (pavimento scivoloso). Boss: **Cav. Biagio Occhipinti**, re dei TIR dell'ortofrutta. Tipo **Erba**, asso Victreebel L31. | **Dossier Carrubba**, `FLAG_DOSSIER_RG`, comizio al Giardino Ibleo |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-RG-01 | Il video coi cavalli (ST-03) | Turi, Modica | Turi ha girato un video elettorale con i cavalli sul viadotto Guerrieri. Rimuovere il cartellone (lotta con il fotografo). | Consenso +1 |
| S-RG-02 | Cioccolato azteco | Cioccolataia, Modica Alta | Ricetta perduta: 3 ingredienti in 3 comuni (cacao al porto di Pozzallo, zucchero a Vittoria, spezie a Scicli). | `CiucculataModica` ×5 (Modulo 3) |
| S-RG-03 | Il commissariato della TV | Comparsa, Scicli, via Mormino Penna | I pullman di turisti cercano il commissario della televisione. Guidare un gruppo nei 4 luoghi giusti senza farli perdere. | Consenso +1 |
| S-RG-04 | La terrazza di Punta Secca | Bagnante, Santa Croce Camerina | Ritrovare l'asciugamano «del commissario» rubato da un Pokémon selvatico sulla spiaggia. | Strumento (Modulo 3) |
| S-RG-05 | Cava d'Ispica | Archeologo, Ispica | Dungeon rupestre D-RG-03; 5 tombe con iscrizioni (puzzle di sequenza). | Fossile (Modulo 3) |
| S-RG-06 | Torre Cabrera | Guardiano, Pozzallo | Riaccendere la torre per la festa del pesce (consegnare legna). | Consenso +1 |
| S-RG-07 | Il Loggiato del Sinatra | Ristoratore, Ispica | Sfida culinaria: indovinare 3 piatti dagli indizi. | `ITEM_LUCKY_EGG` |
| S-RG-08 | Cambiavoti di Ragusa (ST-06) | Chantal (telefono), Vittoria, scuola | Come S-CT-10. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-RG-01 | Mercato di Vittoria | 3 padiglioni (1 mappa da 3 stanze) + piazzale dei TIR (TIR in movimento a tempo) | `Roncigghiu` (casse e reti) | Erba, Coleottero | B-RG-01 |
| D-RG-02 | Ex base NATO di Comiso | 4 aree in 2 mappe: hangar + bunker, sala radar + pista | `Martiddata` | Acciaio, Elettro, Volante | B-RG-02 |
| D-RG-03 | Cava d'Ispica | 3 aree rupestri in 1 mappa (necropoli, Larderia, grotte alte) | `Spallata` (sblocco al ritorno) | Roccia, Spettro | — |

### Boss secondari

B-RG-01 **Il Caporale dei TIR** (Normale/Acciaio, 28) · B-RG-02 **Il Generale in Congedo** che vive nel bunker «per abitudine» (Acciaio/Volante, 30) · B-RG-03 **La Marchesa di Ibla**, che decide chi entra nei palazzi barocchi (Psico, 29).

### Meme ed easter egg

E-RG-01 Il bar chiuso del terminal di Comiso: parlandoci, «Riapriamo quando arriva un volo». · E-RG-02 Le scale di Ibla contate a schermo (340, numero mostrato da un cartello: gag «Il comune dice 340, i turisti 3.400»). · E-RG-03 Cartello ST-09 a Pozzallo. · E-RG-04 Il serbatoio di carrubbe del Monopolista che contiene… un solo carrubo.

---

## 5. Provincia di Caltanissetta (CL) — Atto III · ore 30–37 · Dossier 4

**Area dialettale:** centrale metafonetica (nisseno); Gela con tratti propri; Niscemi e Mazzarino verso il sud-orientale. Riesi con la comunità valdese (italiano).
**Ambiente:** valloni, frane mai riparate (puzzle `Spallata` e `Martiddata`), zolfare dismesse.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-CL-01 | La strada che non c'è | SS626 / trazzere | Frane «dal 2005»: tre puzzle ambientali (massi da spingere, rocce da rompere). | — |
| M-CL-02 | Gela: l'acropoli e il pontile | Gela | Contrasto tra le mura timoleontee e l'ex petrolchimico; il pontile sbarcatoio lunghissimo (mappa con vento e onde). Lotta con il Cambiavoti di Gela. | Consenso +3 |
| M-CL-03 | Le parabole del MUOS | Niscemi, Sughereta → stazione | Dungeon sci-fi a onde (D-CL-02): «campi» che invertono i comandi a tempo. Scoperta: appalti per lo smaltimento illecito di rifiuti speciali sotto la base (ditta inventata). Nessuna battuta sulle famiglie sgomberate dalla frana. | Consenso +3, `FLAG_NISCEMI_MUOS_QUEST` |
| M-CL-04 | Segreteria 4: il Commissario delle Opere Incompiute | Caltanissetta, viadotto (inventato) «Salso 2» | Dungeon sul viadotto di 400 m mai finito: piloni a quote diverse collegati da passerelle provvisorie. Boss: **Ing. Calogero Lo Monaco**, commissario straordinario da 22 anni. Tipo **Roccia**, asso Rhydon L37. | **Dossier Pirrera**, `FLAG_DOSSIER_CL`, comizio in Corso Umberto |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-CL-01 | Il santino in dialetto (ST-03) | Turi, Caltanissetta | Turi ha scritto il santino «in nisseno» con parole catanesi: correggerlo parlando con 4 anziani (scelte multiple). | Consenso +1 |
| S-CL-02 | Il Castello di Mussomeli | Custode, Mussomeli | Dungeon medievale D-CL-01 sulla rupe; leggenda delle tre dame. | MT |
| S-CL-03 | Le case a 1 euro | Coppia di stranieri, Mussomeli | Aiutarli con la burocrazia: 5 uffici, 5 timbri (giro tra NPC). | Consenso +1 |
| S-CL-04 | La zolfara di Gabbara | Ex minatore, San Cataldo | Dungeon D-CL-03 nelle gallerie di zolfo; il minatore racconta i carusi delle zolfare (tono sobrio). | Pietra (Modulo 3) |
| S-CL-05 | Monte degli Ulivi | Pastore valdese, Riesi | Consegna di provviste al centro; lotta d'allenamento con i ragazzi del centro (amichevole). | `ITEM_EXP__SHARE` (costante reale, doppio trattino basso) |
| S-CL-06 | U Cannuni | Barone decaduto, Mazzarino | Ricostruire la storia del castello «U Cannuni» trovando 4 pietre. | Consenso +1 |
| S-CL-07 | Il Rabato | Anziana, Sutera, Monte San Paolino | Salita al santuario (percorso a scalini) e presepe vivente (dicembre, orologio del DS). | Strumento raro |
| S-CL-08 | Cambiavoti di Caltanissetta (ST-06) | Chantal (telefono), Gela | Come S-CT-10. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-CL-01 | Castello Manfredonico (Mussomeli) | 3 piani sulla rupe | `Spallata` | Spettro, Roccia | B-CL-01 |
| D-CL-02 | MUOS (Niscemi) | 3 mappe: sughereta, recinzione, piazzale delle parabole | `Roncigghiu` | Elettro, Acciaio, Coleottero | B-CL-02 |
| D-CL-03 | Zolfara di Gabbara | 3 livelli di gallerie | `Martiddata`, `Spallata` | Roccia, Terra, Veleno | B-CL-03 |
| D-CL-04 | Viadotto Salso 2 | 4 piloni | — | Volante | Segreteria 4 |

### Boss secondari

B-CL-01 **La Dama del Castello** (Spettro, 34) · B-CL-02 **Il Subappaltatore delle Parabole** (Elettro/Acciaio, 35) · B-CL-03 **U Capumastru** della zolfara (Roccia/Terra, 35).

### Meme ed easter egg

E-CL-01 Le antenne Rai di Sant'Anna: un NPC giura che «trasmettono i pensieri». · E-CL-02 Cartello ST-09 a Caltanissetta. · E-CL-03 Il cartello «Lavori in corso — fine lavori 2006» con sotto un adesivo «2026». · E-CL-04 L'amaro di Caltanissetta offerto da ogni nonno (nome generico, nessun marchio).

---

## 6. Provincia di Agrigento (AG) — Atto III · ore 37–46 · Dossier 5

**Area dialettale:** agrigentino; Licata costiera (Calogero), Sciacca (marinaro di San Michele), Lampedusa (pelagio). Metafonia centrale.
**Tema:** sete, autobotti, abusivismo, la Valle dei Templi.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-AG-01 | Calogero | Licata, porto | Rubinetti a secco da 3 settimane; autobotti abusive a 150 € a carico. Calogero blocca la SS115 coi trattori per far passare il giocatore. | `FLAG_RECRUIT_CALOGERO`, Consenso +3 |
| M-AG-02 | Il tubo bucato | Sciacca → Agrigento | Seguire l'acquedotto provinciale (mappe con tubi visibili): 5 saracinesche chiuse di notte da custodi infedeli (inventati). Si aprono solo tra le 20:00 e le 6:00 dell'orologio del DS. | Consenso +3, `FLAG_WATER_MAFIA_DEFEATED` |
| M-AG-03 | Gli Ipogei | Valle dei Templi | Dungeon D-AG-01 negli acquedotti sotterranei antichi: la cisterna (inventata) da cui il consorzio delle autobotti pesca l'acqua. | — |
| M-AG-04 | Lampedusa | Porto Empedocle → traghetto → Lampedusa | Sottotrama sugli appalti (inventati) per la gestione del centro d'accoglienza e del trasporto di carburante: il giocatore smaschera la ditta che fattura carburante mai consegnato. Tono sobrio alla Porta d'Europa; nessuna satira su chi arriva. | `FLAG_LAMPEDUSA_ARC`, Consenso +3 |
| M-AG-05 | Segreteria 5: il Signore delle Acque e del Cemento | Agrigento, via Atenea → Villaseta | Dungeon tra le palazzine abusive con piani in più; boss: **Geom. Gerlando Iacono**, re del cemento e delle autobotti. Tipo **Terra**, asso Gastrodon L43. | **Dossier Telamuni**, `FLAG_DOSSIER_AG`, `Passaggiu` (Volo) disponibile, comizio in piazza Marconi |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-AG-01 | Il comizio sbagliato (ST-03) | Turi, Agrigento | Turi ha prenotato la piazza sbagliata (Agrigento invece di Licata). Portare 20 sostenitori da un comune all'altro (scena col pullman). | Consenso +1 |
| S-AG-02 | Le Terme di Sciacca | Ex bagnino, Sciacca | Le terme storiche sono chiuse per burocrazia: 4 uffici (Comune, Regione, ASP, Soprintendenza), ognuno manda all'altro. Si riaprono vincendo 4 lotte di «funzionari». | Consenso +1, apre le stufe del Monte Kronio (D-AG-03) |
| S-AG-03 | La Scala dei Turchi | Bagnina, Realmonte | Fermare i ragazzi che grattano la marna bianca per portarsela a casa (4 lotte). | Consenso +1 |
| S-AG-04 | La Torre di Carlo V | Pescatore, Porto Empedocle | Il cartello con il nome letterario della città: trovare il libraio che regala un libro (oggetto da leggere: brano scritto nel Modulo 6). | MT |
| S-AG-05 | L'uva Italia | Agricoltore, Canicattì | Proteggere il raccolto da una banda di Pokémon selvatici (lotta a ondate). | Bacche |
| S-AG-06 | I Sette Cortili | Artista, Favara | Farm Cultural Park come luogo positivo: una caccia alle opere (6 installazioni) tra i vicoli. | `ITEM_SOOTHE_BELL` |
| S-AG-07 | Il Gattopardo e la rosolia | Monaca, Palma di Montechiaro | Le Benedettine: consegnare le materie prime per i dolci di mandorla; lettura del passo del romanzo citato nel luogo (testo nel Modulo 6, parafrasi). | `Cassata` ×3 |
| S-AG-08 | La Spiaggia dei Conigli | Volontaria, Lampedusa | Proteggere le tartarughe: spostare 5 ombrelloni abusivi dalla zona dei nidi. | Consenso +1 |
| S-AG-09 | Cambiavoti di Agrigento (ST-06) | Chantal (telefono), Favara | Come S-CT-10. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-AG-01 | Ipogei della Valle dei Templi | 3 livelli di cunicoli d'acqua | `Aliscafu` (canali), `Spallata` | Acqua, Terra, Roccia | B-AG-01 |
| D-AG-02 | Grotta della Scala dei Turchi | 2 mappe di marna bianca e mare | `Aliscafu` | Acqua, Roccia | B-AG-02 |
| D-AG-03 | Stufe del Monte Kronio (Sciacca) | 3 piani di grotte di vapore | `Martiddata` | Fuoco, Psico | B-AG-03 |
| D-AG-04 | Palazzine di Villaseta | 3 edifici abusivi con piani extra collegati da passerelle | — | — | Segreteria 5 |

### Boss secondari

B-AG-01 **Il Fontaniere Infedele** (Acqua, 40) · B-AG-02 **Il Raschiatore** della marna (Roccia, 39) · B-AG-03 **Il Santone del Vapore** (Psico/Fuoco, 41) · B-AG-04 **L'Appaltatore del Carburante** (Lampedusa; Veleno/Acciaio, 42).

### Meme ed easter egg

E-AG-01 L'autobotte che passa a ogni visita con la musica di un ambulante. · E-AG-02 Il Telamone sdraiato: «Sono stanco, riposo da 2.500 anni, come i lavori della statale». · E-AG-03 Cartello ST-09 a Porto Empedocle. · E-AG-04 Il rubinetto di casa a Licata che, aperto, dà un messaggio diverso ogni giorno della settimana.

---

## 7. Provincia di Trapani (TP) — Atto IV · ore 46–53 · Dossier 6

**Area dialettale:** occidentale (trapanese, marsalese, mazarese); Erice; Favignana egadina. Mai `mbare`/`carusu`.
**Tema:** vento, sale, vino, fantasmi, parchi eolici sui terreni espropriati con prestanome (inventati).

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-TP-01 | Selinunte e i covi | Castelvetrano, Parco di Selinunte, Cave di Cusa | Il parco archeologico; in paese, i covi del superlatitante sono stati smantellati: un museo improvvisato, tono sobrio, nessuna lotta. Il primo indizio sui parchi eolici. | — |
| M-TP-02 | Il silenzio del Cretto | Gibellina | Il Grande Cretto di Burri: labirinto bianco, **nessun Pokémon selvatico, nessuna musica allegra**, solo vento. Tre anziani raccontano i fondi della ricostruzione del Belice divorati dagli speculatori. Nessuna lotta. Gibellina Nuova: architetture utopiche in rovina. | `FLAG_CRETTO_DI_BURRI_EVENT` |
| M-TP-03 | Il vento a pagamento | Mazara del Vallo → Marsala | Pale eoliche su terreni agricoli espropriati con prestanome (inventati): la Kasbah di Mazara, la flotta d'altura; a Marsala le cantine e lo Stagnone (D-TP-02). | Consenso +3, `FLAG_WIND_FARM_SYNDICATE` |
| M-TP-04 | Segreteria 6: il Gran Maestro dei Parchi Eolici | Trapani → funivia → Erice, Castello di Venere | La funivia ferma a metà (scena), si sale a piedi nella nebbia. Dungeon nel castello con la nebbia (visibilità ridotta). Boss: **Avv. Vito Asaro**, «Gran Maestro» della loggia (inventata) dei parchi eolici. Tipo **Volante**, asso Staraptor L49. | **Dossier Mulinu**, `FLAG_DOSSIER_TP`, comizio a Trapani |
| M-TP-05 | Il pullman delle 5:40 | Trapani, autostazione | Scena: Palermo è chiusa dalla Zona rossa del Grande Comizio di Mistretta; il pullman regionale gira per l'entroterra fino a Sant'Agata di Militello (R-02). | inizio della parte messinese |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-TP-01 | Il cous cous elettorale (ST-03) | Turi, San Vito Lo Capo | Turi ha promesso «cous cous gratis per tutti» in un comizio: servirne 10 piatti in tempo (minigioco di consegna). | Consenso +1 |
| S-TP-02 | Le saline | Salinaro, Trapani | Riparare 3 mulini a vento (puzzle di orientamento delle pale col vento del giorno). Riprende ST-08. | Consenso +1, `Sali` (Modulo 3) |
| S-TP-03 | Le genovesi ericine | Pasticcera, Erice | Consegnare le genovesi calde a 3 NPC in cima e in fondo alla funivia. | `Genovesi` ×5 (Modulo 3) |
| S-TP-04 | Mozia | Archeologa, Marsala | Raggiungere Mozia a piedi sulla strada sommersa (con bassa marea, orario del DS) e trovare il Giovinetto (statua: gag del museo chiuso il lunedì). | Fossile |
| S-TP-05 | Il Satiro Danzante | Pescatore, Mazara | Il pescatore che lo trovò nella rete (storia vera, raccontata con rispetto) chiede di ritrovare la sua vecchia rete. | `ITEM_SUPER_ROD` se non ancora ottenuta, altrimenti MT |
| S-TP-06 | Lo Zingaro | Guardiaparco, Castellammare/Scopello | La riserva: sentiero costiero di 3 mappe, raccogliere rifiuti lasciati dai turisti. | Consenso +1 |
| S-TP-07 | La tonnara Florio | Ex tonnaroto, Favignana | Racconto della mattanza (sobrio), cave di tufo di Cala Rossa (D-TP-03). | MT |
| S-TP-08 | Cambiavoti di Trapani (ST-06) | Chantal (telefono), Alcamo | Come S-CT-10. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-TP-01 | Cave di Cusa | 2 mappe con colonne mai finite | `Spallata` | Roccia, Terra | B-TP-01 |
| D-TP-02 | Laguna dello Stagnone | mare basso, 3 mappe | `Aliscafu` | Acqua, Volante | B-TP-02 |
| D-TP-03 | Cave di tufo di Cala Rossa | 2 mappe | `Martiddata` | Roccia, Acqua | — |
| D-TP-04 | Castello di Venere | 3 mappe nella nebbia | — | — | Segreteria 6 |
| D-TP-05 | Grande Cretto | 1 mappa labirinto, nessun incontro | — | — | — |

### Boss secondari

B-TP-01 **Lo Scalpellino delle Cave** (Roccia, 46) · B-TP-02 **Il Prestanome** del parco eolico (Volante/Elettro, 47) · B-TP-03 **Il Massaro della Kasbah** (inventato, Buio, 46).

### Meme ed easter egg

E-TP-01 Il vento: ogni NPC all'aperto ha la frase che vola via a metà (testo troncato con «…» e poi «aspetta, rifaccio»). · E-TP-02 Cartello ST-09 a Trapani. · E-TP-03 La funivia di Erice «chiusa per vento» anche quando non c'è vento. · E-TP-04 Il cous cous di San Vito che diventa più grande a ogni visita.

---

## 8. Provincia di Messina (ME) — Atto IV · ore 53–60 · Dossier 7

**Area dialettale:** messinese non metafonetico (Giostra, Torre Faro/Ganzirri marinaro); San Fratello e Mistretta: gallo-italico nei Nebrodi (con variante sicilianizzata dichiarata); Eolie: eoliano.
**Tema:** lo Stretto, il Ponte eterno, la mafia dei pascoli, il lusso di Taormina.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-ME-01 | La mafia dei pascoli | Nebrodi: San Fratello, Sant'Agata, Mistretta | Un allevatore onesto di cavalli sanfratellani contro chi incassa i fondi europei su terreni demaniali mai pascolati (inventati). Dungeon-bosco D-ME-01. | Consenso +3, `FLAG_NEBRODI_PASTURE_MAFIA` |
| M-ME-02 | La costa tirrenica | Capo d'Orlando → Patti/Tindari → Barcellona → Milazzo | Tindari e i laghetti di Marinello; a Milazzo il castello, la raffineria e l'imbarco per le Eolie. | — |
| M-ME-03 | Pippo a Torre Faro | Messina, Torre Faro | Pippo davanti al pilone, col pidone e la birra. Si unisce al gruppo. | `FLAG_RECRUIT_PIPPO` |
| M-ME-04 | La Società Stretto Eterna | Messina, archivi (inventati) | Labirinto burocratico di 5 piani (D-ME-02) con faldoni dal 1971: i funzionari combattono per difendere i gettoni di presenza. | Consenso +3 |
| M-ME-05 | Il galà del Teatro Antico | Taormina | Galà del cinema al Teatro Antico: il giocatore smaschera in diretta il patto elettorale tra albergatori del lusso (inventati) e l'entourage di Mistretta. 4 lotte in abito da sera. ST-05 tappa a Taormina. | Consenso +3 |
| M-ME-06 | Segreteria 7: l'AD delle Partecipate | Messina, Palazzo (inventato) delle Partecipate, vicino al Duomo | Il campanile astronomico suona a mezzogiorno: le porte del dungeon si aprono a ritmo delle statue. Boss: **Dott. Natale Sturiale**, AD delle partecipate regionali. Tipo **Acciaio**, asso Magnezone L55. | **Dossier Pilunu**, `FLAG_DOSSIER_ME`, comizio in piazza Duomo |
| M-ME-07 | L'elicottero di Torre Faro | Torre Faro, hangar della Società Stretto Eterna | Un elicottero comprato nel 2006 «per i sopralluoghi del Ponte» e mai usato. Pippo lo rimette in moto. | `FLAG_ELICOTTERO_PRIVATO`: il Volo funziona anche con la cenere |
| M-ME-08 | Attraversare lo Stretto | Messina, traghetto | Scena: Villa San Giovanni, aeroporto di Reggio Calabria, volo per Punta Raisi (R-02). | inizio Atto V |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-ME-01 | La diretta col filtro (ST-03) | Turi, Taormina | Turi ha trasmesso in diretta il comizio con il filtro «orecchie da gatto». Convincere 5 influencer a non ricondividerlo. | Consenso +1 |
| S-ME-02 | La Sciara del Fuoco | Guida vulcanologica, Stromboli | Salita notturna (orologio del DS 20:00–4:00) al punto di osservazione (D-ME-03). | Pietra (Modulo 3) |
| S-ME-03 | Il dissalatore di Lipari | Calogero (telefono), Lipari | ST-08: il dissalatore fermo; riaccenderlo battendo il Custode delle Pompe. | Consenso +1 |
| S-ME-04 | Il cratere di Vulcano | Pescatore, Vulcano | Bagni di fango e fumarole: trovare 3 Pokémon nascosti nel vapore. | MT |
| S-ME-05 | La Madonna Nera | Sacrestano, Tindari | Visita al santuario e ai laghetti di Marinello (tono rispettoso), raccogliere conchiglie per il presepe. | `ITEM_SOOTHE_BELL` se non ottenuto, altrimenti bacche |
| S-ME-06 | Il Longano | Ex vivaista, Barcellona Pozzo di Gotto | Il torrente che divide la città: riattivare un vecchio ponte (puzzle `Spallata`). | Consenso +1 |
| S-ME-07 | Isola Bella | Bagnante, Taormina | Raggiungere Isola Bella sulla lingua di sabbia e battere il proprietario (inventato) del lido «più esclusivo d'Europa». | Consenso +1 |
| S-ME-08 | Cariddi | Pescatore di pescespada, Ganzirri | Con la MN Mulinello attraversare i gorghi dello Stretto (D-ME-04). | Pokémon Acqua (Modulo 3) |
| S-ME-09 | Cambiavoti di Messina (ST-06) | Chantal (telefono), Giostra | Come S-CT-10. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-ME-01 | Bosco dei Nebrodi | 3 mappe di faggeta e pascoli | `Roncigghiu` | Erba, Normale (cavalli), Coleottero | B-ME-01 |
| D-ME-02 | Archivi della Società Stretto Eterna | 5 piani di faldoni (pareti di carta che si spostano a tempo) | — | nessuno; 10 allenatori «Funzionari» | B-ME-02 |
| D-ME-03 | Sciara del Fuoco (Stromboli) | 2 mappe notturne | `Aliscafu` | Fuoco, Roccia | — |
| D-ME-04 | Gorghi di Cariddi | 2 mappe di mare | `Aliscafu`, Mulinello | Acqua, Drago | — (post-game: leggendario P-08) |

### Boss secondari

B-ME-01 **Il Pascolatore di Carta** (Normale/Terra, 52) · B-ME-02 **Il Dirigente dei Gettoni** (Acciaio/Psico, 53) · B-ME-03 **L'Albergatore del Galà** (Normale/Volante, 53) · B-ME-04 **Il Custode delle Pompe** di Lipari (Acqua/Elettro, 50).

### Meme ed easter egg

E-ME-01 Il cartello ST-09 a Torre Faro, aggiornato a ogni atto. · E-ME-02 Il «buddace»: un NPC catanese a Messina usa l'insulto e un messinese risponde (scambio scritto nel Modulo 6, nessuna volgarità). · E-ME-03 La statua che esce dal campanile astronomico a mezzogiorno: se il giocatore è in piazza, un evento unico al giorno. · E-ME-04 La focaccia messinese che Pippo offre a ogni Ritrovo.

---

## 9. Provincia di Palermo (PA) — Atto V · ore 60–67 · Dossier 8

**Area dialettale:** palermitano urbano (Ballarò/Albergheria, Vucciria, Kalsa, Borgo Vecchio, ZEN), borgate marinare (Mondello, Isola delle Femmine); Piana degli Albanesi arbëreshë (cartelli bilingui; dialoghi arbëreshë solo come saluti, il resto in italiano/siciliano con dichiarazione nel Modulo 6). Mai `mbare`/`carusu`.
**Tono:** il cuore del potere e della memoria. Rallentamento voluto all'ingresso.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-PA-01 | Cento passi | Cinisi (arrivo a Punta Raisi) | Casa Memoria Peppino Impastato: visita sobria, nessuna lotta, una sola musica lenta. Maria e Totò accompagnano il protagonista. | — |
| M-PA-02 | Le steli di Capaci | A29, Capaci e Isola delle Femmine | Il protagonista percorre a piedi il tratto con le steli e il Giardino della Memoria Quarto Savona Quindici. Nessuna lotta, nessun selvatico, nessun NPC che parla tranne Maria e Totò. Sonoro: vento e auto. Il protagonista ripensa al concorso fallito e giura. | `FLAG_CAPACI_MEMORIAL_SILENCE` |
| M-PA-03 | Palermo a due velocità | Politeama/Libertà, Massimo/Maqueda/Quattro Canti, Ballarò, Vucciria, Kalsa, Borgo Vecchio, ZEN 2, Mondello | Con Totò: i salotti di via Libertà contro il caos vitale dei mercati e l'abbandono dello ZEN. Cancello del Consenso ≥ 40 per entrare in centro (il cordone della Zona rossa si apre). | Consenso +3 |
| M-PA-04 | Le carte di Ficuzza | Corleone, Ficuzza | Il collettore dei voti della Conca d'Oro ha le sue carte (registri dei pacchetti di voti, inventati) in una masseria a Ficuzza. Dungeon-bosco D-PA-02. Il CIDMA di Corleone è un luogo di memoria visitabile, sobrio. | `Atto` di ST-02, Consenso +3 |
| M-PA-05 | Segreteria 8: il Collettore della Conca d'Oro | Palermo, Palazzo delle Aquile | Dungeon fra sale di consiglio e corridoi con «portatori di voti». Boss: **On. Totò Scaduto** (omonimo del compagno: gag «chiamatemi Onorevole, il Totò buono è lui»). Tipo **Buio**, asso Drapion L61. | **Dossier Geniu**, `FLAG_DOSSIER_PA`, comizio al Politeama |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-PA-01 | Il manifesto abusivo (ST-03) | Turi, Palermo, via Maqueda | Turi ha attaccato manifesti sopra quelli degli altri candidati: staccarli prima della multa (6 punti). | Consenso +1 |
| S-PA-02 | Pani ca' meusa | Ambulante, Vucciria | Il panino della Vucciria come cura (strumento) e minigioco «schietto o maritato». | `PaniCaMeusa` ×5 (Modulo 3) |
| S-PA-03 | Il Cristo Pantocratore | Sacrestano, Monreale | Rimettere in ordine le tessere di un mosaico (puzzle a griglia 3×3). | MT |
| S-PA-04 | Villa dei Mostri | Custode, Bagheria, Villa Palagonia | Riconoscere 8 statue dei mostri dalle descrizioni (D-PA-03); il sacco edilizio degli anni '60–'70 in sottofondo. | `Sfinciuni` (Modulo 3) |
| S-PA-05 | La FIAT che non c'è | Ex operaio, Termini Imerese | Dungeon industriale spettrale D-PA-04; l'operaio racconta le promesse di riconversione. | Consenso +1 |
| S-PA-06 | La Rocca di Cefalù | Turista, Cefalù | Salita al Tempio di Diana e al castello (sentiero) e lotta col Guardiano della Rocca. | Consenso +1 |
| S-PA-07 | Lingue di Piana | Papàs, Piana degli Albanesi | Cartelli bilingui: trovare 5 parole arbëreshë sui cartelli e dirle a 5 NPC (dizionario nel Modulo 3). Portella della Ginestra come memoria sobria. Cannolo gigante. | `Cannolu` ×5 |
| S-PA-08 | La Diga Jato | Contadino, Partinico | Le campagne a secco con la diga accanto: aprire le chiuse col consenso del consorzio (3 lotte). Riprende ST-08. | Consenso +1 |
| S-PA-09 | Il Festino (evento a calendario) | Devota, Cattedrale | 14–15 luglio: il carro di Santa Rosalia, minigioco di traino. | Strumento raro |
| S-PA-10 | Cambiavoti di Palermo (ST-06) | Chantal (di persona), ZEN 2 | Come S-CT-10; Chantal regala la `UrnaElettor.` se i Cambiavoti sconfitti sono 9. | Consenso +1 |

### Dungeon

| Codice | Nome | Struttura | MN | Selvatici | Boss |
|---|---|---|---|---|---|
| D-PA-01 | Monte Pellegrino e Grotta dell'Addaura | 3 mappe | `Martiddata`, `Spallata` | Roccia, Spettro | post-game P-06 |
| D-PA-02 | Bosco di Ficuzza e Cascata delle Due Rocche | 3 mappe | `Roncigghiu`, Cascata | Erba, Acqua, Buio | B-PA-02 |
| D-PA-03 | Villa Palagonia | 2 mappe | — | Spettro | — |
| D-PA-04 | Ex stabilimento di Termini Imerese | 4 mappe: catena di montaggio, verniciatura, uffici, piazzale | `Spallata` | Acciaio, Elettro, Spettro | B-PA-03 |
| D-PA-05 | Palazzo delle Aquile | 3 piani | — | — | Segreteria 8 |
| D-PA-06 | Via della Lega (Palazzo dei Normanni, corridoi dell'ARS) | 5 piani (2 saltabili con i faldoni di Totò) | `Spallata`, Cascata | Psico, Buio, Spettro (62–68) | — |

### Boss secondari

B-PA-01 **Il Parcheggiatore Capo** di Mondello (Normale/Buio, 58) · B-PA-02 **Il Massaro di Ficuzza** (Erba/Buio, 59) · B-PA-03 **Il Liquidatore** dello stabilimento (Acciaio, 59) · B-PA-04 **U Cassiere**, capo del racket che ha rovinato il fratello di Orazio (ST-04; Buio/Veleno, 60).

### Meme ed easter egg

E-PA-01 «Arancina»: a Palermo gli NPC correggono «arancinu» (simmetrico a E-CT-02); chi ha risposto in modo «coerente» in entrambe le città riceve un oggetto. · E-PA-02 Il coccodrillo della Vucciria (leggenda): un NPC giura di averlo visto; con `Caimanu` (Totodile) in squadra, battuta speciale. · E-PA-03 Cartello ST-09 al porto. · E-PA-04 Il traffico di via Roma: un NPC aspetta l'autobus dal primo atto. · E-PA-05 Il Genio di Palermo: parlandoci, risponde con un indovinello diverso per ogni giorno della settimana.

---

## 10. Provincia di Enna (EN), Lega e finale — Atto V · ore 67–72 · Dossier 9

**Area dialettale:** centrale (ennese); **gallo-italico** a Piazza Armerina, Aidone, Nicosia, Sperlinga (Mistretta senza maschera parla un gallo-italico ennese sicilianizzato: il Modulo 6 dichiara il registro, R-08 della skill).
**Tema:** l'ombelico della Sicilia, nebbia, la resa dei conti.

### Missioni principali

| Codice | Titolo | Dove | Svolgimento | Esito |
|---|---|---|---|---|
| M-EN-01 | La A19 a pezzi | A19 Termini → Enna | Deviazioni sulle trazzere (dungeon esterno D-EN-01), code per l'outlet di Agira la domenica (gag: la strada è più lenta se l'orologio del DS segna domenica). | — |
| M-EN-02 | Il lago che non c'è | Pergusa | Lago prosciugato e autodromo abbandonato: sfida a giri di pista (allenatori in sequenza a tempo). ST-08 ultima tappa. | Consenso +3 |
| M-EN-03 | Segreteria 9: la Commissione Elettorale | Enna Alta, Castello di Lombardia → Rocca di Cerere | Nebbia perenne; il boss è il **Presidente della Commissione Elettorale Regionale, Dott. Filippo La Rosa** (inventato), autore del cavillo di Fontanarossa (chiude il cerchio). Tipo **Psico**, asso Slowking L66. | **Dossier Cerere**, `FLAG_DOSSIER_EN`, ultimo visto elettorale |
| M-EN-04 | La notte dello spoglio: la Lega | Palermo, Palazzo dei Normanni, Sala d'Ercole | Cancello Consenso ≥ 49. Via della Lega (D-PA-06), poi i **4 Campioni**: (1) **Don Tanino**, il Gattopardo della Prima Repubblica — Roccia/Terra, asso L70; (2) **L'Assessora Tecnica venuta dal Nord** — Acciaio/Elettro, asso L72; (3) **Il Re delle Liste Civiche** — Veleno/Spettro, cambia casacca con Staffetta, asso L74; (4) **Il Cardinale delle Opere Pubbliche e dei Rifiuti** — Buio/Fuoco, asso L76. | `FLAG_LEGA_DEFEATED` |
| M-EN-05 | Sotto il temporale | Piazza Armerina | La Sala d'Ercole è vuota: Mistretta è a Piazza Armerina. Temporale (meteo pioggia). I quattro quartieri del Palio dei Normanni, il Duomo; gli 8 compagni bloccano le guardie del corpo (ognuno con una lotta doppia accanto al giocatore). | — |
| M-EN-06 | La Sala della Grande Caccia | Villa Romana del Casale | Mistretta parla con dolcezza paterna (battuta delle specifiche, Modulo 6). Squadra: Persian (`Gattupardu`) L82, Slaking (`Poltrona`) L84, Spiritomb (`Inciuciu`) L84, Tyranitar (`Cupula`) L86, Metagross (`Miliardariu`) L86, Dragonite (`Trinacria`) L88. | `FLAG_PRESIDENT_MISTRETTA_DEFEATED` |
| M-EN-07 | Il palco | Catania, Piazza Duomo (comizio finale) | Folla di sprite che saltano, bandiere della Trinacria, coriandoli; Turi piange abbracciando Orazio; Christian fa le storie; Maria guarda da lontano senza applaudire. Il protagonista è il nuovo Presidente. | — |
| M-EN-08 | Dissolvenza | schermo nero | La fanfara si spegne; pianoforte solo, poi violino in Do minore. Le cinque frasi delle specifiche, una alla volta. Titoli di coda (`atrisorb`) sul nero. | `FLAG_POST_RESIGNATION`, `VAR_TRINACRIA_ATTO` = 6, salvataggio |

### Missioni secondarie

| Codice | Titolo | Committente e luogo | Obiettivo | Ricompensa |
|---|---|---|---|---|
| S-EN-01 | Le due cattedrali | Sacrestani rivali, Nicosia | Santa Maria Maggiore contro San Nicolò: fare da paciere tra i due quartieri (gallo-italico). | Consenso +1 |
| S-EN-02 | Sperlinga negavit | Custode, Sperlinga | Castello scavato nella roccia (D-EN-02); il motto del 1282 inciso sull'ingresso. | MT |
| S-EN-03 | L'outlet della domenica | Commessa, Agira | Parodia del consumismo domenicale: trovare un parcheggio (labirinto di auto). Cassatelle di Agira. | `Cassateddi` (Modulo 3) |
| S-EN-04 | La Granfonte | Contadino, Leonforte | I pescheti insacchettati a mano: aiutare a insacchettare (minigioco); la fontana a 24 cannoli. | Bacche |
| S-EN-05 | La Dea di Morgantina | Museo, Aidone | La statua tornata dall'estero: ritrovare la guida scomparsa nel parco archeologico. | Fossile |
| S-EN-06 | La stella di Centuripe | Anziano, Centuripe | Belvedere sull'Etna (cenere visibile all'orizzonte), consegna di una lettera a Catania (con Volo). | Consenso +1 |

### Dungeon

D-EN-01 **Trazzere dell'A19** (4 mappe esterne, `Spallata`, Normale/Terra) · D-EN-02 **Castello di Sperlinga** (2 piani nella roccia, `Scalaroccia` per la parte alta nel post-game) · D-EN-03 **Rocca di Cerere** (nebbia, 2 mappe) · D-EN-04 **Villa Romana del Casale** (3 sale a mosaico: ogni sala ha un mosaico che indica la strada).

### Meme ed easter egg

E-EN-01 Cartello ST-09 a Enna («la Sicilia ha un centro, il Ponte no»). · E-EN-02 La nebbia di Enna Alta che fa sparire gli NPC a metà frase. · E-EN-03 La pista di Pergusa: il record del giro è battuto da un nonno in Ape. · E-EN-04 Lo studente della Kore che fa la stessa tesi da 9 anni.

---

## 11. Atto VI — Il post-game della disillusione · ore 72–102

Si ricarica la partita: camera di Corso Italia, **sei mesi dopo le dimissioni**. `FLAG_POST_RESIGNATION` è acceso: il motore carica i banchi gemelli (Modulo 1 §7), riattiva tutti gli allenatori 1–699 con +25 livelli. La spazzatura (sprite dei sacchi) è ancora per strada. La cenere c'è ancora. Il Volo funziona ovunque.

### Proporzione delle reazioni (vincolante, provincia per provincia)

- **60% Capro espiatorio:** danno la colpa al protagonista (e alla Bocconi/LUISS) per munnizza, cenere a Fontanarossa, Comiso inutile, buche, siccità.
- **40% Estimatori:** studenti, commercianti onesti, vecchi pescatori; riconoscono il sacrificio.
- Il controllo è meccanico (registro degli NPC, Modulo 1 §7.8).

### Contenuti

| Codice | Contenuto | Dove | Dettagli |
|---|---|---|---|
| P-01 | Ritrovi con gli 8 compagni | luoghi di C-01…C-08 | Una sfida a settimana per compagno, nel giorno indicato (orologio del DS). Squadre L75→85 che crescono dopo ogni vittoria (3 versioni, ID allenatori 700–723). |
| P-02 | Maria sul tetto del tribunale | Catania, Palazzo di Giustizia (piazza Verga), tetto | Super-boss. Si sblocca con i 9 Atti di ST-02 e tutti i Ritrovi vinti almeno una volta. Squadra L95–100: Alakazam (`Bilancia`), Tropius (`Carruba`), Lucario (`Giustizia`) + 3 nel Modulo 6. Nessuna musica di vittoria dopo: solo un dialogo. |
| P-03 | Fantasma di Rocca Busambra | Ficuzza (Corleone), cima | Boss leggendario «della Prima Repubblica» (allenatore 730), con `Scalaroccia` e Cascata. |
| P-04 | Fantasma del Cratere Centrale | Etna, sommità (dopo D-CT-01 e `Scalaroccia`) | Allenatore 731 + leggendario Ho-Oh (nome Modulo 3) dopo la lotta. |
| P-05 | Fantasma del Castello Ursino | Catania, sotterranei (D-CT-07) | Allenatore 732. |
| P-06 | Fantasma di Pantelleria | Pantelleria (traghetto da Trapani, solo post-game): Lago Specchio di Venere, dammusi | Allenatore 733. Mappa nuova. |
| P-07 | I Tre Venti | in giro per l'isola | Raikou, Entei, Suicune vaganti come «Scirocco», «Tramontana», «Maestrale» (nomi nel Modulo 3). |
| P-08 | Lugia nei gorghi di Cariddi | D-ME-04, fondo | Si cattura dopo P-02. |
| P-09 | Fiera del Mediterraneo | Palermo | Le strutture lotta (Frontiera Lotta di HeartGold) come padiglioni della Fiera. |
| P-10 | Nunzio riapre l'officina | San Cristoforo | Chiusura di ST-04: missione di consegna dei pezzi da 4 province. |
| P-11 | Il libro di Turi | Acireale | Distribuire 9 copie del libro (nessuno lo vuole) — una battuta per provincia, 60/40. |
| P-12 | Pokédex nazionale | Prof. Strano | Completamento oltre il regionale. |

### Ore del post-game

Ritrovi (8 × 4 sfide) 8 h · Maria 2 h (più preparazione) · Fantasmi e leggendari 8 h · Fiera 6 h · missioni P-10/P-11 e ri-sfide degli allenatori 6 h. **Totale ≈ 30 h.**

---

## 12. Riepilogo numerico (per il controllo dei Moduli 2 e 6)

| Prov. | Principali | Secondarie | Dungeon | Boss secondari | Easter egg | Segreteria |
|---|---|---|---|---|---|---|
| CT | 10 | 10 | 7 | 6 | 6 | Normale, Chansey 18 |
| SR | 5 | 9 | 4 | 3 | 4 | Acqua, Lanturn 25 |
| RG | 4 | 8 | 3 | 3 | 4 | Erba, Victreebel 31 |
| CL | 4 | 8 | 4 | 3 | 4 | Roccia, Rhydon 37 |
| AG | 5 | 9 | 4 | 4 | 4 | Terra, Gastrodon 43 |
| TP | 5 | 8 | 5 | 3 | 4 | Volante, Staraptor 49 |
| ME | 8 | 9 | 4 | 4 | 4 | Acciaio, Magnezone 55 |
| PA | 5 | 10 | 6 | 4 | 5 | Buio, Drapion 61 |
| EN + finale | 8 | 6 | 4 | — | 4 | Psico, Slowking 66 |
| **Totale** | **54** | **77** | **41** | **30** | **39** | 9 |
| Post-game | 12 voci P | | | | | |

Flag necessari (R-08): 54 + 77 + 30 + 12 ≈ 173 di completamento, più quelli di visibilità degli NPC: rientrano nei 288 dell'intervallo 0x840–0x95F; il resto (visibilità di dettaglio) usa l'intervallo storico liberato (Modulo 1 §4.1).

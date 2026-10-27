"""Testi scritti a mano del blocco 5.3 (gen53.py li unisce alle tabelle calcolate)."""

VERSIONE = '1.0'
DATA = '27/10/2026'

INTESTAZIONE = """# Modulo 5 · Blocco 5.3 — Partiture degli Atti II–IV

**Versione:** {versione} · {data} · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** `F:\\Progetti\\pokeheartgold`

**File del blocco:**

| File | Cosa contiene |
|---|---|
| `docs/MODULO_5/5.3_ATTI_II-IV.md` | questo documento |
| `tools/music/5.3/SEQ_*.py` | le {n_file} partiture (formato R-AUD-12, notazione R-AUD-15) |
| `tools/generatori/5.3/` | generatore di questo documento (`gen53.py`, `text53.py`, copiati da `tools/generatori/5.2/`): rifà il collaudo e scrive le tabelle |

`tools/music/notazione.py` e `tools/music/collauda.py` sono quelli del blocco 5.2, senza modifiche.

Fonti: il blocco 5.1 (pipeline, regole R-AUD-01…14, banchi e limiti), il blocco 5.2 (notazione, collaudo, regole R-AUD-15…21), il registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json` (sezione `musiche`: slot e mappe), la trama `docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md` (§3–§8, Atti II–IV: le righe «Musica» delle province, le operazioni di «U Sistema» e M-TP-02 «Il silenzio del Cretto») e l’archivio originale `files/data/sound/gs_sound_data.sdat` di `pokeheartgold` (SHA-1 `{sha1}`)."""

IN_BREVE = """## 0. In breve

- **{n_file} slot, tutti quelli che il registro 2.5 assegna al blocco 5.3,** tutti musiche di campo: Siracusa (9, con la riserva di Vendicari sugli slot del Safari), Ragusa (4), Caltanissetta (4, col MUOS), Agrigento (3), Trapani (3, col vento del Cretto), Messina (5) e il viaggio in traghetto, aliscafo e pullman.
- **Collaudo superato:** `python -I tools/music/collauda.py --blocchi 5.3` compone le {n_file} partiture, le mette in una copia dell’archivio originale e la confronta con l’originale → `AUDIO_OK` (§2). Nessun limite del 5.1 è vicino: al massimo {poly_max} note insieme su 12, {psg_max} canali PSG su 4 (solo il MUOS), {rumore_max} di rumore su 1 (solo il Cretto), sequenza più lunga {byte_max} byte (sul lettore delle mappe al massimo {byte_max_field} su 15 500), archivio di {sdat_byte} byte.
- **Il brano che finisce.** `SEQ_GS_E_LINEAR`, lo slot del viaggio, in HeartGold non si ripete; il codice A10 del 5.1 vieta allora il ritornello. `{finito}` dura {finito_s} secondi e finisce su un accordo tenuto (R-AUD-22); il Modulo 6 ne tiene conto negli script dei viaggi (§6).
- **Il vento del Cretto.** La trama (M-TP-02) vuole nel Grande Cretto «nessuna musica allegra, solo il suono del vento»: `SEQ_TP_CRETTO_VENTO` è una sola voce sul canale di rumore (programma 53), con le raffiche scritte come note lunghe e l’espressione CC11 che sale e scende (R-AUD-23). Lo stesso metodo serve al 5.4 per Capaci.
- **Armonia riletta da uno strumento** (R-AUD-19): note estranee nelle melodie del blocco: {n_estranee}. Le melodie stanno sugli accordi in ogni movimento; le note di passaggio cadono solo fuori dai movimenti.
- **Banchi e volumi:** ogni brano tiene il banco del suo slot HeartGold (R-AUD-16); quattro slot che HeartGold suona sotto 60 salgono a 64 (R-AUD-24, §2.2). Gli strumenti sono i programmi comuni 0–59, uguali in tutti i banchi.
- **Non provato qui:** l’ascolto. I nomi degli strumenti (§3) sono ruoli dedotti, come nel 5.2; il blocco 5.3 aggiunge due programmi da ascoltare per primi nel 7.3: 49 (onda quadra che si spegne, MUOS) e 53 (rumore, Cretto)."""

NOTAZIONE = """## 1. Come si scrive una partitura

Come nel blocco 5.2 (§1 di `docs/MODULO_5/5.2_ATTO_I.md`): un file `tools/music/5.3/<SIMBOLO>.py` con `SIMBOLO`, `BANCO`, `VOLUME`, `SCHEDA` (titolo, carattere, tonalità, forma, e `perche_volume` quando il volume cambia) e `partitura(A)` scritta con `tools/music/notazione.py`. Il blocco 5.3 usa in più quattro possibilità che la notazione ha già:

| Scrittura | Dove | Significato |
|---|---|---|
| `b.fine_a(11)` al posto di `b.ritornello(…)` | `SEQ_TRN_TRAGHETTO` | il brano finisce alla battuta 11 (R-AUD-22) |
| `v.cc(11, valore, battuta)` | `SEQ_TP_CRETTO_VENTO` | espressione (CC11 → comando SSEQ `0xD5`, tabella del §5 del 5.1) a una battuta qualsiasi, anche frazionaria: le raffiche del vento (R-AUD-23) |
| `v.batteria([schema, schema, …], da, battute)` | `SEQ_ME_ARCHIVI_MAGNETICI` | una lista di schemi, uno per battuta, ripetuta: il campanello della macchina da scrivere a fine frase |
| `b.eco(v, nome, ritardo=0, programma=P, trasponi=±12)` | `SEQ_SR_BAROCCO_NOTO`, `SEQ_SR_MARZAMEMI`, `SEQ_ME_TAORMINA_GALA` | raddoppio della voce con un altro strumento, anche all’ottava |"""

COLLAUDO = """## 2. Collaudo

Esito del {data}, rifatto da `gen53.py` a ogni esecuzione con le funzioni di `collauda.py`:

```
python -I tools/music/collauda.py --blocchi 5.3 --repo F:/Progetti/pokeheartgold
```

`collauda.py` usa `componi.py` (C01–C04), poi `applica` su una copia dell’originale (A01–A12, A22) e `controlla` (A20, A21) del 5.1; scrive in `build/collaudo/` (fuori dal repository e fuori da git) i MIDI, il manifesto e, con `--sdat`, l’archivio da provare nell’emulatore. Risultato: **{n_file} brani, archivio di {sdat_byte} byte, controllo con l’originale superato, `AUDIO_OK`.** Anche `collauda.py --blocchi 5.2 5.3` (i due blocchi insieme, 69 slot) dà `AUDIO_OK`.

### 2.1 I numeri di ogni brano

«Rit.» = battute dell’introduzione + battute del ritornello e la sua durata («finisce a N» per il brano senza ritornello). «Byte» = sequenza SSEQ di Trinacria (fra parentesi quella di HeartGold nello stesso slot). «Insieme» = note che suonano insieme al massimo (limite 12, A06). «Carico» = sequenza + banco + onde (limite A09: 478 544 su `PLAYER_FIELD`, 497 352 su `PLAYER_BGM`)."""

DEVIAZIONI_INTRO = """### 2.2 Volumi diversi dallo slot HeartGold

R-AUD-05 e R-AUD-07 permettono qualsiasi banco musicale e qualsiasi volume; il blocco 5.3 tiene tutti i banchi e cambia solo questi volumi, con la regola R-AUD-24 (gli altri {n_uguali} slot tengono banco e volume di HeartGold):"""

TIMBRI_INTRO = """## 3. Gli strumenti usati

### 3.1 Programmi

Come nel 5.2 (§3.1), il nome di ogni programma è il **ruolo dedotto** dai dati del banco (inviluppo ADSR, zone, campione) e dall’uso che ne fa HeartGold (catalogo del 5.1, §9.2); i nomi delle voci nelle partiture («pompe», «gorghi», «bobine», «remi»…) dicono cosa fa la voce nel brano, il ruolo resta quello della tabella. Un programma che all’ascolto del 7.3 non suona come il suo ruolo si cambia con R-AUD-20. I programmi 49 e 53 sono nuovi rispetto al 5.2."""

TIMBRI = {
    2: ('continuo (tastiera)', '4 zone, sostegno 1, più brillante del programma 0'),
    3: ('accordi (tastiera)', 'sostegno 1; accompagnamento in 35 brani di HeartGold (Goldenrod: 226 note di accordi)'),
    5: ('vibrafono, campanelli', 'sostegno 1, timbro puro; melodia del Centro Pokémon di HeartGold'),
    7: ('chitarra', 'sostegno 40, si spegne a metà'),
    10: ('glockenspiel, campanelle', 'sostegno 1, in HeartGold sempre sopra il Re5'),
    12: ('organo dolce, bordone', 'sostegno pieno, timbro puro'),
    13: ('fisarmonica', 'sostegno quasi pieno, ricco di armoniche (ancia); in HeartGold la melodia di Cianwood'),
    14: ('chitarra (accordi)', 'sostegno 20; accordi ribattuti in HeartGold'),
    16: ('pizzicato leggero', 'decadimento 30, sostegno 1'),
    17: ('pizzicato d’archi', 'decadimento 30, sostegno 1; gli ostinati dei temi del Team Rocket di HeartGold'),
    18: ('marimba', 'sostegno 1, timbro morbido; l’ostinato del treno magnetico di HeartGold'),
    19: ('basso pizzicato', 'sostegno 1; traccia più grave nel 46% dei brani che lo usano'),
    20: ('basso morbido', 'sostegno 100, timbro quasi sinusoidale'),
    21: ('basso sintetico', 'una zona, sostegno pieno; i bassi del Team Rocket'),
    22: ('basso elettrico', 'sostegno 120; il basso delle lotte di HeartGold'),
    23: ('archi', 'il programma più usato di HeartGold (148 brani)'),
    24: ('archi lenti', 'attacco morbido (120), sostegno pieno'),
    25: ('contrabbasso, violoncello, tuba', 'sostegno pieno, registro grave (traccia più grave nel 41% dei brani)'),
    26: ('arpa', '5 zone, sostegno 40'),
    27: ('celesta', 'sostegno 1, timbro puro'),
    28: ('timpani', '66 brani di HeartGold, mai melodia né basso'),
    29: ('tromba', '89 brani di HeartGold, melodia e accompagnamento'),
    30: ('tromboni, sirena della nave', 'ottoni gravi; il basso delle vittorie di HeartGold'),
    32: ('corni, coro', '87 brani di HeartGold, registro centrale'),
    33: ('oboe, canto', 'ancia sostenuta, timbro medio'),
    34: ('clarinetto', 'ancia sostenuta che cresce dopo l’attacco'),
    35: ('flauto', 'il timbro di melodia di HeartGold (traccia più acuta nel 52% dei brani)'),
    36: ('fagotto', 'ancia grave (base Do3), traccia più grave nel 34% dei brani'),
    38: ('flauto dolce', 'timbro puro sostenuto'),
    39: ('batteria', 'disposizione General MIDI (§3.2)'),
    42: ('mandolino, pizzico', 'sostegno 1, attacco netto; in HeartGold lo strumento a pizzico del teatro Kimono e della Torre Campana'),
    48: ('onda quadra (PSG)', 'canale PSG: conta nel limite di 4 (R-AUD-06)'),
    49: ('onda quadra che si spegne (PSG)', 'canale PSG, inviluppo 127/50/0/125: attacco istantaneo e sostegno 0, cioè un «bip» che si spegne da solo; 3 brani di HeartGold'),
    53: ('rumore (vento)', 'canale di rumore, al massimo uno per brano (A07); inviluppo 110/127/60/120, attacco più lento del 54 e sostegno 60, quindi un soffio che resta; mai usato nelle musiche di HeartGold'),
}

BATTERIA_INTRO = """### 3.2 Tasti della batteria (programma 39)

Gli stessi nomi del 5.2 (`notazione.BATTERIA`); la batteria 39 copre i tasti F1–A5 (29–81) e un tasto fuori da lì non suona (A05). «Usi in HeartGold» = note suonate su quel tasto in tutte le musiche `SEQ_GS_*` (gemelli esclusi)."""

REGOLE = [
    ('R-AUD-22', 'Slot che non si ripete',
     'Uno slot che in HeartGold non si ripete (nel registro 2.5 solo `SEQ_GS_E_LINEAR` = `SEQ_TRN_TRAGHETTO`) '
     'riceve un brano che finisce: la partitura chiude con `b.fine_a(N)` e non mette `b.ritornello` (A10 lo '
     'rifiuterebbe). L’ultima battuta è un accordo tenuto, così la fine non sembra un taglio. Dopo la fine la '
     'mappa resta senza musica finché uno script non ne avvia un’altra.'),
    ('R-AUD-23', 'Il vento come rumore',
     'Il vento dei luoghi della memoria (`SEQ_TP_CRETTO_VENTO` nel 5.3, `SEQ_PA_CAPACI_MEMORIA` nel 5.4) è una '
     'voce sola sul programma di rumore 53, `pedale=True` (nessuna armonia da controllare), con note lunghe '
     'attaccate una all’altra (`_`, durata piena: mai due note di rumore insieme, A07) e l’espressione CC11 '
     'scritta a quarti di battuta per le raffiche. Nota più acuta = vento più sottile. Nessun altro strumento: '
     'la trama vuole solo il vento.'),
    ('R-AUD-24', 'Volume minimo',
     'Uno slot che HeartGold suona sotto 60 sale a 64 quando la partitura ha meno voci del brano HeartGold '
     '(è la scelta del 5.2 per San Cristoforo, scritta come regola): con poche voci a un volume così basso il '
     'brano resterebbe sotto le musiche delle mappe vicine. La `SCHEDA` lo dice in `perche_volume`; '
     '`gen53.py` rifiuta ogni altro cambio di volume senza banco diverso.'),
]

NOTE_BLOCCHI = """## 6. Note per gli altri blocchi

- **5.4 (partiture).** Copia questo blocco: `tools/music/5.4/SEQ_*.py`, generatore da `tools/generatori/5.3/` (gestisce già il brano senza ritornello). Il vento di Capaci (`SEQ_PA_CAPACI_MEMORIA`) segue R-AUD-23 come il Cretto; il volume segue R-AUD-24. Il controllo finale di tutto il Modulo 5 resta `collauda.py --blocchi 5.2 5.3 5.4`.
- **Modulo 4 (mappe).** Le mappe di `SEQ_TP_CRETTO_VENTO` (Grande Cretto, Gibellina, Presidio Civico, Porta d’Europa) hanno già il vento nella musica: non serve la piastra sonora del vento forte `SEQ_SE_GS_KYOUHUU` (5.1, §10.6), che lo farebbe sentire due volte.
- **Modulo 6 (script).** I viaggi in traghetto, aliscafo e pullman (`MAP_AG_TRAGHETTO_LAMPEDUSA`, `MAP_TP_ALISCAFO_FAVIGNANA`, `MAP_TP_PULLMAN_5_40`, `MAP_ME_ALISCAFO_EOLIE`, `MAP_ME_TRAGHETTO_STRETTO`) hanno una musica di {finito_s} secondi che finisce (R-AUD-22): la scena del viaggio dura al massimo quanto lei, oppure lo script la riavvia con `PlayBGM SEQ_TRN_TRAGHETTO` quando la scena è più lunga.
- **Lettore `PLAYER_BGM`.** Quattro slot del blocco sono musiche di mappa nel registro ma in HeartGold suonano sul lettore degli eventi: `SEQ_CL_MUOS_ONDE`, `SEQ_TRN_TRAGHETTO`, `SEQ_ME_TAORMINA_GALA`, `SEQ_ME_ARCHIVI_MAGNETICI`. Restano su quel lettore (R-AUD-06) e il loro carico sta nel suo limite (§2.1); che partano dall’intestazione della mappa come le altre non è provato qui e lo controlla il 7.3.
- **Modulo 7 (blocco 7.3).** TASK in più: `python -I tools/music/collauda.py --blocchi 5.2 5.3 --sdat` → `AUDIO_OK`, poi nell’emulatore l’ascolto dei programmi nuovi 49 (`SEQ_CL_MUOS_ONDE`) e 53 (`SEQ_TP_CRETTO_VENTO`: il rumore deve sembrare vento, e le raffiche devono sentirsi), della fine di `SEQ_TRN_TRAGHETTO`, dei quattro slot `PLAYER_BGM` in una loro mappa e dei tre slot che in HeartGold hanno un solo file (`SEQ_GS_C_NIBI` = `SEQ_RG_BAROCCO_IBLEO`, `SEQ_GS_C_TOKIWA` = `SEQ_RG_MERCATO_ALBA`, `SEQ_GS_C_YAMABUKI` = `SEQ_CL_ENTROTERRA_NISSENO`): dopo `applica` sono tre brani diversi, e ognuno deve suonare il suo nella sua mappa."""

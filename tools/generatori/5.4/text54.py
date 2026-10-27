"""Testi scritti a mano del blocco 5.4 (gen54.py li unisce alle tabelle calcolate)."""

VERSIONE = '1.0'
DATA = '27/10/2026'

# Slot dei titoli di coda (R-AUD-25): il brano finisce e dura quanto quello di HeartGold, ± TOLLERANZA_TITOLI s
SLOT_TITOLI = 'SEQ_GS_ENDING'
TOLLERANZA_TITOLI = 3.0
# Slot del finale aggiunti dal registro 2.5 v1.2 (R-AUD-26)
EVENTI = ('SEQ_TRN_PALCO', 'SEQ_TRN_DIMISSIONI', 'SEQ_TRN_FINE')

INTESTAZIONE = """# Modulo 5 · Blocco 5.4 — Partiture dell’Atto V, del finale, dei titoli di coda e del post-game

**Versione:** {versione} · {data} · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** `F:\\Progetti\\pokeheartgold`

**File del blocco:**

| File | Cosa contiene |
|---|---|
| `docs/MODULO_5/5.4_ATTO_V_FINALE.md` | questo documento |
| `tools/music/5.4/SEQ_*.py` | le {n_file} partiture (formato R-AUD-12, notazione R-AUD-15) |
| `tools/generatori/5.4/` | generatore di questo documento (`gen54.py`, `text54.py`, copiati da `tools/generatori/5.3/`): rifà il collaudo del blocco e di tutto il Modulo 5 e scrive le tabelle |
| `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json` | **v1.2**: tre slot nuovi per il finale (R-AUD-26) |
| `docs/MODULO_5/5.1_PIPELINE_E_SFX.md`, `docs/MODULO_5/5.1_BANCHI_SBNK.json` | **v1.1**: rigenerati da `tools/generatori/5.1/gen51.py` col registro nuovo (95 slot invece di 92) |

`tools/music/notazione.py`, `tools/music/collauda.py` e `tools/trinacria_audio.py` sono quelli dei blocchi 5.1–5.3, senza modifiche.

Fonti: il blocco 5.1 (pipeline, regole R-AUD-01…14, banchi e limiti), il blocco 5.2 (notazione, collaudo, regole R-AUD-15…21), il blocco 5.3 (regole R-AUD-22…24), il registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json` (sezione `musiche`: slot, mappe e usi), la trama `docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md` (Atto V M-PA-01…05 e M-EN-01…08, post-game P-02…P-09), `src/credits/credits.c` e `src/register_hall_of_fame.c` di `pokeheartgold` (chi avvia le musiche del finale) e l’archivio originale `files/data/sound/gs_sound_data.sdat` (SHA-1 `{sha1}`)."""

IN_BREVE = """## 0. In breve

- **{n_file} slot, tutti quelli che il registro 2.5 assegna al blocco 5.4:** {n_campo} musiche di campo (provincia di Palermo, Enna, le strade d’oriente e d’occidente, la Fiera del Mediterraneo e i santuari dei Fantasmi), 10 di lotta e vittoria (Mistretta e Maria, i Tre Venti, la Fenice dell’Etna, Colapisci, i leggendari antichi, i capi della Fiera, la vittoria alla Fiera e il vento dopo Maria) e {n_eventi} del finale: il palco, le dimissioni coi titoli di coda e il carillon della schermata «Fine».
- **Tre slot nuovi nel registro (2.5 v1.2, R-AUD-26).** La scaletta chiedeva al 5.4 il palco, il pianoforte e violino in Do minore e i titoli di coda, ma il registro non aveva uno slot per loro. Ora `SEQ_TRN_PALCO` = `SEQ_GS_E_DENDOUIRI`, `SEQ_TRN_DIMISSIONI` = `SEQ_GS_ENDING`, `SEQ_TRN_FINE` = `SEQ_GS_ENDING2`: gli slot che HeartGold suona nell’Albo d’Oro, nei titoli di coda e nella schermata «Fine». Il blocco 5.1 è rigenerato (v1.1) e conta 95 slot.
- **Collaudo superato:** `python -I tools/music/collauda.py --blocchi 5.4` → `AUDIO_OK` (§2). Al massimo {poly_max} note insieme su 12, {psg_max} canale PSG su 4 (solo Tramontana), {rumore_max} di rumore su 1 (Capaci e il tetto di Maria), sequenza più lunga {byte_max} byte (sul lettore delle mappe al massimo {byte_max_field} su 15 500), archivio di {sdat_byte} byte.
- **Il Modulo 5 è completo.** `python -I tools/music/collauda.py --blocchi 5.2 5.3 5.4` mette tutte le {n_modulo} partiture in una copia dell’originale → `AUDIO_OK`: archivio di {sdat_modulo} byte, {byte_modulo} byte di sequenze contro i {byte_modulo_hg} di HeartGold negli stessi slot, al massimo {poly_modulo} note insieme. Ogni slot musicale del registro ha il suo brano.
- **I titoli di coda durano quanto quelli di HeartGold.** I crediti di HeartGold scorrono per un numero fisso di fotogrammi (`CREDITS_FRAMES` = 4976 in `src/credits/credits.c`) e il loro brano dura {sec_hg} secondi senza ripetersi. `SEQ_TRN_DIMISSIONI` dura {sec_trn} secondi (48 battute a 66), finisce su un accordo tenuto e `gen54.py` rifiuta uno scarto oltre 3 secondi (R-AUD-25). Pianoforte solo per le prime 12 battute (43,6 secondi), poi il violino, come chiede M-EN-08.
- **Il vento.** Capaci (M-PA-02: «solo vento e auto sull’asfalto») e il tetto del tribunale dopo Maria (P-02: «nessuna fanfara») seguono R-AUD-23 come il Cretto: una voce sola sul canale di rumore; a Capaci le auto sono note di rumore più acute e brevi fra una raffica e l’altra.
- **La firma di «U Sistema»** (R-AUD-21): l’accordo napoletano chiude le frasi di Palazzo dei Normanni (i Campioni dell’ARS), della marcia di Piazza Armerina, della lotta col Presidente e dei santuari dei Fantasmi. Il palco e le dimissioni stanno sulla stessa tonica, Do, in maggiore e in minore.
- **Armonia riletta da uno strumento** (R-AUD-19): note estranee nelle melodie del blocco: {n_estranee}, anche nel valzer in 3/4, dove ogni semiminima è un movimento.
- **Non provato qui:** l’ascolto. Il 5.4 aggiunge da ascoltare nel 7.3 il pianoforte (programma 0), il programma 24 come violino solo, la durata delle dimissioni contro i titoli che scorrono, le auto di Capaci e il palco sul lettore delle mappe (§6)."""

NOTAZIONE = """## 1. Come si scrive una partitura

Come nei blocchi 5.2 e 5.3 (§1 di `docs/MODULO_5/5.2_ATTO_I.md`): un file `tools/music/5.4/<SIMBOLO>.py` con `SIMBOLO`, `BANCO`, `VOLUME`, `SCHEDA` (titolo, carattere, tonalità, forma, e `perche_volume` quando il volume cambia) e `partitura(A)` scritta con `tools/music/notazione.py`. Il blocco 5.4 usa in più queste possibilità, che la notazione ha già:

| Scrittura | Dove | Significato |
|---|---|---|
| `Brano(A, bpm=168, metro=(3, 4))` e schemi di 3 passi (`'.xx'`, `'1 . .'`) | `SEQ_PA_PALERMO_LIBERTA` | valzer: «um» del contrabbasso sul primo movimento, «pa-pa» del pianoforte sul secondo e sul terzo |
| `b.fine_a(48)` e l’ultima battuta `c3+g3+c4+eb4/1_` | `SEQ_TRN_DIMISSIONI` | il brano finisce dopo 48 battute su un accordo tenuto per tutta la battuta (R-AUD-22, R-AUD-25) |
| due voci sullo stesso programma 0 | `SEQ_TRN_DIMISSIONI` | mano destra (melodia, controllata da R-AUD-19) e mano sinistra (arpeggi sul `Giro`) del pianoforte |
| note di rumore di altezza diversa e `v.cc(11, …)` a un quarto di battuta | `SEQ_PA_CAPACI_MEMORIA` | il vento grave e lungo, l’auto acuta e breve che sale di colpo e si spegne in un movimento (R-AUD-23) |
| `b.eco(v, nome, ritardo=0, programma=48, trasponi=-12)` | `SEQ_TRN_LOTTA_TRAMONTANA` | raddoppio della melodia sull’onda quadra PSG (conta nel limite di 4 PSG) |"""

COLLAUDO = """## 2. Collaudo

Esito del {data}, rifatto da `gen54.py` a ogni esecuzione con le funzioni di `collauda.py`:

```
python -I tools/music/collauda.py --blocchi 5.4 --repo F:/Progetti/pokeheartgold
python -I tools/music/collauda.py --blocchi 5.2 5.3 5.4 --repo F:/Progetti/pokeheartgold
```

`collauda.py` usa `componi.py` (C01–C04), poi `applica` su una copia dell’originale (A01–A12, A22) e `controlla` (A20, A21) del 5.1; scrive in `build/collaudo/` (fuori dal repository e fuori da git) i MIDI, il manifesto e, con `--sdat`, l’archivio da provare nell’emulatore. Risultato del blocco: **{n_file} brani, archivio di {sdat_byte} byte, controllo con l’originale superato, `AUDIO_OK`.** Risultato del Modulo 5 (i tre blocchi insieme): **{n_modulo} brani, archivio di {sdat_modulo} byte, `AUDIO_OK`.**

### 2.1 I numeri di ogni brano

«Rit.» = battute dell’introduzione + battute del ritornello e la sua durata («finisce a N» per il brano senza ritornello). «Byte» = sequenza SSEQ di Trinacria (fra parentesi quella di HeartGold nello stesso slot). «Insieme» = note che suonano insieme al massimo (limite 12, A06). «Carico» = sequenza + banco + onde (limite A09: 478 544 su `PLAYER_FIELD`, 497 352 su `PLAYER_BGM`)."""

DEVIAZIONI_INTRO = """### 2.2 Volumi diversi dallo slot HeartGold

R-AUD-05 e R-AUD-07 permettono qualsiasi banco musicale e qualsiasi volume; il blocco 5.4 tiene tutti i banchi e cambia solo questo volume, con la regola R-AUD-24 (gli altri {n_uguali} slot tengono banco e volume di HeartGold):"""

TIMBRI_INTRO = """## 3. Gli strumenti usati

### 3.1 Programmi

Come nel 5.2 (§3.1), il nome di ogni programma è il **ruolo dedotto** dai dati del banco (inviluppo ADSR, zone, campione) e dall’uso che ne fa HeartGold (catalogo del 5.1, §9.2); i nomi delle voci nelle partiture («abbanniata», «coriandoli», «gorghi», «lava»…) dicono cosa fa la voce nel brano, il ruolo resta quello della tabella. Un programma che all’ascolto del 7.3 non suona come il suo ruolo si cambia con R-AUD-20. Il programma 0 (pianoforte) è nuovo rispetto ai blocchi 5.2 e 5.3; il 24 fa anche il violino solo delle dimissioni."""

TIMBRI = {
    0: ('pianoforte', '5 zone di tasti, inviluppo 127/75/1/110: attacco istantaneo e suono che si spegne piano, '
        'come una corda percossa; 52 brani di HeartGold, anche i titoli di coda'),
    3: ('accordi (tastiera)', 'sostegno 1; accompagnamento in 35 brani di HeartGold (Goldenrod: 226 note di accordi)'),
    5: ('vibrafono, campanelli', 'sostegno 1, timbro puro; melodia del Centro Pokémon di HeartGold'),
    7: ('chitarra', 'sostegno 40, si spegne a metà'),
    10: ('glockenspiel, carillon', 'sostegno 1, in HeartGold sempre sopra il Re5; l’unico strumento della scatola musicale '
         '`SEQ_GS_ENDING2`'),
    12: ('organo dolce, bordone', 'sostegno pieno, timbro puro'),
    13: ('fisarmonica', 'sostegno quasi pieno, ricco di armoniche (ancia); in HeartGold la melodia di Cianwood'),
    14: ('chitarra (accordi)', 'sostegno 20; accordi ribattuti in HeartGold'),
    17: ('pizzicato d’archi', 'decadimento 30, sostegno 1; gli ostinati dei temi del Team Rocket di HeartGold'),
    18: ('marimba', 'sostegno 1, timbro morbido; l’ostinato del treno magnetico di HeartGold'),
    19: ('basso pizzicato', 'sostegno 1; traccia più grave nel 46% dei brani che lo usano'),
    21: ('basso sintetico', 'una zona, sostegno pieno; i bassi del Team Rocket'),
    22: ('basso elettrico', 'sostegno 120; il basso delle lotte di HeartGold'),
    23: ('archi', 'il programma più usato di HeartGold (148 brani)'),
    24: ('archi lenti, violino solo', 'attacco morbido (120), sostegno pieno; una voce sola nel registro del violino '
         '(Sol3–Re7) è il violino delle dimissioni'),
    25: ('contrabbasso, violoncello, tuba', 'sostegno pieno, registro grave (traccia più grave nel 41% dei brani)'),
    26: ('arpa', '5 zone, sostegno 40'),
    27: ('celesta', 'sostegno 1, timbro puro'),
    28: ('timpani, tuono', '66 brani di HeartGold, mai melodia né basso'),
    29: ('tromba', '89 brani di HeartGold, melodia e accompagnamento'),
    30: ('tromboni', 'ottoni gravi; il basso delle vittorie di HeartGold'),
    32: ('corni, coro', '87 brani di HeartGold, registro centrale'),
    33: ('oboe, canto', 'ancia sostenuta, timbro medio'),
    35: ('flauto', 'il timbro di melodia di HeartGold (traccia più acuta nel 52% dei brani)'),
    39: ('batteria', 'disposizione General MIDI (§3.2)'),
    42: ('mandolino, pizzico', 'sostegno 1, attacco netto; in HeartGold lo strumento a pizzico del teatro Kimono e della '
         'Torre Campana'),
    48: ('onda quadra (PSG)', 'canale PSG: conta nel limite di 4 (R-AUD-06)'),
    53: ('rumore (vento, auto)', 'canale di rumore, al massimo uno per brano (A07); inviluppo 110/127/60/120, un soffio '
         'che resta (blocco 5.3, R-AUD-23)'),
}

BATTERIA_INTRO = """### 3.2 Tasti della batteria (programma 39)

Gli stessi nomi dei blocchi 5.2 e 5.3 (`notazione.BATTERIA`); la batteria 39 copre i tasti F1–A5 (29–81) e un tasto fuori da lì non suona (A05). «Usi in HeartGold» = note suonate su quel tasto in tutte le musiche `SEQ_GS_*` (gemelli esclusi)."""

REGOLE = [
    ('R-AUD-25', 'I titoli di coda',
     'La schermata dei crediti avvia da sola lo slot `SEQ_GS_ENDING` (`src/credits/credits.c`, '
     '`Sound_SetSceneAndPlayBGM(0xe, 0x3f8)`) e scorre per un numero fisso di fotogrammi (`CREDITS_FRAMES` = 4976), '
     'senza aspettare la musica. Il brano di quello slot (`SEQ_TRN_DIMISSIONI`) non si ripete (R-AUD-22) e dura '
     'quanto il brano di HeartGold, con al massimo 3 secondi di scarto: `gen54.py` lo calcola dalla mappa dei tempi '
     'e rifiuta il documento se lo scarto è maggiore. Così la musica non finisce prima dei titoli e non resta tagliata '
     'quando arriva la schermata «Fine», che poi avvia `SEQ_TRN_FINE`. Il Modulo 6 riscrive i testi dei crediti '
     'senza cambiare né il loro numero né i tempi (Modulo 1, §9.4).'),
    ('R-AUD-26', 'Slot nuovi nel registro',
     'Una musica che la trama chiede e il registro 2.5 non ha si aggiunge **prima** al registro (sezione `musiche` e '
     '`file_trinacria_seq_h`, con una riga di correzione e la versione nuova), scegliendo lo slot HeartGold che il '
     'gioco suona già nello stesso momento; poi si rigenera il blocco 5.1 (`gen51.py`) e si scrive la partitura. '
     '`componi.py` rifiuta una partitura il cui simbolo non è nel registro (C03). Il 5.4 l’ha fatto per tre slot: '
     '`SEQ_TRN_PALCO` (`SEQ_GS_E_DENDOUIRI`, Albo d’Oro), `SEQ_TRN_DIMISSIONI` (`SEQ_GS_ENDING`, titoli di coda), '
     '`SEQ_TRN_FINE` (`SEQ_GS_ENDING2`, schermata «Fine»).'),
]

NOTE_BLOCCHI = """## 6. Note per gli altri blocchi

- **Modulo 5 completo.** Tutti i 95 slot musicali del registro 2.5 v1.2 hanno una partitura (5.2: 40, 5.3: 29, 5.4: {n_file}); il controllo finale è `python -I tools/music/collauda.py --blocchi 5.2 5.3 5.4` → `AUDIO_OK`. Le musiche di HeartGold fuori dal registro (titolo, bicicletta, Surf, Pokéathlon, radio…) restano quelle originali (blocco 5.1, §11).
- **Modulo 4 (mappe).** Come per il Cretto, le mappe di `SEQ_PA_CAPACI_MEMORIA` (Cinisi, Casa Memoria, Capaci e Isola delle Femmine, Portella della Ginestra, CIDMA di Corleone) hanno già il vento nella musica: niente piastra sonora del vento forte `SEQ_SE_GS_KYOUHUU` (5.1, §10.6).
- **Modulo 6 (script).**
  - *Palco (M-EN-07).* Lo script del comizio avvia `PlayBGM SEQ_TRN_PALCO`. Per M-EN-08 la fanfara «si spegne di colpo»: lo script ferma la musica senza dissolvenza prima di passare allo schermo nero (il comando lo sceglie il Modulo 6 fra quelli di `asm/macros/script.inc`). Se il Modulo 6 tiene la registrazione nell’Albo d’Oro dopo Mistretta, quella schermata suona anche lei `SEQ_TRN_PALCO`, perché `src/register_hall_of_fame.c` avvia lo stesso slot.
  - *Dimissioni (M-EN-08).* La musica la avvia la schermata dei crediti, non lo script. Il pianoforte suona da solo per 43,6 secondi: se le cinque frasi bianche sul nero stanno all’inizio dei crediti (fra i testi di `msg_0440`), il pianoforte le accompagna e il violino entra coi titoli; se il Modulo 6 le mostra in una scena prima dei crediti, quella scena resta in silenzio (la fanfara è appena stata tagliata) e il pianoforte parte coi crediti. In tutti e due i casi i tempi dei crediti non cambiano (R-AUD-25).
  - *Maria sul tetto (P-02).* La lotta usa `SEQ_TRN_LOTTA_PRESIDENTE` come Mistretta (registro 2.5); dopo la vittoria la modifica E3 del registro fa suonare `SEQ_TRN_VITTORIA_MARIA_VENTO`, che è solo vento e si ripete finché lo script non avvia un’altra musica.
- **Modulo 7 (blocco 7.3).** TASK in più: `python -I tools/music/collauda.py --blocchi 5.2 5.3 5.4 --sdat` → `AUDIO_OK` (tutto il Modulo 5), poi nell’emulatore: il pianoforte (programma 0) e il violino (24) di `SEQ_TRN_DIMISSIONI`, che deve finire quando i titoli sfumano verso la schermata «Fine» (circa {sec_trn} secondi: una musica che finisce molto prima o viene tagliata si corregge col tempo `bpm` della partitura, R-AUD-25); il carillon `SEQ_TRN_FINE` dopo 380 fotogrammi sulla schermata «Fine»; `SEQ_TRN_PALCO` sul lettore delle mappe (`SEQ_GS_E_DENDOUIRI` è un evento ma suona su `PLAYER_FIELD`); le auto di `SEQ_PA_CAPACI_MEMORIA` (devono sembrare auto che passano, non raffiche) e il vento di `SEQ_TRN_VITTORIA_MARIA_VENTO` dopo la lotta con Maria."""

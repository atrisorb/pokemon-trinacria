"""Testi scritti a mano del blocco 5.2 (gen52.py li unisce alle tabelle calcolate)."""

VERSIONE = '1.0'
DATA = '27/10/2026'

INTESTAZIONE = """# Modulo 5 · Blocco 5.2 — Partiture del Prologo e dell’Atto I

**Versione:** {versione} · {data} · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** `F:\\Progetti\\pokeheartgold`

**File del blocco:**

| File | Cosa contiene |
|---|---|
| `docs/MODULO_5/5.2_ATTO_I.md` | questo documento |
| `tools/music/5.2/SEQ_*.py` | le {n_file} partiture (formato R-AUD-12): {n_distinti} brani scritti e {n_stesso} file che suonano lo stesso brano di un altro slot (R-AUD-17) |
| `tools/music/notazione.py` | la notazione comune delle partiture 5.2–5.4 (§1): note in testo con controllo delle stanghette, giri di accordi, bassi, arpeggi, batteria, eco e ritornello |
| `tools/music/collauda.py` | collaudo di un blocco senza toccare il repository: compone, applica a una copia dell’originale, controlla, stampa i numeri di ogni brano (§2) |
| `tools/generatori/5.2/` | generatore di questo documento (`gen52.py`, `text52.py`): rifà il collaudo e scrive le tabelle |

Fonti: il blocco 5.1 (pipeline, regole R-AUD-01…14, banchi e limiti), il registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json` (sezione `musiche`: slot, mappe e usi), la trama `docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md` (§2, Atto I: «Musiche guida», missioni M-CT-00…09, S-CT-01…10, dungeon D-CT-01…07) e l’archivio originale `files/data/sound/gs_sound_data.sdat` di `pokeheartgold` (SHA-1 `{sha1}`)."""

IN_BREVE = """## 0. In breve

- **{n_file} slot, tutti quelli che il registro 2.5 assegna al blocco 5.2:** {n_campo} musiche di campo (la provincia di Catania, il Prologo al Cubbar e i luoghi comuni a tutta l’isola: Centri Pokémon, Segreterie, chiese, monumenti, grotte) e {n_lotta} brani di lotta, incontro e vittoria (i tre temi di «U Sistema» al posto del Team Rocket, le lotte con allenatori, selvatici e Segretari, le tre vittorie, gli otto temi d’incontro). I {n_stesso} slot «_EST» (la regione Kanto del motore, cioè la Sicilia orientale) suonano lo stesso brano della loro coppia, come chiede il registro.
- **Collaudo superato:** `python -I tools/music/collauda.py --blocchi 5.2` compone le {n_file} partiture, le mette in una copia dell’archivio originale e la confronta con l’originale → `AUDIO_OK` (§2). Nessun limite del 5.1 è vicino: al massimo {poly_max} note insieme su 12, {psg_max} canale PSG su 4 (solo il Cubbar), sequenza più lunga {byte_max} byte (sul lettore delle mappe al massimo {byte_max_field} su 15 500), archivio di {sdat_byte} byte.
- **Notazione comune.** Le partiture non scrivono eventi MIDI a mano: usano `tools/music/notazione.py`, che legge le note in testo (`d5/4. e5/8 f#5/4`), controlla che ogni stanghetta cada a inizio battuta, dispone gli accordi di un giro con la condotta delle parti, scrive bassi, arpeggi e batteria da schemi di una battuta e mette i marcatori del ritornello (§1). I blocchi 5.3 e 5.4 la usano uguale (R-AUD-15).
- **Armonia riletta da uno strumento.** Le melodie si scrivono sopra un giro di accordi; `Brano.note_estranee()` elenca le note che cadono su un movimento e non stanno nell’accordo. In tutto il blocco sono {n_estranee}, tutte note di passaggio, appoggiature, scale e cromatismi delle introduzioni scritti apposta (§4, voce «Estranee» di ogni brano).
- **Banchi e volumi:** ogni brano tiene il banco del suo slot HeartGold e quasi sempre il suo volume (R-AUD-16); le eccezioni sono elencate nel §2.2. Gli strumenti sono i programmi comuni 0–59 (uguali in tutti i banchi) più la campana 67 di `BANK_BGM_DUNGEON3`.
- **Non provato qui:** l’ascolto. I nomi degli strumenti (§3) sono ruoli dedotti dai dati dei banchi e dall’uso che ne fa HeartGold, non nomi scritti nei dati; la prova d’ascolto nell’emulatore resta un TASK del blocco 7.3 (§6)."""

NOTAZIONE = """## 1. Come si scrive una partitura

Ogni partitura è un file `tools/music/5.2/<SIMBOLO>.py` col formato del 5.1 (R-AUD-12: `SIMBOLO`, `BANCO`, `VOLUME`, `partitura(A)` che restituisce un `MidiWriter`), più la `SCHEDA` che questo documento riporta (titolo, carattere, tonalità, forma). Dentro, la musica si scrive con `tools/music/notazione.py`:

```python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro

GIRO = Giro('Dmaj7 | Bm7 | Em7 | A7')                    # una battuta per |, accordi in parti uguali

def partitura(A):
    b = Brano(A, bpm=108)                                # metro=(4, 4) di default; (6, 8), (3, 4)...
    fl = b.voce('flauto', 35, volume=112, pan=64)        # nome, programma, volume (CC7), pan (CC10)
    fl.suona('| f#5/4. e5/8 d5/4 e5/8 f#5 | d5/2 b4/4 c#5/8 d5 |', da=0, vel=100)
    pf = b.voce('pianoforte', 0, volume=92, pan=40)
    pf.arpeggi(GIRO, '1 5 8 10 12 10 8 5', da=0, registro=(48, 80))
    b.voce('basso', 19).basso(GIRO, '1 - - 1 5 - - .', da=0)
    b.voce('batteria', 39).batteria({{'cassa': 'x....x..', 'bordo': '..x...x.'}}, da=0, battute=4)
    b.eco(fl, 'flauto eco', ritardo=12, volume=40)       # copia ritardata (o raddoppio: ritardo=0, programma=…)
    b.ritornello(0, 4)                                   # battute [0, 4): marcatori loopStart / loopEnd
    return b.fine()
```

| Elemento | Scrittura | Significato |
|---|---|---|
| nota | `c d e f g a b`, poi `#` o `b`, poi l’ottava | `c4` = 60 (do centrale), `f#5` = 78, `bb3` = 58 |
| pausa | `r` | |
| accordo scritto | `c4+e4+g4/2` | note insieme |
| durata | `/1 /2 /4 /8 /16 /32`, `.` puntata, `t` terzina, `*N` | senza durata vale quella del simbolo prima; `r/1*4` = 4 semibrevi |
| segni | `~` legatura, `>` accento (+20), `'` staccato (metà), `_` tenuto (durata piena) | senza segni la nota dura il 90% del suo valore |
| stanghetta | `\\|` o `\\|\\|` | il cursore dev’essere a inizio battuta: un errore di durate si ferma qui (`NotaErrata`) |
| velocità | `v90` | per le note seguenti |
| sigla | `Am`, `F#m7`, `Bb/D`, `E7b9`, `Dmaj7`, `Bbm6`, `F#m7b5`, `A7sus4`… | qualità ammesse: {qualita} |
| gradi (arpeggi, basso) | `1 3 5 7 8 9 10 12 15`, `5,` = un’ottava sotto, `.` pausa, `-` tiene | nel basso `1` è la nota dopo la `/` |
| batteria | `{{'cassa': 'X...x...'}}` | `X` forte, `x` normale, `o` leggero, `.` niente; nomi dei tasti nel §3.2 |

Gli schemi (`accordi`, `arpeggi`, `basso`, `batteria`) sono una battuta di passi uguali: la lunghezza della stringa dà la griglia (8 caratteri in 4/4 = crome, 6 in 6/8 = crome). `Voce.copia(da, battute, a)` ripete battute già scritte; `Brano.ripeti(da, battute, a, trasponi=…)` ripete tutte le voci in un’altra tonalità (la batteria resta com’è), per la seconda passata di un ritornello. `b.voce(…, pedale=True)` segna un bordone, cioè note tenute apposta sotto accordi diversi, che il controllo dell’armonia (R-AUD-19) salta. `Brano.fine()` taglia tutto ciò che supera la fine del ritornello (lo SSEQ salta lì), scrive programma, volume e pan a tempo 0 e lascia a `mw.trinacria` i dati della notazione (tempo, metro, ritornello, voci) che il collaudo e questo documento leggono."""

COLLAUDO = """## 2. Collaudo

Esito del {data}, rifatto da `gen52.py` a ogni esecuzione con le funzioni di `collauda.py`:

```
python -I tools/music/collauda.py --blocchi 5.2 --repo F:/Progetti/pokeheartgold
```

`collauda.py` usa `componi.py` (C01–C04), poi `applica` su una copia dell’originale (A01–A12, A22) e `controlla` (A20, A21) del 5.1; scrive in `build/collaudo/` (fuori dal repository e fuori da git) i MIDI, il manifesto e, con `--sdat`, l’archivio da provare nell’emulatore. Risultato: **{n_file} brani, archivio di {sdat_byte} byte, controllo con l’originale superato, `AUDIO_OK`.**

### 2.1 I numeri di ogni brano

«Rit.» = battute dell’introduzione + battute del ritornello e la sua durata. «Byte» = sequenza SSEQ di Trinacria (fra parentesi quella di HeartGold nello stesso slot). «Insieme» = note che suonano insieme al massimo (limite 12, A06). «Carico» = sequenza + banco + onde (limite A09: 478 544 su `PLAYER_FIELD`, 497 352 su `PLAYER_BGM`)."""

DEVIAZIONI_INTRO = """### 2.2 Banchi e volumi diversi dallo slot HeartGold

R-AUD-05 e R-AUD-07 permettono qualsiasi banco musicale e qualsiasi volume; il blocco 5.2 cambia solo questi (gli altri {n_uguali} slot tengono banco e volume di HeartGold):"""

TIMBRI_INTRO = """## 3. Gli strumenti usati

### 3.1 Programmi

I banchi SBNK non hanno nomi: il nome di ogni programma è il **ruolo dedotto** dai suoi dati (inviluppo ADSR, numero di zone, campione con o senza ripetizione) e dall’uso che ne fa HeartGold (catalogo del 5.1, §9.2). È il nome che le partiture danno alla voce. Se la prova d’ascolto del 7.3 trova un programma che non suona come il ruolo, si cambia solo il numero del programma nella partitura (le note restano) e si rifà il collaudo (R-AUD-20)."""

TIMBRI = {
    0: ('pianoforte', '5 zone, attacco secco, sostegno 1 (suono che si spegne): tastiera percussiva; 52 brani di HeartGold'),
    2: ('continuo (tastiera)', '4 zone, sostegno 1, più brillante del programma 0'),
    3: ('accordi (tastiera)', 'sostegno 1; accompagnamento in 35 brani di HeartGold (Goldenrod: 226 note di accordi)'),
    5: ('vibrafono, campanelli', 'sostegno 1, timbro puro; melodia del Centro Pokémon di HeartGold'),
    7: ('chitarra', 'sostegno 40, si spegne a metà'),
    9: ('riff sintetico', 'sostegno 10, il campione più brillante della tavolozza'),
    10: ('glockenspiel, campanelle', 'sostegno 1, in HeartGold sempre sopra il Re5'),
    11: ('organo', 'sostegno pieno (127)'),
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
    25: ('contrabbasso, violoncello', 'sostegno pieno, registro grave (traccia più grave nel 41% dei brani)'),
    26: ('arpa', '5 zone, sostegno 40'),
    27: ('celesta', 'sostegno 1, timbro puro'),
    28: ('timpani', '66 brani di HeartGold, mai melodia né basso'),
    29: ('tromba', '89 brani di HeartGold, melodia e accompagnamento'),
    30: ('tromboni', 'ottoni gravi; il basso delle vittorie di HeartGold'),
    32: ('corni', '87 brani di HeartGold, registro centrale'),
    33: ('oboe, ciaramella, canto', 'ancia sostenuta, timbro medio'),
    34: ('clarinetto', 'ancia sostenuta che cresce dopo l’attacco'),
    35: ('flauto', 'il timbro di melodia di HeartGold (traccia più acuta nel 52% dei brani)'),
    36: ('fagotto', 'ancia grave (base Do3), traccia più grave nel 34% dei brani'),
    37: ('ottavino, fischietto, sirena', 'registro acuto, melodia nel 35% dei brani che lo usano'),
    38: ('flauto dolce', 'timbro puro sostenuto'),
    39: ('batteria', 'disposizione General MIDI (§3.2)'),
    42: ('mandolino, pizzico', 'sostegno 1, attacco netto; in HeartGold lo strumento a pizzico del teatro Kimono e della Torre Campana'),
    48: ('onda quadra (PSG)', 'canale PSG: conta nel limite di 4 (R-AUD-06)'),
    67: ('campana (solo `BANK_BGM_DUNGEON3`)', 'campione senza ripetizione suonato a Do4, come nella Torre Campana di HeartGold'),
}

BATTERIA_INTRO = """### 3.2 Tasti della batteria (programma 39)

`notazione.BATTERIA` dà un nome ai tasti usati; la batteria 39 copre i tasti F1–A5 (29–81) e un tasto fuori da lì non suona (A05). «Usi in HeartGold» = note suonate su quel tasto in tutte le musiche `SEQ_GS_*` (gemelli esclusi): i tasti più usati confermano la disposizione General MIDI."""

REGOLE = [
    ('R-AUD-15', 'Notazione comune',
     'Le partiture dei blocchi 5.2–5.4 si scrivono con `tools/music/notazione.py` (§1): note in testo con le stanghette, '
     'accordi, bassi, arpeggi e batteria da un `Giro`, `eco` per echi e raddoppi, `ritornello` per i marcatori. Niente '
     'numeri casuali: la stessa partitura dà sempre lo stesso MIDI. Un errore di notazione ferma `componi.py` (C01).'),
    ('R-AUD-16', 'Banco e volume dichiarati',
     'Ogni partitura scrive `BANCO` e `VOLUME`. Il blocco 5.2 tiene il banco dello slot HeartGold (così il carico resta '
     'quello che HeartGold già regge) e il suo volume, salvo le eccezioni del §2.2, scritte con la loro ragione.'),
    ('R-AUD-17', 'Stesso brano su due slot',
     'Quando il registro chiede lo stesso brano su due slot (le coppie «_EST» della regione Kanto del motore), il file '
     'della coppia carica la partitura dell’altro con `runpy` e ne prende `partitura`, `BANCO` e `VOLUME`: le due '
     'sequenze sono identiche byte per byte e suonano uguali (stesso banco, stesso volume). `applica` dà comunque a '
     'ogni slot il suo file (R-AUD-03).'),
    ('R-AUD-18', 'Collaudo del blocco',
     'Prima di consegnare un blocco di partiture: `python -I tools/music/collauda.py --blocchi <blocco>` → `AUDIO_OK`. '
     'I numeri del documento del blocco (byte, note insieme, carico, ritornello) vengono da lì, rifatti dal generatore.'),
    ('R-AUD-19', 'Melodia e armonia',
     'Ogni melodia si scrive sopra il giro di accordi delle altre voci. Le note che cadono su un movimento (in 6/8 su '
     'un movimento puntato), durano almeno una croma e non stanno nell’accordo (`Brano.note_estranee()`) si rileggono '
     'una per una: restano solo se sono note di passaggio, appoggiature o scale volute, e il documento del blocco ne '
     'dà il numero per brano.'),
    ('R-AUD-20', 'Timbri da confermare all’ascolto',
     'I nomi dei programmi del §3 sono ruoli dedotti. Se all’ascolto (blocco 7.3) un programma non suona come il suo '
     'ruolo, si sostituisce il numero del programma nella partitura con un altro programma comune dello stesso '
     'ruolo (tabella del §3.1 o catalogo del 5.1) senza toccare le note, e si rifà il collaudo.'),
    ('R-AUD-21', 'La firma di «U Sistema»',
     'I tre temi di «U Sistema» (incontro, lotta, covo) chiudono le frasi con l’accordo napoletano (Re bemolle in Do '
     'minore, Sol bemolle in Fa minore) e usano ottoni, pizzicato d’archi e basso sintetico. I blocchi 5.3–5.4, '
     'quando scrivono musiche del cartello (Fantasmi, Mistretta), riprendono questa firma.'),
]

NOTE_BLOCCHI = """## 6. Note per gli altri blocchi

- **5.3 e 5.4 (partiture).** Copiano il formato di questo blocco: `tools/music/<blocco>/SEQ_*.py` con `notazione.py`, `SCHEDA` per il documento, collaudo con `collauda.py --blocchi <blocco>` (R-AUD-18); il generatore del documento parte da `tools/generatori/5.2/` (si copia la cartella, come per i blocchi del Modulo 3). Il controllo finale di tutto il Modulo 5 è `collauda.py --blocchi 5.2 5.3 5.4`.
- **Partitura di prova del 5.1.** `tools/music/prova/SEQ_CT_CORSO_ITALIA.py` resta solo per `prova_5_1.py`: `componi.py` senza `--partiture` legge solo le cartelle 5.2–5.4, quindi lo slot `SEQ_GS_T_WAKABA` riceve la partitura vera di `tools/music/5.2/`.
- **Modulo 6 (script).** `SEQ_TRN_SISTEMA_COVO` non è la musica fissa di nessuna mappa: gli eventi nei covi e negli uffici di «U Sistema» lo avviano con `PlayBGM` e tornano alla musica della mappa alla fine. La musica del Prologo (`SEQ_CT_CUBBAR_TECHNO`) è quella delle mappe del Cubbar e del Privè Zagara; il flashback di M-CT-00 non ne chiede un’altra.
- **Modulo 7 (blocco 7.3).** TASK in più rispetto al 5.1: `python -I tools/music/collauda.py --blocchi 5.2 --sdat` → `AUDIO_OK`, poi l’archivio `build/collaudo/gs_sound_data.sdat` nell’emulatore per la prova d’ascolto dei ruoli del §3.1, cominciando dai programmi che non hanno un uso chiaro in HeartGold: 2 (continuo, `SEQ_CT_ACIREALE`), 9 (riff, `SEQ_CT_CUBBAR_TECHNO`), 13 (fisarmonica, `SEQ_CT_PESCHERIA`), 33 (ciaramella, `SEQ_CT_PAESI_ETNEI`), 42 (mandolino, `SEQ_TRN_CENTRO_POKEMON`), 48 (onda quadra PSG, `SEQ_CT_CUBBAR_TECHNO`) e 67 (campana, `SEQ_TRN_CHIESA`). Un programma sbagliato si corregge con R-AUD-20."""

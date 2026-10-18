# MODULO 1 — `INFRASTRUCTURE_AND_ENGINE_SPEC.md`

**Progetto:** Pokémon Trinacria · autore e copyright: **atrisorb**
**Base codice:** `F:\Progetti\pokeheartgold` (clone pret, commit `c28680fe0`) · **Cartella documenti:** `F:\Progetti\pokémon-sicilia`
**Versione del modulo:** 1.4 · 18/10/2026 (v1.4: §10 musiche allineate al registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json`; allineata al registro delle mappe `docs/MODULO_2/2.1_MAPS_CT_SR_RG.json` v1.1 e alla decisione R-10 di `docs/00_TRAMA_ESPANSA_E_SIDEQUEST.md` v1.2 su centralità dei Pokémon e «U Sistema»: §4.3, §4.4, §4.7, §7.1, §7.2, §8.1, §8.2, §10; v1.3: §4.1, §4.2 e §7.8 allineati al registro di flag, variabili e NPC `docs/MODULO_2/2.4_FLAGS_VARS.json`)
**Lettore:** LLM esecutore (Gemini Flash o equivalente). Questo documento non chiede di prendere decisioni: ogni valore è già deciso.

Tutti i fatti tecnici di questo modulo (percorsi, nomi di funzioni, righe di codice, ID liberi) sono stati **letti nel repository** il 15/10/2026. Il codice C dei passi M1-08…M1-14 è scritto sulle firme reali delle funzioni, ma **non è ancora stato compilato**: la compilazione è il criterio di successo di ogni passo.

---

## 0. Regole di esecuzione (valgono per ogni passo)

1. Esegui i passi **in ordine** (M1-01, M1-02, …). Un passo = un ticket. Non saltare passi, non unirli.
2. Ogni passo ha: **File**, **Azione**, **Blocco** (da copiare carattere per carattere), **Verifica** (comando), **Criterio** (PASS/FAIL).
3. «Trova e sostituisci»: il testo da trovare deve comparire **esattamente una volta** nel file. Se compare zero volte o più di una volta: **STOP**, scrivi `FAIL: testo non trovato` e non adattare nulla.
4. Non modificare righe che il passo non nomina. Non riformattare. Non tradurre. Non «migliorare».
5. Rientro del codice C: **4 spazi**, come il resto del repository. Fine riga: LF (`\n`).
6. Codifica dei file: UTF-8 senza BOM, **tranne** `heartgold.us/banner.bsf` (UTF-16 LE con BOM, passo M1-16).
7. Dopo ogni passo che tocca `src/`, `include/`, `asm/`, `files/`: lancia la build (§2.3). L'ultima riga deve essere `BUILD_OK`.
8. Commit: un commit per passo, sul ramo `trinacria`, messaggio `[M1-NN] <titolo del passo>`.
9. Il testo in siciliano **non lo scrivi tu**: lo copi dai moduli 3 e 6. Se un testo siciliano non è fornito, il passo è FAIL.

---

## 1. Correzioni vincolanti alle specifiche iniziali

Le specifiche di partenza (`pokeheartgold/docs/trinacria_spec/`) contengono alcune ipotesi che nel repository reale sono diverse. Valgono le righe di destra.

| Ipotesi nelle specifiche | Realtà nel repository (vincolante) |
|---|---|
| Testi in file `.gmm` / `.msg` | Testi in **`files/msgdata/msg/msg_NNNN.json`** (829 banchi, da `msg_0000` a `msg_0828`; alcuni hanno un suffisso, es. `msg_0542_T20.json`). Si compilano con `tools/msgenc` usando `tools/msgenc/charmap.txt`. |
| Nomi dei Pokémon in `msg_0237.gmm` | `files/msgdata/msg/msg_0237.json` (496 voci; voce 1 = `BULBASAUR`). |
| Mosse in `msg_0750.gmm` | `files/msgdata/msg/msg_0750.json` (468 voci; voce 1 = `Pound`). |
| Strumenti in `msg_0222.gmm` | `files/msgdata/msg/msg_0222.json` (537 voci; voce 1 = `Master Ball`). |
| Audio in `files/sound/gs_sound_data.sdat` | **`files/data/sound/gs_sound_data.sdat`**. |
| Tabella mappe `files/fielddata/maptable/maptable.bin` | Non esiste. Le intestazioni delle mappe sono in **`src/data/map_headers.h`** (array `sMapHeaders`, campi `msgBank`, `scriptsBank`, `weather`, …). In `files/fielddata/maptable/` c'è solo `mapname.bin`. Le costanti `MAP_*` sono in `include/constants/maps.h` (540 mappe). |
| Eventi in `files/fielddata/eventdata/zone_event/` | Confermato: 492 file JSON (`000_DUMMY.json`, `001_UNION.json`, …). |
| Script in `files/fielddata/script/scr_seq/` | Confermato: file `scr_seq_NNNN_<CODICE>.s` (macro in `asm/macros/script.inc`) + `event_<CODICE>.h`. |
| Build con `make` | La build è **meson + ninja**, lanciata da `make` in **WSL** (Ubuntu, utente `atrisorb`), con il compilatore Metrowerks in `tools/mwccarm/` (§2). |
| Il font va esteso per gli accenti | **Falso.** Il font principale contiene già `à è é ì ò ù â ê î ô û À È É Ì Ò Ù Â Ê Î Ô Û ’ ç ë ï ü ñ` (verificato glifo per glifo nei membri 0, 1, 2, 4, 10 del font). L'estensione (§5) aggiunge solo i caratteri **mancanti**: `« » € – — [ ] < > \| ^ \` £ § © ±`. |
| `\n`, `\r`, `\f` | Confermati (`charmap.txt`: `E000=\n`, `25BC=\r`, `25BD=\f`). Nel JSON compaiono come escape JSON `\n` `\r` `\f` (un solo carattere dopo il parsing). |
| `{STRVAR_1 3, 0, 0}` = nome del giocatore | Confermato, **ma** il nome compare solo se lo script ha eseguito prima `BufferPlayersName 0` (macro `BufferPlayersName slot`, comando 190). Regola R-TXT-07 (§6). |

---

## 2. Ambiente, repository e build

### 2.1 Percorsi fissi

| Cosa | Percorso |
|---|---|
| Repository di lavoro (unico posto dove si modifica il gioco) | `F:\Progetti\pokeheartgold` — in WSL `/mnt/f/Progetti/pokeheartgold` |
| Documenti e strumenti sorgente di Trinacria | `F:\Progetti\pokémon-sicilia` (`docs/`, `tools/`) |
| Strumenti Trinacria dentro il repository (copiati al passo M1-03) | `F:\Progetti\pokeheartgold\tools\trinacria\` |
| Compilatore Metrowerks già presente sulla macchina | `F:\Progetti\pokémon-trinacria\tools\mwccarm\` (si copia al passo M1-02) |
| ROM costruita | `F:\Progetti\pokeheartgold\build\pokeheartgold.us.nds` |
| SHA-1 della ROM originale (build non modificata) | `4fcded0e2713dc03929845de631d0932ea2b5a37` (file `heartgold.us/rom.sha1`) |
| Server del dizionario siciliano | `F:\Progetti\sicilian-dialect-mcp\dist\server.js` (Node) |
| Emulatore di prova già configurato | melonDS 1.1 in WSL, comandato da `F:\Progetti\pokémon-trinacria\scripts\sicilia\emu.sh` (istruzioni in `F:\Progetti\pokémon-trinacria\tasks\AMBIENTE.md` §6) |
| Strumenti grafici già provati | `nitrogfx` (compilato dalla build in `build/tools/nitrogfx/nitrogfx`), `F:\Progetti\pokémon-trinacria\scripts\sicilia\mappe\narc.py`, `F:\Progetti\pokémon-trinacria\scripts\guess_ncgr_flags.py` |

> Esiste un secondo progetto, `F:\Progetti\pokémon-trinacria`, con una trama diversa (protagonista di Biancavilla, 16 medaglie, Orazio come boss). **Non si modifica e non si copia la sua trama.** Da lì si riusano solo gli strumenti elencati sopra.

### 2.2 Passo M1-01 — Ramo di lavoro

- **File:** nessuno.
- **Azione (Git Bash):**
  ```bash
  cd /f/Progetti/pokeheartgold
  git status --short
  git switch -c trinacria
  ```
- **Criterio:** `git status --short` mostra solo `?? docs/` (le specifiche) e `git branch --show-current` stampa `trinacria`. Altrimenti FAIL.

### 2.3 Passo M1-02 — Compilatore e build di riferimento

- **Azione (Git Bash):**
  ```bash
  cp -r "/f/Progetti/pokémon-trinacria/tools/mwccarm" /f/Progetti/pokeheartgold/tools/mwccarm
  mkdir -p /f/Progetti/pokeheartgold/tools/trinacria
  cp "/f/Progetti/pokémon-sicilia/tools/build_trinacria.ps1" /f/Progetti/pokeheartgold/tools/trinacria/
  grep -qx 'tools/mwccarm/' /f/Progetti/pokeheartgold/.git/info/exclude || echo 'tools/mwccarm/' >> /f/Progetti/pokeheartgold/.git/info/exclude
  for d in meson-1.12.0 NitroSDK-4.2.30001 NitroSystem-071126.1 NitroWiFi-2.1.30003 libvct-1.3.1 yyjson-0.12.0; do
    [ -d "/f/Progetti/pokeheartgold/subprojects/$d" ] || cp -r "/f/Progetti/pokemon-trinacria-build/subprojects/$d" /f/Progetti/pokeheartgold/subprojects/
  done
  ```
  (Le sei cartelle hanno le stesse revisioni dei file `.wrap` di `pokeheartgold` — verificato il 15/10/2026 — e la stessa versione di meson del `Makefile`, 1.12.0. **`NitroDWC` invece ha una revisione diversa**: meson la scarica da GitHub alla prima build, quindi la prima build richiede la connessione a internet. Le cartelle copiate sono già ignorate da git.)
- **Build (PowerShell, timeout 600000 ms o in background):**
  ```powershell
  & "F:\Progetti\pokeheartgold\tools\trinacria\build_trinacria.ps1"
  ```
- **Criterio:** ultima riga `BUILD_OK` **e** la riga `ROM:` inizia con `4fcded0e2713dc03929845de631d0932ea2b5a37`. La prima build può durare 25–40 minuti.
- **Se FAIL:** apri il log indicato dalla riga `full log:`; se manca `arm-none-eabi-gcc` o `meson` in WSL, è un blocco per l'utente (non installare nulla).

### 2.4 Passo M1-03 — Strumenti Trinacria nel repository

- **Azione (Git Bash):**
  ```bash
  cd /f/Progetti/pokeheartgold
  cp "/f/Progetti/pokémon-sicilia/tools/font_extend.py" tools/trinacria/
  cp "/f/Progetti/pokémon-sicilia/tools/trinacria_msg_lint.py" tools/trinacria/
  cp "/f/Progetti/pokémon-sicilia/tools/dialect_query.mjs" tools/trinacria/
  cp "/f/Progetti/pokémon-sicilia/tools/trinacria_tables.py" tools/trinacria/
  mkdir -p data/trinacria include/trinacria
  python -I tools/trinacria/trinacria_msg_lint.py files/msgdata/msg/msg_0300.json | tail -1
  node tools/trinacria/dialect_query.mjs list_sicilian_municipalities '{"provincia":"CT"}' | head -5
  ```
- **Criterio:** il linter stampa `LINT_FAILED` (è corretto: i testi inglesi di HeartGold superano i 36 caratteri) **senza** traceback Python; il client del dizionario stampa un JSON che contiene `"CT"`. Altrimenti FAIL.

| Strumento | Cosa fa | Ultima riga attesa |
|---|---|---|
| `tools/trinacria/build_trinacria.ps1` | build in WSL | `BUILD_OK` / `BUILD_FAILED` |
| `tools/trinacria/font_extend.py check\|apply\|specimen <png>` | estensione del font (§5) | `FONT_OK` / `FONT_FAILED` |
| `tools/trinacria/trinacria_msg_lint.py [--profile field\|battle\|menu] [--pair PRE POST] [--fix] <json…>` | controllo dei testi (§6) | `LINT_OK` / `LINT_FAILED` |
| `tools/trinacria/dialect_query.mjs <tool> '<json>'` | interroga `sicilian-dialect-mcp` senza client MCP (§6.4) | JSON |
| `tools/trinacria/trinacria_tables.py` | genera le tabelle C da `data/trinacria/*.csv` (§7, §8) | `TABLES_OK` / `TABLES_FAILED` |

---

## 3. Codifica dei testi: cose da sapere prima di scrivere

1. Un banco è un JSON con `"key"` e `"messages"`. Ogni messaggio ha `"id"` (es. `msg_0300_00192`) e `"en_US"`. **La chiave resta `en_US`** anche se il testo è italiano o siciliano: il compilatore legge quella chiave.
2. `"en_US"` è una stringa oppure una **lista di stringhe** spezzata dopo ogni `\n`, `\r`, `\f`. Le due forme sono equivalenti; nei messaggi su più righe si usa la lista (come fa HeartGold).
3. Lo script fa riferimento al testo con il simbolo `msg_<banco>_<indice a 5 cifre>` (es. `NPCMsg msg_0542_T20_00013`). L'**ordine** dei messaggi è quindi parte del codice: non si inseriscono messaggi in mezzo a un banco esistente, si aggiungono **in fondo**.
4. Un banco nuovo si crea in tre mosse: (a) file `files/msgdata/msg/msg_NNNN.json`; (b) riga `NARC_msg_msg_NNNN_bin` in fondo a `files/msgdata/NARC_msg.txt` (il file oggi termina **senza** a capo dopo `NARC_msg_msg_0828_bin`: aggiungi prima un a capo); (c) build. I banchi sono numerati in ordine: il primo banco nuovo di Trinacria è `msg_0829`.

---

## 4. Registro degli ID riservati dal motore

Questi ID sono **fissi**. Il Modulo 2 assegna tutti gli altri all'interno degli intervalli riservati qui sotto, mai fuori.

### 4.1 Flag (`include/constants/flags.h`)

Analisi del 15/10/2026: l'intervallo **0x832–0x95F** (302 flag) non è usato da nessun file del repository (C, assembly, script, eventi). Sta subito dopo i flag degli allenatori (`TRAINER_FLAG_BASE 0x550` + 738 allenatori = 0x831) e prima dei flag di sistema (0x960). Non si cambia `NUM_FLAGS` (2912), quindi il salvataggio non cambia formato.

| ID | Nome | Uso |
|---|---|---|
| 0x832 | `FLAG_POST_RESIGNATION` | mondo dopo le dimissioni (§7) |
| 0x833 | `FLAG_ETNA_ASH_ACTIVE` | pioggia di cenere attiva nell'area etnea (§8) |
| 0x834 | `FLAG_ELICOTTERO_PRIVATO` | sblocca il volo anche con la cenere (§8) |
| 0x835 | `FLAG_TRINACRIA_TRAINERS_RESET` | interno: allenatori già riattivati dopo le dimissioni (§7.4) |
| 0x836–0x83F | riservati al motore | non usare |
| 0x840–0x95F | storia, missioni, visibilità degli NPC | assegnati dal Modulo 2 (288 flag) |

Quando gli script di HeartGold saranno stati sostituiti tutti (Modulo 7), il Modulo 2 libera anche l'intervallo storico **0x040–0x31F** (esclusi gli ID usati dal C: 0x065, 0x06A, 0x06B, 0x070, 0x073, 0x079, 0x07B, 0x087, 0x099, 0x09A, 0x09C, 0x09F, 0x0A7, 0x0C6, 0x0CA, 0x0EE–0x0F2, 0x0F9, 0x118, 0x11A–0x11F, 0x127) e i flag degli oggetti 0x320–0x54F. **Correzione del 18/10/2026 (blocco 2.4):** i flag 0x000–0x03F sono temporanei di mappa (`src/script_manager.c` li azzera a ogni cambio mappa) e non si usano mai per la storia; 0x11C–0x11E sono letti dal C per indice (`FLAG_GOT_BAG + 0…3`, icone del menu). Le assegnazioni definitive e l'elenco dei numeri liberi, calcolato nel repository, sono in `docs/MODULO_2/2.4_FLAGS_VARS.json` (sezione `flag.storico`).

### 4.2 Variabili (`include/constants/vars.h`)

Non usate da nessun file: 0x4059–0x406F (23) e 0x4152–0x416F (30).

| ID | Nome | Valori |
|---|---|---|
| 0x4059 | `VAR_TRINACRIA_ATTO` | 0 = prologo, 1–5 = atti, 6 = post-dimissioni |
| 0x405A | `VAR_TRINACRIA_CONSENSO` | 0–100 (percentuale nei sondaggi) |
| 0x405B–0x406F, 0x4152–0x416F | missioni | assegnati dal Modulo 2 (blocco 2.4: 48 variabili, riserva 0x416D–0x416F) |

Le variabili storiche di HeartGold liberate dalla riscrittura delle mappe (166, tra 0x4030 e 0x416F) diventano variabili di scena `VAR_TR_SCENE_*` (blocco 2.4). Non si usano mai 0x4036–0x4039, 0x4043–0x4048 (lette dal C per indice: `src/sys_vars.c`, Pokémon vaganti) né le altre lette dal C.

### 4.3 Banchi di testo nuovi

| Banco | Contenuto |
|---|---|
| `msg_0829` | gemello post-dimissioni di `msg_0728` (frasi degli allenatori in lotta), stesso numero di messaggi e stesso ordine |
| `msg_0830`–`msg_0933` | gemelli post-dimissioni delle 104 mappe con testi di CT, SR e RG (Modulo 2, blocco 2.1, nell'ordine delle mappe) |
| `msg_0934` e seguenti | gemelli dei blocchi 2.2 e 2.3, e banchi di campagna nuovi delle mappe che in HeartGold usano un banco condiviso; numerazione contigua, senza buchi |

Le mappe senza testi propri (le aree della Zona Safari, che usano il banco condiviso `msg_0003_EVERYWHERE`) non hanno gemello. Il numero nel nome di un banco (542 in `msg_0542_T20`) è la sua posizione in `NARC_msg.txt` (riga n+1 = banco n: verificato il 15/10/2026).

### 4.4 Allenatori

| Costante | Valore | Significato |
|---|---|---|
| `TRINACRIA_POSTGAME_TRAINER_FIRST` | 700 | gli allenatori con ID 700–737 esistono solo nel post-game (compagni da ri-sfidare, Maria, Fantasmi della Prima Repubblica). Non vengono scalati di livello e non vengono riattivati (§7.4). Tutti gli altri allenatori della storia — inclusi i 4 livelli operativi di **«U Sistema»** che sostituiscono il Team Rocket (trama, decisione R-10.2 e R-10.6) — usano gli ID 1–699. |
| `TRINACRIA_POST_LEVEL_BONUS` | 25 | livelli aggiunti alle squadre degli allenatori 1–699 dopo le dimissioni (massimo 100): rappresenta la riorganizzazione di «U Sistema» sotto nuove sigle sei mesi dopo le dimissioni del protagonista (R-10.6). |

### 4.5 Codici di carattere nuovi (§5)

`0x01ED «` · `0x01EE »` · `0x01EF €` · `0x01F0 –` · `0x01F1 —` · `0x01F2 [` · `0x01F3 ]` · `0x01F4 <` · `0x01F5 >` · `0x01F6 |` · `0x01F7 ^` · `0x01F8 \`` · `0x01F9 £` · `0x01FA §` · `0x01FB ©` · `0x01FC ±` · `0x01FD` libero.

### 4.6 Passo M1-04 — Costanti nei file header

**M1-04a — `include/constants/flags.h`**
- **Trova** (una sola volta):
  ```c
  #define NUM_FLAGS 2912
  ```
- **Sostituisci con:**
  ```c
  // Pokemon Trinacria engine flags (0x832-0x95F is unused by HeartGold)
  #define FLAG_TRINACRIA_BASE           0x832
  #define FLAG_POST_RESIGNATION         0x832
  #define FLAG_ETNA_ASH_ACTIVE          0x833
  #define FLAG_ELICOTTERO_PRIVATO       0x834
  #define FLAG_TRINACRIA_TRAINERS_RESET 0x835
  #define FLAG_TRINACRIA_LAST           0x95F

  #define NUM_FLAGS 2912
  ```

**M1-04b — `include/constants/vars.h`**
- **Trova:**
  ```c
  #define NUM_VARS (0x170)
  ```
- **Sostituisci con:**
  ```c
  // Pokemon Trinacria variables (0x4059-0x406F and 0x4152-0x416F are unused by HeartGold)
  #define VAR_TRINACRIA_ATTO     0x4059
  #define VAR_TRINACRIA_CONSENSO 0x405A

  #define NUM_VARS (0x170)
  ```

**M1-04c — nuovo file `include/trinacria/trinacria_engine.h`** (contenuto intero):
```c
#ifndef POKEHEARTGOLD_TRINACRIA_ENGINE_H
#define POKEHEARTGOLD_TRINACRIA_ENGINE_H

// Trainers with id >= this value exist only after the resignation (post-game):
// they are never level-scaled and never re-activated.
#define TRINACRIA_POSTGAME_TRAINER_FIRST 700

// Levels added to story trainers (id < TRINACRIA_POSTGAME_TRAINER_FIRST) after the resignation.
#define TRINACRIA_POST_LEVEL_BONUS 25

// Message bank that replaces msg_0728 (trainer battle texts) after the resignation.
#define TRINACRIA_TRAINER_TEXT_POST_BANK 829

#endif // POKEHEARTGOLD_TRINACRIA_ENGINE_H
```

- **Verifica:** build.
- **Criterio:** `BUILD_OK` e SHA-1 ancora `4fcded0e…` (le costanti non cambiano la ROM finché non sono usate).

### 4.7 Mappe: limiti del motore e numerazioni (decise nel Modulo 2)

I valori sono nel registro del Modulo 2 (`docs/MODULO_2/2.1_MAPS_CT_SR_RG.json`, sezioni `regole` e `piano_globale`); qui c'è il riassunto che serve per leggere i passi del Modulo 1. Le modifiche ai file le applica il Modulo 7 (blocchi 7.2 e 7.5), non questo modulo.

| Cosa | Valore |
|---|---|
| Slot di mappa | 540 (`include/constants/maps.h`): 66 esclusi (il motore li tratta in modo speciale), 119 al blocco 2.1, al massimo 148 al 2.2, al massimo 207 al 2.3. Nessuna mappa nuova oltre i 540. |
| Mondo esterno | matrice 0, **47×17 = 799 celle** (`MAP_MATRIX_MAX_SIZE`): resta di questa misura, il codice non si tocca. |
| Simboli | `MAP_*`, `MAPSEC_*`, `FLYPOINT_*`, `FLAG_SYS_FLYPOINT_*`, `SPAWN_*` di HeartGold vengono **rinominati** (stesso numero). I vecchi nomi restano validi grazie ai file di alias `include/constants/*_hg_compat.h` finché esiste codice HeartGold che li usa. |
| Prossimi numeri liberi (dopo il blocco 2.1) | `msg_0934`, `map_matrix_0322`, MAPSEC 66, `scr_seq_0965`, `zone_event` 491 |
| Regioni del Pokégear | `MAP_REGION_KANTO` = Sicilia orientale (colonna ≥ 24), `MAP_REGION_JOHTO` = Sicilia occidentale |

Per gli alias, i passi di prova di questo modulo che citano `MAP_NEW_BARK` e `FLYPOINT_NEW_BARK` (M1-12, M1-13, M1-14) funzionano anche dopo la rinomina: `MAP_NEW_BARK` diventa un alias di `MAP_CT_CATANIA_CORSO_ITALIA` e `FLYPOINT_NEW_BARK` di `FLYPOINT_CATANIA`.

**Prove a schermo assegnate al Modulo 7** (nate dal registro 2.1):
1. il valore meteo 9 (`WEATHER_UNKNOWN_9`) di Augusta, Priolo e del polo petrolchimico mostra nebbia? Se no, quelle mappe passano a `WEATHER_SUNNY` e il Modulo 4 dà la tinta gialla;
2. le due regioni del Pokégear (lati Johto e Kanto del motore) funzionano come Sicilia occidentale e orientale? Lo conferma il Modulo 4.4.

---

## 5. Font: estensione della tabella caratteri

### 5.1 Stato verificato

- Il font è `files/graphic/font.narc` (11 membri). Il build lo copia così com'è (`files/graphic/meson.build`: `fs.copyfile('font.narc')`); i file `files/graphic/font/font_000000NN.bin` sono la copia estratta dei membri e sono tracciati da git.
- Ogni membro di testo (0, 1, 2, 4, 10) ha 509 glifi 16×16 a 2 bit (1 = inchiostro, 2 = ombra, 3 = fondo della cella, 0 = fuori cella) e una tabella delle larghezze in pixel. Il codice del glifo è il codice della charmap (`glifo = codice − 1`).
- Tutti gli accenti e i circonflessi siciliani **ci sono già**. Il membro 3 (usato solo da `ScrCmd_527` in `scr_seq_0048_D24R0211.s`) non ha accenti: in quel messaggio si scrive senza accenti.
- Mancano nella charmap: `'` e `"` ASCII (si usano `’` `“` `”`), `« » € – —`, `[ ] < > | ^ \``, `£ § © ±` e altri simboli Latin-1 rari. I caratteri `{ } \` restano vietati: sono la sintassi dei comandi di `msgenc`.
- Slot liberi (non mappati e vuoti in tutti i membri): `0x01ED`–`0x01FD` (17).

### 5.2 Passo M1-05 — Estensione

- **Azione (Git Bash, dalla radice del repository):**
  ```bash
  cd /f/Progetti/pokeheartgold
  python -I tools/trinacria/font_extend.py check
  python -I tools/trinacria/font_extend.py apply
  python -I tools/trinacria/font_extend.py check
  python tools/trinacria/font_extend.py specimen /f/Progetti/pokémon-sicilia/docs/font_specimen_trinacria.png
  tail -17 tools/msgenc/charmap.txt
  ```
- **Cosa cambia:** i glifi `0x01ED`–`0x01FC` dei membri 0, 1, 2, 4, 10 (in `font.narc` e nei `.bin`), le loro larghezze, e 16 righe in fondo a `tools/msgenc/charmap.txt` (`01ED=«` … `01FC=±`). L'ombra dei glifi nuovi è calcolata con la stessa regola dei glifi originali (destra, sotto, diagonale).
- **Verifica:** build.
- **Criterio:** i tre comandi stampano `FONT_OK`; le ultime righe della charmap vanno da `01ED=«` a `01FC=±`; `BUILD_OK`. Lo specimen (immagine) mostra 16 simboli leggibili: `« » € – — [ ] < > | ^ \` £ § © ±`.
- **Prova a schermo (Modulo 7):** un cartello di prova con `«Prova» 5 € – [ok] © atrisorb` nella prima mappa; screenshot con l'emulatore.

---

## 6. Testi: formato DS, linter, dialetto

### 6.1 Regole di formattazione (R-TXT)

| Codice | Regola |
|---|---|
| R-TXT-01 | Massimo **36 caratteri** per riga **e** massimo **216 pixel** (riquadro di campo: 27 tile × 8 px; larghezze reali dal font). Il linter controlla entrambe le soglie. |
| R-TXT-02 | Un riquadro ha **2 righe**. `\n` passa alla seconda riga; dopo un `\n` il separatore successivo deve essere `\r` (attende A e scorre di una riga) o `\f` (attende A e pulisce) o la fine del messaggio. Mai tre righe di fila con `\n`. |
| R-TXT-03 | Apostrofo sempre `’` (U+2019), virgolette sempre `“ ”`, puntini `…`. Mai `'` né `"`. (`--fix` del linter corregge `'` e `"` in automatico.) |
| R-TXT-04 | Vietati `{`, `}`, `\` come caratteri di testo. |
| R-TXT-05 | Il nome del giocatore vale 7 caratteri (42 px) nel conteggio; ogni altro `{STRVAR…}` vale 10 caratteri. |
| R-TXT-06 | I messaggi del menu squadra (`msg_0300`) e di sistema terminano con `\r`, come gli originali. I dialoghi degli NPC non terminano con un separatore. |
| R-TXT-07 | Se un messaggio contiene `{STRVAR_1 3, 0, 0}`, lo script che lo mostra deve avere `BufferPlayersName 0` **prima** di `NPCMsg`/`SimpleNPCMsg`. |
| R-TXT-08 | Profili di larghezza del linter: `field` 216 px (dialoghi, cartelli), `battle` 208 px (frasi in lotta, banchi `msg_0728` e `msg_0829`), `menu` 216 px. Il profilo `battle` è prudenziale: si conferma con uno screenshot nel Modulo 7. |

### 6.2 Passo M1-06 — Linter in uso

- **Comando per un banco:** `python -I tools/trinacria/trinacria_msg_lint.py files/msgdata/msg/msg_NNNN.json`
- **Comando per un banco e il suo gemello post-dimissioni:** `python -I tools/trinacria/trinacria_msg_lint.py --pair files/msgdata/msg/msg_PPPP.json files/msgdata/msg/msg_QQQQ.json` (controlla anche stesso numero di messaggi e stessi `{STRVAR…}`).
- **Criterio di ogni passo di testo:** ultima riga `LINT_OK`.

### 6.3 Ripartizione italiano / siciliano (dalle specifiche, vincolante)

- **Italiano:** menu e sistema, cartelli istituzionali, documenti, Maria in contesti formali, il protagonista in contesti formali (italiano colto con inflessioni catanesi).
- **Siciliano della zona esatta:** NPC popolari, commercianti, personaggi di quartiere e i compagni (Turi, Orazio, Christian, Chantal, Totò, Calogero, Pippo). Le coordinate dialettali di ogni comune e quartiere sono nel Modulo 6.
- Shibboleth bloccati: a Catania e nell'est **mai** `picciottu`, `travagghiari`, dittonghi `ie/uo` (`beddu`, `bonu`, `pedi`, `focu`); a Palermo centro **mai** `mbare`, `carusu`.

### 6.4 Uso del dizionario `sicilian-dialect-mcp`

L'esecutore non ha bisogno di un client MCP: usa `tools/trinacria/dialect_query.mjs`, che avvia il server e chiama lo strumento.

```bash
node tools/trinacria/dialect_query.mjs lookup_sicilian_term '{"term":"talìa","comune":"Catania"}'
node tools/trinacria/dialect_query.mjs translate_to_local_dialect '{"italian_query":"ragazzo","comune":"Catania"}'
node tools/trinacria/dialect_query.mjs lookup_sicilian_place '{"query":"Librino"}'
node tools/trinacria/dialect_query.mjs list_sicilian_municipalities '{"provincia":"EN"}'
```

Parametri reali degli strumenti: `lookup_sicilian_term {term, quartiere, comune, provincia}`, `translate_to_local_dialect {italian_query, quartiere, comune, provincia}`, `get_location_vocabulary {quartiere, comune, provincia, include_regional_fallbacks}`, `lookup_sicilian_name {query, genere}`, `lookup_sicilian_surname {cognome, area}`, `lookup_sicilian_place {query, comune, provincia, tipo}`, `list_sicilian_municipalities {provincia, search}`, `lookup_sicilian_saying {query, categoria, area}`, `list_sicilian_sayings_by_theme {categoria}`.

**Limite verificato:** il corpus ha 625 lemmi. Parole comunissime come `mbare` e `munnizza` restituiscono `"risultati_trovati": 0`. Quindi:
1. Ogni parola siciliana usata nei testi è registrata nel **Glossario bloccato** del Modulo 3 (`GLOSSARIO_BLOCCATO.json`) con area, fonte (`MCP` oppure `architetto`) e forma grafica unica.
2. L'esecutore non decide mai una forma: copia il testo del Modulo 6. Il controllo dell'esecutore è meccanico: ogni parola dei testi siciliani deve stare nel Glossario bloccato (lo script di controllo è fornito con il Modulo 3).
3. `upsert_sicilian_term` **non** si usa: il dizionario non si modifica.

---

## 7. Stato globale `FLAG_POST_RESIGNATION`

### 7.1 Architettura (decisa)

Il doppio stato di ogni NPC si ottiene **nel motore**, non con un `if` in ogni script:

1. Ogni banco di testo di una mappa (es. `msg_0901`) ha un **gemello** post-dimissioni (es. `msg_0902`) con **lo stesso numero di messaggi nello stesso ordine**: il messaggio `00005` del gemello è la versione post-dimissioni del messaggio `00005` del banco di campagna.
2. Quando uno script parte, il motore controlla `FLAG_POST_RESIGNATION`: se è attivo, carica il gemello al posto del banco originale. Lo script resta identico (`SimpleNPCMsg msg_0901_00005` mostra automaticamente il testo giusto).
3. Le frasi degli allenatori (`msg_0728`) hanno il gemello `msg_0829` con lo stesso meccanismo.
4. Lo script usa `CheckFlag FLAG_POST_RESIGNATION` / `GoToIfSet FLAG_POST_RESIGNATION, <etichetta>` **solo** quando cambia qualcosa oltre al testo (un NPC che sparisce, una missione che si apre, un allenatore che dopo le dimissioni ti sfida). Lo schema è in §7.6.
5. Dopo le dimissioni, al primo caricamento di una mappa, il motore riattiva tutti gli allenatori 1–699 (azzera i loro flag «sconfitto») e aggiunge `+25` livelli alle loro squadre (massimo 100): tutti gli allenatori del gioco si possono ri-sfidare con le frasi post-dimissioni.

Così il 100% degli NPC ha due stati per costruzione, e il controllo «manca un testo post» diventa meccanico (`--pair` del linter).

### 7.2 Registro dei gemelli: `data/trinacria/post_resignation_banks.csv`

Contenuto al passo M1-07 (solo intestazione: la tabella è vuota finché il banco `msg_0829` non esiste):
```csv
pre_bank,post_bank,note
```
Contenuto dopo il passo M1-10a:
```csv
pre_bank,post_bank,note
728,829,trainer battle texts
```
Il Modulo 2 aggiunge una riga per ogni banco di mappa: le righe sono nella sezione `csv.post_resignation_banks_csv` di ogni blocco del registro (blocco 2.1: da `542,830,MAP_CT_CATANIA_CORSO_ITALIA` in poi, 104 righe; la terza colonna è il simbolo della mappa). Una riga si aggiunge solo quando il gemello esiste. Il generatore (§7.3) produce `include/trinacria/post_resignation_banks.h` e rifiuta (`TABLES_FAILED`) una riga il cui banco non esiste in `files/msgdata/msg/`.

### 7.3 Passo M1-07 — Generatore delle tabelle

- **File:** `data/trinacria/post_resignation_banks.csv` (solo la riga di intestazione, con a capo finale) e `data/trinacria/etna_ash_zone.csv` (contenuto di §8.2, con a capo finale).
- **Azione:** `python -I tools/trinacria/trinacria_tables.py`
- **Criterio:** stampa `TABLES_OK`; esistono `include/trinacria/post_resignation_banks.h` e `include/trinacria/etna_ash_zone.h`. (Collaudato il 15/10/2026 su una copia: con la sola intestazione e con la riga `728,829` produce gli header attesi.)

### 7.4 Passo M1-08 — Funzioni di sistema (`include/sys_flags.h`, `src/sys_flags.c`)

**M1-08a — `include/sys_flags.h`**
- **Trova:**
  ```c
  void ChangeFlag99D(SaveVarsFlags *state, BOOL set);
  ```
- **Sostituisci con:**
  ```c
  void ChangeFlag99D(SaveVarsFlags *state, BOOL set);
  BOOL Save_VarsFlags_CheckPostResignation(SaveVarsFlags *state);
  BOOL Save_VarsFlags_CheckEtnaAshActive(SaveVarsFlags *state);
  BOOL Save_VarsFlags_CheckEtnaAshFlightBlock(SaveVarsFlags *state);
  void Trinacria_ApplyPostResignationReset(SaveVarsFlags *state);
  BOOL Trinacria_IsEtnaAshMap(u32 mapId);
  BOOL Trinacria_IsEtnaAshFlypoint(u32 flypoint);
  ```

**M1-08b — `src/sys_flags.c`**
- **Trova:**
  ```c
  #include "constants/sndseq.h"
  ```
- **Sostituisci con:**
  ```c
  #include "constants/sndseq.h"
  #include "trinacria/etna_ash_zone.h"
  #include "trinacria/trinacria_engine.h"
  ```
- **Poi aggiungi in fondo al file** (dopo l'ultima riga esistente, separato da una riga vuota):
  ```c
  BOOL Save_VarsFlags_CheckPostResignation(SaveVarsFlags *state) {
      return CheckScriptFlag(state, FLAG_POST_RESIGNATION);
  }

  BOOL Save_VarsFlags_CheckEtnaAshActive(SaveVarsFlags *state) {
      return CheckScriptFlag(state, FLAG_ETNA_ASH_ACTIVE);
  }

  BOOL Save_VarsFlags_CheckEtnaAshFlightBlock(SaveVarsFlags *state) {
      if (CheckScriptFlag(state, FLAG_ETNA_ASH_ACTIVE) && !CheckScriptFlag(state, FLAG_ELICOTTERO_PRIVATO)) {
          return TRUE;
      }
      return FALSE;
  }

  void Trinacria_ApplyPostResignationReset(SaveVarsFlags *state) {
      u32 trainerId;
      if (CheckScriptFlag(state, FLAG_TRINACRIA_TRAINERS_RESET)) {
          return;
      }
      for (trainerId = 1; trainerId < TRINACRIA_POSTGAME_TRAINER_FIRST; trainerId++) {
          FlagAction(state, FLAG_ACTION_CLEAR, FLAG_TRAINER(trainerId));
      }
      FlagAction(state, FLAG_ACTION_SET, FLAG_TRINACRIA_TRAINERS_RESET);
  }

  BOOL Trinacria_IsEtnaAshMap(u32 mapId) {
      int i;
      for (i = 0; sTrinacriaEtnaAshMaps[i] != TRINACRIA_TABLE_END_U16; i++) {
          if (sTrinacriaEtnaAshMaps[i] == mapId) {
              return TRUE;
          }
      }
      return FALSE;
  }

  BOOL Trinacria_IsEtnaAshFlypoint(u32 flypoint) {
      int i;
      for (i = 0; sTrinacriaEtnaAshFlypoints[i] != TRINACRIA_TABLE_END_U8; i++) {
          if (sTrinacriaEtnaAshFlypoints[i] == flypoint) {
              return TRUE;
          }
      }
      return FALSE;
  }
  ```
- **Criterio:** `BUILD_OK`.

### 7.5 Passo M1-09 — Scambio dei banchi (`include/script_manager.h`, `src/script_manager.c`)

**M1-09a — `include/script_manager.h`**
- **Trova:**
  ```c
  u32 GetCurrentMapMessageBank(u32 mapId);
  ```
- **Sostituisci con:**
  ```c
  u32 GetCurrentMapMessageBank(u32 mapId);
  u32 Trinacria_SelectMsgBank(u32 bank);
  u32 Trinacria_GetTrainerTextBank(void);
  int Trinacria_ScaleTrainerLevel(u32 trainerId, int level);
  ```

**M1-09b — `src/script_manager.c`, include**
- **Trova:**
  ```c
  #include "script_manager.h"
  ```
  (compare una sola volta, alla riga 14.)
- **Sostituisci con:**
  ```c
  #include "script_manager.h"
  #include "sys_flags.h"
  #include "trinacria/post_resignation_banks.h"
  #include "trinacria/trinacria_engine.h"
  ```

**M1-09c — `src/script_manager.c`, caricamento dei testi**
- **Trova:**
  ```c
  void LoadScriptsAndMessagesParameterized(FieldSystem *fieldSystem, ScriptContext *ctx, int scriptBank, u32 msgBank) {
      ctx->mapScripts = AllocAndReadWholeNarcMemberByIdPair(NARC_fielddata_script_scr_seq, scriptBank, HEAP_ID_FIELD2);
      ctx->msgdata = NewMsgDataFromNarc(MSGDATA_LOAD_LAZY, NARC_msgdata_msg, msgBank, HEAP_ID_FIELD2);
  }

  void LoadScriptsAndMessagesForCurrentMap(FieldSystem *fieldSystem, ScriptContext *ctx) {
      ctx->mapScripts = LoadScriptsForCurrentMap(fieldSystem->location->mapId);
      ctx->msgdata = NewMsgDataFromNarc(MSGDATA_LOAD_LAZY, NARC_msgdata_msg, GetCurrentMapMessageBank(fieldSystem->location->mapId), HEAP_ID_FIELD2);
  }
  ```
- **Sostituisci con:**
  ```c
  // Cached FLAG_POST_RESIGNATION, refreshed every time a script loads its texts.
  // Read by the trainer text and trainer level hooks, which have no FieldSystem.
  static BOOL sTrinacriaPostResignation = FALSE;

  static void Trinacria_RefreshPostResignation(FieldSystem *fieldSystem) {
      SaveVarsFlags *state = Save_VarsFlags_Get(fieldSystem->saveData);
      sTrinacriaPostResignation = Save_VarsFlags_CheckPostResignation(state);
      if (sTrinacriaPostResignation) {
          Trinacria_ApplyPostResignationReset(state);
      }
  }

  u32 Trinacria_SelectMsgBank(u32 bank) {
      int i;
      if (!sTrinacriaPostResignation) {
          return bank;
      }
      for (i = 0; sTrinacriaPostBanks[i].pre != TRINACRIA_TABLE_END_U16; i++) {
          if (sTrinacriaPostBanks[i].pre == bank) {
              return sTrinacriaPostBanks[i].post;
          }
      }
      return bank;
  }

  u32 Trinacria_GetTrainerTextBank(void) {
      return Trinacria_SelectMsgBank(msg_0728);
  }

  int Trinacria_ScaleTrainerLevel(u32 trainerId, int level) {
      int scaled;
      if (!sTrinacriaPostResignation || trainerId >= TRINACRIA_POSTGAME_TRAINER_FIRST) {
          return level;
      }
      scaled = level + TRINACRIA_POST_LEVEL_BONUS;
      if (scaled > 100) {
          scaled = 100;
      }
      return scaled;
  }

  void LoadScriptsAndMessagesParameterized(FieldSystem *fieldSystem, ScriptContext *ctx, int scriptBank, u32 msgBank) {
      Trinacria_RefreshPostResignation(fieldSystem);
      ctx->mapScripts = AllocAndReadWholeNarcMemberByIdPair(NARC_fielddata_script_scr_seq, scriptBank, HEAP_ID_FIELD2);
      ctx->msgdata = NewMsgDataFromNarc(MSGDATA_LOAD_LAZY, NARC_msgdata_msg, Trinacria_SelectMsgBank(msgBank), HEAP_ID_FIELD2);
  }

  void LoadScriptsAndMessagesForCurrentMap(FieldSystem *fieldSystem, ScriptContext *ctx) {
      Trinacria_RefreshPostResignation(fieldSystem);
      ctx->mapScripts = LoadScriptsForCurrentMap(fieldSystem->location->mapId);
      ctx->msgdata = NewMsgDataFromNarc(MSGDATA_LOAD_LAZY, NARC_msgdata_msg, Trinacria_SelectMsgBank(GetCurrentMapMessageBank(fieldSystem->location->mapId)), HEAP_ID_FIELD2);
  }
  ```
- **Criterio:** `BUILD_OK`. A questo punto la tabella dei gemelli è vuota: il gioco non cambia. **Il passo M1-10 va fatto subito dopo**, prima di qualunque prova con il flag acceso.

### 7.6 Passo M1-10 — Gemello delle frasi degli allenatori e aggancio in `trainer_data.c`

**M1-10a — banco `msg_0829`**
- **Azione (Git Bash):**
  ```bash
  cd /f/Progetti/pokeheartgold
  python -I -c "import json; d=json.load(open('files/msgdata/msg/msg_0728.json',encoding='utf-8')); [m.__setitem__('id', m['id'].replace('msg_0728_','msg_0829_')) for m in d['messages']]; json.dump(d, open('files/msgdata/msg/msg_0829.json','w',encoding='utf-8',newline='\n'), ensure_ascii=False, indent=2)"
  printf '\nNARC_msg_msg_0829_bin' >> files/msgdata/NARC_msg.txt
  tail -2 files/msgdata/NARC_msg.txt
  printf '728,829,trainer battle texts\n' >> data/trinacria/post_resignation_banks.csv
  python -I tools/trinacria/trinacria_tables.py
  ```
  (Il gemello nasce come copia: il Modulo 6 ne riscrive ogni messaggio. Una copia identica non cambia il gioco.)
- **Criterio:** le ultime due righe di `NARC_msg.txt` sono `NARC_msg_msg_0828_bin` e `NARC_msg_msg_0829_bin`; il generatore stampa `TABLES_OK`; `include/trinacria/post_resignation_banks.h` contiene `{ 728, 829 },`.

**M1-10b — `src/trainer_data.c`, include**
- **Trova:**
  ```c
  #include "save_misc_data.h"
  ```
- **Sostituisci con:**
  ```c
  #include "save_misc_data.h"
  #include "script_manager.h"
  ```

**M1-10c — `src/trainer_data.c`, banco delle frasi**
- **Trova:**
  ```c
              ReadMsgData_NewNarc_ExistingString(NARC_msgdata_msg, msg_0728, (u32)(rdbuf[0] / 4), heapID, str);
  ```
- **Sostituisci con:**
  ```c
              ReadMsgData_NewNarc_ExistingString(NARC_msgdata_msg, Trinacria_GetTrainerTextBank(), (u32)(rdbuf[0] / 4), heapID, str);
  ```

**M1-10d — `src/trainer_data.c`, livelli** (quattro sostituzioni, ognuna una sola volta nel file)

| Trova | Sostituisci con |
|---|---|
| `CreateMon(mon, species, monSpecies[i].level, iv,` | `CreateMon(mon, species, Trinacria_ScaleTrainerLevel(enemies->trainerId[partyIndex], monSpecies[i].level), iv,` |
| `CreateMon(mon, species, monSpeciesMoves[i].level, iv,` | `CreateMon(mon, species, Trinacria_ScaleTrainerLevel(enemies->trainerId[partyIndex], monSpeciesMoves[i].level), iv,` |
| `CreateMon(mon, species, monSpeciesItem[i].level, iv,` | `CreateMon(mon, species, Trinacria_ScaleTrainerLevel(enemies->trainerId[partyIndex], monSpeciesItem[i].level), iv,` |
| `CreateMon(mon, species, monSpeciesItemMoves[i].level, iv,` | `CreateMon(mon, species, Trinacria_ScaleTrainerLevel(enemies->trainerId[partyIndex], monSpeciesItemMoves[i].level), iv,` |

- **Verifica:** build.
- **Criterio:** `BUILD_OK` e (con `msg_0829` ancora identico a `msg_0728`) partita di prova senza differenze nelle frasi degli allenatori.

### 7.7 Schema di script per gli NPC (vincolante per il Modulo 6)

NPC che parla e basta (il caso del 90% degli NPC). Il doppio stato è automatico:
```asm
scr_seq_<CODICE>_005:
	SimpleNPCMsg msg_0901_00005
	End
```
NPC con nome del giocatore nel testo (R-TXT-07):
```asm
scr_seq_<CODICE>_006:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	NPCMsg msg_0901_00006
	WaitButton
	CloseMsg
	ReleaseAll
	End
```
NPC che cambia **comportamento** dopo le dimissioni (es. un allenatore che solo dopo ti sfida):
```asm
scr_seq_<CODICE>_007:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	GoToIfSet FLAG_POST_RESIGNATION, _<CODICE>_007_POST
	NPCMsg msg_0901_00007
	WaitButton
	CloseMsg
	ReleaseAll
	End

_<CODICE>_007_POST:
	NPCMsg msg_0901_00008
	WaitButton
	CloseMsg
	ReleaseAll
	End
```
Nel caso di comportamento diverso, i messaggi `00007` e `00008` esistono **in entrambi** i banchi (campagna e gemello) per tenere lo stesso ordine; nel gemello il testo `00007` è uguale a quello del banco di campagna.

### 7.8 Registro degli NPC e proporzione 60/40

Ogni NPC ha una riga in `data/trinacria/npc_registry.csv` (consegnato con il Modulo 2, blocco 2.4). Le prime 9 colonne sono queste; il blocco 2.4 (`docs/MODULO_2/2.4_FLAGS_VARS.json`, sezione `npc_registry`) aggiunge `ruolo,visibile,hide_flag,trainer_id,pokemon_species,accanto_a,codice_trama,note` (17 colonne in tutto, anche i Pokémon in scena hanno una riga):
```csv
map_symbol,npc_id,x,y,sprite,msg_bank,msg_index,post_category,dialect_area
```
`post_category` vale `CAPRO` (capro espiatorio) o `ESTIMATORE` per la gente comune e gli allenatori comuni visibili dopo le dimissioni, `ESENTE` per gli altri ruoli (membri di «U Sistema», compagni, personaggi con nome, servizi, luoghi della memoria, Pokémon). Il controllo (`tools/trinacria_registry_check.py --npc …`, consegnato con il blocco 2.4) verifica, provincia per provincia, che `CAPRO` sia tra il 58% e il 62% e `ESTIMATORE` tra il 38% e il 42%.

### 7.9 Passo M1-11 — Prova del doppio stato

- **File:** in `msg_0829.json` cambia **solo** il messaggio `msg_0829_00001` in `["Post-dimissioni: prova\n", "del banco gemello."]`.
- **Prova:** con l'emulatore (Modulo 7, script di prova), in una partita salvata: attiva `FLAG_POST_RESIGNATION` con il menu di debug **oppure** con uno script di prova temporaneo (`SetFlag FLAG_POST_RESIGNATION` in uno NPC), poi affronta un allenatore il cui primo messaggio usa l'indice 1 del suo blocco.
- **Criterio PASS:** il messaggio mostrato è «Post-dimissioni: prova del banco gemello.» e la squadra avversaria ha +25 livelli. Poi **ripristina** `msg_0829_00001` e togli lo script di prova (commit separato `[M1-11] ripristino`).

---

## 8. Meteo `RinaDiL’Etna` e blocco del volo

### 8.1 Comportamento (deciso)

| Situazione | Effetto |
|---|---|
| `FLAG_ETNA_ASH_ACTIVE` acceso e mappa nell'elenco dell'area etnea | il meteo della mappa diventa `WEATHER_SANDSTORM` (7), mostrato come cenere nera dopo il passo M1-15; in lotta il meteo è Terrempesta, il cui nome nel gioco è `RinaDiL’Etna` (Modulo 3) |
| Uso di `Passaggiu` (Volo) dal menu squadra in una mappa dell'area etnea, cenere attiva, senza `FLAG_ELICOTTERO_PRIVATO` | rifiutato con il messaggio «Spazio aereo chiuso per cenere vulcanica! La SAC ti dirotta a piedi!» |
| Mappa del Volo (Pokégear) da qualunque mappa, cenere attiva, senza elicottero | le destinazioni dell'area etnea non si possono selezionare |
| `FLAG_ELICOTTERO_PRIVATO` acceso | nessun blocco del volo; la cenere resta visibile |

Il meteo si calcola **all'ingresso** di una mappa (`src/field_warp_tasks.c`, riga 245). Quando uno script accende o spegne `FLAG_ETNA_ASH_ACTIVE` mentre il giocatore è già nella mappa, lo script esegue subito dopo un `Warp` nella stessa mappa e nelle stesse coordinate (schema nel Modulo 6), così il meteo si aggiorna.

### 8.2 Elenco dell'area etnea: `data/trinacria/etna_ash_zone.csv`

Contenuto iniziale (fixture di prova: la prima mappa di HeartGold, finché il Modulo 2 non crea le mappe siciliane; il Modulo 7 la sostituisce con l'elenco definitivo):
```csv
kind,symbol
map,MAP_NEW_BARK
flypoint,FLYPOINT_NEW_BARK
```
Elenco definitivo: sezione `csv.etna_ash_zone_csv` del registro 2.1 (22 righe). Sono le **19 mappe esterne** di Catania città (Corso Italia, via Etnea, Duomo, San Cristoforo, Galermo, Librino, Ognina, Plaia, Fontanarossa), Misterbianco, Aci Castello, Aci Trezza, Acireale, Nicolosi, Etna Sud, Paternò, Adrano, Bronte, Randazzo, e i **3 punti di volo** `FLYPOINT_CATANIA`, `FLYPOINT_ACIREALE`, `FLYPOINT_NICOLOSI`. Gli interni non ci sono (la cenere cade solo all'aperto) e Caltagirone resta fuori dalla zona. Il Modulo 7 sostituisce le due righe di prova con queste.

### 8.3 Passo M1-12 — Meteo (`src/field_system_rtc_weather.c`)

**M1-12a — include**
- **Trova:**
  ```c
  #include "unk_02055418.h"
  ```
- **Sostituisci con:**
  ```c
  #include "unk_02055418.h"
  #include "constants/weather.h"
  #include "save_vars_flags.h"
  #include "sys_flags.h"
  ```

**M1-12b — calcolo del meteo**
- **Trova:**
  ```c
      u32 weatherType = MapHeader_GetWeatherType(mapId);
      if (mapId != MAP_MOUNT_SILVER_CAVE_SUMMIT) {
  ```
- **Sostituisci con:**
  ```c
      u32 weatherType = MapHeader_GetWeatherType(mapId);
      if (Trinacria_IsEtnaAshMap(mapId) && Save_VarsFlags_CheckEtnaAshActive(Save_VarsFlags_Get(fieldSystem->saveData))) {
          return WEATHER_SANDSTORM;
      }
      if (mapId != MAP_MOUNT_SILVER_CAVE_SUMMIT) {
  ```
- **Criterio:** `BUILD_OK`. Prova (Modulo 7): con il flag acceso, entrando a `MAP_NEW_BARK` compare la tempesta; con il flag spento, no.

### 8.4 Passo M1-13 — Blocco di `Passaggiu` dal menu squadra

**M1-13a — `include/constants/field_move_response.h`**
- **Trova:**
  ```c
  #define FIELD_MOVE_RESPONSE_NOT_NOW         5
  ```
- **Sostituisci con:**
  ```c
  #define FIELD_MOVE_RESPONSE_NOT_NOW         5
  #define FIELD_MOVE_RESPONSE_ETNA_ASH        6
  ```

**M1-13b — `src/field_move.c`** (dentro `FieldMove_CheckFly`)
- **Trova:**
  ```c
      if (!MapHeader_IsFlyAllowed(checkData->mapId)) {
          return FIELD_MOVE_RESPONSE_NOT_HERE;
      }
      if (Save_VarsFlags_CheckHaveFollower(Save_VarsFlags_Get(checkData->fieldSystem->saveData)) == TRUE) {
  ```
  (Verificato: il blocco compare una sola volta, in `FieldMove_CheckFly`.)
- **Sostituisci con:**
  ```c
      if (!MapHeader_IsFlyAllowed(checkData->mapId)) {
          return FIELD_MOVE_RESPONSE_NOT_HERE;
      }
      if (Trinacria_IsEtnaAshMap(checkData->mapId) && Save_VarsFlags_CheckEtnaAshFlightBlock(Save_VarsFlags_Get(checkData->fieldSystem->saveData)) == TRUE) {
          return FIELD_MOVE_RESPONSE_ETNA_ASH;
      }
      if (Save_VarsFlags_CheckHaveFollower(Save_VarsFlags_Get(checkData->fieldSystem->saveData)) == TRUE) {
  ```

**M1-13c — messaggio: `files/msgdata/msg/msg_0300.json`**
- **Azione:** aggiungi **in fondo** alla lista `"messages"` (dopo `msg_0300_00191`) questo oggetto:
  ```json
  {
    "id": "msg_0300_00192",
    "en_US": [
      "Spazio aereo chiuso per cenere\n",
      "vulcanica!\r",
      "La SAC ti dirotta a piedi!\r"
    ]
  }
  ```
- **Verifica testo:** `python -I tools/trinacria/trinacria_msg_lint.py --profile menu files/msgdata/msg/msg_0300.json | grep 00192` non deve stampare nulla (nessun problema sul messaggio 192).

**M1-13d — `src/party_menu_list_items.c`**
- **Trova:**
  ```c
      case FIELD_MOVE_RESPONSE_NOT_NOW:
          msgId = msg_0300_00181;
          break;
  ```
- **Sostituisci con:**
  ```c
      case FIELD_MOVE_RESPONSE_NOT_NOW:
          msgId = msg_0300_00181;
          break;
      case FIELD_MOVE_RESPONSE_ETNA_ASH:
          msgId = msg_0300_00192;
          break;
  ```
- **Criterio:** `BUILD_OK`. Prova (Modulo 7): a `MAP_NEW_BARK` con cenere attiva, Pokémon con Volo, medaglia `BADGE_STORM` presente → appare il messaggio in due riquadri.

### 8.5 Passo M1-14 — Blocco delle destinazioni nella mappa del Volo

- **File:** `src/application/pokegear/map/overlay_101_021E9270.c`, funzione `ov101_021EA81C`.
- **Trova:**
  ```c
          if (!Save_VarsFlags_FlypointFlagAction(mapApp->pokegear->saveVarsFlags, FLAG_ACTION_CHECK, flypoint->flypoint)) {
              continue;
          }
          return i;
  ```
- **Sostituisci con:**
  ```c
          if (!Save_VarsFlags_FlypointFlagAction(mapApp->pokegear->saveVarsFlags, FLAG_ACTION_CHECK, flypoint->flypoint)) {
              continue;
          }
          if (Trinacria_IsEtnaAshFlypoint(flypoint->flypoint) && Save_VarsFlags_CheckEtnaAshFlightBlock(mapApp->pokegear->saveVarsFlags)) {
              continue;
          }
          return i;
  ```
- **Criterio:** `BUILD_OK`. Prova (Modulo 7): con cenere attiva, nella mappa del Volo il cursore non si ferma su New Bark (fixture).

### 8.6 Passo M1-15 — Particelle nere della cenere

La grafica del meteo sta in `files/data/weather_sys.narc` (59 membri), aperto dal codice come `NARC_a_0_6_3` (`asm/overlay_01_021EB1E8.s`, funzione `ov01_021EB64C`). Il membro della tavolozza della tempesta di sabbia si individua con una prova binaria, senza interpretare immagini:

1. Estrai il NARC: `python "F:\Progetti\pokémon-trinacria\scripts\sicilia\mappe\narc.py" unpack files/data/weather_sys.narc /tmp/weather` (comando dello strumento già provato).
2. Elenca i membri che iniziano con `RLCN` (tavolozze NCLR): sono i candidati.
3. Per ogni candidato, uno alla volta: sostituisci tutti i colori tranne lo 0 con magenta `#F800F8`, reimpacchetta, build, entra a `MAP_NEW_BARK` con cenere attiva, screenshot, conta i pixel magenta con `python -c "from PIL import Image; im=Image.open('shot.png').convert('RGB'); print(sum(1 for p in im.getdata() if p==(248,0,248)))"`. Ripristina il NARC originale dopo ogni prova.
4. Il candidato che produce **più di 200** pixel magenta è la tavolozza della sabbia. Annota il suo indice in `data/trinacria/weather_ash_palette.txt`.
5. Sostituisci i colori 1–15 di quella tavolozza, nell'ordine, con: `#101012 #1A1A1E #24242A #2E2E35 #393940 #44444C #505058 #5C5C65 #686872 #75757F #82828C #8F8F99 #9C9CA6 #3A2A22 #5A3A2A` (grigi della cenere; gli ultimi due sono brace spenta). Il colore 0 resta invariato.
6. **Criterio:** `BUILD_OK`; nello screenshot con cenere attiva, almeno 200 pixel hanno colore tra quelli del punto 5; zero pixel del colore sabbia originale nella zona del cielo.

---

## 9. Titolo, introduzione, copyright e crediti → `atrisorb`

### 9.1 Dove stanno le scritte di Nintendo/Game Freak

| Elemento | File | Come si cambia |
|---|---|---|
| Schermata copyright all'avvio | `files/demo/opening/gs_opening/gs_opening_00000005.NCGR` (tile) + `gs_opening_00000013.NSCR` (mappa), caricati su `GF_BG_LYR_MAIN_0` da `src/intro_movie_scene_1.c` (righe 288 e 290); resta a schermo 30 frame, poi dissolvenza di 60 | nuova immagine stessa dimensione e stessa tavolozza (Modulo 4, voce `GFX-COPYRIGHT`) |
| Logo e sfondi del titolo | `files/demo/title/titledemo/` (PNG, NCLR, NSCR, NCGR, due NSBMD del logo) caricati da `src/title_screen.c` (righe 597–628) | nuove immagini (Modulo 4, voci `GFX-TITLE-*`) |
| Crediti | banco `files/msgdata/msg/msg_0440.json` (301 messaggi, caricato da `src/credits/credits.c` riga 245 come `0x1b8`); impaginazione in `src/credits/data1.c` e `data2.c` | si riscrivono i 301 testi **senza cambiarne numero e ordine** (Modulo 6, capitolo «Coda») |
| Nome nel menu del DS | `heartgold.us/banner.bsf` (UTF-16 LE) | passo M1-16 |

### 9.2 Testo della schermata copyright (deciso)

Riga 1: `Pokémon Trinacria` · Riga 2: `© 2026 atrisorb` · Riga 3: `Progetto amatoriale non ufficiale.` · Riga 4: `Pokémon © Nintendo / Creatures / GAME FREAK`.

La riga 4 resta perché è un'attribuzione obbligatoria dei marchi originali: **non** dice che il gioco è loro. Tutte le altre scritte Nintendo/Game Freak (titolo, intro, crediti, banner) diventano `atrisorb`.

### 9.3 Passo M1-16 — Banner del DS

- **Azione (Git Bash, radice del repository):**
  ```bash
  python -I -c "
  lines = ['ImageFile: heartgold.us/icon.nbfc', 'PlttFile: heartgold.us/icon.nbfp', '']
  for lang in ('JP', 'EN', 'FR', 'GE', 'IT', 'SP'):
      lines += [lang + ': Pokémon Trinacria', '    atrisorb']
  lines.append('')
  open('heartgold.us/banner.bsf', 'w', encoding='utf-16', newline='\n').write('\n'.join(lines))
  "
  ```
- **Formato verificato il 15/10/2026:** il file originale è UTF-16 LE con BOM, fine riga LF, righe `ImageFile:`/`PlttFile:`, una riga vuota, poi per ogni lingua `XX: <titolo>` e `    <editore>` (4 spazi), con a capo finale. Il blocco riproduce esattamente questa struttura.
- **Criterio:** `BUILD_OK`; nel menu di melonDS il gioco si chiama «Pokémon Trinacria / atrisorb».

### 9.4 Crediti: vincoli tecnici per il Modulo 6

- Il messaggio 0 e 1 di `msg_0440` sono le intestazioni HeartGold/SoulSilver: diventano `{COLOR 1}{ALN_CENTER} Pokémon Trinacria\n{COLOR 0}\n{ALN_CENTER} Titoli di coda\n\n` (stessa struttura di comandi dell'originale).
- I comandi `{COLOR n}` e `{ALN_CENTER}` di ogni messaggio restano **identici e nello stesso ordine**; cambia solo il testo.
- Nessun nome dello staff di HeartGold. Autore: `atrisorb`. I messaggi senza contenuto nuovo diventano stringhe vuote `""`, non si cancellano.

---

## 10. Musica: aggancio tecnico (dettagli nel Modulo 5)

- L'archivio è `files/data/sound/gs_sound_data.sdat`. I nomi delle sequenze sono in `include/constants/sndseq.h`.
- I nomi Trinacria delle musiche (`SEQ_CT_VERMUT`, `SEQ_TRN_CENTRO_POKEMON`…) sono **alias** degli slot HeartGold, definiti nel file nuovo `include/trinacria/trinacria_seq.h` (contenuto nel registro del Modulo 2, sezione `file_trinacria_seq_h`; versione definitiva nel blocco 2.5: 62 musiche di campo + 30 di lotta, incontro e vittoria). Il file è incluso da `include/constants/sndseq.h` (blocco 2.5), quindi i nomi valgono anche negli script. Nessuna sequenza nuova: il Modulo 5 sostituisce i dati dello slot e del suo gemello `SEQ_GS_P_*` (modalità «suoni GB») quando esiste. Giorno e notte usano lo stesso brano. Gli slot musicali del Team Rocket sono rimappati sui temi di **«U Sistema»** (trama, decisione R-10.6; registro 2.5, sezione `musiche.slot_team_rocket`): incontro `SEQ_GS_EYE_ROCKET`, lotta `SEQ_GS_VS_ROCKET`, covi e uffici `SEQ_GS_E_RIVAL1` (`SEQ_GS_D_AJITO` è già la crisi di Fontanarossa).
- Il gioco ha già un meccanismo «musica diversa se un flag è acceso»: la tabella `sMusicOverrideMap` in `src/sys_flags.c` (`{ mappa, flag, sequenza }`). Il Modulo 5 la usa per: cenere attiva su Fontanarossa, mondo post-dimissioni, silenzio di Capaci.
- Regola: nessuna mappa senza musica, tranne Capaci e il Grande Cretto, dove la sequenza è il vento (Modulo 5, `SEQ_CAPACI_WIND_SILENCE`).

---

## 11. Verifica a schermo

Si riusa l'impianto già provato di `F:\Progetti\pokémon-trinacria\tasks\AMBIENTE.md` §6 (melonDS in WSL, `emu.sh start|keys|touch|shot|stop`). Il Modulo 7 consegna una copia di `emu.sh` puntata su `F:\Progetti\pokeheartgold\build\pokeheartgold.us.nds` e i salvataggi di prova. Ogni prova a schermo ha un criterio misurabile (testo letto con screenshot + confronto, conteggio di pixel, coordinate del giocatore).

---

## 12. Riepilogo dei passi del Modulo 1

| Passo | Titolo | Tocca | Criterio |
|---|---|---|---|
| M1-01 | Ramo `trinacria` | git | ramo attivo, albero pulito |
| M1-02 | Compilatore e build di riferimento | `tools/mwccarm`, `tools/trinacria/build_trinacria.ps1` | `BUILD_OK` + SHA-1 `4fcded0e…` |
| M1-03 | Strumenti Trinacria | `tools/trinacria/` | linter e dizionario rispondono |
| M1-04 | Costanti | `flags.h`, `vars.h`, `include/trinacria/trinacria_engine.h` | `BUILD_OK`, SHA invariato |
| M1-05 | Estensione del font | `font.narc`, `font/*.bin`, `charmap.txt` | `FONT_OK` ×3, `BUILD_OK` |
| M1-06 | Linter in uso | — | `LINT_OK` sui banchi nuovi |
| M1-07 | Tabelle generate | `data/trinacria/*.csv`, `include/trinacria/*.h` | `TABLES_OK` |
| M1-08 | Funzioni di sistema | `sys_flags.h/.c` | `BUILD_OK` |
| M1-09 | Scambio dei banchi | `script_manager.h/.c` | `BUILD_OK` |
| M1-10 | Gemello `msg_0829` + aggancio allenatori | `msg_0829.json`, `NARC_msg.txt`, `trainer_data.c` | `BUILD_OK` |
| M1-11 | Prova del doppio stato | `msg_0829.json` (temporaneo) | testo gemello + livelli +25 a schermo |
| M1-12 | Meteo cenere | `field_system_rtc_weather.c` | tempesta solo con flag |
| M1-13 | Blocco di `Passaggiu` | `field_move_response.h`, `field_move.c`, `msg_0300.json`, `party_menu_list_items.c` | messaggio SAC a schermo |
| M1-14 | Blocco nella mappa del Volo | `overlay_101_021E9270.c` | destinazione non selezionabile |
| M1-15 | Cenere nera | `weather_sys.narc` | ≥200 pixel grigio cenere |
| M1-16 | Banner del DS | `banner.bsf` | nome nel menu |
| — | Copyright, titolo, crediti | grafica (Modulo 4), testi (Modulo 6) | — |

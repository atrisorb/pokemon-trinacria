"""Testi fissi del documento del blocco 6.01 (il resto lo scrive gen601.py dai dati)."""

VERSIONE = '1.0'
DATA = '08/11/2026'

INTESTAZIONE = """# Modulo 6 - Blocco 6.01 - Prologo: il Cubbar e la casa di Corso Italia

**Versione:** {versione} - {data} - **Progetto:** Pokémon Trinacria (autore: atrisorb) - **Repository di destinazione:** `F:\\Progetti\\pokeheartgold`

**File del blocco:**

| File | Cosa contiene |
|---|---|
| `docs/MODULO_6/6.01_PROLOGO.md` | questo documento |
| `docs/MODULO_6/6.01_PROLOGO.json` | indice: file con SHA-1, risorse usate, righe del registro NPC, elenco dei testi per il Glossario, ancore, prove |
| `docs/MODULO_6/6.01_FILE/` | **i file da copiare** nel repository, con lo stesso percorso relativo (18 file: 6 banchi di testo, 9 file di script, 3 file di eventi) |
| `docs/MODULO_6/6.01_NPC.csv` | le 14 righe del registro degli NPC di questo blocco (17 colonne, `data/trinacria/npc_registry.csv`) |
| `tools/trinacria_script_check.py` | strumento nuovo: controlla un blocco del Modulo 6 → `SCRIPT_OK`; `--selftest` → `SELFTEST_OK` (18 guasti provocati sul blocco, uno per codice) |
| `tools/generatori/6.01/` | generatore: `gen601.py`, `content601.py` (testi), `scripts601.py` (script ed eventi), `text601.py` |

Fonti lette nel repository: `asm/macros/script.inc` e `movement.inc` (macro), `files/fielddata/script/scr_seq/` e `files/fielddata/eventdata/zone_event/` dei tre slot (`T25SP0101`, `T20R0201`, `T20R0202`), `files/msgdata/msg/` dei loro banchi, `src/oaks_speech.c`, `src/scrcmd_c.c` (`ScrCmd_NamePlayer`, `ScrCmd_804`), `include/constants/` (flag, variabili, sprite, specie). Dal progetto: trama v1.9 (M-CT-00, M-CT-01, R-05, R-10), registri 2.1 (le tre mappe), 2.4 (flag, variabili, registro NPC), 2.5 (sprite, medaglie), blocchi 3.x (nomi e Glossario), 4.2 (la stanza del Cubbar: celle libere e punti), 4.4 (`ScrCmd_804 2`), 4.5 (sprite) e Modulo 1 (§3, §6, §7.7).
"""

IN_BREVE = """## 0. In breve

- **Primo blocco del Modulo 6.** Oltre ai contenuti del Prologo (M-CT-00 e M-CT-01), fissa il formato che i 37 blocchi successivi ripetono: una cartella `6.NN_FILE/` che si copia nel repository com'è, un indice JSON, un CSV di righe del registro NPC e uno strumento di controllo. Le regole stanno nel §2 (R-SCR-01…R-SCR-15).
- **Tre mappe riscritte per intero:** `MAP_CT_MISTERBIANCO_CUBBAR` (il flashback alle 3:30), `MAP_CT_CATANIA_CASA_PROTAGONISTA_2F` (la camera: inizio partita, risveglio alle 14:00) e `MAP_CT_CATANIA_CASA_PROTAGONISTA_1F` (la madre Graziella e il Pokégear). Le due mappe esterne (`MAP_CT_MISTERBIANCO`, `MAP_CT_CATANIA_CORSO_ITALIA`) non cambiano qui: le scrivono 6.07 e 6.05, che devono rispettare le ancore del §6.
- **Una sola variabile di scena, `VAR_TR_SCENE_CT_01`, regge tutto il Prologo** (valori 0-6, §3). La nuova partita parte, come in HeartGold, nella camera (`src/location_backup.c`): lo script `OnFrame` della camera manda il giocatore nel Cubbar, l'uscita dal Cubbar lo riporta in camera alle 14:00 e la scena della madre al piano terra chiude M-CT-01 (`FLAG_M_CT_01`, `VAR_TRINACRIA_ATTO` = 1).
- **Nessuna lotta, nessun selvatico** (come chiede la trama). Il Cubbar ha 7 persone e 4 Pokémon in scena (`Subwoofer`, `Gattupardu`, `Novicudi`, `Diavulazzu`); la casa ha Graziella e i due Pokémon domestici (`Puparu`, `Leccu`).
- **Ogni messaggio ha il suo gemello post-dimissioni** nello stesso ordine; il controllo è meccanico (linter `--pair`, Glossario, elenco `testi` uguale ai banchi).
- **Cosa non è deciso qui** e va guardato: il §7 elenca le decisioni (la scelta del nome è quella del discorso iniziale di HeartGold, che la richiesta 6.00 traduce).
"""

APPLICAZIONE = """## 1. Come si applica (per il Modulo 7)

Questo blocco non tocca il repository: lo applica il blocco 7.5 (mappe e script di CT, SR, RG) con TASK di questo tipo, uno per mappa:

1. **Copia** ogni file di `docs/MODULO_6/6.01_FILE/<percorso>` in `F:\\Progetti\\pokeheartgold\\<percorso>`, sovrascrivendo l'originale di HeartGold (colonna «azione» = `sostituisci`) o creandolo (`nuovo`). I file sono UTF-8, fine riga LF, senza BOM.
2. **Registra i banchi nuovi** (`msg_0850`, `msg_0851`, `msg_0870`): una riga `NARC_msg_msg_NNNN_bin` in fondo a `files/msgdata/NARC_msg.txt` (Modulo 1 §3.4); i tre gemelli sono nel blocco 2.1 (`gemello_post`).
3. **Intestazioni dei simboli:** `include/trinacria/trinacria_flags.h`, `trinacria_vars.h`, `trinacria_badges.h` e `trinacria_sprites.h` (Modulo 7.2) devono già esserci: gli script usano `FLAG_M_CT_00`, `FLAG_M_CT_01`, `VAR_TR_SCENE_CT_01`, `BADGE_DOSSIER_LIOTRU`, `SPRITE_TRN_CHRISTIAN` e `SPRITE_TRN_GRAZIELLA`.
4. **Riga del registro NPC:** aggiungi le righe di `6.01_NPC.csv` a `data/trinacria/npc_registry.csv`.
5. **Verifica:** build (`BUILD_OK`), `python -I tools/trinacria/trinacria_msg_lint.py --pair <campagna> <gemello>` per ognuno dei tre banchi (`LINT_OK`) e, a schermo, le prove del §8.

I nomi dei file e dei simboli (`scr_seq_0910_T25SP0101`, `msg_0603_T25SP0101`…) sono quelli dei registri 2.1: il blocco **sostituisce il contenuto** dei file di HeartGold degli stessi slot; gli slot non cambiano numero.
"""

REGOLE = """## 2. Regole del Modulo 6 (valgono per i blocchi 6.01-6.38)

| Codice | Regola |
|---|---|
| R-SCR-01 | **Un blocco = una cartella da copiare.** `docs/MODULO_6/6.NN_FILE/` ripete i percorsi di `pokeheartgold` (`files/msgdata/msg/`, `files/fielddata/script/scr_seq/`, `files/fielddata/eventdata/zone_event/`); l'indice `6.NN_*.json` elenca ogni file con SHA-1 e azione; il CSV `6.NN_NPC.csv` ha le righe del registro NPC; `python -I tools/trinacria_script_check.py check docs/MODULO_6/6.NN_*.json` deve dare `SCRIPT_OK`. Le mappe di un blocco sono riscritte per intero: nessun frammento da incollare. |
| R-SCR-02 | **Nomi.** Script `scr_seq_<CODICE>_NNN` (CODICE = `codice_file_hg` del registro 2.1); oggetti `obj_<codice minuscolo>_<ruolo>` (solo minuscole, cifre e `_`, come chiede il registro NPC); etichette locali `_<ruolo>_<fase>` in minuscolo; costanti `_EV_scr_seq_<CODICE>_NNN` e `obj_…` nell'header `event_<CODICE>.h`, nell'ordine di zone_event. I nomi HeartGold dei vecchi oggetti (`obj_T25SP0101_suit`) spariscono con l'header riscritto. |
| R-SCR-03 | **Schemi di script (Modulo 1 §7.7):** persona che parla = `PlaySE SEQ_SE_DP_SELECT`, `LockAll`, `FacePlayer`, `BufferPlayersName 0`, `NPCMsg`, `WaitButton`, `CloseMsg`, `ReleaseAll`, `End`; Pokémon in scena = lo stesso con `PlayCry SPECIES_<specie>, 0` prima di `NPCMsg` e `WaitCry` dopo; cartello o mobile = senza `FacePlayer`. `BufferPlayersName 0` sta in **ogni** script di persona (anche se il suo testo non ha il nome), perché campagna e gemello hanno gli stessi `{STRVAR}` ma uno dei due potrebbe usarlo. Il controllo J10 vuole `BufferPlayersName` nella stessa etichetta del messaggio col nome. |
| R-SCR-04 | **Catene di messaggi.** Quando uno script mostra più messaggi di fila (`NPCMsg` `NPCMsg`…), tutti tranne l'ultimo finiscono con `\\r` (come HeartGold: attende A e scorre); l'ultimo no, e lo script chiude con `WaitButton`, `CloseMsg`. Dentro un messaggio ogni riquadro ha 2 righe unite da `\\n`, i riquadri sono separati da `\\f`; `generatori/6.01/content601.py` spezza le righe con le larghezze vere del font (massimo 34 caratteri e 208 px, sotto i 216 di R-TXT-01). |
| R-SCR-05 | **Gemelli.** Il banco gemello ha lo stesso numero di messaggi nello stesso ordine e gli stessi `{STRVAR}` (J15). Dove la scena non si può rivedere dopo le dimissioni (flashback, risveglio, scena della madre) o l'oggetto è nascosto, il gemello è una **copia** del messaggio; per la gente comune e i Pokémon che restano è il testo di sei mesi dopo (R-10.6): chi è `CAPRO` dà la colpa al protagonista, chi è `ESTIMATORE` lo ringrazia. Mai messaggi inseriti in mezzo a un banco già consegnato (Modulo 1 §3): in fondo. |
| R-SCR-06 | **Scene.** Una scena che parte da sola (all'entrata in mappa) sta nell'intestazione dello script con `InitScriptEntry_OnFrameTable` e `InitScriptGoToIfEqual <variabile>, <valore>, _EV_scr_seq_<CODICE>_NNN + 1`; una scena che parte sul passo è un evento `coords` di zone_event con `var` e `val`. Ogni scena porta avanti la sua variabile alla fine (mai all'indietro, R-VAR-01). La variabile è la prima `VAR_TR_SCENE_<gruppo>_NN` libera del gruppo (R-VAR-03): questo blocco usa `VAR_TR_SCENE_CT_01`; **il prossimo blocco di CT parte da `VAR_TR_SCENE_CT_02`**. |
| R-SCR-07 | **Protagonista, ragazzo o ragazza** (R-GFX-37). Nei testi il protagonista non ha genere: niente aggettivi o participi riferiti a lui («stanco», «pronto»); si dà del tu, si usa il nome (`{STRVAR_1 3, 0, 0}`) o si gira la frase. Dove il genere serve davvero si scrivono due messaggi e si usa `GenderMsgBox <ragazzo>, <ragazza>` (qui solo il saluto di Graziella). |
| R-SCR-08 | **Lingua e area di ogni messaggio.** Ogni messaggio è `it` o `scn`, con l'area del Glossario (`CT` per la provincia di Catania). Un messaggio `scn` contiene solo parole del Glossario ammesse nell'area (J16); i personaggi che parlano in italiano (Catania «bene», narrazione, i Pokémon in scena) usano messaggi `it`; il siciliano entra con messaggi interi e brevi. Una parola nuova entra prima in `glossario_aggiunte` del blocco (id `G601-0001`…). Questo blocco non ne aggiunge. |
| R-SCR-09 | **Ancore dei warp.** `anchor` è l'indice, nella lista `warps` della mappa di destinazione, del warp dove si arriva. Se la mappa di destinazione la scrive un altro blocco, il blocco che per primo la nomina fissa l'indice in `ancore_attese` e il blocco della mappa lo rispetta (J11 controlla gli indici dentro il blocco). Per le mappe di HeartGold già esistenti vale l'indice di HeartGold. |
| R-SCR-10 | **Registro NPC.** Una riga per oggetto di zone_event (persone e Pokémon): coordinate, sprite, `hide_flag` = `eventFlag` (J12), `msg_index` = primo messaggio mostrato dallo script dell'oggetto. Persone senza nome (`POPOLO`) hanno `post_category` `CAPRO` o `ESTIMATORE`; il controllo 60/40 vale per provincia a fine modulo (qui 4 `CAPRO` e 2 `ESTIMATORE`: avviso per meno di 20 NPC). Un Pokémon in scena sta entro 2 caselle da una persona, ha sprite `SPRITE_FOLLOWER_MON_STATIC_<specie>` se esiste, altrimenti `SPRITE_FOLLOWER_MON_<specie>` (prova a schermo nel 7.4). |
| R-SCR-11 | **Caselle libere.** Le persone stanno su caselle raggiungibili: nel Cubbar le celle libere si leggono dalla cella costruita dal 4.2 (`build/grafica/4.2/celle/I_CT_MISTERBIANCO_CUBBAR_0.bin`, permessi); nelle stanze di HeartGold si tengono le coordinate degli oggetti originali o caselle libere vicine (§4). |
| R-SCR-12 | **Funzioni di HeartGold che restano.** La madre che tiene i risparmi (`FLAG_SYS_MOMS_SAVINGS`, menu preleva/deposita) resta con la stessa logica: Graziella è la «banca di famiglia» del protagonista. I nomi HeartGold dei flag (`FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL`, `FLAG_GOT_BAG`…) non si rinominano (R-FLAG-04). |
| R-SCR-13 | **Nuova partita.** Il discorso iniziale di HeartGold (`src/oaks_speech.c`, banco `msg_0219`: ragazzo o ragazza, nome del giocatore) **resta** e lo traduce la richiesta **6.00** (scaletta v2.24: tutta l’interfaccia, con il Prof. Strano al posto di Oak). Per questo M-CT-01 non rifà la «Scelta del nome» della trama: il nome si sceglie lì, prima del Prologo. La partita comincia nella camera (`MAP_CT_CATANIA_CASA_PROTAGONISTA_2F`, `src/location_backup.c`). |
| R-SCR-14 | **Riga finale.** Ogni blocco finisce con `BLOCCO COMPLETO: 6.NN - <conteggi>`; manca = blocco troncato (scaletta, introduzione). |
| R-SCR-15 | **Stato del blocco.** Dopo il blocco il registro NPC, i flag e le variabili usate sono nel JSON (`risorse`): serve al blocco successivo per sapere il prossimo simbolo libero (`risorse.prossimi_liberi`). |
"""

PROLOGO = """## 3. Il Prologo passo per passo

**Variabile di scena `VAR_TR_SCENE_CT_01`** (0x4079, gruppo CT del registro 2.4). Vale per M-CT-00 e M-CT-01, che non hanno variabili di missione.

| Valore | Significato | Chi lo imposta | Cosa parte con questo valore |
|---|---|---|---|
| 0 | nuova partita | (stato iniziale) | `OnFrame` della camera → script `T20R0202_002` (didascalia, dissolvenza, `Warp` nel Cubbar) |
| 1 | nel Cubbar, appena arrivati | `T20R0202_002` | `OnFrame` del Cubbar → script `T25SP0101_011` (arrivo: due messaggi) |
| 2 | nel Cubbar, libero | `T25SP0101_011` | evento `coords` sulla casella (16,23): `T25SP0101_012` («prima di uscire, due parole con Christian») e passo indietro |
| 3 | Christian ha parlato | `T25SP0101_000` | stesso `coords` con val 3: `T25SP0101_013` (didascalia finale, `FLAG_M_CT_00`, dissolvenza, `Warp` in camera) |
| 4 | flashback finito | `T25SP0101_013` | `OnFrame` della camera → script `T20R0202_003` (`ScrCmd_804 2`, ore 14:00, la voce della madre) |
| 5 | risveglio visto | `T20R0202_003` | `OnFrame` del piano terra → script `T20R0201_000` (la scena della madre) |
| 6 | M-CT-01 completata | `T20R0201_000` | nessuno (`FLAG_M_CT_01`, `VAR_TRINACRIA_ATTO` = 1) |

**La scena della madre** (`T20R0201_000`, in ordine): il giocatore scende e Graziella lo raggiunge (movimenti di HeartGold); saluto al maschile o al femminile (`GenderMsgBox`); lo zaino, la tessera, il tasto di salvataggio e le opzioni (`FLAG_GOT_BAG`, `FLAG_GOT_TRAINER_CARD`, `FLAG_GOT_SAVE_BUTTON`, `FLAG_GOT_OPTIONS_BUTTON`, ognuno con la fanfara); il **Pokégear** (`FLAG_GOT_POKEGEAR`: nel Prologo il telefono è il Pokégear, nota del registro 2.4), il piccolo tutorial del telefono con la scelta sì/no; Graziella dice dove andare (il Vermut); poi `FLAG_M_CT_01`, `VAR_TRINACRIA_ATTO` = 1, e torna al suo posto.

**Il Cubbar.** Christian è all'ingresso VIP (la porta nella fila del banco, casella (13,10)), col `Subwoofer` accanto; sei persone della movida stanno sulla pista (le sei caselle `pista_1…pista_6` del 4.2) e tre di loro hanno il loro Pokémon accanto. Nessuna lotta. Per uscire bisogna aver parlato con Christian (variabile 3): dopo, la casella davanti al tappeto d'uscita fa partire la dissolvenza. Dopo il Prologo Christian e il `Subwoofer` spariscono (`hide_flag` = `FLAG_M_CT_00`); le altre persone restano come clientela (il locale si rivede nel post-game, 6.38).
"""

RISORSE_INTRO = """## 5. Risorse usate

| Risorsa | Come si usa nel blocco |
|---|---|
"""

ANCORE = """## 6. Ancore attese (R-SCR-09)

| Da | Verso | Indice atteso | Chi lo rispetta |
|---|---|---|---|
| `MAP_CT_MISTERBIANCO_CUBBAR` (16,24) | `MAP_CT_MISTERBIANCO` | 0 | 6.07: nella lista `warps` di Misterbianco la porta del Cubbar (4.2: casella (1167,168)) è la prima |
| `MAP_CT_CATANIA_CASA_PROTAGONISTA_1F` (3,10) | `MAP_CT_CATANIA_CORSO_ITALIA` | 1 | 6.05: la porta della casa resta il secondo warp, come in HeartGold (`057_T20.json`, indice 1) |
| `MAP_CT_CATANIA_CASA_PROTAGONISTA_1F` (3,3) | `..._2F` | 0 | dentro il blocco: la scala della camera è il primo warp della 2F |
| `MAP_CT_CATANIA_CASA_PROTAGONISTA_2F` (3,4) | `..._1F` | 1 | dentro il blocco: la scala del piano terra è il secondo warp della 1F |

Le mappe esterne mandano in queste porte con i warp dei loro slot (4.2, sezione `collegamenti`): il primo piano della casa tiene i warp di HeartGold (4.2 §8).
"""

DECISIONI = """## 7. Decisioni da guardare

1. **La scelta del nome.** La trama mette «Scelta del nome» in M-CT-01; HeartGold la fa nel discorso iniziale (`src/oaks_speech.c`, `msg_0219`), prima di qualunque mappa. Ho tenuto il discorso e tolto la scelta da M-CT-01 (R-SCR-13): rifarla in camera obbligherebbe a cambiare il codice di avvio. **Deciso dall’autore dopo questo blocco:** il discorso iniziale e tutta l’interfaccia di HeartGold (menu, borsa, riepilogo, frasi di lotta, 408 banchi di sistema) si traducono in italiano con la richiesta **6.00**, da fare per prima (scaletta v2.24); a parlare sarà il Prof. Strano, e le immagini del discorso sono della richiesta 4.8. Finché il 6.00 non è applicato, la prima cosa che il giocatore legge è ancora in inglese.
2. **Ragazzo e ragazza.** I testi sono neutri (R-SCR-07); solo il saluto di Graziella cambia («Ben svegliato/svegliata»).
3. **Il Pokégear in M-CT-01**, non dopo lo starter come in HeartGold (registro 2.4, note): Graziella lo restituisce nella scena al piano terra; `ScrCmd_804 2` (R-GFX-33) sta nel primo script di M-CT-01, il risveglio in camera.
4. **I risparmi di Graziella** restano (R-SCR-12): è una funzione di HeartGold e, qui, una battuta sulla famiglia. Se non piace, basta togliere gli script `_madre_*` e `FLAG_SYS_MOMS_SAVINGS`.
5. **Clientela del Cubbar.** Le sei persone restano nel locale dopo il Prologo, con gli stessi discorsi (nessun testo parla di «stanotte»); Christian e il `Subwoofer` spariscono con `FLAG_M_CT_00`. La porta del Cubbar a Misterbianco è del 6.07.
6. **60/40 provvisorio:** 4 `CAPRO` e 2 `ESTIMATORE` su 6 persone. I blocchi di CT successivi riportano il rapporto verso 60/40.
7. **Persone create:** il figlio e la figlia d'avvocato e di magistrato, il praticante, il PR e il figlio dell'imprenditore del Cubbar sono tipi inventati, senza nome e senza reati (R-05); `Lombardo`, citato dalla trama, è un avvocato inventato.
8. **Sprite generici** (`SPRITE_GORGGEOUSM`, `_GORGGEOUSW`, `_ASSISTANTM`, `_SUNGLASSES`, `_LADY`, `_BADMAN`): tipi di HeartGold senza ruolo fisso nei registri; se nel 7.4 non rendono, si cambia solo lo sprite (J12 poi lo ricontrolla).
"""

PROVE = """## 8. Prove (per il Modulo 7, blocco 7.5)

| Prova | Criterio |
|---|---|
| Nuova partita | dopo il discorso iniziale si è in camera; si legge «Qualche ora prima. Misterbianco, il Cubbar.» e si arriva nel Cubbar sulla casella (16,22) |
| Uscita chiusa | camminare fino al tappeto senza parlare con Christian: si legge «Prima di uscire, due parole con Christian…» e il personaggio fa un passo indietro |
| Christian | parlare con lui: cinque messaggi in catena (il primo e l'ultimo in siciliano); poi di nuovo: un messaggio solo |
| Pokémon in scena | `Subwoofer`, `Gattupardu`, `Novicudi`, `Diavulazzu` rendono (sprite dinamici: `Exploud`, `Ninetales`, `Houndoom`); verso e messaggio a ogni interazione |
| Uscita | dopo Christian la casella (16,23) fa partire il messaggio finale, la dissolvenza e il ritorno in camera: «Ore 14:00» |
| Risveglio | scatta una volta sola; il Pokégear ha il livello 2 della mappa (Est e Ovest) |
| Scena della madre | scendendo la scala parte da sola: tre fanfare (zaino, tessera, salvataggio, opzioni), Pokégear, domanda sul telefono (sì e no danno due messaggi diversi), poi si è liberi; `FLAG_M_CT_01` e `VAR_TRINACRIA_ATTO` = 1 |
| Risparmi | prima dello starter Graziella dice di andare dal Vermut; con `FLAG_GOT_STARTER` propone i risparmi e poi il menu (preleva, deposita, cambia, esci) |
| Gemelli | con `FLAG_POST_RESIGNATION` ogni messaggio mostra il testo del gemello; la casa e il Cubbar mostrano i testi di sei mesi dopo |
| Salvataggio nel Cubbar | ricaricare un salvataggio con la variabile a 2 non rifà la scena di arrivo |
"""

NOTE = """## 9. Note per gli altri blocchi

- **6.02:** la scena del Vermut comincia con `VAR_M_CT_02` = 0; il Pokégear e il livello della mappa sono già a posto. Il Consenso parte da 1 in M-CT-02 (registro 2.4).
- **6.05:** `MAP_CT_CATANIA_CORSO_ITALIA` tiene la porta della casa come secondo warp (ancora attesa) e il cartello `E-CT-05`; in HeartGold lo slot ha gli eventi di Elm e del rivale: vanno tolti nello stesso blocco.
- **6.07:** `MAP_CT_MISTERBIANCO` tiene la porta del Cubbar come primo warp (ancora attesa); la porta si apre sempre (il Cubbar è un locale, non un luogo chiuso), ma Christian non c'è più.
- **6.38:** il Ritrovo di Christian (`P-01`) mette nuovi oggetti nello stesso locale (altri `obj_…`, `hide_flag` = `FLAG_TR_HIDE_POSTGAME`).
- **Tutti:** prossimo `VAR_TR_SCENE_CT_02`; nessun flag di visibilità `FLAG_TR_HIDE_CT_*` consumato; prossimo numero libero dei banchi gemelli e delle matrici come nel blocco 2.1 (non cambia).
"""

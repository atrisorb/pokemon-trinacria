"""Testi scritti a mano del blocco 5.1 (gen51.py li unisce alle tabelle calcolate)."""

VERSIONE = '1.0'
DATA = '27/10/2026'

INTESTAZIONE = """# Modulo 5 · Blocco 5.1 — Pipeline MIDI→SSEQ, banchi SBNK e suoni da mantenere

**Versione:** {versione} · {data} · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** `F:\\Progetti\\pokeheartgold`

**File del blocco:**

| File | Cosa contiene |
|---|---|
| `docs/MODULO_5/5.1_PIPELINE_E_SFX.md` | questo documento |
| `docs/MODULO_5/5.1_BANCHI_SBNK.json` | catalogo generato: i 60 programmi comuni, i programmi propri dei {n_banchi} banchi musicali, l’uso che ne fa HeartGold, i {n_slot} slot delle musiche e i suoni da mantenere |
| `tools/trinacria_audio.py` | lo strumento: legge e riscrive l’archivio audio, converte MIDI→SSEQ, controlla |
| `tools/music/componi.py` | trasforma le partiture Python dei blocchi 5.2–5.4 in file MIDI e nel manifesto |
| `tools/music/prova_5_1.py`, `tools/music/prova/SEQ_CT_CORSO_ITALIA.py` | script di prova della pipeline intera (la partitura è **solo di prova**) |
| `tools/generatori/5.1/` | generatore di questo documento e del catalogo (`gen51.py`, `text51.py`) |

Fonti lette nel repository: `files/data/sound/gs_sound_data.sdat` (SHA-1 `{sha1}`), `files/data/sound/meson.build`, `include/constants/sndseq.h`, `include/sound.h`, `src/sound.c`, `asm/unk_02004A44.s` (tabella dei gemelli «suoni GB»), `src/field/field_control.c` (piastre sonore), `asm/macros/script.inc`, gli script di campo `files/fielddata/script/scr_seq/` e il registro `docs/MODULO_2/2.5_TRAINERS_SPRITES_FLY_SEQ.json` (sezione `musiche`)."""

IN_BREVE = """## 0. In breve

- **L’archivio audio non si compila da sorgenti.** `files/data/sound/meson.build` copia `gs_sound_data.sdat` ({sdat_byte} byte) così com’è nella ROM. Trinacria lo **riscrive**: ogni brano nuovo prende il posto dei dati di uno slot `SEQ_GS_*` e del suo gemello `SEQ_GS_P_*`, e tutto il resto resta identico byte per byte.
- **Strumento scelto: `tools/trinacria_audio.py`**, scritto per Trinacria, solo libreria standard di Python (nessuna installazione). Alternative scartate: in questo ambiente non c’è nessuna libreria audio (`mido`, `midiutil`, `ndspy` assenti), e gli strumenti grafici per Windows (Nitro Studio, VGMTrans, i convertitori dello SDK Nintendo) non danno un esito PASS/FAIL che l’esecutore possa controllare. Lo strumento fa ogni passo con un comando e chiude con `AUDIO_OK` o `AUDIO_FAILED`.
- **Collaudato su tutto l’archivio di HeartGold** (`python -I tools/trinacria_audio.py --selftest` → `SELFTEST_OK`): l’archivio letto e riscritto è identico all’originale; {n_rt} sequenze su {n_rt} passate da SSEQ a MIDI e di nuovo a SSEQ suonano le stesse note, gli stessi controlli e lo stesso ritornello; le musiche riconvertite pesano in mediana l’{rapporto}% degli originali; la tabella dei {n_gemelli} gemelli e i {n_nomi} nomi di `sndseq.h` corrispondono all’archivio; i {n_codici} codici d’errore scattano tutti sul manifesto di prova sbagliato.
- **Slot e gemelli.** I {n_slot} brani del registro 2.5 sostituiscono {n_slot} slot HeartGold e i loro {n_gemelli_slot} gemelli «suoni GB» (gli altri {n_senza_gemello} slot non ne hanno). **{n_condivisi} slot del registro condividono il file dei dati con un altro slot**: lo strumento dà a ogni brano un file proprio (R-AUD-03), quindi nessun’altra musica cambia per sbaglio.
- **Banchi.** I {n_banchi} banchi musicali (`BANK_BASIC` e `BANK_BGM_*`) hanno identici i **programmi 0–59** (la tavolozza comune) e aggiungono da 0 a 8 programmi propri dal 60 in su. Un brano può usare qualsiasi banco musicale (R-AUD-05).
- **Limiti.** {canali} canali per brano ({psg} PSG e {rumore} di rumore); sul lettore delle mappe la sequenza sta in **{heap_field} byte**; il carico (sequenza + banco + onde) non supera quello che HeartGold già carica sullo stesso lettore (R-AUD-06).
- **Suoni da mantenere al 100%.** Effetti (`SEQ_SE_*`), jingle (`SEQ_ME_*`), versi dei Pokémon, banchi, onde e le musiche fuori dal registro non cambiano: `controlla` lo verifica file per file (codice A20). Il Modulo 6 usa negli script di campo i {n_se_campo} effetti e le {n_fanfare} fanfare che HeartGold già suona sul campo (R-AUD-09), la tavolozza dell’Orecchio di Dionisio (R-AUD-10) e i {n_piastre} suoni d’ambiente delle piastre sonore (R-AUD-11)."""

STRUMENTO = """## 1. Lo strumento `tools/trinacria_audio.py`

Si lancia dalla cartella del progetto o del repository; `--repo` indica `F:\\Progetti\\pokeheartgold` (senza, lo strumento lo cerca nella cartella corrente, nella variabile `TRINACRIA_REPO` e accanto al progetto). Ogni problema è una riga `ERRORE <codice> <messaggio>`; l’ultima riga è `AUDIO_OK`/`AUDIO_FAILED` (o `SELFTEST_OK`/`SELFTEST_FAILED`).

| Comando | Cosa fa |
|---|---|
| `--selftest [--repo R]` | collaudo completo (circa 3 minuti): archivio identico, gemelli, nomi, andata e ritorno di tutte le sequenze, brano di prova, `applica` e `controlla` su slot con file condiviso e su uno slot di lotta, manifesto con 12 errori voluti |
| `info` | conteggi dell’archivio e limiti dei lettori delle musiche |
| `slot SEQ_X …` | file, byte, banco, volume, lettore, gemello, ritornello e tracce di uno slot |
| `banco BANK_X …` | strumenti di un banco (tipo, zone di tasti, onde) |
| `mid2sseq IN.mid OUT.sseq` | conversione MIDI→SSEQ con i controlli della convenzione (§5) |
| `sseq2mid SEQ_X OUT.mid` | sequenza HeartGold → MIDI, per studiarla o ascoltarla in un programma qualsiasi |
| `txt SEQ_X` oppure `txt IN.sseq` | disassemblato della sequenza (comandi, etichette, tracce) |
| `onde BANK_X --out DIR` | scrive in WAV le onde del banco, per ascoltare gli strumenti |
| `catalogo --out F.json` | catalogo completo dei banchi (una voce per banco, programmi comuni ripetuti) |
| `applica --manifesto M [--hg ORIG] [--out F]` | costruisce l’archivio di Trinacria dall’originale e dal manifesto (default: scrive `files/data/sound/gs_sound_data.sdat` del repository) |
| `controlla [--sdat F] [--manifesto M] [--hg ORIG]` | confronta l’archivio con l’originale: fuori dagli slot del manifesto tutto deve essere identico |

Cosa sa fare dentro, in breve: legge i blocchi SYMB, INFO, FAT e FILE dell’archivio (SYMB e INFO restano byte per byte, le voci INFO si correggono sul posto; FAT e FILE si riscrivono con l’allineamento a 32 byte di HeartGold e possono crescere in coda); esegue ogni sequenza SSEQ (note, attese, `call`/`ret`, `loop`, salti, variabili, prefissi `random`/`var`/`if`) fino al ritornello; scrive SSEQ da MIDI raccogliendo in sottoprogrammi (`call`/`ret`, un solo livello) le serie di comandi ripetute; legge i banchi SBNK (strumenti semplici, a zone di tasti, batterie, PSG, rumore) e le onde SWAR (PCM8, PCM16, IMA-ADPCM)."""

COLLAUDO = """## 2. Collaudo

Esito del {data} con `python -I tools/trinacria_audio.py --selftest --repo F:/Progetti/pokeheartgold`:

| Prova | Esito |
|---|---|
| Archivio letto e riscritto senza modifiche | identico all’originale ({sdat_byte} byte, SHA-1 `{sha1}`) |
| Gemelli «suoni GB» (`asm/unk_02004A44.s`) | {n_gemelli} coppie su {n_gemelli}: la regola del nome (`SEQ_GS_X` → `SEQ_GS_P_X`, `SEQ_PL_X` → `SEQ_PL_P_X`) dà sempre il gemello della tabella |
| Nomi di `include/constants/sndseq.h` | {n_nomi} su {n_nomi} hanno una voce nell’archivio con lo stesso numero; {n_alias} ha un nome diverso nel blocco SYMB (`SEQ_SE_DP_THROW` = `SEQ_SE_DP_NAGERU`, rinominato dal decomp): lo strumento accetta tutti e due |
| Andata e ritorno SSEQ → MIDI → SSEQ | {n_rt} sequenze su {n_rt} (musiche, gemelli, effetti, jingle, versi): stesse note (tempo, tasto, velocità, durata, programma), stessi controlli, stessi tempi e stesso ritornello. Una sola sequenza non si confronta: `SEQ_GS_P_SAFARI_ROAD` (gemello GB) ha ritornelli diversi per traccia, che un MIDI con due marcatori non rappresenta |
| Peso delle sequenze riconvertite (musiche) | mediana {rapporto}% dell’originale, massimo {rapporto_max}%; la musica di campo più pesante riconvertita è di {campo_max} byte, sotto i {heap_field} dell’heap. Senza i sottoprogrammi (§1) `SEQ_GS_GAME` passerebbe da 11 268 a 20 236 byte |
| Brano di prova (MidiWriter, ppq 96) | note e ritornello identici a quelli scritti |
| `applica` su `SEQ_GS_C_NIBI` + `SEQ_GS_C_YAMABUKI` (stesso file di `SEQ_GS_C_TOKIWA`) e `SEQ_GS_VS_TRAINER` | due file distinti, `SEQ_GS_C_TOKIWA` invariato, gemelli sul file del brano col banco del brano, risultato identico a ogni esecuzione, `controlla` superato |
| `controlla` su un archivio con un effetto cambiato | trovato (A20) |
| Manifesto con errori voluti | A01–A12 tutti trovati, nessun archivio scritto; archivio di partenza diverso dall’originale rifiutato (A22) |

Lo script `python -I tools/music/prova_5_1.py --out <cartella>` rifà la pipeline intera con la partitura di prova: {prova}

**Non provato qui:** l’ascolto in gioco. In questo ambiente la ROM non si compila (i sottoprogetti Nitro di `pokeheartgold` non sono scaricati); la prova d’ascolto nell’emulatore è un TASK del blocco 7.3 (§12)."""

PIPELINE = """## 3. La pipeline, passo per passo

| Passo | Chi | Comando | Esito atteso |
|---|---|---|---|
| 1. Partitura | blocchi 5.2–5.4 | un file `tools/music/<blocco>/<SIMBOLO>.py` per brano (formato in R-AUD-12) | — |
| 2. Composizione | esecutore (7.3) | `python -I tools/music/componi.py` | `build/musica/<SIMBOLO>.mid` e `build/musica/manifesto.json`, `COMPONI_OK` |
| 3. Originale | esecutore, **una volta** | copia di `files/data/sound/gs_sound_data.sdat` in `files/data/sound/gs_sound_data_hg.sdat` (R-AUD-02) | SHA-1 `{sha1}` |
| 4. Archivio di Trinacria | esecutore | `python -I tools/trinacria_audio.py applica --repo F:/Progetti/pokeheartgold --manifesto build/musica/manifesto.json` | una riga per brano, `AUDIO_OK`; scrive `files/data/sound/gs_sound_data.sdat` |
| 5. Controllo | esecutore | `python -I tools/trinacria_audio.py controlla --repo F:/Progetti/pokeheartgold --manifesto build/musica/manifesto.json` | `AUDIO_OK` |
| 6. ROM e ascolto | esecutore (7.3) | build e emulatore | ogni mappa suona il suo brano (registro 2.5) |

I passi 2, 4 e 5 si rifanno da capo a ogni partitura nuova o cambiata: `applica` riparte sempre dall’originale, quindi l’ordine dei blocchi 5.2–5.4 non conta e il risultato è sempre lo stesso. Dove copiare strumento e partiture dentro `pokeheartgold` (come per gli altri strumenti in `tools/trinacria/`) lo decide il blocco 7.3."""

REGOLE = [
    ('R-AUD-01', 'Pipeline unica',
     'Ogni musica di Trinacria nasce da una partitura Python che scrive un MIDI con `MidiWriter` di `tools/trinacria_audio.py`; `componi.py` produce i MIDI e il manifesto; `applica` li converte in SSEQ e li mette nell’archivio. Nessun altro programma scrive in `gs_sound_data.sdat`.'),
    ('R-AUD-02', 'Archivio originale',
     'L’originale di HeartGold (SHA-1 `{sha1}`) si copia una volta in `files/data/sound/gs_sound_data_hg.sdat` e non si modifica mai. `meson.build` non lo elenca, quindi non entra nella ROM. `applica` parte sempre da lui e rifiuta qualsiasi altro archivio di partenza (A22).'),
    ('R-AUD-03', 'Slot, gemello e file propri',
     'Un brano sostituisce lo slot `SEQ_GS_*` del registro 2.5 e il suo gemello `SEQ_GS_P_*`: i due puntano allo stesso file nuovo, con lo stesso banco e lo stesso volume. Lo strumento sceglie il file così: il file dello slot se nessun’altra voce lo usa più, altrimenti quello del gemello, altrimenti il primo file liberato, altrimenti un file nuovo in coda. Gli altri slot che condividevano il file (§8) restano com’erano. Il gemello suona solo con lo strumento chiave `Sunaturi` (GB Sounds), che in Trinacria non si ottiene (3.12): il gioco cambia sequenza ricominciando il brano, quindi il gemello non deve restare a tempo con lo slot.'),
    ('R-AUD-04', 'Convenzione MIDI',
     'MIDI di tipo 0 o 1, qualsiasi risoluzione (si arrotonda a 48 tick per semiminima). Un canale MIDI usato = una traccia SSEQ, in ordine di canale (al massimo 16). Tempo dai meta-eventi; programma = `CC0 × 128 + Program Change`; pitch bend e controller come nella tabella del §5; nessun altro controller (A12). Il ritornello è la coppia di marcatori `loopStart` e `loopEnd` (meta-evento Marker o Text), obbligatoria se lo slot HeartGold si ripete e vietata se non si ripete (A10). Le note con velocità 0 non esistono (sono fine nota), la durata minima è 1 tick. Nessun SysEx.'),
    ('R-AUD-05', 'Banchi',
     'Il brano usa un banco musicale qualsiasi (`BANK_BASIC` o `BANK_BGM_*`, A03); senza indicazione tiene il banco dello slot HeartGold. I programmi 0–59 sono uguali in tutti i banchi (§9.2); i programmi propri (60 e oltre) esistono solo nel loro banco. Ogni nota deve cadere su un programma non vuoto e su una zona di tasti definita (per le batterie: un tasto della batteria), altrimenti non suona (A05). `BANK_GAMEBOY` resta ai gemelli HeartGold non sostituiti.'),
    ('R-AUD-06', 'Limiti del lettore',
     'Ogni slot suona sul lettore che HeartGold gli dà (`PLAYER_FIELD` per le musiche delle mappe, `PLAYER_BGM` per lotte, incontri, eventi). Per brano: al massimo {canali} note insieme (A06), di cui {psg} PSG e {rumore} di rumore (A07); le note si contano per la loro durata scritta, senza la coda di rilascio. I brani HeartGold del registro arrivano fino a {poly_hg_max} note insieme e il gioco toglie il canale alla nota meno importante: Trinacria resta entro {canali} per non perdere note; su `PLAYER_FIELD` la sequenza sta in {heap_field} byte (heap del lettore, A08); sequenza + banco + onde non superano il carico massimo che HeartGold già usa sullo stesso lettore (A09: {carico_field} byte su `PLAYER_FIELD`, {carico_bgm} su `PLAYER_BGM`).'),
    ('R-AUD-07', 'Volume',
     'Il volume della voce INFO (0–127, A04) è quello dello slot HeartGold se la partitura non dà `VOLUME`; il volume di ogni traccia è il CC7. Il gemello prende lo stesso volume.'),
    ('R-AUD-08', 'Suoni da mantenere al 100%',
     'Fuori dagli slot del manifesto e dai loro gemelli niente cambia: effetti `SEQ_SE_*`, jingle `SEQ_ME_*`, versi `SEQ_PV*` coi loro {n_pv_arc} archivi d’onda, tutti i banchi e le onde, gruppi, lettori e le musiche HeartGold che il registro non usa. `controlla` confronta ogni voce e ogni file con l’originale (A20).'),
    ('R-AUD-09', 'Suoni negli script di campo',
     'Gli script del Modulo 6 usano sul campo solo i {n_se_campo} effetti `PlaySE` e le {n_fanfare} fanfare `PlayFanfare` del §10.2–10.3, che HeartGold già suona negli script di campo (quindi con banco e onde caricati), e `PlayCry` con qualsiasi specie. Un effetto fuori elenco si usa solo dopo una prova nell’emulatore registrata dal Modulo 7. Il jingle `SEQ_ME_BADGE` è quello del Dossier ottenuto.'),
    ('R-AUD-10', 'Orecchio di Dionisio (S-SR-02)',
     'Il minigioco dell’eco usa i quattro suoni del §10.5, in quest’ordine di scelta; ogni suono si attende prima del successivo (`WaitCry` per i versi, `WaitSE` per gli effetti). La lunghezza delle sequenze e i dialoghi li scrive il Modulo 6.'),
    ('R-AUD-11', 'Suoni d’ambiente',
     'I {n_piastre} suoni delle piastre sonore (§10.6) restano invariati. Le piastre sono nei dati del terreno di ogni blocco di mappa 32×32 (`sub_02054874`); quali mappe di Trinacria le hanno lo decidono il Modulo 4 (dati delle mappe) e il Modulo 7. Uno script può anche suonare uno di questi suoni con `PlaySE` e fermarlo con `StopSE` (gli script di campo di HeartGold fermano così un suono d’ambiente {n_stopse} volte).'),
    ('R-AUD-12', 'Formato delle partiture (5.2–5.4)',
     'Un file `tools/music/<blocco>/<SIMBOLO>.py` per brano, dove `<SIMBOLO>` è l’alias del registro 2.5 (`SEQ_CT_VERMUT`…), con `SIMBOLO`, facoltativi `BANCO` e `VOLUME`, e la funzione `partitura(A)` che restituisce un `A.MidiWriter`. Esempio completo: `tools/music/prova/SEQ_CT_CORSO_ITALIA.py`. `componi.py` controlla nome, simbolo e doppioni (C01–C04). Le partiture usano `MidiWriter` e non `midiutil`, che qui non è installato.'),
    ('R-AUD-13', 'Sequenze più lunghe del previsto',
     'Se `applica` rifiuta un brano per A08 o A09, la partitura si accorcia o ripete di più le stesse battute (le ripetizioni diventano sottoprogrammi e costano 4 byte l’una): non si cambia lettore né si toglie spazio ad altri slot.'),
    ('R-AUD-14', 'Nessuna sequenza in più',
     'Il numero delle sequenze non cambia: un brano nuovo sta sempre su uno slot HeartGold del registro 2.5 (A01 per uno slot che non è una musica `SEQ_GS_*`, A11 per uno slot usato due volte). La FAT può crescere solo per i file propri di R-AUD-03.'),
]

CONVENZIONE = """## 5. Convenzione MIDI ↔ SSEQ

Valori grezzi 0–127 (il gioco li applica con le sue tabelle). La tabella vale nei due versi: `sseq2mid` scrive i comandi dei brani HeartGold con gli stessi controller, quindi un brano esportato e riconvertito torna identico (§2).

| MIDI | Comando SSEQ | Note |
|---|---|---|
| Note On / Note Off | nota (`0x00–0x7F`, velocità, durata) | durata = distanza fra inizio e fine, minimo 1 tick |
| meta Tempo (`FF 51`) | `0xE1` tempo (BPM) | sempre sulla traccia 0 |
| marcatori `loopStart` / `loopEnd` | etichetta + `0x94` salto | ritornello comune a tutte le tracce |
| CC0 + Program Change | `0x81` programma | programma SBNK = CC0 × 128 + PC |
| Pitch bend | `0xC4` (−128…127) | 64 unità MIDI = 1 passo |
| RPN 0 (CC101 = 0, CC100 = 0, CC6) | `0xC5` ampiezza del bend (semitoni) | |
| CC1 | `0xCA` profondità della modulazione | |
| CC5 | `0xCF` tempo del portamento | |
| CC7 | `0xC1` volume della traccia | |
| CC10 | `0xC0` pan (64 = centro) | |
| CC11 | `0xD5` espressione | |
| CC16 / CC17 / CC18 | `0xCB` velocità / `0xCC` tipo / `0xCD` ampiezza della modulazione | |
| CC19 + CC51 (14 bit) | `0xE0` ritardo della modulazione | MSB poi LSB |
| CC20 | `0xC6` priorità della traccia | |
| CC21 | `0xC2` volume principale | |
| CC22 + CC54 (14 bit, centro 8192) | `0xE3` sweep di altezza | MSB poi LSB |
| CC65 | `0xCE` portamento acceso/spento | |
| CC68 | `0xC8` legato (tie) | |
| CC72 / CC73 / CC75 / CC79 | `0xD3` rilascio / `0xD0` attacco / `0xD1` decadimento / `0xD2` sostegno | sostituiscono l’inviluppo dello strumento |
| CC84 | `0xC9` nota di partenza del portamento | |

Ogni traccia scritta da `mid2sseq` comincia con `0xC7 0` (le note non fermano la traccia), come le musiche di HeartGold; le attese sono comandi `0x80`. Controller ignorati senza errore: 32, 38, 98, 99, 121, 123."""

# Significato degli effetti (dal nome giapponese), solo dove è sicuro.
SIGNIFICATO_SE = {
    'SEQ_SE_DP_SELECT': 'selezione nei menu', 'SEQ_SE_DP_KAIDAN2': 'scale', 'SEQ_SE_DP_REGI': 'cassa del negozio',
    'SEQ_SE_GS_RAKKA01': 'caduta', 'SEQ_SE_GS_ZENIGAME_JOURO': 'annaffiatoio Squirtle',
    'SEQ_SE_GS_SUZUNOONPA2': 'onda del suono della campana', 'SEQ_SE_DP_PINPON': 'campanello «pin-pon»',
    'SEQ_SE_GS_SUZUNOONPA_RU': 'onda del suono della campana', 'SEQ_SE_DP_SAVE': 'salvataggio',
    'SEQ_SE_GS_DENKI_TRAP': 'trappola elettrica', 'SEQ_SE_DP_JIHANKI': 'distributore automatico',
    'SEQ_SE_DP_WALL_HIT2': 'urto contro un ostacolo', 'SEQ_SE_GS_AJITO_SIREN': 'sirena del covo',
    'SEQ_SE_GS_DOKU_TRAP': 'trappola velenosa', 'SEQ_SE_GS_IWA_TRAP': 'trappola di massi',
    'SEQ_SE_GS_PHONE0': 'squillo del Pokégear', 'SEQ_SE_DP_DECIDE': 'conferma', 'SEQ_SE_DP_DOOR10': 'porta',
    'SEQ_SE_GS_TIMESLIP': 'viaggio nel tempo', 'SEQ_SE_GS_ZUKAN06': 'Pokédex',
    'SEQ_SE_GS_KI_UGOKU': 'albero che si muove', 'SEQ_SE_DP_KON': 'colpo secco (bussare)',
    'SEQ_SE_DP_PC_LOGIN': 'accesso al PC', 'SEQ_SE_GS_OKOZUKAI': 'denaro ricevuto', 'SEQ_SE_DP_WALL_HIT': 'urto contro un ostacolo',
    'SEQ_SE_DP_PC_ON': 'accensione del PC', 'SEQ_SE_DP_DOOR': 'porta', 'SEQ_SE_DP_DENSI01': 'suono elettronico',
    'SEQ_SE_DP_CARD2': 'carta', 'SEQ_SE_GS_TAMASYUTUGEN': 'comparsa della sfera',
    'SEQ_SE_GS_N_LINEAR': 'ambiente del treno magnetico', 'SEQ_SE_GS_KUJI_ATARI': 'vincita alla lotteria',
    'SEQ_SE_DP_GYURU': 'giro', 'SEQ_SE_DP_PC_LOGOFF': 'uscita dal PC', 'SEQ_SE_GS_ZUTUKI': 'Bottintesta',
    'SEQ_SE_GS_SUZUSYUTUGEN_HO': 'comparsa della campana', 'SEQ_SE_GS_SUZUSYUTUGEN_RU': 'comparsa della campana',
    'SEQ_SE_GS_IWAOTOSHI01': 'masso che cade', 'SEQ_SE_GS_IWAOTOSHI02': 'masso che cade',
    'SEQ_SE_GS_N_UMIBE': 'riva del mare', 'SEQ_SE_DP_SHIP03': 'nave', 'SEQ_SE_GS_TAKI2': 'cascata',
    'SEQ_SE_GS_KUJI_OOATARI': 'gran vincita alla lotteria', 'SEQ_SE_DP_BUTTON9': 'pulsante',
    'SEQ_SE_PL_KIRAKIRA': 'scintillio',
}

SIGNIFICATO_ME = {
    'SEQ_ME_ASA': 'riposo e cura', 'SEQ_ME_LVUP': 'aumento di livello', 'SEQ_ME_ITEM': 'strumento ricevuto',
    'SEQ_ME_KEYITEM': 'strumento chiave ricevuto', 'SEQ_ME_POKEGET': 'Pokémon ricevuto',
    'SEQ_ME_SHINKAOME': 'evoluzione riuscita', 'SEQ_ME_BADGE': 'medaglia → **Dossier ottenuto**',
    'SEQ_ME_WAZA': 'mossa imparata', 'SEQ_ME_ACCE': 'accessorio', 'SEQ_ME_WASURE': 'mossa dimenticata',
    'SEQ_ME_KINOMI': 'bacca', 'SEQ_ME_TAMAGO_GET': 'uovo ricevuto', 'SEQ_ME_POKEGEAR_REGIST': 'numero registrato nel Pokégear',
    'SEQ_ME_MUSHITORI1': 'premio della gara di cattura', 'SEQ_ME_MUSHITORI2': 'premio della gara di cattura',
    'SEQ_ME_MUSHITORI3': 'premio della gara di cattura', 'SEQ_ME_CARDGAME1': 'gioco di carte',
    'SEQ_ME_CARDGAME2': 'gioco di carte', 'SEQ_ME_BPGET': 'Punti Lotta ricevuti',
    'SEQ_ME_HYOUKA1': 'valutazione del Pokédex', 'SEQ_ME_HYOUKA2': 'valutazione del Pokédex',
    'SEQ_ME_HYOUKA3': 'valutazione del Pokédex', 'SEQ_ME_HYOUKA4': 'valutazione del Pokédex',
    'SEQ_ME_HYOUKA5': 'valutazione del Pokédex', 'SEQ_ME_HYOUKA6': 'valutazione del Pokédex',
}

# Suoni d'ambiente: proposte di uso in Trinacria (le decidono Moduli 4, 6 e 7).
PIASTRE_USO = {
    'WATER_FLOW': 'ruscelli e fiumi',
    'WINDMILL': 'mulini a vento',
    'SEASHORE': 'lungomari e spiagge',
    'PILLAR': '—',
    'WHIRLPOOL': 'Stretto di Messina (Scilla e Cariddi)',
    'WATERFALL': 'cascate',
    'LAVA': 'crateri dell’Etna e Sciara del Fuoco',
    'CHEERS': 'stadio, comizi, piazze in festa',
    'STEAM_WHISTLE': 'porti e traghetti',
    'SNORLAX_SNORING': '`Manzuni` (Snorlax) statico su viale Regione Siciliana',
    'MOTOR': 'Polo petrolchimico, fabbriche',
    'BELLS': 'campanili e chiese',
    'STRONG_WIND': 'Capaci, Grande Cretto, vento di Trapani',
    'ENGINE': 'stazioni, Circumetnea',
    'FOUNTAIN': 'fontane di piazza',
    'ELECTRIC_BARRIER': 'barriere dei covi di «U Sistema»',
}

TAVOLOZZA_ECO = [
    ('1', 'verso di `Taddarita` (Zubat)', '`PlayCry SPECIES_ZUBAT, 0` poi `WaitCry`'),
    ('2', 'verso di `Tammureddu` (Whismur)', '`PlayCry SPECIES_WHISMUR, 0` poi `WaitCry`'),
    ('3', 'colpo secco sulla roccia', '`PlaySE SEQ_SE_DP_KON` poi `WaitSE SEQ_SE_DP_KON`'),
    ('4', 'rintocco «pin-pon»', '`PlaySE SEQ_SE_DP_PINPON` poi `WaitSE SEQ_SE_DP_PINPON`'),
]

NOTE_BLOCCHI = """## 12. Note per gli altri blocchi

- **5.2–5.4 (partiture).** Ogni brano è un file di R-AUD-12; per sentire uno strumento prima di sceglierlo: `python -I tools/trinacria_audio.py onde BANK_BGM_FIELD1 --out <cartella>` (WAV) o `sseq2mid` di un brano HeartGold che lo usa (colonne «Brani HG» e «Registro» del §9.2; l’elenco dei brani è nel catalogo JSON, `tavolozza_comune` e `banchi`). La scaletta (v2.12) dice ora `MidiWriter` al posto di `midiutil` nella riga del 5.2.
- **5.3–5.4 (vento di Capaci e del Grande Cretto).** Gli slot `SEQ_PA_CAPACI_MEMORIA` e `SEQ_TP_CRETTO_VENTO` restano sequenze del registro 2.5 (il Modulo 1 §10 citava un `SEQ_CAPACI_WIND_SILENCE` che il registro non ha: è stato allineato, v1.6). Il vento si può scrivere coi programmi di rumore 53 e 54 della tavolozza comune (un canale di rumore per brano, R-AUD-06) oppure lasciare la sequenza quasi muta e affidare il vento al suono d’ambiente `SEQ_SE_GS_KYOUHUU` (§10.6), suonato da piastra o da script.
- **Modulo 4.** Le piastre sonore (R-AUD-11) sono nei dati del terreno delle mappe; l’icona del vagante resta come annotato nel 3.3.
- **Modulo 6.** R-AUD-09 (effetti di campo), R-AUD-10 (Orecchio di Dionisio). La trasmissione radio del Team Rocket suona `SEQ_GS_SENKYO_R` (`src/application/pokegear/radio/shows/team_rocket.c`), che in HeartGold divide il file con `SEQ_GS_SENKYO`: dopo `applica` resta il brano HeartGold, mentre `SEQ_GS_SENKYO` diventa `SEQ_EN_PIAZZA_ARMERINA_FINALE`. Se la radio va tenuta in Trinacria, il Modulo 6 decide se rimapparla. Le varianti `SEQ_GS_*_PHC` (Pokéwalker) restano HeartGold.
- **Modulo 7 (blocco 7.3).** TASK: copia dell’originale (R-AUD-02), copia di `tools/trinacria_audio.py` e `tools/music/`, `--selftest`, `componi.py`, `applica`, `controlla`, build, e la prova d’ascolto nell’emulatore di almeno uno slot di `PLAYER_FIELD`, uno di `PLAYER_BGM` e uno degli slot col file condiviso del §8 (per esempio `SEQ_GS_C_NIBI`, `SEQ_GS_C_YAMABUKI` e `SEQ_GS_C_TOKIWA` in tre mappe diverse).
- **Blocco 3.12.** Il testo di `Sunaturi` (502, `ottenimento.altro`) diceva «le musiche del Modulo 4»: ora dice Modulo 5. Il 3.12 non era ancora nel repository, quindi resta alla v1.0 (cambia solo quella riga)."""

"""Testi fissi del blocco 4.4 (documento docs/MODULO_4/4.4_UI_TITOLO_POKEGEAR.md)."""

DATA = '28/10/2026'
REGIONI_JSON = {
    'regola': 'R-GFX-33',
    'est': {'lato_motore': 'POKEGEAR_REGION_KANTO / MAP_REGION_KANTO', 'colonne': '24–46', 'nome': 'Est',
            'messaggio': 'msg_0273_00000'},
    'ovest': {'lato_motore': 'POKEGEAR_REGION_JOHTO / MAP_REGION_JOHTO', 'colonne': '0–23', 'nome': 'Ovest',
              'messaggio': 'msg_0273_00001'},
    'livello_di_sblocco': 'ScrCmd_804 2 nel primo script di M-CT-01 (Modulo 6)',
    'volo': 'su tutta l’isola (E-GFX-03)',
}


def riga_finale(man):
    pg = man['pokegear']
    return ('BLOCCO COMPLETO: 4.4 — schermata copyright (4 righe, %d tile su 160); titolo con logo «Pokémon Trinacria», '
            'triscele, alba sull’Etna e riga dell’autore (palette 4 riscritta); mappa della Sicilia nel Pokégear '
            '(%d tile su 768, 27 toppe dei punti di volo, %d cornici per %d luoghi, 20 piantine in %d tile su 576), '
            'regioni Est/Ovest dalla colonna 24, tabella del Volo e tabella dei luoghi rigenerate, 100 descrizioni '
            'in msg_0273; Sondaggio del Consenso nei 6 temi; %d file, 1 tabella e %d sostituzioni di codice '
            '(E-GFX-02…04) con applica --blocchi 4.4; 5 regole R-GFX-29…33; sprite dei personaggi spostati al 4.5'
            % (man['copyright']['tile'], pg['tile_mappa'], pg['cornici'], len(pg['luoghi']), pg['tile_piantine'],
               len(man['file']), len(man['sostituzioni'])))


def _tab(intest, righe):
    out = ['| ' + ' | '.join(intest) + ' |', '|' + '---|' * len(intest)]
    for r in righe:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def documento(man, prova, riga):
    pg = man['pokegear']
    so = man['sondaggio']
    P = []
    a = P.append
    a('# Modulo 4 · Blocco 4.4 — Titolo, copyright, Pokégear e Sondaggio\n')
    a('**Versione:** 1.0 · %s · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** '
      '`F:\\Progetti\\pokeheartgold`\n' % DATA)
    a('**File del blocco:**\n')
    a(_tab(['File', 'Cosa contiene'], [
        ('`docs/MODULO_4/4.4_UI_TITOLO_POKEGEAR.md`', 'questo documento'),
        ('`docs/MODULO_4/4.4_POKEGEAR.json`', 'dati generati: tabella del Volo, i 100 luoghi, le mappe senza luogo, '
         'le piantine, i file sostituiti con lo SHA-1, le modifiche di codice col testo esatto, la prova di `applica`'),
        ('`tools/grafica/4.4/`', 'script di disegno (R-GFX-17): `comune44.py` (NCLR/NSCR/NCGR a forma invariata, testo '
         'col font del gioco), `copyright44.py`, `titolo44.py`, `dati44.py` e `pokegear44.py` (mappa, toppe, luoghi), '
         '`piantine44.py`, `sondaggio44.py`, `testi44.py` (nomi delle regioni e descrizioni), `costruisci44.py` (tutto)'),
        ('`tools/generatori/4.4/`', 'generatore di questo documento e del JSON (`gen44.py`, `text44.py`)'),
        ('`tools/trinacria_gfx.py`', 'comando `applica` esteso ai manifesti «a file» (`applica_file`, codici K22–K23)'),
    ]) + '\n')
    a('Fonti lette nel repository: `src/intro_movie_scene_1.c`, `src/title_screen.c`, '
      '`src/application/pokegear/main/overlay_100_021E5900.c`, `src/application/pokegear/map/` (`pokegear_map.c`, '
      '`fly_map.c`, `overlay_101_021E7FF4.c`, `overlay_101_021E9270.c`, `overlay_101_021F79B4.c`), '
      '`include/application/pokegear/map/pokegear_map_internal.h`, `src/unk_02092BE8.c`, `src/scrcmd_c.c` (ScrCmd_804), '
      '`files/msgdata/msg/msg_0273.json`, i file di `files/demo/` e `files/application/pokegear/`, il font '
      '(`files/graphic/font/font_00000000.bin`, `tools/msgenc/charmap.txt`). Dal progetto: Modulo 1 §9 e M1-04b, trama '
      'v1.9 (R-05, R-06, R-09.6), registri 2.1–2.5, 3.3 (vaganti), blocchi 4.1–4.3 (celle della matrice 0 e schede '
      'delle città, rigenerate con gli script del 4.2 e del 4.3).\n')

    a('## 0. In breve\n')
    a('- **Il blocco è diviso in due.** La richiesta 4.4 della scaletta univa interfaccia e sprite dei personaggi: '
      'troppo per un blocco solo. Il 4.4 fa titolo, copyright, Pokégear e Sondaggio; gli sprite (26 di personaggi, '
      '12 di classe, 36 immagini frontali, 8 dorsi, transizioni, medaglie dei Dossier, testa del protagonista e icona '
      'del vagante nella mappa del Pokégear) passano alla richiesta nuova **4.5** (scaletta v2.19).\n'
      '- **Tutto è generato e provato.** `python -I tools/grafica/4.4/costruisci44.py` scrive i file nuovi in '
      '`build/grafica/4.4/` e le anteprime → `GRAFICA_OK` in pochi secondi; `python -I tools/trinacria_gfx.py applica '
      '--blocchi 4.4` li porta nel repository: %d file, la tabella dei luoghi dentro `pokegear_map.c` e %d sostituzioni '
      'di codice. Prova in una cartella temporanea: %s.\n' % (len(man['file']), len(man['sostituzioni']), '; '.join(prova['righe'])) +
      '- **Copyright:** le quattro righe del Modulo 1 §9.2 al posto di «GAME FREAK presents» e dell’avviso ESRB, col '
      'font del gioco (%d tile su 160).\n' % man['copyright']['tile'] +
      '- **Titolo:** logo «Pokémon / TRINACRIA» nei colori della bandiera con la triscele, fondo con l’alba sull’Etna e '
      'sullo Ionio (%d colori), riga «%s» al posto di «Developed by GAME FREAK inc.».\n'
      % (man['titolo']['colori_fondo'], man['titolo']['autore']) +
      '- **Pokégear:** la mappa è la matrice 0 vista dall’alto, una tile per cella; Est (colonna ≥ 24) e Ovest '
      '(colonna ≤ 23) come vuole la trama R-09.6, ora anche nel codice (E-GFX-02); il Volo vale su tutta l’isola '
      '(E-GFX-03); 27 punti di volo con la toppa grigia «non visitata», 100 luoghi con nome, cornice e descrizione, 20 '
      'piantine di città disegnate dalle celle vere del 4.2 e del 4.3.\n'
      '- **Sondaggio:** sullo schermo superiore del Pokégear, sotto l’orologio, la scritta «Sondaggio», una barra di '
      '20 tacche e la percentuale di `VAR_TRINACRIA_CONSENSO`, in tutti e 6 i temi (E-GFX-04).\n')

    a('## 1. Come si costruisce e come si applica\n')
    a(_tab(['Passo', 'Comando (dalla cartella del progetto)', 'Esito'], [
        ('1. costruzione', '`python -I tools/grafica/4.4/costruisci44.py` (Windows, provato il 28/10/2026; solo libreria standard)',
         '`GRAFICA_OK`; file in `build/grafica/4.4/file/`, anteprime in `build/grafica/4.4/anteprime/`'),
        ('2. prova', '`python -I tools/trinacria_gfx.py applica --blocchi 4.4 --prova <cartella vuota>`',
         '`GRAFICA_OK`; nessun file del repository toccato'),
        ('3. applicazione', '`python -I tools/trinacria_gfx.py applica --blocchi 4.4` (anche insieme: `--blocchi 4.2 4.3 4.4`)',
         '`GRAFICA_OK`; cambiano i file della §2'),
        ('4. build', 'build del Modulo 1 (M1-02)', '`BUILD_OK`; il build converte i PNG con le opzioni del loro `meson.build` (R-GFX-08)'),
    ]) + '\n')
    a('`applica` controlla che ogni file da sostituire sia ancora l’originale di HeartGold (SHA-1 nel manifesto) o '
      'già quello del blocco, che l’inizio della tabella dei luoghi ci sia una volta sola e che ogni testo di codice da '
      'sostituire compaia una volta sola (K23): applicarlo due volte non cambia nulla. Le modifiche di codice usano '
      '`VAR_TRINACRIA_CONSENSO` (M1-04b) e i simboli `MAP_*`/`FLYPOINT_*` rinominati del Modulo 2: il 4.4 si applica '
      'dopo quei passi del Modulo 7.\n')

    a('## 2. File sostituiti\n')
    a(_tab(['File del repository', 'Byte', 'Cosa'], [('`%s`' % f['destinazione'], f['byte'], f['nota']) for f in man['file']]) + '\n')
    a('Più la tabella `sLocationSpecs` dentro `src/application/pokegear/map/pokegear_map.c` (dall’inizio della tabella '
      'al primo `};`) e le modifiche E-GFX-02…04 della §8.\n')

    a('## 3. Regole nuove\n')
    a(_tab(['Regola', 'Titolo', 'Contenuto'], [
        ('R-GFX-29', 'Binari a forma invariata', 'Un NCLR, un NSCR o un NCGR lineare (non a celle, non cifrato) che sta '
         'nel repository come binario si riscrive cambiando solo i dati nel file originale: colori, voci della '
         'schermata, pixel delle tile. Stessa lunghezza e stesse intestazioni (`comune44.py`: `nclr_patch`, `nscr_patch`, '
         '`ncgr_patch`; controllo K22). Provato: %d file binari di `files/demo` e `files/application/pokegear` letti e '
         'riscritti identici. Gli NCGR a celle o cifrati (sprite degli allenatori, 4.5) restano a `nitrogfx` '
         '(R-GFX-08).' % man['prova_forma']['identici']),
        ('R-GFX-30', 'La mappa del Pokégear è la matrice 0', 'Una tile 8×8 della mappa per ogni cella della matrice 0, '
         'due righe di mare sopra (tile (x, y+2)). I colori sono gli indici che la mappa di HeartGold usa già (mare 37–40, '
         'terra 23–31, strade 10, città 2–4, grigi 9 e 18–20, cornici 44–47): le 6 palette dei temi (NCLR 20–25) non '
         'cambiano. Le toppe che il codice copia per il livello di sblocco, il Safari e Sinjoh ricopiano la mappa (non '
         'nascondono nulla); quella della S.S. Aqua mostra il traghetto sul mare.'),
        ('R-GFX-31', 'Cento luoghi', 'La tabella `sLocationSpecs` ha 100 voci fisse (PGMAP_NUM_LOCATIONS). Ci vanno '
         'per forza le 41 strade dei vaganti (il codice cerca la voce della mappa del vagante e senza voce si '
         'ferma: `overlay_101_021E9270.c`, icone dei vaganti), le 27 città col Volo, le 4 isole e Corso Italia; le altre '
         '27 sono le mappe della matrice 0 con più missioni (punteggio di `dati44.py`). Ogni voce è il rettangolo più '
         'grande di celle della mappa che contiene la cella principale; nessuna sovrapposizione. Le %d mappe senza voce '
         'non mostrano un nome sotto il cursore (il nome compare comunque entrando nella mappa).' % len(pg['escluse'])),
        ('R-GFX-32', 'Fogli di tile più alti', 'Il foglio della cornice del tema 5 (`pgear_gra_00000041.png`) passa da '
         '256×24 a 256×32 pixel come gli altri cinque, per far posto alle tile del Sondaggio. È l’unico file del blocco '
         'che non ha le misure dell’originale (deroga a R-GFX-02): il codice carica l’NCGR intero e gli altri temi '
         'occupano già 128 tile.'),
        ('R-GFX-33', 'Est e Ovest', 'Lato Kanto del motore = Sicilia orientale = colonna ≥ 24 della matrice 0; lato '
         'Johto = Sicilia occidentale = colonna ≤ 23 (trama R-09.6, registri 2.1–2.3: nessuna mappa in disaccordo). '
         'Nomi nel Pokégear: «Est» e «Ovest» (la finestra è larga 38 pixel utili: «Livanti» starebbe, «Punenti» no). Il '
         'Modulo 6 mette `ScrCmd_804 2` nel primo script di M-CT-01: col livello 0 di HeartGold il Pokégear '
         'nasconderebbe proprio l’Est, dove comincia il gioco.'),
    ]) + '\n')

    a('## 4. Copyright (GFX-COPYRIGHT)\n')
    a('La prima schermata del filmato d’apertura (`src/intro_movie_scene_1.c`: 30 frame, poi dissolvenza di 60) è '
      '`gs_opening_00000005.NCGR` (160 tile a 4 bit, compresse LZ dal build) con la schermata `gs_opening_00000013.NSCR` '
      'su `GF_BG_LYR_MAIN_0`. In HeartGold mostra «GAME FREAK presents» e l’avviso ESRB. Trinacria ci scrive le quattro '
      'righe del Modulo 1 §9.2, centrate, col font 0 del gioco (bianco con ombra, palette 2 della NCLR 1 come l’avviso '
      'ESRB); il © è il glifo di `tools/font_extend.py`.\n')
    a(_tab(['Riga', 'Testo', 'Larghezza'], [(k + 1, r['testo'], '%d px' % r['px']) for k, r in enumerate(man['copyright']['righe'])]) + '\n')
    a('Gli uccelli animati della stessa scena (`gs_opening_00000023–30`) sono Pokémon e restano (R-GFX-14).\n')

    a('## 5. Titolo (GFX-TITLE-*)\n')
    a(_tab(['Voce', 'File', 'Contenuto'], [
        ('GFX-TITLE-FONDO', '`titledemo_00000034.png` (256×192, 8 bit, indici 128–255)', 'alba sull’Etna col pennacchio '
         'spinto a ovest, colata sul fianco sud, sole sul mare con il riflesso, costa con le luci dei paesi'),
        ('GFX-TITLE-LOGO', '`titledemo_00000003.png` (256×120, 8 bit, indici 1–15)', '«Pokémon» giallo bordato di blu, '
         '«TRINACRIA» dal giallo al rosso come la bandiera siciliana, la triscele sotto; lettere = glifi del font '
         'ingranditi ×2 e ×3 con contorno e ombra'),
        ('GFX-TITLE-AUTORE', '`titledemo_00000015.png` (256×24, 4 bit, palette 7 = indici 124–126)', '«%s» al posto di '
         '«Developed by GAME FREAK inc.»' % man['titolo']['autore']),
        ('GFX-TITLE-PALETTE', '`titledemo_00000004.NCLR`', 'colori nuovi negli indici 1–15, 124–126 e 128–255; 0, '
         '16–31 (sfumati dal bagliore del titolo) e gli altri restano quelli di HeartGold'),
    ]) + '\n')
    a('Le schermate (`titledemo_00000000/17/35.NSCR`) non cambiano: il fondo occupa una tile per posto, il logo è '
      'spostato di tre righe, la riga dell’autore usa la palette 7. I file di SoulSilver (1, 2, 14, 36, 37) non si '
      'toccano. Il modello 3D di Ho-Oh resta (R-GFX-14). La scritta «Touch to Start» è testo del banco msg_0719 '
      '(interfaccia: resta inglese finché non c’è una richiesta che la traduce).\n')

    a('## 6. Pokégear\n')
    a('### 6.1 Regioni\n')
    a('`Pokegear_RegionFromCoords` (E-GFX-02) torna Kanto per x ≥ 24 e Johto per il resto, senza i casi speciali di '
      'Monte Argento e dell’Altopiano Blu (in Trinacria cadrebbero su Gela e su Enna). Il nome stampato in alto a '
      'sinistra è `msg_0273_00000` («Est») per il lato Kanto e `msg_0273_00001` («Ovest») per il lato Johto. Il Volo '
      'di HeartGold vale solo dentro la regione in cui si è (`ov101_021EA7E4`): con E-GFX-03 si vola da Catania a '
      'Trapani e ritorno. Le coordinate del giocatore: sulla matrice 0 sono la cella in cui sta; nelle stanze e sulle '
      'isole sono `worldMapX/Y` dell’intestazione della mappa (registri 2.1–2.3, `src/unk_02092BE8.c`).\n')
    a('### 6.2 Mappa (GFX-PGMAP-MAPPA)\n')
    a('`pgmap_gra_00000010.png` (512×96, 8 bit) e la schermata `pgmap_gra_00000011.NSCR` (64×64 tile, `unk_170`). '
      'Terra e mare vengono dalle celle della matrice 0 dei blocchi 4.2 e 4.3 (paesaggio «mare» e celle vuote = mare), '
      'con la costa arrotondata e la sabbia sul bordo; l’Etna è un cono innevato col fumo, colline e Sicani a puntini, '
      'i Nebrodi a bosco, Pergusa e la Diga Jato come laghi. Le strade sono le mappe di profilo STRADA: un tratto bianco '
      'fra le loro celle e uno verso ogni mappa vicina raggiunta da un confine percorribile. Le città col Volo sono '
      'riquadri rossi grandi quanto la loro riga della tabella del Volo; le altre città e i paesi quadratini rossi, le '
      'località puntini arancioni. Isole minori disegnate nel mare: Favignana (0,6), Lampedusa (16,18), Pantelleria '
      '(4,15), le Eolie (37–40, 0–1). %d tile su 768.\n' % pg['tile_mappa'])
    a(_tab(['Zona della schermata 64×64', 'Cosa c’è', 'Chi la copia'], [
        ('righe 0–19, colonne 0–46', 'la mappa', '`ov101_021EAF40`'),
        ('colonne 48–53 e 54–56, righe 0–19', 'copia delle colonne 22–27 e 29–31', 'livello di sblocco 0 e 1'),
        ('(41,20), (41,27), (48,27), 5×6', 'copia di (1,9)', 'Safari e Fiordoro di HeartGold'),
        ('(55,20) 3×4', 'copia di (19,1)', 'mappe Sinjoh (Pantelleria)'),
        ('(55,24) 3×3', 'il traghetto sul mare in (24,15)', 'mappe S.S. Aqua (Favignana, traghetto di Lampedusa)'),
        ('righe 20–31 dalla colonna 0', 'le 27 toppe «non visitata» (città in grigio)', 'tabella del Volo'),
        ('righe 32–63', 'le %d cornici gialle, una per misura di luogo' % pg['cornici'], 'tabella dei luoghi'),
    ]) + '\n')
    a('### 6.3 Tabella del Volo (`gMapFlypointParams`)\n')
    a('`src/application/pokegear/map/overlay_101_021F79B4.c` si riscrive intero. Le colonne mapIDforName…height sono '
      'quelle del registro 2.5 (stesso ordine delle righe); `unk_05` è il numero della toppa (0xFF = nessuna), '
      '`unk170Src*` dove sta la toppa nella schermata, `unk170Dest*` la sua misura e di quanto sporge a sinistra e in '
      'alto rispetto alla città (al bordo della mappa sporge di 0).\n')
    a(_tab(['Riga', 'Città', 'x, y', 'w×h', 'unk_05', 'Src', 'Dest w×h', 'Dest x, y'],
           [(v['riga'], '`%s`' % v['simbolo'], '%d, %d' % (v['x'], v['y']), '%d×%d' % (v['width'], v['height']),
             v['unk_05'], '%d, %d' % (v['unk170SrcX'], v['unk170SrcY']),
             '%d×%d' % (v['unk170DestWidth'], v['unk170DestHeight']), '%d, %d' % (v['unk170DestX'], v['unk170DestY']))
            for v in pg['volo']]) + '\n')
    a('### 6.4 I 100 luoghi (`sLocationSpecs`)\n')
    a('Coordinate del Pokégear (riga = riga della matrice + 2). `msg` è la descrizione in `msg_0273` (dalla 10 in poi); '
      '`P` è la piantina (0 = nessuna); la cornice è (w+2)×(h+2) tile attorno al luogo, o w×h dentro per i luoghi sul '
      'bordo (Favignana, le Eolie), perché il codice sposta di una tile in alto a sinistra le cornici di 9 tile o più.\n')
    a(_tab(['#', 'Mappa', 'Nome', 'x, y', 'w×h', 'Regione', 'msg', 'P', 'Cornice'],
           [(k, '`%s`' % L['mapId'], L['nome'], '%d, %d' % (L['x'], L['y']), '%d×%d' % (L['width'], L['height']),
             L['regione'], L['testo'], L['piantina'],
             '%d,%d %d×%d' % (L['tilemapUnk170SrcX'], L['tilemapUnk170SrcY'], L['tilemapUnk170DestWidth'], L['tilemapUnk170DestHeight']))
            for k, L in enumerate(pg['luoghi'])]) + '\n')
    a('Mappe della matrice 0 senza luogo (%d): %s.\n' % (len(pg['escluse']), ', '.join('`%s`' % s for s in pg['escluse'])))
    a('### 6.5 Piantine (GFX-PGMAP-PIANTINE)\n')
    a('`pgmap_gra_00000012.png` (256×144, 4 bit) e `pgmap_gra_00000013.NSCR` (`unk_174`): 20 riquadri di 7×7 tile, '
      'palette 2 (uguale nei 6 temi). Ogni piantina è la cella del Centro Pokémon della città, rigenerata con gli '
      'script del 4.2 o del 4.3 (stessa scheda, stesso seme) e ridotta a 28×28 caselle da 2 pixel: strade bianche, '
      'spazi aperti grigio chiaro, Centro rosso, edifici arancioni, acqua azzurra, uscite verdi, il resto a righe. '
      '%d tile su 576. Le altre 7 città col Volo e tutti gli altri luoghi hanno P = 0, come i luoghi di HeartGold senza '
      'piantina.\n' % pg['tile_piantine'])
    a(_tab(['P', 'Città', 'Cella'], [(p['blocco'], '`%s`' % p['mappa'], p['cella']) for p in pg['piantine']]) + '\n')
    a('### 6.6 Testi (`msg_0273`)\n')
    a('Cambiano i messaggi 0–1 (regioni) e 10–109 (descrizioni, due righe di al massimo 224 pixel, controllate dal '
      'costruttore); 110–117 diventano vuoti. I messaggi 2–8 (comandi del Volo: «Choose your destination.», «Fly», '
      '«Quit»…) sono interfaccia e restano come sono. Le descrizioni stanno in `tools/grafica/4.4/testi44.py`: i luoghi '
      'veri sono solo ambientazione (trama R-05).\n')

    a('## 7. Sondaggio (GFX-SONDAGGIO)\n')
    a('Lo schermo superiore del Pokégear è la cornice di `GF_BG_LYR_SUB_0` (`pgear_gra_00000036–41.png` e '
      '`pgear_gra_00000042–47.NSCR`, una coppia per tema, palette 13). Sotto la fascia dell’orologio le righe 12–15 '
      'sono vuote: il blocco ci mette la scritta «Sondaggio» (righe 12–13, dalla colonna 3), la barra (riga 14: capi in '
      '3 e 24, 20 tacche in 4–23) e la percentuale (cifre in 26–28, «%%» in 29). Tile nuove dall’indice 96 '
      '(HeartGold ne usa al massimo 79): sfondo 96, tacca vuota 97, piena 98, capi 99–100, «%%» 101, cifre 0–9 in '
      '102–111, scritta da 112. I colori sono scelti per tema dalla palette 13 (più scuro, più chiaro, il più saturo):\n')
    a(_tab(['Tema', 'Scuro', 'Chiaro', 'Accento', 'Medio', 'Sfondo di HeartGold'],
           [(t['tema'], t['ruoli']['scuro'], t['ruoli']['chiaro'], t['ruoli']['accento'], t['ruoli']['medio'], t['sfondo_hg'])
            for t in so['temi']]) + '\n')
    a('La schermata contiene la barra vuota e «0%»; il codice (E-GFX-04) la riempie a ogni apertura del Pokégear e a ogni '
      'cambio di tema: tacche piene = (Consenso × 20 + 50) / 100, cifre senza zeri davanti, Consenso oltre 100 letto '
      'come 100. Anteprime: `build/grafica/4.4/anteprime/sondaggio_tema0–5.png` (Consenso 7, 23, 37, 49, 60, 100).\n')

    a('## 8. Modifiche di codice\n')
    a('Le applica `applica --blocchi 4.4` come sostituzioni esatte (il testo «Cerca» deve comparire una volta sola). '
      'Il testo completo è anche in `4.4_POKEGEAR.json`, sezione `modifiche_codice`.\n')
    for s in man['sostituzioni']:
        a('**%s** — `%s`\n' % (s['id'], s['file']))
        a('Cerca:\n```c\n%s```\nSostituisci con:\n```c\n%s```\n' % (s['cerca'], s['sostituisci']))

    a('## 9. Note per gli altri blocchi\n')
    a('- **4.5 (nuova richiesta: sprite dei personaggi).** Tutto quello che la scaletta chiedeva al 4.4 sugli sprite, '
      'più due cose trovate qui: la testa del protagonista che fa da segnalino nella mappa del Pokégear '
      '(`pgmap_gra_00000001.png`, celle `pgmap_gra_00000002/3`) e l’icona del vagante nello slot 2, ancora Latias '
      '(blocco 3.3; stesso foglio). Il documento 4.1 §4.8, §7 B e §12 restano la guida per gli sprite.\n'
      '- **Modulo 6.** `ScrCmd_804 2` nel primo script di M-CT-01 (R-GFX-33). Il Consenso si legge da '
      '`VAR_TRINACRIA_CONSENSO` e il Sondaggio lo mostra da solo: nessuno script lo disegna. Le descrizioni dei luoghi '
      'sono già scritte qui (msg_0273): il Modulo 6 non le riscrive.\n'
      '- **Modulo 7 (7.4).** TASK a schermo: schermata copyright; titolo (logo, fondo, riga dell’autore, bagliore); '
      'Pokégear da Corso Italia (cursore sulla cella giusta, nome «Est», piantina di Catania, cornice gialla), toppa '
      'grigia di una città non visitata, Volo da Catania a Trapani, giocatore su Lampedusa (segnalino in (16,18)); '
      'Sondaggio con Consenso 1, 37 e 100 in due temi; Pokégear «mappa del paese» (strumento) con la stessa mappa.\n')

    a('## 10. Decisioni da guardare\n')
    a('- **Blocco diviso** (4.4 interfaccia, 4.5 sprite): la scaletta passa a 73 richieste.\n'
      '- **Nomi delle regioni «Est» e «Ovest»**: in siciliano «Livanti» (36 px) entrerebbe, «Punenti» (39 px) no.\n'
      '- **Volo su tutta l’isola** (E-GFX-03): HeartGold vieta il Volo fra Johto e Kanto; in Trinacria dividerebbe la '
      'Sicilia in due.\n'
      '- **100 luoghi su 167 mappe esterne:** %d mappe della matrice 0 non hanno nome sotto il cursore (§6.4); fra '
      'queste Fontanarossa, Castelvetrano, Capaci e Mistretta, che hanno missioni ma meno di quelle scelte.\n'
      '- **Pantelleria e le Eolie** hanno il riquadro nel mare, ma il segnalino del giocatore va dove dicono '
      '`worldMapX/Y` dei registri: Trapani e Milazzo, i porti d’imbarco.\n'
      '- **Foglio del tema 5 più alto** (R-GFX-32).\n'
      '- **Stile procedurale**, come nel 4.2 e nel 4.3.\n' % len(pg['escluse']))

    a('## 11. Codici d’errore\n')
    a(_tab(['Codice', 'Significato'], [
        ('K22', 'file nuovo con lunghezza o intestazione diverse dall’originale (R-GFX-29)'),
        ('K23', '`applica`: testo da sostituire o inizio della tabella trovato zero o più volte'),
        ('K00', '`applica`: file del repository che non è né l’originale né quello del blocco'),
        ('T01', 'nome di regione oltre 38 pixel'),
        ('T02', 'luogo senza descrizione in `testi44.py`'),
        ('T03', 'riga di descrizione oltre 224 pixel'),
        ('K10–K15', 'controlli dei PNG del 4.1 (stesse misure, indici, colori 555)'),
    ]) + '\n')
    a('## 12. Riga di controllo\n')
    a('`%s`\n' % riga)
    return '\n'.join(P)

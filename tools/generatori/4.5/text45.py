"""Testi fissi del blocco 4.5 (documento docs/MODULO_4/4.5_SPRITE_PERSONAGGI.md)."""

DATA = '28/10/2026'
RUOLI = {'0': 'trasparente (colore dell’originale)', '1': 'contorno', '2': 'pelle', '3': 'pelle in ombra',
         '4': 'capelli', '5': 'capelli in ombra, baffi e barba', '6': 'vestito di sopra', '7': 'sopra in ombra, maniche di profilo',
         '8': 'vestito di sotto', '9': 'sotto in ombra', '10': 'scarpe', '11': 'bianco (camicia, occhi)',
         '12': 'accento A (cravatta, pochette, sciarpa, rossetto)', '13': 'accento B (cappelli, borse, occhiali, bici)',
         '14': 'accento C (oro, attrezzi, ruote, canna)', '15': 'occhi e lenti scure'}

TIPI_POSA = [
    ('fermo', 'in piedi, braccia lungo i fianchi'),
    ('passo', 'il corpo sale di un pixel, una gamba avanti e il braccio opposto avanti (fasi 0 e 1)'),
    ('corsa_fermo / corsa', 'corpo chinato, braccia piegate, passo più lungo, piede staccato da terra'),
    ('bici / bici_salto', 'seduto sulla bicicletta, mani sul manubrio; fase 0 pedali pari, 1 e 2 una gamba giù; salto = tre pixel più in alto'),
    ('surf', 'seduto sul Pokémon, solo busto e ginocchia (il Pokémon lo disegna il gioco)'),
    ('pesca', 'canna indietro (0), alta (1), lanciata (2), tesa (3)'),
    ('scala', 'di spalle o di fronte, un braccio in alto e l’altro a metà, le gambe si alternano (fasi 0–2)'),
    ('salva', 'di fronte; fase 1 con la mano al petto'),
    ('banzai', 'braccia giù (0), larghe (1), a metà (2), in alto (3)'),
    ('spinta', 'braccia avanti; fase 1 un pixel più in alto (`Bottintesta` sugli alberi)'),
]

TABELLE = [
    ('cammina16', '16', '1–4 di spalle, 5–8 di fronte, 9–12 a sinistra, 13–16 a destra; in ogni gruppo: fermo, passo 0, fermo, passo 1 (1 e 3 hanno gli stessi dati)'),
    ('eroe32', '32', '1–16 come cammina16; 17–32 la corsa nello stesso ordine (corsa_fermo, corsa 0, corsa_fermo, corsa 1)'),
    ('bici24', '24', '1–16 bici per direzione (fase 0, 1, 0, 2); 17–24 salto: sinistra 0 e 1, destra 0 e 1, spalle, fronte, fronte 1, spalle 1'),
    ('surf4', '4', 'spalle, fronte, sinistra, destra'),
    ('pesca16', '16', 'quattro fasi per direzione, nell’ordine spalle, fronte, sinistra, destra'),
    ('scala6', '6', '1–3 di spalle, 4–6 di fronte (fasi 0–2)'),
    ('salva2', '2', 'fronte, fronte con la mano al petto'),
    ('banzai12', '12', '1 sinistra fermo, 2 sinistra braccia larghe, 3–6 di spalle: giù, larghe, in alto, a metà; 7–12 ripetono 5, 4, 3, 2, 1, 6 (dati condivisi dell’originale)'),
    ('spinta8', '8', 'due fasi per direzione: spalle, fronte, sinistra, destra'),
]


def riga_finale(man):
    return ('BLOCCO COMPLETO: 4.5 — sprite di campo ridisegnati con un manichino a script: %d personaggi e classi '
            'del registro 2.5 (26 personaggi, 12 classi di «U Sistema»: 16 fotogrammi ciascuno) e %d sprite del '
            'protagonista (ragazzo e ragazza, 9 famiglie: cammina, corre, bici, surf, pesca, scala, salvataggio, '
            'braccia alzate, Bottintesta); %d NSBTX riscritti a forma invariata (prova: %d su %d identici); '
            'applica --blocchi 4.5 provato; regole R-GFX-34…37; immagini di lotta, medaglie e icone del Pokégear '
            'spostate al 4.6' % (len(man['personaggi']), len(man['protagonista']), len(man['file']),
                                 man['prova_forma']['identici'], man['prova_forma']['provati']))


def _tab(intest, righe):
    out = ['| ' + ' | '.join(intest) + ' |', '|' + '---|' * len(intest)]
    for r in righe:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def _acc(p):
    a = list(p['accessori'])
    if p.get('pancia'):
        a.append('pancia')
    return ', '.join(a) or '—'


def documento(man, prova, riga):
    P = []
    a = P.append
    pers = [p for p in man['personaggi'] if p['gruppo'] == 'personaggi']
    classi = [p for p in man['personaggi'] if p['gruppo'] == 'classi']
    a('# Modulo 4 · Blocco 4.5 — Sprite di campo dei personaggi\n')
    a('**Versione:** 1.0 · %s · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** '
      '`F:\\Progetti\\pokeheartgold`\n' % DATA)
    a('**File del blocco:**\n')
    a(_tab(['File', 'Cosa contiene'], [
        ('`docs/MODULO_4/4.5_SPRITE_PERSONAGGI.md`', 'questo documento'),
        ('`docs/MODULO_4/4.5_SPRITE_PERSONAGGI.json`', 'dati generati: schede di ogni sprite, tabelle dei fotogrammi, ruoli della palette, file sostituiti con lo SHA-1, prove'),
        ('`tools/grafica/4.5/`', 'script di disegno (R-GFX-17): `omino45.py` (il manichino), `schede45.py` (personaggi, classi, protagonista, tabelle dei fotogrammi), `comune45.py` (NSBTX a forma invariata, palette), `costruisci45.py` (tutto)'),
        ('`tools/generatori/4.5/`', 'generatore di questo documento e del JSON (`gen45.py`, `text45.py`)'),
    ]) + '\n')
    a('Fonti lette nel repository: `asm/overlay_01_sprite_data.s` (sprite → modello), `include/constants/mmodel.h`, '
      '`include/constants/sprites.h`, i NSBTX di `files/data/mmodel/mmodel/`, `src/player_avatar.c` (sprite del '
      'protagonista per stato), `src/oaks_speech.c` (scelta ragazzo o ragazza). Dal progetto: registro 2.5 (sezione '
      '`sprite`), trama v1.9 (C-01…C-08, M-CT-01/02, R-10.2, R-10.6, segreterie M-*-0x, M-EN-04/06/07, P-03, P-10), '
      'blocchi 4.1 (§4.7, R-GFX-14…17) e 4.4 (R-GFX-29).\n')

    a('## 0. In breve\n')
    a('- **Il blocco è diviso in due**, come il 4.4: qui gli **sprite di campo** (quelli che camminano nelle mappe); '
      'le immagini di lotta (36 classi di fronte, i dorsi dei compagni e del protagonista), le transizioni, le medaglie '
      'dei 9 Dossier, la testa del protagonista e l’icona del vagante nel Pokégear passano alla richiesta nuova **4.6** '
      '(scaletta v2.20, 74 richieste).')
    a('- **Un manichino disegna tutti.** `omino45.py` costruisce un personaggio 32×32 da una scheda (capelli, '
      'vestiti, accessori, corporatura, colori) e da una posa (direzione, movimento, fase): testa di 14×13 pixel, corpo '
      'di 12 righe, piedi alla riga 29, ombra a destra e in basso, contorno scuro tutto attorno. Niente è copiato dagli '
      'sprite di HeartGold (R-GFX-17): di loro si tengono solo le misure del fotogramma e l’ordine dei fotogrammi.')
    a('- **%d sprite di personaggi e classi** (tutti gli slot `SPRITE_TRN_*` del registro 2.5) e **%d sprite del '
      'protagonista**, ragazzo e ragazza, in 9 famiglie (cammina e corre, bicicletta, surf, pesca, scale, '
      'salvataggio, braccia alzate, `Bottintesta`).' % (len(man['personaggi']), len(man['protagonista'])))
    a('- **File a forma invariata (R-GFX-34).** Ogni NSBTX nuovo è l’originale con i soli pixel e i 15 colori '
      'cambiati: stessa lunghezza, stessi nomi di texture, stessi indirizzi. Prova: %d NSBTX di HeartGold con una '
      'palette di 16 colori letti e riscritti identici su %d.' % (man['prova_forma']['identici'], man['prova_forma']['provati']))
    a('- **Nessuna modifica di codice.** I simboli `SPRITE_TRN_*` sono già alias degli slot di HeartGold '
      '(`include/trinacria/trinacria_sprites.h`, registro 2.5): cambia solo la grafica dietro lo slot.\n')

    a('## 1. Come si costruisce e come si applica\n')
    a(_tab(['Passo', 'Comando (dalla cartella del progetto)', 'Esito'], [
        ('1. costruzione', '`python -I tools/grafica/4.5/costruisci45.py` (Windows, provato il %s; solo libreria standard, 3 secondi)' % DATA,
         '`GRAFICA_OK`; file in `build/grafica/4.5/file/`, anteprime in `build/grafica/4.5/anteprime/`'),
        ('2. prova', '`python -I tools/trinacria_gfx.py applica --blocchi 4.5 --prova <cartella vuota>`', '`GRAFICA_OK`; nessun file del repository toccato'),
        ('3. applicazione', '`python -I tools/trinacria_gfx.py applica --blocchi 4.5` (anche insieme: `--blocchi 4.2 4.3 4.4 4.5`)', '`GRAFICA_OK`; cambiano i file della §2'),
        ('4. build', 'build del Modulo 1 (M1-02)', '`BUILD_OK`; il build impacchetta `mmodel.narc` con le voci nell’ordine dei numeri dei file (4.1 §4.7)'),
    ]) + '\n')
    a('`applica` controlla che ogni file da sostituire sia ancora l’originale di HeartGold (SHA-1 nel manifesto) o già '
      'quello del blocco: applicarlo due volte non cambia nulla. Prova di questo blocco in una cartella temporanea: %s.\n'
      % '; '.join(prova['righe']))

    a('## 2. File sostituiti\n')
    a(_tab(['File del repository', 'Byte', 'Cosa'], [('`%s`' % f['destinazione'], f['byte'], f['nota']) for f in man['file']]) + '\n')

    a('## 3. Regole nuove\n')
    a(_tab(['Regola', 'Titolo', 'Contenuto'], [
        ('R-GFX-34', 'NSBTX a forma invariata', 'Uno sprite di campo (NSBTX di `files/data/mmodel/mmodel/` con texture palette16 «nome.numero» e una sola palette) si riscrive cambiando solo i dati delle texture e i colori 1–15 della palette (`comune45.riscrivi`): stessa lunghezza, intestazioni, nomi e indirizzi; il colore 0 (trasparente) resta quello dell’originale. Due fotogrammi che nell’originale condividono i dati devono uscire identici (controllo K22). Gli sprite dei Pokémon non si toccano (R-GFX-14).'),
        ('R-GFX-35', 'Il manichino', 'Ogni personaggio di campo nasce da una scheda di `schede45.py` disegnata da `omino45.py`. Palette a ruoli fissi (§7): così uno sprite nuovo è una scheda in più, non un disegno a mano. Scheda = capelli, sopra, sotto, accessori, `pancia` (0–1), colori dei ruoli, e una riga `perche` che dice da quale passo della trama viene l’aspetto. I personaggi coinvolti nel malaffare sono inventati: nessuno sprite imita una persona reale (trama R-05).'),
        ('R-GFX-36', 'Ordine dei fotogrammi', 'Il numero di ogni fotogramma ha il significato delle tabelle del §6 (letto guardando gli sprite di HeartGold nell’ordine dei nomi delle texture). Una tabella sbagliata si vede solo a schermo: i fotogrammi della bici 17–24 e del banzai 1–2 sono quelli meno sicuri e sono un TASK del 7.4.'),
        ('R-GFX-37', 'Protagonista ragazzo e ragazza', 'HeartGold fa scegliere ragazzo o ragazza in `src/oaks_speech.c` e Trinacria tiene la scelta: le 9 famiglie che il protagonista usa si ridisegnano in tutte e due le versioni, con la stessa scheda tranne capelli e rossetto. Restano di HeartGold, perché nessuna scena di Trinacria li usa: travestimento Rocket, Pokéathlon, statua, gli sprite di Lucas e Lucia di Sinnoh (§5).'),
    ]) + '\n')

    a('## 4. Personaggi e classi\n')
    a('Ogni sprite ha 16 fotogrammi (tabella `cammina16`). «Slot» è lo sprite di HeartGold di cui il simbolo è alias '
      '(registro 2.5); «File» è la voce di `mmodel` riscritta.\n')
    a('### 4.1 Personaggi (26)\n')
    a(_tab(['Simbolo', 'Slot', 'File', 'Chi', 'Capelli', 'Sopra / sotto', 'Accessori', 'Aspetto'],
           [('`%s`' % p['simbolo'], '`%s`' % p['slot'], p['numero'], p['chi'], p['capelli'],
             '%s / %s' % (p['sopra'], p['sotto']), _acc(p), p['perche']) for p in pers]) + '\n')
    a('### 4.2 Classi di «U Sistema» e affini (12)\n')
    a(_tab(['Simbolo', 'Slot', 'File', 'Classe', 'Capelli', 'Sopra / sotto', 'Accessori', 'Aspetto'],
           [('`%s`' % p['simbolo'], '`%s`' % p['slot'], p['numero'], '`%s`' % p['chi'], p['capelli'],
             '%s / %s' % (p['sopra'], p['sotto']), _acc(p), p['perche']) for p in classi]) + '\n')
    a('Gli slot del Team Rocket (`SPRITE_ROCKETM/W`, `SPRITE_RKANBUM/M2/M3/W`) non hanno più l’uniforme con la R: '
      '«U Sistema» non porta divise (trama R-10.2), ogni classe veste il suo racket. Nessuno slot del registro è '
      'condiviso con un altro sprite di HeartGold (controllo K25).\n')

    a('## 5. Protagonista\n')
    sp = man['schede_protagonista']
    a(_tab(['Versione', 'Capelli', 'Sopra / sotto', 'Accessori', 'Aspetto'],
           [(g, s['capelli'], '%s / %s' % (s['sopra'], s['sotto']), ', '.join(s['accessori']), s['perche'])
            for g, s in sp.items()]) + '\n')
    a(_tab(['Modello', 'File', 'Versione', 'Tabella', 'Fotogrammi (dati distinti)', 'Uso', 'Sprite che lo usano'],
           [('`%s`' % p['mmodel'], p['numero'], p['genere'], p['tabella'], '%d (%d)' % (p['fotogrammi'], p['unici']),
             p['uso'], ', '.join('`%s`' % x for x in p['sprite'])) for p in man['protagonista']]) + '\n')
    a('Restano di HeartGold: %s.\n' % ', '.join('`%s`' % x for x in man['non_usati']))

    a('## 6. Pose e tabelle dei fotogrammi\n')
    a(_tab(['Posa', 'Come la disegna il manichino'], TIPI_POSA) + '\n')
    a(_tab(['Tabella', 'Fotogrammi', 'Ordine'], TABELLE) + '\n')
    a('Le direzioni sono quattro: di spalle, di fronte, verso sinistra e verso destra; la destra è lo specchio della '
      'sinistra. Le tabelle complete (posa di ogni numero) sono nel JSON, sezione `tabelle_fotogrammi`.\n')

    a('## 7. Palette\n')
    a('Ogni sprite ha 16 colori con lo stesso ruolo (`omino45.RUOLI`); le ombre si ricavano dal colore di base '
      '(pelle × 0,82, capelli × 0,68, sopra × 0,70, sotto × 0,72) e tutti i colori sono portati alla scala dei 32 valori '
      'di `nitrogfx` (R-GFX-03).\n')
    a(_tab(['Indice', 'Ruolo'], sorted(RUOLI.items(), key=lambda x: int(x[0]))) + '\n')

    a('## 8. Anteprime\n')
    a(_tab(['File (in `build/grafica/4.5/`)', 'Righe'],
           [('`%s`' % x['png'], ', '.join('`%s`' % r for r in x['righe'])) for x in man['anteprime']]) + '\n')
    a('Nei fogli dei personaggi ogni riga ha 8 fotogrammi: di spalle fermo e passo, di fronte fermo e passo, a '
      'sinistra fermo e passo, a destra fermo e passo. In quelli del protagonista ogni riga è una famiglia con tutti '
      'i suoi fotogrammi in ordine.\n')

    a('## 9. Note per gli altri blocchi\n')
    a('- **4.6 (nuova richiesta: immagini di lotta, medaglie e icone).** Immagini frontali delle 36 classi del '
      'registro 2.5 (`note_grafica.classi_con_immagine_nuova`, `files/a/0/5/8`) e dorsi degli 8 compagni e del '
      'protagonista (`files/a/0/0/6`, 4.1 §4.8 e §7 B: cinque voci per classe, la quinta cifrata con `.key`), da '
      'disegnare con gli stessi vestiti e colori delle schede di `schede45.py`; transizioni di lotta da controllare '
      '(registro 2.5, `note_grafica.transizioni`); medaglie dei 9 Dossier; dal 4.4 la testa del protagonista nella mappa '
      'del Pokégear e l’icona del vagante nello slot 2 (ancora Latias), in `pgmap_gra_00000001.png`.')
    a('- **Modulo 6.** Negli eventi si usano i simboli `SPRITE_TRN_*` (lo sprite dei 4 Fantasmi è uno solo). La '
      'scelta ragazzo o ragazza resta (R-GFX-37): i testi che parlano del protagonista o gli si rivolgono devono valere '
      'per tutti e due, o usare i testi doppi di HeartGold per genere. Il palco di M-EN-07 può usare gli sprite del '
      'banzai (braccia alzate di spalle, verso la folla).')
    a('- **Modulo 7 (7.4).** TASK a schermo: `costruisci45.py` → `GRAFICA_OK`, `applica --blocchi 4.5`; un '
      'personaggio per gruppo che cammina nelle 4 direzioni (Turi, Mistretta, uno Scagnozzu); il protagonista, '
      'ragazzo e ragazza, che cammina, corre, va in bici e salta un gradino in bici (fotogrammi 17–24), fa surf, pesca '
      '(le 4 fasi in 4 direzioni), sale una scala, salva, usa `Bottintesta`; la scena del banzai (fotogrammi 1–2). '
      'Se un fotogramma ha la direzione sbagliata si corregge la tabella in `schede45.py`, non il disegno.\n')

    a('## 10. Decisioni da guardare\n')
    a('- **Blocco diviso** (4.5 sprite di campo, 4.6 immagini di lotta, medaglie e icone): la scaletta passa a 74 richieste.')
    a('- **Ragazzo e ragazza.** La trama parla del protagonista al maschile («un uomo solo»), ma HeartGold fa scegliere '
      'e togliere la scelta vuol dire cambiare `src/oaks_speech.c`. Il blocco disegna tutte e due le versioni; se si '
      'preferisce solo il ragazzo, la modifica va nel Modulo 6 o 7 e gli sprite della ragazza restano inutilizzati.')
    a('- **Aspetto del protagonista:** giacca blu, camicia bianca, pantaloni chiari e pochette rossa, da laureato '
      'della Catania «bene»; la ragazza ha gli stessi vestiti, la coda e il rossetto.')
    a('- **Aspetti decisi qui** per i personaggi che la trama non descrive (tabella del §4: Totò commesso dell’ARS coi '
      'bottoni dorati, Pippo con la maglia a righe, il Re delle Liste con la giacca di due colori, i Fantasmi pallidi '
      'col cappello).')
    a('- **Sprite non ridisegnati:** travestimento Rocket, Pokéathlon, statua e gli sprite di Sinnoh del protagonista (§5).')
    a('- **Stile procedurale**, come nei blocchi 4.2–4.4.\n')

    a('## 11. Codici d’errore\n')
    a(_tab(['Codice', 'Significato'], [
        ('K22', 'NSBTX nuovo con forma diversa dall’originale, o due fotogrammi a dati condivisi disegnati diversi (R-GFX-34)'),
        ('K24', 'lo sprite di HeartGold ha fotogrammi diversi da quelli della tabella, o non 32×32'),
        ('K25', 'simbolo senza scheda, slot assente dalla tabella degli sprite, o modello usato anche da un altro sprite'),
        ('K00', '`applica`: file del repository che non è né l’originale né quello del blocco'),
    ]) + '\n')

    a('## 12. Riga di controllo\n')
    a('`%s`\n' % riga)
    return '\n'.join(P)

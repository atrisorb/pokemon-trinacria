"""Testi fissi del blocco 4.6 (documento docs/MODULO_4/4.6_IMMAGINI_DI_LOTTA.md)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'grafica', '4.6'))
import schede46 as S  # noqa: E402

DATA = '28/10/2026'
RUOLI = {'0': 'trasparente (colore dell’originale)', '1': 'contorno', '2': 'pelle', '3': 'pelle in ombra',
         '4': 'capelli', '5': 'capelli in ombra, sopracciglia, baffi', '6': 'vestito di sopra', '7': 'sopra in ombra',
         '8': 'vestito di sotto', '9': 'sotto in ombra', '10': 'scarpe', '11': 'bianco (camicia, occhi, buste)',
         '12': 'accento A (cravatta, pochette, sciarpa, rossetto, metà della Poké Ball)',
         '13': 'accento B (cappelli, borse, cartelline, telefono, occhiali piccoli)',
         '14': 'accento C (oro, bastone, tablet, fascia rifrangente)', '15': 'occhi e lenti scure'}


def riga_finale(man):
    return ('BLOCCO COMPLETO: 4.6 — immagini di lotta ridisegnate col figurino a script (stesse schede del 4.5): '
            '%d immagini frontali (36 classi del registro 2.5 e il protagonista ragazzo e ragazza), %d dorsi (8 compagni '
            'e il protagonista, anche nelle lotte in collegamento), %d ritratti delle transizioni (9 Segretari, 4 Campioni '
            'dell’ARS, Mistretta, 5 classi di «U Sistema», protagonista), il timbro di «U Sistema» al posto della «R» '
            '(2 sprite, 5 schermate); prova di forma %d+%d immagini identiche; modifica E-GFX-05 (%d ID allenatore nelle '
            'tabelle delle transizioni); applica --blocchi 4.6 provato; regole R-GFX-38…41; 4.1 v1.1 (cifratura '
            '-encodebacktofront); medaglie, Scheda Allenatore e icone del Pokégear spostate al 4.7'
            % (len(man['fronti']), len(man['dorsi']), len(man['ritratti']),
               man['prova_forma']['files/a/0/5/8']['identici'], man['prova_forma']['files/a/0/0/6']['identici'],
               len(man['sostituzioni'])))


def _tab(intest, righe):
    out = ['| ' + ' | '.join(intest) + ' |', '|' + '---|' * len(intest)]
    for r in righe:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def _posa(p):
    if p['R'] == 'lancio':
        return 'lancio %d' % p['fase']
    if p['L'] == p['R']:
        return p['L']
    return '%s / %s' % (p['L'], p['R'])


def documento(man, prova, riga):
    P = []
    a = P.append
    a('# Modulo 4 · Blocco 4.6 — Immagini di lotta e transizioni\n')
    a('**Versione:** 1.0 · %s · **Progetto:** Pokémon Trinacria (autore: atrisorb) · **Repository di destinazione:** '
      '`F:\\Progetti\\pokeheartgold`\n' % DATA)
    a('**File del blocco:**\n')
    a(_tab(['File', 'Cosa contiene'], [
        ('`docs/MODULO_4/4.6_IMMAGINI_DI_LOTTA.md`', 'questo documento'),
        ('`docs/MODULO_4/4.6_IMMAGINI_DI_LOTTA.json`', 'dati generati: fronti, dorsi, ritratti con pose e schede, timbri, sostituzioni di codice, file con lo SHA-1, prove'),
        ('`tools/grafica/4.6/`', 'script di disegno (R-GFX-17): `figura46.py` (il figurino: tre viste), `schede46.py` (chi va dove, pose, espressioni), `comune46.py` (formati a forma invariata, cifratura), `costruisci46.py` (tutto)'),
        ('`tools/generatori/4.6/`', 'generatore di questo documento e del JSON (`gen46.py`, `text46.py`)'),
    ]) + '\n')
    a('Fonti lette nel repository: `src/pokemon.c` (`sub_02070D3C`, `TrainerClassToBackpicID`), '
      '`asm/overlay_12_battle_controller_opponent.s` (la lotta mostra la quinta voce), `src/register_hall_of_fame.c`, '
      '`asm/unk_020517A4.s` (classe → transizione), `asm/overlay_01_021EFB38.s` (tabella delle transizioni, archivio '
      '`a/1/0/9`), `asm/overlay_115.s` (Segretari, Campioni, protagonista), `asm/overlay_117.s` (classi di «U Sistema»), '
      '`asm/overlay_120.s` (transizione 46: nessun ritratto), `files/msgdata/msg/msg_0189.json` (solo il nome), '
      '`files/poketool/trainer/trainers.json`, `include/constants/trainer_class.h`, `include/constants/trainers.h`, '
      '`tools/nitrogfx/gfx.c`. Dal progetto: registro 2.5 (`classi_allenatore`, `allenatori`, `note_grafica`), '
      'trama v1.9 (R-05, R-10.2), blocchi 4.1 e 4.5.\n')

    a('## 0. In breve\n')
    a('- **Il blocco è diviso**, come il 4.4 e il 4.5: qui le **immagini di lotta** e la grafica delle **transizioni**; '
      'medaglie dei 9 Dossier, Scheda Allenatore e icone del Pokégear (testa del protagonista, vagante nello slot 2) '
      'passano alla richiesta nuova **4.7** (scaletta v2.21, 75 richieste).')
    a('- **Un figurino, tre viste.** `figura46.py` disegna dalla stessa scheda del 4.5 la figura intera di fronte '
      '(80×80), il dorso che lancia la Poké Ball (80×80) e il ritratto testa e spalle delle transizioni (96×64): '
      'stessi vestiti, colori e accessori dello sprite di campo (R-GFX-39). Niente è copiato da HeartGold.')
    a('- **%d immagini frontali** (36 classi del registro 2.5 e il protagonista, classi 0 e 1), **%d dorsi** (8 compagni '
      'e il protagonista ragazzo e ragazza, anche nelle lotte in collegamento), con lo stesso numero di fotogrammi '
      'dell’originale (1, 3 o 8 i fronti, 5 o 8 i dorsi).' % (len(man['fronti']), len(man['dorsi'])))
    a('- **Le transizioni mostravano i ritratti di HeartGold.** Le transizioni 12–19, 27 e 29–33 (capipalestra, Superquattro, '
      'Campione) e 40–44 (esecutivi del Team Rocket) mostrano un ritratto 96×64 e il nome di un allenatore fisso; la 39 '
      '(reclute) e lo sfondo delle 40–44 la «R». Qui: %d ritratti nuovi e il **timbro di «U Sistema»** (anello con '
      'una piramide a quattro gradoni, R-10.2) al posto della «R» (R-GFX-40, R-GFX-41).' % len(man['ritratti']))
    a('- **Una modifica di codice, E-GFX-05**: %d ID allenatore nelle tabelle delle transizioni '
      '(`asm/overlay_115.s`, `asm/overlay_117.s`), perché il nome scritto nella transizione è quello dell’ID della '
      'tabella, e gli ID di Trinacria non sono quelli di HeartGold.' % len(man['sostituzioni']))
    a('- **Correzione al 4.1 (v1.1).** Il quinto NCGR delle immagini degli allenatori è cifrato dall’ultima parola '
      'alla prima (`-encodebacktofront` di `nitrogfx`), non con `-scanfronttoback`: la prova di andata e ritorno del 4.1 '
      'riusciva lo stesso, ma l’immagine letta era rumore. Corretti lo strumento (`ncgr_flags`), il generatore e il '
      'documento del 4.1.\n')

    a('## 1. Come si costruisce e come si applica\n')
    a(_tab(['Passo', 'Comando (dalla cartella del progetto)', 'Esito'], [
        ('1. costruzione', '`python -I tools/grafica/4.6/costruisci46.py` (Windows, provato il 28/10/2026; solo libreria standard, 10 secondi)',
         '`GRAFICA_OK`; archivi in `build/grafica/4.6/file/`, anteprime in `build/grafica/4.6/anteprime/`'),
        ('2. prova', '`python -I tools/trinacria_gfx.py applica --blocchi 4.6 --prova <cartella vuota>`', '`GRAFICA_OK`; nessun file del repository toccato'),
        ('3. applicazione', '`python -I tools/trinacria_gfx.py applica --blocchi 4.6` (anche insieme: `--blocchi 4.2 4.3 4.4 4.5 4.6`)',
         '`GRAFICA_OK`; cambiano i 3 archivi del §3 e i 2 file `.s` della modifica E-GFX-05'),
        ('4. build', 'build del Modulo 1 (M1-02)', '`BUILD_OK`'),
    ]) + '\n')
    a('Prova di questo blocco in una cartella temporanea: %s.\n' % '; '.join(prova['righe']))

    a('## 2. Formati\n')
    a(_tab(['Cosa', 'Dove', 'Forma'], [
        ('immagini frontali', '`files/a/0/5/8`, voci 5·classe … 5·classe+4', 'NCGR a celle con un blocco di 100 tile per fotogramma (mappatura 1D da 64 KB, trasferimento in VRAM: l’animazione cambia blocco), NCLR (riga 0), NCER, NANR, NCGR «scansionato» 160×80 cifrato'),
        ('dorsi', '`files/a/0/0/6`, voci 5·dorso … (`TRAINER_BACKPIC_*`)', 'come i fronti; l’animazione è il lancio della Poké Ball'),
        ('immagine in lotta', 'quinta voce', 'metà sinistra = fotogramma 0, metà destra = fotogramma 1 (vuota con un solo fotogramma): l’usa `PokepicManager` (lotta) e l’Albo d’Oro; la prima voce l’usano gli sprite animati (ingresso dei capi, lancio)'),
        ('cifratura', 'quinta voce', 'dall’ultima parola alla prima con la chiave dell’originale; la parola finale in chiaro deve essere 0: gli ultimi 4 pixel dell’ultima riga restano trasparenti (controllo in `scrivi_allenatore`)'),
        ('ritratti delle transizioni', '`files/a/1/0/9`', 'gruppi NCLR, NCGR, NCER, NANR; il NCGR ha 96 tile (OBJ 4 bit, mappatura 1D da 32 KB) disposte dalla cella 0 in un riquadro 96×64 (un blocco 64×64 e uno 32×64)'),
        ('«R» e sfondo degli esecutivi', '`files/a/1/0/9` 153–158, 215–221', 'sprite 64×64 (156) e 128×128 (153); sfondo NCGR 216 (256 tile) con 5 schermate NSCR 217–221 e palette 215'),
    ]) + '\n')

    a('## 3. File sostituiti e modifica di codice\n')
    a(_tab(['File del repository', 'Byte', 'Voci cambiate', 'SHA-1 di HeartGold'], [
        ('`%s`' % f['destinazione'], f['byte'], '%d su %d' % (f['voci_cambiate'], f['voci']), '`%s`' % f['sha1_hg'])
        for f in man['file']]) + '\n')
    a('**E-GFX-05 — ID degli allenatori nelle transizioni.** Ogni riga della tabella cambia solo i due byte dell’ID '
      '(il resto del blocco resta uguale); `applica` la porta come sostituzione esatta del blocco con la sua etichetta.\n')
    a(_tab(['File', 'Etichetta', 'Classe', 'Transizione', 'ID HeartGold', 'ID Trinacria', 'Nome scritto'], [
        ('`%s`' % r['tabella'], '`%s`' % r['etichetta'], '`%s`' % r['classe'], r['transizione'], r['id_hg'], r['id_trinacria'],
         (r['nome'] or 'quello del registro (Modulo 6)') if r['membri'] == 1 else '«-» (allenatore 0: la classe ha %d allenatori)' % r['membri'])
        for r in man['ritratti'] if r['id_hg'] is not None]) + '\n')

    a('## 4. Regole nuove\n')
    a(_tab(['Regola', 'Titolo', 'Contenuto'], [
        ('R-GFX-38', 'Immagini degli allenatori a forma invariata',
         'Un’immagine frontale o un dorso si riscrive nelle sue cinque voci cambiando solo i pixel del NCGR a celle, la riga 0 della palette (colore 0 dell’originale) e il NCGR cifrato: stesso numero di fotogrammi, stesse celle e animazioni, chiave dell’originale, cifratura `-encodebacktofront`. Metà sinistra dell’immagine cifrata = fotogramma 0, metà destra = fotogramma 1 o vuota. Prova: tutte le immagini di HeartGold lette e riscritte identiche (§12). Gli ultimi 4 pixel in basso a destra restano trasparenti.'),
        ('R-GFX-39', 'Una scheda, tre viste',
         'Le immagini di lotta e i ritratti nascono dalle schede del 4.5 (`schede45.py`) disegnate da `figura46.py`: un personaggio ha in lotta e nella transizione gli stessi vestiti, colori e accessori dello sprite di campo. Una scheda nuova vale per tutte le viste. La palette è quella a ruoli del 4.5 (R-GFX-35).'),
        ('R-GFX-40', 'Transizioni coi ritratti',
         'Una transizione che mostra un personaggio (ritratto e nome) usa il ritratto della scheda della classe di Trinacria e l’ID dell’allenatore di quella classe (registro 2.5); se la classe ha più allenatori (esecutivi di «U Sistema», Fantasmi) l’ID è 0 e il ritratto mostra la classe. Le transizioni delle classi non usate (capipalestra di Kanto, rivale) restano di HeartGold; la 46 (Maria sul tetto, slot di Red) non ha ritratti.'),
        ('R-GFX-41', 'Il timbro di «U Sistema»',
         '«U Sistema» non ha divise né logo (trama R-10.2): dove HeartGold mostrava la «R» del Team Rocket c’è un timbro (anello con una piramide a quattro gradoni, i quattro livelli di R-10.2), disegnato coi due colori della «R» originale nella sua palette, senza cambiare colori condivisi con altra grafica.'),
    ]) + '\n')

    a('## 5. Immagini frontali\n')
    a('Fotogrammi: 1 = posa ferma; 3 = sequenza d’ingresso dei capi (fermo, indica, pugno o mano al fianco); 8 = lancio '
      'della Poké Ball di fronte (solo la classe 123, Calogero, come l’originale). Le pose sono «braccio a sinistra / '
      'braccio a destra» dell’immagine.\n')
    a(_tab(['Classe', 'Simbolo', 'Slot di HeartGold', 'Scheda (4.5)', 'Fot.', 'Pose', 'Viso', 'Aspetto'], [
        (f['classe'], '`%s`' % f['simbolo'], '`%s`' % f['simbolo_hg'], '`%s`' % f['scheda'], f['fotogrammi'],
         ', '.join(_posa(p) for p in f['pose'][:3]) + (' …' if len(f['pose']) > 3 else ''), f['espressione'],
         S.SCHEDE[f['scheda']]['perche'])
        for f in man['fronti']]) + '\n')

    a('## 6. Dorsi\n')
    a(_tab(['Dorso', 'Simbolo', 'Classe che lo usa', 'Scheda (4.5)', 'Fotogrammi', 'Fasi del lancio'], [
        (d['dorso'], '`%s`' % d['simbolo'], '`%s`' % d['classe'], '`%s`' % d['scheda'], d['fotogrammi'],
         ', '.join(str(x) for x in d['fasi'])) for d in man['dorsi']]) + '\n')
    a('Fasi del lancio (braccio a destra dell’immagine): 0 palla in mano lungo il fianco, 1 carica, 2 braccio alto dietro '
      'la testa, 3 avanti sopra la testa, 4 rilascio a braccio teso (l’ultima dei dorsi a 5 fotogrammi, tenuta a lungo), '
      '5–7 accompagnamento e chiusura. Il gioco sposta le celle dei fotogrammi 3 e seguenti (NCER dell’originale): il '
      'disegno resta nel riquadro 80×80. Gli altri dorsi (rivale, Lucia e Barry) non sono usati da Trinacria e restano.\n')

    a('## 7. Ritratti delle transizioni\n')
    a(_tab(['NCGR', 'NCLR', 'Tabella', 'Classe', 'Transizione', 'Scheda', 'Viso'], [
        (r['ncgr'], r['nclr'], '`%s`' % r['etichetta'], '`%s`' % r['classe'] if r['classe'] != 'protagonista' else 'protagonista',
         r['transizione'], '`%s`' % r['scheda'], r['espressione']) for r in man['ritratti']]) + '\n')
    a('I due ritratti del protagonista (208 ragazzo, 212 ragazza) compaiono nelle transizioni dei Campioni dell’ARS e del '
      'Presidente e hanno una sola palette (211): le due schede del 4.5 hanno gli stessi colori, e il costruttore lo '
      'controlla. Il protagonista guarda a destra, gli avversari a sinistra.\n')

    a('## 8. Il timbro\n')
    a(_tab(['Voci', 'Misura', 'Uso'], [
        (('NCGR %d, NCER %d' % (t['ncgr'], t['ncer'])) if 'ncer' in t else 'NCGR 216, NSCR 217–221, NCLR 215', t['misura'], t['uso'])
        for t in man['timbri']]) + '\n')
    sch = next((t for t in man['timbri'] if t['ncgr'] == 216), None)
    if sch:
        a('Le schermate 218, 220 e 221 avevano la «R» nel riquadro %s: il riquadro torna al fondo (riga per riga nella 221, '
          'dove passa la banda) e il timbro va al suo posto; 217 e 219 restano uguali. Le tile si rifanno tutte insieme: '
          '%d tile su %d, ognuna con la riga di palette che ha tutti i suoi colori.\n' % (sch['cornice_r'], sch['tile'], sch['su']))

    a('## 9. Ruoli della palette\n')
    a('Gli stessi del 4.5 (R-GFX-35); qui sono usati anche per il ritratto e il dorso.\n')
    a(_tab(['Indice', 'Ruolo'], sorted(RUOLI.items(), key=lambda kv: int(kv[0]))) + '\n')

    a('## 10. Anteprime\n')
    a(_tab(['File (in `build/grafica/4.6/`)', 'Righe'], [('`%s`' % x['png'], ', '.join('`%s`' % r for r in x['righe']))
                                                         for x in man['anteprime']]) + '\n')

    a('## 11. Note per gli altri blocchi\n')
    a('- **4.7 (nuova richiesta: medaglie, Scheda Allenatore e icone).** Medaglie dei 9 Dossier (dove le mostra il gioco: '
      'Scheda Allenatore e consegna), l’immagine del protagonista nella Scheda Allenatore, la testa del protagonista nella '
      'mappa del Pokégear e l’icona del vagante nello slot 2 (ancora Latias, blocco 3.3), in `pgmap_gra_00000001.png`. '
      'Il protagonista ha le schede `PROTAGONISTA_RAGAZZO` e `PROTAGONISTA_RAGAZZA` di `schede46.py`; il ritratto si può '
      'disegnare con `figura46.ritratto`.')
    a('- **Modulo 6.** I nomi degli allenatori 1, 99, 149, 198, 246, 297, 352, 412, 488, 524–527 e 552 compaiono anche '
      'nelle transizioni (devono stare nel riquadro del nome come in lotta). Nelle transizioni 40–44 (Collettu Biancu, '
      'Caporali, Cassieri, Cambiavoti, Fantasma) il nome è quello dell’allenatore 0, «-».')
    a('- **Modulo 7 (7.2).** La modifica E-GFX-05 tocca `asm/overlay_115.s` e `asm/overlay_117.s` (solo byte di dati): '
      'il build deve dare `BUILD_OK`.')
    a('- **Modulo 7 (7.4).** TASK a schermo: `costruisci46.py` → `GRAFICA_OK`, `applica --blocchi 4.6`; una lotta contro '
      'una classe di «U Sistema» (Scagnozzu: transizione 39 col timbro), contro un Segretario (ritratto, nome e ingresso '
      'a 3 fotogrammi), contro un esecutivo (Cassieri: sfondo col timbro e ritratto), contro un Campione dell’ARS e '
      'Mistretta (ritratto del protagonista, ragazzo e ragazza); il lancio della Poké Ball del protagonista e di un '
      'compagno (lotta multipla di M-EN-05); una lotta in collegamento (dorso 15/16, fronte 0/1); l’Albo d’Oro.\n')

    a('## 12. Prove\n')
    pf = man['prova_forma']
    a(_tab(['Archivio', 'Lette e riscritte identiche', 'Classi', 'Metà dell’immagine cifrata'], [
        ('`%s`' % k, '%d su %d' % (v['identici'], v['provati']), v['voci'],
         ', '.join('%s: %d' % kv for kv in sorted(v['metà_scansione'].items()))) for k, v in pf.items()]) + '\n')
    a('Le classi di `a/0/5/8` non provate (21, 101, 102, 105: celle capovolte o fotogrammi non 80×80) sono della Frontiera '
      'e del rivale, e il blocco non le tocca. Ogni archivio letto e reimpacchettato senza cambi è identico all’originale '
      '(R-GFX-09). Ogni immagine scritta viene riletta: la metà sinistra cifrata uguale al fotogramma 0.\n')

    a('## 13. Decisioni da guardare\n')
    a('- **Blocco diviso** (4.6 immagini di lotta e transizioni, 4.7 medaglie, Scheda Allenatore e icone): la scaletta passa a 75 richieste.')
    a('- **Nome «-» nelle transizioni 40–44.** Le classi Collettu Biancu, Caporali, Cassieri, Cambiavoti e Fantasma hanno '
      'più allenatori; la tabella ammette un solo ID, quindi uso lo 0. In alternativa: un allenatore per classe (nome sbagliato '
      'per gli altri) o la transizione 39 senza ritratto (cambio del registro 2.5).')
    a('- **Il timbro di «U Sistema»** (anello e piramide a quattro gradoni) al posto della «R», coi colori della «R».')
    a('- **Pose e espressioni**: capi con ingresso «indica» e «pugno», compagni e protagonista sorridenti, avversari col '
      'ghigno, Maria severa.')
    a('- **Restano di HeartGold**: le transizioni dei capipalestra di Kanto e del rivale (classi non usate), le bande di '
      'colore dietro i ritratti dei capi (astratte), «VS».\n')

    a('## 14. Codici d’errore\n')
    a(_tab(['Codice', 'Significato'], [
        ('K26', 'immagine di lotta o archivio non a forma invariata: lettura e riscrittura diverse, fotogrammi non 80×80, angolo in basso a destra non trasparente, cifratura sbagliata'),
        ('K27', 'classe del registro senza scheda, o assente'),
        ('K28', 'tabella delle transizioni non riconosciuta, classe della tabella diversa da quella dell’allenatore, ritratto non 96×64, schermata della «R» impossibile da rifare'),
        ('K00', '`applica`: file del repository che non è né l’originale né quello del blocco'),
        ('K23', '`applica`: blocco di codice da sostituire non trovato una volta sola'),
    ]) + '\n')

    a('## 15. Riga di controllo\n')
    a('`%s`' % riga)
    return '\n'.join(P) + '\n'

"""Testi del documento 4.2 (docs/MODULO_4/4.2_TILESET_EST.md). I numeri arrivano da gen42.py."""
import collections


def num(n):
    s = str(n)
    return s if len(s) <= 4 else '{:,}'.format(n).replace(',', '\u2009')


def tabella(intest, righe):
    out = ['| ' + ' | '.join(intest) + ' |', '|' + '---|' * len(intest)]
    for r in righe:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def riga_finale(d):
    m = d['man']
    return (('BLOCCO COMPLETO: 4.2 — %d celle nuove in a/0/6/5 (voci %d–%d: %d celle della matrice 0, %d modelli di '
            'paesaggio condivisi da %d celle, %d stanze di %d matrici nuove), al massimo %d poligoni; tileset condiviso '
            'della matrice 0 con %d texture (%s byte) e tileset degli interni con %d (%s byte), più le varianti gialle '
            'del polo; %d aree nuove; %d mappe con l’areaDataBank; %d varchi, %d collegamenti porta–stanza, %d punti '
            'per il Modulo 6; %d anteprime d’ingresso di %d dungeon ridisegnate; 7 regole R-GFX-18…24; '
            'trinacria_gfx.py: imd_scena, limite dei poligoni (K21), applica')
            % (len(m['celle']), m['prima_cella'], m['prima_cella'] + len(m['celle']) - 1, len(d['est']), len(d['pae']),
       sum(1 for c in m['matrice_0'] if c.get('paesaggio')), len(d['inte']), len(m['matrici']), max(d['pol']),
       len(d['sic']), num(d['b_sic']), len(d['sic']) + len(d['intx']), num(d['b_int']), len(m['aree']),
       len(m['mappe']), d['n_varchi'], len(d['coll']), d['n_punti'], len(d['ing']),
       len({x['slot'] for x in d['ing']})))


def documento(d):
    m = d['man']
    L = d['limiti']
    out = []
    w = out.append
    w('# Modulo 4 · Blocco 4.2 — Tileset e modelli 3D di Catania, Siracusa, Ragusa e Caltanissetta\n')
    w('**Versione:** 1.0 · 27/10/2026 · **Progetto:** Pokémon Trinacria (autore: atrisorb) · '
      '**Repository di destinazione:** `F:\\Progetti\\pokeheartgold`\n')
    w('**File del blocco:**\n')
    w(tabella(['File', 'Cosa contiene'], [
        ['`docs/MODULO_4/4.2_TILESET_EST.md`', 'questo documento'],
        ['`docs/MODULO_4/4.2_CELLE_EST.json`', 'dati generati: numerazione, tileset, aree, celle, matrici, area di ogni mappa, '
         '**varchi, collegamenti e punti per il Modulo 6**, anteprime d’ingresso, prova di `applica`'],
        ['`tools/grafica/4.2/`', 'script di disegno e di costruzione (R-GFX-17): `tex42.py` e `texint42.py` (texture), '
         '`motore42.py` (celle 3D), `esterni42.py` e `schede42.py` (celle della matrice 0), `interni42.py` e `stanze42.py` '
         '(stanze), `mondo42.py` (registri), `ingressi42.py` (anteprime d’ingresso), `anteprima42.py` (anteprime PNG), '
         '`costruisci42.py` (tutto)'],
        ['`tools/trinacria_gfx.py`', 'lo strumento del 4.1 con tre aggiunte: `imd_scena` (scene 3D), limite dei poligoni '
         '(K21) e comando `applica`'],
        ['`tools/generatori/4.2/`', 'generatore di questo documento e del JSON (`gen42.py`, `text42.py`)'],
    ]))
    w('\nFonti: registri 2.1–2.5 (mappe, matrici, confini percorribili, tabella degli spawn), `3.1_PIANO_INCONTRI.json` '
      '(metodi di ogni mappa), trama v1.9, documento 4.1; nel repository `src/field/fieldmap.c`, '
      '`asm/overlay_01_021E90C0.s` (porte), `include/constants/metatile_behavior.h`, `src/metatile_behavior.c`, '
      '`asm/unk_0203DB6C.s` (bancone), `src/map_preview_graphic.c`, gli archivi `a/0/6/5`, `a/0/4/2`, `a/0/4/4`, '
      '`a/0/7/0`, `bm_field.narc` e gli eventi `zone_event` di HeartGold.\n')

    w('## 0. In breve\n')
    w('- **Tutto è generato e costruito, non descritto.** `python -I tools/grafica/4.2/costruisci42.py` (Windows, circa 3 '
      'minuti) disegna le texture, mette giù le %d celle (matrice 0, paesaggio, stanze), le converte con `g3dcvtr`, '
      'controlla limiti e texture e scrive in `build/grafica/4.2/` le voci di land data, i tileset, le anteprime PNG e '
      '`manifesto.json` → `GRAFICA_OK`. Poi `python -I tools/trinacria_gfx.py applica --blocchi 4.2` porta tutto nel '
      'repository. L’esecutore non disegna nulla a mano.' % len(m['celle']))
    w('- **Matrice 0:** %d celle delle mappe e delle strade di Catania, Siracusa, Ragusa e Caltanissetta (le 20 strade che '
      'stanno in queste province) e %d celle di paesaggio attorno (mare, campagna, Etna, colline) con 4 modelli condivisi.'
      % (len(d['est']), sum(1 for c in m['matrice_0'] if c.get('paesaggio'))))
    w('- **Stanze:** %d celle per le %d matrici nuove (0288–0329) delle mappe interne, grotte e mappe aperte. Gli interni '
      'che riusano una matrice di HeartGold (Centri, case, Vermut, Radio, Distilleria, Zona Safari) restano quelli di '
      'HeartGold con la loro area.' % (len(d['inte']), len(m['matrici'])))
    w('- **Un tileset solo per tutta la matrice 0** (R-GFX-18): il gioco carica il tileset quando si entra in una mappa '
      'con un warp e non lo cambia camminando; quindi ogni cella della matrice 0 deve trovare le sue texture in un tileset '
      'comune. Il 4.2 ne usa %d nomi (%s byte); il 4.3 aggiunge i suoi allo stesso tileset.' % (len(d['sic']), num(d['b_sic'])))
    w('- **Edifici veri in 3D** (R-GFX-22): volumi (tetto, facciata, fianchi), cilindri e sagome a colore trasparente '
      'dentro il modello della cella; il Centro Pokémon è quello di HeartGold (modelli 40 e 15 di `bm_field.narc`).')
    w('- **Per il Modulo 6** il JSON dà, per ogni mappa, i varchi (porte, tappeti, scale, imbocchi, cancelli) con le '
      'coordinate dei warp, le coppie da collegare e i punti della trama (allenatori, cartelli, oggetti) già su caselle '
      'raggiungibili: %d varchi, %d collegamenti, %d punti.' % (d['n_varchi'], len(d['coll']), d['n_punti']))
    w('- **Anteprime d’ingresso** (R-MAP note dei registri): %d immagini di %d dungeon ridisegnate, con l’NSCR nuovo.'
      % (len(d['ing']), len({x['slot'] for x in d['ing']})))
    w('- **Tinta gialla del polo:** le varianti gialle del tileset e le aree `SICILIA_GIALLO`, `APERTI_4_2_GIALLO` sono '
      'già costruite; si usano solo se nel 7.x il meteo 9 non mostra la nebbia (`applica --polo-giallo`).\n')

    w('## 1. Come si costruisce e come si applica\n')
    w(tabella(['Passo', 'Comando (dalla cartella del progetto)', 'Esito'], [
        ['1. costruzione', '`python -I tools/grafica/4.2/costruisci42.py` (Windows: serve `g3dcvtr.exe`, documento 4.1 §2); '
         'con il repository già modificato aggiungere `--rom <ROM originale>`', '`GRAFICA_OK`; file in `build/grafica/4.2/`'],
        ['2. prova', '`python -I tools/trinacria_gfx.py applica --blocchi 4.2 --prova <cartella vuota>`',
         '`GRAFICA_OK`; nessun file del repository toccato'],
        ['3. applicazione', '`python -I tools/trinacria_gfx.py applica --blocchi 4.2` (dopo il 4.3: `--blocchi 4.2 4.3`)',
         '`GRAFICA_OK`; cambiano `files/a/0/6/5`, `a/0/4/4`, `a/0/4/2`, la matrice 0, le matrici 0288–0329, '
         '`src/data/map_headers.h` (solo `.areaDataBank`) e le anteprime d’ingresso'],
        ['4. collaudo', '`python -I tools/trinacria_gfx.py --selftest --rom <ROM originale>`', '`SELFTEST_OK`'],
    ]))
    w('\n`applica` parte sempre dagli archivi originali (repository intatto, altrimenti `--rom`), quindi si può rilanciare: '
      'il risultato è lo stesso. Le voci nuove vanno in coda (R-GFX-09) nell’ordine dei manifesti; il tileset condiviso '
      'della matrice 0 dei blocchi seguenti sostituisce quello del 4.2 allo stesso indice. Nella matrice 0 cambiano solo '
      'modelli e altitudini delle celle del blocco: le intestazioni le scrive il Modulo 2 (R-MAP-05). Le matrici nuove si '
      'scrivono intere (formato R-MAP-13) e devono essere già nel `meson.build` (riga del registro).\n')
    p = d['prova']
    w('Prova eseguita dal generatore (`applica --prova` in una cartella temporanea): %s; dopo l’applicazione `a/0/6/5` ha '
      '%d voci, `a/0/4/4` %d, `a/0/4/2` %d; ogni cella della matrice 0 del blocco ha il suo modello e nessuna cita '
      'texture assenti dal tileset condiviso (K20: %d).\n' % ('; '.join(p['righe']), p['voci_a065'], p['voci_a044'],
                                                                p['voci_a042'], p['k20_matrice_0']))

    w('## 2. Numerazione\n')
    w(tabella(['Archivio', 'Voci di HeartGold', 'Voci del 4.2', 'Il 4.3 parte da'], [
        ['`files/a/0/6/5` (celle)', '0–675', '%d–%d' % (m['prima_cella'], m['prima_cella'] + len(m['celle']) - 1),
         m['prima_cella'] + len(m['celle'])],
        ['`files/a/0/4/4` (tileset)', '0–105', '%d–%d' % (m['primo_tileset'], m['primo_tileset'] + len(m['tileset']) - 1),
         '%d (e riscrive 106 e 107, i tileset condivisi)' % (m['primo_tileset'] + len(m['tileset']))],
        ['`files/a/0/4/2` (aree)', '0–105', '%d–%d' % (m['prima_area'], m['prima_area'] + len(m['aree']) - 1),
         m['prima_area'] + len(m['aree'])],
    ]))
    w('\n### 2.1 Tileset\n')
    w(tabella(['Indice', 'Chiave', 'Texture', 'Byte', 'Uso'], [
        [t['indice'], '`%s`' % t['chiave'], t['texture'], num(t['byte']),
         {'SICILIA': 'tutte le celle della matrice 0 (condiviso, R-GFX-18)',
          'SICILIA_GIALLO': 'variante gialla del precedente (tinta del polo, §9)',
          'INTERNI_4_2': 'stanze, grotte e mappe aperte del 4.2: le texture della matrice 0 più %d degli interni' % len(d['intx']),
          'INTERNI_4_2_GIALLO': 'variante gialla del precedente'}[t['chiave']]] for t in m['tileset']]))
    w('\nVRAM: tileset condiviso + texture degli edifici del set 91 = %s byte; tileset degli interni %s byte (limite %s, '
      'R-GFX-13). Il tileset condiviso ha %d texture su %d e %s byte su %s: **al 4.3 restano %d texture e %s byte**.\n'
      % (num(d['vram_sic']), num(d['vram_int']), num(L['area_vram']), len(d['sic']), L['tileset_texture'],
         num(d['b_sic']), num(L['tileset_byte']), L['tileset_texture'] - len(d['sic']), num(L['tileset_byte'] - d['b_sic'])))
    w('### 2.2 Aree (`a/0/4/2`, 8 byte: texture degli edifici, tileset, texture animate, esterno, luce)\n')
    w(tabella(['Indice', 'Chiave', 'Tileset', 'Texture edifici', 'Esterno', 'Luce', 'Per'], [
        [a['indice'], '`%s`' % a['chiave'], a['tileset'], a['tex_edifici'], a['esterno'], a['luce'],
         {'SICILIA': 'mappe e strade della matrice 0 (set 91: il più piccolo con il Centro Pokémon)',
          'SICILIA_GIALLO': 'Augusta e Priolo con `--polo-giallo`',
          'INTERNI_4_2': 'interni (set 65, vuoto, come gli interni di HeartGold)',
          'GROTTE_4_2': 'grotte (set 85, vuoto; esterno 1, luce 0 come le grotte di HeartGold)',
          'APERTI_4_2': 'mappe aperte e miste (set 20, vuoto; luce del giorno)',
          'APERTI_4_2_GIALLO': 'polo (pontili, sala controllo e torcia) con `--polo-giallo`'}[a['chiave']]]
        for a in m['aree']]))
    ma = d['mappe_area']
    w('\nArea scritta in `areaDataBank` (voce `AREA-<simbolo>` dei registri, R-MAP-08): %s. «HG» = interno su una matrice '
      'di HeartGold: prende l’area delle mappe HeartGold che usano quella matrice (Centri: 26), così le texture del '
      'modello ci sono (R-GFX-12); la Zona Safari tiene i valori dello slot.\n'
      % ', '.join('%s %d' % kv for kv in sorted(ma.items())))

    w('## 3. Regole nuove\n')
    w(tabella(['Regola', 'Titolo', 'Contenuto'], [
        ['R-GFX-18', 'Tileset unico della matrice 0',
         'Il tileset dell’area si carica una volta, quando il campo si apre dopo un warp (`AreaDataManager_Alloc` in '
         '`src/field/fieldmap.c:658`), e non cambia camminando da una mappa all’altra. In HeartGold 25 coppie di mappe '
         'confinanti della matrice 0 hanno aree diverse e le celle vicine citano texture assenti nell’altro tileset '
         '(per esempio Route 5 → Saffron: 10 nomi su 14). In Trinacria tutte le mappe della matrice 0 usano lo stesso '
         'tileset (`SICILIA`, indice 106; la variante gialla 107 ha gli stessi nomi): ogni nome citato da una cella della '
         'matrice 0 esiste lì. Il 4.3 non crea un altro tileset per la matrice 0: aggiunge texture a questo '
         '(budget al §2.1) e lo ricostruisce con tutte le texture del 4.2 e le sue.'],
        ['R-GFX-19', 'Varchi sui confini',
         'Su ogni lato con un confine percorribile (registri, `confini_percorribili`) il passaggio è largo 6 caselle, '
         'dalla 13 alla 18 del lato; fra due celle della stessa mappa dalla 8 alla 23. Gli altri confini hanno un ostacolo '
         'di 2 caselle (palazzi, muro, alberi, roccia o recinzione, secondo il tema) o il mare (R-MAP-06). Così le celle del '
         '4.2 e del 4.3 combaciano senza guardarsi.'],
        ['R-GFX-20', 'Paesaggio attorno alle mappe',
         'Le celle senza mappa che toccano una cella del blocco (anche di spigolo), e le «#» dei registri fino a due celle, '
         'ricevono uno di 4 modelli condivisi: mare, campagna, Etna, colline (tipo scelto in `mondo42.py`: «mare» per il '
         'Golfo di Catania, la costa ionica, la costa iblea e il Golfo di Gela). Tutte le caselle sono bloccate e '
         'l’intestazione resta `MAP_EVERYWHERE`: il mare dei registri («.» accanto alla costa) si vede invece del vuoto, ma '
         'non si naviga fuori dalle mappe. È l’unico cambio a R-MAP-05: le «.» lontane restano senza modello.'],
        ['R-GFX-21', 'Collegamenti delle stanze',
         'Ogni stanza ha un «giù» e, se serve, un «su». La prima stanza di una mappa ha il tappeto d’uscita in basso '
         '(`0x65` WARP_ENTRANCE_SOUTH, come gli interni di HeartGold); le stanze seguenti hanno una scala nel muro nord a '
         'sinistra (giù) e una a destra (su), comportamento `0x6E` WARP_NORTH; nelle mappe aperte giù e su sono le caselle '
         '15 e 16 dei bordi sud e nord. Coppie: su della stanza k ↔ giù della k+1; su dell’ultima ↔ giù della mappa figlia; '
         'giù della prima ↔ porta esterna. Le coppie sono già scritte nel JSON (`collegamenti`).'],
        ['R-GFX-22', 'Edifici, porte e Centro',
         'Gli edifici sono volumi dentro il modello della cella (nessun modello nuovo in `bm_field.narc`). La porta è '
         'disegnata sulla facciata; la sua casella è bloccata con il comportamento `0x69` DOOR, come in HeartGold: '
         'senza un modello animato il gioco fa solo la dissolvenza (`ov01_021E9374`: nessuna porta trovata → '
         '`FieldMap_FadeScreen`, stato 6). Imbocchi di grotte e cancelli sono una casella libera `0x6E` coperta dalla '
         'facciata. Il Centro Pokémon è quello di HeartGold: corpo `bm_field` 40 a 24 unità a nord della porta, porta '
         '`bm_field` 15 a 1,73 unità a sud (misurati su 19 Centri), porta a (16,19), atterraggio (16,20) (R-MAP-14), '
         'set di texture degli edifici 91; i Centri senza volo hanno la porta allo stesso posto.'],
        ['R-GFX-23', 'Comportamenti delle caselle',
         'Valori usati (enum di `metatile_behavior.h`, uso misurato nelle celle di HeartGold): 0x00 normale, 0x02 erba alta '
         '(solo nelle mappe con «G» nel piano 3.1), 0x06 albero da Bottintesta (bloccato), 0x08 pavimento di grotta, 0x10 '
         'acqua dolce, 0x15 mare, 0x20 ghiaccio (celle frigorifere di Ibla, Grotta del Gelo), 0x21 sabbia, 0x4B parete da '
         'Scalaroccia (Etna Sud, P-04), 0x65 tappeto d’uscita, 0x69 porta, 0x6E varco verso nord, 0x80 bancone (si parla '
         'attraverso: `FieldSystem_GetFacingObject`). Collisione 0x00 libera, 0x80 bloccata.'],
        ['R-GFX-24', 'Poligoni',
         'Il modello di una cella ha al massimo %d poligoni, il massimo di HeartGold (K21, misurato dal collaudo). '
         'Nel 4.2 la cella più ricca ne ha %d.' % (L['poligoni_cella'], max(d['pol']))],
    ]))

    w('\n## 4. Scene 3D (`imd_scena`)\n')
    w('Un modello di cella è una lista di quadrilateri: terreno (caselle uguali vicine fuse in rettangoli), volumi '
      '(tetto, facciata sud, fianchi est e ovest; il lato nord non si vede mai), cilindri a 8 lati (serbatoi, torri, '
      'faraglioni, faro), sagome verticali (alberi, lampioni, oggetti; più sagome uguali in fila diventano un solo '
      'quadrilatero) e pannelli delle porte mezza unità davanti alla facciata. Un texel vale un’unità del mondo, quindi '
      'una texture 16×16 copre una casella e una 32×32 quattro; il terreno ha le coordinate di texture legate alla '
      'posizione, senza giunte fra rettangoli; le facciate partono dal basso. Le sagome hanno `color0_mode="transparency"` '
      '(provato: `transparent` fa fallire `g3dcvtr`). Stessa intestazione, stessa scala e stessi materiali dell’IMD '
      'provato in gioco nel 4.1. `g3dcvtr` non accetta percorsi con lettere accentate: `g3d_run` lavora in una cartella '
      'temporanea. Il collaudo dello strumento prova una scena con terreno, volume e sagoma.\n')

    w('## 5. Texture\n')
    w('Disegnate da `tex42.py` e `texint42.py` (R-GFX-17), con un generatore pseudocasuale che dipende solo dal nome: '
      'stesso nome, stesso disegno. Al massimo 16 colori della scala 555 (R-GFX-03), indice 0 trasparente nelle sagome.\n')
    gruppi = collections.OrderedDict([
        ('terreni', d['sic'][:24]), ('muri e facciate', d['sic'][24:36]), ('tetti', d['sic'][36:39]),
        ('porte e imbocchi', d['sic'][39:44]), ('sagome', d['sic'][44:]), ('interni (solo tileset degli interni)', d['intx'])])
    w(tabella(['Gruppo', 'Texture'], [[k, ', '.join('`%s`' % n for n in v)] for k, v in gruppi.items()]))
    w('\nTemi delle celle esterne (`esterni42.py`): %s. Ogni tema dice terreno di base, strade, piazze, vicoli, ostacolo '
      'dei confini, riempimento (palazzi, case con giardini, campi, bosco, sciara, calanchi, industria), facciate, tetti, '
      'altezze e oggetti lungo le strade.\n' % ', '.join('`%s`' % t for t in d['temi']))

    w('## 6. Celle della matrice 0\n')
    w('Una scheda per cella in `schede42.py`: tema, edifici con la porta verso un interno, monumenti, gruppi di oggetti, '
      'acque e punti della trama; lati, mare e Centro vengono dai registri. Il motore (`esterni42.py`) dipinge mare e riva, '
      'mette gli ostacoli dei confini e i varchi, il Centro, gli edifici (porta a sud, casella davanti libera), traccia '
      'strade e vicoli col percorso più breve, riempie, decora, aggiunge l’erba alta e controlla che varchi, porte e punti '
      'siano raggiungibili da ogni varco (altrimenti la cella non si costruisce). Anteprime PNG di ogni cella in '
      '`build/grafica/4.2/anteprime/` e panoramica `matrice_0_blocco_4_2.png`.\n')
    righe = []
    for c in d['est']:
        x, y = int(c['chiave'][2:4]), int(c['chiave'][5:7])
        vs = [v for v in m['varchi'].get(c['mappa'], []) if v['cella'] == c['chiave']]
        porte = ', '.join('%s (%d,%d)%s' % (v['tipo'], v['x'] % 32, v['z'] % 32,
                                            ' → `%s`' % v['verso'][4:] if v.get('verso') and v['verso'].startswith('MAP_')
                                            else (' → Centro' if v.get('verso') == 'CENTRO_POKEMON' else ''))
                          for v in vs) or '—'
        righe.append(['(%d,%d)' % (x, y), '`%s`' % c['mappa'][4:], c['titolo'], c['voce'], c['poligoni'], porte])
    w(tabella(['Cella', 'Mappa', 'Contenuto', 'Voce', 'Poligoni', 'Varchi (casella locale)'], righe))
    tipi = collections.Counter(c.get('paesaggio') for c in m['matrice_0'] if c.get('paesaggio'))
    w('\nPaesaggio: %s (voci %s).\n' % (', '.join('%s %d celle' % kv for kv in sorted(tipi.items())),
                                         ', '.join('%s %d' % (c['chiave'], c['voce']) for c in d['pae'])))

    w('## 7. Stanze\n')
    w('Generate da `interni42.py` con la tabella `stanze42.py`: per ogni mappa le celle della matrice (da ovest a est, come '
      '«stanze» dei registri) e in ogni cella una o più stanze. Stanza chiusa: pavimento, muro nord alto con le scale, '
      'muri laterali, muro sud basso col tappeto; oggetti del preset messi solo se non separano le caselle chiave. '
      'Mappa aperta: una cella esterna senza confini percorribili. Il laboratorio di Modica fa da Centro (R-MAP-14): '
      'tappeto a (8,19), bancone di cura alla riga 12, ritorno a (8,13). Le 5 mappe del Palazzo di Cemento hanno la stessa '
      'matrice (R-MAP-13): piano dispari a ovest, pari a est.\n')
    w(tabella(['Preset', 'Pavimento', 'Pareti', 'Oggetti'], [
        ['`%s`' % k, '`%s`' % v['pav'], '`%s`' % v['par'], ', '.join('%s ×%d' % o for o in v['ogg'])]
        for k, v in d['preset'].items()]))
    w('')
    righe = []
    for mt in m['matrici']:
        righe.append(['`%s`' % mt['file'], '%d×%d' % (mt['larghezza'], mt['altezza']), ', '.join(str(v) for v in mt['voci']),
                      ', '.join('`%s`' % x[4:] for x in mt['mappe'])])
    w(tabella(['Matrice', 'Misure', 'Voci', 'Mappe'], righe))

    w('\n## 8. Per il Modulo 6: varchi, collegamenti, punti\n')
    w('Nel JSON, sezione `varchi`: per ogni mappa le caselle di warp con tipo (`porta`, `uscita`, `scala`, `imbocco`, '
      '`cancello`, `varco`, `arrampicata`), coordinate **assolute nella matrice della mappa** (come gli eventi di HeartGold: '
      'nelle mappe della matrice 0, 32·colonna + x), ruolo (giù/su) e nota. Sezione `collegamenti`: %d coppie già decise '
      '(porta esterna ↔ tappeto della stanza, scala ↔ scala, porta ↔ warp dell’interno HeartGold riusato letto dagli '
      'eventi dello slot); il Modulo 6 scrive i due warp di ogni coppia con queste coordinate. Sezione `punti`: %d caselle '
      'raggiungibili per allenatori, cartelli, oggetti e scene della trama, col riferimento (M-, S-, E-, ST-, P-…). Il '
      'treno della Circumetnea si prende con uno script dal punto `binario_circumetnea` di Randazzo; l’Isola delle Correnti '
      'col punto `bassa_marea` di Portopalo (script). Le porte delle mappe chiuse durante la storia (Palazzo di Giustizia) '
      'esistono: le chiude il Modulo 6 col cartello. Non hanno coppie nel JSON, e va bene così: il primo piano della '
      'casa del protagonista e la Zona Safari di Vendicari tengono i warp dei loro slot di HeartGold.\n'
      % (len(d['coll']), d['n_punti']))

    w('## 9. Tinta gialla del polo petrolchimico\n')
    w('Varianti gialle (`ingiallisci` in `tex42.py`: stessi indici, colori spostati del 32 %% verso il giallo nella scala '
      '555) del tileset condiviso e di quello degli interni, con le aree `SICILIA_GIALLO` e `APERTI_4_2_GIALLO`. Se nel 7.x '
      'il meteo 9 non mostra la nebbia (documento 4.1 §10), `applica --polo-giallo` scrive quelle aree per Augusta, '
      'Priolo, pontili e sala controllo. Effetto voluto: entrando in quelle mappe con un warp tutta la vista è gialla, e '
      'resta gialla camminando fino al warp successivo (R-GFX-18).\n')

    w('## 10. Anteprime d’ingresso\n')
    righe = []
    for slot in sorted({x['slot'] for x in d['ing']}):
        xs = [x for x in d['ing'] if x['slot'] == slot]
        righe.append(['`%s`' % slot, '`%s`' % xs[0]['mappa'][4:], xs[0]['scena'], ', '.join(x['ora'] for x in xs),
                      max(x['tile_distinti'] for x in xs), max(x['colori'] for x in xs)])
    w(tabella(['Slot HeartGold', 'Mappa', 'Scena', 'Ore', 'Tile distinti', 'Colori'], righe))
    w('\nOgni immagine: PNG 256×192 a 8 bit come l’originale (tile distinti in alto, il resto a indice 0) e NSCR con '
      'l’intestazione dell’originale e la mappa nuova (tile ripetuti e capovolti). Il build converte il PNG con le opzioni '
      'del `meson.build` (R-GFX-08); l’NSCR è binario e si copia. Controllo `png --come` sull’originale: superato.\n')

    w('## 11. Strumento\n')
    w(tabella(['Aggiunta', 'Cosa fa'], [
        ['`imd_scena(quadrilateri, cartella, nome, trasparenti)`', 'IMD di una scena 3D (§4)'],
        ['`nsbmd_poligoni`, limite `poligoni_cella`', 'poligoni del modello (K21, R-GFX-24); il collaudo lo rimisura'],
        ['`g3d_run`', 'ora lavora in una cartella temporanea senza accenti'],
        ['`applica --blocchi … [--prova DIR] [--polo-giallo] [--rom R]`', 'porta i manifesti nel repository (§1)'],
        ['`--selftest`', 'in più: limite dei poligoni e scena 3D con sagoma trasparente → `SELFTEST_OK`'],
    ]))

    w('\n## 12. Note per gli altri blocchi\n')
    w('- **4.3.** Copia `tools/grafica/4.2/` in `tools/grafica/4.3/` (regola dei generatori): cambiano schede, stanze, '
      'zona del blocco in `mondo42.py` (province AG, TP, PA, EN, ME e le altre 20 strade), numerazione (prima cella %d, '
      'primo tileset %d, prima area %d) e la lista delle texture nuove. Il tileset `SICILIA` (e `SICILIA_GIALLO`) si '
      'ricostruisce con le 69 texture del 4.2 **più** quelle del 4.3, stessi nomi e stesso disegno (si importano da '
      '`tex42.py`), e il manifesto del 4.3 lo dà con la stessa chiave. Varchi alle caselle 13–18 (R-GFX-19). Le celle di '
      'paesaggio già nel manifesto del 4.2 non si ridisegnano. Le mappe del vento (`SEQ_TP_CRETTO_VENTO`, '
      '`SEQ_PA_CAPACI_MEMORIA`) non hanno piastre sonore (5.3, 5.4): il 4.2 non ne mette nessuna.'
      % (m['prima_cella'] + len(m['celle']), m['primo_tileset'] + len(m['tileset']), m['prima_area'] + len(m['aree'])))
    w('- **4.4.** Nessun legame nuovo.')
    w('- **Modulo 6.** Warp e punti dal JSON (§8). Le scale del Palazzo di Cemento: lo stesso modello per i 5 piani doppi. '
      'Le stanze hanno le caselle chiave libere; gli oggetti di scena (Pokémon di «U Sistema», R-GFX-15) vanno sui punti '
      'o su caselle libere vicine.')
    w('- **Modulo 7 (7.4).** TASK: `costruisci42.py` → `GRAFICA_OK`; `applica --prova` e poi `applica` → `GRAFICA_OK`; '
      'build; a schermo: Corso Italia (cella nuova con volumi e sagome, nord in alto, Centro di HeartGold col suo corpo e '
      'la porta), una porta senza modello animato (dissolvenza), un tappeto d’uscita e una scala, il passaggio a piedi '
      'Via Etnea → Duomo (tileset condiviso: niente texture sbagliate), l’erba alta di Galermo, il ghiaccio delle celle '
      'frigorifere, la parete di Scalaroccia di Etna Sud, un’anteprima d’ingresso (Monti Rossi), e, se serve, la tinta '
      'gialla di Augusta.\n')

    w('## 13. Codici d’errore\n')
    w('Gli stessi del 4.1 (K00–K21). Nuovi casi: K16 per una cella che il motore non riesce a costruire (posto mancante, '
      'porta o varco non raggiungibile), K21 per i poligoni, K05 per un’area o una mappa che `applica` non trova, K04 per '
      'una matrice disegnata con un numero di celle diverso dal registro.\n')
    return '\n'.join(out)

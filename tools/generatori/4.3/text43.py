"""Testi del documento 4.3 (docs/MODULO_4/4.3_TILESET_OVEST.md). I numeri arrivano da gen43.py."""
import collections


def num(n):
    s = str(n)
    return s if len(s) <= 4 else '{:,}'.format(n).replace(',', '\u2009')


def tabella(intest, righe):
    out = ['| ' + ' | '.join(intest) + ' |', '|' + '---|' * len(intest)]
    for r in righe:
        out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    return '\n'.join(out)


def n_pae(m):
    return sum(1 for c in m['matrice_0'] if c.get('paesaggio'))


def riga_finale(d):
    m = d['man']
    return (('BLOCCO COMPLETO: 4.3 — %d celle nuove in a/0/6/5 (voci %d–%d: %d celle della matrice 0, %d modello di '
             'paesaggio nuovo, %d celle di paesaggio, %d stanze e celle aperte di %d matrici nuove, isole comprese), al '
             'massimo %d poligoni; tileset condiviso della matrice 0 ricostruito con %d texture (%d del 4.2 + %d nuove, %s '
             'byte) agli indici 106–107 e tileset degli interni con le %d texture usate (%s byte) al 110; %d aree nuove; '
             '%d mappe con l’areaDataBank; %d varchi, %d collegamenti, %d punti per il Modulo 6; %d anteprime d’ingresso di '
             '%d mappe; 4 regole R-GFX-25…28; applica --blocchi 4.2 4.3 provato')
            % (len(m['celle']), m['prima_cella'], m['prima_cella'] + len(m['celle']) - 1, len(d['est']), len(d['pae']),
               n_pae(m), len(d['inte']), len(m['matrici']), max(d['pol']), len(d['sic42']) + len(d['sic43']),
               len(d['sic42']), len(d['sic43']), num(d['b_sic']), len(d['nomi_int']), num(d['b_int']), len(m['aree']),
               len(m['mappe']), d['n_varchi'], len(d['coll']), d['n_punti'], len(d['ing']),
               len({x['slot'] for x in d['ing']})))


def documento(d):
    m = d['man']
    L = d['limiti']
    out = []
    w = out.append
    nsic = len(d['sic42']) + len(d['sic43'])
    w('# Modulo 4 · Blocco 4.3 — Tileset e modelli 3D di Agrigento, Trapani, Palermo, Enna e Messina\n')
    w('**Versione:** 1.0 · 27/10/2026 · **Progetto:** Pokémon Trinacria (autore: atrisorb) · '
      '**Repository di destinazione:** `F:\\Progetti\\pokeheartgold`\n')
    w('**File del blocco:**\n')
    w(tabella(['File', 'Cosa contiene'], [
        ['`docs/MODULO_4/4.3_TILESET_OVEST.md`', 'questo documento'],
        ['`docs/MODULO_4/4.3_CELLE_OVEST.json`', 'dati generati: numerazione, tileset (coi nomi), aree, celle, matrici, area '
         'di ogni mappa, **varchi, collegamenti e punti per il Modulo 6**, anteprime d’ingresso, prova di `applica`'],
        ['`tools/grafica/4.3/`', 'script copiati dal 4.2 e adattati (R-GFX-17): `tex43.py` e `texint43.py` (texture nuove; '
         'quelle del 4.2 restano in `tools/grafica/4.2/tex42.py` e `texint42.py`), `motore43.py`, `esterni43.py` e '
         '`schede43.py` (celle della matrice 0), `interni43.py` e `stanze43.py` (stanze, mappe aperte, isole), `mondo43.py` '
         '(registri e matrice 0 del 4.2), `ingressi43.py`, `anteprima43.py`, `costruisci43.py` (tutto)'],
        ['`tools/generatori/4.3/`', 'generatore di questo documento e del JSON (`gen43.py`, `text43.py`)'],
    ]))
    w('\nFonti: registri 2.1–2.5, `3.1_PIANO_INCONTRI.json`, trama v1.9, documenti 4.1 e 4.2 (con '
      '`4.2_CELLE_EST.json`: celle e paesaggio già messi nella matrice 0), nel repository `src/map_preview_graphic.c`, gli '
      'archivi `a/0/6/5`, `a/0/4/2`, `a/0/4/4`, `a/0/7/0` e gli eventi `zone_event` degli interni di HeartGold riusati. '
      'Nessuna regola del 4.2 cambia: R-GFX-18…24 valgono anche qui.\n')

    w('## 0. In breve\n')
    w('- **Tutto è generato e costruito, come nel 4.2.** `python -I tools/grafica/4.3/costruisci43.py` (Windows) mette giù '
      'le %d celle, le converte con `g3dcvtr`, controlla limiti e texture e scrive `build/grafica/4.3/manifesto.json` → '
      '`GRAFICA_OK`. Poi `python -I tools/trinacria_gfx.py applica --blocchi 4.2 4.3` porta i due blocchi nel repository '
      'in un colpo solo.' % len(m['celle']))
    w('- **Matrice 0:** %d celle delle mappe dell’ovest e delle altre 20 strade, e %d celle di paesaggio attorno '
      '(%s). Il paesaggio usa i 4 modelli del 4.2 più uno nuovo, «bosco», per i Nebrodi.'
      % (len(d['est']), n_pae(m), ', '.join('%s %d' % kv for kv in sorted(collections.Counter(
          c['paesaggio'] for c in m['matrice_0'] if c.get('paesaggio')).items()))))
    w('- **Stanze e isole:** %d celle per le %d matrici nuove (0330–0383): interni, grotte, mappe aperte e le quattro '
      'isole (Lampedusa, Favignana, Eolie, Pantelleria), che sono esterni su una matrice propria (R-GFX-26).'
      % (len(d['inte']), len(m['matrici'])))
    w('- **Tileset condiviso ricostruito** (R-GFX-18): `SICILIA` (106) e `SICILIA_GIALLO` (107) hanno ora %d texture: le %d '
      'del 4.2, disegnate dallo stesso codice, più %d nuove (%s byte, il 4.2 ne usava %s). `applica` lo scrive allo stesso '
      'indice, quindi anche le celle del 4.2 lo trovano (provato: K20 = 0 su tutte le celle della matrice 0 dei due blocchi).'
      % (nsic, len(d['sic42']), len(d['sic43']), num(d['b_sic']), num(d['b42'])))
    w('- **Tileset degli interni per uso** (R-GFX-25): `INTERNI_4_3` (110) contiene solo le %d texture che le celle del '
      'tileset citano davvero, non tutta la matrice 0 come nel 4.2.' % len(d['nomi_int']))
    w('- **Per il Modulo 6** il JSON dà %d varchi, %d collegamenti già decisi, %d casi da completare (sezione '
      '`collegamenti_modulo_6`) e %d punti della trama su caselle raggiungibili.'
      % (d['n_varchi'], len(d['coll']), len(m['collegamenti_modulo_6']), d['n_punti']))
    w('- **Anteprime d’ingresso:** %d immagini delle %d mappe dell’ovest che stanno su uno slot con l’anteprima.\n'
      % (len(d['ing']), len({x['slot'] for x in d['ing']})))

    w('## 1. Come si costruisce e come si applica\n')
    w(tabella(['Passo', 'Comando (dalla cartella del progetto)', 'Esito'], [
        ['1. costruzione', '`python -I tools/grafica/4.2/costruisci42.py` e `python -I tools/grafica/4.3/costruisci43.py` '
         '(Windows, `g3dcvtr.exe`, documento 4.1 §2); col repository già modificato aggiungere `--rom <ROM originale>`',
         '`GRAFICA_OK` due volte; file in `build/grafica/4.2/` e `build/grafica/4.3/`'],
        ['2. prova', '`python -I tools/trinacria_gfx.py applica --blocchi 4.2 4.3 --prova <cartella vuota>`',
         '`GRAFICA_OK`; nessun file del repository toccato'],
        ['3. applicazione', '`python -I tools/trinacria_gfx.py applica --blocchi 4.2 4.3`',
         '`GRAFICA_OK`; cambiano `files/a/0/6/5`, `a/0/4/4`, `a/0/4/2`, la matrice 0, le matrici 0288–0383, '
         '`src/data/map_headers.h` (solo `.areaDataBank`) e le anteprime d’ingresso'],
        ['4. collaudo', '`python -I tools/trinacria_gfx.py --selftest --rom <ROM originale>`', '`SELFTEST_OK`'],
    ]))
    w('\nL’ordine dei blocchi conta: il manifesto del 4.3 comincia alla voce %d, cioè dopo le celle del 4.2 (altrimenti '
      'K01). Il tileset `SICILIA` del 4.3 ha la stessa chiave di quello del 4.2 e lo sostituisce all’indice 106 (e '
      '`SICILIA_GIALLO` al 107); le aree del 4.2 restano com’erano e puntano già lì.\n' % m['prima_cella'])
    p = d['prova']
    w('Prova eseguita dal generatore (`applica --blocchi 4.2 4.3 --prova` in una cartella temporanea): %s; dopo '
      'l’applicazione `a/0/6/5` ha %d voci, `a/0/4/4` %d, `a/0/4/2` %d; ogni cella della matrice 0 dei due blocchi ha il suo '
      'modello e nessuna cita texture assenti dal tileset condiviso ricostruito (K20: 4.2 %d, 4.3 %d).\n'
      % ('; '.join(p['righe']), p['voci_a065'], p['voci_a044'], p['voci_a042'], p['k20_matrice_0']['4.2'],
         p['k20_matrice_0']['4.3']))

    w('## 2. Numerazione\n')
    w(tabella(['Archivio', 'Voci di HeartGold', 'Voci del 4.2', 'Voci del 4.3', 'Il blocco seguente parte da'], [
        ['`files/a/0/6/5` (celle)', '0–675', '676–869', '%d–%d' % (m['prima_cella'], m['prima_cella'] + len(m['celle']) - 1),
         m['prima_cella'] + len(m['celle'])],
        ['`files/a/0/4/4` (tileset)', '0–105', '106–109', '106 e 107 riscritti, 110 nuovo', 111],
        ['`files/a/0/4/2` (aree)', '0–105', '106–111', '%d–%d' % (m['prima_area'], m['prima_area'] + len(m['aree']) - 1),
         m['prima_area'] + len(m['aree'])],
    ]))
    w('\n### 2.1 Tileset\n')
    w(tabella(['Indice', 'Chiave', 'Texture', 'Byte', 'Uso'], [
        [t['indice'], '`%s`' % t['chiave'], t['texture'], num(t['byte']),
         {'SICILIA': 'tutte le celle della matrice 0, del 4.2 e del 4.3 (condiviso, R-GFX-18): sostituisce quello del 4.2',
          'SICILIA_GIALLO': 'variante gialla del precedente (tinta del polo del 4.2): sostituisce quella del 4.2',
          'INTERNI_4_3': 'stanze, grotte, mappe aperte e isole del 4.3: solo le texture usate (R-GFX-25)'}[t['chiave']]]
        for t in m['tileset']]))
    w('\nVRAM: tileset condiviso + texture degli edifici del set 91 = %s byte; tileset degli interni + set 91 = %s byte '
      '(limite %s, R-GFX-13). Il tileset condiviso ha %d texture su %d e %s byte su %s: ai blocchi seguenti, se mai '
      'servisse, restano %d texture e %s byte.\n'
      % (num(d['vram_sic']), num(d['vram_int']), num(L['area_vram']), nsic, L['tileset_texture'], num(d['b_sic']),
         num(L['tileset_byte']), L['tileset_texture'] - nsic, num(L['tileset_byte'] - d['b_sic'])))
    w('### 2.2 Aree nuove (`a/0/4/2`)\n')
    w(tabella(['Indice', 'Chiave', 'Tileset', 'Texture edifici', 'Esterno', 'Luce', 'Per'], [
        [a['indice'], '`%s`' % a['chiave'], a['tileset'], a['tex_edifici'], a['esterno'], a['luce'],
         {'INTERNI_4_3': 'interni (set 65, vuoto, come gli interni di HeartGold)',
          'GROTTE_4_3': 'grotte (set 85, vuoto; esterno 1, luce 0)',
          'APERTI_4_3': 'mappe aperte e isole (set 91: il Centro Pokémon di HeartGold a Lampedusa; luce del giorno)'}[a['chiave']]]
        for a in m['aree']]))
    ma = d['mappe_area']
    w('\nArea scritta in `areaDataBank` (R-MAP-08): %s. «SICILIA» è l’area 106 del 4.2 (tutta la matrice 0); «HG» = interno '
      'su una matrice di HeartGold (Centri, case, porti, Lega dell’ARS, Fiera): l’area delle mappe HeartGold che la '
      'usano.\n' % ', '.join('%s %d' % kv for kv in sorted(ma.items())))

    w('## 3. Regole nuove\n')
    w(tabella(['Regola', 'Titolo', 'Contenuto'], [
        ['R-GFX-25', 'Tileset degli interni per uso',
         'Il tileset degli interni di un blocco contiene solo le texture che le sue stanze, grotte, mappe aperte e isole '
         'citano (`costruisci43.py` le conta dopo aver messo giù le celle), non tutta la matrice 0. Così resta sotto i '
         'limiti di `a/0/4/4` anche col tileset condiviso cresciuto, e il controllo K20 di ogni cella vale lo stesso.'],
        ['R-GFX-26', 'Isole',
         'Lampedusa, Favignana, le Eolie e Pantelleria sono esterni su una matrice propria (registri: profilo ISOLA): si '
         'disegnano come mappe aperte (una cella per colonna della matrice), area `APERTI_4_3` col set 91. Il «giù» della '
         'prima cella (caselle 15–16 del bordo sud) è l’approdo: il traghetto o l’aliscafo ci porta con uno script '
         '(Modulo 6). Il Centro di Lampedusa ha la porta a (16,19) della prima cella come nelle città; la sua coppia '
         'si trova con `accesso_da` del registro, non con le coordinate del Pokégear.'],
        ['R-GFX-27', 'Mare oltre il bordo della matrice',
         'A nord della costa tirrenica messinese (riga 0, da Sant’Agata a Torre Faro) e a est dello Stretto (colonna 46) '
         'il lato della cella è mare, anche se lì la matrice finisce: `mondo43.py` dà il tipo «mare» alle coordinate fuori '
         'dalla matrice. Vale solo per il disegno dei lati: fuori dalla matrice non c’è nessun modello (R-MAP-05 invariata). '
         'Allo stesso modo le «.» fra la costa e i Nebrodi sono «bosco» e quelle fra Corleone e l’Agrigentino «colline», '
         'non mare: è la geografia, non il bordo, a decidere (R-GFX-20).'],
        ['R-GFX-28', 'Luoghi della memoria',
         'Capaci, Casa Memoria, Portella della Ginestra, la Porta d’Europa, il Grande Cretto, il CIDMA e il Presidio Civico '
         '(R-05): temi sobri (`memoria`, `cretto`, preset `casa` e `archivio`), niente erba alta, niente oggetti comici, '
         'nessun punto per allenatori; solo i punti di raccoglimento della trama. Il Cretto è un labirinto di blocchi '
         'bianchi senza selvatici.'],
    ]))

    w('\n## 4. Scene 3D e motore\n')
    w('Stesso motore del 4.2 (§4 del documento 4.2), copiato in `motore43.py` con due aggiunte: i cilindri possono '
      'partire da un’altezza (`y0`: cupole sui tetti, pilone sulla base) e ci sono i terreni nuovi (`tufo`, `marna`, '
      '`salina`, `cordolo`, `maiolica`). Prefabbricati nuovi in `esterni43.py`: tempio dorico (stilobate, peristilio '
      'con la sagoma `colonnato` in fila, trabeazione; o rovina con i rocchi a terra), saline con mulino e mucchi di sale, '
      'condotta dell’acquedotto con le autobotti, casello autostradale, pilone dello Stretto (cilindro di 160 unità), '
      'chiesa normanna con le cupole rosse, rupe, piloni interrotti dell’A19; riempimento «cretto» per il labirinto di Burri.\n')

    w('## 5. Texture\n')
    w('Le %d texture del 4.2 si disegnano ancora con `tools/grafica/4.2/tex42.py` e `texint42.py` (stesso nome, stesso '
      'disegno); quelle nuove stanno in `tex43.py` (matrice 0) e `texint43.py` (interni) e si registrano nello stesso '
      'catalogo. Al massimo 16 colori della scala 555, indice 0 trasparente nelle sagome.\n' % len(d['sic42']))
    s43 = d['sic43']
    gruppi = collections.OrderedDict([
        ('terreni (matrice 0)', s43[:4]), ('muri, facciate e tetti (matrice 0)', s43[4:13]), ('sagome (matrice 0)', s43[13:]),
        ('interni (solo tileset degli interni)', d['intx'])])
    w(tabella(['Gruppo', 'Texture nuove'], [[k, ', '.join('`%s`' % n for n in v)] for k, v in gruppi.items()]))
    nuovi = [t for t in d['temi'] if t not in d['temi42']]
    w('\nTemi nuovi delle celle esterne (`esterni43.py`): %s.\n' % ', '.join('`%s`' % t for t in nuovi))

    w('## 6. Celle della matrice 0\n')
    w('Una scheda per cella in `schede43.py` (le celle senza scheda prendono il tema della mappa, `TEMA_MAPPA`); lati, mare '
      'e Centro vengono dai registri. I Centri senza punto di volo (Canicattì, Castelvetrano, Castellammare, Alcamo, '
      'Sant’Agata, Termini, Nicosia, Piazza Armerina) hanno la porta a (16,19) della cella indicata da `worldMapX/Y` del '
      'Centro. Palazzo dei Normanni ha il volo ma non il Centro: la porta a (16,19) è l’ingresso della Lega dell’ARS. '
      'Anteprime in `build/grafica/4.3/anteprime/` e panoramica `matrice_0_blocco_4_3.png`.\n')
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
    voci = {}
    for c in m['matrice_0']:
        if c.get('paesaggio'):
            voci[c['paesaggio']] = (c['voce'], c['blocco_modello'])
    w('\nPaesaggio: %s. Modelli: %s.\n' % (', '.join('%s %d celle' % kv for kv in sorted(tipi.items())),
                                          ', '.join('%s voce %d (%s)' % (k, v[0], v[1]) for k, v in sorted(voci.items()))))

    w('## 7. Stanze, mappe aperte e isole\n')
    w('Generate da `interni43.py` con la tabella `stanze43.py`, come nel 4.2 (R-GFX-21). Preset nuovi del 4.3:\n')
    nuovi_p = ('convento', 'ipogeo', 'cisterna', 'cantiere', 'attico', 'grotta_marna', 'stufe', 'cortile', 'stalla',
               'vulcano', 'abisso', 'duomo_oro', 'grotta_tufo', 'villa_romana')
    w(tabella(['Preset', 'Pavimento', 'Pareti', 'Oggetti'], [
        ['`%s`' % k, '`%s`' % v['pav'], '`%s`' % v['par'], ', '.join('%s ×%d' % o for o in v['ogg'])]
        for k, v in d['preset'].items() if k in nuovi_p]))
    w('')
    righe = []
    for mt in m['matrici']:
        righe.append(['`%s`' % mt['file'], '%d×%d' % (mt['larghezza'], mt['altezza']), ', '.join(str(v) for v in mt['voci']),
                      ', '.join('`%s`' % x[4:] for x in mt['mappe'])])
    w(tabella(['Matrice', 'Misure', 'Voci', 'Mappe'], righe))

    w('\n## 8. Per il Modulo 6: varchi, collegamenti, punti\n')
    w('Stesse sezioni del 4.2 (`varchi`, `collegamenti`, `punti`, coordinate assolute nella matrice della mappa). '
      '%d coppie già decise. In più `collegamenti_modulo_6`: %d porte verso interni di HeartGold riusati il cui slot non '
      'ha un warp verso la matrice 0 da cui leggere le coordinate (tabella qui sotto): il Modulo 6 sceglie il warp '
      'd’ingresso dello slot. Le mappe di scena (traghetto per Lampedusa, aliscafi per Favignana e le Eolie, traghetto '
      'dello Stretto, pullman delle 5:40) si prendono con uno script dai punti `molo_aliscafo` (Milazzo), '
      '`imbarco_traghetto` (Messina), `fermata_pullman` (Trapani) e dagli imbarchi di HeartGold riusati; l’arrivo sulle '
      'isole è il «giù» della prima cella (R-GFX-26). Da Via della Lega alla Lega dell’ARS: il «su» dell’ultimo piano va '
      'al warp dell’atrio di HeartGold (coppia nel JSON); l’ingresso dalla Lega (porta di Palazzo dei Normanni → cancello '
      'HeartGold → primo piano di Via della Lega) lo completa il Modulo 6. %d punti.\n'
      % (len(d['coll']), len(m['collegamenti_modulo_6']), d['n_punti']))
    if m['collegamenti_modulo_6']:
        w(tabella(['Da', 'Casella', 'Verso', 'Nota'], [
            ['`%s`' % x['da']['mappa'][4:], '(%d,%d)' % (x['da']['x'], x['da']['z']), '`%s`' % x['a']['mappa'][4:], x['nota']]
            for x in m['collegamenti_modulo_6']]))
        w('')

    w('## 9. Anteprime d’ingresso\n')
    righe = []
    for slot in sorted({x['slot'] for x in d['ing']}):
        xs = [x for x in d['ing'] if x['slot'] == slot]
        righe.append(['`%s`' % slot, '`%s`' % xs[0]['mappa'][4:], xs[0]['scena'], ', '.join(x['ora'] for x in xs),
                      max(x['tile_distinti'] for x in xs), max(x['colori'] for x in xs)])
    w(tabella(['Slot HeartGold', 'Mappa', 'Scena', 'Ore', 'Tile distinti', 'Colori'], righe))
    w('\nSolo tre mappe dell’ovest stanno su uno slot con l’anteprima (registri, `simbolo_hg_sostituito`); gli altri slot '
      'con l’anteprima non sono usati da Trinacria. Stesso formato del 4.2: PNG 256×192 a 8 bit e NSCR con l’intestazione '
      'dell’originale; controllo `png --come` sull’originale superato.\n')

    w('## 10. Strumento\n')
    w('`trinacria_gfx.py` non cambia: `applica --blocchi 4.2 4.3` sostituisce il tileset con la stessa chiave allo stesso '
      'indice e salta le aree già scritte (comportamento del 4.2, ora provato con due blocchi).\n')

    w('## 11. Decisioni da guardare\n')
    w('- **Paesaggio della costa tirrenica e dello Stretto** (R-GFX-27): i lati sul bordo della matrice sono mare; il '
      'registro non lo diceva (fuori dalla matrice non c’è nulla).')
    w('- **Nebrodi e Sicani** (R-GFX-27): le «.» del registro fra la costa e Sperlinga/Nicosia e fra Corleone e '
      'l’Agrigentino non sono mare ma monti.')
    w('- **Lampedusa:** il Centro sta sull’isola alla porta (16,19) della prima cella; l’area `APERTI_4_3` usa il set 91.')
    w('- **Stile procedurale**, come nel 4.2: le schede seguono la trama, il contorno è generato.\n')

    w('## 12. Note per gli altri blocchi\n')
    w('- **4.4.** Nessun legame nuovo.')
    w('- **Modulo 6.** Warp e punti dal JSON (§8). Mappe di scena e isole con gli script indicati.')
    w('- **Modulo 7 (7.4).** TASK: `costruisci42.py` e `costruisci43.py` → `GRAFICA_OK`; `applica --blocchi 4.2 4.3 '
      '--prova` e poi `applica` → `GRAFICA_OK`; build; a schermo: il passaggio a piedi da Randazzo (4.2) a Patti (4.3) '
      'col tileset condiviso ricostruito (niente texture sbagliate), la Valle dei Templi (tempio, colonnato con '
      'trasparenze), il pilone di Torre Faro (cilindro alto), una porta del Centro senza volo (Canicattì), le saline '
      'dello Stagnone, Lampedusa (Centro sull’isola), il labirinto del Cretto, un’anteprima d’ingresso (Valle dei Templi).\n')

    w('## 13. Codici d’errore\n')
    w('Gli stessi del 4.1 e del 4.2 (K00–K21). Nuovo caso K04: una matrice nuova del 4.3 senza stanze in `stanze43.py`.\n')
    return '\n'.join(out)

"""Blocco 4.5 — schede dei personaggi e tabelle dei fotogrammi degli sprite di campo.

Ogni scheda descrive il personaggio per omino45.disegna(): capelli, sopra, sotto, accessori, corporatura e i
colori dei ruoli. Le descrizioni vengono dalla trama v1.9 (C-01…C-08, M-CT-01/02, P-10, R-10.2, M-*-segreterie,
M-EN-04/06, P-03) e dal registro 2.5 (slot). Luoghi e persone reali non compaiono: tutti i personaggi con un
ruolo nel malaffare sono inventati (trama R-05).

Tabelle dei fotogrammi: il numero è il suffisso della texture («seven4.5»). Il significato di ogni numero
(direzione e movimento) è letto guardando gli sprite di HeartGold nell'ordine dei nomi: 1–4 di spalle,
5–8 di fronte, 9–12 a sinistra, 13–16 a destra (fermo, passo, fermo, altro passo)."""

# --------------------------------------------------------------------------------------------- colori

PELLE = dict(chiara=(246, 213, 180), media=(238, 189, 148), olivastra=(213, 164, 115),
             abbronzata=(189, 131, 90), pallida=(205, 213, 222))
CAPELLI = dict(nero=(41, 32, 32), castano=(98, 57, 32), castano_chiaro=(148, 98, 57), biondo=(230, 197, 106),
               grigio=(148, 148, 156), bianco=(222, 222, 230), mogano=(148, 49, 41), rosa=(246, 172, 205),
               brizzolato=(98, 98, 106))
NERO, BIANCO, GRIGIO = (41, 41, 49), (238, 238, 230), (123, 123, 131)
ORO, ARGENTO = (238, 197, 49), (164, 164, 172)
SCARPE_NERE, SCARPE_MARRONI, SCARPE_BIANCHE = (41, 32, 41), (106, 57, 32), (222, 222, 230)


def col(pelle, capelli, sopra, sotto, scarpe, a1=(205, 41, 41), a2=(65, 65, 74), a3=ORO, **k):
    d = dict(pelle=PELLE[pelle], capelli=CAPELLI[capelli], sopra=sopra, sotto=sotto, scarpe=scarpe,
             A1=a1, A2=a2, A3=a3)
    d.update(k)
    return d


# --------------------------------------------------------------------------------------------- protagonista

PROTAGONISTA = {
    'ragazzo': dict(chi='Protagonista (ragazzo), 28 anni, Catania «bene» di Corso Italia',
                    capelli='pettinati', sopra='giacca', sotto='pantaloni', accessori=('pochette',),
                    colori=col('media', 'castano', (41, 57, 115), (205, 180, 131), SCARPE_MARRONI,
                               a1=(230, 57, 41), a2=(74, 74, 82), a3=(156, 156, 164)),
                    perche='giacca blu da laureato LUISS sopra la camicia bianca, pantaloni chiari, pochette rossa'),
    'ragazza': dict(chi='Protagonista (ragazza), 28 anni, Catania «bene» di Corso Italia',
                    capelli='coda', sopra='giacca', sotto='pantaloni', accessori=('pochette', 'rossetto'),
                    colori=col('media', 'castano', (41, 57, 115), (205, 180, 131), SCARPE_MARRONI,
                               a1=(230, 57, 41), a2=(74, 74, 82), a3=(156, 156, 164)),
                    perche='stessi vestiti del ragazzo; capelli lunghi raccolti in una coda con l’elastico rosso, rossetto'),
}

# famiglie di sprite del protagonista: (MMODEL del ragazzo, MMODEL della ragazza, tabella, uso)
FAMIGLIE = [
    ('MMODEL_HERO', 'MMODEL_HEROINE', 'eroe32', 'cammina e corre'),
    ('MMODEL_HERO_2', 'MMODEL_HEROINE_2', 'eroe32', 'seconda copia di HeartGold, stessa tabella'),
    ('MMODEL_CYCLEHERO', 'MMODEL_CYCLEHEROINE', 'bici24', 'in bicicletta (`SH Scassatu`), salto dai gradini'),
    ('MMODEL_SWIMHERO', 'MMODEL_SWIMHEROINE', 'surf4', 'seduto sul Pokémon in `Aliscafu` (Surf)'),
    ('MMODEL_FISHINGHERO', 'MMODEL_FISH_HEROINE', 'pesca16', 'pesca con le canne'),
    ('MMODEL_LADDERHERO', 'MMODEL_LADDERHEROINE', 'scala6', 'sale e scende le scale a pioli'),
    ('MMODEL_SAVEHERO', 'MMODEL_SAVEHEROINE', 'salva2', 'mentre salva'),
    ('MMODEL_BANZAIHERO', 'MMODEL_BANZAIHEROINE', 'banzai12', 'braccia alzate (adatto al palco di M-EN-07)'),
    ('MMODEL_SHAKEHERO', 'MMODEL_SHAKEHEROINE', 'spinta8', '`Bottintesta` sugli alberi'),
]
# sprite del protagonista che restano di HeartGold: travestimento Rocket, Pokéathlon, statua, Lucas
NON_USATI = ['MMODEL_RHERO', 'MMODEL_RHEROINE', 'MMODEL_RBANZAIHERO', 'MMODEL_PKTHHERO', 'MMODEL_PKTHHEROINE',
             'MMODEL_STATUEHERO', 'MMODEL_STATUEHEROINE', 'MMODEL_SAVERHERO', 'MMODEL_SAVERHEROINE',
             'MMODEL_POKEHERO', 'MMODEL_POKEHEROINE', 'MMODEL_SPHERO', 'MMODEL_SPHEROINE',
             'MMODEL_WATERHERO', 'MMODEL_WATERHEROINE']

# --------------------------------------------------------------------------------------------- personaggi

PERSONAGGI = {
    'SPRITE_TRN_TURI': dict(
        capelli='ricci', sopra='maglia', maniche='corte', sotto='pantaloni', accessori=('barba',),
        colori=col('media', 'nero', (238, 131, 41), (65, 90, 148), SCARPE_BIANCHE),
        perche='maglietta arancione come gli agrumi del padre, jeans, ricci e barba'),
    'SPRITE_TRN_ORAZIO': dict(
        capelli='rasati', sopra='tuta_lavoro', sotto='tuta', accessori=('cintura',),
        colori=col('olivastra', 'nero', (49, 82, 148), (49, 82, 148), SCARPE_NERE, a3=(90, 82, 74)),
        perche='tuta blu da meccanico dell’officina di via Plebiscito'),
    'SPRITE_TRN_CHRISTIAN': dict(
        capelli='ciuffo', sopra='felpa', sotto='pantaloni', accessori=('cuffie', 'collana'),
        colori=col('media', 'nero', (49, 49, 57), (57, 65, 98), SCARPE_BIANCHE, a2=(213, 49, 49)),
        perche='felpa nera, cuffie rosse da DJ della movida, ciuffo col gel'),
    'SPRITE_TRN_CHANTAL': dict(
        capelli='lunghi', sopra='maglia', maniche='corte', sotto='pantaloni',
        accessori=('telefono', 'rossetto'),
        colori=col('media', 'rosa', (213, 57, 148), (41, 41, 49), SCARPE_BIANCHE, a1=(205, 49, 82), a2=(57, 57, 65)),
        perche='capelli rosa, maglietta fucsia, leggings e telefono per i video'),
    'SPRITE_TRN_MARIA': dict(
        capelli='caschetto', sopra='tailleur', sotto='pantaloni', accessori=('occhiali', 'cartellina'),
        colori=col('chiara', 'nero', (74, 74, 90), (74, 74, 90), SCARPE_NERE, a2=(123, 98, 65)),
        perche='la PM: tailleur antracite, caschetto nero, occhiali e fascicolo'),
    'SPRITE_TRN_TOTO': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', pancia=1,
        accessori=('cravatta', 'baffi', 'bottoni_oro'),
        colori=col('olivastra', 'grigio', (32, 41, 90), (32, 41, 90), SCARPE_NERE, a1=(156, 32, 41)),
        perche='commesso dell’ARS: giacca blu coi bottoni dorati, baffi grigi'),
    'SPRITE_TRN_CALOGERO': dict(
        capelli='corti', sopra='canotta', sotto='pantaloni', accessori=('paglia', 'baffi'),
        colori=col('abbronzata', 'nero', (230, 230, 222), (123, 90, 57), SCARPE_MARRONI, a1=(106, 74, 41),
                   a3=(222, 197, 123)),
        perche='contadino e pescatore di Licata: cappello di paglia, canottiera, pelle bruciata dal sole'),
    'SPRITE_TRN_PIPPO': dict(
        capelli='calvo', sopra='righe', sotto='pantaloni', accessori=('berretto_lana', 'barba'),
        colori=col('abbronzata', 'bianco', (41, 74, 148), (106, 106, 115), SCARPE_NERE, a2=(41, 49, 98),
                   a3=(205, 49, 49)),
        perche='da 35 anni al pilone di Torre Faro: maglia a righe, berretto di lana, barba bianca'),
    'SPRITE_TRN_GRAZIELLA': dict(
        capelli='cotonati', sopra='abito', sotto='gonna', accessori=('perle', 'rossetto'),
        colori=col('chiara', 'biondo', (41, 106, 115), (41, 106, 115), SCARPE_NERE, a1=(205, 57, 74)),
        perche='la madre: piega cotonata, abito petrolio e filo di perle'),
    'SPRITE_TRN_PROF_STRANO': dict(
        capelli='calvo', sopra='giacca', sotto='pantaloni', accessori=('barba', 'occhiali', 'cravatta'),
        colori=col('chiara', 'bianco', (139, 98, 57), (106, 106, 115), SCARPE_MARRONI, a1=(57, 123, 74),
                   a2=(57, 49, 41)),
        perche='zoologo in pensione: giacca di tweed, barba bianca, occhiali'),
    'SPRITE_TRN_NUNZIO': dict(
        capelli='corti', sopra='tuta_lavoro', sotto='tuta', pancia=1, accessori=('baffi', 'cintura'),
        colori=col('olivastra', 'brizzolato', (90, 106, 82), (90, 106, 82), SCARPE_NERE, a3=(74, 65, 57)),
        perche='il fratello di Orazio: tuta verde da officina, baffi, più robusto'),
    'SPRITE_TRN_MISTRETTA': dict(
        capelli='pettinati', sopra='giacca', doppiopetto=True, sotto='pantaloni', pancia=1,
        accessori=('cravatta', 'pochette'),
        colori=col('chiara', 'grigio', (32, 32, 57), (32, 32, 57), SCARPE_NERE, a1=(189, 32, 41), a3=ORO),
        perche='l’On. Mistretta: doppiopetto blu notte, cravatta rossa, capelli grigi tirati indietro'),
    'SPRITE_TRN_FANTASMA': dict(
        capelli='corti', sopra='cappotto', sotto='pantaloni', accessori=('fedora', 'occhiali_sole'),
        colori=col('pallida', 'grigio', (123, 123, 148), (82, 82, 98), SCARPE_NERE, a1=(57, 57, 74),
                   a2=(82, 82, 98), a3=(164, 172, 197)),
        perche='i Fantasmi della Prima Repubblica: cappotto e cappello grigi, pelle pallida, occhiali scuri'),
    'SPRITE_TRN_SEGRETARIO_CT': dict(
        capelli='riporto', sopra='camice', sotto='pantaloni', pancia=1,
        accessori=('occhiali', 'stetoscopio'),
        colori=col('chiara', 'castano', (238, 238, 238), (41, 57, 106), SCARPE_NERE, a2=(41, 57, 106),
                   a3=(123, 131, 139)),
        camice_interno='A2',
        perche='Dott. Calì, il Ras delle cliniche convenzionate: camice bianco sopra il completo, stetoscopio'),
    'SPRITE_TRN_SEGRETARIO_SR': dict(
        capelli='corti', sopra='giacca', doppiopetto=True, sotto='pantaloni',
        accessori=('capitano', 'barba', 'bottoni_oro'),
        colori=col('olivastra', 'grigio', (32, 41, 90), (230, 230, 222), SCARPE_NERE, a2=(32, 41, 90)),
        perche='Comm. Spataro, «U Baruni dû Portu»: blazer blu coi bottoni d’oro e berretto da armatore'),
    'SPRITE_TRN_SEGRETARIO_RG': dict(
        capelli='calvo', sopra='polo', maniche='corte', sotto='pantaloni', pancia=1,
        accessori=('collana', 'occhiali_sole'),
        colori=col('abbronzata', 'brizzolato', (41, 98, 57), (65, 90, 148), SCARPE_MARRONI),
        perche='Cav. Occhipinti, re dei TIR dell’ortofrutta: polo verde, catena d’oro, occhiali da sole'),
    'SPRITE_TRN_SEGRETARIO_CL': dict(
        capelli='corti', sopra='giacca', sotto='pantaloni', accessori=('casco', 'cravatta', 'occhiali'),
        colori=col('media', 'brizzolato', (106, 106, 115), (106, 106, 115), SCARPE_NERE, a1=(41, 82, 156),
                   a2=(238, 238, 238)),
        perche='Ing. Lo Monaco, commissario da 22 anni: completo grigio e casco bianco da collaudo'),
    'SPRITE_TRN_SEGRETARIO_AG': dict(
        capelli='corti', sopra='camicia', maniche='corte', sotto='pantaloni', pancia=1,
        accessori=('casco', 'baffi', 'cartellina'),
        colori=col('abbronzata', 'nero', (115, 156, 205), (205, 180, 131), SCARPE_MARRONI, a2=(238, 197, 49)),
        perche='Geom. Iacono, il re del cemento: camicia azzurra, casco giallo e progetti sotto il braccio'),
    'SPRITE_TRN_SEGRETARIO_TP': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', accessori=('cravatta', 'barba', 'occhiali'),
        colori=col('media', 'nero', (32, 32, 41), (32, 32, 41), SCARPE_NERE, a1=(106, 49, 123), a2=(148, 148, 156)),
        perche='Avv. Asaro, «Gran Maestro» della loggia dei parchi eolici: abito nero, cravatta viola'),
    'SPRITE_TRN_SEGRETARIO_ME': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', accessori=('cravatta', 'occhiali', 'valigetta'),
        colori=col('chiara', 'castano_chiaro', (148, 156, 164), (98, 106, 115), SCARPE_NERE, a1=(74, 148, 205),
                   a2=(106, 65, 41)),
        perche='Dott. Sturiale, AD delle partecipate: completo grigio chiaro e valigetta'),
    'SPRITE_TRN_SEGRETARIO_PA': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', pancia=1,
        accessori=('cravatta', 'baffi', 'collana', 'occhiali_sole'),
        colori=col('olivastra', 'nero', (106, 41, 49), (57, 41, 41), SCARPE_NERE, a1=(238, 197, 49)),
        perche='On. Totò Scaduto, il collettore della Conca d’Oro: giacca bordeaux, cravatta gialla, catena'),
    'SPRITE_TRN_SEGRETARIO_EN': dict(
        capelli='calvo', sopra='camicia', sotto='pantaloni', accessori=('gilet', 'cravatta', 'occhiali', 'cartellina'),
        colori=col('chiara', 'grigio', (230, 230, 222), (98, 98, 106), SCARPE_NERE, a1=(106, 65, 41),
                   a2=(74, 90, 65)),
        perche='Dott. La Rosa, presidente della Commissione Elettorale: gilet, occhiali, registro dei timbri'),
    'SPRITE_TRN_CAMPIONE_ARS_1': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', accessori=('cravatta', 'baffi', 'bastone'),
        colori=col('chiara', 'bianco', (230, 222, 197), (230, 222, 197), SCARPE_MARRONI, a1=(139, 32, 41),
                   a3=(106, 65, 41)),
        perche='Don Tanino, il Gattopardo: abito crema, baffi bianchi, bastone'),
    'SPRITE_TRN_CAMPIONE_ARS_2': dict(
        capelli='caschetto', sopra='tailleur', sotto='pantaloni', accessori=('occhiali', 'tablet'),
        colori=col('chiara', 'biondo', (123, 131, 148), (123, 131, 148), SCARPE_NERE, a2=(57, 57, 65),
                   a3=(57, 65, 82)),
        perche='l’Assessora Tecnica venuta dal Nord: tailleur grigio, caschetto biondo, tablet'),
    'SPRITE_TRN_CAMPIONE_ARS_3': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', bicolore=True, accessori=(),
        colori=col('media', 'castano', (41, 82, 156), (57, 57, 74), SCARPE_NERE, a1=(213, 82, 41)),
        perche='il Re delle Liste Civiche e dei Trasformisti: giacca metà blu e metà arancione'),
    'SPRITE_TRN_CAMPIONE_ARS_4': dict(
        capelli='riporto', sopra='cappotto', sotto='pantaloni', pancia=1, accessori=('sciarpa', 'occhiali'),
        colori=col('chiara', 'grigio', (41, 41, 49), (41, 41, 49), SCARPE_NERE, a1=(139, 32, 106),
                   a2=(164, 164, 172)),
        perche='il «Cardinale» delle Opere Pubbliche e dei Rifiuti: cappotto nero e sciarpa porpora'),
}

CLASSI = {
    'SPRITE_TRN_SCAGNOZZU': dict(
        capelli='rasati', sopra='camicia', sotto='pantaloni', accessori=('auricolare', 'occhiali_sole', 'collana'),
        colori=col('olivastra', 'nero', (41, 41, 49), (41, 41, 49), SCARPE_NERE, a2=(90, 90, 98)),
        perche='buttafuori e scagnozzo: camicia nera, auricolare, occhiali scuri'),
    'SPRITE_TRN_INFILTRATA': dict(
        capelli='coda', sopra='giacca', sotto='pantaloni', accessori=('occhiali_sole', 'telefono'),
        colori=col('media', 'castano', (41, 41, 49), (41, 41, 49), SCARPE_NERE, a1=(148, 41, 57), a2=(98, 98, 106)),
        perche='giacca nera, coda, telefono: ascolta e riferisce'),
    'SPRITE_TRN_CAMBIAVOTI': dict(
        capelli='cotonati', sopra='abito', sotto='gonna', accessori=('buste', 'collana', 'rossetto'),
        colori=col('chiara', 'mogano', (164, 41, 106), (164, 41, 106), SCARPE_NERE, a1=(205, 41, 57)),
        perche='la capobastone davanti al seggio: abito vistoso, buste coi cinquanta euro'),
    'SPRITE_TRN_CASSIERI': dict(
        capelli='riporto', sopra='giacca', sotto='pantaloni', accessori=('occhiali', 'cravatta', 'valigetta'),
        colori=col('chiara', 'castano', (106, 106, 115), (106, 106, 115), SCARPE_NERE, a1=(57, 74, 123),
                   a2=(41, 41, 49)),
        perche='il ragioniere del pizzo: completo grigio, occhiali, valigetta delle buste'),
    'SPRITE_TRN_CAPORALI': dict(
        capelli='corti', sopra='maglia', sotto='pantaloni', accessori=('casco', 'alta_visibilita', 'telefono'),
        colori=col('abbronzata', 'nero', (230, 106, 32), (65, 90, 148), SCARPE_NERE, a2=(238, 131, 41),
                   a3=(197, 230, 49)),
        perche='capo-cantiere: casco e maglia arancioni con la fascia rifrangente, ricetrasmittente'),
    'SPRITE_TRN_COLLETTU_BIANCU': dict(
        capelli='pettinati', sopra='camicia', sotto='pantaloni', accessori=('cravatta', 'tablet'),
        colori=col('chiara', 'castano_chiaro', (238, 238, 238), (41, 57, 106), SCARPE_NERE, a1=(41, 82, 156),
                   a3=(57, 65, 82)),
        perche='il colletto bianco: camicia bianca, cravatta blu, tablet coi bilanci'),
    'SPRITE_TRN_PORTABORSE': dict(
        capelli='corti', sopra='giacca', sotto='pantaloni', accessori=('occhiali', 'cravatta', 'valigetta'),
        colori=col('media', 'castano', (65, 82, 131), (65, 82, 131), SCARPE_NERE, a1=(156, 41, 41), a2=(106, 65, 41)),
        perche='il portaborse: giacca blu, occhiali, la borsa dell’onorevole'),
    'SPRITE_TRN_FIGGHIU_DI_PAPA': dict(
        capelli='ciuffo', sopra='polo', maniche='corte', sotto='pantaloni', accessori=('occhiali_sole', 'maglione'),
        colori=col('media', 'biondo', (238, 148, 172), (230, 222, 197), SCARPE_MARRONI, a1=(41, 57, 115)),
        perche='polo rosa, maglione sulle spalle, occhiali da sole, mocassini'),
    'SPRITE_TRN_PARCHEGGIATURI': dict(
        capelli='corti', sopra='canotta', sotto='pantaloni', accessori=('berretto', 'borsello', 'fischietto'),
        colori=col('abbronzata', 'nero', (222, 222, 213), (57, 57, 65), SCARPE_NERE, a2=(41, 74, 148),
                   a3=(222, 222, 230)),
        perche='il parcheggiatore abusivo: cappellino, canottiera, borsello a tracolla, fischietto'),
    'SPRITE_TRN_ASSESSURI': dict(
        capelli='pettinati', sopra='giacca', sotto='pantaloni', pancia=1, accessori=('cravatta', 'telefono'),
        colori=col('chiara', 'grigio', (41, 57, 106), (41, 57, 106), SCARPE_NERE, a1=(57, 131, 74), a2=(41, 41, 49)),
        perche='l’assessore: completo blu, cravatta verde, sempre al telefono'),
    'SPRITE_TRN_ZAUDDU': dict(
        capelli='rasati', sopra='felpa', sotto='pantaloni', accessori=('berretto_rovescio', 'collana'),
        colori=col('media', 'nero', (123, 123, 131), (41, 41, 49), SCARPE_BIANCHE, a2=(205, 49, 49), a3=ORO),
        perche='il bulletto: felpa grigia, cappellino al contrario, catenina'),
    'SPRITE_TRN_BUDDACI': dict(
        capelli='corti', sopra='righe', sotto='pantaloni', pancia=1, accessori=('berretto_lana', 'barba'),
        colori=col('abbronzata', 'nero', (41, 74, 148), (41, 57, 98), SCARPE_NERE, a2=(189, 49, 49)),
        perche='lo spaccone del porto: maglia a righe, berretto di lana, barba'),
}

# --------------------------------------------------------------------------------------------- fotogrammi


def _p(d, tipo, fase=0):
    return dict(dir=d, tipo=tipo, fase=fase)


DIR4 = ('su', 'giu', 'sx', 'dx')


def tabella(nome):
    """{numero del fotogramma: posa}."""
    t = {}
    if nome in ('cammina16', 'eroe32'):
        for k, d in enumerate(DIR4):
            for j, p in enumerate((_p(d, 'fermo'), _p(d, 'passo', 0), _p(d, 'fermo'), _p(d, 'passo', 1))):
                t[1 + 4 * k + j] = p
        if nome == 'eroe32':
            for k, d in enumerate(DIR4):
                for j, p in enumerate((_p(d, 'corsa_fermo'), _p(d, 'corsa', 0), _p(d, 'corsa_fermo'),
                                       _p(d, 'corsa', 1))):
                    t[17 + 4 * k + j] = p
    elif nome == 'bici24':
        for k, d in enumerate(DIR4):
            for j, f in enumerate((0, 1, 0, 2)):
                t[1 + 4 * k + j] = _p(d, 'bici', f)
        for n, (d, f) in zip(range(17, 25), (('sx', 0), ('sx', 1), ('dx', 0), ('dx', 1),
                                             ('su', 0), ('giu', 0), ('giu', 1), ('su', 1))):
            t[n] = _p(d, 'bici_salto', f)
    elif nome == 'surf4':
        for k, d in enumerate(DIR4):
            t[1 + k] = _p(d, 'surf')
    elif nome == 'pesca16':
        for k, d in enumerate(DIR4):
            for f in range(4):
                t[1 + 4 * k + f] = _p(d, 'pesca', f)
    elif nome == 'scala6':
        for f in range(3):
            t[1 + f] = _p('su', 'scala', f)
            t[4 + f] = _p('giu', 'scala', f)
    elif nome == 'salva2':
        t[1] = _p('giu', 'salva', 0)
        t[2] = _p('giu', 'salva', 1)
    elif nome == 'banzai12':
        sei = [_p('sx', 'fermo'), _p('sx', 'banzai', 1), _p('su', 'banzai', 0), _p('su', 'banzai', 1),
               _p('su', 'banzai', 3), _p('su', 'banzai', 2)]
        for k, p in enumerate(sei):
            t[1 + k] = p
        for n, src in ((7, 5), (8, 4), (9, 3), (10, 2), (11, 1), (12, 6)):
            t[n] = sei[src - 1]
    elif nome == 'spinta8':
        for k, d in enumerate(DIR4):
            t[1 + 2 * k] = _p(d, 'spinta', 0)
            t[2 + 2 * k] = _p(d, 'spinta', 1)
    else:
        raise KeyError(nome)
    return t

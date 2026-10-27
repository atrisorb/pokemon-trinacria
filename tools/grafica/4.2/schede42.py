"""Schede delle celle esterne del blocco 4.2 (contenuti scritti a mano dalla trama e dai registri).

Per ogni cella della matrice 0: tema, elementi (edifici con porta verso un interno, monumenti, gruppi
di oggetti, acque) e punti per il Modulo 6. I lati, il mare e il Centro Pokémon delle città col volo
vengono dai registri (mondo42.py). Zone: nord, sud, ovest, est, nordovest, nordest, sudovest,
sudest, centro.
"""


def pal(verso=None, w=6, d=4, h=64, fac='fac_barocca', tetto='tetto_piano', porta='portone', zona='centro', **k):
    return dict(tipo='palazzo', verso=verso, w=w, d=d, h=h, fac=fac, tetto=tetto, porta=porta, zona=zona, **k)


def casa(verso=None, w=4, d=3, h=48, fac='fac_intonaco', tetto='tetto_coppi', porta='porta', zona='centro', **k):
    return dict(tipo='casa', verso=verso, w=w, d=d, h=h, fac=fac, tetto=tetto, porta=porta, zona=zona, **k)


def imb(verso, roccia='roccia', w=5, d=3, h=48, zona='nord', **k):
    return dict(tipo='imbocco', verso=verso, roccia=roccia, w=w, d=d, h=h, zona=zona, **k)


def canc(verso, dentro=(), w=9, zona='nord', **k):
    return dict(tipo='cancello', verso=verso, dentro=dentro, w=w, zona=zona, **k)


def mon(sagoma='statua', punto=None, zona='centro', **k):
    return dict(tipo='monumento', sagoma=sagoma, punto=punto, zona=zona, **k)


def gr(pezzi, w, d, zona='centro', **k):
    return dict(tipo='gruppo', pezzi=pezzi, w=w, d=d, zona=zona, **k)


def spec(w, d, punti=0, nome='osservazione', zona='centro', **k):
    return dict(tipo='specchio', w=w, d=d, punti=punti, nome=nome, zona=zona, **k)


def castello(verso=None, w=9, d=7, h=64, fac='muro_lavico', zona='centro', **k):
    return dict(tipo='castello', verso=verso, w=w, d=d, h=h, fac=fac, zona=zona, **k)


def catt(verso=None, fac='fac_barocca', zona='nord', **k):
    return dict(tipo='cattedrale', verso=verso, fac=fac, zona=zona, **k)


def rov(w, d, punto=None, zona='centro', **k):
    return dict(tipo='rovine', w=w, d=d, punto=punto, zona=zona, **k)


def filari(w, d, pianta='albero', zona='centro', **k):
    return dict(tipo='filari', w=w, d=d, pianta=pianta, zona=zona, **k)


SACCHI = ('sacchi', 'cassonetto', 'sacchi', 'cass_brucia')

# --------------------------------------------------------------------------- Catania (CT)
SCHEDE = {
    (39, 5): dict(tema='citta_ct', titolo='Corso Italia e piazza Verga', elementi=[
        casa('MAP_CT_CATANIA_CASA_PROTAGONISTA_1F', w=5, d=4, h=64, fac='fac_barocca', tetto='tetto_piano',
             zona='nordovest', nota='M-CT-01: casa del protagonista'),
        pal('MAP_CT_CATANIA_PALAZZO_GIUSTIZIA', w=10, d=5, h=80, fac='fac_cemento', tetto='tetto_cemento',
            zona='nordest', nota='P-02: Palazzo di Giustizia in piazza Verga, chiuso durante la storia'),
        gr(('palma', 'lampione'), 6, 1, zona='centro', passo=3)],
        punti=[('cartello_st09', 'sud', 'E-CT-05: cartello ST-09 davanti alla stazione, bordo sud')]),
    (38, 5): dict(tema='citta_ct', titolo='via Etnea bassa, piazza Università, via Gemmellaro', elementi=[
        pal('MAP_CT_CATANIA_VERMUT', w=5, d=3, h=64, fac='fac_negozio', porta='porta_vetro', insegna=True,
            zona='nordest', nota='M-CT-02: il Vermut di via Gemmellaro'),
        pal(None, w=9, d=4, h=80, fac='fac_lavica', zona='nordovest', nome='teatro_massimo'),
        gr(('tavolino',), 4, 2, zona='est', punto='tavolini_gemmellaro', nota='M-CT-02: tavolini di via Gemmellaro'),
        gr(SACCHI, 3, 2, zona='sudovest', punto='munnizza_vicolo', nota='M-CT-02: i Munnizza nei vicoli')],
        punti=[('turi_piazza_universita', 'centro', 'S-CT-01: Turi in piazza Università'),
               ('motorino_marciapiede', 'sudest', 'E-CT-04: motorino sul marciapiede'),
               ('arancini', 'ovest', 'E-CT-02: arancini')]),
    (38, 4): dict(tema='citta_ct', titolo='via Etnea alta, Villa Bellini, Savia', erba=False, elementi=[
        dict(tipo='filari', w=10, d=5, pianta='albero', terreno='erba', zona='nordovest'),
        gr(('fiori',), 1, 1, zona='ovest', blocca=False),
        pal(None, w=5, d=3, h=64, fac='fac_negozio', porta='porta_vetro', insegna=True, zona='est', nome='savia'),
        gr(('auto',), 2, 1, zona='sudest', punto='auto_blu', nota='M-CT-02: auto blu in via Santa Filomena')],
        punti=[('scagnozzi_savia', 'est', 'M-CT-02: scagnozzi di U Sistema coi Koffing davanti a Savia'),
               ('pacco_villa_bellini', 'nordovest', 'S-CT-01: pacco di Villa Bellini'),
               ('pacco_via_etnea', 'centro', 'S-CT-01: pacco di via Etnea')]),
    (38, 6): dict(tema='citta_ct', titolo='Piazza Duomo, Palazzo degli Elefanti, Cattedrale, Pescheria', elementi=[
        catt('MAP_CT_CATANIA_CATTEDRALE', zona='nord', nota='S-CT-09: Cattedrale di Sant’Agata'),
        pal('MAP_CT_CATANIA_PALAZZO_ELEFANTI_ATRIO', w=8, d=4, h=80, fac='fac_lavica', zona='ovest',
            nota='M-CT-08: Palazzo degli Elefanti'),
        mon('liotru', punto='liotru', zona='centro', nota='E-CT-01: u Liotru'),
        gr(('tavolino', 'barca', 'sacchi'), 6, 2, zona='sud', punto='pacco_pescheria',
           nota='S-CT-01: pacco della Pescheria')],
        punti=[('comizio_duomo', 'centro', 'ST-01: comizio di Piazza Duomo dopo M-CT-08'),
               ('palco_finale', 'sud', 'M-EN-07: il palco finale')]),
    (37, 6): dict(tema='citta_ct', titolo='Castello Ursino e piazza Federico di Svevia', elementi=[
        castello('MAP_CT_CATANIA_CASTELLO_URSINO', w=9, d=7, h=64, zona='centro',
                 nota='museo civico; D-CT-07 nei sotterranei')],
        punti=[('pacco_castello', 'sud', 'S-CT-01: pacco del Castello Ursino')]),
    (37, 5): dict(tema='citta_ct', titolo='San Cristoforo, via Plebiscito', tema_extra=dict(
        facciate=('fac_intonaco', 'fac_lavica', 'fac_negozio', 'fac_cemento')), elementi=[
        casa('MAP_CT_CATANIA_OFFICINA', w=5, d=3, h=48, fac='fac_negozio', tetto='tetto_piano', porta='saracinesca',
             zona='nordest', nota='M-CT-03: officina di Orazio'),
        gr(('braciere',), 8, 1, zona='centro', punto='braci_plebiscito', nota='M-CT-03: le braci di via Plebiscito'),
        gr(SACCHI, 2, 2, zona='sudovest')],
        punti=[('strozzino_1', 'nordovest', 'M-CT-03: strozzino del pizzo biologico'),
               ('strozzino_2', 'sudovest', 'M-CT-03: strozzino'), ('strozzino_3', 'sudest', 'M-CT-03: strozzino'),
               ('ritrovo_orazio', 'est', 'P-01: Ritrovo di Orazio, martedì'),
               ('nunzio_riapre', 'nordest', 'P-10')]),
    (37, 4): dict(tema='periferia', titolo='Galermo, case popolari', erba=True, elementi=[
        pal('MAP_CT_CATANIA_CASE_POPOLARI', w=10, d=4, h=96, fac='fac_cemento', tetto='tetto_cemento',
            porta='porta', zona='nord', nota='M-CT-04: le case popolari di Christian'),
        gr(SACCHI, 3, 1, zona='sud')],
        punti=[('buttafuori_1', 'ovest', 'M-CT-04: buttafuori'), ('buttafuori_2', 'centro', 'M-CT-04: buttafuori'),
               ('buttafuori_3', 'est', 'M-CT-04: buttafuori')]),
    (36, 6): dict(tema='periferia', titolo='Librino, Palazzo di Cemento', erba=True, elementi=[
        pal('MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02', w=10, d=5, h=128, fac='fac_cemento', tetto='tetto_cemento',
            porta='porta', parabole=True, zona='nord', nota='M-CT-05: ingresso del Palazzo di Cemento'),
        pal(None, w=7, d=3, h=48, fac='fac_intonaco', tetto='tetto_piano', zona='sudest', nome='scuola_seggio'),
        gr(SACCHI, 2, 2, zona='ovest')],
        punti=[('seggio_cambiavoti', 'est', 'S-CT-10: scuola-seggio, Cambiavoti col Pokémon spia sulla cabina'),
               ('ritrovo_chantal', 'sudovest', 'P-01: Ritrovo di Chantal, mercoledì')]),
    (40, 5): dict(tema='costa_lavica', titolo='Ognina, lungomare', erba=True,
                  elementi=[gr(('barca',), 4, 1, zona='sud', passo=2, blocca=True)],
                  punti=[('pacco_ognina', 'centro', 'S-CT-01: pacco di Ognina')]),
    (38, 7): dict(tema='spiaggia', titolo='Plaia (est), lidi', erba=True, elementi=[
        gr(('ombrellone',), 6, 3, zona='est', passo=3, blocca=True)]),
    (37, 7): dict(tema='spiaggia', titolo='Plaia (ovest), Privè Zagara', erba=True, elementi=[
        pal('MAP_CT_CATANIA_PRIVE_ZAGARA', w=7, d=4, h=48, fac='fac_intonaco', tetto='tetto_piano',
            porta='porta_vetro', insegna=True, zona='nord', nota='ST-05: ingresso del Privè Zagara'),
        gr(('ombrellone',), 6, 2, zona='sud', passo=3)]),
    (36, 7): dict(tema='periferia', titolo='Fontanarossa, rotonda e Terminal A', riempi='industria', elementi=[
        pal('MAP_CT_CATANIA_TERMINAL_A_ATRIO', w=14, d=5, h=48, fac='vetrata', tetto='lamiera', porta='porta_vetro',
            zona='nord', nota='M-CT-09: ingresso del Terminal A'),
        mon('cespuglio', punto='rotonda', zona='sud', nota='M-CT-09: rotonda dell’aeroporto, FLAG_ETNA_ASH_ACTIVE')]),
    (36, 5): dict(tema='periferia', titolo='Misterbianco, il Cubbar', elementi=[
        pal('MAP_CT_MISTERBIANCO_CUBBAR', w=8, d=4, h=48, fac='lamiera', tetto='lamiera', porta='porta_vetro',
            insegna=True, zona='nord', nota='M-CT-00: il Cubbar alle 3:30'),
        gr(('auto', 'auto'), 4, 1, zona='centro', passo=2)],
        punti=[('uscita_prologo', 'centro', 'M-CT-00: uscita del prologo')]),
    (41, 5): dict(tema='costa_lavica', titolo='Aci Castello, castello sulla rupe nera', elementi=[
        castello(None, w=9, d=7, h=48, fac='muro_lavico', zona='est')]),
    (41, 4): dict(tema='costa_lavica', titolo='Aci Trezza, i Faraglioni', elementi=[
        gr(('barca',), 6, 1, zona='est', passo=2, punto='varche', nota='S-CT-04: barche dei pescatori')],
        punti=[('pescatore_1', 'nordest', 'S-CT-04: pescatore'), ('pescatore_2', 'est', 'S-CT-04: pescatore'),
               ('pescatore_3', 'sudest', 'S-CT-04: pescatore'), ('pescatore_4', 'centro', 'S-CT-04: pescatore')],
                  faraglioni=True),
    (41, 2): dict(tema='barocco', titolo='Acireale, centro barocco e Piazza Duomo', elementi=[
        catt(None, zona='nordest'),
        casa('MAP_CT_ACIREALE_CASA_TURI', w=4, d=3, h=48, zona='nordovest', nota='C-01: casa di Turi')],
        punti=[('granita_mezzanotte', 'centro', 'S-CT-03: granita di mezzanotte'),
               ('libro_turi', 'ovest', 'P-11')]),
    (41, 3): dict(tema='costa_lavica', titolo='Acireale, la Timpa e Santa Maria la Scala', erba=True, elementi=[
        dict(tipo='filari', w=10, d=5, pianta='albero', terreno='terra', zona='ovest')],
        punti=[('timpa_partenza', 'nord', 'S-CT-02: discesa della Timpa'),
               ('timpa_arrivo', 'sud', 'S-CT-02: arrivo a Santa Maria la Scala'),
               ('b_ct_05', 'sudest', 'S-CT-02: B-CT-05')]),
    (37, 3): dict(tema='paese_etna', titolo='Nicolosi', erba=True, elementi=[
        canc('MAP_CT_ETNA_MONTI_ROSSI', dentro=('alberi',), w=9, zona='nordovest',
             nota='M-CT-06: ingresso della Pineta dei Monti Rossi')]),
    (37, 2): dict(tema='etna', titolo='Etna Sud, Rifugio Sapienza', erba=True, elementi=[
        imb('MAP_CT_ETNA_CRATERI_SILVESTRI', roccia='roccia_nera', zona='nordovest',
            nota='M-CT-06: uscita dei Crateri Silvestri'),
        casa(None, w=6, d=4, h=48, fac='fac_lavica', tetto='tetto_coppi', zona='sudest', nome='rifugio_sapienza'),
        dict(tipo='parete', verso='MAP_CT_ETNA_CRATERE_CENTRALE', w=2, d=7, zona='nordest',
             nota='P-04: parete con Scalaroccia verso il Cratere Centrale')]),
    (34, 5): dict(tema='paese_etna', titolo='Paternò, paese e castello', erba=True, elementi=[
        castello(None, w=7, d=6, h=80, fac='muro_lavico', zona='nordovest')]),
    (35, 5): dict(tema='campagna', titolo='Paternò, le Salinelle', erba=True, elementi=[
        dict(tipo='fango', w=14, d=10, punti=4, nome='ispezione', zona='centro', nota='S-CT-05: punto di ispezione')]),
    (34, 3): dict(tema='paese_etna', titolo='Adrano', erba=True, elementi=[
        castello(None, w=7, d=6, h=64, fac='muro_lavico', zona='nordest')]),
    (33, 3): dict(tema='campagna', titolo='Adrano, Ponte dei Saraceni sul Simeto', erba=True, elementi=[
        dict(tipo='ponte', pos=(10, 12), w=5, punto='ponte_saraceni', nota='S-CT-06: Ponte dei Saraceni')]),
    (34, 2): dict(tema='paese_etna', titolo='Bronte', erba=True, elementi=[
        canc('MAP_CT_BRONTE_SCIARA', dentro=('alberi',), w=9, zona='nordest',
             nota='M-CT-07: ingresso della Sciara dei pistacchi'),
        filari(8, 4, pianta='cespuglio', zona='sudovest')]),
    (34, 0): dict(tema='paese_etna', titolo='Randazzo, paese e stazione della Circumetnea', erba=True, elementi=[
        dict(tipo='binari', pos=(4, 24), w=14, punto='binario_circumetnea',
             nota='S-CT-08: binario e capostazione; si sale sul treno (MAP_CT_CIRCUMETNEA_TRENO) con uno script')],
        punti=[('orario_indicativo', 'sud', 'E-CT-03: orario «indicativo»')]),
    (35, 0): dict(tema='etna', titolo='Randazzo, versante nord dell’Etna', erba=True, elementi=[
        imb('MAP_CT_ETNA_GROTTA_DEL_GELO', roccia='roccia_nera', zona='sudest',
            nota='D-CT-06: ingresso della Grotta del Gelo')]),
    (32, 7): dict(tema='barocco', titolo='Caltagirone, centro', elementi=[
        catt(None, zona='nordovest')]),
    (32, 8): dict(tema='barocco', titolo='Caltagirone, la Scalinata di Santa Maria del Monte', piazza=False, elementi=[
        dict(tipo='scalinata', pos=(13, 3), w=6, d=26, rampe=7, nome='rampa',
             nota='S-CT-07 / D-CT-05: un allenatore per rampa; il ceramista in cima')],
        punti=[('ceramista', 'nord', 'S-CT-07: il maestro ceramista in cima alla Scalinata')]),
    # ----------------------------------------------------------------------- Siracusa (SR)
    (37, 9): dict(tema='paese', titolo='Lentini, magazzini agrumari', erba=True, elementi=[
        pal('MAP_SR_LENTINI_MAGAZZINI', w=10, d=5, h=48, fac='lamiera', tetto='lamiera', porta='saracinesca',
            zona='nord', nota='S-SR-03: magazzini agrumari'),
        filari(8, 4, pianta='albero', zona='sud')]),
    (36, 9): dict(tema='campagna', titolo='Lentini, Biviere', erba=True, elementi=[
        spec(16, 10, punti=5, nome='osservazione', zona='centro', nota='S-SR-04: punto di osservazione del Biviere')]),
    (37, 10): dict(tema='paese', titolo='Carlentini, paese sulla collina', erba=True),
    (39, 9): dict(tema='industria', titolo='Augusta, il porto e l’ingresso del polo', riempi='case', elementi=[
        canc('MAP_SR_POLO_PONTILI_SERBATOI', dentro=('serbatoi',), w=11, zona='nordovest',
             nota='M-SR-02: ingresso del polo petrolchimico')],
        punti=[('operai', 'ovest', 'M-SR-02: operai'), ('pescatori', 'sudest', 'M-SR-02: pescatori che mostrano il mare')]),
    (38, 10): dict(tema='paese', titolo='Melilli', erba=True),
    (39, 10): dict(tema='industria', titolo='Priolo Gargallo, le torce del polo', erba=True, riempi='industria', elementi=[
        canc('MAP_SR_POLO_SALA_CONTROLLO_TORCIA', dentro=('torcia', 'traliccio'), w=9, zona='nordest',
             nota='M-SR-02 / D-SR-01: sala controllo e torcia'),
        gr(('torcia',), 3, 1, zona='nordovest', passo=1)]),
    (39, 11): dict(tema='barocco', titolo='Siracusa in terraferma, corso Gelone', elementi=[
        pal('MAP_SR_SIRACUSA_RADIO', w=6, d=4, h=64, fac='fac_intonaco', porta='porta', zona='nordovest',
            nota='S-SR-01: la Radio di quartiere'),
        gr(('traliccio',), 1, 1, zona='nordovest')]),
    (38, 11): dict(tema='campagna', titolo='Neapolis, Teatro Greco e Latomie', erba=True, elementi=[
        dict(tipo='teatro', w=16, d=8, zona='nord', punto='teatro_greco', nota='parco archeologico, Teatro Greco'),
        imb('MAP_SR_SIRACUSA_LATOMIE', roccia='muro_calcare', w=6, zona='sudovest',
            nota='D-SR-02: ingresso delle Latomie')]),
    (40, 11): dict(tema='barocco', titolo='Ortigia', piazza=False, elementi=[
        mon('statua', punto='archimede', zona='centro', nota='E-SR-01: Archimede'),
        castello('MAP_SR_CASTELLO_MANIACE_INGRESSO', w=7, d=6, h=56, fac='muro_calcare', zona='sud',
                 nota='M-SR-05: ingresso del Castello Maniace'),
        pal(None, w=7, d=4, h=72, fac='fac_barocca', tetto='tetto_coppi', zona='nord', nome='duomo_ortigia'),
        spec(5, 4, punti=1, nome='fonte_aretusa', zona='ovest', margine=0, riva='lastricato', nota='M-SR-04: Fonte Aretusa'),
        ],
        punti=[('comizio_ortigia', 'nord', 'ST-01: comizio in piazza Duomo di Ortigia'),
               ('turi_matteotti', 'centro', 'S-SR-01: Turi in corso Matteotti'),
               ('cartello_st09', 'sudovest', 'E-SR-02: cartello ST-09 in piazza Pancali')]),
    (38, 13): dict(tema='barocco', titolo='Noto', elementi=[catt(None, zona='nordovest')],
                   punti=[('granita_caffe', 'est', 'S-SR-06: la granita del Caffè'),
                          ('anziano_cattedrale', 'nordovest', 'S-SR-06: l’anziano della Cattedrale')]),
    (39, 13): dict(tema='paese', titolo='Avola, la piazza esagonale', erba=True, piazza=True, elementi=[
        pal(None, w=7, d=3, h=48, fac='fac_intonaco', tetto='tetto_piano', zona='nordest', nome='scuola')],
        punti=[('cassa_%d' % k, z, 'S-SR-08: cassa di Nero d’Avola') for k, z in
               enumerate(('nord', 'nordest', 'sudest', 'sud', 'sudovest', 'nordovest'), 1)] +
        [('seggio_cambiavoti', 'est', 'S-SR-09: scuola, Cambiavoti di Siracusa col Pokémon spia')]),
    (38, 14): dict(tema='campagna', titolo='Vendicari, casa del guardiaparco', erba=True, elementi=[
        casa('MAP_SR_VENDICARI_GUARDIAPARCO', w=5, d=3, h=48, fac='muro_calcare', zona='centro',
             nota='S-SR-05: casa del guardiaparco, ingresso della riserva'),
        spec(10, 6, punti=0, zona='sudest', acqua='acqua')]),
    (39, 14): dict(tema='spiaggia', titolo='Marzamemi, la tonnara e piazza Regina Margherita', piazza=True, elementi=[
        pal('MAP_SR_MARZAMEMI_TONNARA', w=10, d=5, h=48, fac='muro_calcare', tetto='tetto_coppi', zona='nordest',
            nota='D-SR-03: ingresso della Tonnara'),
        gr(('barca',), 4, 1, zona='sudest', passo=2)],
        punti=[('concessionario_%d' % k, z, 'M-SR-03: galà con i Concessionari') for k, z in
               enumerate(('centro', 'ovest', 'sud', 'sudovest'), 1)] +
        [('tappa_st05', 'nordovest', 'ST-05: tappa di Marzamemi'), ('e_sr_03', 'est', 'E-SR-03')]),
    (38, 15): dict(tema='paese', titolo='Pachino, serre e pomodorini', erba=True, elementi=[
        dict(tipo='serre', n=4, d=6, zona='nordovest')]),
    (39, 15): dict(tema='spiaggia', titolo='Portopalo, paese e porto', erba=True, elementi=[
        gr(('barca',), 4, 1, zona='est', passo=2)],
        punti=[('faro_capo_passero', 'est', 'E-SR-04: il faro di Capo Passero all’orizzonte')]),
    (39, 16): dict(tema='spiaggia', titolo='Portopalo, Isola delle Correnti', erba=True, elementi=[
        dict(tipo='faro', zona='sud', punto='guardiano_faro', nota='S-SR-07: Guardiano del Faro')],
        punti=[('bassa_marea', 'centro', 'S-SR-07: passaggio con la bassa marea, 6:00–9:00 (script)')]),
    # ----------------------------------------------------------------------- Ragusa (RG)
    (33, 12): dict(tema='barocco', titolo='Ragusa Superiore', elementi=[
        dict(tipo='scalinata', pos=(25, 3), w=4, d=10, rampe=3, nome='scale_ibla', nota='M-RG-01: le scale verso Ibla')]),
    (34, 12): dict(tema='barocco', titolo='Ragusa Ibla', erba=False, elementi=[
        catt(None, zona='nord'),
        pal('MAP_RG_IBLA_SEGRETERIA_MAGAZZINI', w=7, d=4, h=64, zona='nordovest',
            nota='M-RG-04: Palazzo di via del Mercato (Segreteria)'),
        pal('MAP_RG_IBLA_PALAZZO_MARCHESA', w=7, d=4, h=64, zona='sudest', nota='B-RG-03: palazzo della Marchesa'),
        dict(tipo='filari', w=8, d=3, pianta='palma', zona='sudovest', terreno='erba')],
        punti=[('ritrovo_maria', 'centro', 'M-RG-01: ritrovo con Maria'),
               ('comizio_giardino_ibleo', 'sudovest', 'ST-01: comizio al Giardino Ibleo'),
               ('scale_contate', 'ovest', 'E-RG-02: 340 scale')]),
    (33, 13): dict(tema='campagna', titolo='Marina di Ragusa, strada dalla città', erba=True),
    (33, 14): dict(tema='spiaggia', titolo='Marina di Ragusa, lungomare', erba=True, elementi=[
        gr(('ombrellone',), 9, 2, zona='sud', passo=3)]),
    (34, 13): dict(tema='barocco', titolo='Modica', elementi=[
        pal('MAP_RG_MODICA_LABORATORIO', w=5, d=5, h=64, fac='fac_negozio', tetto='tetto_coppi', porta='porta_vetro',
            pos=(14, 15), dx=2, insegna=True,
            nota='M-RG-01: laboratorio di cioccolato, Centro e negozio di Modica (porta a (16,19), R-MAP-14)')],
        punti=[('viadotto_guerrieri', 'nord', 'S-RG-01: video coi cavalli sul viadotto Guerrieri'),
               ('modica_alta', 'nordovest', 'S-RG-02: Modica Alta')]),
    (34, 14): dict(tema='barocco', titolo='Scicli, via Mormino Penna', erba=True,
                   punti=[('mormino_penna', 'centro', 'S-RG-03: via Mormino Penna'),
                          ('spezie', 'est', 'S-RG-02: spezie')]),
    (35, 14): dict(tema='paese', titolo='Pozzallo, Torre Cabrera e il porto', erba=False, props=('lampione',), elementi=[
        castello(None, w=5, d=5, h=64, fac='muro_calcare', zona='sudest')],
        punti=[('torre_cabrera', 'sudest', 'S-RG-06: Torre Cabrera'), ('cacao_porto', 'sud', 'S-RG-02: cacao al porto'),
               ('cartello_st09', 'nord', 'E-RG-03: cartello ST-09'),
               ('memoria', 'sudovest', 'luogo della memoria (R-05.4/5): niente lotte, tono sobrio')]),
    (35, 13): dict(tema='paese', titolo='Ispica, Loggiato del Sinatra', erba=True, elementi=[
        pal(None, w=10, d=3, h=48, fac='fac_barocca', zona='nord', nome='loggiato')],
        punti=[('loggiato_sinatra', 'nord', 'S-RG-07: Loggiato del Sinatra')]),
    (35, 12): dict(tema='calanchi', titolo='Cava d’Ispica', erba=True, tema_extra=dict(roccia='muro_calcare'), elementi=[
        imb('MAP_RG_CAVA_D_ISPICA', roccia='muro_calcare', w=7, zona='nord', nota='S-RG-05 / D-RG-03: Cava d’Ispica')]),
    (31, 12): dict(tema='paese', titolo='Vittoria', elementi=[
        pal('MAP_RG_MERCATO_PADIGLIONI', w=10, d=4, h=48, fac='lamiera', tetto='lamiera', porta='saracinesca',
            zona='nordovest', nota='M-RG-02: mercato ortofrutticolo, alle 4:00'),
        pal(None, w=7, d=3, h=48, fac='fac_intonaco', zona='sudest', nome='scuola')],
        punti=[('seggio_cambiavoti', 'sudest', 'S-RG-08: scuola, Cambiavoti di Ragusa col Pokémon spia'),
               ('zucchero', 'est', 'S-RG-02: zucchero')]),
    (32, 12): dict(tema='paese', titolo='Comiso', erba=True),
    (32, 13): dict(tema='industria', titolo='Comiso, aeroporto e base NATO', erba=True, elementi=[
        pal('MAP_RG_COMISO_TERMINAL', w=12, d=4, h=48, fac='vetrata', tetto='lamiera', porta='porta_vetro',
            zona='nordovest', nota='M-RG-03: terminal deserto'),
        canc('MAP_RG_COMISO_BASE_NATO_HANGAR', dentro=('traliccio',), w=9, zona='sudest',
             nota='M-RG-03: ingresso dell’ex base NATO')],
        punti=[('piazzale_terminal', 'centro', 'M-RG-03: piazzale del terminal deserto')]),
    (31, 13): dict(tema='paese', titolo='Santa Croce Camerina', erba=True),
    (31, 14): dict(tema='spiaggia', titolo='Punta Secca, la terrazza', erba=True, elementi=[
        casa(None, w=5, d=4, h=48, fac='fac_intonaco', tetto='tetto_piano', zona='sudest', nome='casa_terrazza'),
        dict(tipo='faro', zona='sudovest')],
        punti=[('terrazza', 'sudest', 'S-RG-04: la terrazza'), ('asciugamano', 'sud', 'S-RG-04: l’asciugamano rubato')]),
    (32, 14): dict(tema='spiaggia', titolo='Punta Secca, spiaggia verso Marina', erba=True, elementi=[
        gr(('ombrellone',), 6, 2, zona='sud', passo=3)]),
    # ----------------------------------------------------------------------- Caltanissetta (CL)
    (28, 12): dict(tema='nisseno', titolo='Gela, centro storico e Mura Timoleontee', erba=False, elementi=[
        rov(10, 4, punto='mura_timoleontee', zona='nordovest', nota='M-CL-02: Mura Timoleontee di Capo Soprano'),
        rov(6, 4, punto='molino_a_vento', zona='nordest', nota='M-CL-02: acropoli di Molino a Vento')]),
    (29, 12): dict(tema='industria', titolo='Gela, Macchitella e pontile del polo', riempi='case', elementi=[
        dict(tipo='serbatoi', n=3, h=64, zona='nordest'),
        gr(('recinzione',), 6, 1, zona='sudest', passo=1, punto='pontile_sbarrato',
           nota='M-CL-02: pontile sbarrato del polo, presidiato coi Koffing, Grimer e Magnemite')],
        punti=[('cambiavoti_lungomare', 'sud', 'S-CL-08 / ST-06: Cambiavoti sul lungomare col Pokémon spia')]),
    (31, 10): dict(tema='nisseno', titolo='Niscemi, Belvedere del Maroglio', erba=True,
                   punti=[('belvedere', 'nord', 'M-CL-03: Belvedere del Maroglio'),
                          ('comitati', 'centro', 'M-CL-03: comitati cittadini')]),
    (32, 10): dict(tema='bosco', titolo='Sughereta di Niscemi (nord)', erba=True),
    (32, 11): dict(tema='bosco', titolo='Sughereta di Niscemi (sud), cancello del MUOS', erba=True, elementi=[
        canc('MAP_CL_NISCEMI_MUOS_RECINZIONE', dentro=('traliccio',), w=9, zona='sud',
             nota='M-CL-03 / D-CL-02: cancello della Base MUOS')],
        punti=[('grande_quercia', 'nordest', 'M-CL-03: Grande Quercia Mosaico')]),
    (27, 10): dict(tema='nisseno', titolo='Mazzarino, «U Cannuni»', erba=True, elementi=[
        rov(8, 5, punto='u_cannuni', zona='nord', muro='muro_calcare',
            nota='S-CL-06: ruderi del castello, la troupe col Charmeleon truccato da drago')]),
    (27, 11): dict(tema='nisseno', titolo='Mazzarino, paese', erba=True),
    (25, 10): dict(tema='nisseno', titolo='Riesi, Monte degli Ulivi', erba=True, elementi=[
        casa(None, w=6, d=3, h=48, fac='fac_intonaco', zona='nord', nome='centro_valdese'),
        filari(10, 5, pianta='albero', zona='sud')],
        punti=[('pastore_valdese', 'nord', 'S-CL-05: il Pastore valdese')]),
    (25, 11): dict(tema='nisseno', titolo='Riesi, paese', erba=True),
    (24, 8): dict(tema='calanchi', titolo='SS626, svincolo per Caltanissetta', erba=True),
    (24, 9): dict(tema='calanchi', titolo='SS626, cantiere del Viadotto Salso 2', erba=True, elementi=[
        canc('MAP_CL_VIADOTTO_SALSO_PILONI', dentro=('traliccio',), w=9, zona='nord',
             nota='M-CL-04 / D-CL-04: cantiere del Viadotto Salso 2 (Segreteria 4)')],
        punti=[('cartello_lavori', 'centro', 'E-CL-03: cartello lavori 31/12/2006 → 31/12/2026'),
               ('operai_lo_monaco', 'sud', 'M-CL-01: operai che provocano micro-frane')]),
    (24, 10): dict(tema='calanchi', titolo='SS626, bivio per Riesi e Canicattì', erba=True),
    (23, 8): dict(tema='nisseno', titolo='Caltanissetta, Piazza Garibaldi e Corso Umberto', elementi=[
        mon('statua', punto='fontana_tritone', zona='nordovest', nota='M-CL-04: Fontana del Tritone'),
        pal('MAP_CL_CALTANISSETTA_DISTILLERIA', w=6, d=4, h=64, fac='fac_barocca', porta='portone', insegna=True,
            zona='nordest', nota='E-CL-04: la distilleria storica dell’amaro')],
        punti=[('comizio_corso_umberto', 'sud', 'M-CL-04 / ST-01: comizio finale'),
               ('santino', 'ovest', 'S-CL-01 / ST-03: il santino in dialetto'),
               ('cartello_st09', 'sudovest', 'E-CL-02: cartello ST-09 della stazione'),
               ('cartellone_amaro', 'est', 'E-CL-04: cartellone dell’amaro')]),
    (23, 7): dict(tema='nisseno', titolo='Caltanissetta, colle Sant’Anna', erba=True, elementi=[
        gr(('traliccio',), 3, 1, zona='nord', passo=1, punto='antenne_rai',
           nota='E-CL-01: le antenne Rai di Sant’Anna')]),
    (22, 8): dict(tema='nisseno', titolo='San Cataldo, centro storico', erba=True,
                  punti=[('sampauluna', 'centro', 'S-CL-04: il centro dei Sampauluna')]),
    (22, 7): dict(tema='calanchi', titolo='San Cataldo, contrada Gabbara', erba=True, elementi=[
        imb('MAP_CL_GABBARA_ZOLFARA_GALLERIE', roccia='roccia', w=6, zona='nord',
            nota='S-CL-04 / D-CL-03: imbocco della Zolfara di Gabbara')]),
    (20, 8): dict(tema='nisseno', titolo='Sutera, il Rabato', erba=True, elementi=[
        dict(tipo='scalinata', pos=(13, 3), w=4, d=12, rampe=4, nome='salita_san_paolino',
             nota='S-CL-07: salita al santuario sul Monte San Paolino')]),
    (20, 9): dict(tema='nisseno', titolo='Sutera, sotto il monte', erba=True),
    (20, 7): dict(tema='nisseno', titolo='Mussomeli, centro', elementi=[
        pal('MAP_CL_MUSSOMELI_UFFICI_COMUNALI', w=7, d=4, h=64, fac='fac_barocca', zona='nordest',
            nota='S-CL-03: Uffici Comunali, le case a 1 euro')],
        punti=[('pensionati', 'ovest', 'S-CL-03: la coppia di pensionati con la planimetria del 1924')]),
    (20, 6): dict(tema='calanchi', titolo='Mussomeli, rupe del Castello Manfredonico', erba=True, elementi=[
        castello('MAP_CL_CASTELLO_MANFREDONICO', w=9, d=7, h=64, fac='muro_calcare', zona='nord',
                 nota='S-CL-02 / D-CL-01: Castello Manfredonico')]),
}

# Centri Pokémon senza punto di volo: anche lì la porta è a (16,19), come nelle città col volo.
CENTRI_SENZA_VOLO = {(34, 5), (34, 2), (38, 15), (22, 8)}

# Temi delle strade (le altre: «strada»)
TEMI_STRADE = {
    'MAP_STRADA_A18_ACIREALE': 'strada_etna',
    'MAP_STRADA_SS284_RANDAZZO_BRONTE': 'strada_etna',
    'MAP_STRADA_SS121_ADRANO_PATERNO': 'strada',
    'MAP_STRADA_SS114_CATANIA_AUGUSTA': 'strada_costa',
    'MAP_STRADA_SS115_GELA_LICATA': 'strada_costa',
    'MAP_STRADA_SS122_CALTANISSETTA_ENNA': 'strada_calanchi',
    'MAP_STRADA_SS122_CANICATTI_CALTANISSETTA': 'strada_calanchi',
    'MAP_STRADA_SS189_SAN_CATALDO_SUTERA': 'strada_calanchi',
    'MAP_STRADA_SS189_SUTERA_AGRIGENTO': 'strada_calanchi',
    'MAP_STRADA_SS189_MUSSOMELI_LERCARA': 'strada_calanchi',
}

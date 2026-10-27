"""Schede delle celle esterne del blocco 4.3 (contenuti scritti a mano dalla trama e dai registri).

Per ogni cella della matrice 0: tema, elementi (edifici con porta verso un interno, monumenti, gruppi
di oggetti, acque) e punti per il Modulo 6. Le celle senza scheda prendono il tema della mappa
(TEMA_MAPPA) o della strada (TEMI_STRADE). I lati, il mare e il Centro Pokémon delle città col volo
vengono dai registri (mondo43.py). Zone: nord, sud, ovest, est, nordovest, nordest, sudovest, sudest,
centro. Le porte verso interni di HeartGold riusati portano al warp dello slot (costruisci43.py).
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


def castello(verso=None, w=9, d=7, h=64, fac='muro_calcare', zona='centro', **k):
    return dict(tipo='castello', verso=verso, w=w, d=d, h=h, fac=fac, zona=zona, **k)


def catt(verso=None, fac='fac_barocca', zona='nord', **k):
    return dict(tipo='cattedrale', verso=verso, fac=fac, zona=zona, **k)


def rov(w, d, punto=None, zona='centro', **k):
    return dict(tipo='rovine', w=w, d=d, punto=punto, zona=zona, **k)


def filari(w, d, pianta='albero', zona='centro', **k):
    return dict(tipo='filari', w=w, d=d, pianta=pianta, zona=zona, **k)


def tempio(w=10, d=6, zona='centro', **k):
    return dict(tipo='tempio', w=w, d=d, zona=zona, **k)


def saline(w=14, d=9, zona='centro', **k):
    return dict(tipo='saline', w=w, d=d, zona=zona, **k)


def rupe(w, d, zona='centro', **k):
    return dict(tipo='rupe', w=w, d=d, zona=zona, **k)


def normanna(verso=None, w=7, d=4, zona='centro', **k):
    return dict(tipo='chiesa_normanna', verso=verso, w=w, d=d, zona=zona, **k)


SACCHI = ('sacchi', 'cassonetto', 'sacchi', 'cass_brucia')
MERCATO = ('bancarella', 'carretto', 'bancarella')

# --------------------------------------------------------------------------- Agrigento (AG)
SCHEDE = {
    (22, 11): dict(tema='paese_tufo', titolo='Licata, il porto e il Faro di San Giacomo', elementi=[
        casa('MAP_AG_LICATA_CASA_RUBINETTO', w=4, d=3, zona='nordovest',
             nota='E-AG-04: la casa del rubinetto asciutto'),
        dict(tipo='faro', zona='sudovest', punto='faro_san_giacomo', nota='porto di Licata'),
        gr(('autobotte',), 2, 1, zona='nordest', punto='autobotte_doppia_fila',
           nota='E-AG-01: l’autobotte in doppia fila col Donphan')],
        punti=[('turi_porto', 'sudest', 'S-AG-01 / ST-03: Turi al porto dopo il comizio sbagliato'),
               ('ritrovo_calogero', 'sud', 'P-01: Ritrovo del venerdì con Calogero')]),
    (23, 11): dict(tema='paese_tufo', titolo='Licata, ponte sul Salso', elementi=[
        dict(tipo='ponte', pos=(14, 12), w=4, punto='foce_salso', nota='M-AG-01: la foce del Salso'),
        dict(tipo='condotta', w=10, autobotti=2, zona='nordovest', punto='autobotti_consorzio',
             nota='M-AG-01: Calogero davanti alle autobotti del consorzio (FLAG_RECRUIT_CALOGERO)')]),
    (19, 11): dict(tema='spiaggia', titolo='Palma di Montechiaro, Marina di Palma', erba=True),
    (20, 11): dict(tema='barocco', titolo='Palma di Montechiaro, Chiesa Madre e Monastero', elementi=[
        pal('MAP_AG_PALMA_MONASTERO', w=7, d=4, h=48, fac='fac_barocca', tetto='tetto_coppi', zona='nordest',
            nota='S-AG-07: il Monastero delle Benedettine e la ruota'),
        pal(None, w=8, d=4, h=48, fac='fac_tufo', zona='nordovest', nome='palazzo_ducale')],
        punti=[('scalinata_chiesa_madre', 'nord', 'S-AG-07: la scalinata della Chiesa Madre')]),
    (21, 11): dict(tema='paese_tufo', titolo='Palma di Montechiaro, verso Licata', erba=True),
    (20, 10): dict(tema='paese_tufo', titolo='Favara, i Sette Cortili', elementi=[
        gr(('tavolino', 'statua', 'cespuglio'), 6, 3, zona='centro', punto='sette_cortili',
           nota='S-AG-06: i Sette Cortili')],
        punti=[('smeargle_1', 'nordovest', 'S-AG-06: uno Smeargle del collettivo'),
               ('smeargle_2', 'nordest', 'S-AG-06: uno Smeargle del collettivo'),
               ('smeargle_3', 'sudovest', 'S-AG-06: uno Smeargle del collettivo'),
               ('cambiavoti_favara', 'sudest', 'S-AG-09 / ST-06: Cambiavoti di Agrigento col Pokémon spia')]),
    (21, 10): dict(tema='vigne', titolo='Favara, campagna verso Canicattì', erba=True),
    (22, 10): dict(tema='paese_tufo', titolo='Canicattì, centro'),
    (23, 10): dict(tema='vigne', titolo='Canicattì, i tendoni dell’Uva Italia', erba=True, elementi=[
        filari(12, 6, pianta='vite', zona='nordovest', terreno='terra'),
        filari(8, 4, pianta='vite', zona='sudest', terreno='terra')],
        punti=[('vigneto_1', 'nord', 'S-AG-05: sciame di Yanma e Staravia sui tendoni'),
               ('vigneto_2', 'centro', 'S-AG-05: sciame'), ('vigneto_3', 'est', 'S-AG-05: sciame')]),
    (17, 9): dict(tema='periferia', titolo='Agrigento, Villaseta', erba=True, elementi=[
        canc('MAP_AG_VILLASETA_CANTIERI', dentro=('traliccio',), w=9, zona='nord',
             nota='M-AG-05 / D-AG-04: i Cantieri di Villaseta (Segreteria 5)'),
        gr(('autobotte',), 4, 1, zona='sud', passo=2)]),
    (18, 9): dict(tema='paese_tufo', titolo='Agrigento, via Atenea e piazza Marconi', elementi=[
        catt(None, fac='fac_tufo', zona='nordovest')],
        punti=[('calogero_atenea', 'nordest', 'M-AG-02: Calogero e i turni idrici'),
               ('comizio_marconi', 'sud', 'M-AG-05 / ST-01: comizio finale in piazza Marconi'),
               ('comizio_sbagliato', 'ovest', 'S-AG-01 / ST-03: il comizio notturno di Turi col pastore e il Mareep')]),
    (18, 10): dict(tema='templi', titolo='Valle dei Templi, Tempio di Ercole e Kolymbethra', erba=True, elementi=[
        tempio(w=10, d=5, rovina=True, zona='nordest', punto='tempio_ercole', nota='Tempio di Ercole'),
        filari(10, 5, pianta='albero', zona='sudovest', terreno='erba'),
        imb('MAP_AG_IPOGEI_GALLERIE', roccia='tufo', w=6, zona='nordovest',
            nota='M-AG-03 / D-AG-01: imbocco degli Ipogei di Akragas')]),
    (19, 10): dict(tema='templi', titolo='Valle dei Templi, Tempio della Concordia e di Giunone', erba=True, elementi=[
        tempio(w=12, d=6, zona='nord', punto='tempio_concordia', nota='M-AG-03: Tempio della Concordia, la Via Sacra'),
        tempio(w=8, d=5, rovina=True, zona='sudest', punto='tempio_giunone', nota='Tempio di Giunone'),
        dict(tipo='rupe', w=6, d=1, h=8, roccia='tufo', zona='sudovest', punto='telamone',
             nota='E-AG-02: il Telamone sdraiato coi tre Slakoth')]),
    (17, 10): dict(tema='paese_tufo', titolo='Porto Empedocle, via Roma e il molo', elementi=[
        casa('MAP_AG_PORTO_EMPEDOCLE_LIBRERIA', w=4, d=3, fac='fac_tufo', zona='nordovest',
             nota='S-AG-04: la Libreria di Porto Empedocle'),
        pal('MAP_AG_PORTO_EMPEDOCLE_IMBARCO', w=6, d=3, h=32, fac='vetrata', tetto='lamiera', porta='porta_vetro',
            zona='nordest', nota='M-AG-04: biglietteria e imbarco per Lampedusa'),
        castello(None, w=5, d=5, h=48, fac='tufo', zona='centro', nome='torre_carlo_v'),
        gr(('traghetto',), 2, 1, zona='sudest', passo=2)],
        punti=[('cartello_st09', 'ovest', 'E-AG-03: cartello ST-09 della stazione di Porto Empedocle Bassa'),
               ('torre_carlo_v', 'centro', 'S-AG-04: gli indizi letterari alla Torre di Carlo V')]),
    (16, 10): dict(tema='spiaggia', titolo='Porto Empedocle, spiaggia di Marinella', erba=True,
                   punti=[('marinella', 'centro', 'S-AG-04: l’indizio di Marinella')]),
    (14, 9): dict(tema='paese_tufo', titolo='Realmonte, la costa', erba=True),
    (15, 9): dict(tema='spiaggia', titolo='Realmonte, la Scala dei Turchi', erba=True, elementi=[
        rupe(12, 4, roccia='marna', h=48, zona='nord'),
        imb('MAP_AG_GROTTA_SCALA_DEI_TURCHI', roccia='marna', w=5, zona='nordest',
            nota='S-AG-03 / D-AG-02: la Grotta della Marna')],
        punti=[('belvedere_scala', 'centro', 'S-AG-03: il belvedere sulla scogliera bianca')]),
    (16, 9): dict(tema='paese_tufo', titolo='Realmonte, paese', erba=True),
    (13, 8): dict(tema='campagna', titolo='Acquedotto Costiero, foce del Platani', erba=True, elementi=[
        dict(tipo='condotta', w=22, autobotti=2, zona='centro', punto='condotta_platani',
             nota='M-AG-02: la condotta colabrodo')],
        punti=[('scagnozzo_1', 'nord', 'M-AG-02: scagnozzo del consorzio di notte')]),
    (14, 8): dict(tema='paese_tufo', titolo='Acquedotto Costiero, Siculiana', erba=True, elementi=[
        dict(tipo='condotta', w=16, autobotti=1, zona='sud', punto='condotta_siculiana', nota='M-AG-02')],
        punti=[('scagnozzo_2', 'centro', 'M-AG-02: scagnozzo del consorzio di notte')]),
    (13, 9): dict(tema='spiaggia', titolo='Acquedotto Costiero, Torre Salsa', erba=True, elementi=[
        dict(tipo='condotta', w=14, autobotti=1, zona='nord', punto='condotta_torre_salsa',
             nota='M-AG-02: liberata la condotta, FLAG_WATER_MAFIA_DEFEATED')],
        punti=[('scagnozzo_3', 'est', 'M-AG-02: scagnozzo del consorzio di notte')]),
    (11, 8): dict(tema='tufo', titolo='Sciacca, il porto peschereccio', elementi=[
        gr(('barca',), 6, 1, zona='sud', passo=2, blocca=True)],
        punti=[('porto_sciacca', 'sudest', 'M-AG-02: la pista delle dispersioni comincia al porto')]),
    (12, 8): dict(tema='tufo', titolo='Sciacca, piazza Scandaliato e le Terme', elementi=[
        pal(None, w=8, d=4, h=48, fac='fac_liberty', zona='nordovest', nome='terme_chiuse'),
        imb('MAP_AG_SCIACCA_STUFE_KRONIO', roccia='roccia', w=5, zona='nordest',
            nota='S-AG-02 / D-AG-03: la salita alle Stufe del Monte Kronio')],
        punti=[('piazza_scandaliato', 'centro', 'M-AG-02: piazza Scandaliato'),
               ('terme_chiuse', 'ovest', 'S-AG-02: il parco delle Terme chiuse')]),
    # ----------------------------------------------------------------------- Trapani (TP)
    (5, 7): dict(tema='templi', titolo='Selinunte, l’Acropoli sul mare', erba=True, elementi=[
        tempio(w=10, d=5, rovina=True, zona='nord', punto='acropoli', nota='M-TP-01: l’Acropoli di Selinunte'),
        canc('MAP_TP_CAVE_DI_CUSA', dentro=('alberi',), w=9, zona='sudest',
             nota='M-TP-01 / D-TP-01: il sentiero verso le Cave di Cusa')]),
    (6, 7): dict(tema='templi', titolo='Selinunte, la Collina Orientale', erba=True, elementi=[
        tempio(w=12, d=6, zona='nord', punto='tempio_e', nota='la Collina Orientale, Tempio E'),
        tempio(w=10, d=5, rovina=True, rocchi=5, zona='sudovest', punto='tempio_g', nota='i rocchi del Tempio G')]),
    (5, 6): dict(tema='campagna', titolo='Castelvetrano, uliveti della Nocellara', erba=True, elementi=[
        filari(12, 7, pianta='albero', zona='centro', terreno='terra')]),
    (6, 6): dict(tema='paese_tufo', titolo='Castelvetrano, il Sistema delle Piazze', elementi=[
        pal('MAP_TP_CASTELVETRANO_PRESIDIO_CIVICO', w=7, d=4, h=48, fac='fac_intonaco', porta='portone',
            zona='nordovest', nota='M-TP-01: il Presidio Civico in un immobile restituito (R-05)')],
        punti=[('forno_pane_nero', 'nordest', 'M-TP-01: i forni del Pane Nero')]),
    (6, 5): dict(tema='paese', titolo='Gibellina Nuova, la Stella del Belice', tema_extra=dict(
        facciate=('fac_cemento', 'fac_intonaco')), elementi=[
        mon('traliccio', punto='stella_del_belice', zona='nord', nota='M-TP-02: la Stella di Consagra all’ingresso')]),
    (7, 5): dict(tema='campagna', titolo='Gibellina, salita al Grande Cretto', erba=True,
                 elementi=[canc('MAP_TP_GRANDE_CRETTO', dentro=(), w=9, zona='nord',
                                nota='M-TP-02 / D-TP-05: il Grande Cretto (R-05: niente lotte)')]),
    (3, 6): dict(tema='tufo', titolo='Mazara del Vallo, Porto Canale e Kasbah', elementi=[
        pal('MAP_TP_MAZARA_MUSEO_SATIRO', w=6, d=4, h=56, fac='fac_barocca', tetto='tetto_coppi', zona='nordovest',
            nota='S-TP-05: il Museo del Satiro Danzante (Sant’Egidio)'),
        casa('MAP_TP_MAZARA_CORTILE_KASBAH', w=5, d=3, fac='maiolica', tetto='tetto_piano', zona='nordest',
             nota='M-TP-03: il cortile maiolicato della Kasbah')],
        punti=[('kasbah_vicoli', 'est', 'M-TP-03: i vicoli maiolicati')]),
    (4, 6): dict(tema='tufo', titolo='Mazara del Vallo, cantieri navali e lungomare', elementi=[
        gr(('barca',), 6, 1, zona='sud', passo=2, blocca=True)],
        punti=[('capitan_ciccio', 'sudovest', 'S-TP-05: Capitan Ciccio, il comandante del peschereccio')]),
    (2, 5): dict(tema='tufo', titolo='Marsala, Porta Garibaldi e le cantine', elementi=[
        pal(None, w=6, d=3, h=48, fac='fac_tufo', zona='nordovest', nome='porta_garibaldi'),
        pal(None, w=8, d=4, h=40, fac='fac_tufo', tetto='tetto_coppi', zona='nordest', nome='cantina_storica')],
        punti=[('piazza_repubblica', 'ovest', 'M-TP-03: piazza della Repubblica')]),
    (3, 5): dict(tema='vigne', titolo='Marsala, contrade e crinali eolici', erba=True, elementi=[
        filari(12, 6, pianta='vite', zona='sudovest', terreno='terra'),
        gr(('pala_eolica',), 6, 1, zona='nordest', passo=2)]),
    (1, 5): dict(tema='saline', titolo='Stagnone, le Saline e l’imbarcadero', elementi=[
        saline(w=14, d=9, zona='nordest', punti=2, nome='salinaio', nota='M-TP-03: le Saline dello Stagnone'),
        canc('MAP_TP_STAGNONE_LAGUNA', dentro=(), w=7, zona='sudest',
             nota='M-TP-03 / D-TP-02 / S-TP-04: l’imbarcadero per la laguna e Mozia')]),
    (1, 4): dict(tema='saline', titolo='Trapani, le Saline e la Torre di Ligny', elementi=[
        saline(w=12, d=9, zona='centro', punti=1, nome='salinaio', nota='S-TP-02: il salinaio e il fior di sale'),
        castello(None, w=5, d=5, h=48, fac='tufo', zona='nordovest', nome='torre_di_ligny')]),
    (2, 4): dict(tema='tufo', titolo='Trapani, centro storico e Porto Aliscafi', elementi=[
        pal('MAP_TP_TRAPANI_IMBARCO', w=7, d=3, h=32, fac='vetrata', tetto='lamiera', porta='porta_vetro',
            zona='nordovest', nota='S-TP-07: Terminal Aliscafi per Favignana'),
        gr(('cartello',), 3, 1, zona='nordest', passo=1, punto='cartelli_45_gradi',
           nota='E-TP-01: i cartelli inclinati dal vento')],
        punti=[('fermata_pullman', 'sudovest', 'M-TP-05: la fermata del pullman delle 5:40 (si sale con uno script)'),
               ('cartello_st09', 'sudest', 'E-TP-02: cartello ST-09 della stazione'),
               ('comizio_trapani', 'centro', 'M-TP-04 / ST-01: comizio finale dopo Vito Asaro')]),
    (3, 4): dict(tema='paese_tufo', titolo='Trapani, la stazione di valle della funivia', elementi=[
        casa(None, w=5, d=3, fac='fac_cemento', tetto='tetto_cemento', zona='nord', nome='funivia_valle')],
        punti=[('funivia_valle', 'nord', 'E-TP-03: la funivia ferma col Drifblim legato al cavo')]),
    (2, 3): dict(tema='paese_monti', titolo='Erice, Castello di Venere e Giardini del Balio', elementi=[
        castello('MAP_TP_CASTELLO_VENERE_CORTILI', w=9, d=7, h=64, fac='muro_calcare', zona='nord',
                 nota='M-TP-04 / D-TP-04: il Castello di Venere (Segreteria 6)'),
        filari(8, 4, pianta='pino', zona='sudovest', terreno='erba'),
        castello(None, w=5, d=5, h=48, fac='muro_calcare', zona='sudest', nome='torri_pepoli')]),
    (3, 3): dict(tema='paese_monti', titolo='Erice, Porta Trapani e il Duomo', elementi=[
        catt(None, fac='muro_calcare', zona='nordest'),
        casa('MAP_TP_ERICE_PASTICCERIA', w=4, d=3, fac='muro_calcare', zona='nordovest',
             nota='S-TP-03: la pasticceria delle genovesi')],
        punti=[('funivia_monte', 'sud', 'E-TP-03: la stazione di monte della funivia')]),
    (3, 2): dict(tema='spiaggia', titolo='San Vito Lo Capo, la spiaggia', erba=True),
    (4, 2): dict(tema='paese_tufo', titolo='San Vito Lo Capo, il lungomare', elementi=[
        gr(('tavolino',), 4, 2, zona='centro', punto='gara_cous_cous', nota='S-TP-01 / ST-03: la gara del cous cous')],
        punti=[('cous_cous_snorlax', 'sud', 'E-TP-04: il piatto di cous cous che attira uno Snorlax')]),
    (5, 2): dict(tema='macchia', titolo='Riserva dello Zingaro, ingresso nord', erba=True,
                 punti=[('guardia_forestale', 'centro', 'S-TP-06: le guardie forestali')]),
    (6, 2): dict(tema='macchia', titolo='Riserva dello Zingaro, Cala Capreria', erba=True,
                 punti=[('nido_1', 'nordest', 'S-TP-06: nido di Staraptor'), ('nido_2', 'sudovest', 'S-TP-06: nido di Pidgeot')]),
    (6, 3): dict(tema='paese_tufo', titolo='Scopello, il baglio e i faraglioni', faraglioni=True, elementi=[
        pal(None, w=7, d=4, h=32, fac='fac_tufo', tetto='tetto_coppi', zona='sudovest', nome='baglio')]),
    (7, 3): dict(tema='paese_tufo', titolo='Castellammare del Golfo, il porto e il castello', elementi=[
        castello(None, w=7, d=5, h=48, fac='muro_calcare', zona='nordovest')]),
    (7, 4): dict(tema='paese_tufo', titolo='Alcamo, piazza Ciullo e il Castello', elementi=[
        castello(None, w=7, d=6, h=56, fac='muro_calcare', zona='nordovest')],
        punti=[('cambiavoti_alcamo', 'est', 'S-TP-08 / ST-06: Cambiavoti di Trapani in piazza Ciullo')]),
    (8, 4): dict(tema='vigne', titolo='Alcamo, Monte Bonifato', erba=True),
    # ----------------------------------------------------------------------- Palermo (PA)
    (10, 2): dict(tema='industria', titolo='Cinisi, aeroporto di Punta Raisi', riempi='case', elementi=[
        pal(None, w=12, d=4, h=40, fac='vetrata', tetto='lamiera', porta='porta_vetro', zona='nord', nome='aerostazione')],
        punti=[('arrivo_volo', 'centro', 'M-ME-08: l’arrivo in volo a Punta Raisi')]),
    (10, 3): dict(tema='paese', titolo='Cinisi, corso Umberto', props=('lampione',), elementi=[
        casa('MAP_PA_CINISI_CASA_MEMORIA', w=5, d=3, fac='fac_intonaco', zona='nordest',
             nota='M-PA-01: Casa Memoria (R-05.3, R-05.4)')],
        punti=[('cento_passi', 'centro', 'M-PA-01: i cento passi, in silenzio, con Maria e Totò')]),
    (11, 2): dict(tema='memoria', titolo='Isola delle Femmine, il lungomare', erba=False),
    (11, 3): dict(tema='memoria', titolo='Capaci, il Giardino della Memoria', erba=False, elementi=[
        gr(('stele',), 5, 1, zona='centro', passo=1, punto='steli_capaci',
           nota='M-PA-02: le steli; FLAG_CAPACI_MEMORIAL_SILENCE (R-05.4: niente lotte, niente selvatici)')]),
    (9, 3): dict(tema='paese', titolo='Partinico, il paese', erba=True),
    (9, 4): dict(tema='paese', titolo='Partinico, verso la Valle dello Jato', erba=True,
                 punti=[('contadini_a_secco', 'sud', 'S-PA-08: i contadini lasciati a secco')]),
    (10, 4): dict(tema='vigne', titolo='Partinico, la campagna', erba=True),
    (9, 5): dict(tema='campagna', titolo='Diga Jato, l’invaso (nord-ovest)', erba=True, elementi=[
        spec(18, 12, punti=0, zona='sudest', acqua='acqua')]),
    (10, 5): dict(tema='campagna', titolo='Diga Jato, l’invaso (nord-est)', erba=True, elementi=[
        spec(18, 12, punti=0, zona='sudovest', acqua='acqua')]),
    (9, 6): dict(tema='campagna', titolo='Diga Jato, la diga e le chiuse', erba=True, elementi=[
        dict(tipo='rupe', w=14, d=2, h=40, roccia='fac_cemento', zona='nord'),
        dict(tipo='condotta', w=12, autobotti=0, zona='centro', punto='chiusa_1', nota='S-PA-08: la prima chiusa')],
        punti=[('chiusa_2', 'est', 'S-PA-08: la seconda chiusa'), ('chiusa_3', 'sud', 'S-PA-08: la terza chiusa')]),
    (10, 6): dict(tema='campagna', titolo='Diga Jato, la valle sotto la diga', erba=True),
    (11, 1): dict(tema='spiaggia', titolo='Mondello, Capo Gallo', erba=True),
    (12, 1): dict(tema='spiaggia', titolo='Mondello, la spiaggia e i villini', elementi=[
        pal(None, w=6, d=4, h=48, fac='fac_liberty', tetto='tetto_coppi', zona='nordest', nome='charleston'),
        gr(('auto', 'auto'), 6, 1, zona='centro', passo=2, punto='parcheggio_abusivo',
           nota='B-PA-01: il Parcheggiatore Capo di Mondello coi Manzuni')]),
    (12, 2): dict(tema='periferia', titolo='Palermo, ZEN 2', erba=True, elementi=[
        pal(None, w=12, d=5, h=96, fac='fac_cemento', tetto='tetto_cemento', zona='nord', nome='insula'),
        gr(SACCHI, 3, 1, zona='sudovest')],
        punti=[('cambiavoti_zen', 'centro', 'S-PA-10 / ST-06: il 9° Cambiavoti con Chantal; UrnaElettor. se 9/9')]),
    (13, 1): dict(tema='rocca', titolo='Monte Pellegrino, l’Addaura', erba=True, elementi=[
        imb('MAP_PA_MONTE_PELLEGRINO_GROTTE', roccia='roccia', w=6, zona='sud',
            nota='D-PA-01: la Grotta dell’Addaura')]),
    (13, 2): dict(tema='rocca', titolo='Monte Pellegrino, il Santuario di Santa Rosalia', erba=True, elementi=[
        rupe(10, 3, roccia='roccia', h=48, zona='nordovest'),
        pal(None, w=6, d=3, h=40, fac='muro_calcare', tetto='tetto_coppi', zona='nordest', nome='santuario')]),
    (14, 2): dict(tema='strada_citta', titolo='Monte Pellegrino, piazzale della Fiera', elementi=[
        canc('MAP_PA_FIERA_INGRESSO_ESTERNO', dentro=(), w=11, zona='nord',
             nota='P-09: il viale della Fiera del Mediterraneo (post-game)')]),
    (15, 2): dict(tema='palermo', titolo='Palermo, Borgo Vecchio', elementi=[
        gr(MERCATO, 6, 1, zona='centro', passo=2)],
        punti=[('cartello_st09', 'sudovest', 'E-PA-03: cartello ST-09 al porto di Palermo')]),
    (16, 2): dict(tema='palermo', titolo='Palermo, il porto', elementi=[
        gr(('traghetto',), 4, 1, zona='nord', passo=2)]),
    (13, 3): dict(tema='palermo', titolo='Palermo, Teatro Politeama e via Libertà', elementi=[
        pal(None, w=12, d=5, h=64, fac='fac_liberty', tetto='tetto_piano', zona='nord', nome='politeama')],
        punti=[('cancello_consenso', 'sud', 'M-PA-03: il cancello del Consenso >= 40'),
               ('comizio_politeama', 'centro', 'M-PA-05: comizio di provincia al Politeama')]),
    (14, 3): dict(tema='palermo', titolo='Palermo, piazza Politeama'),
    (15, 3): dict(tema='palermo', titolo='Palermo, Teatro Massimo, via Maqueda e piazza Pretoria', elementi=[
        pal(None, w=10, d=5, h=80, fac='fac_liberty', tetto='tetto_piano', zona='nordovest', nome='teatro_massimo'),
        pal('MAP_PA_PALAZZO_AQUILE_CORRIDOI', w=8, d=4, h=64, fac='fac_barocca', zona='nordest',
            nota='M-PA-05 / D-PA-05: Palazzo delle Aquile (Segreteria 8)'),
        mon('statua', punto='fontana_pretoria', zona='sudest', nota='piazza Pretoria')],
        punti=[('manifesto_mankey', 'ovest', 'S-PA-01 / ST-03: il manifesto dei Mankey di Turi'),
               ('festino', 'centro', 'S-PA-09: il Festino lungo il Cassaro, 14–15 luglio'),
               ('fermata_101', 'sud', 'E-PA-04: lo Slowpoke che aspetta il 101')]),
    (16, 3): dict(tema='palermo', titolo='Palermo, Vucciria, Kalsa e piazza Marina', elementi=[
        casa('MAP_PA_PALERMO_COVO_CASSIERE', w=4, d=3, fac='fac_intonaco', tetto='tetto_piano', porta='saracinesca',
             zona='nordest', nota='B-PA-04: il covo di U Cassiere (ST-04)'),
        gr(MERCATO, 6, 2, zona='nordovest', passo=2, punto='meusaio', nota='S-PA-02: il meusaio col Magby'),
        mon('statua', punto='genio_di_palermo', zona='sudest', nota='E-PA-05: il Genio col serpente')],
        punti=[('coccodrillo', 'sudovest', 'E-PA-02: il coccodrillo della Vucciria')]),
    (14, 4): dict(tema='palermo', titolo='Palermo, Albergheria e San Giovanni degli Eremiti', elementi=[
        normanna(None, w=7, d=4, zona='nordovest', cupole=3, nome='san_giovanni_eremiti'),
        gr(MERCATO, 6, 2, zona='sudest', passo=2)],
        punti=[('disputa_arancina', 'centro', 'E-PA-01: «arancina» o «arancinu»')]),
    (15, 4): dict(tema='palermo', titolo='Palermo, Mercato di Ballarò', elementi=[
        casa('MAP_PA_PALERMO_CASA_TOTO', w=4, d=3, fac='fac_intonaco', tetto='tetto_piano', zona='nordest',
             nota='M-PA-03 / ST-07 / P-01: la casa di Totò'),
        gr(MERCATO, 8, 2, zona='centro', passo=2, punto='ballaro', nota='M-PA-03: Totò e PaniCaMeusa a Ballarò')]),
    (13, 4): dict(tema='palermo', titolo='Palermo, Porta Nuova e Palazzo dei Normanni', elementi=[
        pal('MAP_PA_PALERMO_LEGA_INGRESSO', w=9, d=5, h=64, fac='fac_normanna', tetto='tetto_piano',
            pos=(12, 15), dx=4, nota='M-EN-04: ingresso della Lega dell’ARS (porta a (16,19), atterraggio del Volo)'),
        pal(None, w=5, d=3, h=72, fac='fac_normanna', zona='nordovest', nome='porta_nuova')],
        punti=[('notte_dello_spoglio', 'sud', 'M-EN-04: la notte dello spoglio'),
               ('palazzo_orleans', 'est', 'M-EN-08: i sei mesi a Palazzo d’Orléans')]),
    (12, 5): dict(tema='paese', titolo='Monreale, il belvedere sulla Conca d’Oro', erba=True, elementi=[
        filari(10, 4, pianta='albero', zona='sud', terreno='terra')]),
    (13, 5): dict(tema='paese', titolo='Monreale, il Duomo', elementi=[
        catt('MAP_PA_MONREALE_DUOMO', fac='fac_normanna', zona='nord', nota='S-PA-03: il Duomo di Monreale')]),
    (14, 5): dict(tema='paese', titolo='Piana degli Albanesi, Hora e Arbëreshëvet',
                  punti=[('cartello_bilingue_%d' % k, z, 'S-PA-07: cartello bilingue arbëreshë') for k, z in
                         enumerate(('nord', 'est', 'sud', 'ovest', 'centro'), 1)]),
    (15, 5): dict(tema='paese', titolo='Piana degli Albanesi, il lago', erba=True, elementi=[
        spec(14, 8, punti=0, zona='sud', acqua='acqua')],
        punti=[('cannolo', 'nord', 'S-PA-07: il cannolo finale')]),
    (16, 5): dict(tema='memoria', titolo='Piana degli Albanesi, verso Portella della Ginestra', erba=True, elementi=[
        canc('MAP_PA_PORTELLA_DELLA_GINESTRA', dentro=(), w=7, zona='nord',
             nota='S-PA-07: Portella della Ginestra (R-05.4)')]),
    (13, 6): dict(tema='paese_monti', titolo='Corleone, il paese'),
    (14, 6): dict(tema='paese_monti', titolo='Corleone, il CIDMA', elementi=[
        pal('MAP_PA_CORLEONE_CIDMA', w=7, d=4, h=48, fac='fac_intonaco', zona='nordovest',
            nota='M-PA-04: il CIDMA, visita sobria con Maria (R-05.4)')]),
    (15, 6): dict(tema='montagna', titolo='Corleone, la Cascata delle Due Rocche', erba=True, elementi=[
        dict(tipo='ponte', pos=(14, 22), w=3, punto='cascata_due_rocche',
             nota='M-PA-04: la Cascata delle Due Rocche (Cascata)'),
        rupe(8, 3, roccia='roccia', h=64, zona='nordovest'), rupe(8, 3, roccia='roccia', h=64, zona='nordest')]),
    (16, 6): dict(tema='montagna', titolo='Bosco di Ficuzza, la radura', erba=True, elementi=[
        canc('MAP_PA_FICUZZA_VOLIERE_PIZZINI', dentro=('alberi',), w=9, zona='nord',
             nota='D-PA-02 / M-PA-04: le voliere dei pizzini alati')]),
    (17, 6): dict(tema='montagna', titolo='Bosco di Ficuzza, Rocca Busambra', erba=True, elementi=[
        dict(tipo='parete', verso='MAP_PA_ROCCA_BUSAMBRA_VETTA', w=2, d=7, roccia='roccia', cima='terra', zona='nord',
             nota='P-03 / P-07: la parete di Rocca Busambra (Scalaroccia, post-game)')]),
    (17, 5): dict(tema='montagna', titolo='Bosco di Ficuzza, la Palazzina Reale', erba=True, elementi=[
        pal(None, w=9, d=4, h=48, fac='fac_intonaco', tetto='tetto_coppi', zona='nord', nome='palazzina_reale')],
        punti=[('registri_scambio', 'centro', 'M-PA-04: le carte di Ficuzza')]),
    (17, 3): dict(tema='paese', titolo='Bagheria, la borgata di Aspra', erba=True, elementi=[
        gr(('barca',), 6, 1, zona='nord', passo=2)]),
    (17, 4): dict(tema='palermo', titolo='Bagheria, Villa Palagonia', elementi=[
        pal('MAP_PA_BAGHERIA_VILLA_PALAGONIA', w=9, d=4, h=56, fac='fac_barocca', tetto='tetto_coppi', zona='nord',
            nota='D-PA-03 / S-PA-04: Villa Palagonia, la Villa dei Mostri'),
        gr(('statua',), 6, 1, zona='centro', passo=1)]),
    (18, 4): dict(tema='paese', titolo='Bagheria, le ville settecentesche', erba=True, elementi=[
        pal(None, w=8, d=4, h=48, fac='fac_barocca', tetto='tetto_coppi', zona='nord', nome='villa_cattolica')]),
    (20, 3): dict(tema='paese', titolo='Termini Imerese, il porto', erba=True, elementi=[
        gr(('barca',), 4, 1, zona='nord', passo=2)]),
    (21, 3): dict(tema='paese', titolo='Termini Imerese, il paese alto'),
    (19, 4): dict(tema='industria', titolo='Termini Imerese, il polo industriale', erba=True, elementi=[
        canc('MAP_PA_TERMINI_EX_STABILIMENTO', dentro=('traliccio',), w=11, zona='nord',
             nota='D-PA-04 / S-PA-05: l’ex stabilimento')],
        punti=[('ex_operaio', 'centro', 'S-PA-05: l’ex operaio davanti ai capannoni')]),
    (20, 4): dict(tema='industria', titolo='Termini Imerese, i capannoni', riempi='industria', erba=True),
    (22, 3): dict(tema='barocco', titolo='Cefalù, il lungomare'),
    (23, 3): dict(tema='rocca', titolo='Cefalù, la Rocca e il Tempio di Diana', erba=True, elementi=[
        rupe(14, 5, roccia='roccia', h=96, zona='nord'),
        rov(8, 4, punto='tempio_di_diana', zona='centro', nota='S-PA-06: il Guardiano della Rocca')]),
    (24, 3): dict(tema='barocco', titolo='Cefalù, il Duomo normanno', elementi=[
        catt(None, fac='fac_normanna', zona='nordovest')]),
    (21, 5): dict(tema='montagna', titolo='Alte Madonie, Polizzi', erba=True),
    (22, 5): dict(tema='montagna', titolo='Alte Madonie, Petralia', erba=True,
                  punti=[('raccordo_madonie', 'centro', 'M-EN-01: il raccordo montano')]),
    (23, 5): dict(tema='montagna', titolo='Alte Madonie, i faggeti', erba=True),
    (24, 5): dict(tema='paese_monti', titolo='Alte Madonie, Gangi', erba=True),
    # ----------------------------------------------------------------------- Enna (EN)
    (28, 3): dict(tema='paese_monti', titolo='Nicosia, San Nicolò', elementi=[catt(None, fac='muro_calcare', zona='nord')],
                  punti=[('sacrestano_san_nicolo', 'nord', 'S-EN-01: il sacrestano di San Nicolò')]),
    (29, 3): dict(tema='paese_monti', titolo='Nicosia, il centro'),
    (30, 3): dict(tema='paese_monti', titolo='Nicosia, Santa Maria Maggiore', elementi=[
        catt(None, fac='fac_barocca', zona='nord')],
        punti=[('sacrestano_santa_maria', 'nord', 'S-EN-01: il sacrestano di Santa Maria Maggiore')]),
    (31, 3): dict(tema='paese_monti', titolo='Nicosia, verso Troina', erba=True),
    (31, 2): dict(tema='montagna', titolo='Nicosia, i boschi a nord', erba=True),
    (32, 2): dict(tema='montagna', titolo='Nicosia, verso i Nebrodi', erba=True),
    (26, 3): dict(tema='paese_monti', titolo='Sperlinga, il castello nella roccia', elementi=[
        rupe(12, 4, roccia='tufo', h=64, zona='nord'),
        imb('MAP_EN_CASTELLO_DI_SPERLINGA', roccia='tufo', w=5, zona='nord', nota='S-EN-02 / D-EN-02: Sperlinga negavit')]),
    (25, 3): dict(tema='paese_monti', titolo='Sperlinga, le case grotta', erba=True),
    (27, 3): dict(tema='paese_monti', titolo='Sperlinga, il borgo', erba=True),
    (29, 5): dict(tema='paese_monti', titolo='Leonforte, la Granfonte', elementi=[
        dict(tipo='rupe', w=12, d=1, h=24, roccia='muro_calcare', zona='nord', punto='granfonte',
             nota='S-EN-04: la Granfonte')]),
    (30, 4): dict(tema='campagna', titolo='Leonforte, i pescheti', erba=True, elementi=[
        filari(12, 6, pianta='albero', zona='centro', terreno='terra')],
        punti=[('pescheto', 'sud', 'S-EN-04: insacchettare le pesche')]),
    (31, 5): dict(tema='periferia', titolo='Agira, Sicilia Outlet Village (ovest)', erba=False, elementi=[
        pal(None, w=12, d=4, h=40, fac='fac_negozio', tetto='tetto_piano', porta='porta_vetro', insegna=True,
            zona='nord', nome='outlet_ovest'),
        gr(('auto',), 8, 2, zona='sud', passo=2)]),
    (32, 5): dict(tema='periferia', titolo='Agira, Sicilia Outlet Village (est)', erba=False, elementi=[
        pal(None, w=12, d=4, h=40, fac='fac_negozio', tetto='tetto_piano', porta='porta_vetro', insegna=True,
            zona='nord', nome='outlet_est'),
        gr(('auto',), 8, 2, zona='centro', passo=2, punto='parcheggio_outlet',
           nota='S-EN-03: il parcheggio della domenica; M-EN-01: il blocco domenicale')]),
    (33, 4): dict(tema='paese_monti', titolo='Centuripe, la stella', erba=True,
                  punti=[('lettera_urgente', 'centro', 'S-EN-06: la lettera urgente per Catania')]),
    (29, 6): dict(tema='periferia', titolo='Enna Bassa, il Polo Universitario', elementi=[
        pal(None, w=12, d=4, h=48, fac='vetrata', tetto='tetto_piano', porta='porta_vetro', zona='nord', nome='universita')],
        punti=[('studente_fuori_corso', 'centro', 'E-EN-04: lo studente fuori corso col suo Slowpoke')]),
    (27, 6): dict(tema='paese_monti', titolo='Enna Alta, il Belvedere',
                  punti=[('cartello_st09', 'nordovest', 'E-EN-01: cartello ST-09 sul centro geografico'),
                         ('nebbia_psichica', 'est', 'E-EN-02: gli NPC che spariscono nella nebbia')]),
    (25, 7): dict(tema='paese_monti', titolo='Enna Alta, Castello di Lombardia e Rocca di Cerere', elementi=[
        castello(None, w=9, d=7, h=64, fac='muro_calcare', zona='nordovest'),
        canc('MAP_EN_ROCCA_DI_CERERE_NEBBIA', dentro=(), w=7, zona='nordest',
             nota='M-EN-03 / D-EN-03: la Rocca di Cerere nella nebbia (Segreteria 9)')]),
    (26, 7): dict(tema='paese_monti', titolo='Enna Alta, il Duomo', elementi=[catt(None, fac='muro_calcare', zona='nord')],
                  punti=[('comizio_enna', 'sud', 'M-EN-03 / ST-01: comizio finale di provincia')]),
    (26, 8): dict(tema='autodromo', titolo='Lago di Pergusa (nord)', erba=True, elementi=[
        spec(20, 10, punti=0, zona='sud', acqua='acqua')],
        punti=[('scagnozzo_pista_1', 'nord', 'M-EN-02: scagnozzi coi Rapidash e Yanmega')]),
    (26, 9): dict(tema='autodromo', titolo='Lago di Pergusa (sud)', erba=True, elementi=[
        spec(20, 10, punti=1, nome='lago_che_non_ce', zona='nord', acqua='acqua',
             nota='M-EN-02: il lago che non c’è, ultima tappa di ST-08')],
        punti=[('scagnozzo_pista_2', 'sud', 'M-EN-02: scagnozzi coi Rapidash e Yanmega')]),
    (25, 8): dict(tema='autodromo', titolo='Autodromo di Pergusa, curva ovest', erba=True,
                  punti=[('nonno_ape', 'centro', 'E-EN-03: il nonno in Ape 50 spinta da uno Slugma')]),
    (27, 9): dict(tema='autodromo', titolo='Autodromo di Pergusa, traguardo', erba=True,
                  punti=[('traguardo', 'centro', 'M-EN-02: la sfida a tempo lungo la pista')]),
    (29, 7): dict(tema='paese_monti', titolo='Aidone, il paese', erba=True),
    (31, 7): dict(tema='templi', titolo='Morgantina, l’agorà', erba=True, elementi=[
        rov(12, 6, punto='agora', zona='centro', nota='S-EN-05: la guida e il suo Xatu tra le rovine')]),
    (31, 8): dict(tema='templi', titolo='Morgantina, il teatro', erba=True, elementi=[
        dict(tipo='teatro', w=14, d=7, zona='nord', punto='teatro_morgantina', nota='S-EN-05: la Dea di Morgantina')]),
    (28, 8): dict(tema='paese_monti', titolo='Piazza Armerina, i quartieri alti', erba=True),
    (29, 8): dict(tema='paese_monti', titolo='Piazza Armerina, il centro',
                  punti=[('temporale_%d' % k, z, 'M-EN-05: i compagni sotto il temporale') for k, z in
                         enumerate(('nordovest', 'nord', 'nordest', 'ovest', 'est', 'sudovest', 'sud', 'sudest'), 1)]),
    (30, 8): dict(tema='paese_monti', titolo='Piazza Armerina, la Cattedrale', elementi=[
        catt(None, fac='fac_barocca', zona='nord')]),
    (28, 9): dict(tema='templi', titolo='Piazza Armerina, la Villa Romana del Casale', erba=True, elementi=[
        pal('MAP_EN_VILLA_ROMANA_CASALE_GALLERIE', w=12, d=5, h=40, fac='muro_calcare', tetto='lamiera',
            porta='portone', zona='nord', nota='M-EN-06 / D-EN-04: la Villa Romana del Casale')],
        punti=[('varco_villa', 'centro', 'M-EN-05: il varco aperto verso la Villa')]),
    # ----------------------------------------------------------------------- Messina (ME)
    (26, 0): dict(tema='paese', titolo='Sant’Agata di Militello, il lungomare'),
    (27, 0): dict(tema='paese', titolo='Sant’Agata di Militello, la stazione',
                  punti=[('arrivo_pullman', 'centro', 'M-TP-05: l’arrivo del pullman delle 5:40'),
                         ('verso_nebrodi', 'sud', 'M-ME-01: si parte verso i pascoli')]),
    (26, 1): dict(tema='paese_monti', titolo='San Fratello', erba=True,
                  punti=[('allevatori_rapidash', 'centro', 'M-ME-01: gli allevatori dei Rapidash sanfratellani')]),
    (28, 1): dict(tema='paese_monti', titolo='Mistretta', erba=True,
                  punti=[('denuncia_demanio', 'centro', 'M-ME-01: i terreni demaniali coi prestanome')]),
    (30, 1): dict(tema='montagna', titolo='Bosco dei Nebrodi, la faggeta ovest', erba=True),
    (31, 1): dict(tema='montagna', titolo='Bosco dei Nebrodi, i pascoli', erba=True, elementi=[
        canc('MAP_ME_NEBRODI_PASCOLI_FANTASMA', dentro=('alberi',), w=9, zona='nord',
             nota='D-ME-01 / M-ME-01: i pascoli fantasma')]),
    (32, 1): dict(tema='montagna', titolo='Bosco dei Nebrodi, la faggeta est', erba=True),
    (28, 0): dict(tema='spiaggia', titolo='Capo d’Orlando, il lungomare', erba=True,
                  punti=[('costa_tirrenica', 'centro', 'M-ME-02: la costa tirrenica')]),
    (29, 0): dict(tema='paese', titolo='Capo d’Orlando, il centro'),
    (32, 0): dict(tema='paese', titolo='Patti, il centro', erba=True),
    (33, 0): dict(tema='paese_monti', titolo='Tindari, il Santuario e i Laghetti di Marinello', erba=True, elementi=[
        catt('MAP_ME_TINDARI_SANTUARIO', fac='fac_intonaco', zona='nordovest', nota='S-ME-05: la Madonna Nera'),
        spec(10, 6, punti=2, nome='marinello', zona='sudest', acqua='mare_basso', riva='sabbia',
             nota='S-ME-05: le conchiglie levigate dagli Shellder')]),
    (36, 0): dict(tema='paese', titolo='Barcellona Pozzo di Gotto, il centro'),
    (37, 0): dict(tema='paese', titolo='Barcellona Pozzo di Gotto, il Longano', erba=True, elementi=[
        dict(tipo='ponte', pos=(13, 14), w=4, punto='passerella_longano', nota='S-ME-06: la passerella (Spallata)')]),
    (38, 0): dict(tema='paese', titolo='Milazzo, il Castello', elementi=[
        castello(None, w=11, d=7, h=64, fac='muro_calcare', zona='centro')]),
    (39, 0): dict(tema='paese', titolo='Milazzo, il lungomare'),
    (40, 0): dict(tema='paese', titolo='Milazzo, il porto e il molo dell’aliscafo', elementi=[
        gr(('traghetto',), 2, 1, zona='nordest', passo=2)],
        punti=[('molo_aliscafo', 'nordest', 'M-ME-02 / S-ME-02–04: il molo dell’aliscafo per le Eolie (script)')]),
    (43, 0): dict(tema='autostrada', titolo='A20, Barriera di Villafranca Tirrena', elementi=[
        dict(tipo='casello', w=6, zona='nordovest', punto='barriera', nota='M-ME-03: la Barriera di Villafranca')]),
    (44, 0): dict(tema='paese', titolo='Ganzirri, i laghi', erba=True, elementi=[
        spec(14, 8, punti=0, zona='centro', acqua='acqua')]),
    (45, 0): dict(tema='paese', titolo='Torre Faro, il pilone', elementi=[
        dict(tipo='pilone', zona='centro', punto='pippo_pilone', nota='M-ME-03: Pippo e il suo Piloni sotto il pilone')],
        punti=[('cartello_st09', 'sudovest', 'E-ME-01: cartello ST-09 aggiornato a ogni atto'),
               ('ritrovo_pippo', 'sud', 'P-01: Ritrovo settimanale con Pippo')]),
    (46, 0): dict(tema='paese', titolo='Capo Peloro, l’hangar e la feluca', elementi=[
        pal('MAP_ME_TORRE_FARO_HANGAR', w=8, d=4, h=40, fac='lamiera', tetto='lamiera', porta='saracinesca',
            zona='nordovest', nota='M-ME-07: l’hangar dell’elicottero'),
        canc('MAP_ME_GORGHI_DI_CARIDDI', dentro=(), w=7, zona='nordest',
             nota='S-ME-08 / D-ME-04: il pontile della feluca verso i Gorghi di Cariddi')]),
    (44, 1): dict(tema='messina', titolo='Messina, viale Giostra',
                  punti=[('cambiavoti_messina', 'centro', 'S-ME-09 / ST-06: Cambiavoti di Messina')]),
    (45, 1): dict(tema='messina', titolo='Messina, piazza Duomo e il Campanile', elementi=[
        catt(None, fac='fac_barocca', zona='nordovest')],
        punti=[('leone_campanile', 'nordovest', 'E-ME-03: il ruggito del leone a mezzogiorno'),
               ('focaccia', 'est', 'E-ME-04: la focaccia divisa con Pippo'),
               ('comizio_messina', 'sud', 'M-ME-06: comizio in piazza Duomo')]),
    (46, 1): dict(tema='messina', titolo='Messina, la Falce portuale', elementi=[
        pal('MAP_ME_ARCHIVI_STRETTO_ETERNA', w=8, d=4, h=80, fac='fac_cemento', tetto='tetto_cemento',
            porta='porta_vetro', zona='nordovest', nota='M-ME-04 / D-ME-02: gli Archivi della Società Stretto Eterna'),
        pal('MAP_ME_PALAZZO_PARTECIPATE_ATRIO', w=8, d=4, h=64, fac='fac_liberty', zona='sudovest',
            nota='M-ME-06: il Palazzo delle Partecipate (Segreteria 7)'),
        gr(('traghetto',), 2, 1, zona='nordest', passo=2)],
        punti=[('imbarco_traghetto', 'est', 'M-ME-08: l’imbarco sul traghetto dello Stretto (script)'),
               ('disputa_buddace', 'centro', 'E-ME-02: la disputa sul buddace')]),
    (42, 1): dict(tema='barocco', titolo='Taormina, corso Umberto e il Teatro Antico', elementi=[
        canc('MAP_ME_TAORMINA_TEATRO_ANTICO', dentro=(), w=9, zona='nordest',
             nota='M-ME-05: il galà del Teatro Antico (ST-05)')],
        punti=[('diretta_turi', 'ovest', 'S-ME-01 / ST-03: la diretta col filtro Meowth')]),
    (43, 1): dict(tema='spiaggia', titolo='Taormina, Isola Bella', erba=True, elementi=[
        gr(('ombrellone',), 6, 2, zona='sud', passo=3)],
        punti=[('lido_scoglio', 'sud', 'S-ME-07: il lido da 100 euro a scoglio')]),
    (42, 2): dict(tema='spiaggia', titolo='Giardini Naxos, il lungomare', erba=True,
                  punti=[('verso_gala', 'centro', 'M-ME-05: verso il galà')]),
    (43, 2): dict(tema='paese', titolo='Giardini Naxos, Capo Schisò', erba=True),
}

# Centri Pokémon senza punto di volo: porta a (16,19) come nelle città col volo (worldMapX/Y del Centro).
CENTRI_SENZA_VOLO = {(22, 10), (6, 6), (7, 3), (7, 4), (26, 0), (21, 3), (29, 3), (29, 8)}
# Mappe col punto di volo ma senza Centro: la porta a (16,19) porta altrove (Lega dell'ARS).
SENZA_CENTRO = {'MAP_PA_PALERMO_PALAZZO_NORMANNI'}

# Tema delle celle senza scheda, per mappa
TEMA_MAPPA = {
    'MAP_AG_LICATA': 'paese_tufo', 'MAP_AG_PALMA_DI_MONTECHIARO': 'paese_tufo', 'MAP_AG_CANICATTI': 'paese_tufo',
    'MAP_AG_FAVARA': 'paese_tufo', 'MAP_AG_AGRIGENTO': 'paese_tufo', 'MAP_AG_VALLE_DEI_TEMPLI': 'templi',
    'MAP_AG_PORTO_EMPEDOCLE': 'paese_tufo', 'MAP_AG_REALMONTE': 'paese_tufo', 'MAP_AG_ACQUEDOTTO_COSTIERO': 'campagna',
    'MAP_AG_SCIACCA': 'tufo',
    'MAP_TP_SELINUNTE': 'templi', 'MAP_TP_CASTELVETRANO': 'paese_tufo', 'MAP_TP_GIBELLINA': 'paese',
    'MAP_TP_MAZARA_DEL_VALLO': 'tufo', 'MAP_TP_MARSALA': 'tufo', 'MAP_TP_MARSALA_STAGNONE': 'saline',
    'MAP_TP_TRAPANI': 'tufo', 'MAP_TP_ERICE': 'paese_monti', 'MAP_TP_SAN_VITO_LO_CAPO': 'paese_tufo',
    'MAP_TP_ZINGARO': 'macchia', 'MAP_TP_CASTELLAMMARE_DEL_GOLFO': 'paese_tufo', 'MAP_TP_ALCAMO': 'paese_tufo',
    'MAP_PA_CINISI': 'paese', 'MAP_PA_CAPACI_ISOLA_DELLE_FEMMINE': 'memoria', 'MAP_PA_PARTINICO': 'paese',
    'MAP_PA_DIGA_JATO': 'campagna', 'MAP_PA_PALERMO_MONDELLO': 'spiaggia', 'MAP_PA_PALERMO_ZEN_2': 'periferia',
    'MAP_PA_MONTE_PELLEGRINO': 'rocca', 'MAP_PA_PALERMO_BORGO_VECCHIO_PORTO': 'palermo',
    'MAP_PA_PALERMO_POLITEAMA': 'palermo', 'MAP_PA_PALERMO_MASSIMO_MAQUEDA': 'palermo',
    'MAP_PA_PALERMO_VUCCIRIA_KALSA': 'palermo', 'MAP_PA_PALERMO_BALLARO': 'palermo', 'MAP_PA_MONREALE': 'paese',
    'MAP_PA_PIANA_DEGLI_ALBANESI': 'paese', 'MAP_PA_CORLEONE': 'paese_monti', 'MAP_PA_BOSCO_DI_FICUZZA': 'montagna',
    'MAP_PA_BAGHERIA': 'paese', 'MAP_PA_TERMINI_IMERESE': 'paese', 'MAP_PA_CEFALU': 'barocco',
    'MAP_PA_MADONIE_ALTE': 'montagna', 'MAP_PA_PALERMO_PALAZZO_NORMANNI': 'palermo',
    'MAP_EN_NICOSIA': 'paese_monti', 'MAP_EN_SPERLINGA': 'paese_monti', 'MAP_EN_LEONFORTE': 'paese_monti',
    'MAP_EN_AGIRA': 'paese_monti', 'MAP_EN_CENTURIPE': 'paese_monti', 'MAP_EN_ENNA_BASSA': 'periferia',
    'MAP_EN_ENNA_ALTA': 'paese_monti', 'MAP_EN_LAGO_DI_PERGUSA': 'autodromo', 'MAP_EN_AIDONE_MORGANTINA': 'paese_monti',
    'MAP_EN_PIAZZA_ARMERINA': 'paese_monti', 'MAP_EN_A19_TRAZZERE': 'campagna',
    'MAP_ME_SANT_AGATA_DI_MILITELLO': 'paese', 'MAP_ME_SAN_FRATELLO': 'paese_monti', 'MAP_ME_MISTRETTA': 'paese_monti',
    'MAP_ME_BOSCO_DEI_NEBRODI': 'montagna', 'MAP_ME_CAPO_D_ORLANDO': 'paese', 'MAP_ME_PATTI_TINDARI': 'paese',
    'MAP_ME_BARCELLONA_POZZO_DI_GOTTO': 'paese', 'MAP_ME_MILAZZO': 'paese', 'MAP_ME_TORRE_FARO_GANZIRRI': 'paese',
    'MAP_ME_MESSINA_GIOSTRA': 'messina', 'MAP_ME_MESSINA_CENTRO': 'messina', 'MAP_ME_TAORMINA': 'barocco',
    'MAP_ME_GIARDINI_NAXOS': 'spiaggia',
}

# Temi delle strade (le altre: «strada»)
TEMI_STRADE = {
    'MAP_STRADA_SS113_CAPO_ORLANDO_TINDARI': 'strada_costa',
    'MAP_STRADA_SS117_MISTRETTA_SANTO_STEFANO': 'strada_monti',
    'MAP_STRADA_SS185_SELLA_MANDRAZZI': 'strada_monti',
    'MAP_STRADA_A20_MILAZZO_MESSINA': 'autostrada_costa',
    'MAP_STRADA_A18_MESSINA_TAORMINA': 'autostrada_costa',
    'MAP_STRADA_SS120_TROINA_CESARO': 'strada_monti',
    'MAP_STRADA_SS117BIS_PIAZZA_ARMERINA': 'strada_monti',
    'MAP_STRADA_SS115_SCIACCA_SELINUNTE': 'strada_costa',
    'MAP_STRADA_SS624_SCIACCA_PALERMO': 'strada_vigne',
    'MAP_STRADA_A29_ALCAMO_MARSALA': 'autostrada',
    'MAP_STRADA_SS187_CASTELLAMMARE_TRAPANI': 'strada',
    'MAP_STRADA_A29_ALCAMO_PALERMO': 'autostrada_costa',
    'MAP_STRADA_VIALE_REGIONE_SICILIANA': 'strada_citta',
    'MAP_STRADA_SS186_PARTINICO_MONREALE': 'strada',
    'MAP_STRADA_SS624_ALTOFONTE_PIANA': 'strada',
    'MAP_STRADA_SS118_CORLEONE_MARINEO': 'strada_monti',
    'MAP_STRADA_SS113_PALERMO_BAGHERIA': 'strada_citta',
    'MAP_STRADA_A19_BAGHERIA_TERMINI': 'autostrada_costa',
    'MAP_STRADA_SS286_CEFALU_MADONIE': 'strada_monti',
    'MAP_STRADA_SS121_MISILMERI_LERCARA': 'strada',
}

# Le Trazzere dell'A19 (D-EN-01) sono una mappa ma hanno l'aspetto di una strada interrotta
for _c, _t in (((25, 5), 'D-EN-01: trazzera regia fra i piloni spezzati'), ((26, 5), 'D-EN-01'),
               ((27, 5), 'D-EN-01'), ((25, 6), 'D-EN-01'), ((26, 6), 'D-EN-01: verso Enna Alta')):
    SCHEDE[_c] = dict(tema='campagna', titolo='Trazzere e viadotti interrotti dell’A19', erba=True, elementi=[
        dict(tipo='piloni_rotti', w=20, h=80, zona='nord', punto='piloni_%d_%d' % _c, nota=_t + '; M-EN-01: la A19 a pezzi')])

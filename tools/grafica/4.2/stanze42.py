"""Stanze delle mappe interne con matrice nuova (registri 2.1 e 2.2, matrici 0288–0329).

Per ogni mappa: una lista di celle (da ovest a est, come «matrice.stanze» dei registri), ogni cella
con una o più stanze. Stanza chiusa: S(nome, preset, larghezza, altezza, punti). Mappa aperta:
A(nome, tema, elementi, punti, erba). FIGLIE: la mappa a cui porta il «su» dell'ultima stanza.
"""


def S(nome, preset, w=14, h=14, punti=0):
    return ('stanza', nome, preset, w, h, punti)


def A(nome, tema, elementi=(), punti=(), erba=False, **extra):
    return ('aperta', nome, tema, list(elementi), list(punti), erba, extra)


def gr(pezzi, w, d, zona='centro', **k):
    return dict(tipo='gruppo', pezzi=pezzi, w=w, d=d, zona=zona, **k)


STANZE = {
    # Catania
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02': [[S('piano_dispari', 'condominio', 12, 14, 1), S('piano_pari', 'condominio', 12, 14, 1)]],
    'MAP_CT_CATANIA_PALAZZO_ELEFANTI_ATRIO': [[S('atrio', 'sportelli', 20, 14, 2)], [S('corridoi_code', 'sportelli', 24, 12, 4)]],
    'MAP_CT_CATANIA_PALAZZO_ELEFANTI_SALA': [[S('sala_cali', 'salone', 14, 12, 1)]],
    'MAP_CT_CATANIA_CATTEDRALE': [[S('navata', 'chiesa', 16, 22, 2)]],
    'MAP_CT_CATANIA_CASTELLO_URSINO': [[S('museo', 'castello_lavico', 18, 16, 1)]],
    'MAP_CT_CATANIA_CASTELLO_URSINO_SOTTERRANEI': [[S('b1f', 'grotta_lavica', 22, 20, 1)], [S('b2f', 'grotta_lavica', 22, 20, 1)],
                                                   [S('b3f', 'grotta_lavica', 18, 16, 1)]],
    'MAP_CT_CATANIA_PRIVE_ZAGARA': [[S('prive', 'club', 18, 14, 3)]],
    'MAP_CT_CATANIA_TERMINAL_A_ATRIO': [[S('atrio', 'terminal', 24, 14, 2)], [S('controlli', 'terminal', 20, 12, 2)]],
    'MAP_CT_CATANIA_TERMINAL_A_GATE': [[S('gate', 'terminal', 24, 14, 2)], [S('sala_vip', 'salone', 14, 10, 1)]],
    'MAP_CT_CATANIA_PALAZZO_GIUSTIZIA': [[S('atrio', 'ufficio', 18, 14, 1)], [S('tetto', 'terrazza', 22, 18, 1)]],
    'MAP_CT_MISTERBIANCO_CUBBAR': [[S('pista', 'club', 22, 16, 6)]],
    'MAP_CT_ETNA_MONTI_ROSSI': [[A('pineta_in_fiamme', 'bosco', [gr(('braciere',), 6, 3, zona='nord')], erba=True)],
                                [A('colata_2001', 'etna', erba=True)]],
    'MAP_CT_ETNA_CRATERI_SILVESTRI': [[A('bocca_spenta', 'etna', [dict(tipo='fango', w=12, d=8, punti=1, nome='bocca',
                                                                         zona='centro')], erba=True)]],
    'MAP_CT_ETNA_CRATERE_CENTRALE': [[A('cratere', 'etna', [dict(tipo='fango', w=16, d=10, punti=1, nome='orlo',
                                                                  zona='nord')], [('fantasma', 'centro', 'P-04')])]],
    'MAP_CT_BRONTE_SCIARA': [[A('terrazze_basse', 'etna', [dict(tipo='filari', w=12, d=5, pianta='cespuglio', zona='nord'),
                                                           dict(tipo='filari', w=10, d=4, pianta='cespuglio', zona='sud')], erba=True)],
                             [A('terrazze_alte', 'etna', [dict(tipo='filari', w=10, d=5, pianta='cespuglio', zona='ovest'),
                                                          dict(tipo='casa', w=6, d=4, h=48, fac='fac_lavica', tetto='tetto_coppi',
                                                               porta=None, zona='nordest')],
                                [('don_saro', 'nordest', 'B-CT-04')], erba=True)]],
    'MAP_CT_CIRCUMETNEA_TRENO': [[S('carrozza', 'treno', 26, 6, 3)]],
    'MAP_CT_ETNA_GROTTA_DEL_GELO': [[S('1f', 'grotta_gelo', 22, 20, 1)], [S('b1f', 'grotta_gelo', 22, 20, 2)]],
    # Siracusa
    'MAP_SR_LENTINI_MAGAZZINI': [[S('magazzino_1', 'magazzino', 7, 14, 1), S('magazzino_2', 'magazzino', 7, 14, 1),
                                  S('magazzino_3', 'magazzino', 7, 14, 1)]],
    'MAP_SR_POLO_PONTILI_SERBATOI': [[A('pontili', 'industria', [dict(tipo='serbatoi', n=2, h=48, zona='nordovest')],
                                        erba=True, diag_mare=(), pre=[(0, 2, 32, 8, 'mare'), (13, 2, 6, 8, 'basolato')])],
                                     [A('serbatoi', 'industria', [dict(tipo='serbatoi', n=3, h=64, zona='nordovest'),
                                                                  dict(tipo='serbatoi', n=3, h=64, zona='nordest')], erba=True)]],
    'MAP_SR_POLO_SALA_CONTROLLO_TORCIA': [[S('sala_controllo', 'controllo', 20, 14, 2)],
                                          [A('torcia', 'industria', [gr(('torcia',), 3, 1, zona='nord', passo=1, punto='torcia',
                                                                        nota='M-SR-02: foto dello scarico')],
                                             [('ing_torcia', 'centro', 'B-SR-01')], erba=True)]],
    'MAP_SR_SIRACUSA_LATOMIE': [[S('paradiso', 'latomia', 24, 20, 2)], [S('orecchio_dionisio', 'latomia', 14, 20, 1)]],
    'MAP_SR_CASTELLO_MANIACE_INGRESSO': [[S('ingresso', 'castello', 18, 14, 1)], [S('cortile_a_marea', 'castello', 22, 18, 3)]],
    'MAP_SR_CASTELLO_MANIACE_SALA': [[S('sala_spataro', 'salone', 16, 12, 1)]],
    'MAP_SR_MARZAMEMI_TONNARA': [[S('camera_della_morte', 'tonnara', 22, 18, 2)], [S('magazzini_club', 'magazzino', 20, 14, 2)]],
    # Ragusa
    'MAP_RG_IBLA_SEGRETERIA_MAGAZZINI': [[S('frigo_1', 'frigo', 20, 16, 2)], [S('frigo_2', 'frigo', 20, 16, 2)]],
    'MAP_RG_IBLA_SEGRETERIA_UFFICIO': [[S('ufficio_occhipinti', 'salone', 14, 12, 1)]],
    'MAP_RG_IBLA_PALAZZO_MARCHESA': [[S('salone_marchesa', 'salone', 18, 14, 1)]],
    'MAP_RG_MODICA_LABORATORIO': 'laboratorio',
    'MAP_RG_MERCATO_PADIGLIONI': [[S('padiglione_1', 'mercato', 20, 16, 2)], [S('padiglione_2', 'mercato', 20, 16, 2)],
                                  [S('padiglione_3', 'mercato', 20, 16, 2)]],
    'MAP_RG_MERCATO_PIAZZALE': [[A('piazzale_ovest', 'industria', [gr(('auto',), 6, 2, zona='centro', passo=2)], erba=True)],
                                [A('piazzale_est', 'industria', [gr(('auto',), 6, 2, zona='centro', passo=2)],
                                   [('caporale_tir', 'centro', 'B-RG-01')], erba=True)]],
    'MAP_RG_COMISO_TERMINAL': [[S('terminal', 'terminal', 24, 16, 3)]],
    'MAP_RG_COMISO_BASE_NATO_HANGAR': [[S('hangar', 'hangar', 24, 18, 2)], [S('bunker', 'bunker', 16, 14, 1)]],
    'MAP_RG_COMISO_BASE_NATO_PISTA': [[S('sala_radar', 'radar', 20, 14, 2)],
                                      [A('pista', 'industria', [dict(tipo='filari', w=20, d=1, pianta='lampione', zona='centro')], erba=True)]],
    'MAP_RG_CAVA_D_ISPICA': [[S('necropoli', 'latomia', 24, 20, 5)], [S('larderia', 'latomia', 24, 20, 1)],
                             [S('grotte_alte', 'latomia', 20, 18, 1)]],
    # Caltanissetta
    'MAP_CL_NISCEMI_MUOS_RECINZIONE': [[A('perimetro', 'bosco', [gr(('recinzione',), 12, 1, zona='nord', passo=1)], erba=True)],
                                       [A('trasformatori', 'industria', [dict(tipo='serbatoi', n=2, h=32, zona='nord')], erba=True)]],
    'MAP_CL_NISCEMI_MUOS_PARABOLE': [[A('piazzale_parabole', 'industria', [gr(('traliccio', 'parabola'), 9, 3, zona='nord', passo=2)],
                                        [('subappaltatore', 'centro', 'B-CL-02')], erba=True)],
                                     [S('cabina_trasformatori', 'cabina', 16, 12, 1)]],
    'MAP_CL_VIADOTTO_SALSO_PILONI': [[A('campo_base', 'calanchi', [dict(tipo='serbatoi', n=2, h=32, zona='nordovest')], erba=True)],
                                     [A('piloni', 'calanchi', [gr(('traliccio',), 6, 1, zona='nord', passo=2)], erba=True)],
                                     [A('rampa_gru', 'calanchi', [gr(('traliccio',), 3, 1, zona='nord', passo=1)], erba=True)]],
    'MAP_CL_VIADOTTO_SALSO_CABINA': [[S('cabina_commissario', 'cabina', 14, 10, 1)]],
    'MAP_CL_GABBARA_ZOLFARA_GALLERIE': [[S('discenderia', 'zolfara', 24, 20, 1)], [S('galleria_carrelli', 'zolfara', 24, 20, 3)]],
    'MAP_CL_GABBARA_ZOLFARA_FONDO': [[S('camera_di_fondo', 'zolfara', 20, 16, 2)]],
    'MAP_CL_MUSSOMELI_UFFICI_COMUNALI': [[S('sportello', 'sportelli', 20, 14, 1)], [S('archivio_1924', 'archivio', 20, 14, 1)]],
    'MAP_CL_CASTELLO_MANFREDONICO': [[S('cortile_scuderie', 'castello', 22, 18, 1)], [S('sala_baroni', 'castello', 22, 16, 1)],
                                     [S('sale_gotiche', 'castello', 20, 16, 2)]],
}

# Le mappe che condividono la matrice di un'altra (Palazzo di Cemento: 5 mappe, una matrice)
STESSA_MATRICE = {
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P03_P04': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02',
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P05_P06': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02',
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P07_P08': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02',
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P09_P10': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02',
}

FIGLIE = {
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P01_P02': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P03_P04',
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P03_P04': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P05_P06',
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P05_P06': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P07_P08',
    'MAP_CT_CATANIA_PALAZZO_CEMENTO_P07_P08': 'MAP_CT_CATANIA_PALAZZO_CEMENTO_P09_P10',
    'MAP_CT_CATANIA_PALAZZO_ELEFANTI_ATRIO': 'MAP_CT_CATANIA_PALAZZO_ELEFANTI_SALA',
    'MAP_CT_CATANIA_CASTELLO_URSINO': 'MAP_CT_CATANIA_CASTELLO_URSINO_SOTTERRANEI',
    'MAP_CT_CATANIA_TERMINAL_A_ATRIO': 'MAP_CT_CATANIA_TERMINAL_A_GATE',
    'MAP_CT_ETNA_MONTI_ROSSI': 'MAP_CT_ETNA_CRATERI_SILVESTRI',
    'MAP_CT_ETNA_CRATERI_SILVESTRI': 'MAP_CT_ETNA_SUD',
    'MAP_SR_CASTELLO_MANIACE_INGRESSO': 'MAP_SR_CASTELLO_MANIACE_SALA',
    'MAP_SR_POLO_PONTILI_SERBATOI': 'MAP_SR_POLO_SALA_CONTROLLO_TORCIA',
    'MAP_RG_IBLA_SEGRETERIA_MAGAZZINI': 'MAP_RG_IBLA_SEGRETERIA_UFFICIO',
    'MAP_RG_MERCATO_PADIGLIONI': 'MAP_RG_MERCATO_PIAZZALE',
    'MAP_RG_COMISO_BASE_NATO_HANGAR': 'MAP_RG_COMISO_BASE_NATO_PISTA',
    'MAP_CL_NISCEMI_MUOS_RECINZIONE': 'MAP_CL_NISCEMI_MUOS_PARABOLE',
    'MAP_CL_VIADOTTO_SALSO_PILONI': 'MAP_CL_VIADOTTO_SALSO_CABINA',
    'MAP_CL_GABBARA_ZOLFARA_GALLERIE': 'MAP_CL_GABBARA_ZOLFARA_FONDO',
}

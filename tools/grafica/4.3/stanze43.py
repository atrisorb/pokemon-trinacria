"""Stanze delle mappe con matrice nuova del blocco 4.3 (registri 2.2 e 2.3, matrici 0330–0383).

Per ogni mappa: una lista di celle (da ovest a est, come «matrice.stanze» dei registri), ogni cella
con una o più stanze. Stanza chiusa: S(nome, preset, larghezza, altezza, punti). Mappa aperta:
A(nome, tema, elementi, punti, erba, **extra) — anche le isole (Lampedusa, Favignana, Eolie,
Pantelleria), che sono esterni su una matrice propria. FIGLIE: la mappa a cui porta il «su»
dell'ultima stanza.
"""
from schede43 import pal, imb, canc, gr, spec, rov, saline


def S(nome, preset, w=14, h=14, punti=0):
    return ('stanza', nome, preset, w, h, punti)


def A(nome, tema, elementi=(), punti=(), erba=False, **extra):
    return ('aperta', nome, tema, list(elementi), list(punti), erba, extra)


MARE_NORD = [(0, 0, 32, 8, 'mare'), (0, 8, 32, 1, 'mare_basso')]

STANZE = {
    # Agrigento
    'MAP_AG_PALMA_MONASTERO': [[S('parlatorio_della_ruota', 'convento', 16, 12, 1)]],
    'MAP_AG_IPOGEI_GALLERIE': [[S('cunicoli', 'ipogeo', 22, 18, 2)], [S('chiuse', 'ipogeo', 22, 18, 2)]],
    'MAP_AG_IPOGEI_CISTERNA': [[S('grande_cisterna', 'cisterna', 22, 18, 2)]],
    'MAP_AG_VILLASETA_CANTIERI': [[S('piano_terra', 'cantiere', 22, 16, 2)], [S('impalcature', 'cantiere', 22, 16, 2)],
                                  [S('scale_attico', 'cantiere', 18, 14, 1)]],
    'MAP_AG_VILLASETA_ATTICO_IACONO': [[S('attico_piscina', 'attico', 20, 16, 1)]],
    'MAP_AG_LAMPEDUSA': [[A('porto', 'paese_tufo', [pal('MAP_AG_LAMPEDUSA_DEPOSITI', w=8, d=4, h=40, fac='lamiera',
                                                         tetto='lamiera', porta='saracinesca', zona='nordovest',
                                                         nota='M-AG-04: i depositi del carburante e il dissalatore'),
                                                     gr(('barca',), 4, 1, zona='sudest', passo=2)],
                            [('pescherecci_senza_gasolio', 'est', 'M-AG-04: i pescherecci rimasti senza gasolio')],
                            pc=True, isola=True)],
                         [A('spiaggia_dei_conigli', 'spiaggia', [canc('MAP_AG_LAMPEDUSA_PORTA_D_EUROPA', w=7, zona='nord',
                                                                      nota='M-AG-04: il sentiero verso la Porta d’Europa')],
                            [('biologi_marini', 'sud', 'S-AG-08: i biologi e la schiusa degli Squirtle e dei Lapras')],
                            erba=True, isola=True)]],
    'MAP_AG_LAMPEDUSA_DEPOSITI': [[S('depositi_carburante', 'magazzino', 22, 16, 1)],
                                  [S('dissalatore', 'cabina', 20, 14, 1)]],
    'MAP_AG_LAMPEDUSA_PORTA_D_EUROPA': [[A('cavallo_bianco', 'memoria', [], [
        ('porta_d_europa', 'nord', 'M-AG-04: la Porta d’Europa con Calogero e i volontari (R-05: niente lotte)')],
        pre=MARE_NORD)]],
    'MAP_AG_GROTTA_SCALA_DEI_TURCHI': [[S('grotta_di_marna', 'grotta_marna', 22, 18, 1)],
                                       [S('cavita_marina', 'grotta_marna', 22, 18, 2)]],
    'MAP_AG_SCIACCA_STUFE_KRONIO': [[S('stufa_bassa', 'stufe', 22, 18, 1)], [S('stufa_alta', 'stufe', 22, 18, 1)],
                                    [S('camera_sulfurea', 'stufe', 18, 14, 1)]],
    # Trapani
    'MAP_TP_CAVE_DI_CUSA': [[A('cave_ovest', 'cava', [dict(tipo='tempio', w=8, d=4, rovina=True, rocchi=6, zona='nord')],
                               erba=True)],
                            [A('rocchi_del_tempio_g', 'cava', [dict(tipo='tempio', w=10, d=4, rovina=True, rocchi=7, zona='nord')],
                               [('scalpellino', 'centro', 'B-TP-01: lo Scalpellino delle Cave')], erba=True)]],
    'MAP_TP_CASTELVETRANO_PRESIDIO_CIVICO': [[S('presidio_civico', 'archivio', 20, 14, 1)]],
    'MAP_TP_GRANDE_CRETTO': [[A('cretto_ovest', 'cretto')],
                             [A('cretto_est', 'cretto', [], [('anziano_abitante', 'centro',
                                                              'M-TP-02: l’anziano abitante; FLAG_CRETTO_DI_BURRI_EVENT')])]],
    'MAP_TP_MAZARA_MUSEO_SATIRO': [[S('museo_del_satiro', 'museo', 18, 14, 1)]],
    'MAP_TP_MAZARA_CORTILE_KASBAH': [[S('cortile_maiolicato', 'cortile', 20, 16, 1)]],
    'MAP_TP_STAGNONE_LAGUNA': [[A('saline_dello_stagnone', 'saline', [saline(w=20, d=9, zona='nord', punti=0)], erba=True)],
                               [A('parco_eolico', 'saline', [gr(('pala_eolica',), 10, 2, zona='nord', passo=2)],
                                  [('prestanome', 'centro', 'B-TP-02: il Prestanome; FLAG_WIND_FARM_SYNDICATE')], erba=True)],
                               [A('mozia', 'campagna', [rov(10, 5, punto='giovinetto_di_mozia', zona='nord',
                                                            nota='S-TP-04: il Giovinetto di Mozia')], erba=True)]],
    'MAP_TP_FAVIGNANA': [[A('porto_di_favignana', 'paese_tufo', [pal('MAP_TP_FAVIGNANA_TONNARA_FLORIO', w=8, d=4, h=48,
                                                                     fac='fac_tufo', tetto='tetto_coppi', zona='nordest',
                                                                     nota='S-TP-07: l’Ex Stabilimento Florio'),
                                                                 gr(('barca',), 4, 1, zona='sudovest', passo=2)],
                            isola=True)],
                         [A('verso_cala_rossa', 'cava', [canc('MAP_TP_FAVIGNANA_CALA_ROSSA', w=7, zona='nord',
                                                              nota='S-TP-07 / D-TP-03: le cave di Cala Rossa')], erba=True,
                            isola=True)]],
    'MAP_TP_FAVIGNANA_TONNARA_FLORIO': [[S('arcate_di_tufo', 'tonnara', 24, 18, 2)]],
    'MAP_TP_FAVIGNANA_CALA_ROSSA': [[A('cave_di_tufo', 'cava', erba=True)],
                                    [A('cala_rossa', 'cava', [], [('cala', 'nord', 'D-TP-03: la cala turchese')], erba=True,
                                       pre=MARE_NORD)]],
    'MAP_TP_CASTELLO_VENERE_CORTILI': [[S('cortile_normanno', 'castello', 22, 18, 2)],
                                       [S('torre_del_maestrale', 'castello', 20, 16, 2)]],
    'MAP_TP_CASTELLO_VENERE_LOGGIA': [[S('loggia_di_venere', 'salone', 18, 14, 1)]],
    'MAP_TP_PULLMAN_5_40': [[S('pullman_regionale', 'treno', 26, 6, 3)]],
    'MAP_TP_PANTELLERIA': [[A('porto_di_pantelleria', 'eolie', [gr(('barca',), 4, 1, zona='sudest', passo=2)], isola=True)],
                           [A('montagna_grande', 'vulcano', [canc('MAP_TP_PANTELLERIA_SPECCHIO_VENERE', w=7, zona='nord',
                                                                  nota='P-06: lo Specchio di Venere')], erba=True,
                              isola=True)]],
    'MAP_TP_PANTELLERIA_SPECCHIO_VENERE': [[A('sentiero_del_lago', 'vulcano', erba=True)],
                                           [A('specchio_di_venere', 'vulcano', [spec(18, 10, punti=0, zona='nord',
                                                                                      acqua='acqua', riva='sabbia')],
                                              [('quarto_fantasma', 'centro', 'P-06: il 4° Fantasma, allenatore 733')])]],
    # Messina
    'MAP_ME_NEBRODI_PASCOLI_FANTASMA': [[A('pascoli_fantasma', 'montagna', [gr(('recinzione',), 10, 1, zona='nord', passo=1)],
                                           [('pascolatore', 'centro', 'B-ME-01: il Pascolatore di Carta')], erba=True)],
                                        [S('casolare', 'stalla', 18, 14, 1)]],
    'MAP_ME_TINDARI_SANTUARIO': [[S('santuario_della_madonna_nera', 'chiesa', 16, 22, 1)]],
    'MAP_ME_ISOLE_EOLIE': [[A('lipari', 'eolie', [pal(None, w=8, d=4, h=40, fac='lamiera', tetto='lamiera', zona='nordest',
                                                      nome='dissalatore')],
                              [('dissalatore', 'nordest', 'S-ME-03 / ST-08: il dissalatore di Lipari'),
                               ('custode_pompe', 'centro', 'B-ME-04: il Custode delle Pompe')], isola=True)],
                           [A('vulcano', 'vulcano', [dict(tipo='fango', w=10, d=8, punti=3, nome='fumarola', zona='centro',
                                                          nota='S-ME-04: censire i Pokémon Fuoco/Veleno nei vapori')],
                              erba=True, isola=True)],
                           [A('stromboli', 'vulcano', [imb('MAP_ME_STROMBOLI_SCIARA_DEL_FUOCO', roccia='roccia_nera', w=5,
                                                           zona='nord', nota='S-ME-02 / D-ME-03: la Sciara del Fuoco')],
                              erba=True, isola=True)]],
    'MAP_ME_STROMBOLI_SCIARA_DEL_FUOCO': [[S('sciara_bassa', 'vulcano', 22, 18, 1)], [S('bocca_attiva', 'vulcano', 22, 18, 1)]],
    'MAP_ME_TORRE_FARO_HANGAR': [[S('hangar_elicottero', 'hangar', 24, 18, 1)]],
    'MAP_ME_GORGHI_DI_CARIDDI': [[A('gorgo_esterno', 'eolie', [spec(24, 18, punti=0, zona='centro', acqua='mare', riva='scoglio')])],
                                 [A('gorgo_centrale', 'eolie', [spec(24, 18, punti=1, nome='cariddi', zona='centro',
                                                                     acqua='mare', riva='scoglio',
                                                                     nota='S-ME-08: Cariddi (Aliscafu e Mulinello)')])]],
    'MAP_ME_ABISSO_CARIDDI': [[S('abisso', 'abisso', 22, 18, 1)]],
    'MAP_ME_ARCHIVI_STRETTO_ETERNA': [[S('piano_1', 'archivio', 12, 14, 1), S('piano_2', 'archivio', 12, 14, 1)],
                                      [S('piano_3', 'archivio', 12, 14, 1), S('piano_4', 'archivio', 12, 14, 1)],
                                      [S('piano_5', 'archivio', 20, 14, 1)]],
    'MAP_ME_PALAZZO_PARTECIPATE_ATRIO': [[S('antecamera', 'sportelli', 20, 14, 1)], [S('puzzle_magnetico', 'controllo', 22, 16, 2)]],
    'MAP_ME_PALAZZO_PARTECIPATE_SALA': [[S('sala_di_sturiale', 'salone', 18, 14, 1)]],
    'MAP_ME_TAORMINA_TEATRO_ANTICO': [[A('cavea', 'barocco', [dict(tipo='teatro', w=16, d=8, zona='nord', punto='cavea',
                                                                  nota='M-ME-05: il galà')], piazza=False)],
                                      [A('scena_del_gala', 'barocco', [pal(None, w=12, d=3, h=48, fac='muro_calcare',
                                                                           zona='nord', nome='frons_scaenae')],
                                         [('albergatore', 'centro', 'B-ME-03: l’Albergatore del Galà')], piazza=False)]],
    # Palermo
    'MAP_PA_CINISI_CASA_MEMORIA': [[S('casa_memoria', 'casa', 16, 12, 1)]],
    'MAP_PA_MONTE_PELLEGRINO_GROTTE': [[S('grotta_alta', 'grotta', 22, 18, 1)], [S('grotta_mediana', 'grotta', 22, 18, 1)],
                                       [S('grotta_delle_incisioni', 'grotta', 18, 16, 1)]],
    'MAP_PA_PALAZZO_AQUILE_CORRIDOI': [[S('piano_primo', 'sportelli', 22, 14, 2)], [S('piano_secondo', 'ufficio', 22, 14, 2)]],
    'MAP_PA_PALAZZO_AQUILE_SALA_SCADUTO': [[S('sala_di_scaduto', 'salone', 18, 14, 1)]],
    'MAP_PA_PALERMO_COVO_CASSIERE': [[S('covo', 'bunker', 18, 14, 1)]],
    'MAP_PA_PALERMO_CASA_TOTO': [[S('casa_dei_faldoni', 'archivio', 18, 14, 1)]],
    'MAP_PA_MONREALE_DUOMO': [[S('navata_d_oro', 'duomo_oro', 16, 22, 1)]],
    'MAP_PA_PORTELLA_DELLA_GINESTRA': [[A('portella', 'memoria', [gr(('stele',), 3, 1, zona='nord', passo=1, punto='lapide',
                                                                    nota='S-PA-07: luogo della memoria (R-05.4)')])]],
    'MAP_PA_CORLEONE_CIDMA': [[S('cidma', 'archivio', 18, 14, 1)]],
    'MAP_PA_FICUZZA_VOLIERE_PIZZINI': [[A('radura_delle_voliere', 'montagna', [gr(('recinzione',), 8, 1, zona='nord', passo=1)],
                                         [('massaro', 'centro', 'B-PA-02: il Massaro di Ficuzza')], erba=True)],
                                       [S('casotto_dei_registri', 'archivio', 16, 12, 1)]],
    'MAP_PA_ROCCA_BUSAMBRA_VETTA': [[A('vetta', 'rocca', [], [('primo_fantasma', 'centro', 'P-03: il 1° Fantasma, allenatore 730'),
                                                             ('tre_venti', 'nord', 'P-07: i Tre Venti di Sicilia')])]],
    'MAP_PA_BAGHERIA_VILLA_PALAGONIA': [[A('viale_dei_mostri', 'villa_mostri', [gr(('statua',), 8, 1, zona='nord', passo=1)],
                                          [('mostro_%d' % k, z, 'S-PA-04: una statua da riconoscere') for k, z in
                                           enumerate(('nordovest', 'nordest', 'sudovest', 'sudest'), 1)], piazza=False)],
                                        [A('cortile_ellittico', 'villa_mostri', [gr(('statua',), 8, 1, zona='sud', passo=1)],
                                           [('mostro_%d' % k, z, 'S-PA-04: una statua da riconoscere') for k, z in
                                            enumerate(('nordovest', 'nordest', 'sudovest', 'sudest'), 5)], piazza=False)]],
    'MAP_PA_TERMINI_EX_STABILIMENTO': [[S('reparto_lastratura', 'hangar', 24, 18, 1)],
                                       [S('reparto_verniciatura', 'hangar', 24, 18, 1)],
                                       [S('magazzino_ricambi', 'magazzino', 12, 14, 0),
                                        S('ufficio_del_liquidatore', 'ufficio', 12, 14, 1)]],
    'MAP_PA_PALERMO_VIA_DELLA_LEGA': [[S('piano_1', 'sportelli', 12, 14, 1), S('piano_2', 'ufficio', 12, 14, 1)],
                                      [S('piano_3', 'archivio', 12, 14, 1), S('piano_4', 'salone', 12, 14, 1)],
                                      [S('piano_5', 'salone', 20, 14, 1)]],
    # Enna
    'MAP_EN_CASTELLO_DI_SPERLINGA': [[S('piano_rupestre', 'grotta_tufo', 22, 18, 1)], [S('piano_alto', 'grotta_tufo', 20, 16, 1)]],
    'MAP_EN_ROCCA_DI_CERERE_NEBBIA': [[A('rocca_nella_nebbia', 'rocca', erba=True)],
                                      [A('tempio_di_cerere', 'rocca', [rov(10, 5, punto='ara_di_cerere', zona='nord',
                                                                           nota='D-EN-03: la nebbia psichica')], erba=True)]],
    'MAP_EN_COMMISSIONE_ELETTORALE': [[S('commissione', 'salone', 18, 14, 1)]],
    'MAP_EN_VILLA_ROMANA_CASALE_GALLERIE': [[S('peristilio', 'villa_romana', 22, 18, 2)],
                                            [S('ambulacro', 'villa_romana', 24, 12, 2)],
                                            [S('sala_delle_dieci_ragazze', 'villa_romana', 20, 16, 2)]],
    'MAP_EN_SALA_DELLA_GRANDE_CACCIA': [[S('sala_della_grande_caccia', 'villa_romana', 24, 14, 1)]],
}

STESSA_MATRICE = {}

FIGLIE = {
    'MAP_AG_IPOGEI_GALLERIE': 'MAP_AG_IPOGEI_CISTERNA',
    'MAP_AG_VILLASETA_CANTIERI': 'MAP_AG_VILLASETA_ATTICO_IACONO',
    'MAP_TP_CASTELLO_VENERE_CORTILI': 'MAP_TP_CASTELLO_VENERE_LOGGIA',
    'MAP_ME_PALAZZO_PARTECIPATE_ATRIO': 'MAP_ME_PALAZZO_PARTECIPATE_SALA',
    'MAP_ME_GORGHI_DI_CARIDDI': 'MAP_ME_ABISSO_CARIDDI',
    'MAP_PA_PALAZZO_AQUILE_CORRIDOI': 'MAP_PA_PALAZZO_AQUILE_SALA_SCADUTO',
    'MAP_PA_PALERMO_VIA_DELLA_LEGA': 'MAP_PA_PALERMO_LEGA_ATRIO',
    'MAP_EN_ROCCA_DI_CERERE_NEBBIA': 'MAP_EN_COMMISSIONE_ELETTORALE',
    'MAP_EN_VILLA_ROMANA_CASALE_GALLERIE': 'MAP_EN_SALA_DELLA_GRANDE_CACCIA',
}

# Isole: esterni su una matrice propria (arrivo dal traghetto o dall'aliscafo con uno script, Modulo 6)
ISOLE = ('MAP_AG_LAMPEDUSA', 'MAP_TP_FAVIGNANA', 'MAP_ME_ISOLE_EOLIE', 'MAP_TP_PANTELLERIA')

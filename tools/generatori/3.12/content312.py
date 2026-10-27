# Blocco 3.12: nomi, descrizioni e provenienza degli strumenti 361-536.
# (n, nome, genere, plurale, lemma_mcp, significato, nota, descrizione, altro)
# Come nel 3.11 (content311.py). Le MT 34-92 e le MN 01-08 (361-427) non sono qui: gen312.py le costruisce dalla
# mossa insegnata (R-STR-11); qui ci sono solo i loro premi e oggetti a terra (MT_ALTRO, per numero di strumento).
# nome «G30» = strumento del Glossario 3.0 (SH Scassatu, Ciucculatta); nome «IT» = nome italiano della trama
# (Amuleto, Atti, Faldoni: TRAMA_IT dello strumento di controllo, R-STR-18).
# Nelle descrizioni «[SP:SIMBOLO]» diventa il nome siciliano della specie (blocchi 3.1-3.5) e «[MV:Nome inglese]»
# il nome della mossa (blocchi 3.6-3.9); nelle note «{Specie}» diventa il numero della specie, come nel 3.11.

PROVINCE = {'CT': 'Catania', 'SR': 'Siracusa', 'RG': 'Ragusa', 'CL': 'Caltanissetta', 'AG': 'Agrigento',
            'TP': 'Trapani', 'ME': 'Messina', 'PA': 'Palermo', 'EN': 'Enna'}
# Atti di ST-02 e faldoni di ST-07 (R-STR-18): slot -> provincia. Le missioni e le mappe sono del registro 2.4
# (sezione «sottotrame»); l'elenco degli slot è anche nello strumento di controllo (ATTI, FALDONI).
ATTO_MISSIONE = {'CT': 'M-SR-04', 'SR': 'M-SR-05', 'RG': 'M-RG-04', 'CL': 'M-CL-04', 'AG': 'M-AG-05',
                 'TP': 'M-TP-04', 'ME': 'M-ME-06', 'PA': 'M-PA-04', 'EN': 'M-EN-03'}
FALDONE_MAPPA = {'CT': 'MAP_CT_CATANIA_PALAZZO_ELEFANTI_ATRIO', 'SR': 'MAP_SR_CASTELLO_MANIACE_INGRESSO',
                 'RG': 'MAP_RG_IBLA_SEGRETERIA_MAGAZZINI', 'CL': 'MAP_CL_VIADOTTO_SALSO_PILONI',
                 'AG': 'MAP_AG_VILLASETA_CANTIERI', 'TP': 'MAP_TP_CASTELLO_VENERE_CORTILI',
                 'ME': 'MAP_ME_PALAZZO_PARTECIPATE_ATRIO', 'PA': 'MAP_PA_PALAZZO_AQUILE_CORRIDOI',
                 'EN': 'MAP_EN_ROCCA_DI_CERERE_NEBBIA'}

_NO = 'Non si ottiene in Trinacria (R-STR-17): '
_TERRA = 'A terra: 1 in %s (FLAG_TR_ITEM_%s_*).'
_NASC = 'Nascosta: 1 in %s (FLAG_TR_HIDDEN_%s_*).'
_PG_TERRA = 'Post-game: 1 a terra in %s (FLAG_TR_ITEM_%s_*).'
_PG_NASC = 'Post-game: 1 nascosta in %s (FLAG_TR_HIDDEN_%s_*).'
_PESCA = ' Si usa vicino all’acqua per pescare i Pokémon.'
_PIRAZZU = ('Pirazzu %s dal profumo %s. Il maestro ceramista di Caltagirone ci fa una %s.')
_PIANTE = 'Dalle piante di Pirazzi (gli alberi delle Ghicocche di HeartGold, R-STR-19) di %s e %s: uno al giorno per pianta.'
_BALL = ('La fa il maestro ceramista di Caltagirone (S-CT-07) con un %s: si lascia un giorno e si ritira il giorno '
         'dopo (R-STR-19). Non si compra.')
_SCHEDA = 'Scheda coi record delle gare dei Pokémon: conta %s.'
_POKEATHLON = (_NO + 'in Trinacria non c’è il Pokéathlon (lo slot MAP_POKEATHLON_DOME è diventato '
               'MAP_AG_IPOGEI_GALLERIE, registro 2.2).')


def _atto(n, p):
    nota = ('Nome italiano della trama (ST-02, «Atto»), con la sigla della provincia: uno per provincia, come nel '
            'registro 2.4 (R-STR-18).')
    desc = 'Atto del Fascicolo Trinacria: carte sulle biotruffe di U Sistema in provincia di %s.' % PROVINCE[p]
    m = ATTO_MISSIONE[p]
    altro = 'Lo dà lo script di %s; VAR_ST_02 +1 (ST-02, registro 2.4). Unico.' % m
    if p == 'CT':
        altro = ('Lo dà lo script di M-SR-04: Maria lo consegna a Ortigia come primo Atto (le carte degli hangar di '
                 'Fontanarossa, M-CT-09); VAR_ST_02 +1 (ST-02, registro 2.4). Unico.')
    return (n, 'IT', 'm', 'Atti ' + p, None, None, nota, desc, altro)


def _faldone(n, p):
    nota = ('Nome italiano della trama (ST-07, «faldoni»), con la sigla della provincia: uno per Segreteria, come '
            'nel registro 2.4 (R-STR-18).')
    desc = ('Faldone dell’ARS coi registri delle quote Pokémon, nascosto in provincia di %s.'
            % PROVINCE[p])
    altro = ('Nascosto in %s: si raccoglie solo con FLAG_C_06 (FLAG_ST_07_FALDONE_%s, VAR_ST_07 +1; ST-07, '
             'registro 2.4). Unico.' % (FALDONE_MAPPA[p], p))
    return (n, 'IT', 'm', 'Faldoni ' + p, None, None, nota, desc, altro)


STRUMENTI = [
 # --- Atti, Amuleto e strumenti chiave di Sinnoh 429-467 ----------------------------------------------
 _atto(429, 'CT'), _atto(430, 'SR'),
 (431, 'Circaturi', 'm', None, 'circari', 'cercatore', 'Slot del Poké Radar di Sinnoh, che HeartGold non dà.',
  'Apparecchio che scova i Pokémon nascosti nell’erba alta. La batteria si ricarica camminando.',
  _NO + 'come in HeartGold.'),
 (432, 'Libbrettu', 'm', None, None, 'libretto', None,
  'Libretto dove si segnano i Punti Lotta guadagnati.',
  _NO + 'come in HeartGold; i Punti Lotta della Fiera del Mediterraneo (P-09) si vedono sulla Scheda Allenatore.'),
 (433, 'Diariu', 'm', None, None, 'diario', None,
  'Quaderno che tiene il diario del viaggio, giorno per giorno.', _NO + 'come in HeartGold.'),
 (434, 'ScatulaBolli', 'f', None, None, 'scatola dei bolli', '«scàtula», scatola; l’accento interno si omette (R-GRA-03).',
  'Scatola per i bolli da attaccare alle capsule delle Poké Ball.',
  _NO + 'la trama non dà bolli né capsule.'),
 (435, 'Cufittedda', 'f', None, 'cufittedda', 'cestino di vimini', None,
  'Cestino di vimini dove si tengono in ordine gli accessori dei Pokémon.',
  _NO + 'in Trinacria non ci sono gare di bellezza.'),
 _atto(436, 'RG'),
 (437, 'Taccuinu', 'm', None, None, 'taccuino', None,
  'Taccuino per segnare gli amici, i loro Codici Amico e le partite giocate insieme.',
  'Si riceve al banco delle connessioni del Centro Pokémon di Catania (MAP_CT_CATANIA_CENTRO_POKEMON), alla prima '
  'visita.'),
 _atto(438, 'CL'),
 (439, 'IT', 'm', 'Amuleto', None, None,
  'Nome italiano della trama (ST-12, «Amuleto»). Sta sullo slot dell’Old Charm, l’antico portafortuna di Sinnoh '
  '(R-STR-18).',
  'Amuleto del Prof. Strano per chi ha completato il Pokédex regionale. Non ha effetto: porta fortuna.',
  'Premio di ST-12: lo consegna il Prof. Strano al Vermut (MAP_CT_CATANIA_VERMUT) col Pokédex regionale completo '
  '(FLAG_ST_12_AMULETO_CONSEGNATO). Unico.'),
 _atto(440, 'AG'), _atto(441, 'TP'),
 (442, 'Cartina', 'f', None, None, 'cartina', None,
  'Cartina dell’isola da guardare quando si vuole. Mostra anche dove ci si trova.',
  _NO + 'la mappa della Sicilia sta nel Pokégear (R-09.6 della trama).'),
 (443, 'Sfidaturi', 'm', None, None, 'sfidante', None,
  'Apparecchio che indica gli Allenatori che vogliono lottare di nuovo. Si ricarica camminando.',
  _NO + 'come in HeartGold.'),
 (444, 'Caruseddu', 'm', None, 'caruseddu', 'salvadanaio di terracotta', None,
  'Salvadanaio di terracotta per i gettoni delle sale giochi. Ne tiene fino a 50.000.',
  _NO + 'in Trinacria non ci sono sale giochi (MAP_GOLDENROD_GAME_CORNER è diventato MAP_CT_MISTERBIANCO_CUBBAR, '
  'registro 2.1).'),
 (445, 'Cannuzza', 'f', None, None, 'piccola canna',
  'Diminutivo di «canna»: la Canna Vecchia della trama (R-10.7). Famiglia «Canna-» per le canne (R-STR-19), '
  'deviazione D-21.',
  'Canna da pesca vecchia e tutta rattoppata.' + _PESCA,
  'Premio di S-CT-04 (il pescatore anziano di Aci Trezza, la lotta in barca tra i Faraglioni).'),
 (446, 'CannaBona', 'f', None, None, 'canna buona', 'La Canna Buona della trama (R-10.7), deviazione D-21.',
  'Canna da pesca nuova e di buona qualità.' + _PESCA,
  'Premio di M-SR-03: il vecchio rais della tonnara di Marzamemi.'),
 (447, 'Cannazza', 'f', None, None, 'canna grande',
  'Accrescitivo di «canna»: la Super Canna della trama (R-10.7), deviazione D-21.',
  'Canna da pesca grande e robusta, da armatore.' + _PESCA,
  'Premio di M-TP-03: l’armatore del porto di Mazara del Vallo.'),
 (448, 'Vagnaturi', 'm', None, 'vagnari', 'annaffiatoio', None,
  'Annaffiatoio a forma di [SP:PSYDUCK]. Fa crescere bene le Bacche piantate.',
  _NO + 'le Bacche nei vasi si annaffiano con lo Sbrizzaturi (n. 477).'),
 (449, 'ScatulaDuci', 'f', None, None, 'scatola dei dolci', None,
  'Scatola per i dolcetti cotti con le Bacche.', _NO + 'come in HeartGold.'),
 (450, 'G30', None, None, None, None, None,
  'Scooter SH tutto scassato, regalo di Orazio. Con lui si va molto più veloci che a piedi.',
  'Premio di M-CT-03: Orazio lo consegna nell’officina di San Cristoforo (MAP_CT_CATANIA_OFFICINA) quando entra nel '
  'gruppo (FLAG_C_02). Unico.'),
 _atto(451, 'ME'), _atto(452, 'PA'),
 (453, 'PinnaLunari', 'f', None, 'luna', 'piuma lunare', '«pinna», penna; «lunari» come PetraLunari (n. 81).',
  'Piuma che brilla come la luna. Dicono che scacci gli incubi.',
  'Post-game: a terra accanto a Lunafauci, alle Isole Eolie (MAP_ME_ISOLE_EOLIE, piano 3.1).'),
 _atto(454, 'EN'),
 (455, 'ZufuluCelu', 'm', None, None, 'zufolo del cielo', 'Famiglia «Zufulu-» del 3.10 (gli zufoli).',
  'Zufolo dal suono che rimbomba e non sembra di questo mondo. Nessuno sa chi l’abbia fatto.',
  _NO + 'Patreternu è un mitico non ottenibile (piano 3.1).'),
 (456, 'Bigliettu', 'm', None, None, 'biglietto', None,
  'Biglietto del traghetto, con una nave disegnata sopra.',
  _NO + 'i traghetti della trama (Stretto, Eolie, Egadi, Pantelleria) sono scene e non chiedono biglietto.'),
 _faldone(457, 'CT'),
 (458, 'PetraLava', 'f', None, None, 'pietra di lava',
  'Non è una pietra dell’evoluzione: la famiglia «Petra-» copre anche le altre pietre (PetraFirma, n. 229).',
  'Pietra nata dalla lava fusa e indurita: dentro c’è ancora il magma.',
  'Post-game: a terra accanto a Firraru a Pantelleria (MAP_TP_PANTELLERIA, piano 3.1).'),
 _faldone(459, 'SR'), _faldone(460, 'RG'), _faldone(461, 'CL'), _faldone(462, 'AG'), _faldone(463, 'TP'),
 (464, 'Sciroppu', 'm', None, None, 'sciroppo', None,
  'Sciroppo miracoloso della farmacia. Guarisce un Pokémon da qualsiasi male.',
  _NO + 'la trama non ha il faro col Pokémon malato di HeartGold.'),
 (465, 'Rigistraturi', 'm', None, None, 'registratore', None,
  'Apparecchio che registra le lotte con gli amici o alla Fiera del Mediterraneo.',
  'Si riceve al primo ingresso nella Fiera del Mediterraneo (P-09, post-game).'),
 (466, 'CiuriGrazia', 'm', 'CiuriGrazia', None, 'fiore della grazia',
  '«ciuri», fiore (singolare e plurale); «Ciurita» è la specie n. {Ciurita}.',
  'Fiore che si mette nei mazzi per dire grazie, nei giorni di festa.',
  _NO + 'Ciurita è un mitico non ottenibile (piano 3.1).'),
 _faldone(467, 'ME'),
 # --- Strumenti chiave di HeartGold 468-484 ------------------------------------------------------------
 (468, 'Cascitta', 'f', None, None, 'cassetta', None,
  'Cassetta di legno dove si tengono fino a 99 Pirazzi di ogni colore.',
  'Regalo del maestro ceramista di Caltagirone alla fine di S-CT-07, insieme a un PirazzuRussu (R-STR-19). Unica.'),
 (469, 'Scartafazzu', 'm', None, None, 'scartafaccio', None,
  'Quaderno dove si segnano tutte le forme di [SP:UNOWN] trovate.',
  'Premio di S-RG-05: l’archeologo di Ispica lo dà quando compaiono i primi Littra (R-10.7 della trama). Unico.'),
 (470, 'Grasta', 'f', None, 'grasta', 'vaso di terracotta',
  'Le quattro «grasti» di HeartGold sono un solo strumento: il nome è al singolare come gli altri.',
  'Vasi di terracotta per coltivare le Bacche dovunque si vada.',
  'Regalo di un vivaista di CT prima del 1° Dossier, insieme allo Sbrizzaturi (n. 477); il Modulo 6 sceglie la '
  'mappa della provincia.'),
 (471, 'Ciauraturi', 'm', None, 'ciauru', 'fiutatore', 'Da «ciaurari», annusare: il «Pokégear» che fiuta i faldoni di ST-07.',
  'Apparecchio di Totò che fiuta gli strumenti nascosti: suona e si accende quando ne trova uno.',
  'Regalo di Totò alla prima telefonata (M-CT-09, quando si imposta FLAG_C_06): serve a fiutare i faldoni di ST-07 '
  'e gli strumenti nascosti.'),
 (472, 'CartuzzaBlu', 'f', None, None, 'cartoncino blu', None,
  'Cartoncino dove si raccolgono i punti di un programma della radio.',
  _NO + 'la trama non ha il programma radio della parola d’ordine di HeartGold.'),
 _faldone(473, 'PA'),
 (474, 'CampanaPura', 'f', None, None, 'campana pura', None,
  'Campana antica dal suono gentile e cristallino.',
  _NO + 'FeniceEtna compare senza campana (P-04 della trama).'),
 (475, 'ChiaviCarta', 'f', 'ChiaviCarta', None, 'chiave a scheda', '«chiavi», chiave (femminile, invariabile).',
  'Chiave a scheda che apre una saracinesca blindata.', _NO + 'come le altre chiavi delle missioni di HeartGold.'),
 (476, 'Chiavazza', 'f', None, None, 'chiave grande e vecchia', None,
  'Vecchia chiave che apre una porta dei sotterranei.', _NO + 'come le altre chiavi delle missioni di HeartGold.'),
 (477, 'Sbrizzaturi', 'm', None, 'sbrizziari', 'spruzzino', 'Da «sbrizziari», piovigginare.',
  'Spruzzino per annaffiare le Bacche piantate nei vasi.',
  'Regalo del vivaista di CT insieme alla Grasta (n. 470).'),
 (478, 'ScamaRussa', 'f', None, 'russu', 'scaglia rossa', 'Famiglia «Scama-» (ScamaDiCori, n. 93).',
  'Scaglia di un [SP:GYARADOS] rosso. Brilla come una fiamma.',
  _NO + 'la trama non ha il lago col Sirpintuni rosso di HeartGold.'),
 (479, 'PupazzuPersu', 'm', None, None, 'pupazzo perso', '«Pupazzu» è lo strumento n. 63 (Poké Doll); «Pupidda» è una specie.',
  'Il pupazzo di Pokémon che una ragazza ha perso in treno.', _NO + 'come le altre consegne di HeartGold.'),
 (480, 'Abbunamentu', 'm', None, None, 'abbonamento', None,
  'Abbonamento al treno: si sale quando si vuole e quanto si vuole.',
  _NO + 'il treno della trama (Circumetnea, S-CT-08) è una scena.'),
 (481, 'Ricambiu', 'm', None, None, 'pezzo di ricambio', None,
  'Pezzo di ricambio di una centrale elettrica, rubato da qualcuno.',
  _NO + 'i ricambi di P-10 li portano i Pokémon delle province, senza strumento.'),
 (482, 'PinnaJanca', 'f', None, 'jancu', 'piuma bianca', None,
  'Piuma argentata e lucente, caduta dal fondo dello Stretto.',
  'Post-game, dopo P-02: a terra accanto a Colapisci nell’abisso di Cariddi (MAP_ME_ABISSO_CARIDDI, P-08).'),
 (483, 'PinnaColuri', 'f', None, None, 'piuma dei colori', None,
  'Piuma coi sette colori dell’arcobaleno, caduta sul Cratere Centrale.',
  'Post-game, dopo il Fantasma di P-04: a terra accanto a FeniceEtna (MAP_CT_ETNA_CRATERE_CENTRALE).'),
 (484, 'OvuStranu', 'm', None, None, 'uovo strano', '«ovu», uovo, come PetraOvu (n. 110).',
  'Uovo misterioso: non si sa cosa contiene.',
  _NO + 'l’uovo di Strina di M-SR-04 si dà già come uovo (piano 3.1).'),
 # --- Pirazzi e Ball artigianali 485-500 (R-STR-19) -----------------------------------------------------
 (485, 'PirazzuRussu', 'm', None, 'russu', 'perastro rosso',
  '«pirazzu», perastro (pero selvatico), al posto delle Ghicocche; colori come Zufulu- e Cocciu- del 3.10.',
  _PIRAZZU % ('rosso', 'pungente', 'ScaluniBall'), _PIANTE.replace('%s e %s', '%s ed %s') % ('CT', 'EN')),
 (486, 'PirazzuGiarnu', 'm', None, 'ggiarnu', 'perastro giallo', None,
  _PIRAZZU % ('giallo', 'vivace', 'LunaBall'), _PIANTE % ('SR', 'AG')),
 (487, 'PirazzuBlu', 'm', None, None, 'perastro blu', None,
  _PIRAZZU % ('blu', 'd’erba', 'IscaBall'), _PIANTE % ('ME', 'TP')),
 (488, 'PirazzuVirdi', 'm', None, 'virdi', 'perastro verde', None,
  _PIRAZZU % ('verde', 'misterioso', 'CumpariBall'), _PIANTE % ('RG', 'PA')),
 (489, 'PirazzuRosa', 'm', None, None, 'perastro rosa', None,
  _PIRAZZU % ('rosa', 'dolce', 'ZitaBall'), _PIANTE % ('SR', 'ME')),
 (490, 'PirazzuJancu', 'm', None, 'jancu', 'perastro bianco', None,
  'Pirazzu bianco che non sa di niente. Il maestro ceramista di Caltagirone ci fa una CurriBall.',
  _PIANTE % ('TP', 'PA')),
 (491, 'PirazzuNiuru', 'm', None, 'niuru', 'perastro nero', None,
  _PIRAZZU % ('nero', 'indescrivibile', 'PisantiBall'), _PIANTE % ('CT', 'CL')),
 (492, 'CurriBall', 'f', None, 'curriri', 'ball della corsa', None,
  'Ball che rende più facile catturare i Pokémon veloci.', _BALL % 'PirazzuJancu'),
 (493, 'ScaluniBall', 'f', None, None, 'ball del gradino', '«scaluni», gradino.',
  'Ball per i Pokémon di livello più basso del proprio Pokémon.', _BALL % 'PirazzuRussu'),
 (494, 'IscaBall', 'f', None, None, 'ball dell’esca', '«isca», esca.',
  'Ball per i Pokémon presi all’amo con una canna.', _BALL % 'PirazzuBlu'),
 (495, 'PisantiBall', 'f', None, None, 'ball pesante', None,
  'Ball per catturare i Pokémon molto pesanti.', _BALL % 'PirazzuNiuru'),
 (496, 'ZitaBall', 'f', None, 'zita', 'ball della fidanzata', None,
  'Ball per i Pokémon di sesso opposto al proprio Pokémon.', _BALL % 'PirazzuRosa'),
 (497, 'CumpariBall', 'f', None, 'cumpari', 'ball del compare', None,
  'Ball che rende più affettuoso il Pokémon catturato.', _BALL % 'PirazzuVirdi'),
 (498, 'LunaBall', 'f', None, 'luna', 'ball della luna', None,
  'Ball per i Pokémon che si evolvono con la PetraLunari.', _BALL % 'PirazzuGiarnu'),
 (499, 'GaraBall', 'f', None, None, 'ball della gara', None,
  'Ball speciale della gara di cattura dei Pokémon Coleottero.',
  _NO + 'la trama non ha la Gara Coleotteri (MAP_NATIONAL_PARK è uno slot escluso, registro 2.1).'),
 (500, 'ParcuBall', 'f', None, None, 'ball del parco', None,
  'Ball speciale del Parco Amici.', _NO + 'la trama non ha il Parco Amici (MAP_PAL_PARK è uno slot escluso, registro 2.1).'),
 # --- Altri strumenti chiave di HeartGold 501-504 -------------------------------------------------------
 (501, 'LibbruFoto', 'm', 'LibbruFoto', None, 'album delle foto', '«libbru», libro.',
  'Album dove si tengono le foto scattate durante il viaggio.', _NO + 'come le altre fotografie di HeartGold.'),
 (502, 'Sunaturi', 'm', None, None, 'suonatore', 'Da «sunari», suonare.',
  'Lettore musicale per ascoltare vecchie canzoni. Si usa con un solo pulsante.',
  _NO + 'le musiche del Modulo 5 non hanno i brani di questo lettore.'),
 (503, 'CampanaMari', 'f', None, 'mari', 'campana del mare', None,
  'Campana antica dal suono gentile e calmo come il mare.',
  _NO + 'Colapisci compare senza campana (P-08 della trama).'),
 (504, 'G30', None, None, None, None, None,
  'Cioccolato di Modica lavorato a freddo. I turisti lo comprano da portare a casa.',
  '5 dalla cioccolataia di Modica Alta (S-RG-02). È uno strumento chiave senza effetto, come in HeartGold.'),
 # --- Schede delle gare 505-531 (Pokéathlon) -------------------------------------------------------------
] + [(505 + i, 'Cartedda%02d' % (i + 1), 'f', None, None, 'cartoncino %02d' % (i + 1),
      'Le 27 schede del Pokéathlon: «cartedda», cartoncino, col numero della scheda di HeartGold.' if i == 0 else None,
      _SCHEDA % t, _POKEATHLON) for i, t in enumerate([
    'le vittorie', 'le sconfitte', 'gli scatti dei Pokémon', 'i salti dei Pokémon',
    'le vittorie nella corsa a ostacoli', 'le vittorie nella staffetta', 'le vittorie nella cattura delle bandiere',
    'le vittorie nello sfondamento dei blocchi', 'le vittorie nella presa del disco',
    'le vittorie nel lancio delle palle di neve', 'i punti dei Pokémon', 'gli errori dei Pokémon',
    'le volte che i Pokémon si sono intralciati', 'le spinte dei Pokémon', 'le cadute dei Pokémon',
    'le vittorie nel lancio degli anelli', 'le vittorie nel salto delle lampade', 'le vittorie nella spinta nel cerchio',
    'le vittorie in collegamento', 'le sconfitte in collegamento', 'le gare vinte', 'le gare perse',
    'i cambi di Pokémon', 'le vittorie nel tiro in porta', 'i premi dei singoli Pokémon', 'gli ordini dati ai Pokémon',
    'il tempo passato alle gare'])] + [
 # --- Sfere e pietre dei leggendari di Hoenn 532-536 ----------------------------------------------------
 (532, 'SferaVirdi', 'f', None, 'virdi', 'sfera verde', 'Famiglia «Sfera-» del 3.10 (le sfere dei leggendari).',
  'Sfera verde e lucente legata a [SP:RAYQUAZA], il signore del cielo.',
  'Post-game, dopo P-03: a terra accanto a Celuautu sulla vetta di Rocca Busambra (MAP_PA_ROCCA_BUSAMBRA_VETTA, '
  'piano 3.1).'),
 _faldone(533, 'EN'),
 (534, 'SferaRussa', 'f', None, 'russu', 'sfera rossa', None,
  'Sfera rossa e lucente legata a [SP:GROUDON], il signore della terra.',
  'Post-game: a terra accanto a Terramotu nelle Stufe del Monte Kronio (MAP_AG_SCIACCA_STUFE_KRONIO, piano 3.1).'),
 (535, 'SferaBlu', 'f', None, None, 'sfera blu', None,
  'Sfera blu e lucente legata a [SP:KYOGRE], il signore del mare.',
  'Post-game: a terra accanto a Diluviu a Lampedusa (MAP_AG_LAMPEDUSA, piano 3.1).'),
 (536, 'PetraArcana', 'f', None, None, 'pietra misteriosa', None,
  'Sfera di cristallo scavata dalla terra, bellissima e coperta di pezzetti di roccia.',
  'Post-game: a terra accanto a Favugnu a Favignana (MAP_TP_FAVIGNANA, piano 3.1).'),
]

# Come si ottengono le MT 34-92 e le MN 01-08 (per numero di strumento). Le MT 38, 41, 52, 54, 55, 70, 72, 76, 78,
# 79, 83 e 87 si comprano alla Fiera del Mediterraneo (banconi 7 e 20, piano del 3.10): niente altro.
# Le MN si ricevono col Dossier che ne sblocca l'uso fuori dalla lotta (R-03 della trama, R-STR-16).
MT_ALTRO = {
    361: _TERRA % ('SR', 'SR'), 362: '1 a terra alla Sciara del Fuoco (MAP_ME_STROMBOLI_SCIARA_DEL_FUOCO, FLAG_TR_ITEM_ME_*).',
    363: _TERRA % ('CL', 'CL'), 364: _NASC % ('CT', 'CT') + ' Sull’Etna.', 365: None,
    366: _TERRA % ('RG', 'RG'), 367: _TERRA % ('TP', 'TP'), 368: None, 369: _TERRA % ('CT', 'CT'),
    370: _NASC % ('SR', 'SR'), 371: _TERRA % ('RG', 'RG'), 372: _TERRA % ('SR', 'SR'), 373: _TERRA % ('CT', 'CT'),
    374: _TERRA % ('TP', 'TP'), 375: _NASC % ('ME', 'ME'), 376: _NASC % ('PA', 'PA'),
    377: 'Post-game: 1 a terra sul Cratere Centrale (MAP_CT_ETNA_CRATERE_CENTRALE, FLAG_TR_ITEM_CT_*).',
    378: _TERRA % ('AG', 'AG'), 379: None, 380: _TERRA % ('EN', 'EN'), 381: None, 382: None,
    383: _TERRA % ('PA', 'PA'), 384: _NASC % ('CL', 'CL'), 385: _NASC % ('RG', 'RG'), 386: _NASC % ('PA', 'PA'),
    387: _NASC % ('AG', 'AG'), 388: _TERRA % ('CL', 'CL'), 389: _TERRA % ('EN', 'EN'), 390: _TERRA % ('PA', 'PA'),
    391: _PG_NASC % ('CL', 'CL'), 392: _NASC % ('TP', 'TP'),
    393: _TERRA % ('ME', 'ME'), 394: _TERRA % ('PA', 'PA'),
    395: _PG_TERRA % ('EN', 'EN'), 396: _TERRA % ('AG', 'AG'), 397: None,
    398: _NASC % ('EN', 'EN'), 399: None, 400: _TERRA % ('SR', 'SR'), 401: _TERRA % ('TP', 'TP'),
    402: _TERRA % ('ME', 'ME'), 403: None, 404: _TERRA % ('RG', 'RG'), 405: None, 406: None,
    407: _TERRA % ('AG', 'AG'), 408: _NASC % ('ME', 'ME'), 409: _NASC % ('TP', 'TP'), 410: None,
    411: _TERRA % ('CL', 'CL'), 412: _NASC % ('EN', 'EN'), 413: _TERRA % ('RG', 'RG'), 414: None,
    415: _TERRA % ('CT', 'CT'), 416: _NASC % ('SR', 'SR'), 417: _TERRA % ('PA', 'PA'), 418: _TERRA % ('ME', 'ME'),
    419: _PG_NASC % ('PA', 'PA'),
    420: 'Si riceve col Dossier Aretusa (Segreteria 2, Siracusa); si usa fuori dalla lotta da quel Dossier (R-03).',
    421: 'Si riceve col Dossier Telamuni (Segreteria 5, Agrigento); si usa fuori dalla lotta da quel Dossier (R-03).',
    422: 'Si riceve col Dossier Pirrera (Segreteria 4, Caltanissetta); si usa fuori dalla lotta da quel Dossier (R-03).',
    423: 'Si riceve col Dossier Carrubba (Segreteria 3, Ragusa Ibla); si usa fuori dalla lotta da quel Dossier (R-03).',
    424: 'Si riceve col Dossier Pilunu (Segreteria 7, Messina); si usa fuori dalla lotta da quel Dossier (R-03).',
    425: 'Si riceve col Dossier Liotru (Segreteria 1, Catania); si usa fuori dalla lotta da quel Dossier (R-03).',
    426: 'Si riceve col Dossier Geniu (Segreteria 8, Palermo); si usa fuori dalla lotta da quel Dossier (R-03).',
    427: 'Si riceve col Dossier Cerere (Segreteria 9, Enna Alta); si usa fuori dalla lotta da quel Dossier (R-03).',
}

DEVIAZIONI = [
    {'id': 'D-21', 'oggetto': 'Cannuzza (n. 445), CannaBona (n. 446) e Cannazza (n. 447)',
     'forma_specifica': 'Canna Vecchia, Canna Buona, Super Canna (trama R-10.7, S-CT-04, M-SR-03, M-TP-03)',
     'forma_bloccata': 'Cannuzza, CannaBona, Cannazza',
     'motivo': 'La trama descrive le tre canne in italiano, senza dare un nome (R-STR-01: ogni strumento ha un nome '
               'siciliano). «una CannaVecchia» misura 91 px > 90 (L-04): la famiglia «Canna-» usa il diminutivo, '
               '«bona» e l’accrescitivo. Nei dialoghi del Modulo 6 si usano i nomi bloccati.'},
    {'id': 'D-22', 'oggetto': 'MN05 (n. 424) e MN06 (n. 425)',
     'forma_specifica': 'MN 5 Spaccaroccia/Martiddata e MN 6 Mulinello/Garòfalu (note del Glossario 3.0 v1.1, '
                        'trama v1.5)',
     'forma_bloccata': 'MN05 = Garòfalu (MOVE_WHIRLPOOL), MN06 = Martiddata (MOVE_ROCK_SMASH)',
     'motivo': 'In HeartGold ITEM_HM05 insegna Whirlpool e ITEM_HM06 Rock Smash (sTMHMMoves in src/item.c): il '
               'Modulo 3 non cambia la mossa delle MT e delle MN (R-STR-11). Il Glossario 3.0 v1.2 corregge le due '
               'note.'},
]

"""Blocco 4.6 — chi va in quale immagine di lotta e in quale ritratto, con quale posa ed espressione.

Le schede (aspetto e colori) sono quelle del 4.5 (tools/grafica/4.5/schede45.py): qui si dice solo quale scheda
va in quale voce. Le classi da ridisegnare e la scheda di ognuna vengono dal registro 2.5
(note_grafica.classi_con_immagine_nuova, classi_allenatore.elenco[].sprite_classe); i dorsi dei compagni da
note_grafica.dorsi; le transizioni dalle tabelle di asm/overlay_115.s e asm/overlay_117.s (lette da
costruisci46.py)."""
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(QUI, '..', '4.5'))
import schede45 as S45      # noqa: E402

SCHEDE = dict(S45.PERSONAGGI)
SCHEDE.update(S45.CLASSI)
SCHEDE['PROTAGONISTA_RAGAZZO'] = S45.PROTAGONISTA['ragazzo']
SCHEDE['PROTAGONISTA_RAGAZZA'] = S45.PROTAGONISTA['ragazza']

# fronti del protagonista (classi 0 e 1: lotte in collegamento, Fiera, Albo d'Oro)
FRONTI_PROTAGONISTA = {0: 'PROTAGONISTA_RAGAZZO', 1: 'PROTAGONISTA_RAGAZZA'}

# dorsi del protagonista (TRAINER_BACKPIC_*: 0 e 1 in lotta, 15 e 16 nelle lotte in collegamento)
DORSI_PROTAGONISTA = {0: ('PROTAGONISTA_RAGAZZO', 'TRAINER_BACKPIC_ETHAN'),
                      1: ('PROTAGONISTA_RAGAZZA', 'TRAINER_BACKPIC_LYRA'),
                      15: ('PROTAGONISTA_RAGAZZO', 'TRAINER_BACKPIC_ETHAN_2'),
                      16: ('PROTAGONISTA_RAGAZZA', 'TRAINER_BACKPIC_LYRA_2')}

# ritratti del protagonista nelle transizioni dei Campioni dell'ARS e del Presidente: asm/overlay_115.s
# (ov115_0225F978) carica gli sprite 0xD0/0xD1/0xD2 e 0xD4/0xD5/0xD6 con la palette 0xD3 (una sola per tutti e due)
RITRATTI_PROTAGONISTA = [(208, 209, 'PROTAGONISTA_RAGAZZO'), (212, 213, 'PROTAGONISTA_RAGAZZA')]
PALETTE_RITRATTI_PROTAGONISTA = 211

# espressione del viso per categoria del registro 2.5
ESPRESSIONE = {'PROTAGONISTA': 'sorriso', 'COMPAGNO': 'sorriso', 'POSTGAME': 'serio', 'LEGA': 'ghigno',
               'SEGRETERIA': 'ghigno', 'U_SISTEMA': 'ghigno', 'SICILIANA': 'ghigno'}
ESPRESSIONE_CLASSE = {'TRAINERCLASS_MAGISTRATA': 'severo'}

# oggetto in mano nel fotogramma 0 (il primo accessorio della lista che la scheda ha): braccio e posa
OGGETTI = [('tablet', 'LR', 'tablet'), ('cartellina', 'L', 'cartellina'), ('valigetta', 'L', 'valigetta'),
           ('telefono', 'R', 'telefono'), ('buste', 'R', 'buste'), ('bastone', 'R', 'bastone')]


def posa_base(s):
    for nome, braccia, posa in OGGETTI:
        if nome in s.get('accessori', ()):
            if braccia == 'LR':
                return dict(L=posa, R=posa)
            return dict(L=posa, R='giu') if braccia == 'L' else dict(L='giu', R=posa)
    return dict(L='giu', R='giu')


def pose_fronte(s, n, espr):
    """Pose dei fotogrammi di un'immagine frontale con n fotogrammi (1, 3 o 8 nelle classi di Trinacria).
    3 = sequenza d'ingresso (fermo, indica, pugno o mano al fianco); 8 = lancio della Poké Ball."""
    b = posa_base(s)
    b['espr'] = espr
    if n == 1:
        return [b]
    if n == 3:
        if b['L'] == 'giu' and b['R'] == 'giu':
            g1, g2 = dict(L='indica', R='fianchi'), dict(L='fianchi', R='pugno')
        elif b['L'] == 'tablet':
            g1, g2 = dict(L='indica', R='giu'), dict(L='fianchi', R='pugno')
        elif b['L'] == 'giu':
            g1, g2 = dict(b, L='indica'), dict(b, L='fianchi')
        else:
            g1, g2 = dict(b, R='pugno'), dict(b, R='fianchi')
        return [b, dict(g1, espr=espr), dict(g2, espr=espr)]
    if n == 8:
        L = b['L'] if b['L'] not in ('tablet',) else 'giu'
        return [dict(L=L, R='lancio', fase=k, espr=espr) for k in range(8)]
    raise ValueError('fotogrammi: %d' % n)


def fasi_retro(n):
    """Fasi del lancio (figura46.RETRO_FASI) per un dorso di n fotogrammi: 8 = tutte, 5 = fino al rilascio."""
    if n == 8:
        return list(range(8))
    if n == 5:
        return [0, 1, 2, 3, 4]
    raise ValueError('fotogrammi del dorso: %d' % n)


DESCRIZIONE_POSE = [
    ('fermo', 'in piedi, braccia lungo i fianchi, o con l’oggetto della scheda: valigetta, cartellina, tablet, telefono all’orecchio, buste, bastone'),
    ('indica', 'braccio teso verso sinistra, verso il giocatore, con l’indice'),
    ('fianchi', 'mano sul fianco'),
    ('pugno', 'pugno alzato accanto alla testa'),
    ('lancio 0–7', 'lancio della Poké Ball di fronte (solo la classe di Calogero, 8 fotogrammi come l’originale): palla in mano, carica, braccio alto, sopra la testa, rilascio, accompagnamento, chiusura'),
]

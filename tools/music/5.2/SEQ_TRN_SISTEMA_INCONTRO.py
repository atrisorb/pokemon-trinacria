"""«U Sistema»: tema d'incontro (classi U_SISTEMA, Parcheggiaturi e Assessuri; R-10.6, modifiche E1/E2)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_SISTEMA_INCONTRO'
BANCO = 'BANK_BASIC'
VOLUME = 71
SCHEDA = {
    'titolo': '«U Sistema» — incontro',
    'carattere': 'lo scagnozzo che ti guarda storto: ottoni all\'unisono che camminano con aria da '
                 'padroni, cromatismi in giù, basso sintetico; l\'accordo di Re bemolle (napoletano) '
                 'è la firma armonica dei tre temi di «U Sistema»',
    'tonalita': 'Do minore',
    'forma': 'introduzione di 1 battuta (due colpi di ottoni); ritornello di 8 battute',
}

GIRO = Giro('Cm | Cm | Ab7 | G7 | Cm | Cm | Db | G7')

MELODIA = (
    '| c5/8 r c5 eb5 g5/4 f#5/8 g5 | g5/8 ab5 g5 f5 eb5/4 c5 | eb5/4. db5/8 c5/4 ab4 | b4/4 d5 f5 g5 '
    '| c6/8 r c6 bb5 g5/4 eb5 | eb5/8 d5 c5 d5 g4/2 | ab4/4 db5 f5 ab5 | g5/4 f5 d5 b4 |'
)


def partitura(A):
    b = Brano(A, bpm=152)
    ot = b.voce('ottoni', 29, volume=112, pan=60)
    ob = b.voce('ottoni bassi', 30, volume=96, pan=40)
    pz = b.voce('pizzicato', 17, volume=88, pan=96)
    bs = b.voce('basso', 21, volume=110, pan=64)
    bt = b.voce('batteria', 39, volume=96, pan=64)
    ob.suona('| c4+eb4+g4/8> r/8 r/4 r/4 g3+b3+d4+f4/4> |', da=0, vel=104)
    ot.suona(MELODIA, da=1, vel=100)
    b.eco(ot, 'ottoni ottava', ritardo=0, volume=70, pan=90, trasponi=-12, programma=30)
    pz.accordi(GIRO, '.x.x.x.x', da=1, registro=(55, 67), vel=70, gate=0.4)
    bs.basso(GIRO, '1 . 8 . 1 5 8 .', da=1)
    bt.batteria({'cassa': 'x..x..x.', 'rullante': '..x...x.', 'hh': 'xoxoxoxo'}, da=1, battute=8)
    b.ritornello(1, 9)
    return b.fine()

"""La dissolvenza e i titoli di coda (M-EN-08): pianoforte solo, poi violino in Do minore. Lo slot
HeartGold (SEQ_GS_ENDING) non si ripete e dura quanto i titoli di coda: il brano finisce (A10)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notazione import Brano, Giro  # noqa: E402

SIMBOLO = 'SEQ_TRN_DIMISSIONI'
BANCO = 'BANK_BGM_OPEND'
VOLUME = 64
SCHEDA = {
    'titolo': 'Le dimissioni',
    'carattere': 'la fanfara del palco si è spenta: pianoforte solo, un tema lento in Do minore che '
                 'scende per terze, lungo abbastanza per le cinque frasi sul nero dei sei mesi a Palazzo '
                 'd\'Orléans; poi entra il violino, struggente, sopra gli arpeggi del pianoforte e il '
                 'violoncello; nella parte centrale il tema si apre in La bemolle e Mi bemolle con gli '
                 'archi, come l\'ultima speranza, e torna in Do minore per finire su un accordo tenuto',
    'tonalita': 'Do minore',
    'forma': 'pianoforte solo 12 battute (tema di 8 + 4 di passaggio); violino col tema (8) e la sua '
             'variante (8); parte centrale di 12 battute in La bemolle e Mi bemolle; ritorno del tema '
             '(8) con l\'accordo finale tenuto; nessun ritornello',
    'perche_volume': 'HeartGold suona lo slot a 59 con 11 tracce; le 5 voci di questa partitura a 59 '
                     'resterebbero sotto la fanfara del palco che la precede (99)',
}

TEMA = Giro('Cm | Ab | Fm | G | Cm | Ab | Dm7b5 G | Cm')
PASSAGGIO = Giro('Ab | Fm | Dm7b5 | G')
VARIANTE = Giro('Cm | Eb | Ab | G | Fm | Cm | Dm7b5 G | Cm')
CENTRO = Giro('Ab | Eb | Fm | Cm | Ab | Eb | Db | G | Ab | Bb | Eb | G')
RITORNO = Giro('Cm | Ab | Fm | G | Cm | Ab | Dm7b5 G')          # l'ultima battuta è l'accordo tenuto

T_TEMA = ('| g5/2 eb5/4 c5 | c6/2. ab5/4 | f5/4. g5/8 ab5/4 c6 | b5/2 d5/2 '
          '| eb5/4. f5/8 g5/4 c6 | eb6/2 c6/4 ab5 | ab5/4 f5 g5 b4 |')
T_PASSAGGIO = '| c5/4 eb5 ab5 c6 | ab5/2 f5/4 c5 | d5/4 f5 ab5 c6 | b5/2. r/4 |'
T_VARIANTE = ('| c6/2 g5/4 eb5 | g5/4. ab5/8 bb5/4 eb6 | eb6/2 c6/4 ab5 | b5/2 d6/4 g6 '
              '| ab6/4. g6/8 f6/4 c6 | eb6/2 c6/4 g5 | ab5/4 c6 b5 d6 | c6/1 |')
T_CENTRO = ('| c6/2 eb6/4 ab6 | g6/2. eb6/4 | f6/4. eb6/8 c6/4 ab5 | g5/2 c6/4 eb6 '
            '| ab6/2 c7/4 ab6 | g6/4. f6/8 eb6/4 bb5 | ab5/4 db6 f6 ab6 | g6/2 d6/4 b5 '
            '| c6/4 eb6 ab6 c7 | d7/2 bb6/4 f6 | eb6/2. g5/4 | g5/2 b5/4 d6 |')


def partitura(A):
    b = Brano(A, bpm=66)
    pf = b.voce('pianoforte', 0, volume=100, pan=56)
    ps = b.voce('pianoforte sinistra', 0, volume=84, pan=48)
    vl = b.voce('violino', 24, volume=112, pan=72)
    vc = b.voce('violoncello', 25, volume=90, pan=40)
    ar = b.voce('archi', 23, volume=60, pan=96)
    # 0-11: pianoforte solo
    pf.suona(T_TEMA + ' c5/1 |', da=0, vel=82).suona(T_PASSAGGIO, da=8, vel=78)
    # 12-27: entra il violino; 28-39: parte centrale; 40-47: ritorno e accordo finale
    vl.suona(T_TEMA + ' c5/1 |', da=12, vel=88).suona(T_VARIANTE, da=20, vel=94)
    vl.suona(T_CENTRO, da=28, vel=102).suona(T_TEMA + ' c5/1_ |', da=40, vel=86)
    giro = TEMA + PASSAGGIO + TEMA + VARIANTE + CENTRO + RITORNO
    ps.arpeggi(giro, '1 5 8 10 12 10 8 5', da=0, registro=(36, 60), vel=64)
    ps.suona('| c3+g3+c4+eb4/1_ |', da=47, vel=70)
    vc.basso(TEMA + VARIANTE + CENTRO + RITORNO, '1 - - - - - - -', da=12, registro=(31, 50), gate=0.95)
    vc.suona('| c2/1_ |', da=47, vel=90)
    ar.accordi(CENTRO, 'x-------', da=28, registro=(55, 70), vel=58)
    b.fine_a(48)
    return b.fine()

"""Texture nuove del blocco 4.3 (R-GFX-17): province di Agrigento, Trapani, Palermo, Enna e Messina.

Si registrano nel catalogo di tex42.py, che resta l'unica fonte delle 69 texture del 4.2: il tileset
condiviso della matrice 0 (R-GFX-18) si ricostruisce con SICILIA_4_2 + SICILIA_4_3, stessi nomi e
stesso disegno per le texture del 4.2. Stesse regole: al massimo 16 colori della scala 555, indice 0
trasparente nelle sagome, disegno che dipende solo dal nome.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '4.2'))
from tex42 import (Tex, tex, hexc, mix, lastre, rumore, pietre, onde, chioma, palo, scatola, facciata,  # noqa: E402
                   LAVA, CALCARE, ERBA, MARE, TERRA, COTTO, FOGLIA, LEGNO, METALLO, SICILIA_4_2)

TUFO = [hexc('9a7a46'), hexc('b8955a'), hexc('cca86a'), hexc('dcbc80'), hexc('ecd49c')]
MARNA = [hexc('a8a49c'), hexc('c8c4bc'), hexc('dedad2'), hexc('eeebe4'), hexc('fafaf6')]


# ---- terreni ------------------------------------------------------------------------------


@tex('tufo', 32, 32)
def _tufo(n, w, h, s):
    # calcarenite gialla delle cave (Cusa, Favignana) e delle mura di Trapani e Marsala
    t = Tex(n, w, h, TUFO + [hexc('7a5c34')])
    t.fill(2)
    lastre(t, 16, 16, 0, sfalsa=True, vari=(1, 2, 3, 2))
    t.speckle([1, 3, 4, 5], 0.14)
    return t


@tex('marna', 32, 32)
def _marna(n, w, h, s):
    # la marna bianca della Scala dei Turchi: strati orizzontali ondulati
    t = Tex(n, w, h, MARNA + [hexc('8a8478')])
    t.fill(3)
    for y0 in range(0, 32, 6):
        for x in range(32):
            y = y0 + (1 if (x // 5) % 2 else 0)
            t.put(x, y, 1)
            t.put(x, y + 1, 2)
    t.speckle([4, 5], 0.06)
    return t


@tex('salina', 32, 32)
def _salina(n, w, h, s):
    # vasche delle saline di Trapani e dello Stagnone: acqua bassa rosata, argini di terra
    t = Tex(n, w, h, [hexc('c89a9a'), hexc('dcb4b0'), hexc('ecd0cc'), hexc('f8ecea'), TERRA[1], TERRA[2]])
    t.fill(1)
    t.speckle([0, 2, 3], 0.12)
    t.rect(0, 0, 32, 2, 4)
    t.rect(0, 0, 2, 32, 4)
    t.hline(0, 2, 32, 5)
    t.vline(2, 0, 32, 5)
    return t


@tex('cordolo', 32, 32)
def _cordolo(n, w, h, s):
    # pista dell'autodromo di Pergusa: asfalto con il cordolo bianco e rosso sul bordo nord
    t = Tex(n, w, h, [hexc('2e2e32'), hexc('3c3c40'), hexc('4c4c50'), hexc('f0f0ec'), hexc('c83228')])
    t.fill(1)
    t.speckle([0, 2], 0.2)
    for x in range(0, 32, 8):
        t.rect(x, 0, 4, 3, 3)
        t.rect(x + 4, 0, 4, 3, 4)
    return t


# ---- muri, facciate, tetti ------------------------------------------------------------------


@tex('fac_tufo', 32, 32)
def _fac_tufo(n, w, h, s):
    # case di tufo di Trapani, Marsala, Mazara e delle Egadi, persiane verdi
    t = facciata(n, w, h, [TUFO[1], TUFO[2], TUFO[3]], TUFO[4], hexc('2a3a4a'), hexc('3a6a4a'), zoccolo=TUFO[0])
    t.speckle([0], 0.05)
    return t


@tex('fac_liberty', 32, 32)
def _fac_liberty(n, w, h, s):
    # il liberty palermitano (via Libertà, Politeama): intonaco ocra, lesene e balconi in ferro
    t = facciata(n, w, h, [hexc('c8a070'), hexc('dab27e'), hexc('e8c890')], hexc('f4e8cc'),
                 hexc('2c3a4a'), hexc('4a3a2a'), balcone=hexc('1e2a24'))
    t.rect(0, 2, 3, 30, 3)
    t.rect(29, 2, 3, 30, 3)
    for x in (13, 18):
        t.put(x, 4, 3)
        t.put(x, 5, 3)
    return t


@tex('fac_normanna', 32, 32)
def _fac_normanna(n, w, h, s):
    # pietra dorata arabo-normanna (Palazzo dei Normanni, Monreale, Cefalù): archi ciechi intrecciati
    t = Tex(n, w, h, [hexc('8a6a3a'), hexc('a8844a'), hexc('c4a060'), hexc('d8b878'), hexc('3a2a1a'),
                      hexc('6a4a2a')])
    t.fill(2)
    t.speckle([1, 3], 0.12)
    for y in range(0, 32, 8):
        t.hline(0, y, 32, 5)
    for x0 in (2, 18):
        t.rect(x0 + 2, 10, 8, 18, 4)
        t.disc(x0 + 6, 10, 4, 4, wrap=False)
        t.disc(x0 + 6, 10, 6, 3, wrap=False, ry=6)
        t.disc(x0 + 6, 10, 4, 4, wrap=False)
        t.rect(x0 + 2, 10, 8, 18, 4)
    t.rect(0, 29, 32, 3, 1)
    return t


@tex('trabeazione', 32, 32)
def _trabeazione(n, w, h, s):
    # trabeazione dei templi dorici: architrave, triglifi e metope (Agrigento, Selinunte)
    t = Tex(n, w, h, TUFO + [hexc('6a5030')])
    t.fill(2)
    t.rect(0, 0, 32, 4, 4)
    t.hline(0, 4, 32, 5)
    t.rect(0, 5, 32, 12, 3)
    for x in range(0, 32, 8):
        t.rect(x, 6, 3, 10, 1)
        t.vline(x + 1, 6, 10, 5)
    t.hline(0, 17, 32, 5)
    t.rect(0, 18, 32, 14, 2)
    t.speckle([0, 1], 0.1, (0, 18, 32, 14))
    return t


@tex('cupola_rossa', 32, 32)
def _cupola_rossa(n, w, h, s):
    # le cupole rosse di San Giovanni degli Eremiti e di San Cataldo: intonaco rosso a bande
    t = Tex(n, w, h, [hexc('8a2a1e'), hexc('a83a28'), hexc('c44c32'), hexc('d86a4a'), hexc('5a1a12')])
    t.fill(2)
    for y in range(0, 32, 4):
        t.hline(0, y, 32, 1)
    t.speckle([0, 3], 0.08)
    for x in range(0, 32, 16):
        t.vline(x, 0, 32, 4)
    return t


@tex('maiolica', 32, 32)
def _maiolica(n, w, h, s):
    # maioliche della Kasbah di Mazara e delle panchine di Monreale: stelle blu e gialle
    t = Tex(n, w, h, [hexc('f4f0e4'), hexc('2a5ca8'), hexc('5a8ad0'), hexc('e8c040'), hexc('3a8a5a'),
                      hexc('8a8478')])
    t.fill(0)
    for y0 in range(0, 32, 8):
        for x0 in range(0, 32, 8):
            t.frame(x0, y0, 8, 8, 5)
            t.disc(x0 + 4, y0 + 4, 2.5, 1, wrap=True)
            t.put(x0 + 4, y0 + 4, 3)
            for dx, dy in ((1, 1), (6, 1), (1, 6), (6, 6)):
                t.put(x0 + dx, y0 + dy, 2 if (x0 + y0) % 16 else 4)
    return t


@tex('tubo', 32, 16)
def _tubo(n, w, h, s):
    # la condotta dell'acquedotto, rattoppata e gocciolante (Acquedotto Costiero, Diga Jato)
    t = Tex(n, w, h, [hexc('3a4448'), hexc('5a666a'), hexc('7a888c'), hexc('a0acb0'), hexc('8a5a3a'),
                      hexc('6aa0c8')])
    t.fill(2)
    t.hline(0, 0, 32, 0)
    t.rect(0, 2, 32, 3, 3)
    t.rect(0, 11, 32, 5, 1)
    for x in (0, 16):
        t.rect(x, 0, 2, 16, 0)
    t.speckle([4], 0.08, (0, 5, 32, 6))
    t.put(9, 15, 5)
    t.put(24, 14, 5)
    return t


@tex('casello', 32, 32)
def _casello(n, w, h, s):
    # casello autostradale (Barriera di Villafranca sull'A20): cabine con le corsie e le sbarre
    t = Tex(n, w, h, [hexc('d8d8d0'), hexc('f0f0e8'), hexc('2a5a9a'), hexc('3a7ac8'), hexc('c83228'),
                      hexc('1a1a1a'), hexc('8a8a86')])
    t.fill(1)
    t.rect(0, 0, 32, 5, 2)
    t.hline(0, 5, 32, 3)
    for x in (3, 19):
        t.rect(x, 9, 10, 12, 6)
        t.rect(x + 1, 10, 8, 6, 3)
        t.rect(x, 21, 10, 11, 0)
    for x in range(0, 32, 4):
        t.put(x, 30, 4 if (x // 4) % 2 else 1)
    return t


@tex('pilone', 32, 32)
def _pilone(n, w, h, s):
    # il traliccio del pilone di Torre Faro: maglie d'acciaio a bande bianche e rosse
    t = Tex(n, w, h, [hexc('9ab8d8'), hexc('f0f0ec'), hexc('c83228'), hexc('6a6a6a'), hexc('3a3a3a')])
    t.fill(0)
    band = 1
    for y in range(32):
        if y % 16 == 0:
            band = 2 if band == 1 else 1
        for x in (0, 1, 30, 31):
            t.put(x, y, band)
        t.put(y, y, 3)
        t.put(31 - y, y, 3)
        if y % 8 == 0:
            t.hline(0, y, 32, band)
    return t


# ---- sagome (indice 0 trasparente) --------------------------------------------------------


@tex('colonnato', 16, 32, sagoma=True)
def _colonnato(n, w, h, s):
    # colonna dorica scanalata con capitello: in fila diventa il peristilio del tempio
    t = Tex(n, w, h, [(0, 0, 0)] + TUFO + [hexc('6a5030')], sagoma=True)
    t.rect(1, 0, 14, 3, 4)
    t.hline(1, 3, 14, 6)
    t.rect(3, 4, 10, 2, 3)
    t.rect(4, 6, 8, 26, 3)
    for x in (5, 7, 9, 11):
        t.vline(x, 6, 26, 2)
    t.vline(4, 6, 26, 1)
    t.speckle([1, 5], 0.06, (4, 6, 8, 26), wrap=False)
    return t


@tex('stele', 16, 32, sagoma=True)
def _stele(n, w, h, s):
    # le steli di Capaci: pietra scura e liscia, nessuna scritta leggibile da lontano (tono sobrio)
    t = Tex(n, w, h, [(0, 0, 0), hexc('3a3e44'), hexc('4e545c'), hexc('6a7078'), hexc('e8e4d8')], sagoma=True)
    t.rect(4, 4, 8, 26, 2)
    t.rect(4, 4, 2, 26, 1)
    t.rect(10, 4, 2, 26, 3)
    t.hline(4, 3, 8, 3)
    t.rect(2, 29, 12, 3, 1)
    t.hline(6, 12, 4, 4)
    return t


@tex('pala_eolica', 16, 32, sagoma=True)
def _pala_eolica(n, w, h, s):
    # pala eolica scollegata dei crinali trapanesi: torre bianca e rotore fermo
    t = Tex(n, w, h, [(0, 0, 0), hexc('c8ccd0'), hexc('eceef0'), hexc('8a9096')], sagoma=True)
    t.rect(7, 8, 2, 24, 2)
    t.vline(7, 8, 24, 1)
    t.rect(6, 6, 4, 3, 3)
    for k in range(7):
        t.put(8, 6 - k, 2, wrap=False)
        t.put(8 - k, 7 + k // 2, 2, wrap=False)
        t.put(8 + k, 7 + k // 2, 1, wrap=False)
    return t


@tex('mulino', 32, 32, sagoma=True)
def _mulino(n, w, h, s):
    # mulino a vento delle saline: torre di tufo bianco, tetto conico e quattro vele
    t = Tex(n, w, h, [(0, 0, 0), hexc('e8e2d0'), hexc('f8f4e8'), hexc('b8b0a0'), COTTO[1], LEGNO[1],
                      hexc('f0ece0')], sagoma=True)
    t.rect(11, 14, 10, 18, 2)
    t.rect(11, 14, 2, 18, 3)
    t.rect(14, 24, 4, 8, 5)
    for k in range(6):
        t.hline(16 - k - 1, 8 + k, 2 * k + 2, 4, wrap=False)
    for k in range(12):
        t.put(16 + k, 8 - k // 2, 6, wrap=False)
        t.put(16 - k, 8 + k // 2, 6, wrap=False)
        t.put(16 + k // 2, 8 + k, 5, wrap=False)
        t.put(16 - k // 2, 8 - k, 5, wrap=False)
    return t


@tex('mucchio_sale', 16, 16, sagoma=True)
def _mucchio_sale(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('c8c4bc'), hexc('ecebe6'), hexc('fcfcfa'), hexc('a84c2a')], sagoma=True)
    for y in range(5, 15):
        r = (y - 4) * 0.75
        t.hline(int(8 - r), y, int(2 * r), 2, wrap=False)
        t.put(int(8 + r) - 1, y, 1, wrap=False)
    t.put(8, 5, 3)
    t.hline(2, 14, 12, 4)
    return t


@tex('faggio', 32, 32, sagoma=True)
def _faggio(n, w, h, s):
    # faggio dei Nebrodi e delle Madonie: tronco grigio liscio, chioma fitta
    t = Tex(n, w, h, [(0, 0, 0), hexc('6a6a62'), hexc('8a8a80'), hexc('1e3a1a'), hexc('2c5222'),
                      hexc('3e6a2c'), hexc('5a8a3a'), hexc('14280e')], sagoma=True)
    t.rect(14, 18, 4, 14, 2)
    t.vline(14, 18, 14, 1)
    chioma(t, 16, 11, 14, 11, [4, 5, 6, 5], 7)
    return t


@tex('mandorlo', 32, 32, sagoma=True)
def _mandorlo(n, w, h, s):
    # mandorlo in fiore della Valle dei Templi
    t = Tex(n, w, h, [(0, 0, 0), LEGNO[0], LEGNO[1], hexc('e8b8c8'), hexc('f4d4dc'), hexc('fcf0f2'),
                      hexc('c48a9c'), hexc('5a7a3a')], sagoma=True)
    t.rect(15, 18, 3, 14, 2)
    t.vline(15, 18, 14, 1)
    for k in range(6):
        t.put(15 - k, 18 - k, 1, wrap=False)
        t.put(18 + k, 18 - k, 1, wrap=False)
    chioma(t, 16, 11, 13, 9, [3, 4, 5, 4], 6)
    t.speckle([7], 0.03, (4, 4, 24, 14), wrap=False)
    for i in range(len(t.px)):
        if t.px[i] == 7 and not (4 <= i % 32 < 28):
            t.px[i] = 0
    return t


@tex('vite', 16, 16, sagoma=True)
def _vite(n, w, h, s):
    # filare di vite (Marsala, Canicattì): palo, tralci e grappoli
    t = Tex(n, w, h, [(0, 0, 0), LEGNO[1], hexc('3a6a2a'), hexc('5a8a3a'), hexc('7aa04a'), hexc('5a2a5a'),
                      hexc('c8d070')], sagoma=True)
    palo(t, 7, 2, 16, 1)
    t.hline(1, 3, 14, 1)
    chioma(t, 8, 7, 7, 4, [2, 3, 4], 2)
    for x, y in ((4, 9), (10, 10), (12, 8)):
        t.put(x, y, 5)
        t.put(x, y + 1, 5)
    t.put(6, 10, 6)
    return t


@tex('palma_nana', 16, 16, sagoma=True)
def _palma_nana(n, w, h, s):
    # palma nana (giummara) dello Zingaro e di San Vito
    t = Tex(n, w, h, [(0, 0, 0), hexc('2a4a22'), hexc('3e6a2e'), hexc('5a8a3e'), hexc('7aa452'), LEGNO[1]],
            sagoma=True)
    t.rect(7, 12, 2, 4, 5)
    for k, (dx, dy) in enumerate(((-7, -4), (7, -4), (-5, -9), (5, -9), (0, -11), (-7, 1), (7, 1))):
        for i in range(8):
            x = 8 + dx * i / 7
            y = 12 + dy * i / 7
            t.put(int(x), int(y), 1 + (i % 4), wrap=False)
    return t


@tex('guardrail', 16, 16, sagoma=True)
def _guardrail(n, w, h, s):
    # guardrail dell'autostrada (in fila diventa una barriera continua)
    t = Tex(n, w, h, [(0, 0, 0), hexc('5a6066'), hexc('9aa2a8'), hexc('c8d0d4'), hexc('d8b030')], sagoma=True)
    t.rect(0, 7, 16, 4, 2)
    t.hline(0, 7, 16, 3)
    t.hline(0, 10, 16, 1)
    t.rect(7, 11, 2, 5, 1)
    t.put(7, 8, 4)
    return t


@tex('autobotte', 32, 16, sagoma=True)
def _autobotte(n, w, h, s):
    # l'autobotte abusiva del consorzio dell'acqua (Licata, Agrigento, Lampedusa)
    t = Tex(n, w, h, [(0, 0, 0), hexc('1a1a1a'), hexc('4a4a4a'), hexc('2a5ca8'), hexc('5a8ad0'),
                      hexc('c8ccd0'), hexc('eceef0'), hexc('d8b030')], sagoma=True)
    t.rect(2, 3, 20, 8, 5)
    t.hline(2, 3, 20, 6)
    t.hline(2, 10, 20, 2)
    for x in (6, 12, 18):
        t.vline(x, 3, 8, 2)
    t.rect(22, 4, 8, 7, 3)
    t.rect(24, 5, 4, 3, 4)
    t.hline(22, 4, 8, 4)
    for cx in (6, 12, 26):
        t.disc(cx, 12.5, 2.5, 1)
        t.disc(cx, 12.5, 1, 2)
    t.put(29, 9, 7)
    return t


@tex('carretto', 32, 16, sagoma=True)
def _carretto(n, w, h, s):
    # carretto siciliano dipinto (mercati di Palermo, Bagheria)
    t = Tex(n, w, h, [(0, 0, 0), hexc('1a1a1a'), hexc('d8b030'), hexc('c83228'), hexc('2a5ca8'),
                      hexc('3a8a4a'), LEGNO[1], LEGNO[2]], sagoma=True)
    t.rect(4, 3, 20, 7, 2)
    for x in range(5, 23, 4):
        t.rect(x, 4, 3, 5, 3 + (x // 4) % 3)
    t.hline(4, 3, 20, 7)
    t.hline(24, 8, 8, 6)
    for cx in (9, 19):
        t.disc(cx, 11.5, 4, 3)
        t.disc(cx, 11.5, 2.5, 2)
        t.put(cx, 11, 1)
    return t


@tex('bancarella', 32, 16, sagoma=True)
def _bancarella(n, w, h, s):
    # bancarella di Ballarò e della Vucciria: tenda a strisce, cassette di frutta e pesce
    t = Tex(n, w, h, [(0, 0, 0), hexc('c83228'), hexc('f0ece0'), LEGNO[1], hexc('e88a2a'), hexc('d8c040'),
                      hexc('5a8a3a'), hexc('8ab4cc'), hexc('2a2a2a')], sagoma=True)
    for x in range(1, 31):
        t.vline(x, 1, 4, 1 if (x // 3) % 2 else 2)
    palo(t, 2, 5, 16, 8)
    palo(t, 29, 5, 16, 8)
    t.rect(3, 9, 26, 5, 3)
    for k, x in enumerate(range(4, 28, 4)):
        t.rect(x, 7, 3, 2, (4, 5, 6, 7)[k % 4])
    return t


@tex('traghetto', 32, 32, sagoma=True)
def _traghetto(n, w, h, s):
    # traghetto attraccato (Messina, Milazzo, Porto Empedocle, Trapani)
    t = Tex(n, w, h, [(0, 0, 0), hexc('1a2a4a'), hexc('2a4a8a'), hexc('f0f0ec'), hexc('c8ccd0'),
                      hexc('2e3640'), hexc('c83228'), hexc('d8b030')], sagoma=True)
    for y in range(20, 30):
        k = max(0, y - 26)
        t.hline(1 + k, y, 30 - 2 * k, 2 if y > 24 else 3, wrap=False)
    t.hline(1, 24, 30, 1)
    t.rect(6, 12, 20, 8, 3)
    t.rect(10, 6, 12, 6, 4)
    for x in range(8, 25, 3):
        t.put(x, 15, 5)
        t.put(x, 16, 5)
    t.rect(19, 2, 3, 5, 6)
    t.hline(19, 2, 3, 7)
    return t


# --------------------------------------------------------------------------- aree
# Texture nuove del tileset condiviso della matrice 0 (R-GFX-18): si aggiungono a SICILIA_4_2.
SICILIA_4_3 = [
    # terreni
    'tufo', 'marna', 'salina', 'cordolo',
    # muri, facciate, tetti
    'fac_tufo', 'fac_liberty', 'fac_normanna', 'trabeazione', 'cupola_rossa', 'maiolica', 'tubo',
    'casello', 'pilone',
    # sagome
    'colonnato', 'stele', 'pala_eolica', 'mulino', 'mucchio_sale', 'faggio', 'mandorlo', 'vite',
    'palma_nana', 'guardrail', 'autobotte', 'carretto', 'bancarella', 'traghetto',
]
SICILIA = SICILIA_4_2 + SICILIA_4_3

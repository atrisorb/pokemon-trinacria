"""Texture degli interni, delle grotte e delle mappe aperte del blocco 4.2 (R-GFX-17).

Si registrano nel catalogo di tex42.py. Il tileset degli interni del blocco contiene le 69 texture
della matrice 0 (stessi nomi) più queste 29: così le mappe aperte (pineta, polo, MUOS, cantiere)
usano gli stessi terreni delle celle esterne.
"""
from tex42 import (Tex, tex, hexc, mix, lastre, mattoni, rumore, chioma, palo, LEGNO, FOGLIA)


@tex('pav_marmo', 32, 32)
def _pav_marmo(n, w, h, s):
    t = Tex(n, w, h, [hexc('2a2a2e'), hexc('d8d4cc'), hexc('ece8e0'), hexc('b8b2a8'), hexc('7a3a2a')])
    for y in range(32):
        for x in range(32):
            t.put(x, y, 0 if (x // 8 + y // 8) % 2 else 2)
    t.speckle([3], 0.05)
    t.frame(0, 0, 32, 32, 4)
    return t


@tex('parquet', 32, 32)
def _parquet(n, w, h, s):
    t = Tex(n, w, h, LEGNO + [hexc('c49460')])
    for y0 in range(0, 32, 8):
        for x0 in range(0, 32, 8):
            vert = (x0 // 8 + y0 // 8) % 2
            for k in range(0, 8, 2):
                c = 2 + (k // 2) % 3
                if vert:
                    t.rect(x0 + k, y0, 2, 8, c)
                    t.vline(x0 + k, y0, 8, 0)
                else:
                    t.rect(x0, y0 + k, 8, 2, c)
                    t.hline(x0, y0 + k, 8, 0)
    return t


@tex('pav_ufficio', 32, 32)
def _pav_ufficio(n, w, h, s):
    t = Tex(n, w, h, [hexc('7a7a76'), hexc('a4a29c'), hexc('b8b6ae'), hexc('c8c6be')])
    t.fill(2)
    lastre(t, 16, 16, 0, sfalsa=False, vari=(1, 2, 3, 2))
    return t


@tex('moquette', 32, 32)
def _moquette(n, w, h, s):
    t = Tex(n, w, h, [hexc('5a1a22'), hexc('7a2430'), hexc('8e2e3a'), hexc('c8a040')])
    t.fill(1)
    t.speckle([0, 2], 0.3)
    for k in range(0, 32, 16):
        t.hline(0, k, 32, 3)
        t.vline(k, 0, 32, 3)
    return t


@tex('cemento', 32, 32)
def _cemento(n, w, h, s):
    t = Tex(n, w, h, [hexc('5c5c5a'), hexc('6e6e6a'), hexc('82827c'), hexc('949490')])
    t.fill(2)
    t.speckle([0, 1, 3], 0.3)
    t.hline(0, 0, 32, 1)
    t.vline(0, 0, 32, 1)
    return t


@tex('pav_grotta', 32, 32)
def _pav_grotta(n, w, h, s):
    t = Tex(n, w, h, [hexc('4a4034'), hexc('5c5042'), hexc('6e6250'), hexc('827460'), hexc('3a3228')])
    t.fill(2)
    rumore(t, [0, 1, 3, 4], 0.4, macchie=3)
    return t


@tex('ghiaccio', 32, 32)
def _ghiaccio(n, w, h, s):
    t = Tex(n, w, h, [hexc('7aa8c8'), hexc('9cc4dc'), hexc('bcdcec'), hexc('e0f0f8'), hexc('f8ffff')])
    t.fill(2)
    for k in range(0, 32, 9):
        for i in range(10):
            t.put(k + i, i * 2, 4)
            t.put(k + i + 1, i * 2, 3)
    t.speckle([0, 1], 0.08)
    return t


@tex('pav_zolfo', 32, 32)
def _pav_zolfo(n, w, h, s):
    t = Tex(n, w, h, [hexc('5a5030'), hexc('7a6a34'), hexc('a08c34'), hexc('c8b040'), hexc('e8d860')])
    t.fill(1)
    rumore(t, [0, 2, 3, 4], 0.45, macchie=4)
    return t


def parete(n, w, h, base, scuro, chiaro, motivo='intonaco'):
    t = Tex(n, w, h, [scuro, base, chiaro, hexc('2a2a2a'), mix(base, scuro, 0.5)])
    t.fill(1)
    t.speckle([4, 2], 0.08)
    if motivo == 'pannelli':
        for x in range(0, 32, 16):
            t.frame(x + 1, 6, 14, 22, 0)
    elif motivo == 'boiserie':
        t.rect(0, 18, 32, 14, 0)
        for x in range(0, 32, 8):
            t.frame(x + 1, 20, 6, 10, 4)
        t.hline(0, 18, 32, 2)
    elif motivo == 'piastrelle':
        lastre(t, 8, 8, 4, sfalsa=False)
    elif motivo == 'mattoni':
        mattoni(t, 8, 4, 0, [1, 4, 1, 2])
    t.hline(0, 31, 32, 3)
    return t


@tex('par_intonaco', 32, 32)
def _par_intonaco(n, w, h, s):
    return parete(n, w, h, hexc('d8c8a8'), hexc('a89878'), hexc('ece0c8'))


@tex('par_ufficio', 32, 32)
def _par_ufficio(n, w, h, s):
    return parete(n, w, h, hexc('b8bcc0'), hexc('7a8088'), hexc('d4d8dc'), 'pannelli')


@tex('par_legno', 32, 32)
def _par_legno(n, w, h, s):
    return parete(n, w, h, hexc('a83a3a'), LEGNO[1], hexc('c85a4a'), 'boiserie')


@tex('par_piastr', 32, 32)
def _par_piastr(n, w, h, s):
    return parete(n, w, h, hexc('dce4e8'), hexc('8a9aa4'), hexc('f4f8f8'), 'piastrelle')


@tex('par_mattoni', 32, 32)
def _par_mattoni(n, w, h, s):
    return parete(n, w, h, hexc('9a5a3a'), hexc('5a3020'), hexc('b47450'), 'mattoni')


@tex('par_club', 32, 32)
def _par_club(n, w, h, s):
    t = parete(n, w, h, hexc('2a1a3a'), hexc('140a1e'), hexc('4a2a64'))
    for x in range(2, 32, 6):
        t.put(x, 10, 2)
        t.put(x + 1, 10, 2)
    return t


@tex('muro_cima', 16, 16)
def _muro_cima(n, w, h, s):
    t = Tex(n, w, h, [hexc('101014'), hexc('1c1c22'), hexc('26262e')])
    t.fill(0)
    t.speckle([1, 2], 0.2)
    return t


@tex('tappeto', 16, 16)
def _tappeto(n, w, h, s):
    t = Tex(n, w, h, [hexc('5a1a22'), hexc('a83030'), hexc('d8b040')])
    t.fill(1)
    t.frame(1, 1, 14, 14, 2)
    t.frame(0, 0, 16, 16, 0)
    return t


@tex('scala', 16, 16)
def _scala(n, w, h, s):
    t = Tex(n, w, h, [hexc('1a1a1e'), hexc('6a6a6a'), hexc('9a9a96'), hexc('c4c4c0')])
    t.fill(0)
    for y in range(0, 16, 4):
        t.rect(1, y + 1, 14, 2, 2 if y < 8 else 1)
        t.hline(1, y + 1, 14, 3)
    return t


@tex('scrivania', 32, 16)
def _scrivania(n, w, h, s):
    t = Tex(n, w, h, LEGNO + [hexc('e8e8e0'), hexc('3a5a8a')])
    t.fill(2)
    t.hline(0, 0, 32, 3)
    t.rect(2, 3, 6, 4, 4)
    t.rect(20, 2, 8, 6, 5)
    t.rect(0, 10, 32, 6, 1)
    t.vline(16, 10, 6, 0)
    return t


@tex('scaffale', 32, 32)
def _scaffale(n, w, h, s):
    t = Tex(n, w, h, LEGNO + [hexc('b83a2a'), hexc('2a5ca8'), hexc('e8d040'), hexc('f0f0e8')])
    t.fill(1)
    for y in range(2, 32, 8):
        t.rect(2, y, 28, 6, 0)
        x = 3
        while x < 29:
            k = t.rng.i(1, 3)
            t.rect(x, y + 1, k, 5, t.rng.i(4, 7))
            x += k + 1
        t.hline(1, y + 6, 30, 3)
    return t


@tex('bancone', 32, 16)
def _bancone(n, w, h, s):
    t = Tex(n, w, h, [hexc('3a2a1e'), LEGNO[2], LEGNO[3], hexc('e8e0cc'), hexc('b8b0a0')])
    t.fill(1)
    t.rect(0, 0, 32, 3, 3)
    t.hline(0, 3, 32, 4)
    for x in range(0, 32, 8):
        t.vline(x, 4, 12, 0)
        t.frame(x + 1, 6, 6, 8, 2)
    return t


@tex('cassa', 16, 16)
def _cassa(n, w, h, s):
    t = Tex(n, w, h, LEGNO + [hexc('c8a070')])
    t.fill(2)
    t.frame(0, 0, 16, 16, 0)
    for y in range(4, 16, 4):
        t.hline(1, y, 14, 1)
    for k in range(14):
        t.put(1 + k, 1 + k, 4)
    return t


@tex('sedia', 16, 16, sagoma=True)
def _sedia(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), LEGNO[0], LEGNO[2], hexc('a83030')], sagoma=True)
    t.rect(4, 2, 8, 7, 2)
    t.rect(5, 3, 6, 5, 3)
    t.rect(3, 9, 10, 2, 1)
    palo(t, 4, 11, 16, 1)
    palo(t, 11, 11, 16, 1)
    return t


@tex('pianta', 16, 32, sagoma=True)
def _pianta(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('8a4a2a'), hexc('a85a34')] + FOGLIA[1:], sagoma=True)
    t.rect(4, 24, 8, 8, 1)
    t.rect(5, 24, 6, 7, 2)
    chioma(t, 8, 14, 6, 10, [4, 5, 6], 3)
    return t


@tex('panca', 32, 16)
def _panca(n, w, h, s):
    t = Tex(n, w, h, [LEGNO[0], LEGNO[1], LEGNO[2], LEGNO[3]])
    t.fill(2)
    t.hline(0, 0, 32, 3)
    t.rect(0, 8, 32, 8, 1)
    for x in range(0, 32, 4):
        t.vline(x, 9, 7, 0)
    return t


@tex('candelora', 16, 32, sagoma=True)
def _candelora(n, w, h, s):
    # le candelore di Sant’Agata: colonne dorate con le candele
    t = Tex(n, w, h, [(0, 0, 0), hexc('8a6a20'), hexc('c8a030'), hexc('f0d860'), hexc('f8f8e8'), hexc('f88a20')],
            sagoma=True)
    t.rect(4, 10, 8, 20, 2)
    t.vline(5, 10, 20, 3)
    t.vline(10, 10, 20, 1)
    t.rect(3, 28, 10, 4, 1)
    t.rect(2, 6, 12, 4, 3)
    for x in (4, 7, 10):
        t.vline(x, 2, 4, 4)
        t.put(x, 1, 5)
    return t


@tex('stalagmite', 16, 32, sagoma=True)
def _stalagmite(n, w, h, s):
    t = Tex(n, w, h, [(0, 0, 0), hexc('4e4436'), hexc('6a5e4a'), hexc('86785e'), hexc('a49478')], sagoma=True)
    for y in range(8, 32):
        r = (y - 8) / 4.5
        t.hline(int(8 - r), y, max(1, int(2 * r)), 2, wrap=False)
        t.put(int(8 - r), y, 1, wrap=False)
        t.put(int(8 + r) - 1, y, 3, wrap=False)
    t.vline(7, 8, 8, 4)
    return t


@tex('carrello', 16, 16, sagoma=True)
def _carrello(n, w, h, s):
    # carrello della zolfara
    t = Tex(n, w, h, [(0, 0, 0), hexc('1e1e1e'), hexc('5a4030'), hexc('7a5a40'), hexc('c8b040')], sagoma=True)
    for y in range(4, 12):
        k = (y - 4) // 3
        t.hline(1 + k, y, 14 - 2 * k, 3)
    t.hline(1, 4, 14, 2)
    t.rect(3, 5, 10, 2, 4)
    t.disc(4.5, 13, 2, 1)
    t.disc(11.5, 13, 2, 1)
    return t


@tex('fusto', 16, 16, sagoma=True)
def _fusto(n, w, h, s):
    # fusti accatastati di nascosto
    t = Tex(n, w, h, [(0, 0, 0), hexc('2a3a2a'), hexc('3c5a3c'), hexc('5a7a4a'), hexc('d8c040'), hexc('7a4a30')],
            sagoma=True)
    for x0 in (1, 8):
        t.rect(x0, 3, 7, 13, 2)
        t.vline(x0, 3, 13, 1)
        t.vline(x0 + 5, 3, 13, 3)
        t.hline(x0, 6, 7, 1)
        t.hline(x0, 12, 7, 1)
        t.rect(x0 + 2, 8, 3, 2, 4)
    t.speckle([5], 0.05, (1, 3, 14, 13), wrap=False)
    return t


@tex('quadro_com', 32, 16)
def _quadro_com(n, w, h, s):
    # quadro comandi e monitor: sala controllo, sala radar, cabina del Commissario
    t = Tex(n, w, h, [hexc('2a2e34'), hexc('4a525a'), hexc('1a4a2a'), hexc('40d860'), hexc('e83a2a'), hexc('f8d040')])
    t.fill(1)
    for x in range(2, 30, 10):
        t.rect(x, 2, 8, 6, 2)
        t.hline(x + 1, 4, 6, 3)
        t.put(x + 2, 6, 3)
    for x in range(2, 30, 3):
        t.put(x, 11, 4 if x % 2 else 5)
    t.rect(0, 13, 32, 3, 0)
    return t


INTERNI_4_2 = [
    'pav_marmo', 'parquet', 'pav_ufficio', 'moquette', 'cemento', 'pav_grotta', 'ghiaccio', 'pav_zolfo',
    'par_intonaco', 'par_ufficio', 'par_legno', 'par_piastr', 'par_mattoni', 'par_club', 'muro_cima', 'tappeto',
    'scala', 'scrivania', 'scaffale', 'bancone', 'cassa', 'sedia', 'pianta', 'panca', 'candelora', 'stalagmite',
    'carrello', 'fusto', 'quadro_com',
]

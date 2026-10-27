"""Texture nuove degli interni, delle grotte e delle mappe aperte del blocco 4.3 (R-GFX-17).

Si registrano nel catalogo di tex42.py accanto a quelle di texint42.py. Il tileset degli interni del
4.3 non è una lista fissa: contiene le texture che le stanze, le grotte, le mappe aperte e le isole
del blocco citano davvero (costruisci43.py le conta dopo aver messo giù le celle), così resta sotto i
limiti di HeartGold anche se il tileset condiviso della matrice 0 cresce.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '4.2'))
import texint42  # noqa: E402,F401  (registra le texture degli interni del 4.2)
from tex42 import Tex, tex, hexc, lastre, rumore, LAVA  # noqa: E402


@tex('mosaico', 32, 32)
def _mosaico(n, w, h, s):
    # pavimento a mosaico della Villa Romana del Casale: tessere chiare, cornici a treccia
    t = Tex(n, w, h, [hexc('e8dcc0'), hexc('d4c4a0'), hexc('a83a28'), hexc('2a3a5a'), hexc('c8a040'),
                      hexc('5a7a3a'), hexc('3a2a1a')])
    t.fill(0)
    t.speckle([1], 0.25)
    t.frame(0, 0, 32, 32, 3)
    t.frame(2, 2, 28, 28, 2)
    for k in range(4, 28, 4):
        t.put(k, 2, 4)
        t.put(2, k, 4)
    t.disc(16, 16, 6, 4, wrap=False)
    t.disc(16, 16, 4, 5, wrap=False)
    t.disc(16, 16, 2, 2, wrap=False)
    t.put(16, 16, 6)
    return t


@tex('par_mosaico', 32, 32)
def _par_mosaico(n, w, h, s):
    # le pareti d'oro bizantino del Duomo di Monreale e della Cappella Palatina
    t = Tex(n, w, h, [hexc('8a6a1a'), hexc('b8902a'), hexc('d8b040'), hexc('f0d870'), hexc('2a3a6a'),
                      hexc('a83a28'), hexc('f4ecd8')])
    t.fill(2)
    t.speckle([1, 3], 0.3)
    t.rect(10, 6, 12, 20, 4)
    t.disc(16, 6, 6, 4, wrap=False)
    t.disc(16, 9, 3, 6, wrap=False)
    t.rect(13, 13, 6, 12, 5)
    t.hline(0, 30, 32, 0)
    t.hline(0, 31, 32, 0)
    return t


@tex('cretto', 32, 32)
def _cretto(n, w, h, s):
    # il cemento bianco del Grande Cretto di Burri: lastre con le crepe che ricalcano le vie
    t = Tex(n, w, h, [hexc('b8b4ac'), hexc('d4d0c8'), hexc('e8e6e0'), hexc('f4f2ee'), hexc('9a968e')])
    t.fill(2)
    t.speckle([1, 3], 0.18)
    x = 9
    for y in range(32):
        t.put(x, y, 4)
        if y % 6 == 5:
            x += 1 if (y // 6) % 2 else -1
    t.hline(0, 20, 32, 4)
    return t


@tex('lava_viva', 32, 32)
def _lava_viva(n, w, h, s):
    # la Sciara del Fuoco di Stromboli: crosta nera con le colate accese (bloccata)
    t = Tex(n, w, h, LAVA[:3] + [hexc('a82a10'), hexc('e85a18'), hexc('f8a030'), hexc('f8e070')])
    t.fill(1)
    rumore(t, [0, 2], 0.3)
    for x0 in (5, 21):
        x = x0
        for y in range(32):
            t.put(x, y, 4)
            t.put(x + 1, y, 5 if y % 3 else 6)
            t.put(x + 2, y, 3)
            if y % 4 == 3:
                x += 1 if (y // 4) % 2 else -1
    return t


@tex('vapore', 16, 32, sagoma=True)
def _vapore(n, w, h, s):
    # nuvola di vapore delle Stufe di San Calogero sul Monte Kronio
    t = Tex(n, w, h, [(0, 0, 0), hexc('c8ccd0'), hexc('e0e4e8'), hexc('f4f6f8')], sagoma=True)
    for cy, r in ((26, 5), (19, 5.5), (12, 5), (6, 4)):
        t.disc(8, cy, r, 1, ry=r * 0.9)
        t.disc(7, cy - 1, r - 1.5, 2, ry=(r - 1.5) * 0.9)
        t.disc(6, cy - 2, r - 3, 3, ry=max(0.5, (r - 3) * 0.9))
    return t


INTERNI_4_3_NUOVE = ['mosaico', 'par_mosaico', 'cretto', 'lava_viva', 'vapore']

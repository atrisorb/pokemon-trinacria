"""Blocco 4.4 — schermata del titolo (GFX-TITLE-*).

src/title_screen.c (TitleScreenAnim_Load2dBgGfx, versione HeartGold) carica sullo schermo superiore:
  - GF_BG_LYR_SUB_3: titledemo_00000034.png (256×192, 8 bit, schermata 35 = una tile per posto), il fondo;
  - GF_BG_LYR_SUB_2: titledemo_00000003.png (256×120, 8 bit, schermata 0: tre righe più in basso), il logo,
    con la palette estesa presa da titledemo_00000004.NCLR;
  - GF_BG_LYR_SUB_1: titledemo_00000015.png (256×24, 4 bit, schermata 17, palette 7), la riga dello sviluppatore;
  - palette dello schermo: titledemo_00000004.NCLR (256 colori) per tutti e tre.
Divisione degli indici della NCLR 4 (stessa di HeartGold): logo 1–15 (0 trasparente), 16–31 invariati (il
bagliore del titolo li sfuma: TitleScreenAnim_RunTopScreenGlow), riga dell'autore 124–126, fondo 128–255.
Il disegno è tutto procedurale (R-GFX-17): lettere del logo = glifi del font del gioco ingranditi, con
contorno e sfumatura; triscele (la Trinacria della bandiera siciliana) da segmenti spessi; fondo = alba
sull'Etna e sullo Ionio con retinatura ordinata 4×4."""
import math

import comune44 as C

LOGO = 'files/demo/title/titledemo/titledemo_00000003.png'
FONDO = 'files/demo/title/titledemo/titledemo_00000034.png'
AUTORE = 'files/demo/title/titledemo/titledemo_00000015.png'
NCLR = 'files/demo/title/titledemo/titledemo_00000004.NCLR'
NSCR_LOGO = 'files/demo/title/titledemo/titledemo_00000000.NSCR'
NSCR_FONDO = 'files/demo/title/titledemo/titledemo_00000035.NSCR'
NSCR_AUTORE = 'files/demo/title/titledemo/titledemo_00000017.NSCR'
TESTO_AUTORE = '© 2026 atrisorb · progetto amatoriale'

L = dict(contorno=1, blu_scuro=2, blu=3, azzurro=4, giallo_chiaro=5, giallo=6, arancio=7, rosso=8,
         rosso_scuro=9, bianco=10, crema=11, ombra=12, oro=13, grigio=14, pelle=15)
COLORI_LOGO = {1: (16, 16, 40), 2: (24, 48, 120), 3: (48, 104, 208), 4: (128, 184, 248), 5: (255, 244, 168),
               6: (248, 208, 48), 7: (240, 140, 32), 8: (216, 40, 32), 9: (128, 16, 24), 10: (255, 255, 255),
               11: (248, 232, 200), 12: (8, 8, 24), 13: (176, 120, 24), 14: (128, 128, 144), 15: (240, 184, 152)}
COLORI_AUTORE = {124: (248, 248, 248), 125: (72, 72, 96), 126: (16, 16, 32)}
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


# ------------------------------------------------------------------------------------------- palette

def _rampa(stops, n):
    """n colori interpolati fra le tappe [(t, rgb)]."""
    out = []
    for k in range(n):
        t = k / (n - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                a = (t - t0) / (t1 - t0) if t1 > t0 else 0
                out.append(tuple(round(c0[i] + (c1[i] - c0[i]) * a) for i in range(3)))
                break
    return out


RAMPE = {   # nome: (primo indice, tappe, numero di colori)
    'cielo': (128, [(0, (18, 20, 60)), (0.35, (70, 44, 110)), (0.62, (186, 84, 92)), (0.82, (244, 146, 70)),
                    (1, (255, 226, 150))], 44),
    'sole': (172, [(0, (255, 232, 160)), (1, (255, 255, 236))], 6),
    'mare': (178, [(0, (232, 150, 96)), (0.25, (150, 84, 96)), (0.6, (52, 46, 96)), (1, (12, 18, 52))], 24),
    'etna': (202, [(0, (22, 14, 30)), (1, (96, 58, 70))], 16),
    'fumo': (218, [(0, (60, 50, 78)), (1, (176, 150, 168))], 14),
    'costa': (232, [(0, (6, 6, 18)), (1, (44, 34, 52))], 12),
    'luci': (244, [(0, (255, 200, 90)), (1, (255, 120, 40))], 4),
    'lava': (248, [(0, (255, 210, 80)), (0.5, (240, 80, 20)), (1, (120, 20, 20))], 8),
}


def palette_fondo():
    col = {}
    for nome, (i0, stops, n) in RAMPE.items():
        for k, c in enumerate(_rampa(stops, n)):
            col[i0 + k] = c
    return col


def _da(nome, t, x, y):
    """Indice della rampa al punto t∈[0,1] con retinatura ordinata."""
    i0, _, n = RAMPE[nome]
    v = max(0.0, min(1.0, t)) * (n - 1)
    k = int(v)
    if k < n - 1 and (v - k) * 16 > BAYER[y % 4][x % 4] + 0.5:
        k += 1
    return i0 + k


def _rumore(x, y):
    v = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((v ^ (v >> 16)) & 0xFFFF) / 65535.0


def _liscio(x, y, passo):
    gx, gy = x / passo, y / passo
    x0, y0 = int(math.floor(gx)), int(math.floor(gy))
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b, c, d = _rumore(x0, y0), _rumore(x0 + 1, y0), _rumore(x0, y0 + 1), _rumore(x0 + 1, y0 + 1)
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


# ---------------------------------------------------------------------------------------------- fondo

def disegna_fondo():
    W, H = 256, 192
    oriz = 150
    sx, sy, sr = 66, 148, 15
    pix = [0] * (W * H)
    # profilo dell'Etna: base larga a destra, cima piatta col cratere
    def etna(x):
        cima = 186
        if abs(x - cima) <= 7:
            return 70
        d = abs(x - cima) - 7
        return 70 + d * (0.55 + 0.004 * d) - 4 * math.sin(d / 9.0)
    for y in range(H):
        for x in range(W):
            if y < oriz:
                t = y / oriz
                d = math.hypot(x - sx, (y - sy) * 1.2)
                c = _da('cielo', t + max(0, 0.22 - d / 300), x, y)
                if d < sr:
                    c = _da('sole', 1 - d / sr, x, y)
                elif d < sr + 3:
                    c = _da('cielo', 1.0, x, y)
                if y >= etna(x):
                    alt = (y - etna(x)) / 60.0
                    c = _da('etna', 0.15 + 0.35 * max(0, 1 - alt) + (0.25 if x < 186 - (y - 70) * 0.1 else 0), x, y)
                    # colata sul fianco sud
                    if 120 < y < oriz and abs(x - (190 + (y - 120) * 0.35) - 3 * math.sin(y / 5.0)) < 1.2:
                        c = _da('lava', (y - 120) / 40.0, x, y)
            else:
                t = (y - oriz) / (H - oriz)
                c = _da('mare', 0.12 + 0.88 * t, x, y)
                # riflesso del sole: righe orizzontali spezzate
                lar = 10 + (y - oriz) * 0.6
                if abs(x - sx) < lar and (y % 3 != 0) and _rumore(x // 3, y) > 0.35 + abs(x - sx) / lar * 0.6:
                    c = _da('sole', 0.2, x, y) if y < oriz + 12 else _da('mare', 0.02, x, y)
            pix[y * W + x] = c
    # pennacchio dal cratere, spinto dal vento verso ovest
    for y in range(8, 72):
        for x in range(60, 230):
            k = (70 - y) / 62.0
            cx = 186 - k * 120 - 8 * math.sin(k * 5)
            r = 4 + k * 22
            d = abs(x - cx) / r + abs(y - (70 - k * 62)) / (6 + k * 10)
            dens = 1.0 - d + 0.35 * (_liscio(x, y, 7) - 0.5)
            if dens > 0.15 and y < etna(x):
                pix[y * W + x] = _da('fumo', min(1, 0.25 + dens * 0.6 + 0.25 * (1 - k)), x, y)
    # costa in primo piano con le luci dei paesi
    for x in range(W):
        top = H - 10 - 6 * math.sin(x / 23.0) - 4 * _liscio(x, 0, 9) - (10 if x > 150 else 0) * min(1, (x - 150) / 40)
        for y in range(int(top), H):
            pix[y * W + x] = _da('costa', 0.2 + 0.6 * (H - y) / 20.0, x, y)
        if x % 7 == 3 and _rumore(x, 3) > 0.45:
            yy = int(top) + 2 + int(_rumore(x, 9) * 4)
            if yy < H:
                pix[yy * W + x] = _da('luci', _rumore(x, 5), x, yy)
    return W, H, pix


# ----------------------------------------------------------------------------------------------- logo

def _maschera_testo(font, testo, scala):
    w = font.larghezza(testo)
    W, H = w * scala, 16 * scala
    m = [[False] * W for _ in range(H)]
    x0 = 0
    for ch in testo:
        g, gw = font.glifo(ch)
        for r in range(16):
            for c in range(min(gw, 16)):
                if g[r][c] == 1:
                    for dy in range(scala):
                        for dx in range(scala):
                            m[r * scala + dy][(x0 + c) * scala + dx] = True
        x0 += gw
    # taglia le righe vuote
    righe = [r for r in range(H) if any(m[r])]
    m = m[righe[0]:righe[-1] + 1]
    return m


def _dilata(m, r):
    H, W = len(m), len(m[0])
    out = [[False] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if m[y][x]:
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        if dx * dx + dy * dy <= r * r + r and 0 <= y + dy < H and 0 <= x + dx < W:
                            out[y + dy][x + dx] = True
    return out


def _metti_testo(pix, W, m, x0, y0, riempi, contorno, ombra, spessore):
    pad = spessore + 1
    H0, W0 = len(m), len(m[0])
    M = [[False] * (W0 + 2 * pad) for _ in range(H0 + 2 * pad)]
    for y in range(H0):
        for x in range(W0):
            M[y + pad][x + pad] = m[y][x]
    bordo = _dilata(M, spessore)
    for y in range(len(M)):
        for x in range(len(M[0])):
            px, py = x0 + x - pad, y0 + y - pad
            if bordo[y][x] and 0 <= px + 1 < W and 0 <= py + 2 < len(pix) // W and not pix[(py + 2) * W + px + 1]:
                pix[(py + 2) * W + px + 1] = ombra
    for y in range(len(M)):
        for x in range(len(M[0])):
            px, py = x0 + x - pad, y0 + y - pad
            if not (0 <= px < W and 0 <= py < len(pix) // W):
                continue
            if M[y][x]:
                pix[py * W + px] = riempi((y - pad) / max(1, H0 - 1), px, py)
            elif bordo[y][x]:
                pix[py * W + px] = contorno


def _segmento(px, py, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _triscele(pix, W, cx, cy, R):
    gambe = []
    for k in range(3):
        a = math.radians(-90 + 120 * k)
        anca = (cx + 0.18 * R * math.cos(a), cy + 0.18 * R * math.sin(a))
        ginocchio = (cx + 0.62 * R * math.cos(a), cy + 0.62 * R * math.sin(a))
        b = a + math.radians(78)
        caviglia = (ginocchio[0] + 0.5 * R * math.cos(b), ginocchio[1] + 0.5 * R * math.sin(b))
        c = b + math.radians(80)
        punta = (caviglia[0] + 0.2 * R * math.cos(c), caviglia[1] + 0.2 * R * math.sin(c))
        gambe += [(anca, ginocchio, 0.13 * R), (ginocchio, caviglia, 0.10 * R), (caviglia, punta, 0.07 * R)]
    testa = 0.27 * R
    for y in range(int(cy - R - 4), int(cy + R + 5)):
        for x in range(int(cx - R - 4), int(cx + R + 5)):
            if not (0 <= x < W and 0 <= y < len(pix) // W):
                continue
            dt = math.hypot(x - cx, y - cy)
            dg = min(_segmento(x, y, a, b) - w for a, b, w in gambe)
            raggi = 0.42 * R + 0.06 * R * math.cos(12 * math.atan2(y - cy, x - cx))
            if dt <= testa - 1.2:
                v = L['pelle']
                if abs(y - (cy - 0.06 * R)) < 1 and abs(abs(x - cx) - 0.1 * R) < 1:
                    v = L['contorno']
                if abs(y - (cy + 0.12 * R)) < 0.8 and abs(x - cx) < 0.08 * R:
                    v = L['rosso']
            elif dt <= testa:
                v = L['contorno']
            elif dg <= 0:
                v = L['pelle'] if dg < -1.3 else L['contorno']
            elif dt <= raggi:
                v = L['giallo'] if dt < raggi - 1.3 else L['oro']
            elif dg <= 1.4:
                v = L['contorno']
            else:
                continue
            pix[y * W + x] = v


def disegna_logo(font):
    W, H = 256, 120
    pix = [0] * (W * H)
    # «Pokémon» in giallo bordato di blu
    m1 = _maschera_testo(font, 'Pokémon', 2)
    x1 = (W - len(m1[0])) // 2
    _metti_testo(pix, W, m1, x1, 3, lambda t, x, y: L['giallo_chiaro'] if t < 0.35 else L['giallo'],
                 L['blu'], L['blu_scuro'], 2)
    # «TRINACRIA» coi colori della bandiera: dal giallo al rosso
    m2 = _maschera_testo(font, 'TRINACRIA', 3)
    x2 = (W - len(m2[0])) // 2
    def caldo(t, x, y):
        if t < 0.2:
            return L['giallo_chiaro']
        if t < 0.45:
            return L['giallo']
        if t < 0.7:
            return L['arancio']
        return L['rosso']
    _metti_testo(pix, W, m2, x2, 31, caldo, L['rosso_scuro'], L['ombra'], 2)
    # triscele sotto il titolo
    _triscele(pix, W, 128, 92, 25)
    return W, H, pix


def disegna_autore(font, W=256, H=24):
    pix = [0] * (W * H)
    w = font.larghezza(TESTO_AUTORE)
    if w > W - 8:
        raise C.Errore('riga dell\'autore larga %d px' % w)
    # indici della palette 7 (124–126 → 12–14 nel PNG a 4 bit)
    font.scrivi(pix, W, H, (W - w) // 2, 4, TESTO_AUTORE, 12, 14)
    return W, H, pix


def costruisci(repo):
    font = C.Font(repo)
    b_nclr = C.leggi(repo, NCLR)
    _, orig = C.nclr_leggi(b_nclr)
    col = [None] * 256
    for i, c in COLORI_LOGO.items():
        col[i] = c
    for i, c in COLORI_AUTORE.items():
        col[i] = c
    for i, c in palette_fondo().items():
        col[i] = c
    nuova = C.nclr_patch(b_nclr, col)
    _, colori = C.nclr_leggi(nuova)
    fw, fh, fpix = disegna_fondo()
    lw, lh, lpix = disegna_logo(font)
    aw, ah, apix = disegna_autore(font)
    usati_logo = sorted(set(lpix))
    if any(16 <= v < 128 for v in usati_logo):
        raise C.Errore('il logo usa indici fuori da 0–15')
    if min(fpix) < 128:
        raise C.Errore('il fondo usa indici sotto 128')
    return dict(nclr=nuova, colori=colori, colori_hg=orig,
                fondo=(fw, fh, fpix), logo=(lw, lh, lpix), autore=(aw, ah, apix),
                colori_fondo=len(set(fpix)), colori_logo=len(usati_logo))


def schermo(repo, r):
    """Anteprima dello schermo superiore: fondo, logo spostato dalla schermata 0, riga dell'autore (17)."""
    W, H = 256, 192
    fw, fh, fpix = r['fondo']
    out = list(fpix)
    lw, lh, lpix = r['logo']
    wt, ht, voci = C.nscr_leggi(C.leggi(repo, NSCR_LOGO))
    for i, e in enumerate(voci[:32 * 24]):
        t = e & 0x3FF
        if t == 0:
            continue
        sx, sy = t % 32, t // 32
        dx, dy = i % 32, i // 32
        for y in range(8):
            for x in range(8):
                v = lpix[(sy * 8 + y) * lw + sx * 8 + x]
                if v:
                    out[(dy * 8 + y) * W + dx * 8 + x] = v
    aw, ah, apix = r['autore']
    wt, ht, voci = C.nscr_leggi(C.leggi(repo, NSCR_AUTORE))
    for i, e in enumerate(voci[:32 * 24]):
        t, p = e & 0x3FF, e >> 12
        sx, sy = t % 32, t // 32
        dx, dy = i % 32, i // 32
        if sy >= ah // 8:
            continue
        for y in range(8):
            for x in range(8):
                v = apix[(sy * 8 + y) * aw + sx * 8 + x]
                if v:
                    out[(dy * 8 + y) * W + dx * 8 + x] = p * 16 + v
    return W, H, out

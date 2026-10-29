"""Blocco 4.4 — il «Sondaggio» del Pokégear (barra del Consenso, trama R-06; GFX-SONDAGGIO).

Lo schermo superiore del Pokégear è la cornice su GF_BG_LYR_SUB_0: tile pgear_gra_000000{36+t}.png e schermata
pgear_gra_000000{42+t}.NSCR, una coppia per ciascuno dei 6 temi t (src/application/pokegear/main/
overlay_100_021E5900.c, PokegearApp_LoadSkinGraphics), palette 13 della NCLR 24+t. Sotto la fascia
dell'orologio (righe 12–15) la cornice è vuota (tile 1): lì vanno la scritta «Sondaggio», la barra di 20
tacche e la percentuale. Le tile nuove stanno dall'indice 96 in poi (le schermate di HeartGold ne usano al
massimo 79); la parte fissa è scritta nella schermata, la parte che dipende dal Consenso la scrive il codice
(modifica E-GFX-04) con FillBgTilemapRect a ogni apertura del Pokégear e a ogni cambio di tema."""
import os

import comune44 as C

TEMI = 6
PAL = 13
RIGA_SCRITTA = 12       # righe 12–13: «Sondaggio» (cella del font alta 16)
RIGA_BARRA = 14
X_SCRITTA = 3
X0 = 4                  # prima tacca
SEGMENTI = 20
X_CIFRE = 26            # centinaia, decine, unità in 26–28, «%» in 29
T = dict(sfondo=96, vuoto=97, pieno=98, capo_sx=99, capo_dx=100, perc=101, cifra0=102, scritta=112)
SCRITTA = 'Sondaggio'
ALTEZZA = 32            # fogli di 256×32 pixel = 128 tile

# cifre 3×5 e «%» (righe dall'alto, '#' = inchiostro)
CIFRE = {
    '0': ['###', '#.#', '#.#', '#.#', '###'], '1': ['.#.', '##.', '.#.', '.#.', '###'],
    '2': ['###', '..#', '###', '#..', '###'], '3': ['###', '..#', '.##', '..#', '###'],
    '4': ['#.#', '#.#', '###', '..#', '..#'], '5': ['###', '#..', '###', '..#', '###'],
    '6': ['###', '#..', '###', '#.#', '###'], '7': ['###', '..#', '.#.', '.#.', '.#.'],
    '8': ['###', '#.#', '###', '#.#', '###'], '9': ['###', '#.#', '###', '..#', '###'],
    '%': ['#..#', '...#', '..#.', '.#..', '#..#'],
}


def png(rel_tema):
    return 'files/application/pokegear/pgear_gra/pgear_gra_%08d.png' % rel_tema


def ruoli(pal):
    """Indici della palette 13 per scuro, chiaro, accento, a partire dalla luminosità e dalla saturazione."""
    lum = lambda i: sum(pal[i])
    sat = lambda i: max(pal[i]) - min(pal[i])
    idx = list(range(1, 16))
    scuro = min(idx, key=lum)
    chiaro = max(idx, key=lum)
    accento = max((i for i in idx if i not in (scuro, chiaro)), key=lambda i: (sat(i), lum(i)))
    medio = sorted(idx, key=lum)[len(idx) // 2]
    return scuro, chiaro, accento, medio


def tile_nuove(sfondo, ruolo, font):
    """-> {indice: tile} per un tema."""
    scuro, chiaro, accento, medio = ruolo
    out = {T['sfondo']: [list(r) for r in sfondo]}

    def base():
        return [list(r) for r in sfondo]
    t = base()
    for x in range(8):
        t[1][x] = t[6][x] = scuro
        for y in range(2, 6):
            t[y][x] = medio if x != 7 else scuro
    out[T['vuoto']] = t
    t = base()
    for x in range(8):
        t[1][x] = t[6][x] = scuro
        for y in range(2, 6):
            t[y][x] = (chiaro if y == 2 else accento) if x != 7 else scuro
    out[T['pieno']] = t
    t = base()
    for y in range(1, 7):
        t[y][7] = scuro
    out[T['capo_sx']] = t
    t = base()
    for y in range(1, 7):
        t[y][0] = scuro
    out[T['capo_dx']] = t
    for k, ch in enumerate('0123456789%'):
        t = base()
        g = CIFRE[ch]
        ox = 2 if len(g[0]) == 3 else 1
        for y, riga in enumerate(g):
            for x, c in enumerate(riga):
                if c == '#':
                    t[1 + y][ox + x] = chiaro
                    if 2 + y < 8 and ox + x + 1 < 8 and (x + 1 >= len(riga) or riga[x + 1] != '#'):
                        t[2 + y][ox + x + 1] = scuro if t[2 + y][ox + x + 1] != chiaro else chiaro
        out[T['perc'] if ch == '%' else T['cifra0'] + k] = t
    # scritta «Sondaggio» su 2 righe di tile
    w = font.larghezza(SCRITTA)
    n = (w + 7) // 8
    W, H = n * 8, 16
    pix = []
    for y in range(H):
        for x in range(W):
            pix.append(sfondo[y % 8][x % 8])
    font.scrivi(pix, W, H, 0, 0, SCRITTA, chiaro, scuro)
    k = T['scritta']
    for ty in range(2):
        for tx in range(n):
            out[k] = [list(r) for r in C.tile_di(pix, W, tx, ty)]
            k += 1
    return out, n


def costruisci(repo):
    font = C.Font(repo)
    temi = []
    for t in range(TEMI):
        rel = png(36 + t)
        im = C.G.png_read(os.path.join(repo, *rel.split('/')))
        W, H = im['larghezza'], im['altezza']
        pix = list(im['pixel'])
        if H < ALTEZZA:
            # il foglio del tema 5 è alto 24 pixel (96 tile): sale a 32 come gli altri cinque (R-GFX-32)
            pix += [0] * (W * (ALTEZZA - H))
            H = ALTEZZA
        nt = (W // 8) * (H // 8)
        tile = [C.tile_di(pix, W, k % (W // 8), k // (W // 8)) for k in range(nt)]
        b_scr = C.leggi(repo, 'files/application/pokegear/pgear_gra/pgear_gra_%08d.NSCR' % (42 + t))
        wt, ht, voci = C.nscr_leggi(b_scr)
        usate = {v & 0x3FF for v in voci}
        if max(usate) >= T['vuoto']:
            raise C.Errore('tema %d: la cornice usa già la tile %d' % (t, max(usate)))
        _, col = C.nclr_leggi(C.leggi(repo, 'files/application/pokegear/pgear_gra/pgear_gra_%08d.NCLR' % (24 + t)))
        pal = col[PAL * 16:PAL * 16 + 16]
        ruolo = ruoli(pal)
        import collections
        zona = collections.Counter(voci[y * wt + x] & 0x3FF for y in range(RIGA_SCRITTA, RIGA_BARRA + 2)
                                   for x in range(2, 30))
        sfondo = zona.most_common(1)[0][0]
        nuove, n = tile_nuove(tile[sfondo], ruolo, font)
        if T['scritta'] + 2 * n > nt:
            raise C.Errore('tema %d: la scritta non entra nel foglio' % t)
        for k, tt in nuove.items():
            tile[k] = tt
        for k, tt in enumerate(tile):
            for y in range(8):
                for x in range(8):
                    pix[(k // (W // 8) * 8 + y) * W + (k % (W // 8)) * 8 + x] = tt[y][x]
        voci = list(voci)
        for ty in range(2):
            for tx in range(n):
                voci[(RIGA_SCRITTA + ty) * wt + X_SCRITTA + tx] = C.voce(T['scritta'] + ty * n + tx, PAL)
        for y in range(RIGA_SCRITTA, RIGA_BARRA + 1):
            for x in range(X_SCRITTA, X_CIFRE + 4):
                voci[y * wt + x] = C.voce(T['sfondo'], PAL)
        for ty in range(2):
            for tx in range(n):
                voci[(RIGA_SCRITTA + ty) * wt + X_SCRITTA + tx] = C.voce(T['scritta'] + ty * n + tx, PAL)
        voci[RIGA_BARRA * wt + X0 - 1] = C.voce(T['capo_sx'], PAL)
        for i in range(SEGMENTI):
            voci[RIGA_BARRA * wt + X0 + i] = C.voce(T['vuoto'], PAL)
        voci[RIGA_BARRA * wt + X0 + SEGMENTI] = C.voce(T['capo_dx'], PAL)
        voci[RIGA_BARRA * wt + X_CIFRE + 2] = C.voce(T['cifra0'], PAL)
        voci[RIGA_BARRA * wt + X_CIFRE + 3] = C.voce(T['perc'], PAL)
        temi.append(dict(tema=t, png=rel, png_pix=pix, W=W, H=H,
                         palette_png=[tuple(c) for c in im['palette']],
                         nscr_rel='files/application/pokegear/pgear_gra/pgear_gra_%08d.NSCR' % (42 + t),
                         nscr=C.nscr_patch(b_scr, voci), voci=voci, wt=wt, ht=ht, colori=col,
                         ruoli=dict(zip(('scuro', 'chiaro', 'accento', 'medio'), ruolo)), tile=tile,
                         sfondo_hg=sfondo))
    return dict(temi=temi, tile=T, codice=codice())


def codice():
    """Testo C della modifica E-GFX-04 (funzione nuova e chiamata)."""
    return '''// Trinacria (blocco 4.4, E-GFX-04): il «Sondaggio», barra del Consenso sullo schermo superiore (trama R-06).
// Tile 96–125 dei fogli pgear_gra_00000036–41 (tools/grafica/4.4/sondaggio44.py), palette 13.
#define SONDAGGIO_PAL         %d
#define SONDAGGIO_RIGA        %d
#define SONDAGGIO_X0          %d
#define SONDAGGIO_SEGMENTI    %d
#define SONDAGGIO_X_CIFRE     %d
#define SONDAGGIO_TILE_SFONDO %d
#define SONDAGGIO_TILE_VUOTO  %d
#define SONDAGGIO_TILE_PIENO  %d
#define SONDAGGIO_TILE_CIFRA0 %d

static void Trinacria_PokegearSondaggio(PokegearAppData *pokegearApp) {
    u16 consenso = *Save_VarsFlags_GetVarAddr(pokegearApp->saveVarsFlags, VAR_TRINACRIA_CONSENSO);
    u8 pieni;
    u8 i;

    if (consenso > 100) {
        consenso = 100;
    }
    pieni = (consenso * SONDAGGIO_SEGMENTI + 50) / 100;
    for (i = 0; i < SONDAGGIO_SEGMENTI; i++) {
        FillBgTilemapRect(pokegearApp->bgConfig, GF_BG_LYR_SUB_0, i < pieni ? SONDAGGIO_TILE_PIENO : SONDAGGIO_TILE_VUOTO, SONDAGGIO_X0 + i, SONDAGGIO_RIGA, 1, 1, SONDAGGIO_PAL);
    }
    FillBgTilemapRect(pokegearApp->bgConfig, GF_BG_LYR_SUB_0, consenso >= 100 ? SONDAGGIO_TILE_CIFRA0 + 1 : SONDAGGIO_TILE_SFONDO, SONDAGGIO_X_CIFRE, SONDAGGIO_RIGA, 1, 1, SONDAGGIO_PAL);
    FillBgTilemapRect(pokegearApp->bgConfig, GF_BG_LYR_SUB_0, consenso >= 10 ? SONDAGGIO_TILE_CIFRA0 + (consenso / 10) %% 10 : SONDAGGIO_TILE_SFONDO, SONDAGGIO_X_CIFRE + 1, SONDAGGIO_RIGA, 1, 1, SONDAGGIO_PAL);
    FillBgTilemapRect(pokegearApp->bgConfig, GF_BG_LYR_SUB_0, SONDAGGIO_TILE_CIFRA0 + consenso %% 10, SONDAGGIO_X_CIFRE + 2, SONDAGGIO_RIGA, 1, 1, SONDAGGIO_PAL);
}
''' % (PAL, RIGA_BARRA, X0, SEGMENTI, X_CIFRE, T['sfondo'], T['vuoto'], T['pieno'], T['cifra0'])


def simula(tema, consenso):
    """Voci della schermata dopo Trinacria_PokegearSondaggio (per l'anteprima e il collaudo)."""
    v = list(tema['voci'])
    wt = tema['wt']
    c = min(consenso, 100)
    pieni = (c * SEGMENTI + 50) // 100
    for i in range(SEGMENTI):
        v[RIGA_BARRA * wt + X0 + i] = C.voce(T['pieno'] if i < pieni else T['vuoto'], PAL)
    v[RIGA_BARRA * wt + X_CIFRE] = C.voce(T['cifra0'] + 1 if c >= 100 else T['sfondo'], PAL)
    v[RIGA_BARRA * wt + X_CIFRE + 1] = C.voce(T['cifra0'] + (c // 10) % 10 if c >= 10 else T['sfondo'], PAL)
    v[RIGA_BARRA * wt + X_CIFRE + 2] = C.voce(T['cifra0'] + c % 10, PAL)
    return v

"""Blocco 4.4 — schermata copyright all'avvio (GFX-COPYRIGHT).

In HeartGold è la prima schermata del filmato (src/intro_movie_scene_1.c, 30 frame + dissolvenza di 60):
tile gs_opening_00000005.NCGR (160 tile a 4 bit, compresse LZ dal build) e schermata
gs_opening_00000013.NSCR su GF_BG_LYR_MAIN_0, colori della palette gs_opening_00000001.NCLR. Mostra
«GAME FREAK presents» e l'avviso ESRB. Trinacria ci scrive le quattro righe decise dal Modulo 1 §9.2, col
font del gioco, bianco con l'ombra grigia della stessa palette 2 che l'avviso ESRB usa già."""
import comune44 as C

NCGR = 'files/demo/opening/gs_opening/gs_opening_00000005.NCGR'
NSCR = 'files/demo/opening/gs_opening/gs_opening_00000013.NSCR'
NCLR = 'files/demo/opening/gs_opening/gs_opening_00000001.NCLR'
PAL = 2
RIGHE = [            # (testo, riga di tile della cima della cella del font)
    ('Pokémon Trinacria', 7),
    ('© 2026 atrisorb', 10),
    ('Progetto amatoriale non ufficiale.', 14),
    ('Pokémon © Nintendo / Creatures / GAME FREAK', 18),
]


def costruisci(repo):
    font = C.Font(repo)
    b_ncgr, b_nscr = C.leggi(repo, NCGR), C.leggi(repo, NSCR)
    g = C.ncgr_leggi(b_ncgr)
    wt, ht, voci = C.nscr_leggi(b_nscr)
    _, colori = C.nclr_leggi(C.leggi(repo, NCLR))
    pal = colori[PAL * 16:PAL * 16 + 16]
    lum = sorted(range(1, 16), key=lambda i: sum(pal[i]))
    ink, ombra = lum[-1], lum[len(lum) // 2]
    W, H = wt * 8, ht * 8
    pix = [0] * (W * H)
    larghezze = {}
    for testo, riga in RIGHE:
        w = font.larghezza(testo)
        if w > W - 8:
            raise C.Errore('copyright: «%s» misura %d px' % (testo, w))
        larghezze[testo] = w
        font.scrivi(pix, W, H, (W - w) // 2, riga * 8, testo, ink, ombra)
    fog = C.Foglio(len(g['tile']), flip=False, prime=[[[0] * 8 for _ in range(8)]])
    nuove = []
    for ty in range(ht):
        for tx in range(wt):
            nuove.append(fog.aggiungi(C.tile_di(pix, W, tx, ty), PAL))
    tile = list(fog.tile) + [[[0] * 8 for _ in range(8)]] * (len(g['tile']) - len(fog.tile))
    return dict(ncgr=C.ncgr_patch(b_ncgr, tile), nscr=C.nscr_patch(b_nscr, nuove), tile_usate=len(fog.tile),
                tile_file=len(g['tile']), pix=pix, W=W, H=H, colori=colori, larghezze=larghezze,
                ink=PAL * 16 + ink, ombra=PAL * 16 + ombra)

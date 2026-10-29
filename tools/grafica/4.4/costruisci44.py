"""Blocco 4.4 — costruisce titolo, copyright, Pokégear e Sondaggio in build/grafica/4.4 (R-GFX-17).

    python -I tools/grafica/4.4/costruisci44.py [--repo R] [--rom ROM]

Scrive i file nuovi (PNG, NCLR, NSCR, NCGR, la tabella del Volo in C, il banco msg_0273), le anteprime e
manifesto.json, che `trinacria_gfx.py applica --blocchi 4.4` porta nel repository: file sostituiti interi,
la tabella sLocationSpecs dentro pokegear_map.c e le modifiche E-GFX-02…04 come sostituzioni esatte.
Gli originali si leggono dal repository; se è già modificato serve --rom (riconosciuti dallo SHA-1).
Ultima riga: GRAFICA_OK oppure GRAFICA_FAILED. Solo libreria standard, gira in pochi secondi."""
import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import comune44 as C          # noqa: E402
import dati44                 # noqa: E402
import pokegear44             # noqa: E402
import piantine44             # noqa: E402
import copyright44            # noqa: E402
import titolo44               # noqa: E402
import sondaggio44            # noqa: E402
import testi44                # noqa: E402

G = C.G
OUT = C.OUT
errors = []
MSG = 'files/msgdata/msg/msg_0273.json'
VOLO_C = 'src/application/pokegear/map/overlay_101_021F79B4.c'
LUOGHI_C = 'src/application/pokegear/map/pokegear_map.c'
REGIONE_C = 'src/application/pokegear/main/overlay_100_021E5900.c'
VOLO_REGIONE_C = 'src/application/pokegear/map/overlay_101_021E9270.c'
PRIMO_TESTO = 10            # msg_0273_00010: prima descrizione (come HeartGold)
LARGHEZZA_DESCRIZIONE = 224
LARGHEZZA_REGIONE = 38


def err(m):
    errors.append(m)
    print('ERRORE ' + m)


class Repo:
    """Originali: dal repository se intatti, altrimenti dalla ROM (--rom)."""

    def __init__(self, repo, rom=None):
        self.repo, self.rom = repo, rom

    def leggi(self, rel):
        return C.leggi(self.repo, rel)


def scrivi(rel_build, b):
    p = os.path.join(OUT, *rel_build.split('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'wb') as fh:
        fh.write(b if isinstance(b, bytes) else b.encode('utf-8'))
    return rel_build


def stessa_forma(nome, vecchio, nuovo):
    if len(vecchio) != len(nuovo) or vecchio[:16] != nuovo[:16]:
        err('K22 %s: lunghezza o intestazione diverse dall\'originale (%d / %d byte)' % (nome, len(vecchio), len(nuovo)))


def png_nuovo(repo, rel, w, h, palette, pix, bpp, come=True):
    tmp = os.path.join(OUT, 'file', *rel.split('/'))
    C.salva_png(tmp, w, h, palette, pix, bpp)
    orig = os.path.join(repo, *rel.split('/'))
    for c, m in G.png_check(tmp, come=orig if come else None, bpp=bpp):
        err('%s %s: %s' % (c, rel, m))
    return 'file/' + rel


def c_volo(volo, dati):
    righe = []
    for v, r in zip(volo, dati.voli):
        righe.append('    { %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d },' % (
            r['mapIDforName'], r['mapIDforWarp'], r['flypoint'], v['unk_05'], r['x'], r['y'],
            v['unk170SrcX'], v['unk170SrcY'], r['width'], r['height'], v['unk170DestWidth'],
            v['unk170DestHeight'], v['unk170DestX'], v['unk170DestY']))
    return ('#include "global.h"\n\n#include "constants/maps.h"\n\n'
            '#include "application/pokegear/map/pokegear_map_internal.h"\n\n'
            '// Pokémon Trinacria (blocco 4.4): punti di volo sulla mappa della Sicilia. x, y = cella della matrice 0;\n'
            '// unk_05 = numero della toppa «non visitata», unk170* = dove sta nella schermata pgmap_gra_00000011 e\n'
            '// come si posa attorno alla città (tools/grafica/4.4/pokegear44.py).\n'
            'const MapFlypointParam gMapFlypointParams[] = {\n' + '\n'.join(righe) + '\n};\n')


def c_luoghi(luoghi):
    out = ['const PokegearMapLocationSpec sLocationSpecs[PGMAP_NUM_LOCATIONS] = {']
    for L in luoghi:
        out += ['    {',
                '     .mapId = %s,' % L['mapId'],
                '     .x = %d,' % L['x'],
                '     .y = %d,' % L['y'],
                '     .width = %d,' % L['width'],
                '     .height = %d,' % L['height'],
                '     .objXoffset = %d,' % L['objXoffset'],
                '     .objYoffset = %d,' % L['objYoffset'],
                '     .flavorText = msg_0273_%05d,' % L['testo'],
                '     .tilemapUnk174BlockID = %d,' % L['piantina'],
                '     .tilemapUnk170SrcX = %d,' % L['tilemapUnk170SrcX'],
                '     .tilemapUnk170SrcY = %d,' % L['tilemapUnk170SrcY'],
                '     .tilemapUnk170DestWidth = %d,' % L['tilemapUnk170DestWidth'],
                '     .tilemapUnk170DestHeight = %d,' % L['tilemapUnk170DestHeight'],
                '     },']
    out.append('};')
    return '\n'.join(out)


def msg_0273(orig, luoghi, font):
    j = json.loads(orig)
    msgs = j['messages']
    msgs[0]['en_US'] = testi44.REGIONI['est']
    msgs[1]['en_US'] = testi44.REGIONI['ovest']
    for k in (0, 1):
        if font.larghezza(msgs[k]['en_US']) > LARGHEZZA_REGIONE:
            err('T01 nome di regione «%s» oltre %d px' % (msgs[k]['en_US'], LARGHEZZA_REGIONE))
    usati = set()
    for L in luoghi:
        a, b = testi44.DESCRIZIONI.get(L['mapId'], (None, None))
        if a is None:
            err('T02 manca la descrizione di %s' % L['mapId'])
            continue
        for riga in (a, b):
            if font.larghezza(riga) > LARGHEZZA_DESCRIZIONE:
                err('T03 %s: «%s» misura %d px > %d' % (L['mapId'], riga, font.larghezza(riga), LARGHEZZA_DESCRIZIONE))
        m = msgs[L['testo']]
        m.pop('garbage', None)
        m['en_US'] = [a + '\n', b]
        usati.add(L['testo'])
    for k in range(PRIMO_TESTO, len(msgs)):
        if k not in usati:
            msgs[k].pop('garbage', None)
            msgs[k]['en_US'] = ''
    return json.dumps(j, ensure_ascii=False, indent=2) + '\n'


def sostituzioni(repo):
    """Modifiche di codice E-GFX-02…04: (id, file, cerca, sostituisci). `cerca` dev'esserci una volta sola."""
    reg = C.leggi(repo, REGIONE_C).decode('utf-8')
    a = reg.index('PokegearRegion Pokegear_RegionFromCoords(u16 x, u16 y) {')
    b = reg.index('\n}\n', a) + 3
    e02 = (reg[a:b],
           'PokegearRegion Pokegear_RegionFromCoords(u16 x, u16 y) {\n'
           '    // Trinacria (blocco 4.4, E-GFX-02): colonna >= 24 della matrice 0 = Sicilia orientale (lato Kanto),\n'
           '    // il resto = Sicilia occidentale (lato Johto); niente casi speciali di Monte Argento e Altopiano Blu (trama R-09.6)\n'
           '    if (x >= %d) {\n'
           '        return POKEGEAR_REGION_KANTO;\n'
           '    }\n'
           '    return POKEGEAR_REGION_JOHTO;\n'
           '}\n' % dati44.COLONNA_EST)
    vr = C.leggi(repo, VOLO_REGIONE_C).decode('utf-8')
    a = vr.index('BOOL ov101_021EA7E4(PokegearMapAppData *mapApp, u16 x, u16 y) {')
    b = vr.index('\n}\n', a) + 3
    e03 = (vr[a:b],
           'BOOL ov101_021EA7E4(PokegearMapAppData *mapApp, u16 x, u16 y) {\n'
           '    // Trinacria (blocco 4.4, E-GFX-03): il Volo vale su tutta l\'isola, fra Sicilia orientale e occidentale\n'
           '    return TRUE;\n'
           '}\n')
    chiamata = ('skinIdx + NARC_pgear_gra_pgear_gra_00000042_NSCR, GF_BG_LYR_SUB_0, GF_BG_GFX_TYPE_SCRN, 0, 0);\n')
    e04a = (chiamata, chiamata + '    Trinacria_PokegearSondaggio(pokegearApp);\n')
    testa = 'void PokegearApp_LoadSkinGraphics(PokegearAppData *pokegearApp, u8 skinIdx) {\n'
    e04b = (testa, sondaggio44.codice() + '\n' + testa)
    inc = '#include "map_header.h"\n'
    e04c = (inc, '#include "constants/vars.h"\n\n' + inc + '#include "save_vars_flags.h"\n')
    out = [('E-GFX-02', REGIONE_C) + e02, ('E-GFX-03', VOLO_REGIONE_C) + e03,
           ('E-GFX-04', REGIONE_C) + e04c, ('E-GFX-04', REGIONE_C) + e04b, ('E-GFX-04', REGIONE_C) + e04a]
    testi = {}
    for ident, f, cerca, sost in out:
        t = testi.setdefault(f, C.leggi(repo, f).decode('utf-8'))
        if t.count(cerca) != 1:
            err('K23 %s: il testo da sostituire in %s compare %d volte' % (ident, f, t.count(cerca)))
        else:
            testi[f] = t.replace(cerca, sost)
    return [dict(id=i, file=f, cerca=c, sostituisci=s) for i, f, c, s in out]


def prova_forma(repo):
    """R-GFX-29: ogni NCLR, NSCR e NCGR lineare di files/demo e files/application/pokegear letto e riscritto
    con le funzioni di comune44.py dev'essere identico. -> (identici, provati)."""
    n = ok = 0
    for base in ('files/demo', 'files/application/pokegear'):
        for radice, _, fs in os.walk(os.path.join(repo, *base.split('/'))):
            for f in sorted(fs):
                b = open(os.path.join(radice, f), 'rb').read()
                e = f.rsplit('.', 1)[-1]
                if e == 'NCLR':
                    r = C.nclr_patch(b, C.nclr_leggi(b)[1])
                elif e == 'NSCR':
                    r = C.nscr_patch(b, C.nscr_leggi(b)[2])
                elif e == 'NCGR':
                    g = C.ncgr_leggi(b)
                    if g['tiled'] or g['mapping']:
                        continue
                    r = C.ncgr_patch(b, g['tile'])
                else:
                    continue
                n += 1
                if r == b:
                    ok += 1
                else:
                    err('K22 %s: letto e riscritto non è identico' % f)
    return ok, n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo')
    ap.add_argument('--rom')
    a = ap.parse_args(argv)
    repo = G.find_repo(a.repo)
    sys.stdout.reconfigure(errors='backslashreplace')
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    font = C.Font(repo)
    man = dict(blocco='4.4', tipo='file', file=[], blocchi_testo=[], sostituzioni=[], anteprime=[])
    ok, n = prova_forma(repo)
    man['prova_forma'] = dict(identici=ok, provati=n)
    print('forma invariata: %d file su %d letti e riscritti identici' % (ok, n))

    def registra(dest, sorgente, nota):
        orig = C.leggi(repo, dest)
        nuovo = open(os.path.join(OUT, *sorgente.split('/')), 'rb').read()
        man['file'].append(dict(destinazione=dest, sorgente=sorgente, sha1_hg=G.sha1(orig), sha1_nuovo=G.sha1(nuovo),
                                byte=len(nuovo), nota=nota))

    def anteprima(nome, w, h, pix, colori, scala=2):
        p = os.path.join(OUT, 'anteprime', nome + '.png')
        C.anteprima(p, w, h, pix, colori, scala)
        man['anteprime'].append('anteprime/%s.png' % nome)

    # 1. copyright
    cp = copyright44.costruisci(repo)
    for rel, b, nota in ((copyright44.NCGR, cp['ncgr'], 'tile della schermata copyright'),
                         (copyright44.NSCR, cp['nscr'], 'schermata copyright')):
        stessa_forma(rel, C.leggi(repo, rel), b)
        registra(rel, scrivi('file/' + rel, b), nota)
    g = C.ncgr_leggi(cp['ncgr'])
    wt, ht, v = C.nscr_leggi(cp['nscr'])
    w, h, pix = C.schermata_pixel(g['tile'], v, wt, ht, cp['colori'], False)
    anteprima('copyright', w, 192, pix[:w * 192], cp['colori'])
    print('copyright: %d tile su %d' % (cp['tile_usate'], cp['tile_file']))

    # 2. titolo
    ti = titolo44.costruisci(repo)
    stessa_forma(titolo44.NCLR, C.leggi(repo, titolo44.NCLR), ti['nclr'])
    registra(titolo44.NCLR, scrivi('file/' + titolo44.NCLR, ti['nclr']), 'palette del titolo')
    for rel, (w, h, pix), bpp, pal, nota in (
            (titolo44.LOGO, ti['logo'], 8, ti['colori'], 'logo «Pokémon Trinacria» con la triscele'),
            (titolo44.FONDO, ti['fondo'], 8, ti['colori'], 'alba sull’Etna e sullo Ionio'),
            (titolo44.AUTORE, ti['autore'], 4, ti['colori'][112:128], 'riga dell’autore')):
        registra(rel, png_nuovo(repo, rel, w, h, pal, pix, bpp), nota)
    w, h, pix = titolo44.schermo(repo, ti)
    anteprima('titolo', w, h, pix, ti['colori'])
    print('titolo: fondo %d colori, logo %d' % (ti['colori_fondo'], ti['colori_logo']))

    # 3. Pokégear: mappa, piantine, tabelle
    d = dati44.Dati()
    pg = pokegear44.costruisci(d)
    pi = piantine44.costruisci()
    rel_nclr = 'files/application/pokegear/map/pgmap_gra/pgmap_gra_%08d.NCLR'
    _, col20 = C.nclr_leggi(C.leggi(repo, rel_nclr % 20))
    _, col14 = C.nclr_leggi(C.leggi(repo, rel_nclr % 14))
    fw, fh, fpix = pg['foglio'].immagine(64, 12)
    rel = 'files/application/pokegear/map/pgmap_gra/pgmap_gra_00000010.png'
    registra(rel, png_nuovo(repo, rel, fw, fh, col20, fpix, 8), 'tile della mappa della Sicilia')
    rel = 'files/application/pokegear/map/pgmap_gra/pgmap_gra_00000011.NSCR'
    b = C.nscr_patch(C.leggi(repo, rel), pg['schermata'])
    stessa_forma(rel, C.leggi(repo, rel), b)
    registra(rel, scrivi('file/' + rel, b), 'mappa, toppe e cornici (unk_170)')
    fw, fh, fpix = pi['foglio'].immagine(32, 18)
    rel = 'files/application/pokegear/map/pgmap_gra/pgmap_gra_00000012.png'
    registra(rel, png_nuovo(repo, rel, fw, fh, col14[32:48], fpix, 4), 'tile delle piantine')
    rel = 'files/application/pokegear/map/pgmap_gra/pgmap_gra_00000013.NSCR'
    b = C.nscr_patch(C.leggi(repo, rel), pi['schermata'])
    stessa_forma(rel, C.leggi(repo, rel), b)
    registra(rel, scrivi('file/' + rel, b), '20 piantine (unk_174)')
    for k, L in enumerate(pg['luoghi']):
        L['testo'] = PRIMO_TESTO + k
        L['piantina'] = pi['blocchi'].get(L['mapId'], 0)
    registra(VOLO_C, scrivi('file/' + VOLO_C, c_volo(pg['volo'], d)), 'tabella del Volo (gMapFlypointParams)')
    registra(MSG, scrivi('file/' + MSG, msg_0273(C.leggi(repo, MSG).decode('utf-8'), pg['luoghi'], font)),
             'nomi delle regioni e descrizioni dei luoghi')
    src = C.leggi(repo, LUOGHI_C).decode('utf-8')
    inizio = 'const PokegearMapLocationSpec sLocationSpecs[PGMAP_NUM_LOCATIONS] = {'
    if src.count(inizio) != 1:
        err('K23 %s: inizio di sLocationSpecs non trovato' % LUOGHI_C)
    man['blocchi_testo'].append(dict(file=LUOGHI_C, inizio=inizio, fine='\n};\n', testo=c_luoghi(pg['luoghi']) + '\n',
                                     nota='tabella dei 100 luoghi (sLocationSpecs)'))
    man['sostituzioni'] = sostituzioni(repo)
    w, h, pix = C.schermata_pixel(pg['foglio'].tile, pg['schermata'], 64, 64, col20, True)
    anteprima('pokegear_schermata', w, h, pix, col20)
    anteprima('pokegear_mappa', 376, 160, [pix[y * w + x] for y in range(160) for x in range(376)], col20, 3)
    w, h, pix = C.schermata_pixel(pi['foglio'].tile, pi['schermata'], 32, 35, col14, False)
    anteprima('pokegear_piantine', w, h, pix, col14)
    print('Pokégear: %d tile di mappa su %d, %d luoghi, %d cornici, %d piantine (%d tile su %d)'
          % (len(pg['foglio'].tile), pokegear44.TILE_MAX, len(pg['luoghi']), pg['cornici'], len(pi['blocchi']),
             len(pi['foglio'].tile), piantine44.TILE_MAX))

    # 4. Sondaggio
    so = sondaggio44.costruisci(repo)
    for t in so['temi']:
        registra(t['png'], png_nuovo(repo, t['png'], t['W'], t['H'], t['palette_png'], t['png_pix'], 4,
                                     come=t['H'] == 32 and t['tema'] != 5), 'cornice col Sondaggio, tema %d' % t['tema'])
        stessa_forma(t['nscr_rel'], C.leggi(repo, t['nscr_rel']), t['nscr'])
        registra(t['nscr_rel'], scrivi('file/' + t['nscr_rel'], t['nscr']), 'schermata della cornice, tema %d' % t['tema'])
        w, h, pix = C.schermata_pixel(t['tile'], sondaggio44.simula(t, (7, 23, 37, 49, 60, 100)[t['tema']]),
                                      t['wt'], t['ht'], t['colori'], False)
        anteprima('sondaggio_tema%d' % t['tema'], w, h, pix, t['colori'])

    # 5. dati per il documento
    man['pokegear'] = dict(volo=pg['volo'], luoghi=[{k: v for k, v in L.items()} for L in pg['luoghi']],
                           escluse=pg['escluse'], tile_mappa=len(pg['foglio'].tile), cornici=pg['cornici'],
                           piantine=[dict(blocco=b, mappa=s, cella=pi['celle'][s]) for s, b in sorted(pi['blocchi'].items(), key=lambda x: x[1])],
                           tile_piantine=len(pi['foglio'].tile))
    man['copyright'] = dict(tile=cp['tile_usate'], righe=[dict(testo=t, px=cp['larghezze'][t]) for t, _ in copyright44.RIGHE])
    man['titolo'] = dict(colori_fondo=ti['colori_fondo'], colori_logo=ti['colori_logo'], autore=titolo44.TESTO_AUTORE)
    man['sondaggio'] = dict(tile=so['tile'], temi=[dict(tema=t['tema'], ruoli=t['ruoli'], sfondo_hg=t['sfondo_hg'])
                                                   for t in so['temi']])
    scrivi('manifesto.json', json.dumps(man, ensure_ascii=False, indent=1))
    print('%d file, %d blocchi di testo, %d sostituzioni, %d anteprime'
          % (len(man['file']), len(man['blocchi_testo']), len(man['sostituzioni']), len(man['anteprime'])))
    print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

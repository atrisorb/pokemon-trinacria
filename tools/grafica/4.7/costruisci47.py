"""Blocco 4.6 — costruisce le immagini di lotta e la grafica delle transizioni in build/grafica/4.6 (R-GFX-17).

    python -I tools/grafica/4.6/costruisci46.py [--repo R]

1. prova di forma: tutte le immagini degli allenatori di HeartGold lette e riscritte identiche;
2. immagini frontali (files/a/0/5/8) delle classi del registro 2.5 e del protagonista, dorsi (files/a/0/0/6) dei
   compagni e del protagonista, disegnati da figura46.py con le schede del 4.5;
3. transizioni (files/a/1/0/9): ritratti dei Segretari, dei Campioni dell'ARS, del Presidente, delle 5 classi di
   «U Sistema» con transizione propria e del protagonista; il timbro di «U Sistema» al posto della «R»;
4. tabelle delle transizioni (asm/overlay_115.s, asm/overlay_117.s): ID dell'allenatore di cui si scrive il nome
   (modifica E-GFX-05, sostituzioni esatte nel manifesto);
5. anteprime e manifesto.json per `trinacria_gfx.py applica --blocchi 4.6`.
Ultima riga: GRAFICA_OK oppure GRAFICA_FAILED. Solo libreria standard."""
import argparse
import json
import os
import re
import shutil
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import comune46 as C          # noqa: E402
import figura46 as F          # noqa: E402
import schede46 as S          # noqa: E402

G = C.G
C44 = C.C44
OUT = C.OUT
REGISTRO = os.path.join(C.PROJ, 'docs', 'MODULO_2', '2.5_TRAINERS_SPRITES_FLY_SEQ.json')
OV115 = 'asm/overlay_115.s'
OV117 = 'asm/overlay_117.s'
TRAINERS_JSON = 'files/poketool/trainer/trainers.json'
FONDO = (214, 230, 206)
errors = []


def err(m):
    errors.append(m)
    print('ERRORE ' + m)


def scrivi(rel_build, b):
    p = os.path.join(OUT, *rel_build.split('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'wb') as fh:
        fh.write(b if isinstance(b, bytes) else b.encode('utf-8'))
    return rel_build


# ------------------------------------------------------------------------------------------ anteprime

def foglio(path, righe, scala=2, spazio=4):
    """righe = [(lista di (w, h, pix), palette di 16 colori)]: una riga per voce, immagini affiancate."""
    W = max(sum(w + spazio for w, _, _ in imgs) for imgs, _ in righe) * scala
    alt = [max(h for _, h, _ in imgs) for imgs, _ in righe]
    H = (sum(alt) + spazio * len(righe)) * scala
    pix = [0] * (W * H)
    pal = [FONDO]
    y0 = 0
    for (imgs, colori), hr in zip(righe, alt):
        base = len(pal) - 1
        pal += list(colori[1:16])
        x0 = 0
        for w, h, p in imgs:
            for y in range(h):
                for x in range(w):
                    c = p[y * w + x]
                    if c:
                        for dy in range(scala):
                            row = ((y0 + y) * scala + dy) * W + (x0 + x) * scala
                            for dx in range(scala):
                                pix[row + dx] = base + c
            x0 += w + spazio
        y0 += hr + spazio
    if len(pal) > 256:
        raise C.Errore('troppe palette in un foglio')
    C44.salva_png(path, W, H, pal, pix, bpp=8)


# ------------------------------------------------------------------------------------- tabelle asm

def blocchi_rodata(testo):
    """Blocchi di dati dopo .rodata: [(etichetta, testo esatto del blocco, byte)]."""
    out = []
    righe = testo.split('\n')
    try:
        i = righe.index('\t.rodata')
    except ValueError:
        return out
    cur = None
    for r in righe[i + 1:]:
        m = re.match(r'^(\w+):', r)
        if m:
            cur = [m.group(1), [r], []]
            out.append(cur)
            continue
        if cur is not None and r.startswith('\t.byte '):
            cur[1].append(r)
            cur[2] += [int(v, 16) for v in r[len('\t.byte '):].split(',')]
        elif cur is not None and r.strip() == '' and len(cur[1]) > 1:
            cur = None
    return [(e, '\n'.join(t), bytes(b)) for e, t, b in out if b]


def con_byte(blocco, nuovi):
    """Lo stesso testo del blocco coi byte nuovi (stesso numero di byte per riga)."""
    righe = blocco.split('\n')
    out, k = [righe[0]], 0
    for r in righe[1:]:
        n = len(r[len('\t.byte '):].split(','))
        out.append('\t.byte ' + ', '.join('0x%02X' % v for v in nuovi[k:k + n]))
        k += n
    return '\n'.join(out)


def u16(b, o):
    return b[o] | (b[o + 1] << 8)


def tabelle_transizioni(repo):
    """-> lista di voci dict(file, etichetta, blocco, byte, offset_id, id_hg, ritratto=(NCLR, NCGR, NCER, NANR))."""
    voci = []
    for rel in (OV115, OV117):
        testo = C.leggi(repo, rel).decode('utf-8')
        for et, blocco, b in blocchi_rodata(testo):
            if rel == OV115 and len(b) == 20 and b[:4] == bytes((0x00, 0x60, 0x0D, 0x00)):
                voci.append(dict(file=rel, etichetta=et, blocco=blocco, byte=b, offset_id=4, id_hg=u16(b, 4),
                                 classe_hg=u16(b, 8), ritratto=tuple(b[12:16]), tipo='capo'))
            elif rel == OV115 and len(b) == 8 and b[1] == 0:
                n = b[0]
                voci.append(dict(file=rel, etichetta=et, blocco=blocco, byte=b, offset_id=6, id_hg=u16(b, 6),
                                 classe_hg=u16(b, 4), ritratto=(n, n + 1, n + 2, n + 3), tipo='lega'))
            elif rel == OV117 and len(b) == 8 and list(b[:4]) == [b[0] + k for k in range(4)]:
                voci.append(dict(file=rel, etichetta=et, blocco=blocco, byte=b, offset_id=4, id_hg=u16(b, 4),
                                 classe_hg=None, ritratto=tuple(b[:4]), tipo='esecutivo'))
    return voci


# ---------------------------------------------------------------------------------------- schermate

def rendi_schermata(files, i_scr, tiles):
    wt, ht, voci = C44.nscr_leggi(files[i_scr])
    W, H = wt * 8, ht * 8
    pix = [None] * (W * H)
    for i, e in enumerate(voci):
        t = C44.capovolta(tiles[e & 0x3FF], e >> 10 & 1, e >> 11 & 1)
        p = e >> 12
        bx, by = i % wt * 8, i // wt * 8
        for y in range(8):
            for x in range(8):
                v = t[y][x]
                pix[(by + y) * W + bx + x] = None if v == 0 else p * 16 + v
    return W, H, pix


def emblema_su(pix, W, H, cx, cy, r, pieno, bordo, riempi=True):
    em = F.emblema(W, H, cx, cy, r, pieno=riempi)
    for x, y in em['pieno']:
        pix[y * W + x] = pieno
    for x, y in em['bordo']:
        pix[y * W + x] = bordo
    return em


def schermate_r(files):
    """Le 5 schermate dello sfondo delle transizioni degli esecutivi (NCLR 215, NCGR 216, NSCR 217–221): la «R»
    di 218, 220 e 221 diventa il timbro di «U Sistema», 217 e 219 restano uguali; poi le tile si rifanno tutte."""
    colori = C44.nclr_leggi(files[215])[1]
    tiles = C.tile4(C.ncgr_byte(files[216]))
    sch = {i: rendi_schermata(files, i, tiles) for i in range(217, 222)}
    W, H, p220 = sch[220]
    cnt = Counter(p220)
    fondo = cnt.most_common(1)[0][0]
    r_pix = [(i % W, i // W) for i, v in enumerate(p220) if v != fondo]
    xs, ys = [q[0] for q in r_pix], [q[1] for q in r_pix]
    bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
    dentro = Counter(v for v in p220 if v != fondo)
    (pieno, _), (bordo, _) = dentro.most_common(2)[:2]
    cx, cy = (bx0 + bx1) / 2 + 0.5, (by0 + by1) / 2 + 0.5
    r = max(bx1 - bx0, by1 - by0) / 2 + 1
    zona = {(x, y) for y in range(by0 - 2, by1 + 3) for x in range(bx0 - 2, bx1 + 3)}
    nuove = {}
    for i, (W, H, p) in sch.items():
        q = list(p)
        if i in (218, 220):
            # fondo = colore più usato della schermata; la «R» = i due colori più usati nella sua zona
            f_i = Counter(p).most_common(1)[0][0]
            cz = Counter(p[y * W + x] for x, y in zona if p[y * W + x] != f_i).most_common(2)
            for x, y in zona:
                q[y * W + x] = f_i
            emblema_su(q, W, H, cx, cy, r, cz[0][0], cz[1][0])
        elif i == 221:
            # dietro la «R» passa la banda orizzontale: la zona si riempie riga per riga col pixel alla sua sinistra
            for x, y in zona:
                q[y * W + x] = p[y * W + bx0 - 3]
            emblema_su(q, W, H, cx, cy, r, pieno, bordo)
        nuove[i] = (W, H, q)
    # tile nuove: ogni tile prende la riga di palette che contiene tutti i suoi colori
    c555 = [G.bgr555(c) for c in colori]
    fog = C44.Foglio(len(tiles))
    voci = {}
    for i in range(217, 222):
        W, H, q = nuove[i]
        vv = []
        for ty in range(H // 8):
            for tx in range(W // 8):
                blocco = [q[(ty * 8 + y) * W + tx * 8 + x] for y in range(8) for x in range(8)]
                usati = {v for v in blocco if v is not None}
                righe = sorted({v // 16 for v in usati}) or [0]
                riga = None
                for rr in ([righe[0]] if len(righe) == 1 else []) + list(range(len(colori) // 16)):
                    riga_c = c555[rr * 16 + 1:rr * 16 + 16]
                    if all(c555[v] in riga_c for v in usati):
                        riga = rr
                        break
                if riga is None:
                    raise C.Errore('schermata %d tile (%d,%d): nessuna riga di palette ha tutti i colori' % (i, tx, ty))
                rc = c555[riga * 16 + 1:riga * 16 + 16]
                t = [[0 if blocco[y * 8 + x] is None else
                      (blocco[y * 8 + x] % 16 if blocco[y * 8 + x] // 16 == riga else rc.index(c555[blocco[y * 8 + x]]) + 1)
                      for x in range(8)] for y in range(8)]
                vv.append(fog.aggiungi(t, riga))
        voci[i] = vv
    nt = list(fog.tile) + [[[0] * 8 for _ in range(8)]] * (len(tiles) - len(fog.tile))
    out = {216: C.ncgr_con_byte(files[216], C.byte4([list(map(list, t)) for t in nt]))}
    for i in range(217, 222):
        out[i] = C44.nscr_patch(files[i], voci[i])
    anteprime = {i: nuove[i] for i in range(217, 222)}
    return out, dict(tile=len(fog.tile), su=len(tiles), cornice_r=[bx0, by0, bx1, by1], centro=[cx, cy], raggio=r), anteprime, colori


def timbro_sprite(files, i_cg, i_ce):
    """Sprite della «R» (64×64 o più) -> timbro coi due colori più usati della «R» (riempimento e contorno)."""
    W, H, pix = C.sprite(files, i_cg, i_ce)
    cnt = Counter(v for v in pix if v)
    (pieno, _), (bordo, _) = cnt.most_common(2)[:2]
    q = [0] * (W * H)
    emblema_su(q, W, H, W / 2, H / 2, min(W, H) / 2 - 1.5, pieno, bordo)
    return W, H, pix, q


# --------------------------------------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo')
    a = ap.parse_args(argv)
    repo = G.find_repo(a.repo)
    sys.stdout.reconfigure(errors='backslashreplace')
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    reg = json.load(open(REGISTRO, encoding='utf-8'))
    elenco = {v['indice']: v for v in reg['classi_allenatore']['elenco']}
    per_hg = {v['simbolo_hg']: v for v in elenco.values()}
    ng = reg['note_grafica']
    nuove = ng['classi_con_immagine_nuova']
    trans = {v['classe']: v['transizione'] for v in ng['transizioni']}
    allenatori = reg['allenatori']['elenco']
    hg_tr = json.loads(C.leggi(repo, TRAINERS_JSON).decode('utf-8'))['trainers']
    man = dict(blocco='4.6', tipo='file', file=[], sostituzioni=[], fronti=[], dorsi=[], ritratti=[], timbri=[],
               anteprime=[])

    narc = {}
    for rel in (C.FRONTI, C.DORSI, C.TRANSIZIONI):
        b = C.leggi(repo, rel)
        n = G.Narc(b)
        if n.pack() != b:
            err('K26 %s: l’archivio letto e reimpacchettato non è identico' % rel)
        narc[rel] = (b, n, list(n.files))

    # 1. prova di forma
    prova = {}
    for rel in (C.FRONTI, C.DORSI):
        files = narc[rel][2]
        ok = tot = 0
        rel_c = Counter()
        for i in range(len(files) // 5):
            try:
                o, r = C.prova_allenatore(files, i)
            except C.Errore:
                continue
            tot += 1
            ok += o
            rel_c[r] += 1
            if not o:
                err('K26 %s voce %d: letta e riscritta non è identica' % (rel, i * 5))
        prova[rel] = dict(identici=ok, provati=tot, voci=len(files) // 5, metà_scansione=dict(rel_c))
        print('forma: %s %d su %d identiche (%d classi nell’archivio)' % (rel, ok, tot, len(files) // 5))
    man['prova_forma'] = prova

    def classe_di(indice):
        v = elenco[indice]
        sk = v['sprite_classe']
        if sk not in S.SCHEDE:
            err('K27 %s: manca la scheda %s' % (v['simbolo'], sk))
            return v, None
        return v, sk

    def espressione(v):
        return S.ESPRESSIONE_CLASSE.get(v['simbolo'], S.ESPRESSIONE.get(v['categoria'], 'serio'))

    # 2. immagini frontali
    files = narc[C.FRONTI][2]
    righe_ant = []
    fronti = [(k, S.FRONTI_PROTAGONISTA[k], elenco[k]) for k in sorted(S.FRONTI_PROTAGONISTA)]
    for sim in nuove:
        v = next((x for x in elenco.values() if x['simbolo'] == sim), None)
        if v is None:
            err('K27 %s: classe assente dal registro' % sim)
            continue
        _, sk = classe_di(v['indice'])
        if sk:
            fronti.append((v['indice'], sk, v))
    for idx, sk, v in fronti:
        s = S.SCHEDE[sk]
        try:
            al = C.allenatore(files, idx)
            pose = S.pose_fronte(s, al['nf'], espressione(v))
            fot = [F.figura_fronte(s, p) for p in pose]
            pal = C.palette(s)
            nuove_voci = C.scrivi_allenatore(al, fot, pal)
        except (C.Errore, ValueError) as e:
            err('K26 fronte della classe %d (%s): %s' % (idx, v['simbolo'], e))
            continue
        files[idx * 5:idx * 5 + 5] = nuove_voci
        man['fronti'].append(dict(classe=idx, simbolo=v['simbolo'], simbolo_hg=v['simbolo_hg'], categoria=v['categoria'],
                                  scheda=sk, fotogrammi=al['nf'], voci=[idx * 5 + k for k in range(5)],
                                  pose=[dict(L=p['L'], R=p['R'], fase=p.get('fase', 0)) for p in pose],
                                  espressione=pose[0]['espr'], transizione=trans.get(v['simbolo'])))
        righe_ant.append(([(80, 80, f) for f in fot], pal))
    for k in range(0, len(righe_ant), 13):
        nome = 'fronti_%d' % (k // 13 + 1)
        foglio(os.path.join(OUT, 'anteprime', nome + '.png'), righe_ant[k:k + 13])
        man['anteprime'].append(dict(png='anteprime/%s.png' % nome, righe=[f['simbolo'] for f in man['fronti'][k:k + 13]]))

    # 3. dorsi
    files = narc[C.DORSI][2]
    dorsi = []
    for v in ng['dorsi']:
        ci = next(x for x in elenco.values() if x['simbolo'] == v['classe'])
        _, sk = classe_di(ci['indice'])
        if sk:
            dorsi.append((v['valore'], sk, v['dorso_hg'], v['classe']))
    for k, (sk, nome) in sorted(S.DORSI_PROTAGONISTA.items()):
        dorsi.append((k, sk, nome, 'TRAINERCLASS_PKMN_TRAINER_ETHAN' if 'RAGAZZO' in sk else 'TRAINERCLASS_PKMN_TRAINER_LYRA'))
    righe_ant = []
    for idx, sk, nome, classe in sorted(dorsi):
        s = S.SCHEDE[sk]
        try:
            al = C.allenatore(files, idx)
            fasi = S.fasi_retro(al['nf'])
            fot = [F.figura_retro(s, f) for f in fasi]
            pal = C.palette(s)
            nuove_voci = C.scrivi_allenatore(al, fot, pal)
        except (C.Errore, ValueError) as e:
            err('K26 dorso %d (%s): %s' % (idx, nome, e))
            continue
        files[idx * 5:idx * 5 + 5] = nuove_voci
        man['dorsi'].append(dict(dorso=idx, simbolo=nome, classe=classe, scheda=sk, fotogrammi=al['nf'], fasi=fasi,
                                 voci=[idx * 5 + k for k in range(5)]))
        righe_ant.append(([(80, 80, f) for f in fot], pal))
    foglio(os.path.join(OUT, 'anteprime', 'dorsi.png'), righe_ant)
    man['anteprime'].append(dict(png='anteprime/dorsi.png', righe=[d['simbolo'] for d in man['dorsi']]))

    # 4. ritratti delle transizioni e ID degli allenatori
    files = narc[C.TRANSIZIONI][2]
    righe_ant = []
    for t in tabelle_transizioni(repo):
        cls_hg = hg_tr[t['id_hg']]['class'] if t['id_hg'] < len(hg_tr) else None
        v = per_hg.get(cls_hg)
        if t['classe_hg'] is not None and v is not None and v['indice'] != t['classe_hg']:
            err('K28 %s %s: classe %d nella tabella, %s per l’allenatore %d' % (t['file'], t['etichetta'], t['classe_hg'],
                                                                              cls_hg, t['id_hg']))
            continue
        if v is None or v['simbolo'] not in nuove:
            continue
        _, sk = classe_di(v['indice'])
        if not sk:
            continue
        i_pl, i_cg, i_ce, i_an = t['ritratto']
        if [G.kind(files[i]) for i in t['ritratto']] != ['NCLR', 'NCGR', 'NCER', 'NANR']:
            err('K28 %s %s: le voci %s non sono NCLR, NCGR, NCER, NANR' % (t['file'], t['etichetta'], t['ritratto']))
            continue
        cella = C.ncer_celle(files[i_ce])[0]
        if any(o['pal'] for o in cella) or C.cornice(cella)[2:] != (96, 64):
            err('K28 ritratto %d: cella non 96×64 o con palette diversa da 0' % i_cg)
            continue
        s = S.SCHEDE[sk]
        pix = F.ritratto(s, -1, espressione(v))
        pal = C.palette(s)
        files[i_cg] = C.scrivi_sprite(files, i_cg, i_ce, 96, pix)
        files[i_pl] = C44.nclr_patch(files[i_pl], [None] + list(pal[1:16]))
        membri = [x for x in allenatori if x.get('classe') == v['simbolo']]
        nuovo_id = membri[0]['id'] if len(membri) == 1 else 0
        nb = bytearray(t['byte'])
        nb[t['offset_id']], nb[t['offset_id'] + 1] = nuovo_id & 0xFF, nuovo_id >> 8
        so = dict(id='E-GFX-05 %s' % t['etichetta'], file=t['file'], cerca=t['blocco'], sostituisci=con_byte(t['blocco'], nb))
        man['sostituzioni'].append(so)
        man['ritratti'].append(dict(voci=list(t['ritratto']), ncgr=i_cg, nclr=i_pl, tabella=t['file'], etichetta=t['etichetta'],
                                    tipo=t['tipo'], classe_hg=cls_hg, classe=v['simbolo'], scheda=sk,
                                    transizione=trans.get(v['simbolo']), espressione=espressione(v),
                                    id_hg=t['id_hg'], id_trinacria=nuovo_id,
                                    nome=(membri[0].get('nome_in_lotta') if len(membri) == 1 else None),
                                    membri=len(membri)))
        righe_ant.append(([(96, 64, pix)], pal))
    pal_p = None
    for i_cg, i_ce, sk in S.RITRATTI_PROTAGONISTA:
        s = S.SCHEDE[sk]
        pal = C.palette(s)
        if pal_p is not None and pal != pal_p:
            err('K28 ritratti del protagonista: le due schede hanno colori diversi ma una sola palette (voce %d)'
                % S.PALETTE_RITRATTI_PROTAGONISTA)
        pal_p = pal
        pix = F.ritratto(s, 1, 'sorriso')
        files[i_cg] = C.scrivi_sprite(files, i_cg, i_ce, 96, pix)
        man['ritratti'].append(dict(voci=[S.PALETTE_RITRATTI_PROTAGONISTA, i_cg, i_ce, i_ce + 1], ncgr=i_cg,
                                    nclr=S.PALETTE_RITRATTI_PROTAGONISTA, tabella=OV115, etichetta='ov115_0225F978',
                                    tipo='protagonista', classe_hg=None, classe='protagonista', scheda=sk,
                                    transizione='29–33 (Campioni dell’ARS e Presidente)', espressione='sorriso',
                                    id_hg=None, id_trinacria=None, nome=None, membri=None))
        righe_ant.append(([(96, 64, pix)], pal))
    i = S.PALETTE_RITRATTI_PROTAGONISTA
    files[i] = C44.nclr_patch(files[i], [None] + list(pal_p[1:16]))
    for k in range(0, len(righe_ant), 11):
        nome = 'ritratti_%d' % (k // 11 + 1)
        foglio(os.path.join(OUT, 'anteprime', nome + '.png'), righe_ant[k:k + 11])
        man['anteprime'].append(dict(png='anteprime/%s.png' % nome,
                                     righe=['%s (%d)' % (r['scheda'], r['ncgr']) for r in man['ritratti'][k:k + 11]]))

    # 5. il timbro di «U Sistema» al posto della «R»
    righe_ant = []
    for i_cg, i_ce, i_pl, uso in ((156, 158, 3, 'transizione 39 (Scagnozzu, Infiltrata): sprite ripetuto sei volte '
                                               '(asm/overlay_117.s, ov117_0225F020)'),
                                  (153, 155, 3, '«R» grande, voci 153–155 (nessun uso trovato nel codice: si cambia lo stesso)')):
        try:
            W, H, vecchio, nuovo = timbro_sprite(files, i_cg, i_ce)
        except (C.Errore, ValueError) as e:
            err('K28 timbro %d: %s' % (i_cg, e))
            continue
        files[i_cg] = C.scrivi_sprite(files, i_cg, i_ce, W, nuovo)
        man['timbri'].append(dict(ncgr=i_cg, ncer=i_ce, misura='%d×%d' % (W, H), uso=uso))
        colori = C44.nclr_leggi(files[i_pl])[1]
        righe_ant.append(([(W, H, vecchio), (W, H, nuovo)], colori[:16]))
    try:
        nuovi, info, ant_sch, colori = schermate_r(files)
        for i, b in nuovi.items():
            files[i] = b
        man['timbri'].append(dict(ncgr=216, nscr=list(range(217, 222)), nclr=215, misura='5 schermate 256×256',
                                  uso='sfondo delle transizioni 40–44 (asm/overlay_117.s, ov117_0225F524)', **info))
        for i, (W, H, q) in ant_sch.items():
            C44.anteprima(os.path.join(OUT, 'anteprime', 'schermata_%d.png' % i), W, H,
                          [0 if v is None else v for v in q], list(colori) + [(0, 0, 0)] * (256 - len(colori)), 1)
            man['anteprime'].append(dict(png='anteprime/schermata_%d.png' % i, righe=['NSCR %d' % i]))
    except (C.Errore, ValueError) as e:
        err('K28 schermate della «R»: %s' % e)
    if righe_ant:
        foglio(os.path.join(OUT, 'anteprime', 'timbri.png'), righe_ant)
        man['anteprime'].append(dict(png='anteprime/timbri.png', righe=['sprite %d prima e dopo' % t['ncgr']
                                                                       for t in man['timbri'] if 'ncer' in t]))

    # 6. archivi
    for rel in (C.FRONTI, C.DORSI, C.TRANSIZIONI):
        orig, n, fl = narc[rel]
        cambiate = sum(1 for x, y in zip(n.files, fl) if x != y)
        n.files = fl
        nuovo = n.pack()
        if len(G.Narc(nuovo).files) != len(fl):
            err('K26 %s: numero di voci cambiato' % rel)
        sorg = scrivi('file/' + rel, nuovo)
        man['file'].append(dict(destinazione=rel, sorgente=sorg, sha1_hg=G.sha1(orig), sha1_nuovo=G.sha1(nuovo),
                                byte=len(nuovo), voci_cambiate=cambiate, voci=len(fl)))
        print('%s: %d voci cambiate su %d' % (rel, cambiate, len(fl)))

    scrivi('manifesto.json', json.dumps(man, ensure_ascii=False, indent=1))
    print('%d fronti, %d dorsi, %d ritratti, %d timbri, %d sostituzioni di codice'
          % (len(man['fronti']), len(man['dorsi']), len(man['ritratti']), len(man['timbri']), len(man['sostituzioni'])))
    print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

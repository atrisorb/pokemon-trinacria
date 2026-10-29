"""Blocco 4.5 — costruisce gli sprite di campo dei personaggi in build/grafica/4.5 (R-GFX-17).

    python -I tools/grafica/4.5/costruisci45.py [--repo R]

Disegna con omino45.py le schede di schede45.py, riscrive a forma invariata (R-GFX-34) gli NSBTX degli slot
del registro 2.5 (26 personaggi, 12 classi) e delle 9 famiglie di sprite del protagonista (ragazzo e
ragazza), scrive le anteprime e manifesto.json, che `trinacria_gfx.py applica --blocchi 4.5` porta nel
repository (file sostituiti interi, riconosciuti dallo SHA-1). Ultima riga: GRAFICA_OK oppure
GRAFICA_FAILED. Solo libreria standard, gira in pochi secondi."""
import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import comune45 as C          # noqa: E402
import omino45 as O           # noqa: E402
import schede45 as S          # noqa: E402

G = C.G
OUT = C.OUT
REGISTRO = os.path.join(C.PROJ, 'docs', 'MODULO_2', '2.5_TRAINERS_SPRITES_FLY_SEQ.json')
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


def foglio(path, righe, palette, scala=3):
    """Anteprima: una riga per voce, ogni voce una lista di fotogrammi (1024 indici) con la sua palette."""
    n = max(len(r) for r in righe)
    cw = 33 * scala
    Wd, Hd = n * cw, len(righe) * cw
    pix = [0] * (Wd * Hd)
    pal = [(214, 230, 206)]
    for r, (fr_list, colori) in enumerate(zip(righe, palette)):
        base = len(pal) - 1
        pal += colori[1:16]
        for k, fr in enumerate(fr_list):
            for y in range(32):
                for x in range(32):
                    c = fr[y * 32 + x]
                    if not c:
                        continue
                    v = base + c
                    for dy in range(scala):
                        row = (r * cw + y * scala + dy) * Wd + k * cw + x * scala
                        for dx in range(scala):
                            pix[row + dx] = v
    if len(pal) > 256:
        raise C.Errore('troppe palette in un foglio')
    C.C44.salva_png(path, Wd, Hd, pal, pix, bpp=8)


def costruisci_sprite(repo, mmodel, numero, scheda, tab):
    rel = C.MMODEL % numero
    orig = C.leggi(repo, rel)
    st = C.struttura(orig)
    if set(st['fotogrammi']) != set(tab):
        err('K24 %s (%s): fotogrammi %s, la tabella ne ha %s' % (mmodel, rel, sorted(st['fotogrammi']), sorted(tab)))
        return None
    if any((w, h) != (32, 32) for _, w, h in st['fotogrammi'].values()):
        err('K24 %s: fotogrammi non 32×32' % mmodel)
        return None
    fr = {n: O.disegna(scheda, p) for n, p in tab.items()}
    pal = C.palette(scheda['colori'])
    c555 = [st['colori'][0]] + [G.bgr555(c) for c in pal[1:]]
    try:
        nuovo = C.riscrivi(orig, fr, c555)
    except C.Errore as e:
        err('K22 %s: %s' % (mmodel, e))
        return None
    return dict(rel=rel, orig=orig, nuovo=nuovo, fotogrammi=fr, palette=pal, struttura=st)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo')
    a = ap.parse_args(argv)
    repo = G.find_repo(a.repo)
    sys.stdout.reconfigure(errors='backslashreplace')
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    reg = json.load(open(REGISTRO, encoding='utf-8'))['sprite']
    sp2mm, mmnum, usi = C.mmodel_di(repo)
    man = dict(blocco='4.5', tipo='file', file=[], anteprime=[], personaggi=[], protagonista=[], non_usati=S.NON_USATI)

    # 0. prova della forma su tutti gli sprite di campo con una sola palette a 16 colori
    ok = n = 0
    cartella = os.path.join(repo, 'files', 'data', 'mmodel', 'mmodel')
    for f in sorted(os.listdir(cartella)):
        if not f.endswith('.NSBTX'):
            continue
        b = open(os.path.join(cartella, f), 'rb').read()
        try:
            C.struttura(b)
        except C.Errore:
            continue
        n += 1
        if C.prova_forma(b):
            ok += 1
        else:
            err('K22 %s: letto e riscritto non è identico' % f)
    man['prova_forma'] = dict(identici=ok, provati=n)
    print('forma invariata: %d NSBTX su %d letti e riscritti identici' % (ok, n))

    def registra(r, nota):
        sorg = scrivi('file/' + r['rel'], r['nuovo'])
        man['file'].append(dict(destinazione=r['rel'], sorgente=sorg, sha1_hg=G.sha1(r['orig']),
                                sha1_nuovo=G.sha1(r['nuovo']), byte=len(r['nuovo']), nota=nota))

    # 1. personaggi e classi del registro 2.5
    righe, pals, nomi = [], [], []
    cammina = S.tabella('cammina16')
    for gruppo, schede in (('personaggi', S.PERSONAGGI), ('classi', S.CLASSI)):
        for v in reg[gruppo]:
            simbolo, slot = v['simbolo'], v['slot_hg']
            scheda = schede.get(simbolo)
            if scheda is None:
                err('K25 %s: manca la scheda' % simbolo)
                continue
            mm = sp2mm.get(slot)
            if mm is None:
                err('K25 %s: lo slot %s non è nella tabella degli sprite' % (simbolo, slot))
                continue
            altri = [x for x in usi.get(mm, []) if x != slot]
            if altri:
                err('K25 %s: il modello %s è usato anche da %s' % (simbolo, mm, ', '.join(altri)))
            r = costruisci_sprite(repo, mm, mmnum[mm], scheda, cammina)
            if r is None:
                continue
            chi = v.get('personaggio') or v.get('classe')
            registra(r, '%s (%s)' % (simbolo, chi))
            man['personaggi'].append(dict(gruppo=gruppo, simbolo=simbolo, slot=slot, mmodel=mm, numero=mmnum[mm],
                                          file=r['rel'], chi=chi, codice=v.get('codice', ''),
                                          capelli=scheda['capelli'], sopra=scheda['sopra'], sotto=scheda['sotto'],
                                          accessori=list(scheda.get('accessori', ())), pancia=scheda.get('pancia', 0),
                                          perche=scheda['perche'], texture=r['struttura']['nome']))
            righe.append([r['fotogrammi'][k] for k in (1, 2, 5, 6, 9, 10, 13, 14)])
            pals.append(r['palette'])
            nomi.append(simbolo)
    for k in range(0, len(righe), 13):
        nome = 'personaggi_%d' % (k // 13 + 1)
        foglio(os.path.join(OUT, 'anteprime', nome + '.png'), righe[k:k + 13], pals[k:k + 13])
        man['anteprime'].append(dict(png='anteprime/%s.png' % nome, righe=nomi[k:k + 13]))

    # 2. protagonista: 9 famiglie × 2
    for genere, idx in (('ragazzo', 0), ('ragazza', 1)):
        scheda = S.PROTAGONISTA[genere]
        righe, pals = [], []
        for fam in S.FAMIGLIE:
            mm, tab_nome, uso = fam[idx], fam[2], fam[3]
            if mm not in mmnum:
                err('K25 %s: non è in mmodel.h' % mm)
                continue
            tab = S.tabella(tab_nome)
            r = costruisci_sprite(repo, mm, mmnum[mm], scheda, tab)
            if r is None:
                continue
            registra(r, 'protagonista (%s): %s' % (genere, uso))
            man['protagonista'].append(dict(genere=genere, mmodel=mm, numero=mmnum[mm], file=r['rel'],
                                            tabella=tab_nome, fotogrammi=len(tab),
                                            unici=len({o for o, _, _ in r['struttura']['fotogrammi'].values()}),
                                            uso=uso, sprite=sorted(usi.get(mm, []))))
            righe.append([r['fotogrammi'][k] for k in sorted(tab)])
            pals.append(r['palette'])
        nome = 'protagonista_%s' % genere
        foglio(os.path.join(OUT, 'anteprime', nome + '.png'), righe, pals, scala=2)
        man['anteprime'].append(dict(png='anteprime/%s.png' % nome, righe=[f[idx] for f in S.FAMIGLIE]))
    man['schede_protagonista'] = {g: dict(capelli=s['capelli'], sopra=s['sopra'], sotto=s['sotto'],
                                          accessori=list(s['accessori']), perche=s['perche'], chi=s['chi'])
                                  for g, s in S.PROTAGONISTA.items()}

    scrivi('manifesto.json', json.dumps(man, ensure_ascii=False, indent=1))
    print('%d file (%d sprite di personaggi e classi, %d del protagonista), %d anteprime'
          % (len(man['file']), len(man['personaggi']), len(man['protagonista']), len(man['anteprime'])))
    print('GRAFICA_FAILED' if errors else 'GRAFICA_OK')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

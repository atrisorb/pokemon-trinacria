#!/usr/bin/env python3
"""Script di prova della pipeline audio (blocco 5.1).

Uso: python -I tools/music/prova_5_1.py --out <cartella> [--repo F:/Progetti/pokeheartgold]

Compone la partitura di prova tools/music/prova/SEQ_CT_CORSO_ITALIA.py, la mette
nello slot SEQ_GS_T_WAKABA (e nel gemello SEQ_GS_P_T_WAKABA) di una copia
dell'archivio originale e controlla che tutto il resto sia rimasto identico.
Nella cartella scrive: SEQ_CT_CORSO_ITALIA.mid, .sseq, .txt (disassemblato),
manifesto.json e gs_sound_data.sdat (da copiare in files/data/sound/ per
ascoltarlo nell'emulatore). Non tocca il repository.
Ultima riga: AUDIO_OK oppure AUDIO_FAILED.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import trinacria_audio as A  # noqa: E402
import componi as C  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', required=True)
    ap.add_argument('--repo')
    a = ap.parse_args(argv)
    repo = a.repo or A.default_repo()
    if not repo:
        print('ERRORE A00 repository di HeartGold non trovato (--repo)')
        print('AUDIO_FAILED')
        return 1
    reg = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'docs', 'MODULO_2',
                       '2.5_TRAINERS_SPRITES_FLY_SEQ.json')
    alias = C.alias_from_registry(reg)
    man, errs = C.componi([os.path.join(HERE, 'prova', 'SEQ_CT_CORSO_ITALIA.py')], a.out, alias)
    A.print_errs(errs)
    if errs:
        print('AUDIO_FAILED')
        return 1
    A.write(os.path.join(a.out, 'manifesto.json'), json.dumps(man, ensure_ascii=False, indent=1).encode('utf-8'))
    hg, hg_path = A.hg_original(repo)
    out, rep, errs = A.applica(hg, man, a.out, repo=repo)
    for r in rep:
        print(r)
    A.print_errs(errs)
    if errs:
        print('AUDIO_FAILED')
        return 1
    errs = A.controlla(hg, out, man, a.out)
    A.print_errs(errs)
    if errs:
        print('AUDIO_FAILED')
        return 1
    sseq, info = A.midi_to_sseq(A.read(os.path.join(a.out, 'SEQ_CT_CORSO_ITALIA.mid')))
    A.write(os.path.join(a.out, 'SEQ_CT_CORSO_ITALIA.sseq'), sseq)
    A.write(os.path.join(a.out, 'SEQ_CT_CORSO_ITALIA.txt'), A.disasm(sseq).encode('utf-8'))
    A.write(os.path.join(a.out, 'gs_sound_data.sdat'), out)
    print('originale: %s' % hg_path)
    print('sequenza: %d byte, %d tracce, %d note, ritornello %s' % (
        len(sseq), info['tracce'], info['note'], info['ritornello']))
    print('archivio: %d byte (originale %d), controllo con l\'originale superato' % (len(out), len(hg)))
    print('AUDIO_OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())

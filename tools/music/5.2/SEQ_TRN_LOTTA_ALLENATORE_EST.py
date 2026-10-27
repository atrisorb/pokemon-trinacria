"""Lotta con un allenatore nella Sicilia orientale (regione Kanto del motore): stesso brano di
SEQ_TRN_LOTTA_ALLENATORE, con lo stesso banco e lo stesso volume, così suona identico."""
import os
import runpy

_BASE = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'SEQ_TRN_LOTTA_ALLENATORE.py'))

SIMBOLO = 'SEQ_TRN_LOTTA_ALLENATORE_EST'
BANCO = _BASE['BANCO']
VOLUME = _BASE['VOLUME']
SCHEDA = dict(_BASE['SCHEDA'], stesso_brano='SEQ_TRN_LOTTA_ALLENATORE')
partitura = _BASE['partitura']

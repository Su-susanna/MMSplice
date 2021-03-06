"""Top-level package for mmsplice."""

__author__ = """Jun Cheng & M.Hasan Celik"""
__email__ = 'chengju@in.tum.de'
__version__ = '1.0.3'

from keras.models import load_model
from mmsplice.mmsplice import MMSplice, \
    writeVCF, \
    predict_save, \
    predict_all_table, \
    ACCEPTOR_INTRON, \
    ACCEPTOR, \
    EXON, \
    EXON3,\
    DONOR, \
    DONOR_INTRON, \
    LINEAR_MODEL, \
    LOGISTIC_MODEL,\
    EFFICIENCY_MODEL

__all__ = [
    'load_model',
    'MMSplice',
    'writeVCF',
    'predict_save',
    'predict_all_table',
    'ACCEPTOR_INTRON',
    'ACCEPTOR',
    'EXON',
    'EXON3',
    'DONOR',
    'DONOR_INTRON',
    'LINEAR_MODEL',
    'LOGISTIC_MODEL',
    'EFFICIENCY_MODEL'
]

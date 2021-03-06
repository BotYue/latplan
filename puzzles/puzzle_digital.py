import numpy as np
from .model.puzzle import *
from .split_image import split_image
from .util import preprocess
import os

def setup():
    setting['base'] = 5

    def loader(width,height):
        return preprocess(np.array(_get_panel()))

    def _get_panel():
        return [
            [[0, 0, 1, 0, 0,],
             [0, 1, 0, 1, 0,],
             [0, 1, 0, 1, 0,],
             [0, 1, 0, 1, 0,],
             [0, 0, 1, 0, 0,],],
            [[0, 0, 1, 0, 0,],
             [0, 0, 1, 0, 0,],
             [0, 0, 1, 0, 0,],
             [0, 0, 1, 0, 0,],
             [0, 0, 1, 0, 0,],],
            [[0, 1, 1, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 1, 1, 1, 0,],
             [0, 1, 0, 0, 0,],
             [0, 1, 1, 1, 0,],],
            [[0, 1, 1, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 1, 1, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 1, 1, 1, 0,],],
            [[0, 1, 0, 1, 0,],
             [0, 1, 0, 1, 0,],
             [0, 1, 1, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 0, 0, 1, 0,],],
            [[0, 1, 1, 1, 0,],
             [0, 1, 0, 0, 0,],
             [0, 1, 1, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 1, 1, 1, 0,],],
            [[0, 1, 1, 1, 0,],
             [0, 1, 0, 0, 0,],
             [0, 1, 1, 1, 0,],
             [0, 1, 0, 1, 0,],
             [0, 1, 1, 1, 0,],],
            [[0, 1, 1, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 0, 0, 1, 0,],
             [0, 0, 0, 1, 0,],],
            [[0, 1, 1, 1, 0,],
             [0, 1, 0, 1, 0,],
             [0, 1, 1, 1, 0,],
             [0, 1, 0, 1, 0,],
             [0, 1, 1, 1, 0,],],
            # [[0, 1, 1, 1, 0,],
            #  [0, 1, 0, 1, 0,],
            #  [0, 1, 1, 1, 0,],
            #  [0, 0, 0, 1, 0,],
            #  [0, 0, 0, 1, 0,],],
            # [[0, 0, 0, 0, 0,],
            #  [0, 0, 1, 1, 0,],
            #  [0, 1, 0, 1, 0,],
            #  [0, 1, 0, 1, 0,],
            #  [0, 1, 1, 1, 0,],],
            # [[0, 0, 0, 0, 0,],
            #  [0, 1, 0, 0, 0,],
            #  [0, 1, 1, 0, 0,],
            #  [0, 1, 0, 1, 0,],
            #  [0, 1, 1, 0, 0,],],
            # [[0, 0, 0, 0, 0,],
            #  [0, 0, 1, 1, 0,],
            #  [0, 1, 0, 0, 0,],
            #  [0, 1, 0, 0, 0,],
            #  [0, 0, 1, 1, 0,],],
            # [[0, 0, 0, 0, 0,],
            #  [0, 0, 0, 1, 0,],
            #  [0, 0, 1, 1, 0,],
            #  [0, 1, 0, 1, 0,],
            #  [0, 0, 1, 1, 0,],],
            # [[0, 0, 1, 0, 0,],
            #  [0, 1, 0, 1, 0,],
            #  [0, 1, 1, 1, 0,],
            #  [0, 1, 0, 0, 0,],
            #  [0, 0, 1, 1, 0,],],
            # [[0, 0, 0, 1, 0,],
            #  [0, 0, 1, 0, 0,],
            #  [0, 1, 1, 1, 0,],
            #  [0, 0, 1, 0, 0,],
       ]
    
    
    setting['loader'] = loader

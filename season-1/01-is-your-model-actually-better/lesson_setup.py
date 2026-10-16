import numpy as np
from scipy.stats import bootstrap, permutation_test
from IPython.display import display
from demo_visuals import *
baseline = np.array([0.110, 0.170, 0.140, 0.190, 0.130])
candidate = np.array([0.095, 0.150, 0.125, 0.175, 0.120])
difference = candidate - baseline

def mean_difference(x, y, axis=-1):
    return np.mean(x - y, axis=axis)

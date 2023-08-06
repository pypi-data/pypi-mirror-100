# -*- coding: utf-8 -*-

__version__ = "0.3.0"


from . import numba_backend
from . import tensor_backend

from .tensor_backend import neurons
from .tensor_backend import synapses


def set_backend(backend):
    global neurons
    global synapses

    if backend in ['tensor', 'numpy', 'pytorch', 'tensorflow', 'jax']:
        neurons = tensor_backend.neurons
        synapses = tensor_backend.synapses

    elif backend in ['numba', 'numba-parallel', 'numba-cuda']:
        neurons = numba_backend.neurons
        synapses = numba_backend.synapses

    else:
        raise ValueError(f'Unknown backend "{backend}".')

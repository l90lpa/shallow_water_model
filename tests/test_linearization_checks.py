
import numpy as np

from .utils import linearization_checks as lc

## Parameters
shape = (3,3)
dtype = np.float64
rng = np.random.default_rng(12345)

## argument generators
def primalArg():
    return np.array(rng.normal(0.0, 1.0, shape), dtype=dtype)

def tangentArg():
    return np.array(rng.normal(0.0, 1.0, shape), dtype=dtype)

def cotangentArg():
    return np.array(rng.normal(0.0, 1.0, shape), dtype=dtype)

## vector field operations for the arguments
def scale(a, x):
    return a * x

def add(x, y):
    return x + y
        
def dot(x,y):
    dot_ = np.sum(x * y)
    return dot_

def norm(x):
    return np.sqrt(dot(x,x))

## test function and its linearizations
def identity(s):
    return s

def identity_tlm(s, ds):
    return identity(s), ds

def identity_adm(s, ds):
    return identity(s), ds


def test_tlm_linearity():
    success, absolute_error = lc.testTLMLinearity(identity_tlm, primalArg, tangentArg, scale, norm, 1.0e-15)
    print(f"TLM Linearity Test: success={success}, absolute error={absolute_error}")
    assert success

def test_tlm_approx():
    success, relative_error = lc.testTLMApprox(identity, identity_tlm, primalArg, tangentArg, scale, add, norm, 1.0e-15)
    print(f"TLM Approximation Test: success={success}, relative error={relative_error}")
    assert success

def test_spectral_theorem():
    success, absolute_error = lc.testSpectralTheorem(identity_tlm, identity_adm, primalArg, tangentArg, cotangentArg, dot, 1.0e-15)
    print(f"Spectral Theorem (\"Dot Product\") Test: success={success}, absolute error={absolute_error}")
    assert success
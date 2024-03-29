""" Testing fitdata module

Testing fitting functions.
"""

import pytest
import numpy as np

from elisarep import fitdata


def test_func():
    """ Simple fitdata function
    """
    assert fitdata.func(1.0e9, 0.01, 0.9, 500_000_000.0,
                        1.0) == pytest.approx(0.6545787829565919)


def test_inv_func():
    """ Testing inverse function
    """
    assert fitdata.inv_func(0.6, 0.01, 0.9, 500_000_000.0,
                            1.0) == pytest.approx(770046043.1062976)


def test_fit_reference():
    """ Testing reference
    """
    x = np.array([17954000000.0, 8977000000.0, 4488500000.0,
                 2244250000.0, 1122125000.0, 561062500.0, 280531250.0])
    y = np.array([1.4609, 0.7627, 0.45620000000000005,
                 0.29560000000000003, 0.15300000000000002, 0.0824, 0.0465])
    r = fitdata.fit_reference(fitdata.func, x, y)

    np.set_printoptions(precision=15)
    print(r[0])
    print(r[1])
    e0 = np.array([2.458263134007747e-02, 8.757114266301876e-01,
                  177515309668323.03, 4.489354892866454e+03])
    e1 = np.array([[1.207920070761124e-03, 2.508353224895644e-03,
                    -4.635234909384080e+14, -1.016221678724365e+04],
                   [2.508353224895644e-03, 7.529487573883436e-03,
                    -1973827276500353.5, -4.339550201713505e+04],
                   [-4.635234909384080e+14, -1973827276500353.5,
                    1.4082172971070022e+33, 3.109869366362530e+22],
                   [-1.016221678724365e+04, -4.339550201713505e+04,
                    3.109869366362530e+22, 6.867831382517489e+11]])

    np.testing.assert_array_almost_equal(e0, r[0])
    np.testing.assert_array_almost_equal(e1, r[1])

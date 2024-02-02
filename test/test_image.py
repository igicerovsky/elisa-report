""" Tests for the image module."""
import pandas as pd
import numpy as np
from elisarep.image import mask_index, na_index, confidence_intervals


def test_mask_index():
    """
    Test function for the mask_index function.

    This function tests the behavior of the mask_index function by creating a DataFrame
    with a specific structure and checking the output against expected values.

    Returns:
        None
    """
    idx = pd.MultiIndex.from_product([['A'],
                                      [1, 2, 3, 4]],
                                     names=['col', 'row'])
    key = 'mask_reason'
    col = ['concentration', key]
    df = pd.DataFrame([(10, "failed"), (11, np.nan),
                       (6, '<8'), (16, None)], idx, col)

    actual = mask_index(df, key)
    expected = [0, 2]

    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(actual, expected))


def test_na_index():
    """
    Test function for the na_index function.

    This function tests the behavior of the na_index function by creating a DataFrame
    with a specific structure and checking the output against expected values.

    Returns:
        None
    """
    idx = pd.MultiIndex.from_product([['A'],
                                      [1, 2, 3, 4]],
                                     names=['col', 'row'])
    key = 'backfit'
    col = [key, 'mask_reason']
    df = pd.DataFrame([(np.nan, "failed"), (11, np.nan),
                       (np.nan, '<8'), (16, None)], idx, col)

    actual = na_index(df, key)
    expected = [0, 2]

    assert len(actual) == len(expected)
    assert all(a == b for a, b in zip(actual, expected))


def test_confidence_intervals():
    """
    Test function for the confidence_intervals function.

    This function tests the behavior of the confidence_intervals function by providing
    a covariance matrix and parameter estimates, and checking the output against expected values.

    Returns:
        None
    """
    pcov = np.array([[0.01, 0.02],
                     [0.02, 0.04]])
    popt = np.array([1.0, 2.0])

    popt_low, popt_high = confidence_intervals(pcov, popt)

    expected_low = np.array([0.9, 1.8])
    expected_high = np.array([1.1, 2.2])

    assert np.allclose(popt_low, expected_low)
    assert np.allclose(popt_high, expected_high)

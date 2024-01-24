"""Display measured data as image/graph

Draw graph images using the measured data.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import distributions
import pandas as pd

from .sample import sample_check
from .fitdata import fit_reference_auto_rm, func


def fit_image(x, y, popt, pcov, file_path, confidence_interval=95.0,
              confidence=None, interval_ratio=2.0,
              rm_index=None,
              sx=None, sy=None, mask_idx=None, sna_idx=None,
              valid_sample=True):
    r"""Plot the fitted function with confidence intervals.

    Confidence intervals coud be set using `confidence` parameter.
    'student-t' method is a correct one producing wider confidence intervals.

    Parameters
    ----------
    x : array_like
        x-axis reference values.
    y : array_like
        y-axis reference values.
    popt : iterable
        Fit parameters.
    pcov : 
        Covariance matrix from fitting algorithm.
    file_path : string
        Path where the graph image is saved or `None`
    confidence_interval : float 
        Confidence interval in %
    interval_ratio: float
        Ration of min and max extention of x axis for fitted curve plot.
    rm_index: list
        Index of a removed point.
    sx : array_like
        Sample x-values.
    sy : array_like
        Sample x-values.
    mask_idx : array_like
        Indices of masked samples.
    sna_idx : 
        Indices of nan data excluded.
    valid_sample : bool
        Is sample valid?
    """
    if rm_index is None:
        rm_index = []
    if mask_idx is None:
        mask_idx = []
    if sna_idx is None:
        sna_idx = []
    # confidence [None, 'student-t', 'sqrt_err']

    kw_scatter = {'marker': 'x'}
    if not valid_sample:
        kw_scatter = {'marker': 'o', 'facecolors': 'none'}
    if (sx is not None) and (sy is not None):
        if len(sx.drop(mask_idx, axis=0)) != 0:
            plt.scatter(sx.drop(mask_idx, axis=0), sy.drop(mask_idx, axis=0),
                        s=48, linewidths=0.6, label='point valid',
                        color='forestgreen', **kw_scatter)
        if (len(sx.iloc[mask_idx]) != 0) and (list(mask_idx) != list(sna_idx)):
            plt.scatter(sx.iloc[mask_idx], sy.iloc[mask_idx],
                        s=48, linewidths=0.8, label='point masked', color='r', **kw_scatter)

    if len(x.drop(rm_index, axis=0)) != 0:
        plt.scatter(x.drop(rm_index, axis=0), y.drop(rm_index, axis=0), marker='+',
                    color='royalblue', s=48, linewidths=0.8, label='reference')
    if len(x.iloc[rm_index]) != 0:
        plt.scatter(x.iloc[rm_index], y.iloc[rm_index], marker='.',
                    color='r', s=48, linewidths=0.8, label='reference masked')
    plt.xscale('log')

    if confidence is None or confidence == 'student-t':
        popt_low, popt_high = confidence_intervals_studentt(
            y, popt, pcov, confidence_interval)
    else:
        popt_low, popt_high = confidence_intervals(pcov, popt)

    num_pts = 400
    t = np.arange(x.min(), x.max(), (x.max() - x.min()) / num_pts)
    plt.plot(t, func(t, *popt), color='slategray', linewidth=0.2)

    sx_n = sx[~sx.isna()] if sx is not None else None
    x_min_ext = x.min() / interval_ratio
    if sx is not None:
        x_min_ext = min(x_min_ext, sx_n.min())
    ext_legend = False
    if x.min() != x_min_ext:
        t = np.arange(x_min_ext, x.min(),
                      (x.min() - x_min_ext) / (num_pts / 10.0))
        plt.plot(t, func(t, *popt), color='red',
                 linestyle=(0, (5, 10)), linewidth=0.2, label='ext')
        ext_legend = True

    x_max_ext = x.max() * interval_ratio
    if sx is not None:
        x_max_ext = max(x_max_ext, sx_n.max())
    if x.max() != x_max_ext:
        t = np.arange(x.max(), x_max_ext,
                      (x_max_ext - x.max()) / (num_pts / 10.0))
        # no label, only one extension label
        ext_label = None
        if not ext_legend:
            ext_label = 'ext'
        plt.plot(t, func(t, *popt), color='red',
                 linestyle=(0, (5, 10)), linewidth=0.2, label=ext_label)

    # show NaN concentration values somewhere -> show OD
    sx_na = sx[sx.isna()] if sx is not None else None
    if sx is not None:
        sna_idx = sx[~sx.isna()].index
        if len(sx_na) != 0:
            x_na = np.full(shape=len(sx_na), fill_value=x_min_ext * 0.5)
            y_na = sy.drop(sna_idx, axis=0)
            plt.scatter(x_na, y_na, marker='_', color='red', s=48,
                        linewidths=0.8, label='backfit failed')

    plt.xlabel('concentration [cp/ml]')
    plt.ylabel('Optical density')

    t = np.arange(x_min_ext, x_max_ext, (x_max_ext - x_min_ext) / num_pts)
    bound_upper = func(t, *popt_high)
    bound_lower = func(t, *popt_low)
    # plotting the confidence intervals
    plt.fill_between(t, bound_lower, bound_upper,
                     color='black', alpha=0.15)

    plt.legend()

    if file_path is not None:
        plt.savefig(file_path)
    plt.clf()


def confidence_intervals(pcov, popt):
    perr = np.sqrt(np.diag(pcov))
    popt_high = popt + perr
    popt_low = popt - perr
    return popt_low, popt_high


def confidence_intervals_studentt(y, popt, pcov, confidence_interval):
    alpha = (100.0 - confidence_interval) / 100.0
    n = len(y)    # number of data points
    p = len(popt)  # number of parameters
    dof = max(0, n - p)  # number of degrees of freedom

    # student-t value for the dof and confidence level
    tval = distributions.t.ppf(1.0 - alpha / 2., dof)
    sigma_popt = np.empty(len(popt), dtype=np.float64)
    param_names = ['a', 'b', 'c', 'd']
    for i, p, var, pname in zip(range(n), popt, np.diag(pcov), param_names):
        sigma = var ** 0.5
        st = sigma * tval
        sigma_popt[i] = st
    popt_high = popt + sigma_popt
    popt_low = popt - sigma_popt
    return popt_low, popt_high


def mask_index(df: pd.DataFrame) -> list:
    """Get the index of masked data

    Parameters:
    -----------
    df : pandas.datarame

    Returns:
    --------
    index
        Index of masked data.
    """
    b = df.reset_index(level=[0, 1])
    b = b[b['mask_reason'].notna()]

    return b.index


def na_index(df: pd.DataFrame):
    """Get index of `na` data
    """
    b = df.reset_index(level=[0, 1])
    b = b[b['backfit'].isna()]

    return b.index


def sample_img(samples, reference, sample_type, sample_num, img_file=None) -> None:
    """Draw image of a sample

    Sample image contains reference curve and sample points 
    to see the context between them.

    Parameters:
    -----------
    samples : pandas.dataframe
        Dataframe of all samples.
    reference : pandas.dataframe
        Dataframe of reference.
    sample_type : string
        Type od sample one of 'r'(reference), 'k'(controll german), 's' (sample).
    sample_num : int
        Sample number.
    img_file : path_like
        Image fime name or `None`. Optional, if specified file is saved.
    show : bool
        Display image.
    """

    sd = sample_check(samples, sample_type, sample_num)

    mask_idx = mask_index(sd['sample'])
    x = reference.reset_index(level=[0, 1])['plate_layout_conc']
    y = reference.reset_index(level=[0, 1])['OD_delta']
    fit_result = fit_reference_auto_rm(x, y)
    # compute original concenmtration
    sd['sample'].loc[:, ['conc_plot']] = sd['sample'].apply(
        lambda x: x['concentration'] / x['plate_layout_dil'], axis=1)
    sx = sd['sample'].reset_index(level=[0, 1])['conc_plot']
    sy = sd['sample'].reset_index(level=[0, 1])['OD_delta']
    fit_image(x, y, fit_result[0][0], fit_result[0][1], img_file, confidence='student-t',
              rm_index=fit_result[1], mask_idx=mask_idx,
              sx=sx, sy=sy, sna_idx=na_index(sd['sample']),
              valid_sample=sd['valid'], interval_ratio=1.0)

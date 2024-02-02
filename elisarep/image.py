"""Display measured data as image/graph

Draw graph images using the measured data.
"""
from dataclasses import dataclass
import io

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import distributions
import pandas as pd

from .sample import sample_check
from .fitdata import fit_reference_auto_rm, func


@dataclass
class ImageFitResult:
    """Image fit result

    Parameters
    ----------
    x : array_like
        x-axis values.
    y : array_like
        y-axis value.
    popt : array_like
        fit parameters.
    pcov : array_like
        covariance matrix.
    """
    x: pd.Series
    y: pd.Series
    popt: np.iterable
    pcov: np.iterable
    rm_index: list


@dataclass
class SampleData:
    """Sample data

    Parameters  
    ----------
    sx : pd.Series
        Sample x-axis values.   
    sy : pd.Series  
        Sample y-axis values.
     mask_idx : list
        Masked sample index.
    na_idx : list
        Sample index with NaN values.
    """
    sx: pd.Series = None
    sy: pd.Series = None
    mask_idx: list = None
    na_idx: list = None
    valid: bool = True


def draw_sample(sample: SampleData):
    """Draw sample points.
    """
    kw_scatter = {'marker': 'x'}
    if not sample.valid:
        kw_scatter = {'marker': 'o', 'facecolors': 'none'}
    if (sample.sx is not None) and (sample.sy is not None):
        if len(sample.sx.drop(sample.mask_idx, axis=0)) != 0:
            plt.scatter(sample.sx.drop(sample.mask_idx, axis=0),
                        sample.sy.drop(sample.mask_idx, axis=0),
                        s=48, linewidths=0.6, label='point valid',
                        color='forestgreen', **kw_scatter)
        if ((len(sample.sx.iloc[sample.mask_idx]) != 0)
                and (list(sample.mask_idx) != list(sample.na_idx))):
            plt.scatter(sample.sx.iloc[sample.mask_idx], sample.sy.iloc[sample.mask_idx],
                        s=48, linewidths=0.8, label='point masked', color='r', **kw_scatter)


def draw_ext(fit_res: ImageFitResult, sample: SampleData, interval_ratio: float):
    """Draw extension of fitted curve.

    Parameters
    ----------
    fit_res : ImageFitResult
        Fit result.
    sample : SampleData
        Sample data.
    interval_ratio: float
        Ratio of min and max extention of x axis for fitted curve plot.
    """
    num_pts = 400
    t = np.arange(fit_res.x.min(), fit_res.x.max(),
                  (fit_res.x.max() - fit_res.x.min()) / num_pts)
    plt.plot(t, func(t, *fit_res.popt), color='slategray', linewidth=0.2)

    sx_n = sample.sx[~sample.sx.isna()] if sample.sx is not None else None
    x_min_ext = fit_res.x.min() / interval_ratio
    if sample.sx is not None:
        x_min_ext = min(x_min_ext, sx_n.min())
    ext_legend = False
    if fit_res.x.min() != x_min_ext:
        t = np.arange(x_min_ext, fit_res.x.min(),
                      (fit_res.x.min() - x_min_ext) / (num_pts / 10.0))
        plt.plot(t, func(t, *fit_res.popt), color='red',
                 linestyle=(0, (5, 10)), linewidth=0.2, label='ext')
        ext_legend = True

    x_max_ext = fit_res.x.max() * interval_ratio
    if sample.sx is not None:
        x_max_ext = max(x_max_ext, sx_n.max())
    if fit_res.x.max() != x_max_ext:
        t = np.arange(fit_res.x.max(), x_max_ext,
                      (x_max_ext - fit_res.x.max()) / (num_pts / 10.0))
        # no label, only one extension label
        ext_label = None
        if not ext_legend:
            ext_label = 'ext'
        plt.plot(t, func(t, *fit_res.popt), color='red',
                 linestyle=(0, (5, 10)), linewidth=0.2, label=ext_label)

    return x_min_ext, x_max_ext


def draw_fit(fit_res: ImageFitResult):
    """Draw fitted curve.

    Parameters
    ----------
    fit_res : ImageFitResult
        Fit result.
    """
    if len(fit_res.x.drop(fit_res.rm_index, axis=0)) != 0:
        plt.scatter(fit_res.x.drop(fit_res.rm_index, axis=0),
                    fit_res.y.drop(fit_res.rm_index, axis=0), marker='+',
                    color='royalblue', s=48, linewidths=0.8, label='reference')
    if len(fit_res.x.iloc[fit_res.rm_index]) != 0:
        plt.scatter(fit_res.x.iloc[fit_res.rm_index],
                    fit_res.y.iloc[fit_res.rm_index], marker='.',
                    color='r', s=48, linewidths=0.8, label='reference masked')
    plt.xscale('log')


def check_no_data(data):
    """Check if data is None and return empty list.
    """
    if data is None:
        data = []
    return data


def fit_image(fit_res: ImageFitResult,
              sample: SampleData,
              confidence_interval=95.0,
              confidence=None, interval_ratio=2.0):
    r"""Plot the fitted function with confidence intervals.

    Confidence intervals coud be set using `confidence` parameter.
    'student-t' method is a correct one producing wider confidence intervals.

    Parameters
    ----------
    fit_res : ImageFitResult
        Fit result.
    sample : SampleData
        Sample data.
    confidence_interval : float 
        Confidence interval in %
    interval_ratio: float
        Ration of min and max extention of x axis for fitted curve plot.
    confidence : None, 'student-t', 'sqrt_err'
        Confidence intervals method.
    """
    check_no_data(fit_res.rm_index)
    check_no_data(sample.mask_idx)
    check_no_data(sample.na_idx)

    draw_sample(sample)
    draw_fit(fit_res)
    x_min_ext, x_max_ext = draw_ext(fit_res, sample, interval_ratio)

    # show NaN concentration values somewhere -> show OD
    sx_na = sample.sx[sample.sx.isna()] if sample.sx is not None else None
    if sample.sx is not None:
        sample.na_idx = sample.sx[~sample.sx.isna()].index
        if len(sx_na) != 0:
            x_na = np.full(shape=len(sx_na), fill_value=x_min_ext * 0.5)
            y_na = sample.sy.drop(sample.na_idx, axis=0)
            plt.scatter(x_na, y_na, marker='_', color='red', s=48,
                        linewidths=0.8, label='backfit failed')
    plt.xlabel('concentration [cp/ml]')
    plt.ylabel('Optical density')

    t = np.arange(x_min_ext, x_max_ext, (x_max_ext - x_min_ext) / 256)
    if confidence is None or confidence == 'student-t':
        popt_low, popt_high = confidence_intervals_studentt(
            fit_res.y, fit_res.popt, fit_res.pcov, confidence_interval)
    else:
        popt_low, popt_high = confidence_intervals(fit_res.pcov, fit_res.popt)
    # plotting the confidence intervals
    plt.fill_between(t,
                     func(t, *popt_low), func(t, *popt_high),
                     color='black', alpha=0.15)
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='svg')
    buf.seek(0)
    plt.clf()

    return buf


def save_image(buf, file_path):
    """Save image to file

    Parameters
    ----------
    buf : io.BytesIO
        Image buffer.
    file_path : path_like
        Image file path.
    """
    with open(file_path, 'wb') as f:
        f.write(buf.getbuffer())


def confidence_intervals(pcov, popt):
    """Compute confidence intervals using covariance matrix."""
    perr = np.sqrt(np.diag(pcov))
    popt_high = popt + perr
    popt_low = popt - perr
    return popt_low, popt_high


def confidence_intervals_studentt(y, popt, pcov, confidence_interval):
    """Compute confidence intervals using student-t distribution."""
    alpha = (100.0 - confidence_interval) / 100.0
    n = len(y)    # number of data points
    p = len(popt)  # number of parameters
    dof = max(0, n - p)  # number of degrees of freedom

    # student-t value for the dof and confidence level
    tval = distributions.t.ppf(1.0 - alpha / 2., dof)
    sigma_popt = np.empty(p, dtype=np.float64)
    for i, var in zip(range(n), np.diag(pcov)):
        sigma = var ** 0.5
        st = sigma * tval
        sigma_popt[i] = st

    return popt - sigma_popt, popt + sigma_popt


def mask_index(df: pd.DataFrame, key: str = 'mask_reason') -> list:
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
    b = b[b[key].notna()]

    return b.index


def na_index(df: pd.DataFrame, key: str = 'backfit') -> list:
    """Get index of `na` data
    """
    b = df.reset_index(level=[0, 1])
    b = b[b[key].isna()]

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
    nai = na_index(sd['sample'])
    sample_data = SampleData(
        sx=sx, sy=sy, mask_idx=mask_idx, na_idx=nai, valid=sd['valid'])
    img = fit_image(ImageFitResult(x, y, fit_result[0][0], fit_result[0][1], fit_result[1]),
                    sample_data,
                    confidence='student-t',
                    interval_ratio=1.0)
    if img_file:
        save_image(img, img_file)

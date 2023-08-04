import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import distributions

from .sample import sample_check
from .fitdata import fit_reference_auto_rm, func

def fit_image(x, y, popt, pcov, file_path, confidence_interval=95.0,
    confidence=None, interval_ratio=2.0,
    rm_index=[],
    sx=None, sy=None, mask_index=[], sna_idx=[],
    verbose=False, valid_sample=True, show=True):
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
    mask_index : array_like
        Indices of masked samples.
    verbose : bool
        Print verbose output.
    show : bool
        Show the graph. If `False` image is saved if file path is given. 
    """

    # confidence [None, 'student-t', 'sqrt_err'] 
    if verbose:
        print('parameter', popt)
    perr = np.sqrt(np.diag(pcov))
    sigma_err = 1.0
    chisq = np.sum((perr / sigma_err) ** 2)
    if verbose:
        print('chisq={0:.4}; error={1}'.format(np.sqrt(chisq), perr))
        # print('function calls', infodict['nfev'])

    kwargs = { 'marker': 'x'}
    if not valid_sample:
        kwargs = { 'marker': 'o', 'facecolors':'none'}
    if (sx is not None) and (sy is not None):
        if len(sx.drop(mask_index, axis=0)) != 0:
            plt.scatter(sx.drop(mask_index, axis=0), sy.drop(mask_index, axis=0),
                        s=48, linewidths=0.6, label='sample valid', color='forestgreen', **kwargs)
        if (len(sx.iloc[mask_index]) != 0) and (list(mask_index) != list(sna_idx)):
            plt.scatter(sx.iloc[mask_index], sy.iloc[mask_index],
                        s=48, linewidths=0.8, label='sample masked', color='r', **kwargs)

    if len(x.drop(rm_index, axis=0)) != 0:
        plt.scatter(x.drop(rm_index, axis=0), y.drop(rm_index, axis=0), marker='+',
                color='royalblue', s=48, linewidths=0.8, label='reference')
    if len(x.iloc[rm_index]) != 0:
        plt.scatter(x.iloc[rm_index], y.iloc[rm_index], marker='.',
                color='r', s=48, linewidths=0.8, label='reference masked')
    plt.xscale('log')
    
    alpha = (100.0 - confidence_interval) / 100.0 
    n = len(y)    # number of data points
    p = len(popt) # number of parameters
    dof = max(0, n - p) # number of degrees of freedom

    # student-t value for the dof and confidence level
    tval = distributions.t.ppf(1.0 - alpha / 2., dof) 
    sigma_popt = np.empty(len(popt), dtype=np.float64)
    param_names = ['a', 'b', 'c', 'd']
    for i, p, var, pname in zip(range(n), popt, np.diag(pcov), param_names):
        sigma = var ** 0.5
        st = sigma * tval
        sigma_popt[i] = st
        if verbose:
            print('{0}: {1:.3} [{2:.3}, {3:.3}]; err={4:.3}[{5:.2f}%]'.format(pname, p, p - st, p + st, st, 100*st/p))

    if confidence==None or confidence=='student-t':
        if verbose: print('student-t is used for error estimation using {} degrees of freedom'.format(dof))
        popt_high = popt + sigma_popt
        popt_low = popt - sigma_popt
    else:
        if verbose: print('sqrt of covariance matrix diagonal is used for error estimation')
        popt_high = popt + perr
        popt_low = popt - perr

    num_pts = 400
    x_min = x.min()
    x_max = x.max()
    t = np.arange(x_min, x_max, (x_max - x_min) / num_pts)
    plt.plot(t, func(t, *popt), color='slategray', linewidth=0.2)

    sx_n = sx[~sx.isna()] if sx is not None else None
    x_min_ext = x.min() / interval_ratio
    if sx is not None: x_min_ext = min(x_min_ext, sx_n.min())
    if x_min != x_min_ext:
        t = np.arange(x_min_ext, x_min, (x_min - x_min_ext) / (num_pts / 10.0))
        plt.plot(t, func(t, *popt), color='red', linestyle=(0, (5, 10)), linewidth=0.2, label='ext')

    x_max_ext = x.max() * interval_ratio
    if sx is not None: x_max_ext = max(x_max_ext, sx_n.max())
    if x_max != x_max_ext:
        t = np.arange(x_max, x_max_ext, (x_max_ext - x_max) / (num_pts / 10.0))
        # no label, only one extension labe
        plt.plot(t, func(t, *popt), color='red', linestyle=(0, (5, 10)), linewidth=0.2)

    # show NaN concentration values somewhere -> show OD
    sx_na = sx[sx.isna()] if sx is not None else None
    if sx is not None:
        if verbose: print("NaN indices:", sx_na.index)
        sna_idx = sx[~sx.isna()].index
        if len(sx_na) != 0:
            x_na = np.full(shape=len(sx_na), fill_value=x_min_ext * 0.5)
            y_na = sy.drop(sna_idx, axis=0)
            plt.scatter(x_na, y_na, marker='_', color='red', s=48, linewidths=0.8, label='backfit failed')

    plt.xlabel('concentration [cp/ml]')
    plt.ylabel('Optical density')

    t = np.arange(x_min_ext, x_max_ext, (x_max_ext - x_min_ext) / num_pts)
    bound_upper = func(t, *popt_high)
    bound_lower = func(t, *popt_low)
    # plotting the confidence intervals
    plt.fill_between(t, bound_lower, bound_upper,
                    color = 'black', alpha = 0.15)
    
    plt.legend()

    if file_path is not None:
         plt.savefig(file_path)
    if show:
        plt.show()
    else:
        plt.clf()


def mask_index(df):
    b = df.reset_index(level=[0,1])
    b = b[b['mask_reason'].notna()]

    return b.index


def na_index(df):
    b = df.reset_index(level=[0,1])
    b = b[b['backfit'].isna()]
    
    return b.index


def sample_img(samples, reference, sample_type, sample_num, img_file=None, show=True, verbose=False):
    sd = sample_check(samples, sample_type, sample_num)
    if verbose:
        print(sample_type, sample_num)

    mask_idx = mask_index(sd['sample'])
    x = reference.reset_index(level=[0,1])['plate_layout_conc']
    y = reference.reset_index(level=[0,1])['OD_delta']
    fit_result = fit_reference_auto_rm(x, y, verbose=verbose)
    # compute original concenmtration 
    sd['sample'].loc[:, ['conc_plot']] = sd['sample'].apply(lambda x: x['concentration'] / x['plate_layout_dil'], axis=1)
    sx = sd['sample'].reset_index(level=[0,1])['conc_plot']
    sy = sd['sample'].reset_index(level=[0,1])['OD_delta']
    fit_image(x, y, fit_result[0][0], fit_result[0][1], img_file, confidence='student-t',
              rm_index=fit_result[1], mask_index=mask_idx,
              sx=sx, sy=sy, sna_idx=na_index(sd['sample']), show=show, valid_sample=sd['valid'], interval_ratio=1.0)
 
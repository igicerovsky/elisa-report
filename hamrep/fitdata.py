import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from scipy.stats import distributions
from sklearn.metrics import r2_score


def func(x, a, b, c, d):
    """Fit function see SOP `220726_SOP_Capsid-AAV9-ELISA_V4` `5.1`

    Parameters
    ----------
    x : array_like
        x-axis values, $\Delta$ OD (450nm - 620nm)
    a : float
        minimum value (lowest possible point)  .
    b : float 
        slope at inflection point `c`
    c : float
        inflection point of the curve  
    d : float
        maximum value (highest possible point)

    Returns
    -------
    float64
        concentration [cp/ml]
    """
    return d + ((a - d) / (1.0 + (x / c) ** b))


def inv_func(y, a, b, c, d):
    """Inverse fit function see SOP `220726_SOP_Capsid-AAV9-ELISA_V4` `5.1`

    Parameters
    ----------
    y : array_like
        x-axis values, concentration [cp/ml]
    a : float
        minimum value (lowest possible point)  .
    b : float 
        slope at inflection point `c`
    c : float
        inflection point of the curve  
    d : float
        maximum value (highest possible point)

    Returns
    -------
    float64
         $\Delta$ OD (450nm - 620nm)
    """
    return c * (((a - d) / (y - d)) - 1.0) ** (1.0 / b)


def fit_reference(fnc, x, y):
    """Fit data to reference according to SOP `220726_SOP_Capsid-AAV9-ELISA_V4` `5.1`

    Parameters
    ----------
    x : array_like
        x data
    y : array_like
        y data
    a : float

    Returns
    -------
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
    """
    p0 = [y.min(), 0.9, x[len(x) - 2], y.max()]
    return curve_fit(fnc, x, y, p0=p0, method='lm', full_output=True, maxfev=10000)


def conc_func(x, dil, *popt):
    """Function computing concentration

    Parameters
    ----------
    x : array_like
        x data
    dil : float
        dilution
    popt : 2D-array
        fit equation parameters

    Returns
    -------
    float64
        Inverse concentration value
    """
    return inv_func(x, *popt) * dil


def fit_sheet(popt, pcov, n, confidence_interval=95.0):
    """Generate dataframe with fit parameters and errors

    Parameters
    ----------
    popt : array
        fit parameters as output from fitting function
    pcov : 2-D array
        covariance matrix returned from nonlinear fitting
    n : int
        length of data used in fit function used to compute degrees of freedom
    confidence_interval : float64
        confidence interval in percent, by default 95%

    Returns
    -------
    Pandas dataframe contaning fit parameters and corresponding errors for tabular output
    """

    # `confidence_interval` 95% confidence interval = 100*(1-alpha)
    alpha = (100.0 - confidence_interval) / 100.0
    p = len(popt)  # number of parameters
    dof = max(0, n - p)  # number of degrees of freedom

    # student-t value for the dof and confidence level
    tval = distributions.t.ppf(1.0 - alpha / 2.0, dof)

    sigma_popt = np.empty(len(popt), dtype=np.float64)
    confidence_interval = [None] * 4
    for i, p, var in zip(range(n), popt, np.diag(pcov)):
        sigma = var ** 0.5
        st = sigma * tval
        sigma_popt[i] = st
        confidence_interval[i] = '[{0:.3}, {1:.3}]'.format(p - st, p + st)

    param_names = ['a', 'b', 'c', 'd']
    perr = np.sqrt(np.diag(pcov))

    return pd.DataFrame({'Parameter name': param_names, 'Estimated value': popt,
                         'Error': perr, 'Confidence interval': confidence_interval})


def backfit(df, param):
    """Computes backfit for reference dataframe

    Parameters
    ----------
    df : pandas.dataframe
        datframe with reference cutve
    param : array
        fit parameters

    Returns
    -------
    pandas.dataframe
        backfit dataframe for report
    """

    bf = df[['OD_delta', 'plate_layout_conc']].copy()
    bf = bf.reindex(['plate_layout_conc', 'OD_delta'], axis=1)
    bf.rename(columns={
              'plate_layout_conc': 'Standard Value [cp/ml]', 'OD_delta': 'Optical density'}, inplace=True)
    bf.loc[:, ['Concentration backfit [cp/ml]']
           ] = bf.apply(lambda x: inv_func(x['Optical density'], *param), axis=1)
    bf.loc[:, ['SV to OD fit']] = bf.apply(
        lambda x: func(x['Standard Value [cp/ml]'], *param), axis=1)
    bf.index.name = 'Well'
    bf = bf.reindex(['Standard Value [cp/ml]', 'Concentration backfit [cp/ml]',
                    'Optical density', 'SV to OD fit'], axis=1)
    bf.loc[:, ['Recovery rate [%]']] = bf.apply(lambda x: (
        x['Concentration backfit [cp/ml]'] / x['Standard Value [cp/ml]']) * 100.0, axis=1)

    return bf


def fit_reference_auto_rm(x, y, err_threshold=0.998, verbose=False):
    """Fits the reference and removes a point to fing min error

    Parameters
    ----------
    x : array_like
        x-axis values.
    y : array_like
        y-axis value.
    err_threshold : float64
        error threshold to to skip point removal
    verbose :  boolean
        verbose output

    Returns
    -------
    array
        parameters of the filt
    int
        index of the removed point, -1 if no point is removed
    float64
        error
    pandas dataframe
        fit statistics as dataframe
    """

    fit_stats = pd.DataFrame(columns=['idx', 'metric', 'note'])
    fc = None
    try:
        fc = fit_reference(func, x, y)
    except Exception as e:
        estr = '{0}, {1} Reason: {2}'.format(np.nan, -1, str(e))
        if verbose:
            print(e)

    idx = []
    r2_max = 0.0
    if fc:
        def bfn(l): return inv_func(l, *fc[0])
        x_hat = bfn(y)
        try:
            r2_max = r2_score(x, x_hat)
        except:
            r2_max = 0.0

    if verbose:
        print('R-squared is invalid for nonlinear models!')
        print('metric, index')
        print('{0:.5f}, {1}'.format(r2_max, idx))

    if r2_max > err_threshold:
        fit_stats.loc[len(fit_stats)] = [-1, r2_max, '']
        return fc, idx, r2_max, fit_stats
    elif r2_max == 0.0:
        fit_stats.loc[len(fit_stats)] = [-1, np.nan, '']
    else:
        fit_stats.loc[len(fit_stats)] = [-1, r2_max,
                                         'metric < threshold ({:.3f} < {:.3f})'.format(r2_max, err_threshold)]

    for i in range(len(x)):
        xd = x.drop([i], axis=0)
        yd = y.drop([i], axis=0)
        try:
            fc_i = fit_reference(func, xd.to_numpy(), yd.to_numpy())
        except Exception as e:
            estr = '{0}, {1} Reason: {2}'.format(np.nan, [i], str(e))
            if verbose:
                print(e)
            fit_stats.loc[len(fit_stats)] = [i, np.nan, str(e)]
            continue

        def bfn(l): return inv_func(l, *fc_i[0])
        x_hat = bfn(yd)
        try:
            r_squared = r2_score(xd, x_hat)
        except:
            fit_stats.loc[len(fit_stats)] = [i, r_squared,
                                             'Invalid covariance matrix.']
            continue

        if np.isinf(fc_i[1]).any():
            fit_stats.loc[len(fit_stats)] = [i, r_squared,
                                             'Invalid covariance matrix.']
            continue

        fit_stats.loc[len(fit_stats)] = [i, r_squared, '']
        if verbose:
            print('{0:.3f}, {1}'.format(r_squared, i))
        if (r_squared > r2_max) and not np.isinf(fc_i[1]).any():
            r2_max = r_squared
            fc = fc_i
            idx = [i]

    fit_stats.set_index('idx', inplace=True)
    fit_stats.loc[idx, 'note'] = 'Maximum.'

    return fc, idx, r2_max, fit_stats

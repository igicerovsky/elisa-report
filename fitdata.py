import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd


def func(x, a, b, c, d):
    return d + ((a - d) / (1.0 + (x / c) ** b))


def inv_func(y, a, b, c, d):
    return c * (((a - d) / (y - d)) - 1.0) ** (1.0 / b)


def fit_reference(func, x, y):
    p0 = [y.min(), 0.9, x[len(x) - 2], y.max()]
    return curve_fit(func, x, y, p0=p0, method='lm', full_output=True, maxfev=10000)


def fit_magic(data):
    popt, pcov, infodict, mesg, ier = fit_reference(func,
        data['Conc'], data['OD'])
    
    print(popt)
    perr = np.sqrt(np.diag(pcov))
    print(perr)


    plt.scatter(data['Conc'], data['OD'], marker='+', s=48, linewidths=0.8)
    plt.xscale('log')

    num_pts = 100
    t = np.arange(data['Conc'].min(), data['Conc'].max(), (data['Conc'].max() - data['Conc'].min()) / num_pts)
    plt.plot(t, func(t, *popt), 'r-',
             label='fit: a=%f, b=%f, c=%f, d=%f' % tuple(popt),
             linewidth=0.4)
    plt.xlabel('conc [?cp/ml]')
    plt.ylabel('OD [?unit]')
    plt.show()


""" Sample handling
"""
from enum import Enum
from itertools import combinations

import math

from decimal import Decimal
import numpy as np
import pandas as pd
from scipy.stats import variation

from .constants import RESULT_DIGITS, MIN_VALID_SAMPLE_POINTS, SAMPLE_TYPES
from .constants import CV_THRESHOLD, PRE_DILUTION_THRESHOLD
from .fitdata import conc_func, inv_func, backfit, DataRange


def get_sample(dfa: pd.DataFrame, stype: str, sample_num: int) -> pd.DataFrame:
    """ Get sample
    """
    if stype not in SAMPLE_TYPES:
        raise ValueError(f'Invalid sample type: {stype}')
    dfa = dfa.loc[(dfa['plate_layout_ident'] == stype) &
                  (dfa['plate_layout_num'] == sample_num)]
    return dfa


def make_concentration(ref_val_max: float, dilution: list) -> pd.DataFrame:
    """ Create concentration dataframe
    """
    conc = pd.DataFrame({'dilution': dilution})
    conc.loc[:, ['concentration']] = conc.apply(
        lambda x: ref_val_max / x['dilution'], axis=1)
    conc.index = range(1, len(dilution) + 1)
    return conc


def sample_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """ Get sorted sample numbers
    """
    sample_nums = df['plate_layout_num'].astype(int).unique()
    sample_nums.sort()
    return sample_nums


def mask_value_fn(val, odmin, odmax, note):
    """ Masking function
    """
    dgts = RESULT_DIGITS
    if val < odmin:
        return f'{note} {Decimal(val):.{dgts}e} < {Decimal(odmin):.{dgts}e}'
    if val > odmax:
        return f'{note} {Decimal(val):.{dgts}e} > {Decimal(odmax):.{dgts}e}'
    if math.isnan(val):
        return 'NaN'
    return None


def mask_value_short_fn(val, vmin, vmax, dil):
    """ Masking function 
    """
    ex = False
    if val < vmin:
        if ex:
            v = Decimal(vmin * dil)
            return f'<{v:.{RESULT_DIGITS}e}'
        return '<LOQ'
    if val > vmax:
        if ex:
            v = Decimal(vmax * dil)
            return f'>{v:.{RESULT_DIGITS}e}'
        return '>ULOQ'
    if math.isnan(val):
        return 'Backfit failed.'
    return None


def mask_sample_cv(df_in: pd.DataFrame, valid_pts: list, cv_threshold: float):
    """ Aply masking to a sample
    """
    df = df_in[df_in['mask_reason'].isna()]
    cv_min = cv_threshold  # variation(df['concentration'], ddof=1)
    non_mask_idx = []
    indices = df.index
    if len(indices) <= valid_pts:
        return [], [], cv_min

    # Reverse combinations order to break if `CV` < `cv_threshold`
    for l in reversed(range(valid_pts, len(indices) + 1)):
        for subset in combinations(indices, l):
            comb = list(subset)
            t = df.loc[comb]
            cv = variation(t['concentration'], ddof=1)
            if cv < cv_min:
                non_mask_idx = comb
                cv_min = cv
        # break if CV drops below threshold
        if cv_min < cv_threshold:
            break

    mask_idx = list(set(indices).symmetric_difference(non_mask_idx))
    return mask_idx, non_mask_idx, cv_min


def process_sample(samples, stype, sample_num):
    """ Process a sample
    """
    sample = get_sample(samples, stype, sample_num)
    smp_t = sample[sample.mask_reason.isna()]
    cv = np.nan
    mean = np.nan

    if len(smp_t['concentration']) > 1:
        cv = variation(smp_t['concentration'], ddof=1)
        mean = np.mean(smp_t['concentration'])
    elif len(smp_t['concentration']) == 1:
        mean = np.mean(smp_t['concentration'])

    return sample, cv, mean


def sample_check(samples, stype, sample_num, cv_thresh=CV_THRESHOLD,
                 min_valid_pts=MIN_VALID_SAMPLE_POINTS):
    """ Check sample for validity
    """
    s = process_sample(samples, stype, sample_num)
    valid = True
    note = ''
    if s[1] > cv_thresh:
        note = f'CV > {cv_thresh}; '
        valid = False
    smp = s[0]
    valid_pts = smp['mask_reason'].isna().sum()
    if valid_pts < min_valid_pts:
        note += (f'Not enough valid sample points. '
                 f'Required {min_valid_pts}, available {valid_pts};')
        valid = False
    elif valid_pts != len(smp['mask_reason']):
        note += (f'Reduced number of sample points. '
                 f'Measured {len(smp["mask_reason"])}, valid {valid_pts};')
        valid &= True

    note_cols = smp[~smp['mask_reason'].isna()]
    if len(note_cols) != 0:
        if (note_cols['mask_reason'] == note_cols['mask_reason'].iloc[0]).all():
            if note_cols['mask_reason'].iloc[0]:
                note += note_cols['mask_reason'].iloc[0]
            if note_cols['od_mask_reason'].iloc[0]:
                note += ';' + note_cols['od_mask_reason'].iloc[0]

    return {'sample': smp, 'cv': s[1], 'mean': s[2],
            'note': note, 'type': stype, 'num': sample_num,
            'valid': valid, 'valid_pts': valid_pts}


class SampleInfo(str, Enum):
    """ SampleInfo data class.
    """
    NAN_LOW = 'NaN below reference'
    NAN_HIGH = 'NaN above reference'
    LOW = 'value below reference'
    HIGH = 'value above reference'
    CV = 'CV above threshold'
    VALID_PTS = 'few valid points'
    LIMITS_3S = 'test invalid'


def sampleinfo_to_str(info, multiplier=1.0):
    """ Convert sample info to string
    """
    if info is None:
        return None

    if not info:
        return None

    if info['enum'] == SampleInfo.CV:
        return f'CV>{CV_THRESHOLD * 100:.1f}%({float(info["value"]) * 100.0:.1f}%)'

    if info['enum'] == SampleInfo.VALID_PTS:
        return f'{info["value"]} valid point'

    if info['enum'] == SampleInfo.LIMITS_3S:
        return 'test invalid'

    return f'{info["sign"]}{float(info["value"]) * multiplier:.4e}'


def sample_info(samples: pd.DataFrame, stype: str, sample_num: int, dr: DataRange) -> dict:
    """ Generate sample info
    """
    s = get_sample(samples, stype, sample_num)
    sc = sample_check(samples, stype, sample_num)
    above_ref_od_max = s['OD_delta'] > dr.od_fit[1]
    below_ref_od_min = s['OD_delta'] < dr.od_fit[0]
    msgdc = {}
    if s['backfit'].isna().all():
        if above_ref_od_max.all():
            msgdc = {'sign': '>', 'value': Decimal(
                dr.sv[1]), 'enum': SampleInfo.NAN_HIGH}
        if below_ref_od_min.all():
            msgdc = {'sign': '<', 'value': Decimal(
                dr.sv[0]), 'enum': SampleInfo.NAN_LOW}
    elif sc['cv'] > CV_THRESHOLD:
        msgdc = {'sign': f'>{CV_THRESHOLD:.2f}',
                 'value': sc['cv'], 'enum': SampleInfo.CV}
    elif not s['mask_reason'].isna().all():
        t = s[['OD_delta', 'plate_layout_dil', 'concentration', 'backfit']]
        t_not_na = t[~t['backfit'].isna()]

        if t_not_na['OD_delta'].max() < dr.od_fit[0]:
            msgdc = {'sign': '<', 'value': Decimal(
                dr.sv[0]), 'enum': SampleInfo.LOW}
            # dr.sv[0] * sc['sample']['plate_layout_dil'].min()), 'enum': SampleInfo.LOW}
        elif t_not_na['OD_delta'].min() > dr.od_fit[1]:
            msgdc = {'sign': '>', 'value': Decimal(
                # dr.sv[1] * sc['sample']['plate_layout_dil'].max()), 'enum': SampleInfo.HIGH}
                dr.sv[1]), 'enum': SampleInfo.HIGH}

    if sc['valid_pts'] < MIN_VALID_SAMPLE_POINTS and sc['valid_pts'] != 0:
        msgdc = {'sign': '',
                 'value': sc['valid_pts'], 'enum': SampleInfo.VALID_PTS}

    del sc['sample']
    del sc['note']
    sc['info'] = msgdc

    return sc


def control_info(val: float, limits: tuple) -> dict:
    """ Create info for control sample
    """
    msgdc = {}
    if not limits:
        raise AttributeError('Please provide controll limits!')
    if val < limits[0]:
        msgdc = {'sign': '<',
                 'value': limits[0], 'enum': SampleInfo.LIMITS_3S}
    elif val > limits[1]:
        msgdc = {'sign': '>',
                 'value': limits[1], 'enum': SampleInfo.LIMITS_3S}
    return msgdc


def final_sample_info(all_info, pre_dilution, limits):
    """ Final table info assembly
    """
    if not all_info:
        raise AttributeError("Invalid sample info!")
    info = all_info['info']
    # check 3s limits
    if all_info['type'] == 'k':
        info = control_info(all_info['mean'] * pre_dilution, limits)

    if not info:
        return '', True

    msg = ''
    valid_ex = False
    if info['enum'] == SampleInfo.NAN_HIGH:
        msg = f'>{info["value"] * pre_dilution:.{RESULT_DIGITS}e}'
    elif info['enum'] == SampleInfo.NAN_LOW or info['enum'] == SampleInfo.LOW:
        if pre_dilution <= PRE_DILUTION_THRESHOLD:
            valid_ex = True
            msg = f'<{info["value"] * pre_dilution:.{RESULT_DIGITS}e}'
        else:
            valid_ex = False
            msg = f'<{info["value"] * pre_dilution:.{RESULT_DIGITS}e}'
    elif info['enum'] == SampleInfo.HIGH:
        msg = f'>{info["value"] * pre_dilution:.{RESULT_DIGITS}e}'
    elif info['enum'] == SampleInfo.VALID_PTS:
        msg = f'{all_info["valid_pts"]} valid point'
    elif info['enum'] == SampleInfo.CV:
        msg = f'CV>{CV_THRESHOLD * 100.0:.1f}%({info["value"] * 100.0:.1f}%)'
    elif info['enum'] == SampleInfo.LIMITS_3S:
        msg = 'test invalid'
    else:
        msg = ''
        valid_ex = True

    return msg, valid_ex


def generate_results(df_data, datarange):
    """ Compute results
    """
    dfres = pd.DataFrame(
        columns=['id', 'CV [%]', 'Reader Data [cp/ml]', 'Note', 'Valid', 'info'])
    knum = 1
    s = sample_check(df_data, 'k', knum)
    si = sample_info(df_data, 'k', knum, datarange)
    dfres.loc[len(dfres)] = [
        f'control {knum:02d}', s['cv'], s['mean'], s['note'], s['valid'], si]

    rnum = 1
    s = sample_check(df_data, 'r', rnum)
    si = sample_info(df_data, 'r', knum, datarange)
    dfres.loc[len(dfres)] = [
        f'reference {knum:02d}', s['cv'], s['mean'], s['note'], s['valid'], si]

    for i in sample_numbers(df_data):
        stype = 's'
        s = sample_check(df_data, stype, i)
        si = sample_info(df_data, stype, i, datarange)
        dfres.loc[len(dfres)] = [f'sample {i:02d}',
                                 s['cv'], s['mean'], s['note'], s['valid'], si]

    dfres.set_index(dfres['id'], inplace=True)
    dfres = dfres.drop('id', axis=1)

    return dfres


def data_range(ref, popt):
    """ Retrieve data ranges
    """
    bf = backfit(ref, popt)

    od_min = bf['Optical density'].min()
    od_max = bf['Optical density'].max()

    od_fit_min = bf['SV to OD fit'].min()
    od_fit_max = bf['SV to OD fit'].max()

    sv_min = bf['Standard Value [cp/ml]'].min()
    sv_max = bf['Standard Value [cp/ml]'].max()

    cb_min = bf['Concentration backfit [cp/ml]'].min()
    cb_max = bf['Concentration backfit [cp/ml]'].max()

    return DataRange((sv_min, sv_max),
                     (od_min, od_max),
                     (od_fit_min, od_fit_max),
                     (cb_min, cb_max))


def apply_fit(df, popt):
    """ Apply fit function to OD value
    """
    df.loc[:, ['concentration']] = df.apply(lambda x: conc_func(
        x['OD_delta'], x['plate_layout_dil'], *popt), axis=1)
    df.loc[:, ['backfit']] = df.apply(
        lambda x: inv_func(x['OD_delta'], *popt), axis=1)

    return df


def init_samples(df, reference_conc):
    """ Generate samples info
    """
    skr = df.loc[(df['plate_layout_ident'] == 's')
                 | (df['plate_layout_ident'] == 'k')
                 | (df['plate_layout_ident'] == 'r')
                 ]
    skr.loc[:, ['plate_layout_dil']] = skr['plate_layout_dil_id'].map(
        reference_conc['dilution'])
    skr.loc[:, ['plate_layout_conc']] = skr['plate_layout_dil_id'].map(
        reference_conc['concentration'])

    return skr


def mask_sample(df, dr):
    """ Mask sample
    """
    df.loc[:, ['od_mask_reason']] = df.apply(
        lambda x: mask_value_fn(
            x['OD_delta'], dr.od[0], dr.od[1], 'Measured OD'),
        axis=1)
    df.loc[:, ['mask_reason']] = df.apply(
        lambda x: mask_value_short_fn(
            x['backfit'], dr.cb[0], dr.cb[1], x['plate_layout_dil']),
        axis=1)

    # mask samples for CV < threshold, controll is considered normal sample
    sample = get_sample(df, 'k', 1)
    mask_idx, _, _ = mask_sample_cv(
        sample, MIN_VALID_SAMPLE_POINTS, CV_THRESHOLD)
    df.loc[mask_idx, ['mask_reason']] = "cv-masked"

    for i in sample_numbers(df):
        sample = get_sample(df, 's', i)
        mask_idx, _, _ = mask_sample_cv(
            sample, MIN_VALID_SAMPLE_POINTS, CV_THRESHOLD)
        df.loc[mask_idx, ['mask_reason']] = "cv-masked"

    return df

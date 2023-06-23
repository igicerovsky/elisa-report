import pandas as pd
from decimal import Decimal
import math
from scipy.stats import variation
import constants as cc
import numpy as np
from enum import Enum
from dataclasses import dataclass
import typing

@dataclass
class DataRange:
    sv: typing.Tuple[int, int]
    od: typing.Tuple[int, int]
    od_fit: typing.Tuple[int, int]
    cb: typing.Tuple[int, int]


def get_sample(dfa, type, sample_num):
    # TODO: check for valid `type` `and sample_num`
    dfa = dfa.loc[(dfa['plate_layout_ident']==type) & (dfa['plate_layout_num']==sample_num)]
    return dfa


def make_concentration(ref_val_max, dilution):
    conc  = pd.DataFrame({'dilution': dilution})
    conc.loc[:, ['concentration']] = conc.apply(lambda x: ref_val_max / x['dilution'], axis=1)
    conc.index = range(1, len(dilution) + 1)
    return conc


def unique_sample_numbers(df):
    sample_nums = df['plate_layout_num'].astype(int).unique()
    sample_nums.sort()
    return sample_nums


def mask_reason_fn(val, odmin, odmax, note):
    if val < odmin:
        return '{2} {0:.3e} < {1:.3e}'.format(Decimal(val), Decimal(odmin), note)
    if val > odmax:
        return '{2} {0:.3e} > {1:.3e}'.format(Decimal(val), Decimal(odmin), note)
    if math.isnan(val):
        return 'NaN'
    return None


def mask_reason_short_fn(val, vmin, vmax, dil, note):
    if val < vmin:
        return '<{:.3e}'.format(Decimal(vmin * dil))
    if val > vmax:
        return '>{:.3e}'.format(Decimal(vmax * dil))
    if math.isnan(val):
        return 'Backfit failed.'
    return None


def process_sample(samples, stype, sample_num):
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


def sample_check(samples, stype, sample_num, cv_thresh=cc.CV_THRESHOLD,
                 min_valid_pts=cc.MIN_VALID_SAMPLE_POINTS):
    s = process_sample(samples, stype, sample_num)
    valid = True
    note = ''
    if s[1] > cv_thresh:
        note = 'CV > {}; '.format(cv_thresh)
        valid = False
    smp = s[0]
    valid_pts = smp['mask_reason'].isna().sum()
    if valid_pts < min_valid_pts:
        note += 'Not enough valid sample points. Required {}, available {};'.format(min_valid_pts, valid_pts)
        valid = False
    elif valid_pts != len(smp['mask_reason']):
        note += 'Reduced number of sample points. Measured {}, valid {};'.format(len(smp['mask_reason']), valid_pts)
        valid &= True

    note_cols = smp[~smp['mask_reason'].isna()]
    if len(note_cols)!= 0:
        if (note_cols['mask_reason'] == note_cols['mask_reason'][0]).all():
            note += note_cols['mask_reason'][0] + ';' + note_cols['od_mask_reason'][0]
        # else:
        #     note += note_cols['mask_reason'].str.cat(sep=', ')

    return {'sample':smp, 'cv':s[1], 'mean':s[2], 'note':note, 'type':stype, 'num':sample_num, 'valid':valid, 'valid_pts': valid_pts}


class SampleInfo(str, Enum):
    NAN_LOW = 'NaN below reference'
    NAN_HIGH = 'NaN above reference'
    LOW = 'value below reference'
    HIGH = 'value above reference'
    CV = 'CV above threshold'
    VALID_PTS = 'few valid points'


def sampleinfo_to_str(info, multiplier=1.0):
    if info is None:
        return None

    if not info:
        return None;
    
    if info['enum'] == SampleInfo.CV:
        return 'CV>{:.1f}%({:.1f}%)'.format(cc.CV_THRESHOLD * 100, float(info['value']) * 100.0)

    if info['enum'] == SampleInfo.VALID_PTS:
        return '{} valid point'.format(info['value'])

    return '{}{:.4e}'.format(info['sign'], float(info['value']) * multiplier)


def sample_info(samples, stype, sample_num, dr: DataRange, verbose=False):
    s = get_sample(samples, stype, sample_num)
    sc = sample_check(samples, stype, sample_num)
    if verbose:
        print('OD=[{}, {}]'.format(dr.od[0], dr.od[1]))
        print('OD_fit=[{:.3}, {:.3}]'.format(Decimal(dr.od_fit[0]), Decimal(dr.od_fit[1])))
        print('SV=[{:.3e}, {:.3e}]'.format(Decimal(dr.sv[0]), Decimal(dr.sv[1])))
        print('CB=[{}, {}]'.format(dr.cb[0], dr.cb[1]))
    above_ref_od_max = s['OD_delta'] > dr.od_fit[1]
    below_ref_od_min = s['OD_delta'] < dr.od_fit[0]
    msgdc = {}
    if s['backfit'].isna().all():
        if above_ref_od_max.all():
            msgdc = {'sign': '>', 'value': Decimal(dr.sv[1]), 'enum': SampleInfo.NAN_HIGH}
        if below_ref_od_min.all():
            msgdc = {'sign': '<', 'value': Decimal(dr.sv[0]), 'enum': SampleInfo.NAN_LOW}
    elif sc['cv'] > cc.CV_THRESHOLD:
        msgdc = {'sign': '>{:.2f}'.format(cc.CV_THRESHOLD), 'value': sc['cv'], 'enum': SampleInfo.CV}
    elif not s['mask_reason'].isna().all():
        t = s[['OD_delta', 'plate_layout_dil', 'concentration', 'backfit']]
        t_not_na = t[~t['backfit'].isna()]
        
        if t_not_na['OD_delta'].max() < dr.od_fit[0]:
            t_below_ref = t_not_na[below_ref_od_min]
            # msgdc = {'sign': '<', 'value': t_below_ref['concentration'].max(), 'enum': SampleInfo.LOW}
            msgdc = {'sign': '<', 'value': Decimal(dr.sv[0] * sc['sample']['plate_layout_dil'].min()), 'enum': SampleInfo.LOW}
        elif t_not_na['OD_delta'].min() > dr.od_fit[1]:
            t_above_ref = t_not_na[above_ref_od_max]
            # print('*** {} *  {} = {}'.format(sv_max, sc['sample']['plate_layout_dil'].max(), sv_max * sc['sample']['plate_layout_dil'].max()))
            msgdc = {'sign': '>', 'value': Decimal(dr.sv[1] * sc['sample']['plate_layout_dil'].max()), 'enum': SampleInfo.HIGH}
    
    if sc['valid_pts'] < cc.MIN_VALID_SAMPLE_POINTS and sc['valid_pts'] != 0:
        msgdc = {'sign': '', 'value': sc['valid_pts'], 'enum': SampleInfo.VALID_PTS}

    del sc['sample']
    del sc['note']
    sc['info'] = msgdc
    
    return sc
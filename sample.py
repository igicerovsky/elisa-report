import pandas as pd
from decimal import Decimal
import math
from scipy.stats import variation
import constants as cnt
import numpy as np


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


def sample_check(samples, stype, sample_num, cv_thresh=cnt.CV_THRESHOLD,
                 min_valid_pts=cnt.MIN_VALID_SAMPLE_POINTS):
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

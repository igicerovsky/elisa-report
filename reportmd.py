import math
from os import path
from fitdata import fit_sheet, fit_reference_auto_rm, backfit
from image import fit_image, sample_img
from sample import final_sample_info, sample_check, sample_info, sampleinfo_to_str
import constants as cc
import worklist as wk
import pandas as pd
from tqdm import tqdm


def make_final(sl, wl_raw, plate_id):
    wl, cd = wk.worklist_sample(wl_raw, plate_id)

    final = pd.concat([wl, sl], axis=1)
    final.loc[:, ['Result [cp/ml]']] = final.apply(lambda x: x['Reader Data [cp/ml]'] * x[cd['Dilution']], axis=1)
    final.loc[:, ['CV [%]']] = final.apply(lambda x: x['CV [%]'] * 100, axis=1)
    # reorder columns
    final = final.reindex([cd['SampleID'], cd['Dilution'], cd['Viscosity'], 'Reader Data [cp/ml]', 'Result [cp/ml]', 'CV [%]', 'Valid', 'info'], axis=1)
    final.rename(columns={cd['SampleID']: 'Sample Name', cd['Dilution']: 'Pre-dilution'}, inplace=True)
    final.drop('Viscosity_{}'.format(plate_id), axis=1, inplace=True)
    final.index.name = 'Sample type'
    final.loc[:, ['info_ex']] = final.apply(lambda x: final_sample_info(x['info'], x['Pre-dilution'])[0], axis=1)
    final.loc[:, ['valid_ex']] = final.apply(lambda x: final_sample_info(x['info'], x['Pre-dilution'])[1], axis=1)
    return final


# Header

def header_section(date, id, plate_id, msg):
    md =  '## Header\n\n'

    md += 'Date: {}\n\n'.format(date)
    md += 'Identification: {}\n\n'.format(id)
    md += 'Plate: {}\n\n'.format(plate_id)
    md += 'Comment: {}\n\n'.format(msg)

    return md


# Parameters

def param_section(df_params):
    md =  '## Parameters\n\n'

    md += 'Parameters:\n\n' + df_params.to_markdown() + '\n\n'

    return md


# Fit reference curve

def fit_section_md(df_ref, popt, pcov, out_dir):
    x = df_ref.reset_index(level=[0,1])['plate_layout_conc']
    y = df_ref.reset_index(level=[0,1])['OD_delta']
    fit_result = fit_reference_auto_rm(x, y)
    result_img = path.join(out_dir, 'fit.svg')
    fit_image(x, y, fit_result[0][0], fit_result[0][1], result_img,
      confidence='student-t', rm_index=fit_result[1], verbose=False, show=False)
 
    n = len(x) - len(fit_result[1])
    df_fit = fit_sheet(popt, pcov, n)

    md = '## Reference Curve Fit\n\n'
    md += '$y = {d + \\frac{a - d}{{1 + (\\frac{ x }{ c })^b}} }$  \n\n'

    param_legend = """\
`y` &nbsp;&nbsp;&nbsp;$\Delta$ OD (450nm - 620nm)  
`x` &nbsp;&nbsp;&nbsp;concentration [cp/ml]  
`a` &nbsp;&nbsp;&nbsp;minimum value (lowest possible point)  
`b` &nbsp;&nbsp;&nbsp;slope at inflection point `c`  
`c` &nbsp;&nbsp;&nbsp;inflection point of the curve  
`d` &nbsp;&nbsp;&nbsp;maximum value (highest possible point)  
    """
    md += param_legend

    md += '!["alt text"](./img/fit.svg)'

    md += '\n\n'
    md += 'Verbose fitting progress, metric is R-squared:\n\n'
    md += fit_result[3].to_markdown() + '\n\n'

    md += 'Fit parameters\n\n'
    md += df_fit.to_markdown(index=False) + '\n\n'
    md += 'Backfit...'
    fit_result = fit_reference_auto_rm(x, y)
    df_backfit = backfit(df_ref, fit_result[0][0])
    md += '\n\n' + df_backfit.to_markdown() + '\n\n'

    return md


# Sample section

def sample_to_md(dc):
    s_view = dc['sample'][['OD_delta', 'plate_layout_dil', 'concentration', 'mask_reason']]
    md = "### Sample: {0} '{1}' {2}\n\n".format(cc.SAMPLE_TYPES[dc['type']], dc['type'], dc['num'])
    md += s_view.to_markdown()
    md += '\n\n'
    md += "CV = {:2.3} [%]  \n".format(100 * dc['cv'])
    md += "mean = {:.4} [cp/ml]  \n".format(dc['mean'])
    md += "valid = {}  \n".format(dc['valid'])
    if dc['note']:
         md += "note: {}  ".format(dc['note'])

    return md

def sample_section_md(samples, reference, dr, img_dir):
    md = '## Sample evaluation\n\n' 
    k = sample_check(samples, 'k', 1)
    md += sample_to_md(k)
    md += '\n'
    sfile = 'control_{0:02d}.svg'.format(1)
    img_file = path.join(img_dir, sfile)
    sample_img(samples, reference, 'k', 1, img_file, show=False)
    md += '!["alt text"](./img/{})\n\n'.format(sfile)
    sample_n = samples['plate_layout_num'].astype(int).unique()
    sample_n.sort()
    for i in tqdm(sample_n):
        stype = 's'
        s = sample_check(samples, stype, i)
        md += sample_to_md(s)
        # sample info
        si = sample_info(samples, stype, i, dr, verbose=False)
        si_str = sampleinfo_to_str(si['info'])
        if si_str:
            md += '\n'
            md += 'info: ' + si_str + '  '
        md += '\n'
        sfile = 'sample_{0:02d}.svg'.format(i)
        img_file = path.join(img_dir, sfile)
        sample_img(samples, reference, stype, i, img_file=img_file, show=False, verbose=False)
        md += '![{0}](./img/{0})\n'.format(sfile)
        if i != sample_n[-1]:
            md += '\n'
    return md

def save_md(file_path, md_txt):
    try:
        with open(file_path, 'w') as fl:
            fl.write(md_txt)
    except Exception as e:
        print('Error: ' + str(e))


# Result section

def format_results_val(x):
    res = ''
    if math.isnan(x['Result [cp/ml]']):
        res = x['Comment']
    else:
        res = '{:.{dgts}e}'.format(x['Result [cp/ml]'], dgts=cc.RESULT_DIGITS)
    if x['valid_ex']:
        res = '**{}**'.format(res)
    else:
        res = '( {} )*'.format(res)
    
    return res



def format_cv(x):
    if math.isnan(x):
        return 'NA'
    return '{:.{dgts}f}'.format(x, dgts=cc.CV_DIGITS)


def format_results(df):
    df.loc[:, ['Comment']] = df.apply(lambda x: final_sample_info(x['info'], x['Pre-dilution'])[0], axis=1)
    df.loc[:, ['CV [%]']] = df.apply(lambda x: format_cv(x['CV [%]']), axis=1)
    df.loc[:, ['Result [cp/ml]']] = df.apply(lambda x: format_results_val(x), axis=1)
    df.drop(['info', 'Valid', 'Reader Data [cp/ml]', 'info_ex', 'valid_ex'], axis=1, inplace=True)
    
    return df


def result_section(df):
    md = '## Analysis Results\n\n'

    df_formated = format_results(df)
    md += df_formated.to_markdown(floatfmt="#.{}f".format(cc.CV_DIGITS))
    md += '\n\n'
    md += '\* sample will be retested\n\n'
    
    return md
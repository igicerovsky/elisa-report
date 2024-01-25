""" Markdown report assembly
"""

import math
from os import path
from datetime import datetime
import pandas as pd
from tqdm import tqdm

from .typing import PathLike
from .fitdata import fit_sheet, fit_reference_auto_rm, backfit
from .image import fit_image, sample_img, ImageFitResult, save_image
from .sample import final_sample_info, sample_check, sample_info, sampleinfo_to_str
from .constants import RESULT_DIGITS, SAMPLE_TYPES, CV_DIGITS
from .worklist import worklist_sample
from .config import config as cfg
from .config import LIMITS_NAME


def make_final(sl, wl_raw, plate_id):
    """Make final report dataframe"""
    limits = cfg[LIMITS_NAME]
    wl, cd = worklist_sample(wl_raw, plate_id)

    final = pd.concat([wl, sl], axis=1)
    final.loc[:, ['Result [cp/ml]']] = final.apply(
        lambda x: x['Reader Data [cp/ml]'] * x[cd['Dilution']], axis=1)
    final.loc[:, ['CV [%]']] = final.apply(lambda x: x['CV [%]'] * 100, axis=1)
    # reorder columns
    final = final.reindex([cd['SampleID'], cd['Dilution'], cd['Viscosity'],
                          'Reader Data [cp/ml]', 'Result [cp/ml]', 'CV [%]',
                           'Valid', 'info'], axis=1)
    final.rename(columns={cd['SampleID']: 'Sample Name',
                 cd['Dilution']: 'Pre-dilution'}, inplace=True)
    final.drop(f'Viscosity_{plate_id}', axis=1, inplace=True)
    final.index.name = 'Sample type'
    final.loc[:, ['info_ex']] = final.apply(
        lambda x: final_sample_info(x['info'], x['Pre-dilution'], limits)[0], axis=1)
    final.loc[:, ['valid_ex']] = final.apply(
        lambda x: final_sample_info(x['info'], x['Pre-dilution'], limits)[1], axis=1)
    return final


# Header

def header_section(dc: dict, plate_id: int, msg: str) -> str:
    """Generate header section"""
    md = '## Header\n\n'

    dt = datetime.strptime(dc['date'], "%y%m%d")
    md += f'Date: **{dt.strftime("%d %b %Y")}**  \n'
    md += f'Identification: **{dc["gn"]}**  \n'
    md += f'Protocol: **{dc["protocol"]}**  \n'
    md += f'Analyzed by: **{dc["analyst"]}**  \n'
    md += f'Plate: **{plate_id}**  \n'
    md += f'Comment: {msg}  \n\n'

    return md


# Parameters

def param_section(df_params: pd.DataFrame) -> str:
    """Generate parameter section"""
    md = '## Parameters\n\n'

    md += 'Parameters:\n\n' + df_params.to_markdown() + '\n\n'

    return md


# Fit reference curve

def fit_section_md(df_ref: pd.DataFrame, popt, pcov, out_dir: PathLike) -> str:
    """Generate fit section"""
    x = df_ref.reset_index(level=[0, 1])['plate_layout_conc']
    y = df_ref.reset_index(level=[0, 1])['OD_delta']
    fit_result = fit_reference_auto_rm(x, y)
    result_img = path.join(out_dir, 'fit.svg')
    img = fit_image(ImageFitResult(x, y, fit_result[0][0], fit_result[0][1]),
                    confidence='student-t', rm_index=fit_result[1])
    save_image(img, result_img)

    n = len(x) - len(fit_result[1])
    df_fit = fit_sheet(popt, pcov, n)

    md = '## Reference Curve Fit\n\n'
    md += '$y = {d + \\frac{a - d}{{1 + (\\frac{ x }{ c })^b}} }$  \n\n'

    param_legend = """\
`y` &nbsp;&nbsp;&nbsp;$\\Delta$ OD (450nm - 620nm)  
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

def sample_to_md(dc: dict) -> str:
    """Generate sample section"""
    s_view = dc['sample'][['OD_delta', 'plate_layout_dil',
                           'concentration', 'mask_reason']]
    md = f"### Sample: {SAMPLE_TYPES[dc['type']]} '{dc['type']}' {dc['num']}\n\n"
    s_view.index.name = 'Well'
    md += s_view.to_markdown()
    md += '\n\n'
    md += f"CV = {100 * dc['cv']:2.3} [%]  \n"
    md += f"mean = {dc['mean']:.4} [cp/ml]  \n"
    md += f"valid = {dc['valid']}  \n"
    if dc['note']:
        md += f"note: {dc['note']}  "

    return md


def blank_to_md(blank: pd.DataFrame) -> str:
    """Generate blank section"""
    md = '### Blank\n\n'
    blank.index.name = 'Well'
    md += blank[['OD_delta', 'OD_450', 'OD_630']].to_markdown()
    md += '\n'
    return md


def sample_section_md(samples: pd.DataFrame, reference,
                      blank, dr, img_dir: PathLike) -> str:
    """Generate sample section"""
    # this works for pdflatex
    pg_break = '\\pagebreak\n\n'
    # pg_break = '<div style="page-break-after: always;"></div>\n\n'
    md = '## Sample evaluation\n\n'
    md += blank_to_md(blank)
    md += '\n'
    md += pg_break
    md += sample_to_md(sample_check(samples, 'k', 1))
    md += '\n'
    nfl = 1
    sfile = f'control_{nfl:02d}.svg'
    sample_img(samples, reference, 'k', 1,
               path.join(img_dir, sfile))
    md += f'!["alt text"](./img/{sfile})\n\n'
    md += pg_break

    sample_n = samples['plate_layout_num'].astype(int).unique()
    sample_n.sort()
    for i in tqdm(sample_n):
        stype = 's'
        md += sample_to_md(sample_check(samples, stype, i))
        # sample info
        si = sample_info(samples, stype, i, dr)
        si_str = sampleinfo_to_str(si['info'])
        if si_str:
            md += '\n'
            md += 'info: ' + si_str + '  '
        md += '\n'
        sfile = f'sample_{i:02d}.svg'
        img_file = path.join(img_dir, sfile)
        sample_img(samples, reference, stype, i, img_file=img_file)
        md += f'![{sfile}](./img/{sfile})\n'
        if i != sample_n[-1]:
            md += '\n'
            md += pg_break
    return md


def save_md(file_path: PathLike, md_txt: str) -> None:
    """Save markdown text to file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as fl:
            fl.write(md_txt)
    except FileNotFoundError as e:
        print('Error: ' + str(e))


# Result section

def format_results_val(x: float) -> str:
    """Format result value"""
    res = ''
    if math.isnan(x['Result [cp/ml]']):
        res = x['Comment']
    else:
        v = x["Result [cp/ml]"]
        res = f'{v:.{RESULT_DIGITS}e}'
    if x['valid_ex']:
        res = f'**{res}**'
    elif x['info_ex'] == 'test invalid':
        res = f'[ {res} ]'
    else:
        res = f'( {res} )*'

    return res


def format_cv(x: float) -> str:
    """Format CV value"""
    if math.isnan(x):
        return 'NA'
    return f'{x:.{CV_DIGITS}f}'


def format_results(df: pd.DataFrame, limits: dict) -> pd.DataFrame:
    """Format results dataframe"""
    df.loc[:, ['Comment']] = df.apply(lambda x: final_sample_info(
        x['info'], x['Pre-dilution'], limits)[0], axis=1)
    df.loc[:, ['CV [%]']] = df.apply(lambda x: format_cv(x['CV [%]']), axis=1)
    df.loc[:, ['Result [cp/ml]']] = df.apply(format_results_val, axis=1)
    df.drop(['info', 'Valid', 'Reader Data [cp/ml]',
            'info_ex', 'valid_ex'], axis=1, inplace=True)

    return df


def result_section(df: pd.DataFrame) -> str:
    """Generate result section"""
    limits = cfg[LIMITS_NAME]
    md = '## Analysis Results\n\n'

    df_formated = format_results(df, limits)
    md += df_formated.to_markdown(floatfmt=f"#.{CV_DIGITS}f")
    md += '\n\n'
    md += '\\* sample will be retested\n\n'

    return md

""" Main report
"""
import os
from zlib import crc32

import pandas as pd

from .typing import PathLike
from .readdata import read_concat_data, concat_data_with_layouts
from .sample import init_samples, apply_fit, mask_sample, data_range, generate_results
from .fitdata import fit_reference_auto_rm, FitData
from .reportmd import header_section, make_final, result_section, fit_section_md
from .reportmd import param_section, sample_section_md


def check_report_crc(report: str, crc: int) -> None:
    """ Check report CRC
    """
    res = bytearray(report, 'utf8')
    t = crc32(res)

    if t != crc:
        raise ValueError(f'Report CRC missmatch! {t} != {crc}')


def init_fit_data(df_all: pd.DataFrame, reference_conc: float) -> FitData:
    """ Initialize fit data
    """
    dfg = init_samples(df_all, reference_conc)
    ref = dfg.loc[(dfg['plate_layout_ident'] == 'r')]
    x = ref.reset_index(level=[0, 1])['plate_layout_conc']
    y = ref.reset_index(level=[0, 1])['OD_delta']
    fit = fit_reference_auto_rm(x, y)
    popt = fit[0][0]
    pcov = fit[0][1]
    dr = data_range(ref, popt)

    return FitData(ref, popt, pcov, dr)


def report_plate(plate_id: int, report_params: dict,
                 input_data_path: PathLike, report_dir: PathLike, info: dict):
    """ Report plate generation for main report
    """
    od = read_concat_data(input_data_path)
    df_all = concat_data_with_layouts(od, report_params['layouts'])
    fd = init_fit_data(df_all, report_params['refconc'])
    dfg = init_samples(df_all, report_params['refconc'])
    dfg = apply_fit(dfg, fd.popt)
    dfg = mask_sample(dfg, fd.dr)
    sl = generate_results(dfg, fd.dr)

    report = '''\
---
geometry: margin=1cm
documentclass: extarticle
mainfont: Noto Sans
fontsize: 10pt
colorlinks: true
---

# Automatically Generated Markdown Report for ELISA\n\n'''

    report += header_section(info, plate_id, '')
    final = make_final(sl, report_params['worklist'], plate_id).drop(
        'reference 01', axis=0)
    report += result_section(final)
    report += param_section(report_params['params'])
    img_dir = os.path.join(report_dir, 'img')
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    report += fit_section_md(fd.ref, fd.popt, fd.pcov, img_dir)
    blank = df_all.loc[(df_all['plate_layout_ident'] == 'b')]
    report += sample_section_md(dfg, fd.ref, blank, fd.dr, img_dir)

    return report, final

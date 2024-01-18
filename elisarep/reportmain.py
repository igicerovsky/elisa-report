import os
from .readdata import read_concat_data, concat_data_with_layouts
from .sample import init_samples, apply_fit, mask_sample, data_range, generate_results
from .fitdata import fit_reference_auto_rm
from zlib import crc32
from .reportmd import header_section, make_final, result_section, fit_section_md, param_section, sample_section_md


def check_report_crc(report: str, crc: int) -> None:
    res = bytearray(report, 'utf8')
    t = crc32(res)

    if t != crc:
        raise Exception('Report CRC missmatch! {} != {}'.format(t, crc))

    return None


def report_plate(plate_id, worklist, params, layouts, reference_conc,
                 input_data_path, report_dir, info):

    od = read_concat_data(input_data_path)
    df_all = concat_data_with_layouts(od, layouts)

    dfg = init_samples(df_all, reference_conc)

    ref = dfg.loc[(dfg['plate_layout_ident'] == 'r')]
    blank = df_all.loc[(df_all['plate_layout_ident'] == 'b')]
    x = ref.reset_index(level=[0, 1])['plate_layout_conc']
    y = ref.reset_index(level=[0, 1])['OD_delta']
    fit = fit_reference_auto_rm(x, y, verbose=False)
    popt = fit[0][0]
    pcov = fit[0][1]
    dr = data_range(ref, popt)

    dfg = apply_fit(dfg, popt)
    dfg = mask_sample(dfg, dr)
    sl = generate_results(dfg, dr)

    report = '''\
---
geometry: margin=1cm
documentclass: extarticle
mainfont: Noto Sans
fontsize: 10pt
colorlinks: true
---

# Automatically Generated Markdown report

This a PoC for automatic report generation...\n\n'''

    report += header_section(info, plate_id, ':)')
    final = make_final(sl, worklist, plate_id).drop(
        'reference 01', axis=0)
    report += result_section(final)
    report += param_section(params)
    img_dir = os.path.join(report_dir, 'img')
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    report += fit_section_md(ref, popt, pcov, img_dir)
    report += sample_section_md(dfg, ref, blank, dr, img_dir)

    return report, final

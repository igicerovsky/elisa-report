import os
from readdata import read_concat_data, concat_data_with_layouts
from sample import init_samples, apply_fit, mask_sample, data_range, generate_results
from fitdata import fit_reference_auto_rm
from zlib import crc32
import reportmd as rmd


def check_report_crc(report: str, crc):
    res = bytearray(report,'utf8')
    t = crc32(res)

    if t != crc:
        raise Exception('Report CRC missmatch! {} != {}'.format(t, crc))
    else:
         print('\nReport CRC is OK. ({})\n'.format(t))

def report_plate(plate_id, worklist, params, plate_layout_id, plate_layout_num,
                 plate_layout_dil_id, reference_conc,
                 input_data_path, report_dir, report_file_path
                 ):

    od = read_concat_data(input_data_path)
    df_all = concat_data_with_layouts(od, plate_layout_id, plate_layout_num, plate_layout_dil_id)

    dfg = init_samples(df_all, reference_conc)

    ref = dfg.loc[(dfg['plate_layout_ident']=='r')]
    x = ref.reset_index(level=[0,1])['plate_layout_conc']
    y = ref.reset_index(level=[0,1])['OD_delta']
    fit = fit_reference_auto_rm(x, y, verbose=False)
    popt = fit[0][0]
    pcov = fit[0][1]
    dr = data_range(ref, popt)

    dfg = apply_fit(dfg, popt)
    dfg = mask_sample(dfg, dr)
    sl = generate_results(dfg, dr)

    report = '''
# Automatically Generated Markdown report

This a PoC for automatic report generation...\n\n'''

    report += rmd.header_section('05 May 2023', 'GN004240-033', plate_id, ':)')
    report += rmd.result_section(rmd.make_final(sl, worklist, plate_id).drop('reference 01', axis=0))
    report += rmd.param_section(params)
    img_dir = os.path.join(report_dir, 'img')
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    report += rmd.fit_section_md(ref, popt, pcov, img_dir) # TODO: !!! global fit_result[3]

    report += rmd.sample_section_md(dfg, ref, dr, img_dir)

    if not report_file_path:
        print(report_file_path)
        rmd.save_md(report_file_path, report)

    return report


from os import path
import argparse
import warnings


from scipy.optimize import OptimizeWarning
from zlib import crc32

from hamrep.readdata import read_params
from hamrep.mkinout import make_input_paths
from hamrep.worklist import predil_worklist, check_worklist
from hamrep.sample import make_concentration
from hamrep.readdata import read_layouts
from hamrep.mdhandling import md2docx, md2pdf, export_main_report
from hamrep.reportmd import save_md
from hamrep.config import config as cfg
from hamrep.config import init_config, REFVAL_NAME, DIL_NAME
import hamrep.reportgen as rg

WARNING_DISABLE = True

if WARNING_DISABLE:
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', OptimizeWarning)
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def main_report(analysis_dir, txt_input, config_dir, docxa: bool = True, docxr: bool = False, pdf: bool = True):
    print(f'Analysis diretory directory {analysis_dir}')
    print(f'Configuration directory {config_dir}')

    init_config(analysis_dir, config_dir)

    input_files = make_input_paths(analysis_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = predil_worklist(worklist_file_path)
    params = read_params(params_file_path)
    reference_conc = make_concentration(
        cfg[REFVAL_NAME], cfg[DIL_NAME])

    lay = read_layouts(path.join(config_dir, cfg['plate_layout_id']),
                       path.join(config_dir, cfg['plate_layout_num']),
                       path.join(config_dir, cfg['plate_layout_dil_id']))

    if txt_input:
        reports = rg.gen_report_raw(
            wl_raw, params, lay, reference_conc, analysis_dir)
    else:
        valid_plates = check_worklist(wl_raw)
        reports = rg.gen_report_calc(valid_plates, wl_raw, params, lay,
                                     reference_conc, analysis_dir)

    if docxa:
        export_main_report(reports, analysis_dir, cfg['pandoc_bin'],
                           cfg['reference_docx'])

    for report in reports:
        print('Report for plate {} saved as {}'.format(
            report['plate'], report['path']))
        save_md(report['path'], report['md'])

        if docxr:
            md2docx(cfg['pandoc_bin'],
                    cfg['reference_docx'], report['path'])
        if pdf:
            md2pdf(cfg['pandoc_bin'],
                   cfg['pdflatex_bin'], report['path'])

        binr = bytearray(report['md'], 'utf8')
        t = crc32(binr)
        print("CRC for '{}' is {}".format(report['path'], t))

    print('Done.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "analysis", help="analysis directory", default=None)
    parser.add_argument('--calc', action='store_true',
                        help="use calc files as input")
    parser.add_argument('--cfg', help="config and params directory",
                        default='./data')

    args = parser.parse_args()
    analysis_dir = args.analysis
    txt_input = not args.calc
    config_dir = args.cfg

    main_report(analysis_dir, txt_input, config_dir)


if __name__ == "__main__":
    main()

from os import path
import argparse
import warnings
import json

from scipy.optimize import OptimizeWarning
from zlib import crc32

from hamrep.readdata import read_params
from hamrep.mkinout import make_input_paths
from hamrep.worklist import predil_worklist, check_worklist
from hamrep.sample import make_concentration
from hamrep.readdata import read_layouts, read_params_json
from hamrep.mdhandling import md2docx, md2pdf, export_main_report
import hamrep.reportgen as rg
from hamrep.reportmd import save_md


CONFIG_FILENAME = 'config.json'
WARNING_DISABLE = True

if WARNING_DISABLE:
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', OptimizeWarning)
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


config = {
    "default": {
        "referenceValue": 1.0E+10,
        "limits": [
            1.0E+10,
            1.0E+12
        ]
    },
    "dilutions": [
        1.0,
        2.0,
        4.0,
        8.0,
        16.0,
        32.0,
        64.0
    ]
}


def read_config(filename):
    keys = ['pandoc_bin', 'pdflatex_bin', 'reference_docx', 'params_filename',
            'plate_layout_id', 'plate_layout_num', 'plate_layout_dil_id', 'numeric_warning_disable',
            'AAV8', 'AAV9', 'default', 'dilutions']
    with open(filename) as json_config:
        for key, value in json.load(json_config).items():
            if key in keys:
                config[key] = value
            else:
                raise KeyError(key)


def aav_type(analysis_dir):
    a_type = None
    if analysis_dir.lower().find('aav9') != -1:
        a_type = 'AAV9'
        print('Applying parameters for AAV9.')
    elif analysis_dir.lower().find('aav8') != -1:
        a_type = 'AAV8'
        print('Applying parameters for AAV8.')
    else:
        print('Applying default/custom parameters.')
        a_type = 'default'
    return a_type


def main_report(analysis_dir, txt_input, config_dir, docxa: bool = True, docxr: bool = False, pdf: bool = True):
    print(f'Processing directory {analysis_dir}')

    read_config(path.join(config_dir, "config.json"))

    input_files = make_input_paths(analysis_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = predil_worklist(worklist_file_path)
    params = read_params(params_file_path)
    a_type = aav_type(analysis_dir)
    ref_val_max, dilutions, limits = read_params_json(
        analysis_dir, config_dir, CONFIG_FILENAME, a_type)
    reference_conc = make_concentration(ref_val_max, dilutions)

    lay = read_layouts(path.join(config_dir, config['plate_layout_id']),
                       path.join(config_dir, config['plate_layout_num']),
                       path.join(config_dir, config['plate_layout_dil_id']))

    if txt_input:
        reports = rg. gen_report_raw(
            wl_raw, params, lay, reference_conc, analysis_dir, limits)
    else:
        valid_plates = check_worklist(wl_raw)
        reports = rg.gen_report_calc(valid_plates, wl_raw, params, lay,
                                     reference_conc, analysis_dir)

    if docxa:
        export_main_report(reports, analysis_dir, config['pandoc_bin'],
                           config['reference_docx'], limits)

    for report in reports:
        print('Report for plate {} saved as {}'.format(
            report['plate'], report['path']))
        save_md(report['path'], report['md'])

        if docxr:
            md2docx(config['pandoc_bin'],
                    config['reference_docx'], report['path'])
        if pdf:
            md2pdf(config['pandoc_bin'],
                   config['pdflatex_bin'], report['path'])

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

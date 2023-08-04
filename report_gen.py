from os import path
import argparse
import warnings

from readdata import read_params
from scipy.optimize import OptimizeWarning
from mkinout import make_input_paths, make_output_paths, make_input_analysis, basename_from_inputdir, parse_dir_name
from worklist import read_worklist, check_worklist
from sample import make_concentration
from reportmain import report_plate
from readdata import read_layouts, read_params_json
from zlib import crc32
import reportgen as rg
from mdhandling import export_palte_reports, export_main_report


WARNING_DISABLE = True
DATA_DIR = './data'
PARAMS_FILENAME = 'params.json'
PLATE_LAYOUT_ID = 'plate_layout_ident.csv'
PLATE_LAYOUT_NUM = 'plate_layout_num.csv'
PLATE_LAYOUT_DIL_ID = 'plate_layout_dil_id.csv'


if WARNING_DISABLE:
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', OptimizeWarning)
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def main_report(working_dir, txt_input, docxa:bool = True, docxr:bool = False, pdf:bool = True):
    print(f'Processing directory {working_dir}')
    input_files = make_input_paths(working_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = read_worklist(worklist_file_path)
    valid_plates = check_worklist(wl_raw)
    params = read_params(params_file_path)
    ref_val_max, dilutions = read_params_json(working_dir, DATA_DIR, PARAMS_FILENAME)
    reference_conc = make_concentration(ref_val_max, dilutions)

    lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                        path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                        path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    if txt_input:
        reports =rg. gen_report_raw(wl_raw, params, lay, reference_conc, working_dir)
    else:
        reports = rg.gen_report_calc(valid_plates, wl_raw, params, lay,
                                            reference_conc, working_dir)

    if docxa:
        export_main_report(reports, working_dir)
    export_palte_reports(reports, docxr, pdf)

    for report in reports:
        binr = bytearray(report['md'],'utf8')
        t = crc32(binr)
        print("CRC for '{}' is {}".format(report['path'], t))
    print('Done.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workdir", help="working directory of an experiment", default=None)
    parser.add_argument('--calc', action='store_true', help="use calc files as input")

    args = parser.parse_args()
    working_dir = args.workdir
    txt_input = not args.calc

    main_report(working_dir, txt_input)


if __name__ == "__main__":
    main()

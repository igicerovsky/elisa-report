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

def gen_report(valid_plates, worklist, params, layout, reference_conc,
               working_dir, base_name):
    reports = []
    files = []
    for plate in valid_plates:
        print('Processing plate {} of {}'.format(plate, len(valid_plates)))

        output_files = make_output_paths(working_dir, base_name, plate)
        analysis_file_path = make_input_analysis(working_dir, base_name, plate)
        report_file_path = output_files['report']
        results_file_path = output_files['plate_results']
        report_dir = path.dirname(path.abspath(report_file_path))
        info = parse_dir_name(working_dir)
        reports.append(report_plate(info, worklist, params, layout,
                    reference_conc, analysis_file_path, report_dir, report_file_path
                    ))
        files.append(report_file_path)

    return reports, files


def main_report(working_dir):
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

    reports, files = gen_report(valid_plates, wl_raw, params, lay,
        reference_conc, working_dir, basename_from_inputdir(working_dir))
    for report, file in zip(reports, files):
        binr = bytearray(report,'utf8')
        t = crc32(binr)
        print("CRC for '{}' is {}".format(file, t))
    print('Done.')

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--workdir", help="working directory of an experiment", default=None)

    args = parser.parse_args()
    working_dir = args.workdir
    main_report(working_dir)


if __name__ == "__main__":
    main()

from os import path
import argparse
import warnings

from readdata import read_params
from fitdata import fit_magic
from readdata import read_concat_data
from scipy.optimize import OptimizeWarning
from mkinout import make_input_paths, make_output_paths
from worklist import read_worklist, check_worklist
from sample import make_concentration
from reportmain import report_plate
from readdata import read_layouts
from zlib import crc32

WARNING_DISABLE = True
DATA_DIR = './data'
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
        hamilton_file_path = output_files['results']
        report_file_path = output_files['report']
        report_dir = path.dirname(path.abspath(report_file_path))
        reports.append(report_plate(plate, worklist, params, layout,
                    reference_conc, hamilton_file_path, report_dir, report_file_path
                    ))
        files.append(report_file_path)

    return reports, files


def main_report(working_dir, base_name):
    input_files = make_input_paths(working_dir, base_name)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    ref_val_max = 1.7954e+10
    dilutions = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]

    wl_raw = read_worklist(worklist_file_path)
    valid_plates = check_worklist(wl_raw)
    params = read_params(params_file_path)
    reference_conc = make_concentration(ref_val_max, dilutions)

    lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                        path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                        path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    reports, files = gen_report(valid_plates, wl_raw, params, lay, reference_conc, working_dir, base_name)
    for report, file in zip(reports, files):
        binr = bytearray(report,'utf8')
        t = crc32(binr)
        print("CRC for '{}' is {}".format(file, t))
    print('Done.')

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--basename", help="base name", default=None)
    parser.add_argument("-d", "--workdir", help="working directory of an experiment", default=None)
    # parser.add_argument("-w", "--worklist", help="worklist path (xls)", default=None)
    # parser.add_argument("-p", "--params", help="parameters path (csv)", default=None)

    args = parser.parse_args()
    working_dir = args.workdir
    base_name = args.basename
    main_report(working_dir, base_name)


if __name__ == "__main__":
    main()

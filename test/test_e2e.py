from os import path
import warnings
from scipy.optimize import OptimizeWarning
import subprocess
from hamrep.sample import make_concentration
from hamrep.worklist import read_worklist, check_worklist
from hamrep.readdata import read_params
from hamrep.reportmain import report_plate, check_report_crc
from hamrep.mkinout import make_output_paths, basename_from_inputdir, parse_dir_name, make_input_analysis, make_input_paths
from hamrep.readdata import read_layouts
from hamrep.reportgen import gen_report_calc


warnings.simplefilter('ignore', RuntimeWarning)
warnings.simplefilter('ignore', OptimizeWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def test_e2e():
    working_dir = './reports/230426_AAV9-ELISA_igi_GN004240-033'

    input_files = make_input_paths(working_dir)
    WORKLIST_FILE_PATH = input_files['worklist']
    PARAMS_FILE_PATH = input_files['params']

    DATA_DIR = './data'


    PLATE_LAYOUT_ID = 'plate_layout_ident.csv'
    PLATE_LAYOUT_NUM = 'plate_layout_num.csv'
    PLATE_LAYOUT_DIL_ID = 'plate_layout_dil_id.csv'


    lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                        path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                        path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    wl_raw = read_worklist(WORKLIST_FILE_PATH)
    valid_plates = check_worklist(wl_raw)
    params = read_params(PARAMS_FILE_PATH)

    # TODO: read reference value from parameters
    REF_VAL_MAX = 1.7954e+10
    DILUTIONS = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]

    reference_conc = make_concentration(REF_VAL_MAX, DILUTIONS)

    reports = gen_report_calc(valid_plates, wl_raw, params, lay,
                                            reference_conc, working_dir)

    CHECK_REPORT_CRC = True
    REPORT_PLATES_CRC = [864111381, 3242056329]
    if CHECK_REPORT_CRC:
        for report, crc in zip(reports, REPORT_PLATES_CRC):
            try:
                check_report_crc(report['md'], crc)
            except Exception as e:
                print('{} for {}'.format(e, report['path']))
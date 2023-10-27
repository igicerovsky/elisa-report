from os import path
import warnings
import json

from scipy.optimize import OptimizeWarning

from hamrep.readdata import read_params
from hamrep.mkinout import make_input_paths
from hamrep.worklist import predil_worklist
from hamrep.sample import make_concentration
from hamrep.readdata import read_layouts, read_params_json
import hamrep.reportgen as rg
from hamrep.reportmain import check_report_crc


DATA_DIR = './data'
PARAMS_FILENAME = 'params.json'
PLATE_LAYOUT_ID = 'plate_layout_ident.csv'
PLATE_LAYOUT_NUM = 'plate_layout_num.csv'
PLATE_LAYOUT_DIL_ID = 'plate_layout_dil_id.csv'

ANALYSIS_DIR = 'reports/export/230801_AAV9-ELISA_sey_GN004240-053'
warnings.simplefilter('ignore', RuntimeWarning)
warnings.simplefilter('ignore', OptimizeWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def test_e2e():
    input_files = make_input_paths(ANALYSIS_DIR)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = predil_worklist(worklist_file_path)
    params = read_params(params_file_path)
    ref_val_max, dilutions = read_params_json(
        ANALYSIS_DIR, DATA_DIR, PARAMS_FILENAME)
    reference_conc = make_concentration(ref_val_max, dilutions)

    lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                       path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                       path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    reports = rg. gen_report_raw(
        wl_raw, params, lay, reference_conc, ANALYSIS_DIR)

    CHECK_REPORT_CRC = True
    REPORT_PLATES_CRC = [4195121021, 1426265408, 2440240818]
    if CHECK_REPORT_CRC:
        for report, crc in zip(reports, REPORT_PLATES_CRC):
            try:
                check_report_crc(report['md'], crc)
            except Exception as e:
                print('{} for {}'.format(e, report['path']))

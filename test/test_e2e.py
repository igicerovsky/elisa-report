from os import path
import warnings

from scipy.optimize import OptimizeWarning

from hamrep.readdata import read_params
from hamrep.mkinout import make_input_paths, parse_dir_name
from hamrep.worklist import predil_worklist
from hamrep.sample import make_concentration
from hamrep.readdata import read_layouts, read_params_json
import hamrep.reportgen as rg
from hamrep.reportmain import check_report_crc
from hamrep.reportmdassembly import assembly


DATA_DIR = './data'
PARAMS_FILENAME = 'params.json'
PLATE_LAYOUT_ID = 'plate_layout_ident.csv'
PLATE_LAYOUT_NUM = 'plate_layout_num.csv'
PLATE_LAYOUT_DIL_ID = 'plate_layout_dil_id.csv'

warnings.simplefilter('ignore', RuntimeWarning)
warnings.simplefilter('ignore', OptimizeWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def generic_test(analysis_dir, report_plates_crc, assembly_crc):
    input_files = make_input_paths(analysis_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = predil_worklist(worklist_file_path)
    params = read_params(params_file_path)
    ref_val_max, dilutions, limits = read_params_json(
        analysis_dir, DATA_DIR, PARAMS_FILENAME)
    reference_conc = make_concentration(ref_val_max, dilutions)

    lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                       path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                       path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    reports = rg. gen_report_raw(
        wl_raw, params, lay, reference_conc, analysis_dir, limits)

    for report, crc in zip(reports, report_plates_crc):
        try:
            check_report_crc(report['md'], crc)
        except Exception as e:
            print('{} for {}'.format(e, report['path']))

    parsed_dir = parse_dir_name(analysis_dir)
    md_assembly = assembly(
        reports, protocol=parsed_dir['protocol'], limits=limits)

    check_report_crc(md_assembly, assembly_crc)


def test_e2e_aav9():
    analysis_dir = 'reports/export/230801_AAV9-ELISA_sey_GN004240-053'
    report_plates_crc = [4195121021, 1426265408, 2440240818]
    assembly_crc = 224918877
    generic_test(analysis_dir, report_plates_crc, assembly_crc)


def test_e2e_aav8():
    analysis_dir = 'reports/all/231024_AAV8-ELISA_sey_GN004240-058'
    report_plates_crc = [0]
    assembly_crc = 0
    generic_test(analysis_dir, report_plates_crc, assembly_crc)

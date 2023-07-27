from os import path
import warnings
from scipy.optimize import OptimizeWarning
import subprocess
from sample import make_concentration
from worklist import read_worklist, check_worklist
from readdata import read_params
from reportmain import report_plate, check_report_crc
from mkinout import make_output_paths, basename_from_inputdir, parse_dir_name

warnings.simplefilter('ignore', RuntimeWarning)
warnings.simplefilter('ignore', OptimizeWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def test_e2e():
    from mkinout import make_input_paths
    WORKING_DIR = './reports/230426_AAV9-ELISA_igi_GN004240-033'

    input_files = make_input_paths(WORKING_DIR)
    WORKLIST_FILE_PATH = input_files['worklist']
    PARAMS_FILE_PATH = input_files['params']

    DATA_DIR = './data'

    from readdata import read_layouts

    PLATE_LAYOUT_ID = 'plate_layout_ident.csv'
    PLATE_LAYOUT_NUM = 'plate_layout_num.csv'
    PLATE_LAYOUT_DIL_ID = 'plate_layout_dil_id.csv'


    g_lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                        path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                        path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    g_wl_raw = read_worklist(WORKLIST_FILE_PATH)
    g_valid_plates = check_worklist(g_wl_raw)
    g_params = read_params(PARAMS_FILE_PATH)

    # TODO: read reference value from parameters
    REF_VAL_MAX = 1.7954e+10
    DILUTIONS = [1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]

    g_reference_conc = make_concentration(REF_VAL_MAX, DILUTIONS)

    def gen_report(valid_plates, worklist, params, layout, reference_conc,
                working_dir, base_name):
        reports = []
        for plate in valid_plates:
            print('Processing plate {} of {}'.format(plate, len(valid_plates)))

            output_files = make_output_paths(working_dir, base_name, plate)
            analysis_file_path = output_files['analysis']
            report_file_path = output_files['report']
            report_dir = path.dirname(path.abspath(report_file_path))
            info = parse_dir_name(working_dir)
            md = report_plate(plate, worklist, params, layout,
                        reference_conc, analysis_file_path,
                        report_dir, report_file_path,
                        info
                        )
            reports.append({'md': md, 'path': report_file_path})
        return reports

    reports = gen_report(g_valid_plates, g_wl_raw, g_params, g_lay, g_reference_conc,
        WORKING_DIR, basename_from_inputdir(WORKING_DIR))

    CHECK_REPORT_CRC = True
    REPORT_PLATES_CRC = [864111381, 3242056329]
    if CHECK_REPORT_CRC:
        for report, crc in zip(reports, REPORT_PLATES_CRC):
            try:
                check_report_crc(report['md'], crc)
            except Exception as e:
                print('{} for {}'.format(e, report['path']))

    for report in reports:
        report_file_path = path.abspath(report['path'])
        report_dir = path.dirname(path.abspath(report_file_path))
        docx_path = path.splitext(report_file_path)[0] + '.docx'
        print('Generating Word {} for {}'.format(docx_path, report_file_path))
        subprocess.run(['c:/work/pandoc/pandoc', '-o', docx_path, '-f', 'markdown', '-t', 'docx', '--resource-path', report_dir, report_file_path])

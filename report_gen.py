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


def main_report(working_dir, txt_input, docxa: bool = True, docxr: bool = False, pdf: bool = True):
    print(f'Processing directory {working_dir}')

    with open(path.join(DATA_DIR, "config.json")) as json_file:
        jd = json.load(json_file)
        reference_doc = jd['reference_docx']
        pdflatex_bin = jd['pdflatex_bin']
        pandoc_bin = jd['pandoc_bin']

    input_files = make_input_paths(working_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = predil_worklist(worklist_file_path)
    valid_plates = check_worklist(wl_raw)
    params = read_params(params_file_path)
    ref_val_max, dilutions = read_params_json(
        working_dir, DATA_DIR, PARAMS_FILENAME)
    reference_conc = make_concentration(ref_val_max, dilutions)

    lay = read_layouts(path.join(DATA_DIR, PLATE_LAYOUT_ID),
                       path.join(DATA_DIR, PLATE_LAYOUT_NUM),
                       path.join(DATA_DIR, PLATE_LAYOUT_DIL_ID))

    if txt_input:
        reports = rg. gen_report_raw(
            wl_raw, params, lay, reference_conc, working_dir)
    else:
        reports = rg.gen_report_calc(valid_plates, wl_raw, params, lay,
                                     reference_conc, working_dir)

    if docxa:
        export_main_report(reports, working_dir, pandoc_bin, reference_doc)

    for report in reports:
        print('Report for plate {} saved as {}'.format(
            report['plate'], report['path']))
        save_md(report['path'], report['md'])

        if docxr:
            md2docx(pandoc_bin, reference_doc, report['path'])
        if pdf:
            md2pdf(pandoc_bin, pdflatex_bin, report['path'])

        binr = bytearray(report['md'], 'utf8')
        t = crc32(binr)
        print("CRC for '{}' is {}".format(report['path'], t))

    print('Done.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "workdir", help="working directory of an experiment", default=None)
    parser.add_argument('--calc', action='store_true',
                        help="use calc files as input")
    parser.add_argument('--cfg', help="use calc files as input",
                        default='./data/config.json')

    args = parser.parse_args()
    working_dir = args.workdir
    txt_input = not args.calc

    main_report(working_dir, txt_input)


if __name__ == "__main__":
    main()

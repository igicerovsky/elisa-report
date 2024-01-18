""" E2e test for report generating

Test the whole pipeline.
"""

from os import path
import warnings

from scipy.optimize import OptimizeWarning

from elisarep.readdata import read_params
from elisarep.mkinout import make_input_paths, parse_dir_name
from elisarep.worklist import predil_worklist
from elisarep.sample import make_concentration
from elisarep.readdata import read_layouts
import elisarep.reportgen as rg
from elisarep.reportmain import check_report_crc
from elisarep.reportmdassembly import assembly
from elisarep.config import config as cfg
from elisarep.config import init_config, REFVAL_NAME, DIL_NAME
from elisarep.typing import PathLike

CONFIG_DIR = './data'
PLATE_LAYOUT_ID = 'plate_layout_ident.csv'
PLATE_LAYOUT_NUM = 'plate_layout_num.csv'
PLATE_LAYOUT_DIL_ID = 'plate_layout_dil_id.csv'

warnings.simplefilter('ignore', RuntimeWarning)
warnings.simplefilter('ignore', OptimizeWarning)
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def generic_test(analysis_dir: PathLike, report_plates_crc: list, assembly_crc: int) -> None:
    """Run test for given parameters

    Parameters:
    -----------
    analysis_dir : PathLike
        Analisis directory
    report_plates_crc: list
      List of CRCs for each plate
    assembly_crc : int
        Final report asssebly CRC

    Raises:
    -------
    Exception
      If check fail, exception is raisee.
    """

    input_files = make_input_paths(analysis_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    init_config(analysis_dir, CONFIG_DIR)

    wl_raw = predil_worklist(worklist_file_path)
    params = read_params(params_file_path)
    reference_conc = make_concentration(
        cfg[REFVAL_NAME], cfg[DIL_NAME])

    lay = read_layouts(path.join(CONFIG_DIR, PLATE_LAYOUT_ID),
                       path.join(CONFIG_DIR, PLATE_LAYOUT_NUM),
                       path.join(CONFIG_DIR, PLATE_LAYOUT_DIL_ID))

    reports = rg. gen_report_raw(
        wl_raw, params, lay, reference_conc, analysis_dir)

    for report, crc in zip(reports, report_plates_crc):
        check_report_crc(report['md'], crc)

    parsed_dir = parse_dir_name(analysis_dir)
    md_assembly = assembly(
        reports, protocol=parsed_dir['protocol'])

    check_report_crc(md_assembly, assembly_crc)


def test_e2e_aav9():
    """ Test for AAV9
    """
    analysis_dir = './test/analysis/230801_AAV9-ELISA_sey_GN004240-053'
    report_plates_crc = [481216317, 1583512440, 1864635915]
    assembly_crc = 1006124183
    generic_test(analysis_dir, report_plates_crc, assembly_crc)


def test_e2e_aav9_dilthr():
    """AAV9 test
    """
    analysis_dir = './test/analysis/231122_AAV9-ELISA_sey_GN004240-064'
    report_plates_crc = [1614107716]
    assembly_crc = 2473881083
    generic_test(analysis_dir, report_plates_crc, assembly_crc)


def test_e2e_aav8():
    """AAV8 test
    """
    analysis_dir = './test/analysis/231024_AAV8-ELISA_sey_GN004240-058'
    report_plates_crc = [4112746544]
    assembly_crc = 2800641728
    generic_test(analysis_dir, report_plates_crc, assembly_crc)

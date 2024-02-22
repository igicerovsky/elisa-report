""" E2e test for report generating

Test the whole pipeline.
"""

from os import path
from zlib import crc32
import warnings

from scipy.optimize import OptimizeWarning

from elisarep.readdata import read_params
from elisarep.mkinout import make_input_paths, parse_dir_name, make_mdil_path
from elisarep.worklist import predil_worklist
from elisarep.sample import make_concentration
from elisarep.readdata import read_layouts
import elisarep.reportgen as rg
from elisarep.reportmain import check_report_crc
from elisarep.reportmdassembly import assembly, assembly_word, iter_block_items
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


def check_docx(document, crc_expected):
    """Check docx document

    Parameters:
    -----------
    document : str
        Document to check
    crc : int
        Expected CRC

    Raises:
    -------
    Exception
        If check fail, exception is raisee.
    """
    doctxt = ''
    for block in iter_block_items(document):
        doctxt += block.text
    crc_actual = crc32(doctxt.encode())
    assert crc_actual == crc_expected, f'Expected {crc_expected}, got {crc_actual}'


def generic_test(analysis_dir: PathLike, report_plates_crc: list,
                 md_crc: int, word_crc: int) -> None:
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
    predil_file_path = make_mdil_path(analysis_dir)

    init_config(analysis_dir, CONFIG_DIR)

    report_params = {
        'worklist': predil_worklist(worklist_file_path, predil_file_path),
        'params': read_params(params_file_path),
        'layouts': read_layouts(path.join(CONFIG_DIR, cfg['plate_layout_id']),
                                path.join(CONFIG_DIR, cfg['plate_layout_num']),
                                path.join(CONFIG_DIR, cfg['plate_layout_dil_id'])),
        'refconc': make_concentration(
            cfg[REFVAL_NAME], cfg[DIL_NAME])
    }
    reports = rg.gen_report_raw(report_params, analysis_dir)

    for report, crc in zip(reports, report_plates_crc):
        check_report_crc(report['md'], crc)

    parsed_dir = parse_dir_name(analysis_dir)
    md_assembly = assembly(
        reports, protocol=parsed_dir['protocol'])
    check_report_crc(md_assembly, md_crc)

    doc = assembly_word(
        reports, parsed_dir['protocol'], footer=False,
        reference_doc=path.join(CONFIG_DIR, cfg['reference_docx']),
    )
    check_docx(doc, word_crc)


def test_e2e_aav9():
    """ Test for AAV9
    """
    analysis_dir = './test/analysis/230801_AAV9-ELISA_sey_GN004240-053'
    report_plates_crc = [1243771558, 2794876820, 1165470534]
    generic_test(analysis_dir, report_plates_crc,
                 md_crc=60030663,
                 word_crc=3887589158)


def test_e2e_aav9_dilthr():
    """AAV9 test
    """
    analysis_dir = './test/analysis/231122_AAV9-ELISA_sey_GN004240-064'
    report_plates_crc = [3271910687]
    generic_test(analysis_dir, report_plates_crc,
                 md_crc=2473881083,
                 word_crc=825627088)


def test_e2e_aav8():
    """AAV8 test
    """
    analysis_dir = './test/analysis/231024_AAV8-ELISA_sey_GN004240-058'
    report_plates_crc = [858956047]
    generic_test(analysis_dir, report_plates_crc,
                 md_crc=117438155,
                 word_crc=3671054324)

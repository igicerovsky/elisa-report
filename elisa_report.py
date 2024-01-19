""" Main ELISA report generation script

Generates ELISA report from photometer output; analysis performed on Hamilton robot.
"""

from os import path, getcwd
import argparse
import warnings

from zlib import crc32

from tkinter import StringVar, Button, Entry, DISABLED, Tk
from tkinter import filedialog

from scipy.optimize import OptimizeWarning

from elisarep.readdata import read_params
from elisarep.mkinout import make_input_paths
from elisarep.worklist import predil_worklist
from elisarep.sample import make_concentration
from elisarep.readdata import read_layouts
from elisarep.mdhandling import md2docx, md2pdf, export_main_report
from elisarep.reportmd import save_md
from elisarep.config import config as cfg
from elisarep.config import init_config, REFVAL_NAME, DIL_NAME
from elisarep.typing import PathLike, PathLikeOrNone
import elisarep.reportgen as rg

WARNING_DISABLE = True

WINDOW = None


if WARNING_DISABLE:
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', OptimizeWarning)
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def main_report(analysis_dir: PathLike, config_dir: PathLike,
                docxa: bool = True, docxr: bool = False, pdf: bool = True) -> None:
    """ Generate main report
    """
    print(f'Analysis diretory {analysis_dir}')
    print(f'Configuration directory {config_dir}')

    init_config(analysis_dir, config_dir)

    input_files = make_input_paths(analysis_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    reports = rg.gen_report_raw(
        predil_worklist(worklist_file_path),
        read_params(params_file_path),
        read_layouts(path.join(config_dir, cfg['plate_layout_id']),
                     path.join(config_dir, cfg['plate_layout_num']),
                     path.join(config_dir, cfg['plate_layout_dil_id'])),
        make_concentration(
            cfg[REFVAL_NAME], cfg[DIL_NAME]),
        analysis_dir)

    if docxa:
        export_main_report(reports, analysis_dir, cfg['pandoc_bin'],
                           path.join(config_dir, cfg['reference_docx']))

    for report in reports:
        print(f"Report for plate {report['plate']} saved as {report['path']}")
        save_md(report['path'], report['md'])

        if docxr:
            md2docx(cfg['pandoc_bin'],
                    cfg['reference_docx'], report['path'])
        if pdf:
            md2pdf(cfg['pandoc_bin'],
                   cfg['pdflatex_bin'], report['path'])

        binr = bytearray(report['md'], 'utf8')
        t = crc32(binr)
        print(f"CRC for '{report['path']}' is {t}")

    print('Done.')


def browse_analysis(init_folder: PathLikeOrNone) -> None:
    """ Browse analysis folder
    """
    initialdir = getcwd()
    if init_folder:
        initialdir = init_folder
    dirname = filedialog.askdirectory(initialdir=initialdir,
                                      title="Select a Hamilton Analysis Folder")
    if dirname:
        global analysis_folder, entry_analysis
        analysis_folder.set(dirname)
        entry_analysis.update()
        global WINDOW
        WINDOW.destroy()


def browse_config(init_folder: PathLikeOrNone) -> None:
    """ Browse config folder
    """
    dirname = filedialog.askdirectory(initialdir=init_folder,
                                      title="Select a Config Folder")

    if dirname:
        global config_folder
        config_folder.set(dirname)


def gui(config_dir: PathLikeOrNone, init_folder: PathLikeOrNone) -> PathLikeOrNone:
    """ GUI dialaog for data input
    """
    window = Tk()
    window.title('HAMILTON Analysis')
    window.geometry("800x80")

    global analysis_folder
    analysis_folder = StringVar()
    analysis_folder.set('')
    global config_folder
    config_folder = StringVar()
    if config_dir:
        config_folder.set(config_dir)
    else:
        config_folder.set(path.join(getcwd(), 'data'))

    button_analysis = Button(window, text="Browse Analysis Folder",
                             command=lambda: browse_analysis(init_folder))
    button_analysis.grid(column=0, row=0)

    global entry_analysis
    entry_analysis = Entry(textvariable=analysis_folder,
                           state=DISABLED, width=110)
    entry_analysis.grid(row=0, column=1,
                        padx=10, pady=10)

    button_config = Button(window, text="Browse Config Folder",
                           command=lambda: browse_config(config_dir))
    button_config.grid(column=0, row=1)
    entry_config = Entry(textvariable=config_folder, state=DISABLED, width=110)
    entry_config.grid(row=1, column=1,
                      padx=10, pady=10)
    window.mainloop()

    return analysis_folder.get()


def main() -> None:
    """ Main
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--analysis", help="analysis directory", default=None)
    parser.add_argument('--cfg', help="config and params directory",
                        default='./data')
    parser.add_argument('--ifld', help="initial analysis folder", default=None)

    args = parser.parse_args()
    analysis_dir = args.analysis
    if analysis_dir:
        analysis_dir.rstrip("/\\")
    config_dir = args.cfg
    init_folder = args.ifld

    if not analysis_dir:
        analysis_dir = gui(config_dir, init_folder)
    if not analysis_dir:
        print('Canceled.')
        return

    try:
        main_report(analysis_dir, config_dir)
    except Exception as e:
        print(e)
        print('Failed!')


if __name__ == "__main__":
    main()

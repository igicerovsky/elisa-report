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

    report_params = {
        'worklist': predil_worklist(worklist_file_path),
        'params': read_params(params_file_path),
        'layouts': read_layouts(path.join(config_dir, cfg['plate_layout_id']),
                                path.join(config_dir, cfg['plate_layout_num']),
                                path.join(config_dir, cfg['plate_layout_dil_id'])),
        'refconc': make_concentration(
            cfg[REFVAL_NAME], cfg[DIL_NAME])
    }
    reports = rg.gen_report_raw(report_params, analysis_dir)

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


class Gui:
    """ GUI class
    """

    def __init__(self, window, config_dir: PathLikeOrNone, init_folder: PathLikeOrNone) -> None:
        self.window = window
        self.window.title('HAMILTON Analysis')
        self.window.geometry("800x80")
        self.init_folder = init_folder

        self.analysis_folder = StringVar()
        self.analysis_folder.set('')
        self.config_folder = StringVar()
        if config_dir:
            self.config_folder.set(config_dir)
        else:
            self.config_folder.set(path.join(getcwd(), 'data'))

        button_analysis = Button(self.window, text="Browse Analysis Folder",
                                 command=lambda: self.browse_analysis())
        button_analysis.grid(column=0, row=0)

        self.entry_analysis = Entry(textvariable=self.analysis_folder,
                                    state=DISABLED, width=110)
        self.entry_analysis.grid(row=0, column=1,
                                 padx=10, pady=10)

        button_config = Button(self.window, text="Browse Config Folder",
                               command=lambda: self.browse_config())
        button_config.grid(column=0, row=1)
        entry_config = Entry(textvariable=self.config_folder,
                             state=DISABLED, width=110)
        entry_config.grid(row=1, column=1,
                          padx=10, pady=10)

    def browse_analysis(self) -> None:
        """ Browse analysis folder
        """
        initialdir = getcwd()
        if self.init_folder:
            initialdir = self.init_folder
        dirname = filedialog.askdirectory(initialdir=initialdir,
                                          title="Select a Hamilton Analysis Folder")
        if dirname:
            self.analysis_folder.set(dirname)
            self.entry_analysis.update()
            self.window.destroy()

    def browse_config(self) -> None:
        """ Browse config folder
        """
        dirname = filedialog.askdirectory(initialdir=self.config_folder.get(),
                                          title="Select a Config Folder")

        if dirname:
            self.config_folder.set(dirname)

    def res(self) -> None:
        """ Result
        """
        return self.analysis_folder.get(), self.config_folder.get()


def gui_fn(config_dir: PathLikeOrNone, init_folder: PathLikeOrNone) -> PathLikeOrNone:
    """ GUI dialaog for data input
    """
    window = Tk()
    gui = Gui(window, config_dir, init_folder)
    window.mainloop()
    return gui.res()


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
        analysis_dir, config_dir = gui_fn(config_dir, init_folder)
    if not analysis_dir:
        print('Canceled.')
        return

    try:
        main_report(analysis_dir, config_dir)
    except (KeyError, ValueError, FileNotFoundError, Exception, ) as e:
        print(e)
        print('Failed!')


if __name__ == "__main__":
    main()

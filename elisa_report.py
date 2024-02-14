""" Main ELISA report generation script

Generates ELISA report from photometer output; analysis performed on Hamilton robot.
"""

from dataclasses import dataclass
from os import path, getcwd
import argparse
import warnings

from zlib import crc32

from tkinter import StringVar, Button, Entry, NORMAL, DISABLED, Tk
from tkinter import filedialog, messagebox

from scipy.optimize import OptimizeWarning

from elisarep.readdata import read_params
from elisarep.mkinout import make_mdil_path, make_params_path, make_worklist_path
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


@dataclass
class InputFiles:
    """ Input files
    """
    analysis_dir: PathLike
    config_dir: PathLike
    params_file_path: PathLike
    worklist_file_path: PathLike
    mdil_file_path: PathLikeOrNone


def main_report(fl: InputFiles,
                docxa: bool = True, docxr: bool = False, pdf: bool = True) -> None:
    """ Generate main report
    """
    print(f'Analysis diretory {fl.analysis_dir}')
    print(f'Configuration directory {fl.config_dir}')

    init_config(fl.analysis_dir, fl.config_dir)

    report_params = {
        'worklist': predil_worklist(fl.worklist_file_path, fl.mdil_file_path),
        'params': read_params(fl.params_file_path),
        'layouts': read_layouts(path.join(fl.config_dir, cfg['plate_layout_id']),
                                path.join(fl.config_dir,
                                          cfg['plate_layout_num']),
                                path.join(fl.config_dir, cfg['plate_layout_dil_id'])),
        'refconc': make_concentration(
            cfg[REFVAL_NAME], cfg[DIL_NAME])
    }
    reports = rg.gen_report_raw(report_params, fl.analysis_dir)

    if docxa:
        export_main_report(reports, fl.analysis_dir, cfg['pandoc_bin'],
                           path.join(fl.config_dir, cfg['reference_docx']))

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


def add_msg(msg, add: str) -> None:
    """ Add message
    """
    if msg:
        return msg + '\n' + add
    return add


class Gui:
    """ GUI class
    """
    class BrowsePath:
        """ Browse path
        """

        def __init__(self, wnd, text: str, command,
                     col, row,
                     var: str = None,
                     bstate=NORMAL) -> None:  # pylint: disable=too-many-arguments
            self.button = Button(wnd, text=text, command=command, state=bstate)
            self.var = StringVar()
            self.var.set(var)
            self.entry = Entry(textvariable=self.var,
                               state=DISABLED, width=110)
            self.button.grid(column=col, row=row)
            self.entry.grid(row=row, column=col + 1,
                            padx=10, pady=10)

        def val(self) -> str:
            """ Value
            """
            if self.var.get() == 'None':
                return None
            return self.var.get()

        def set(self, val: str) -> None:
            """ Set value
            """
            self.var.set(val)
            self.entry.update()
            self.button['state'] = NORMAL

    def __init__(self, window, config_dir: PathLikeOrNone,
                 init_folder: PathLikeOrNone) -> None:
        self.window = window
        self.window.title('HAMILTON Analysis')
        self.window.geometry("840x220")
        self.init_folder = init_folder
        self.group = {}

        def analysis_fn():
            self.browse_analysis()
        self.group["analysis"] = self.BrowsePath(self.window, text="Browse Analysis Folder",
                                                 command=analysis_fn, row=0, col=0)

        cfg_folder = config_dir if config_dir else path.join(getcwd(), 'data')

        def browse_fn():
            self.browse_config()
        self.group["config"] = self.BrowsePath(self.window, text="Browse Config Folder",
                                               command=browse_fn, row=1, col=0, var=cfg_folder)

        def params_fn():
            self.browse_params()
        self.group["params"] = self.BrowsePath(self.window, text="Browse Parameters File",
                                               command=params_fn, row=2, col=0, bstate=DISABLED)

        def worklist_fn():
            self.browse_worklist()
        self.group["worklist"] = self.BrowsePath(self.window, text="Browse Worklist File",
                                                 command=worklist_fn, row=3, col=0, bstate=DISABLED)

        def mdil_fn():
            self.browse_mdil()
        self.group["mdil"] = self.BrowsePath(self.window, text="Browse Manual Dilution File",
                                             command=mdil_fn, row=4, col=0, bstate=DISABLED)

    def browse_mdil(self) -> None:
        """Browse manual dilution filename"""
        filename = filedialog.askopenfilename(initialdir=self.group["analysis"].val(),
                                              title="Select Manual Dilution File",
                                              filetypes=[('XLS Files', '*.xlsx')])
        if filename:
            self.group["mdil"].set(filename)
            self.check_requirements(self.group["params"].val(),
                                    self.group["worklist"].val(),
                                    filename)

    def browse_worklist(self) -> None:
        """Browse params filename"""
        filename = filedialog.askopenfilename(initialdir=self.group["analysis"].val(),
                                              title="Select Worklist File",
                                              filetypes=[('XLS Files', '*.xls')])
        if filename:
            self.group["worklist"].set(filename)
            self.check_requirements(self.group["worklist"].val(),
                                    filename,
                                    self.group["mdil"].val())

    def browse_params(self) -> None:
        """Brows params filename"""
        filename = filedialog.askopenfilename(initialdir=self.group["analysis"].val(),
                                              title="Select Parameters File",
                                              filetypes=[('CSV Files', '*.csv')])
        if filename:
            self.group["params"].set(filename)
            self.check_requirements(filename,
                                    self.group["worklist"].val(),
                                    self.group["mdil"].val())

    def browse_analysis(self) -> None:
        """ Browse analysis folder
        """
        initialdir = getcwd()
        if self.init_folder:
            initialdir = self.init_folder
        dirname = filedialog.askdirectory(initialdir=initialdir,
                                          title="Select a Hamilton Analysis Folder")
        if dirname:
            self.group["analysis"].set(dirname)
            params_path = make_params_path(dirname)
            worklist_path = make_worklist_path(dirname)
            mdil_path = make_mdil_path(dirname)
            self.check_requirements(params_path, worklist_path, mdil_path)

    def check_requirements(self, params_path, worklist_path, mdil_path) -> None:
        """Check if all requirements are met"""
        msg = None
        if not params_path:
            msg = add_msg(
                msg, "Defalult parameters file is missing \nor file name is invalid.\n")
        self.group["params"].set(params_path)

        if not worklist_path:
            msg = add_msg(
                msg, "Defalult worklist file is missing or \nfile name is invalid.\n")
        self.group["worklist"].set(worklist_path)

        if not mdil_path:
            msg = add_msg(
                msg, "Defalult manual dilution worklist file is missing \nor file name is invalid.")
        self.group["mdil"].set(mdil_path)

        if msg:
            messagebox.showwarning("Invalid file",
                                   msg,
                                   parent=self.window)
        else:
            self.window.destroy()

    def browse_config(self) -> None:
        """ Browse config folder
        """
        dirname = filedialog.askdirectory(initialdir=self.group["config"].val(),
                                          title="Select a Config Folder")

        if dirname:
            self.group["config"].set(dirname)

    def res(self) -> None:
        """ Result
        """
        return (self.group["analysis"].val(), self.group["config"].val(),
                self.group["params"].val(), self.group["worklist"].val(), self.group["mdil"].val())


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
        analysis_dir, config_dir, params_file, worklist_file, mdil_file = gui_fn(
            config_dir, init_folder)
    if not analysis_dir:
        print('Canceled.')
        return

    try:
        main_report(InputFiles(analysis_dir, config_dir,
                    params_file, worklist_file, mdil_file))
    except (KeyError, ValueError, FileNotFoundError, ) as e:
        print(e)
        print('Failed!')


if __name__ == "__main__":
    main()

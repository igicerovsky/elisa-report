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


def svar2path(svar: StringVar) -> PathLikeOrNone:
    """ Convert StringVar to path
    """
    if svar.get() == 'None' or not svar:
        return None
    return svar.get()


class Gui:
    """ GUI class
    """
    class BrowsePath:
        """ Browse path
        """

        def __init__(self, wnd, text: str, command, col, row, var: str = None) -> None:
            self.button = Button(wnd, text=text, command=command)
            self.var = StringVar()
            self.var.set(var)
            self.entry = Entry(textvariable=self.var,
                               state=DISABLED, width=110)
            self.button.grid(column=col, row=row)
            self.entry.grid(row=row, column=col+1,
                            padx=10, pady=10)

    def __init__(self, window, config_dir: PathLikeOrNone,
                 init_folder: PathLikeOrNone) -> None:
        self.window = window
        self.window.title('HAMILTON Analysis')
        self.window.geometry("840x220")
        self.init_folder = init_folder

        def analysis_fn():
            self.browse_analysis()
        self.analysis = self.BrowsePath(self.window, text="Browse Analysis Folder",
                                        command=analysis_fn, row=0, col=0)

        cfg_folder = config_dir if config_dir else path.join(getcwd(), 'data')

        def browse_fn():
            self.browse_config()
        self.config = self.BrowsePath(self.window, text="Browse Config Folder",
                                      command=browse_fn, row=1, col=0, var=cfg_folder)

        def params_fn():
            self.browse_params()
        self.params = self.BrowsePath(self.window, text="Browse Parameters File",
                                      command=params_fn, row=2, col=0)

        def worklist_fn():
            self.browse_worklist()
        self.worklist = self.BrowsePath(self.window, text="Browse Worklist File",
                                        command=worklist_fn, row=3, col=0)

        def mdil_fn():
            self.browse_mdil()
        self.mdil = self.BrowsePath(self.window, text="Browse Manual Dilution File",
                                    command=mdil_fn, row=4, col=0)

    def browse_mdil(self) -> None:
        """Browse manual dilution filename"""
        filename = filedialog.askopenfilename(initialdir=self.analysis.var.get(),
                                              title="Select Manual Dilution File",
                                              filetypes=[('XLS Files', '*.xlsx')])
        if filename:
            self.mdil.var.set(filename)
            self.mdil.entry.update()
            self.check_requirements(svar2path(self.params.var),
                                    svar2path(self.worklist. var),
                                    filename)

    def browse_worklist(self) -> None:
        """Browse params filename"""
        filename = filedialog.askopenfilename(initialdir=self.analysis.var.get(),
                                              title="Select Worklist File",
                                              filetypes=[('XLS Files', '*.xls')])
        if filename:
            self.worklist. var.set(filename)
            self.worklist.entry.update()
            self.check_requirements(svar2path(self.worklist. var),
                                    filename,
                                    svar2path(self.mdil.var))

    def browse_params(self) -> None:
        """Brows params filename"""
        filename = filedialog.askopenfilename(initialdir=self.analysis.var.get(),
                                              title="Select Parameters File",
                                              filetypes=[('CSV Files', '*.csv')])
        if filename:
            self.params.var.set(filename)
            self.params.entry.update()
            self.check_requirements(filename,
                                    svar2path(self.worklist.var),
                                    svar2path(self.mdil.var))

    def browse_analysis(self) -> None:
        """ Browse analysis folder
        """
        initialdir = getcwd()
        if self.init_folder:
            initialdir = self.init_folder
        dirname = filedialog.askdirectory(initialdir=initialdir,
                                          title="Select a Hamilton Analysis Folder")
        if dirname:
            self.analysis.var.set(dirname)
            self.analysis.entry.update()
            params_path = make_params_path(dirname)
            worklist_path = make_worklist_path(dirname)
            mdil_path = make_mdil_path(dirname)
            self.check_requirements(params_path, worklist_path, mdil_path)

    def check_requirements(self, params_path, worklist_path, mdil_path) -> None:
        """Check if all requirements are met"""
        close_win = True
        if not params_path:
            messagebox.showwarning("Invalid file",
                                   "Defalult parameters file is missing \nor file name is invalid.",
                                   parent=self.window)
            close_win = False
        self.params.button['state'] = NORMAL
        self.params.var.set(params_path)
        self.params.entry.update()

        if not worklist_path:
            messagebox.showwarning("Invalid file",
                                   "Defalult worklist file is missing or \nfile name is invalid.",
                                   parent=self.window)
            close_win = False
        self.worklist.button['state'] = NORMAL
        self.worklist.var.set(worklist_path)
        self.worklist.entry.update()

        if not mdil_path:
            messagebox.showwarning("Invalid file",
                                   "Manual dilution worklist file is missing \nor file name is invalid.",
                                   parent=self.window)
            close_win = False
        self.mdil.button['state'] = NORMAL
        self.mdil.var.set(mdil_path)
        self.mdil.entry.update()

        if close_win:
            self.window.destroy()

    def browse_config(self) -> None:
        """ Browse config folder
        """
        dirname = filedialog.askdirectory(initialdir=self.config.var.get(),
                                          title="Select a Config Folder")

        if dirname:
            self.config.var.set(dirname)
            self.config.entry.update()

    def res(self) -> None:
        """ Result
        """
        return (self.analysis.var.get(), self.config.var.get(),
                self.params.var.get(), self.worklist.var.get(), self.mdil.var.get())


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

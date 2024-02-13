""" Main ELISA report generation script

Generates ELISA report from photometer output; analysis performed on Hamilton robot.
"""

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


def main_report(analysis_dir: PathLike, config_dir: PathLike,
                params_file_path: PathLike, worklist_file_path: PathLike,
                mdil_file_path: PathLike,
                docxa: bool = True, docxr: bool = False, pdf: bool = True) -> None:
    """ Generate main report
    """
    print(f'Analysis diretory {analysis_dir}')
    print(f'Configuration directory {config_dir}')

    init_config(analysis_dir, config_dir)

    report_params = {
        'worklist': predil_worklist(worklist_file_path, mdil_file_path),
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


def svar2path(svar: StringVar) -> PathLikeOrNone:
    """ Convert entry to path
    """
    if svar.get() == 'None' or not svar:
        return None
    return svar.get()


class Gui:
    """ GUI class
    """

    def __init__(self, window, config_dir: PathLikeOrNone,
                 init_folder: PathLikeOrNone) -> None:
        self.window = window
        self.window.title('HAMILTON Analysis')
        self.window.geometry("840x220")
        self.init_folder = init_folder

        self.analysis_folder = StringVar()
        self.analysis_folder.set('')
        self.config_folder = StringVar()
        if config_dir:
            self.config_folder.set(config_dir)
        else:
            self.config_folder.set(path.join(getcwd(), 'data'))
        self.params_file = StringVar(value='')
        self.worklist_file = StringVar(value='')
        self.mdil_file = StringVar(value='')

        def analysis_fn():
            self.browse_analysis()
        button_analysis = Button(self.window, text="Browse Analysis Folder",
                                 command=analysis_fn)
        button_analysis.grid(column=0, row=0)

        self.entry_analysis = Entry(textvariable=self.analysis_folder,
                                    state=DISABLED, width=110)
        self.entry_analysis.grid(row=0, column=1,
                                 padx=10, pady=10)

        def browse_fn():
            self.browse_config()
        button_config = Button(self.window, text="Browse Config Folder",
                               command=browse_fn)
        button_config.grid(column=0, row=1)
        self.entry_config = Entry(textvariable=self.config_folder,
                                  state=DISABLED, width=110)
        self.entry_config.grid(row=1, column=1,
                               padx=10, pady=10)

        def params_fn():
            self.browse_params()
        self.button_params = Button(self.window, text="Browse Parameters File",
                                    command=params_fn, state=DISABLED)
        self.button_params.grid(column=0, row=2)
        self.entry_params = Entry(textvariable=self.params_file,
                                  state=DISABLED, width=110)
        self.entry_params.grid(row=2, column=1,
                               padx=10, pady=10)

        def worklist_fn():
            self.browse_worklist()
        self.button_worklist = Button(self.window, text="Browse Worklist File",
                                      command=worklist_fn, state=DISABLED)
        self.button_worklist.grid(column=0, row=3)
        self.entry_worklist = Entry(textvariable=self.worklist_file,
                                    state=DISABLED, width=110)
        self.entry_worklist.grid(row=3, column=1,
                                 padx=10, pady=10)

        def mdil_fn():
            self.browse_mdil()
        self.button_mdil = Button(self.window, text="Browse Manual Dilution File",
                                  command=mdil_fn, state=DISABLED)
        self.button_mdil.grid(column=0, row=4)
        self.entry_mdil = Entry(textvariable=self.mdil_file,
                                state=DISABLED, width=110)
        self.entry_mdil.grid(row=4, column=1,
                             padx=10, pady=10)

    def browse_mdil(self) -> None:
        """Browse manual dilution filename"""
        filename = filedialog.askopenfilename(initialdir=self.analysis_folder.get(),
                                              title="Select Manual Dilution File",
                                              filetypes=[('XLS Files', '*.xlsx')])
        if filename:
            self.mdil_file.set(filename)
            self.entry_mdil.update()
            self.check_requirements(
                svar2path(self.params_file),
                svar2path(self.worklist_file), filename)

    def browse_worklist(self) -> None:
        """Browse params filename"""
        filename = filedialog.askopenfilename(initialdir=self.analysis_folder.get(),
                                              title="Select Worklist File",
                                              filetypes=[('XLS Files', '*.xls')])
        if filename:
            self.worklist_file.set(filename)
            self.entry_worklist.update()
            self.check_requirements(
                svar2path(self.worklist_file),
                filename,
                svar2path(self.mdil_file))

    def browse_params(self) -> None:
        """Brows params filename"""
        filename = filedialog.askopenfilename(initialdir=self.analysis_folder.get(),
                                              title="Select Parameters File",
                                              filetypes=[('CSV Files', '*.csv')])
        if filename:
            self.params_file.set(filename)
            self.entry_params.update()
            self.check_requirements(
                filename,
                svar2path(self.worklist_file),
                svar2path(self.mdil_file))

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
            params_path = make_params_path(dirname)
            worklist_path = make_worklist_path(dirname)
            mdil_path = make_mdil_path(dirname)
            self.check_requirements(params_path, worklist_path, mdil_path)

    def check_requirements(self, params_path, worklist_path, mdil_path) -> None:
        close_win = True
        if not params_path:
            messagebox.showwarning("Invalid file",
                                   "Defalult parameters file is missing or file name is invalid.")
            close_win = False
        self.button_params['state'] = NORMAL
        self.params_file.set(params_path)
        self.entry_params.update()

        if not worklist_path:
            messagebox.showwarning("Invalid file",
                                   "Defalult worklist file is missing or file name is invalid.")
            close_win = False
        self.button_worklist['state'] = NORMAL
        self.worklist_file.set(worklist_path)
        self.entry_worklist.update()

        if not mdil_path:
            messagebox.showwarning("Invalid file",
                                   "Manual worklist file is missing or file name is invalid.")
            close_win = False
        self.button_mdil['state'] = NORMAL
        self.mdil_file.set(mdil_path)
        self.entry_mdil.update()

        if close_win:
            self.window.destroy()
        return None

    def browse_config(self) -> None:
        """ Browse config folder
        """
        dirname = filedialog.askdirectory(initialdir=self.config_folder.get(),
                                          title="Select a Config Folder")

        if dirname:
            self.config_folder.set(dirname)
            self.entry_config.update(dirname)

    def res(self) -> None:
        """ Result
        """
        return (self.analysis_folder.get(), self.config_folder.get(),
                self.params_file.get(), self.worklist_file.get(), self.mdil_file.get())


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
        main_report(analysis_dir, config_dir,
                    params_file, worklist_file, mdil_file)
    except (KeyError, ValueError, FileNotFoundError, ) as e:
        print(e)
        print('Failed!')


if __name__ == "__main__":
    main()

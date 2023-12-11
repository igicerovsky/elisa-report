from os import path, getcwd
import argparse
import warnings

from scipy.optimize import OptimizeWarning
from zlib import crc32

from tkinter import *
from tkinter import filedialog

from hamrep.readdata import read_params
from hamrep.mkinout import make_input_paths
from hamrep.worklist import predil_worklist, check_worklist
from hamrep.sample import make_concentration
from hamrep.readdata import read_layouts
from hamrep.mdhandling import md2docx, md2pdf, export_main_report
from hamrep.reportmd import save_md
from hamrep.config import config as cfg
from hamrep.config import init_config, REFVAL_NAME, DIL_NAME
import hamrep.reportgen as rg

WARNING_DISABLE = True

if WARNING_DISABLE:
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', OptimizeWarning)
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')


def main_report(analysis_dir, config_dir, docxa: bool = True, docxr: bool = False, pdf: bool = True,
                txt_input=True):
    print(f'Analysis diretory {analysis_dir}')
    print(f'Configuration directory {config_dir}')

    init_config(analysis_dir, config_dir)

    input_files = make_input_paths(analysis_dir)
    worklist_file_path = input_files['worklist']
    params_file_path = input_files['params']

    wl_raw = predil_worklist(worklist_file_path)
    params = read_params(params_file_path)
    reference_conc = make_concentration(
        cfg[REFVAL_NAME], cfg[DIL_NAME])

    lay = read_layouts(path.join(config_dir, cfg['plate_layout_id']),
                       path.join(config_dir, cfg['plate_layout_num']),
                       path.join(config_dir, cfg['plate_layout_dil_id']))

    if txt_input:
        reports = rg.gen_report_raw(
            wl_raw, params, lay, reference_conc, analysis_dir)
    else:
        valid_plates = check_worklist(wl_raw)
        reports = rg.gen_report_calc(valid_plates, wl_raw, params, lay,
                                     reference_conc, analysis_dir)

    if docxa:
        export_main_report(reports, analysis_dir, cfg['pandoc_bin'],
                           path.join(config_dir, cfg['reference_docx']))

    for report in reports:
        print('Report for plate {} saved as {}'.format(
            report['plate'], report['path']))
        save_md(report['path'], report['md'])

        if docxr:
            md2docx(cfg['pandoc_bin'],
                    cfg['reference_docx'], report['path'])
        if pdf:
            md2pdf(cfg['pandoc_bin'],
                   cfg['pdflatex_bin'], report['path'])

        binr = bytearray(report['md'], 'utf8')
        t = crc32(binr)
        print("CRC for '{}' is {}".format(report['path'], t))

    print('Done.')


def browse_analysis():
    filename = filedialog.askdirectory(initialdir=getcwd(),
                                       title="Select a Hamilton Analysis Folder")
    global analysis_file, entry_analysis
    analysis_file.set(filename)
    entry_analysis.update()
    global window
    window.destroy()


def browse_config(config_folder):
    filename = filedialog.askdirectory(initialdir=config_folder,  # os.patrh.join(os.getcwd(), 'data'),
                                       title="Select a Config Folder")
    global analysis_file
    analysis_file.set(filename)


def gui(config_dir):
    global window
    window = Tk()
    window.title('HAMILTON Analysis')
    window.geometry("800x100")

    global analysis_file
    analysis_file = StringVar()
    analysis_file.set('...')
    global config_folder
    config_folder = StringVar()
    if config_dir:
        config_folder.set(config_dir)
    else:
        config_folder.set(path.join(getcwd(), 'data'))

    button_analysis = Button(window, text="Browse Analysis Folder",
                             command=browse_analysis)
    button_analysis.grid(column=0, row=0)

    global entry_analysis
    entry_analysis = Entry(textvariable=analysis_file,
                           state=DISABLED, width=110)
    entry_analysis.grid(row=0, column=1,
                        padx=10, pady=10)

    button_config = Button(window, text="Browse Config Folder",
                           command=browse_config)
    button_config.grid(column=0, row=1)
    entry_config = Entry(textvariable=config_folder, state=DISABLED, width=110)
    entry_config.grid(row=1, column=1,
                      padx=10, pady=10)
    window.mainloop()

    main_report(analysis_file.get(), config_folder.get())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--analysis", help="analysis directory", default=None)
    parser.add_argument('--cfg', help="config and params directory",
                        default='./data')
    parser.add_argument('--gui', action='store_true',
                        help="use calc files as input")

    args = parser.parse_args()
    analysis_dir = args.analysis
    if analysis_dir:
        analysis_dir.rstrip("/\\")
    config_dir = args.cfg

    if args.analysis:
        main_report(analysis_dir, config_dir)
    else:
        gui(config_dir)


if __name__ == "__main__":
    main()

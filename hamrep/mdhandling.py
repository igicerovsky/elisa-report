from os import path
import subprocess

from .reportmd import save_md
from .reportmdassembly import assembly
from .mkinout import parse_dir_name


PDFLATEX_EXE = 'c:/Users/hwn6193/AppData/Local/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe'
REFERENCE_DOCX = './data/custom-reference.docx'
PANDOC_PATH = 'c:/work/pandoc/pandoc'


def export_plate_reports(reports, generate_plate_docx, generate_plate_pdf):
    for report in reports:
        print('Report for plate {} saved as {}'.format(report['plate'], report['path']))
        save_md(report['path'], report['md'])
        xlsx_file = path.splitext(report['path'])[0] + '_results.xlsx'
        report['df'].to_excel(xlsx_file)
        report_dir = path.dirname(path.abspath(report['path']))

        if generate_plate_docx:
            docx_path = path.splitext(report['path'])[0] + '.docx'
            print('Generating Word {} from {}'.format(docx_path, report['path']))
            subprocess.run([PANDOC_PATH, '-o', docx_path,
                                '-f', 'markdown', '-t', 'docx',
                                '--resource-path', report_dir,
                                '--reference-doc', REFERENCE_DOCX,
                                report['path']])

        if generate_plate_pdf:
            pdf_path = path.splitext(report['path'])[0] + '.pdf'
            print(f'Generating PDF {pdf_path} from {report["path"]}')
            subprocess.run([PANDOC_PATH, '-o', pdf_path,
                            '--resource-path', report_dir,
                            '--pdf-engine', PDFLATEX_EXE,
                            report['path']])


def export_main_report(reports, working_dir):
    parsed_dir = parse_dir_name(working_dir)
    md_assembly = assembly(reports, protocol=parsed_dir['protocol'])
    mdfile = '{}_{}.md'.format(parsed_dir['date'], parsed_dir['protocol'])
    md_filepath = path.join(working_dir, mdfile)
    save_md(md_filepath, md_assembly)
    docx_path = path.splitext(md_filepath)[0] + '.docx'
    print('Generating Word {} from {}'.format(docx_path, md_filepath))
    subprocess.run([PANDOC_PATH, '-o', docx_path,
                        '-f', 'markdown', '-t', 'docx',
                        '--resource-path', working_dir,
                        '--reference-doc', REFERENCE_DOCX,
                        md_filepath])
from os import path
import subprocess

from .reportmd import save_md
from .reportmdassembly import assembly
from .mkinout import parse_dir_name


def md2docx(pandoc_bin, reference_doc, md_filepath):
    docx_path = path.splitext(md_filepath)[0] + '.docx'
    print('Generating Word {} from {}'.format(docx_path, md_filepath))
    report_dir = path.dirname(path.abspath(md_filepath))
    try:
        subprocess.run([pandoc_bin, '-o', docx_path,
                            '-f', 'markdown', '-t', 'docx',
                            '--resource-path', report_dir,
                            '--reference-doc', reference_doc,
                            md_filepath])
    except Exception as e:
        print(e)


def md2pdf(pandoc_bin, pdflatex_bin, md_filepath):
    pdf_path = path.splitext(md_filepath)[0] + '.pdf'
    print(f'Generating PDF {pdf_path} from {md_filepath}')
    report_dir = path.dirname(path.abspath(md_filepath))
    try:
        subprocess.run([pandoc_bin, '-o', pdf_path,
                        '--resource-path', report_dir,
                        '--pdf-engine', pdflatex_bin,
                        md_filepath])
    except Exception as e:
        print(e)


def export_main_report(reports, working_dir, pandoc_bin, reference_doc):
    parsed_dir = parse_dir_name(working_dir)
    md_assembly = assembly(reports, protocol=parsed_dir['protocol'])
    mdfile = '{}_{}.md'.format(parsed_dir['date'], parsed_dir['protocol'])
    md_filepath = path.join(working_dir, mdfile)
    save_md(md_filepath, md_assembly)

    md2docx(pandoc_bin, reference_doc, md_filepath)
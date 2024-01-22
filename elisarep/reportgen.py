"""Generate reports from raw data files."""

from os import path

from .reportmain import report_plate
from .mkinout import make_output_paths, basename_from_inputdir, parse_dir_name
from .mkinout import find_analysis, parse_photometer_filename
from .typing import PathLike


def gen_report_raw(worklist, params, layout, reference_conc,
                   working_dir: PathLike):
    """Generate report from raw data files"""

    reports = []
    pdr = parse_dir_name(working_dir)
    match_pattern = f'^{pdr["date"]}_{pdr["protocol"]}_.*\.txt$'
    alist = find_analysis(working_dir, match_pattern)
    if not alist:
        raise (FileNotFoundError(
            (f'Analysis data file not found using match pattern {match_pattern}. '
             f'Please export analysis results.')))
    print(alist)
    for analysis_file in alist:
        dc = parse_photometer_filename(analysis_file)
        plate = int(dc['plate'])
        print('Processing plate {plate} of {len(alist)}')

        base_name = basename_from_inputdir(working_dir)
        output_files = make_output_paths(working_dir, base_name, plate)
        report_file_path = output_files['report']

        report_dir = path.dirname(path.abspath(report_file_path))
        info = parse_dir_name(working_dir)
        md, dfres = report_plate(plate, worklist, params, layout,
                                 reference_conc, analysis_file, report_dir,
                                 info)
        reports.append(
            {'md': md, 'df': dfres, 'path': report_file_path, 'plate': plate})

    return reports

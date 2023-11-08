from os import path

from .reportmain import report_plate
from .mkinout import make_output_paths, basename_from_inputdir, parse_dir_name
from .mkinout import find_analysis, parse_photometer_filename, make_input_analysis


def gen_report_raw(worklist, params, layout, reference_conc, working_dir, limits):
    reports = []
    pdr = parse_dir_name(working_dir)
    match_pattern = r'^{}_{}_.*\.txt$'.format(pdr['date'], pdr['protocol'])
    alist = find_analysis(working_dir, match_pattern)
    if not alist:
        raise (Exception(
            f'Analysis data file not found using match pattern {match_pattern}. Please export analysis results.'))
    print(alist)
    for analysis_file in alist:
        dc = parse_photometer_filename(analysis_file)
        plate = int(dc['plate'])
        print('Processing plate {} of {}'.format(plate, len(alist)))

        base_name = basename_from_inputdir(working_dir)
        output_files = make_output_paths(working_dir, base_name, plate)
        report_file_path = output_files['report']

        report_dir = path.dirname(path.abspath(report_file_path))
        info = parse_dir_name(working_dir)
        md, dfres = report_plate(plate, worklist, params, layout,
                                 reference_conc, analysis_file, report_dir,
                                 info, limits
                                 )
        reports.append(
            {'md': md, 'df': dfres, 'path': report_file_path, 'plate': plate})

    return reports


def gen_report_calc(valid_plates, worklist, params, layout, reference_conc, working_dir, limits):
    base_name = basename_from_inputdir(working_dir)
    reports = []
    info = parse_dir_name(working_dir)
    for plate in valid_plates:
        print('Processing plate {} of {}'.format(plate, len(valid_plates)))

        out_files = make_output_paths(working_dir, base_name, plate)
        analysis_file_path = make_input_analysis(working_dir, base_name, plate)
        report_dir = path.dirname(path.abspath(out_files['report']))
        md, dfres = report_plate(plate, worklist, params, layout,
                                 reference_conc, analysis_file_path, report_dir,
                                 info, limits
                                 )
        reports.append(
            {'md': md, 'df': dfres, 'path': out_files['report'], 'plate': plate})
    return reports

from os import path, listdir
from datetime import datetime
import re


def find_analysis(work_dir):
    files = listdir(work_dir)
    pd = parse_dir_name(work_dir)
    rs = r'^{}_{}_.*\.txt$'.format(pd['date'], pd['protocol'])
    r = re.compile(rs)
    ll = []
    for fl in files:
        m = r.match(fl)
        if m:
            ll.append(path.join(work_dir, fl))
    return ll


def parse_photometer_filename(path_name):
    if not path.isfile(path_name):
        raise Exception('Not a directory!')
    fle = path.split(path_name)[1]
    fl = path.splitext(fle)
    s = fl[0].split('_')
    dt = datetime.strptime(s[3]+s[4], "%Y%m%d%H%M%S")
    dc = { 'datetime': dt, 'plate': s[2], 'protocol': s[1]}
    return dc


def parse_dir_name(path_name):
    if path.isdir(path_name):
        path_name = path.basename(path_name)
    else:
        raise Exception('Not directory! {}'.format(path_name))

    s = path_name.split('_')
    if len(s) != 4:
        raise Exception('Invalid method results directory: {}'.format(path_name))

    dc = {'date': s[0], 'protocol': s[1], 'analyst': s[2], 'gn': s[3]}
    return dc


def make_base_name(date, gn):
    return date + '_' + gn + '_-_'


def basename_from_inputdir(input_dir):
    p = parse_dir_name(input_dir)
    return make_base_name(p['date'], p['gn'])


def make_input_paths(input_dir):
    p = parse_dir_name(input_dir)
    base_name = basename_from_inputdir(input_dir)
    worklist = path.join(input_dir, base_name + 'worklist-ELISA.xls')
    if not path.isfile(worklist):
        raise Exception("Worklist file path is invlaid: {}".format(worklist))

    params = path.join(input_dir, base_name + p['protocol'] +'_Parameters.csv')
    if not path.isfile(params):
        raise Exception("Parameters file path is invlaid: {}".format(params))

    return {'worklist': worklist, 'params': params}


def make_input_analysis(input_dir, base_name, plate_id):
    analysis =  path.join(input_dir, base_name + 'calc{}.xlsx'.format(plate_id))
    if not path.isfile(analysis):
        raise Exception("Results file path is invlaid! {}".format(analysis))

    return analysis


def make_output_paths(input_dir, base_name, plate_id):
    base = path.join(input_dir, 'results_plate_{}'.format(plate_id))
    plate = path.join(base, '{}results_plate_{}.md'.format(base_name, plate_id))
    report = path.join(base, '{}report_plate_{}.md'.format(base_name, plate_id))

    return {'plate_results': plate, 'report': report}
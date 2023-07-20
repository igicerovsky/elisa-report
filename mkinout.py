from os import path


# def make_input_paths(input_dir, base_name):
#     worklist = path.join(input_dir, base_name + 'worklist-ELISA.xls')
#     if not path.isfile(worklist):
#         raise Exception("Worklist file path is invlaid: {}".format(worklist))

#     params = path.join(input_dir, base_name + 'AAV9-ELISA_Parameters.csv')

#     return {'worklist': worklist, 'params': params}


def parse_dir_name(path_name):
    print(path_name)
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


def make_input_paths(input_dir):
    print(input_dir)
    p =  parse_dir_name(input_dir)
    print(p)
    base_name = make_base_name(p['date'], p['gn'])
    worklist = path.join(input_dir, base_name + 'worklist-ELISA.xls')
    if not path.isfile(worklist):
        raise Exception("Worklist file path is invlaid: {}".format(worklist))

    params = path.join(input_dir, base_name + p['protocol'] +'_Parameters.csv')
    if not path.isfile(params):
        raise Exception("Parameters file path is invlaid: {}".format(params))

    return {'worklist': worklist, 'params': params}


def make_output_paths(input_dir, base_name, plate_id):
    results =  path.join(input_dir, base_name + 'calc{}.xlsx'.format(plate_id))
    if not path.isfile(results):
        raise Exception("Results file path is invlaid! {}".format(results))
    
    report = path.join(input_dir, 'results_plate_{}'.format(plate_id))
    report = path.join(report, '{}report_plate_{}.md'.format(base_name, plate_id))

    return {'results': results, 'report': report}
from os import path


def make_input_paths(input_dir, base_name):
    worklist = path.join(input_dir, base_name + 'worklist-ELISA.xls')
    if not path.isfile(worklist):
        raise Exception("Worklist file path is invlaid: {}".format(worklist))

    params = path.join(input_dir, base_name + 'AAV9-ELISA_Parameters.csv')

    return {'worklist': worklist, 'params': params}

def make_output_paths(input_dir, base_name, plate_id):
    results =  path.join(input_dir, base_name + 'calc{}.xlsx'.format(plate_id))
    if not path.isfile(results):
        raise Exception("Rewsults file path is invlaid: {}".format(results))
    
    report = path.join(input_dir, 'results_plate_{}'.format(plate_id))
    report = path.join(report, '{}report_plate_{}.md'.format(base_name, plate_id))

    return {'results': results, 'report': report}
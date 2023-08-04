import pandas as pd


def check_worklist(wl):
    valid_plates = []
    for i in range(1, 4):
        invalid_sample = wl['SampleID_{}'.format(i)].isnull().values.any()
        if not invalid_sample: valid_plates.append(i)
    return valid_plates


def read_worklist(worklist_file):
    wl = pd.read_excel(worklist_file)
    wl.set_index([['control 01', 'reference 01', 'blank', 'sample 01', 'sample 02', 'sample 03',
        'sample 04', 'sample 05', 'sample 06', 'sample 07', 'sample 08', 'sample 09', 'sample 10',
        'sample 11', 'sample 12', 'sample 13', 'sample 14', 'sample 15', 'sample 16', 'sample 17',
        'sample 18', 'sample 19', 'sample 20', 'sample 21']], inplace=True)
    check_worklist(wl)
    wl.drop('blank', axis=0, inplace=True)
    wl.index.name = 'Sample type'

    return wl


def worklist_sample(wl, plate_id):
    invalid_sample = wl['SampleID_{}'.format(plate_id)].isnull().values.any()
    if invalid_sample:
        return None, None
    
    cols_id =['SampleID', 'Dilution', 'Viscosity']
    cols = [x + '_' + str(plate_id) for x in cols_id]
    cols_dict = {x : y for x,y in zip(cols_id, cols)}

    return wl[cols], cols_dict

import pandas as pd
from os import path


def check_worklist(wl: pd.DataFrame) -> list:
    valid_plates = []
    for i in range(1, 4):
        invalid_sample = wl['SampleID_{}'.format(i)].isnull().values.any()
        if not invalid_sample:
            valid_plates.append(i)
    return valid_plates


def read_worklist(worklist_file: str) -> pd.DataFrame:
    wl = pd.read_excel(worklist_file)
    wl.set_index([['control 01', 'reference 01', 'blank', 'sample 01', 'sample 02', 'sample 03',
                   'sample 04', 'sample 05', 'sample 06', 'sample 07', 'sample 08', 'sample 09', 'sample 10',
                   'sample 11', 'sample 12', 'sample 13', 'sample 14', 'sample 15', 'sample 16', 'sample 17',
                   'sample 18', 'sample 19', 'sample 20', 'sample 21']], inplace=True)
    check_worklist(wl)
    wl.drop('blank', axis=0, inplace=True)
    wl.index.name = 'Sample type'

    return wl


def worklist_sample(wl: pd.DataFrame, plate_id: int) -> tuple:
    invalid_sample = wl['SampleID_{}'.format(plate_id)].isnull().values.any()
    if invalid_sample:
        return None, None

    cols_id = ['SampleID', 'Dilution', 'Viscosity']
    cols = [x + '_' + str(plate_id) for x in cols_id]
    cols_dict = {x: y for x, y in zip(cols_id, cols)}

    return wl[cols], cols_dict


def predil_worklist(worklist_file: str) -> pd.DataFrame:
    MANUAL_DILUTION_EXT_NAME = '_ManualDil'
    wl = read_worklist(worklist_file)

    worklist_predil_path = path.splitext(
        worklist_file)[0] + MANUAL_DILUTION_EXT_NAME + '.xlsx'
    if path.isfile(worklist_predil_path):
        print(f'Reading pre-dilution from {worklist_predil_path}')
        wl_pdil = read_worklist(worklist_predil_path)

        wl['Dilution_1'] = wl['Dilution_1'] * wl_pdil['Dilution_1']
        wl['Dilution_2'] = wl['Dilution_2'] * wl_pdil['Dilution_2']
        wl['Dilution_3'] = wl['Dilution_3'] * wl_pdil['Dilution_3']
        wl['Dilution_4'] = wl['Dilution_4'] * wl_pdil['Dilution_4']

    return wl

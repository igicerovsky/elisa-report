""" Worklist handling
"""

from os import path

import pandas as pd

from .typing import PathLike


def check_worklist(wl: pd.DataFrame) -> list:
    """ Find number of valid plates in worklist
    """
    valid_plates = []
    for i in range(1, 4):
        invalid_sample = wl[f'SampleID_{i}'].isnull().values.any()
        if not invalid_sample:
            valid_plates.append(i)
    return valid_plates


def read_worklist(worklist_file: str) -> pd.DataFrame:
    """ Read Hamilton-friendly worklist
    """
    wl = pd.read_excel(worklist_file)
    wl.set_index([['control 01', 'reference 01', 'blank',
                   'sample 01', 'sample 02', 'sample 03',
                   'sample 04', 'sample 05', 'sample 06',
                   'sample 07', 'sample 08', 'sample 09',
                   'sample 10', 'sample 11', 'sample 12',
                   'sample 13', 'sample 14', 'sample 15',
                   'sample 16', 'sample 17', 'sample 18',
                   'sample 19', 'sample 20', 'sample 21']], inplace=True)
    check_worklist(wl)
    wl.drop('blank', axis=0, inplace=True)
    wl.index.name = 'Sample type'

    return wl


def worklist_sample(wl: pd.DataFrame, plate_id: int) -> tuple:
    """ Create samples from worklist for given plate
    """
    invalid_sample = wl[f'SampleID_{plate_id}'].isnull().values.any()
    if invalid_sample:
        return None, None

    cols_id = ['SampleID', 'Dilution', 'Viscosity']
    cols = [x + '_' + str(plate_id) for x in cols_id]
    cols_dict = dict(zip(cols_id, cols))

    return wl[cols], cols_dict


def predil_worklist(worklist_file: PathLike, worklist_predil_path: PathLike) -> pd.DataFrame:
    """ Create pre-dilution from worklist
    """
    wl = read_worklist(worklist_file)

    if path.isfile(worklist_predil_path):
        print(f'Reading pre-dilution from {worklist_predil_path}')
        wl_pdil = read_worklist(worklist_predil_path)

        wl['Dilution_1'] = wl['Dilution_1'] * wl_pdil['Dilution_1']
        wl['Dilution_2'] = wl['Dilution_2'] * wl_pdil['Dilution_2']
        wl['Dilution_3'] = wl['Dilution_3'] * wl_pdil['Dilution_3']
        wl['Dilution_4'] = wl['Dilution_4'] * wl_pdil['Dilution_4']

    return wl

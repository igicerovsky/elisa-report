"""Routines handling file naming conventions

This module contains routines for parsing filenames, and creation of 
base name for files and directories.
"""

from os import path, listdir
from datetime import datetime
import re

from .typing import PathLike


def find_analysis(work_dir: PathLike, match_pattern: str) -> list:
    """ Find analysis files in directory
    """
    files = listdir(work_dir)
    # rs = r'^{}_{}_.*\.txt$'.format(pd['date'], pd['protocol'])
    r = re.compile(match_pattern)
    ll = []
    for fl in files:
        m = r.match(fl)
        if m:
            ll.append(path.join(work_dir, fl))
    return ll


def parse_photometer_filename(path_name: PathLike) -> dict:
    """Parses analysis filename

    Parameters
    ----------
        path_name: path_like

    Returns
    -------
    dictionary
        dictionary containing parsed `datetime`, `plate` number and `protocol name`

    Raises
    ------
    Exception
        If pathname isn't a file exception is raised.
    """
    if not path.isfile(path_name):
        raise FileNotFoundError('Not a file!')
    fle = path.split(path_name)[1]
    fl = path.splitext(fle)
    s = fl[0].split('_')
    if len(s) != 5:
        raise NameError(
            f'Plate file is invalid! {fle}\n It shall contain 5 items delimited by \'_\'')
    dt = datetime.strptime(s[3]+s[4], "%Y%m%d%H%M%S")
    dc = {'datetime': dt, 'plate': s[2], 'protocol': s[1]}
    return dc


def parse_dir_name(path_name: PathLike) -> dict:
    """Parses directory name

    Parameters
    ----------
    path_name: path_like
        analysis directory path

    Returns
    -------
    dictionary
        dictionary containing parsed `date`, `protocol`, `analyst` and `gn`

    Raises
    ------
    Exception
        If pathname isn't a directory exception is raised.
    """
    if path.isdir(path_name):
        path_name = path.basename(path_name)
    else:
        raise FileNotFoundError(f'Not directory! {path_name}')

    s = path_name.split('_')
    if len(s) != 4:
        raise NameError(
            'Invalid method results directory: {path_name}')

    dc = {'date': s[0], 'protocol': s[1], 'analyst': s[2], 'gn': s[3]}
    return dc


def make_base_name(date: str, gn: str) -> str:
    """Create base report name

    Parameters:
    -----------
    date: string
        parsed date
    gn: string
        identifier

    Returns
    -------
    string
        Concatenated base name
    """
    return date + '_' + gn + '_-_'


def basename_from_inputdir(input_dir: PathLike) -> str:
    """Create base name from input folder name

    Parameters:
    -----------
    inout_dir: path_like
        directory where measurements are located

    Returns:
    string
        Base name
    """
    p = parse_dir_name(input_dir)
    return make_base_name(p['date'], p['gn'])


def make_input_paths(input_dir: PathLike) -> dict:
    """Make worklist and parameters path names

    Worklist and parameters files have fixed formats defined in README.md

    Parameters:
    -----------
    input_dir: path_like
        directory where measurements are located

    Returns
    -------
    dictionary
        Paths to `worklist` and `params` files
    """
    p = parse_dir_name(input_dir)
    base_name = basename_from_inputdir(input_dir)
    worklist = path.join(input_dir, base_name + 'worklist-ELISA.xls')
    if not path.isfile(worklist):
        raise FileNotFoundError(f"Worklist file path is invlaid: {worklist}")

    params = path.join(input_dir, base_name +
                       p['protocol'] + '_Parameters.csv')
    if not path.isfile(params):
        raise FileNotFoundError("Parameters file path is invlaid: {params}")

    return {'worklist': worklist, 'params': params}


def make_output_paths(input_dir: PathLike, base_name: str, plate_id: int) -> dict:
    """Make output data paths

    Parameters:
    -----------
    input_dir: path_like
        Analysis input directory
    base_name: string
        Analysis base name
    plate_id: int
        Plate number to be processed

    Returns:
    dictionary
        File path to 'plate_results' 'report'
    """
    base = path.join(input_dir, f'results_plate_{plate_id}')
    plate = path.join(base, f'{base_name}results_plate_{plate_id}.md')
    report = path.join(base, f'{base_name}report_plate_{plate_id}')

    return {'plate_results': plate, 'report': report}

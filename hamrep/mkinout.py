"""Routines handling file naming conventions

This module contains routines for parsing filenames, and creation of 
base name for files and directories.
"""

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
        raise Exception('Not a file!')
    fle = path.split(path_name)[1]
    fl = path.splitext(fle)
    s = fl[0].split('_')
    dt = datetime.strptime(s[3]+s[4], "%Y%m%d%H%M%S")
    dc = {'datetime': dt, 'plate': s[2], 'protocol': s[1]}
    return dc


def parse_dir_name(path_name):
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
        raise Exception('Not directory! {}'.format(path_name))

    s = path_name.split('_')
    if len(s) != 4:
        raise Exception(
            'Invalid method results directory: {}'.format(path_name))

    dc = {'date': s[0], 'protocol': s[1], 'analyst': s[2], 'gn': s[3]}
    return dc


def make_base_name(date, gn):
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


def basename_from_inputdir(input_dir):
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


def make_input_paths(input_dir):
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
        raise Exception("Worklist file path is invlaid: {}".format(worklist))

    params = path.join(input_dir, base_name +
                       p['protocol'] + '_Parameters.csv')
    if not path.isfile(params):
        raise Exception("Parameters file path is invlaid: {}".format(params))

    return {'worklist': worklist, 'params': params}


def make_input_analysis(input_dir, base_name, plate_id):
    """Make file path to analysis results (measured data) located in analysis/input directory

    Parameters:
    -----------
    input_dir: path_like
        Analysis input directory
    base_name: string
        Analysis base name
    plate_id: int
        Plate number to be processed

    Raises:
    -------
    Exception
        If given analysis file doesn't exist an exception is raised

    Returns:
    --------
    path_like
        File name of an analysis results
    """
    analysis = path.join(input_dir, base_name + 'calc{}.xlsx'.format(plate_id))
    if not path.isfile(analysis):
        raise Exception("Analysis file path is invlaid! {}".format(analysis))

    return analysis


def make_output_paths(input_dir, base_name, plate_id):
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
    base = path.join(input_dir, 'results_plate_{}'.format(plate_id))
    plate = path.join(
        base, '{}results_plate_{}.md'.format(base_name, plate_id))
    report = path.join(
        base, '{}report_plate_{}.md'.format(base_name, plate_id))

    return {'plate_results': plate, 'report': report}

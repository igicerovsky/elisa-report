"""Plate layout handling functions
"""
import pandas as pd


def to_matrix(l, n):
    """Convert list to matrix

    Parameters:
    -----------
    l : list
      List to be rearanged as 2D list
    n : int
      Number of columns

    Raises:
    -------
    Exception
      If list cannot be resized to matrix, number of columns is invalid.
    """

    if (len(l) % n) != 0:
        raise ValueError(
            f"Number of columns {n} not allowed! {len(l)} % {n} != 0 ({len(l) % n})")
    return [l[i:i+n] for i in range(0, len(l), n)]


def index_plate_layout(plate_layout):
    """ Index plate layout
    """
    plate_layout.set_index(
        [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], inplace=True)
    plate_layout.columns = range(1, plate_layout.columns.size + 1)

    return plate_layout


def to_plate_layout(lst):
    """ List to DataFrame for plate
    """
    l_2d = to_matrix(lst, 8)
    plate_layout = pd.DataFrame(l_2d).T

    return index_plate_layout(plate_layout)


def read_plate_layout(file_path):
    """ Read plate layout from file
    """
    plate_layout = pd.read_csv(file_path)
    index_plate_layout(plate_layout)

    return plate_layout


def save_plate_layout_csv(layout_list, out_file):
    """ Save plate layout
    """
    l = to_plate_layout(layout_list)
    l.to_csv(out_file, index=False)

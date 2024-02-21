""" Configuration for ELISA module

Global config used in elisarep module.
"""

from os import path
import json

from .typing import PathLike


VERSION = '0.1.7'
DESCRIPTION = 'Hamilton report generation for ELISA'
LONG_DESCRIPTION = 'Genrate report from Hamilton photometer output for ELISA.'
NAME = 'elisarep'

CONFIG_FILENAME = 'config.json'

REFVAL_NAME = 'referenceValue'
LIMITS_NAME = 'limits'
DIL_NAME = 'dilutions'
SOP_NAME = 'SOP'
MHF_NAME = 'MHF'

config = {}


def analysis_type(analysis_dir: PathLike) -> dict:
    """ Retrieve analysis type
    """
    if analysis_dir.lower().find('aav9') != -1:
        config['a_type'] = 'AAV9'
        print('Applying parameters for AAV9.')
    elif analysis_dir.lower().find('aav8') != -1:
        config['a_type'] = 'AAV8'
        print('Applying parameters for AAV8.')
    else:
        config['a_type'] = 'default'
        print('Applying default/custom parameters.')
    return config['a_type']


def init_config(analysis_dir: PathLike, config_dir: PathLike) -> None:
    """ Initialize config
    """
    a_type = analysis_type(analysis_dir)
    read_config(path.join(config_dir, CONFIG_FILENAME), a_type)


def read_config(filename: PathLike, a_type: str) -> dict:
    """ Read config from file
    """
    keys = ['pandoc_bin', 'pdflatex_bin', 'reference_docx',
            'plate_layout_id', 'plate_layout_num', 'plate_layout_dil_id', 'numeric_warning_disable',
            DIL_NAME]
    k_type = ['AAV8', 'AAV9', 'default']
    with open(filename, encoding="utf-8") as json_config:
        items = json.load(json_config).items()
        if not items:
            raise ValueError(f"Config file '{filename}' is empty!")
        for key, value in items:
            if key in keys:
                config[key] = value
            elif not key in k_type:
                raise KeyError(key)
        dc = dict(items)
        if a_type in dc:
            config[REFVAL_NAME] = dc[a_type][REFVAL_NAME]
            config[LIMITS_NAME] = dc[a_type][LIMITS_NAME]
            config[SOP_NAME] = dc[a_type][SOP_NAME]
            config[MHF_NAME] = dc[a_type][MHF_NAME]
        elif not a_type in k_type:
            raise (KeyError(
                f"Analysis type '{a_type}' copuld not be identified! Shall be one of {k_type}. "))

    return config

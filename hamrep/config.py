from os import path
import json

CONFIG_FILENAME = 'config.json'

REFVAL_NAME = 'referenceValue'
LIMITS_NAME = 'limits'
DIL_NAME = 'dilutions'

config = {
    "default": {
        "referenceValue": 1.0E+10,
        "limits": [
            1.0E+10,
            1.0E+12
        ]
    },
    "dilutions": [
        1.0,
        2.0,
        4.0,
        8.0,
        16.0,
        32.0,
        64.0
    ]
}


def init_config(analysis_dir, config_dir):
    read_config(path.join(config_dir, CONFIG_FILENAME))
    a_type = analysis_type(analysis_dir)
    config[REFVAL_NAME] = config[a_type][REFVAL_NAME]
    config[LIMITS_NAME] = config[a_type][LIMITS_NAME]


def read_config(filename):
    keys = ['pandoc_bin', 'pdflatex_bin', 'reference_docx', 'params_filename',
            'plate_layout_id', 'plate_layout_num', 'plate_layout_dil_id', 'numeric_warning_disable',
            'AAV8', 'AAV9', 'default', DIL_NAME]
    with open(filename) as json_config:
        for key, value in json.load(json_config).items():
            if key in keys:
                config[key] = value
            else:
                raise KeyError(key)


def analysis_type(analysis_dir):
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

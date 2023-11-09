import pandas as pd
from .layouthandle import read_plate_layout, to_matrix
from os import path
import json
import chardet
from pathlib import Path
from io import StringIO


def get_encoding(file_name):
    blob = Path(file_name).read_bytes()
    result = chardet.detect(blob)
    charenc = result['encoding']

    return charenc


SKIP_LINES = 3
SKIP_BEGIN = 1


def read_exported_data(file_name):
    count = 0
    csv_str = ''
    char_enc = get_encoding(file_name)
    with open(file_name, encoding=char_enc) as fp:
        for line in fp:
            count += 1
            if count < SKIP_LINES:
                continue
            sline = line.rstrip('\n')
            cline = sline.replace('\t', ',')
            cline = cline.rstrip(',')
            cline = cline[SKIP_BEGIN:]
            csv_str += cline + '\n'
            if count == 12:
                break
    return csv_str


def read_data_txt(file_path):
    strdata = read_exported_data(file_path)
    csv_io = StringIO(strdata)
    df = pd.read_csv(csv_io, sep=",")
    # TODO: move ranges to config file
    df_450 = get_data_crop(df, range(0, 8), range(1, 13))
    df_630 = get_data_crop(df, range(0, 8), range(14, 26))

    return df_450, df_630


def to_multi_index(df_single_index, name):
    df_multi_idx = df_single_index.stack().to_frame()
    df_multi_idx.columns = [name]

    return df_multi_idx


def index_plate_layout(plate_layout):
    plate_layout.set_index(
        [['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], inplace=True)
    plate_layout.columns = range(1, plate_layout.columns.size + 1)

    return plate_layout


def to_plate_layout(lst):
    l_2d = to_matrix(lst, 8)
    plate_layout = pd.DataFrame(l_2d).T
    # plate_layout.set_index([['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], inplace=True)
    # plate_layout.columns = range(1, plate_layout.columns.size + 1)

    return index_plate_layout(plate_layout)


def save_plate_layout_csv(layout_list, out_file):
    l = to_plate_layout(layout_list)
    l.to_csv(out_file)


def get_data_crop(df, row_span, col_span):
    crop = df.iloc[row_span, col_span].copy()
    crop.reset_index(drop=True, inplace=True)
    crop.set_index([['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], inplace=True)
    crop.columns = range(1, crop.columns.size+1)
    return crop


def read_data_xls(file_path):
    data = pd.read_excel(file_path, sheet_name=None)
    df_450 = get_data_crop(data["Data"], range(2, 10), range(2, 14))
    df_630 = get_data_crop(data["Data"], range(2, 10), range(15, 27))

    return df_450, df_630


def read_concat_data(data_file_path):
    ext = path.splitext(data_file_path)[1]
    if ext == '.txt':
        read_fn = read_data_txt
    elif ext == '.xlsx':
        read_fn = read_data_xls
    else:
        raise Exception(f'Invalid inpit data file {data_file_path}')

    df_450, df_630 = read_fn(data_file_path)
    df_delta = df_450 - df_630
    df_delta_all = to_multi_index(df_delta, "OD_delta")
    df_450_all = to_multi_index(df_450, "OD_450")
    df_630_all = to_multi_index(df_630, "OD_630")

    return pd.merge(df_delta_all,
                    pd.merge(df_450_all, df_630_all,
                             left_index=True, right_index=True),
                    left_index=True, right_index=True)


def concat_layouts(playout_id, playout_num, playout_dil_id):
    res = to_multi_index(playout_id, 'plate_layout_ident')
    res = pd.merge(res, to_multi_index(
        playout_num, 'plate_layout_num'), left_index=True, right_index=True)
    res = pd.merge(res, to_multi_index(
        playout_dil_id, 'plate_layout_dil_id'), left_index=True, right_index=True)

    return res


def concat_data_with_layouts(df_data, df_layout):
    return pd.merge(df_data, df_layout, left_index=True, right_index=True)


def read_params(file_path):
    params = pd.read_csv(file_path, sep=';')
    params.set_index('Variable', inplace=True)

    return params


def read_layouts(file_id, file_num, file_dil):
    plate_layout_id = read_plate_layout(file_id)
    plate_layout_num = read_plate_layout(file_num)
    plate_layout_dil_id = read_plate_layout(file_dil)

    return concat_layouts(plate_layout_id, plate_layout_num, plate_layout_dil_id)


def read_params_json(analysis_dir, config_dir, params_filename, a_type):
    params_path_default = path.join(config_dir, params_filename)
    params_path_local = path.join(analysis_dir, params_filename)
    params_path = None

    if path.exists(params_path_local):
        params_path = params_path_local
        print(f'Loading local params {params_path}')
    elif path.exists(params_path_default):
        params_path = params_path_default
        print(f'Loading default params {params_path}')
    else:
        raise Exception(
            f'Parameters file not found {params_path_local}, {params_path_default}')
    with open(params_path_default) as json_file:
        data = json.load(json_file)
        dilutions = data['dilutions']
        ref_val_max = data[a_type]['referenceValue']
        limits = data[a_type]['limits']

    return ref_val_max, dilutions, limits

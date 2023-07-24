import pandas as pd
from layouthandle import read_plate_layout
from os import path
import json


def to_multi_index(df_single_index, name):
  df_multi_idx = df_single_index.stack().to_frame()
  df_multi_idx.columns = [name]

  return df_multi_idx

def to_matrix(l, n):
  return [l[i:i + n] for i in range(0, len(l), n)]


def index_plate_layout(plate_layout):
  plate_layout.set_index([['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], inplace=True)
  plate_layout.columns = range(1, plate_layout.columns.size + 1)

  return plate_layout


def to_plate_layout(lst):
  l_2d = to_matrix(lst, 8)
  plate_layout = pd.DataFrame(l_2d).T
  #plate_layout.set_index([['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']], inplace=True)
  #plate_layout.columns = range(1, plate_layout.columns.size + 1)

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
  df_450, df_630 = read_data_xls(data_file_path)
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
  res = pd.merge(res, to_multi_index(playout_num, 'plate_layout_num'), left_index=True, right_index=True)
  res = pd.merge(res, to_multi_index(playout_dil_id, 'plate_layout_dil_id'), left_index=True, right_index=True)

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


def read_params_json(working_dir, data_dir, params_filename):
    params_path_default = path.join(data_dir, params_filename)
    params_path_local = path.join(working_dir, params_filename)
    params_path = None

    if path.exists(params_path_local):
        params_path = params_path_local
        print(f'Loading local params {params_path}')
    elif path.exists(params_path_default):
        params_path = params_path_default
        print(f'Loading default params {params_path}')
    else:
        raise Exception(f'Parameters file not found {params_path_local}, {params_path_default}')

    with open(params_path_default) as json_file:
        data = json.load(json_file)
        dilutions = data['dilutions']
        ref_val_max = data['referenceValue']

    return ref_val_max, dilutions

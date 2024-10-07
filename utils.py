import os
import shutil

import pandas as pd


def my_round(raw):
    if pd.isna(raw):
        return raw
    else:
        return round(raw)

def init_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def read_csv(file_path,descriptions_csv=None,type=None):
    data_csv = pd.read_csv(file_path)
    data_csv = data_csv.dropna(subset=["id"])
    if descriptions_csv is not None and type is not None:
        data_csv = pd.merge(
            data_csv,
            descriptions_csv[descriptions_csv["type"] == type],
            on="id",
            how="left",
        )
    return data_csv
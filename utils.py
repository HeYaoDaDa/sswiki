import os
import re
import shutil
from typing import Any

import json5
import pandas as pd


def is_empty(s) -> bool:
    return pd.isna(s) or not s


def get_description(description_csv: pd.Series) -> str:
    description = ""
    if not pd.isna(description_csv["text1"]):
        description += description_csv["text1"]
    if not pd.isna(description_csv["text2"]):
        description += "\n" + description_csv["text2"]
    if not pd.isna(description_csv["text3"]):
        description += "\n" + description_csv["text3"]
    if not pd.isna(description_csv["text4"]):
        description += "\n" + description_csv["text4"]
    return description


def split_tags(tags) -> list[str]:
    if is_empty(tags):
        return []
    else:
        return tags.split(", ")

def get_img(img) -> str:
    if is_empty(img):
        return '/favicon.png'
    else:
        return '/' + img

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


def read_csv(file_path, descriptions_csv=None, des_type=None):
    data_csv = pd.read_csv(file_path)
    data_csv = data_csv.dropna(subset=["id"])
    if descriptions_csv is not None and des_type is not None:
        data_csv = pd.merge(
            data_csv,
            descriptions_csv[descriptions_csv["type"] == des_type],
            on="id",
            how="left",
        )
    return data_csv


def read_ss_json(file_path) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()
        # 分割成行，并删除每行中的#号及其后面的内容
        lines = file_content.splitlines()
        processed_lines = [line.split("#")[0] for line in lines if line]
        # 补上value处的引号
        processed_lines = [
            re.sub(
                r'("[\S ]+":)([_,a-z,A-Z]+)([,\}])',
                r'\1"\2"\3',
                processed_line,
            )
            for processed_line in processed_lines
        ]
        processed_lines = [
            re.sub(r"\[([_,a-z,A-Z]+)\]", r'["\1"]', processed_line)
            for processed_line in processed_lines
        ]
        # 将处理后的内容合并为一个字符串
        processed_content = "\n".join(processed_lines)
        return json5.loads(processed_content)

import os
import logging
import shutil

import pandas as pd

import generate_ship
import generate_ship_system

logging.basicConfig(level=logging.INFO)


def init_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)


SS_DIR = r"C:\Users\ecquaria\Documents\ss\starsector_cn"
work_dir = os.path.dirname(os.path.abspath(__file__))
md_hulls_dir = os.path.join(work_dir, "hulls")
md_ship_systems_dir = os.path.join(work_dir, "shipsystems")
init_folder(md_hulls_dir)
init_folder(md_ship_systems_dir)

descriptions_csv_path = os.path.join(SS_DIR, "data/strings/descriptions.csv")
descriptions_csv = pd.read_csv(descriptions_csv_path)
descriptions_csv = descriptions_csv.dropna(subset=["id"])

wing_data_csv_path = os.path.join(SS_DIR, "data/hulls/wing_data.csv")
wing_data_csv = pd.read_csv(wing_data_csv_path)
wing_data_csv = wing_data_csv.dropna(subset=["id"])

ship_data_csv_path = os.path.join(SS_DIR, "data/hulls/ship_data.csv")
ship_data_csv = pd.read_csv(ship_data_csv_path)
ship_data_csv = ship_data_csv.dropna(subset=["id"])
ship_data_csv = pd.merge(
    ship_data_csv,
    descriptions_csv[descriptions_csv["type"] == "SHIP"],
    on="id",
    how="left",
)

ship_systems_csv_path = os.path.join(SS_DIR, "data/shipsystems/ship_systems.csv")
ship_systems_csv = pd.read_csv(ship_systems_csv_path)
ship_systems_csv = ship_systems_csv.dropna(subset=["id"])
ship_systems_csv = pd.merge(
    ship_systems_csv,
    descriptions_csv[descriptions_csv["type"] == "SHIP_SYSTEM"],
    on="id",
    how="left",
)

ship_system_list_map = {}
for _, ship_system in ship_systems_csv.iterrows():
    ship_system_md, ship_system_name = generate_ship_system.generate_ship_system(
        ship_system
    )

    ship_system_list_map[ship_system["id"]] = ship_system_name

    ship_system_file = os.path.join(md_ship_systems_dir, ship_system["id"])
    with open(ship_system_file + ".md", "w", encoding="utf-8") as file:
        file.write(ship_system_md)
with open(os.path.join(work_dir, "shipsystems.md"), "w", encoding="utf-8") as file:
    md = '# 战术系统\n\n'
    for key, value in ship_system_list_map.items():
        md += f"[{value}](shipsystems/{key}.md)\n"
    file.write(md)

(ship_dict, ship_skin_dict) = generate_ship.read_ship_jsons(
    os.path.join(SS_DIR, "data/hulls")
)
hull_list_map = {}
for ship_id, ship_json in ship_dict.items():
    ship_data_result = ship_data_csv.loc[ship_data_csv["id"] == ship_id]
    if ship_data_result.empty:
        logging.warning("ship id %s miss ship_data.csv", ship_id)
        continue
    ship_data = ship_data_result.iloc[0]
    logging.info("generate ship skin:%s", ship_id)
    hull_md, hull_name = generate_ship.generate_ship(
        ship_data, ship_json, None, ship_systems_csv
    )
    hull_list_map[ship_id] = hull_name
    hull_file = os.path.join(md_hulls_dir, ship_id)
    with open(hull_file + ".md", "w", encoding="utf-8") as file:
        file.write(hull_md)
for ship_id, ship_skin_json in ship_skin_dict.items():
    base_ship_id = ship_skin_json["baseHullId"]
    ship_data_result = ship_data_csv.loc[ship_data_csv["id"] == base_ship_id]
    if ship_data_result.empty:
        logging.warning("skin base ship id %s miss ship_data.csv", base_ship_id)
        continue
    ship_data = ship_data_result.iloc[0]
    logging.info("generate ship skin:%s", ship_id)
    hull_md, hull_name = generate_ship.generate_ship(
        ship_data,
        ship_dict[base_ship_id],
        ship_skin_json,
        ship_systems_csv,
    )
    hull_list_map[ship_id] = hull_name
    hull_file = os.path.join(md_hulls_dir, ship_id)
    with open(hull_file + ".md", "w", encoding="utf-8") as file:
        file.write(hull_md)
with open(os.path.join(work_dir, "hulls.md"), "w", encoding="utf-8") as file:
    hulls_md = "# 舰船\n\n"
    for key, value in hull_list_map.items():
        hulls_md += f"[{value}](hulls/{key}.md)\n"
    file.write(hulls_md)

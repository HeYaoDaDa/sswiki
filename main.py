import logging
import os

import generate_hull_mod
import generate_ship
import utils
from config import SS_DIR
from ship import Ship
from ship_system import ShipSystem

logging.basicConfig(level=logging.INFO)

work_dir = os.path.dirname(os.path.abspath(__file__))
md_hulls_dir = os.path.join(work_dir, "hulls")
md_ship_systems_dir = os.path.join(work_dir, "shipsystems")
md_hull_mods_dir = os.path.join(work_dir, "hullmods")
utils.init_folder(md_hulls_dir)
utils.init_folder(md_ship_systems_dir)
utils.init_folder(md_hull_mods_dir)

descriptions_csv = utils.read_csv(os.path.join(SS_DIR, "strings/descriptions.csv"))

ship_system_csvs = utils.read_csv(
    os.path.join(SS_DIR, "shipsystems/ship_systems.csv"),
    descriptions_csv,
    "SHIP_SYSTEM",
)
wing_data_csv = utils.read_csv(os.path.join(SS_DIR, "hulls/wing_data.csv"))
hull_mods_csv = utils.read_csv(os.path.join(SS_DIR, "hullmods/hull_mods.csv"))
ship_data_csv = utils.read_csv(
    os.path.join(SS_DIR, "hulls/ship_data.csv"), descriptions_csv, "SHIP"
)
weapon_data_csv = utils.read_csv(
    os.path.join(SS_DIR, "weapons/weapon_data.csv"), descriptions_csv, "WEAPON"
)
# Ship System
ship_system_id_map: dict[str, ShipSystem] = {}
for _, ship_system_csv in ship_system_csvs.iterrows():
    ship_system = ShipSystem(ship_system_csv)
    ship_system_id_map[ship_system.id] = ship_system
# Ship mod
hull_mod_list_map = {}
for _, hull_mod in hull_mods_csv.iterrows():
    hull_mod_md, hull_mod_name = generate_hull_mod.generate_hull_mod(hull_mod)

    hull_mod_list_map[hull_mod["id"]] = hull_mod_name

    hull_mod_file = os.path.join(md_hull_mods_dir, hull_mod["id"])
    with open(hull_mod_file + ".md", "w", encoding="utf-8") as file:
        file.write(hull_mod_md)
with open(os.path.join(work_dir, "hullmods.md"), "w", encoding="utf-8") as file:
    md = "# 舰船插件\n\n"
    for key, value in hull_mod_list_map.items():
        md += f"[{value}](hullmods/{key}.md)\n"
    file.write(md)
# Ship
ship_id_map: dict[str, Ship] = {}
#
(ship_dict, ship_skin_dict) = generate_ship.read_ship_jsons(
    os.path.join(SS_DIR, "hulls")
)
hull_list_map = {}
for ship_id, ship_json in ship_dict.items():
    ship_data_result = ship_data_csv.loc[ship_data_csv["id"] == ship_id]
    if ship_data_result.empty:
        logging.warning("ship id %s miss ship_data.csv", ship_id)
        continue
    ship_data = ship_data_result.iloc[0]
    logging.info("generate ship skin:%s", ship_id)
    ship = Ship(ship_data, ship_json, None, ship_system_id_map)
    ship_id_map[ship.id] = ship
for ship_id, ship_skin_json in ship_skin_dict.items():
    base_ship_id = ship_skin_json["baseHullId"]
    ship_data_result = ship_data_csv.loc[ship_data_csv["id"] == base_ship_id]
    if ship_data_result.empty:
        logging.warning("skin base ship id %s miss ship_data.csv", base_ship_id)
        continue
    ship_data = ship_data_result.iloc[0]
    logging.info("generate ship skin:%s", ship_id)
    ship = Ship(ship_data, ship_dict[base_ship_id], ship_skin_json, ship_system_id_map)
    ship_id_map[ship.id] = ship
# generate page
for ship_system in ship_system_id_map.values():
    md_path = os.path.join(md_ship_systems_dir, ship_system.id) + ".md"
    ship_system.create_md_file(md_path)
ShipSystem.create_list_md_file(ship_system_id_map.values(), work_dir)

for ship in ship_id_map.values():
    md_path = os.path.join(md_hulls_dir, ship.id) + ".md"
    ship.create_md_file(md_path)
Ship.create_list_md_file(ship_id_map.values(), work_dir)
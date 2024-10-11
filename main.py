import logging
import os

import generate_ship
import utils
from config import SS_DIR
from ship import Ship
from ship_mod import ShipMod
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
for _, ship_mod_csv in ship_system_csvs.iterrows():
    ship_mod = ShipSystem(ship_mod_csv)
    ship_system_id_map[ship_mod.id] = ship_mod
ship_system_id_map = dict(
    sorted(ship_system_id_map.items(), key=lambda item: item[1].id)
)
# Ship mod
ship_mod_id_map: dict[str, ShipMod] = {}
for _, ship_mod_csv in hull_mods_csv.iterrows():
    ship_mod = ShipMod(ship_mod_csv)
    ship_mod_id_map[ship_mod.id] = ship_mod
ship_mod_id_map = dict(sorted(ship_mod_id_map.items(), key=lambda item: item[1].id))
# Ship
ship_id_map: dict[str, Ship] = {}
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
ship_id_map = dict(sorted(ship_id_map.items(), key=lambda item: item[1].id))
# generate page
for ship_system in ship_system_id_map.values():
    md_path = os.path.join(md_ship_systems_dir, ship_system.id) + ".md"
    ship_system.create_md_file(md_path, ship_id_map)
ShipSystem.create_list_md_file(ship_system_id_map.values(), work_dir)

for ship_mod in ship_mod_id_map.values():
    md_path = os.path.join(md_hull_mods_dir, ship_mod.id) + ".md"
    ship_mod.create_md_file(md_path)
ShipMod.create_list_md_file(ship_mod_id_map.values(), work_dir)

for ship in ship_id_map.values():
    md_path = os.path.join(md_hulls_dir, ship.id) + ".md"
    ship.create_md_file(md_path)
Ship.create_list_md_file(ship_id_map.values(), work_dir)

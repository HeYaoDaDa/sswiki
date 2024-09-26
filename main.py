import pandas as pd
import os,json,shutil,generate_ship,util,generate_ship_system

def read_hull_files(directory):
    json_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ship'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        key = data.get('hullId', data.get('skinHullId', None))
                        if key is not None:
                            json_dict[key] = data
                        else:
                            print(f"Warning: Neither 'hullId' nor 'skinHullId' found in {file_path}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from {file_path}")
                except Exception as e:
                    print(f"An error occurred while reading {file_path}: {e}")
    return json_dict

def init_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

ss_dir = r"/opt/starsector_097_zh"
work_dir = os.path.dirname(os.path.abspath(__file__))
md_hulls_dir = os.path.join(work_dir,'hulls')
md_ship_systems_dir = os.path.join(work_dir,'shipsystems')
init_folder(md_hulls_dir)
init_folder(md_ship_systems_dir)

descriptions_csv_path = os.path.join(ss_dir,'data/strings/descriptions.csv')
descriptions_csv = pd.read_csv(descriptions_csv_path)
descriptions_csv = descriptions_csv.dropna(subset=['id'])

wing_data_csv_path = os.path.join(ss_dir,'data/hulls/wing_data.csv')
wing_data_csv = pd.read_csv(wing_data_csv_path)
wing_data_csv = wing_data_csv.dropna(subset=['id'])

ship_data_csv_path = os.path.join(ss_dir,'data/hulls/ship_data.csv')
ship_data_csv = pd.read_csv(ship_data_csv_path)
ship_data_csv = ship_data_csv.dropna(subset=['id'])
ship_data_csv = pd.merge(ship_data_csv, descriptions_csv[descriptions_csv['type'] == 'SHIP'], on='id', how='left')

ship_systems_csv_path = os.path.join(ss_dir,'data/shipsystems/ship_systems.csv')
ship_systems_csv = pd.read_csv(ship_systems_csv_path)
ship_systems_csv = ship_systems_csv.dropna(subset=['id'])
ship_systems_csv = pd.merge(ship_systems_csv, descriptions_csv[descriptions_csv['type'] == 'SHIP_SYSTEM'], on='id', how='left')

ship_system_list_map = {}
for _, ship_system in ship_systems_csv.iterrows():
    ship_system_md,ship_system_name = generate_ship_system.generate_ship_system(ship_system)
    
    ship_system_list_map[ship_system["id"]] = ship_system_name

    ship_system_file = os.path.join(md_ship_systems_dir, ship_system["id"])
    with open(ship_system_file+'.md', 'w', encoding='utf-8') as file:
        file.write(ship_system_md)
with open(os.path.join(work_dir,'shipsystems.md'), 'w', encoding='utf-8') as file:
    md = f"# 战术系统\n\n"
    for key,value in ship_system_list_map.items():
        md += f"[{value}](shipsystems/{key}.md)\n"
    file.write(md)

hull_map = read_hull_files(os.path.join(ss_dir,'data/hulls'))
hull_list_map = {}
for _,hull in ship_data_csv.iterrows():
    hull_ship = hull_map.get(hull["id"])
    hull_md,hull_name = generate_ship.generate_ship(hull, hull_ship, ship_systems_csv)
    
    hull_list_map[hull["id"]] = hull_name

    hull_file = os.path.join(md_hulls_dir,hull["id"])
    with open(hull_file+'.md', 'w', encoding='utf-8') as file:
        file.write(hull_md)
with open(os.path.join(work_dir,'hulls.md'), 'w', encoding='utf-8') as file:
    hulls_md = f"# 舰船\n\n"
    for key,value in hull_list_map.items():
        hulls_md += f"[{value}](hulls/{key}.md)\n"
    file.write(hulls_md)

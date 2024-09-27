import json
import logging
import os
import re

import json5
import pandas as pd

import util

slot_size_map = {
    "SMALL": "小型",
    "MEDIUM": "中型",
    "LARGE": "大型",
}

slot_type_map = {
    "BALLISTIC": "实弹",
    "ENERGY": "能量",
    "MISSILE": "导弹",
    "HYBRID": "混合",
    "SYNERGY": "协同",
    "COMPOSITE": "复合",
    "UNIVERSAL": "通用",
}


def read_ship_jsons(hulls_dir):
    ship_dict = {}
    ship_skin_dict = {}
    for root, _, files in os.walk(hulls_dir):
        for file in files:
            if file.endswith(".ship") or file.endswith(".skin"):
                file_path = os.path.join(root, file)
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
                    data = json5.loads(processed_content)
                    hull_id = data.get("hullId")
                    skin_hull_id = data.get("skinHullId")
                    if hull_id is not None:
                        ship_dict[hull_id] = data
                    elif skin_hull_id is not None:
                        ship_skin_dict[skin_hull_id] = data
                    else:
                        logging.warning(
                            "Warning: Neither 'hullId' nor 'skinHullId' found in %s",
                            file_path,
                        )
    return (ship_dict, ship_skin_dict)


def generate_ship(ship_data_csv, ship_json, ship_skin_json, ship_systems_csv):
    is_skin = ship_skin_json is not None

    if is_skin:
        hull_name = ship_skin_json.get("hullName")
    else:
        hull_name = ship_data_csv["name"]
    if pd.isna(hull_name) or len(hull_name) == 0:
        hull_name = ship_json["hullName"]
    if pd.isna(hull_name) or len(hull_name) == 0:
        hull_name = ship_data_csv["id"]

    shield_type = ship_data_csv["shield type"]
    shield_type_html = "无盾"
    if shield_type == "FRONT":
        shield_type_html = "前盾"
    elif shield_type == "OMNI":
        shield_type_html = "全盾"
    elif shield_type == "PHASE":
        shield_type_html = "右键战术系统"

    have_shield = False
    if shield_type == "FRONT" or shield_type == "OMNI":
        have_shield = True

    special_system_id = ship_data_csv["defense id"]

    is_phasecloak = False
    if special_system_id == "phasecloak":
        is_phasecloak = True

    if is_phasecloak:
        field1 = "相位线圈激活"
        field2 = "相位线圈维持(幅能每秒)"
        field3 = ""
    elif have_shield:
        field1 = "护盾角度"
        field2 = "护盾维持(幅能/秒)"
        field3 = "护盾效率(幅能/伤害)"
    else:
        field1 = ""
        field2 = ""
        field3 = ""

    designation = ship_data_csv["designation"]

    hull_description = ""
    if (
        is_skin
        and "descriptionPrefix" in ship_skin_json
        and ship_skin_json["descriptionPrefix"].strip()
    ):
        hull_description += ship_skin_json["descriptionPrefix"] + "\n\n"
    if not pd.isna(ship_data_csv["text1"]):
        hull_description += ship_data_csv["text1"]
    if not pd.isna(ship_data_csv["text2"]):
        hull_description += "\n\n" + ship_data_csv["text2"]
    if not pd.isna(ship_data_csv["text3"]):
        hull_description += "\n\n" + ship_data_csv["text3"]
    if not pd.isna(ship_data_csv["text4"]):
        hull_description += "\n\n" + ship_data_csv["text4"]

    if (
        is_skin
        and "spriteName" in ship_skin_json
        and ship_skin_json["spriteName"].strip()
    ):
        hull_img = f"/{ship_skin_json['spriteName']}"
    else:
        hull_img = f"/{ship_json['spriteName']}"

    supplies_mo = ship_data_csv["supplies/mo"]

    hitpoints = ship_data_csv["hitpoints"]

    cr_day = ship_data_csv["cr %/day"]

    cargo = ship_data_csv["cargo"]

    armor_rating = ship_data_csv["armor rating"]

    cr_to_deploy = ship_data_csv["CR to deploy"]

    max_crew = ship_data_csv["max crew"]

    supplies_rec = ship_data_csv["supplies/rec"]

    min_crew = ship_data_csv["min crew"]

    if is_phasecloak:
        shield_arc = util.my_round(
            ship_data_csv["max flux"] * ship_data_csv["phase cost"]
        )
    elif have_shield:
        shield_arc = ship_data_csv["shield arc"]
    else:
        shield_arc = ""

    peak_cr_sec = ship_data_csv["peak CR sec"]

    fuel = ship_data_csv["fuel"]

    if is_phasecloak:
        shield_upkeep = util.my_round(
            ship_data_csv["max flux"] * ship_data_csv["phase upkeep"]
        )
    elif have_shield:
        shield_upkeep = util.my_round(
            ship_data_csv["flux dissipation"] * ship_data_csv["shield upkeep"]
        )
    else:
        shield_upkeep = ""

    max_burn = ship_data_csv["max burn"]

    shield_efficiency = ""
    if have_shield:
        shield_efficiency = ship_data_csv["shield efficiency"]

    fuel_ly = ship_data_csv["fuel/ly"]

    max_flux = ship_data_csv["max flux"]

    flux_dissipation = ship_data_csv["flux dissipation"]

    ordnance_points = ship_data_csv["ordnance points"]

    fighter_bays = ship_data_csv["fighter bays"]

    reconnaissance_range = ""

    max_speed = ship_data_csv["max speed"]

    system_id = ship_data_csv["system id"]

    detection_range = ""

    if is_skin and "baseValueMult" in ship_skin_json:
        base_value = util.my_round(
            ship_data_csv["base value"] * ship_skin_json["baseValueMult"]
        )
    else:
        base_value = ship_data_csv["base value"]

    system_name = ""
    special_system_name = ""
    system_description = ""
    special_system_description = ""
    if not pd.isna(system_id):
        system_name = ship_systems_csv.loc[
            ship_systems_csv["id"] == system_id, "name"
        ].iloc[0]
        system_description = ship_systems_csv.loc[
            ship_systems_csv["id"] == system_id, "text3"
        ].iloc[0]

    if not pd.isna(special_system_id):
        special_system_name = ship_systems_csv.loc[
            ship_systems_csv["id"] == special_system_id, "name"
        ].iloc[0]
        special_system_description = ship_systems_csv.loc[
            ship_systems_csv["id"] == special_system_id, "text3"
        ].iloc[0]

    weapon_slot_map = {}
    if ship_json.get("weaponSlots") is not None:
        for weapon_slot in ship_json["weaponSlots"]:
            if weapon_slot["type"] in [
                "BALLISTIC",
                "ENERGY",
                "MISSILE",
                "HYBRID",
                "SYNERGY",
                "COMPOSITE",
                "UNIVERSAL",
            ]:
                weapon_map = weapon_slot_map.get(weapon_slot["type"])
                if weapon_map is None:
                    weapon_map = {}
                num = weapon_map.get(weapon_slot["size"])
                if num is None:
                    weapon_map[weapon_slot["size"]] = 1
                else:
                    weapon_map[weapon_slot["size"]] = num + 1
                weapon_slot_map[weapon_slot["type"]] = weapon_map

    installation_slot = ""
    if len(weapon_slot_map) > 0:
        installation_slot_list = []
        for slot_type, slot_map in weapon_slot_map.items():
            for size, num in slot_map.items():
                installation_slot_list.append(
                    f"{num}x {slot_size_map[size]}{slot_type_map[slot_type]}"
                )
        installation_slot = ", ".join(installation_slot_list)
    if not pd.isna(fighter_bays) and fighter_bays > 0:
        installation_slot += f", {round(fighter_bays)}x 飞行甲板"

    armament_details = ""

    hull_slot = ""

    json_str = json.dumps(ship_json, indent=4)

    result = f"""# {hull_name}-级 {designation}

## 描述

<table class="table table-bordered" data-toggle="table" data-show-header="false"><thead style="display:none"><tr><th style="width:75%;text-align:left;vertical-align:top;">title</th><th style="width:25%;text-align:center;vertical-align:middle;"></th></tr></thead><tr><td style="width:75%;text-align:left;vertical-align:top;">{hull_description}</td><td style="width:25%;text-align:center;vertical-align:middle;"><img decoding="async" src="{hull_img}"></td></tr></tbody></table>

## 详细信息

<table style="table table-bordered"><colgroup><col style="width: 21%"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"></colgroup><thead><tr><th colspan="4"style="text-align:center;">后勤数据</th><th colspan="2"style="text-align:center;">战斗性能</th></tr></thead><tbody><tr><td>作战后消耗的战备值(CR)</td><td style="text-align:right;">{cr_to_deploy}%</td><td>维护消耗(补给/月)</td><td style="text-align:right;">{supplies_mo}</td><td>结构值</td><td style="text-align:right;">{hitpoints}</td></tr><tr><td>战备值(CR)恢复速率(每天)</td><td style="text-align:right;">{cr_day}</td><td>载货量</td><td style="text-align:right;">{cargo}</td><td>装甲值</td><td style="text-align:right;">{armor_rating}</td></tr><tr><td>部署成本(补给)</td><td style="text-align:right;">{supplies_rec}</td><td>最大载员</td><td style="text-align:right;">{max_crew}</td><td>防御方式</td><td style="text-align:right;">{shield_type_html}</td></tr><tr><td>部署点</td><td style="text-align:right;">{supplies_rec}</td><td>必要船员</td><td style="text-align:right;">{min_crew}</td><td>{field1}</td><td style="text-align:right;">{shield_arc}</td></tr><tr><td>峰值时间(秒)</td><td style="text-align:right;">{peak_cr_sec}</td><td>燃料容量</td><td style="text-align:right;">{fuel}</td><td>{field2}</td><td style="text-align:right;">{shield_upkeep}</td></tr><tr><td></td><td style="text-align:right;"></td><td>最大宇宙航速</td><td style="text-align:right;">{max_burn}</td><td>{field3}</td><td style="text-align:right;">{shield_efficiency}</td></tr><tr><td></td><td style="text-align:right;"></td><td>燃料消耗(光年)</td><td style="text-align:right;">{fuel_ly}</td><td>幅能容量</td><td style="text-align:right;">{max_flux}</td></tr><tr><td></td><td style="text-align:right;"></td><td></td><td style="text-align:right;"></td><td>幅能耗散</td><td style="text-align:right;">{flux_dissipation}</td></tr><tr><td>装配点数</td><td style="text-align:right;">{ordnance_points}</td><td>被侦察范围</td><td style="text-align:right;">{reconnaissance_range}</td><td>最高航速</td><td style="text-align:right;">{max_speed}</td></tr><tr><td>战术系统</td><td style="text-align:right;">[{system_name}](/shipsystems/{system_id}.md)</td><td>探测范围</td><td style="text-align:right;">{detection_range}</td><td></td><td style="text-align:right;"></td></tr><tr><td></td><td colspan="5">{system_description}</td></tr><tr><td>特殊系统</td><td colspan="5">[{special_system_name}](/shipsystems/{special_system_id}.md)</td></tr><tr><td></td><td colspan="5">{special_system_description}</td></tr><tr><td>安装槽位:</td><td colspan="5">{installation_slot}</td></tr><tr><td>军备详情:</td><td colspan="5">{armament_details}</td></tr><tr><td>船体插槽:</td><td colspan="5">{hull_slot}</td></tr></tbody></table>

## 其他字段信息

<details><summary>点击展开/折叠</summary><table style="table table-bordered"><colgroup><col style="width: 21%"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"></colgroup><thead style="display:none"><tr><th>title</th><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td>ID</td><td style="text-align:right;">{ship_data_csv["id"]}</td><td>科技类型</td><td style="text-align:right;">{ship_data_csv["tech/manufacturer"]}</td><td>自动分</td><td style="text-align:right;">{ship_data_csv["fleet pts"]}</td></tr><tr><td>加速度(机动性的一部分)</td><td style="text-align:right;">{ship_data_csv["acceleration"]}</td><td>减速度(机动性的一部分)</td><td style="text-align:right;">{ship_data_csv["deceleration"]}</td><td>最大转弯速度(机动性的一部分)</td><td style="text-align:right;">{ship_data_csv["max turn rate"]}</td></tr><tr><td>转弯加速度(机动性的一部分)</td><td style="text-align:right;">{ship_data_csv["turn acceleration"]}</td><td>质量</td><td style="text-align:right;">{ship_data_csv["mass"]}</td><td>range</td><td style="text-align:right;">{ship_data_csv["range"]}</td></tr><tr><td>成本价</td><td style="text-align:right;">{base_value}</td><td>峰值时间耗尽后CR消耗(每秒)</td><td style="text-align:right;">{ship_data_csv["CR loss/sec"]}</td><td>c/s</td><td style="text-align:right;">{ship_data_csv["c/s"]}</td></tr><tr><td>c/f</td><td style="text-align:right;">{ship_data_csv["c/f"]}</td><td>f/s</td><td style="text-align:right;">{ship_data_csv["f/s"]}</td><td>f/f</td><td style="text-align:right;">{ship_data_csv["f/f"]}</td></tr><tr><td>crew/s</td><td style="text-align:right;">{ship_data_csv["crew/s"]}</td><td>crew/f</td><td style="text-align:right;">{ship_data_csv["crew/f"]}</td><td>hints</td><td style="text-align:right;">{ship_data_csv["hints"]}</td></tr><tr><td>Tags</td><td style="text-align:right;">{ship_data_csv["tags"]}</td><td>稀有度(数字越小越罕见)</td><td style="text-align:right;">{ship_data_csv["rarity"]}</td><td>炸碎概率</td><td style="text-align:right;">{ship_data_csv["breakProb"]}</td></tr><tr><td>最少碎片数</td><td style="text-align:right;">{ship_data_csv["minPieces"]}</td><td>最多碎片数</td><td style="text-align:right;">{ship_data_csv["maxPieces"]}</td><td>进场与出场时使用的战术系统</td><td style="text-align:right;">{ship_data_csv["travel drive"]}</td></tr><tr><td>飞行甲板数量</td><td style="text-align:right;">{fighter_bays}</td><td>number</td><td style="text-align:right;">{ship_data_csv["number"]}</td><td></td><td style="text-align:right;"></td></tr></tbody></table></details>

## Ship文件信息

<details><summary>点击展开/折叠</summary><pre style="background-color:#272b30;color:#c8c8c8;"><code>{json_str}</code></pre></details>
"""
    return (result, hull_name)

import os

import pandas as pd

import constants
import page_utils
import utils
from ship_system import ShipSystem


class Ship:

    def __init__(
        self,
        ship_data_csv,
        ship_json,
        ship_skin_json,
        ship_system_id_map: dict[str, ShipSystem],
    ) -> None:
        self.is_skin = ship_skin_json is not None
        # id
        self.id = ship_data_csv["id"]
        if self.is_skin:
            self.id = ship_skin_json["skinHullId"]
        else:
            self.id = ship_data_csv["id"]
        # name
        if self.is_skin:
            self.name = ship_skin_json.get("hullName")
        else:
            self.name = ship_data_csv["name"]
        if utils.is_empty(self.name):
            self.name = ship_json["hullName"]
        if utils.is_empty(self.name):
            self.name = self.id

        self.size = ship_json["hullSize"]
        self.shield_type = ship_data_csv["shield type"]
        self.shield_type_str = "无盾"
        if self.shield_type == "FRONT":
            self.shield_type_str = "前盾"
        elif self.shield_type == "OMNI":
            self.shield_type_str = "全盾"
        elif self.shield_type == "PHASE":
            self.shield_type_str = "右键战术系统"

        self.have_shield = False
        if self.shield_type == "FRONT" or self.shield_type == "OMNI":
            self.have_shield = True

        self.special_system_id = ship_data_csv["defense id"]

        self.is_phasecloak = False
        if self.special_system_id == "phasecloak":
            self.is_phasecloak = True

        if self.is_phasecloak:
            self.field1 = "相位线圈激活"
            self.field2 = "相位线圈维持(幅能每秒)"
            self.field3 = ""
        elif self.have_shield:
            self.field1 = "护盾角度"
            self.field2 = "护盾维持(幅能/秒)"
            self.field3 = "护盾效率(幅能/伤害)"
        else:
            self.field1 = ""
            self.field2 = ""
            self.field3 = ""

        self.designation = ship_data_csv["designation"]

        self.description = utils.get_description(ship_data_csv)
        if (
            self.is_skin
            and "descriptionPrefix" in ship_skin_json
            and ship_skin_json["descriptionPrefix"].strip()
        ):
            self.description = (
                ship_skin_json["descriptionPrefix"] + "\n" + self.description
            )

        if (
            self.is_skin
            and "spriteName" in ship_skin_json
            and ship_skin_json["spriteName"].strip()
        ):
            self.img = utils.get_img(ship_skin_json["spriteName"])
        else:
            self.img = utils.get_img(ship_json["spriteName"])

        self.supplies_mo = utils.get_str(ship_data_csv["supplies/mo"])
        self.hitpoints = utils.get_str(ship_data_csv["hitpoints"])
        self.cr_day = utils.get_str(ship_data_csv["cr %/day"])
        self.cargo = utils.get_str(ship_data_csv["cargo"])
        self.armor_rating = utils.get_str(ship_data_csv["armor rating"])
        self.cr_to_deploy = utils.get_str(ship_data_csv["CR to deploy"])
        self.max_crew = utils.get_str(ship_data_csv["max crew"])
        self.supplies_rec = utils.get_str(ship_data_csv["supplies/rec"])
        self.min_crew = utils.get_str(ship_data_csv["min crew"])

        if self.is_phasecloak:
            self.shield_arc = utils.my_round(
                ship_data_csv["max flux"] * ship_data_csv["phase cost"]
            )
        elif self.have_shield:
            self.shield_arc = ship_data_csv["shield arc"]
        else:
            self.shield_arc = ""

        if self.is_phasecloak:
            self.shield_upkeep = utils.my_round(
                ship_data_csv["max flux"] * ship_data_csv["phase upkeep"]
            )
        elif self.have_shield:
            self.shield_upkeep = utils.my_round(
                ship_data_csv["flux dissipation"] * ship_data_csv["shield upkeep"]
            )
        else:
            self.shield_upkeep = ""

        self.peak_cr_sec = utils.get_str(ship_data_csv["peak CR sec"])
        self.fuel = utils.get_str(ship_data_csv["fuel"])
        self.max_burn = utils.get_str(ship_data_csv["max burn"])

        self.shield_efficiency = ""
        if self.have_shield:
            self.shield_efficiency = ship_data_csv["shield efficiency"]

        self.fuel_ly = ship_data_csv["fuel/ly"]

        self.max_flux = ship_data_csv["max flux"]

        self.flux_dissipation = ship_data_csv["flux dissipation"]

        self.ordnance_points = ship_data_csv["ordnance points"]

        self.fighter_bays = ship_data_csv["fighter bays"]

        self.reconnaissance_range = ""

        self.max_speed = ship_data_csv["max speed"]

        self.system_id = ship_data_csv["system id"]

        self.detection_range = ""

        if self.is_skin and "baseValueMult" in ship_skin_json:
            self.base_value = utils.my_round(
                ship_data_csv["base value"] * ship_skin_json["baseValueMult"]
            )
        else:
            self.base_value = ship_data_csv["base value"]

        self.system_name = ""
        self.special_system_name = ""
        self.system_description = ""
        self.special_system_description = ""

        if not pd.isna(self.system_id):
            self.system_name = ship_system_id_map[self.system_id].name
            self.system_description = ship_system_id_map[
                self.system_id
            ].short_description
            ship_system_id_map[self.system_id].ships.add(ship_data_csv["id"])

        if not pd.isna(self.special_system_id):
            self.special_system_name = ship_system_id_map[self.special_system_id].name
            self.special_system_description = ship_system_id_map[
                self.special_system_id
            ].short_description
            ship_system_id_map[self.special_system_id].special_ships.add(
                ship_data_csv["id"]
            )

        self.weapon_slot_map = {}
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
                    weapon_map = self.weapon_slot_map.get(weapon_slot["type"])
                    if weapon_map is None:
                        weapon_map = {}
                    num = weapon_map.get(weapon_slot["size"])
                    if num is None:
                        weapon_map[weapon_slot["size"]] = 1
                    else:
                        weapon_map[weapon_slot["size"]] = num + 1
                    self.weapon_slot_map[weapon_slot["type"]] = weapon_map

        self.installation_slot = ""
        if len(self.weapon_slot_map) > 0:
            self.installation_slot_list = []
            for slot_type, slot_map in self.weapon_slot_map.items():
                for size, num in slot_map.items():
                    self.installation_slot_list.append(
                        f"{num}x {constants.SLOT_SIZE_MAP[size]}{constants.SLOT_TYPE_MAP[slot_type]}"
                    )
            self.installation_slot = ", ".join(self.installation_slot_list)
        if not pd.isna(self.fighter_bays) and self.fighter_bays > 0:
            self.installation_slot += f", {round(self.fighter_bays)}x 飞行甲板"

        self.armament_details = ""
        self.hull_slot = ""

    def create_md_file(self, md_path: str) -> None:
        md = self.__generate_md()
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(md)

    @staticmethod
    def create_list_md_file(ships, work_dir: str) -> None:
        ships = list(ships)
        ships.sort(key=lambda ship: ship.id)
        ship_list_md = "# 舰船 原始数据\n"
        ship_list_md += "\n"
        for size, size_str in constants.HULL_SIZE_MAP.items():
            ships1 = [
                (ship.name, ship.img, f"/hulls/{ship.id}.md")
                for ship in ships
                if ship.size == size
            ]
            if len(ships1) > 0:
                ship_list_md += f"## {size_str}\n"
                ship_list_md += "\n"
                ship_list_md += page_utils.generate_list_md(ships1, 200)
                ship_list_md += "\n"
        with open(os.path.join(work_dir, "hulls.md"), "w", encoding="utf-8") as file:
            file.write(ship_list_md)

    def __generate_md(self) -> str:
        result = ""
        result += f"# {self.name}-级 {self.designation}\n"
        result += "\n"
        result += page_utils.generate_description(self.description, self.img)
        result += "\n"
        result += generate_detail_info(self)
        result += "\n"
        result += page_utils.generate_other_info({})
        return result


def generate_detail_info(ship: Ship) -> str:
    return f"""## 详细信息

<table><colgroup><col style="width: 21%;"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"></colgroup><thead><tr><th colspan="4"style="text-align:center;">后勤数据</th><th colspan="2"style="text-align:center;">战斗性能</th></tr></thead><tbody><tr><td>作战后消耗的战备值(CR)</td><td style="text-align:right;">{ship.cr_to_deploy}%</td><td>维护消耗(补给/月)</td><td style="text-align:right;">{ship.supplies_mo}</td><td>结构值</td><td style="text-align:right;">{ship.hitpoints}</td></tr><tr><td>战备值(CR)恢复速率(每天)</td><td style="text-align:right;">{ship.cr_day}</td><td>载货量</td><td style="text-align:right;">{ship.cargo}</td><td>装甲值</td><td style="text-align:right;">{ship.armor_rating}</td></tr><tr><td>部署成本(补给)</td><td style="text-align:right;">{ship.supplies_rec}</td><td>最大载员</td><td style="text-align:right;">{ship.max_crew}</td><td>防御方式</td><td style="text-align:right;">{ship.shield_type_str}</td></tr><tr><td>部署点</td><td style="text-align:right;">{ship.supplies_rec}</td><td>必要船员</td><td style="text-align:right;">{ship.min_crew}</td><td>{ship.field1}</td><td style="text-align:right;">{ship.shield_arc}</td></tr><tr><td>峰值时间(秒)</td><td style="text-align:right;">{ship.peak_cr_sec}</td><td>燃料容量</td><td style="text-align:right;">{ship.fuel}</td><td>{ship.field2}</td><td style="text-align:right;">{ship.shield_upkeep}</td></tr><tr><td></td><td style="text-align:right;"></td><td>最大宇宙航速</td><td style="text-align:right;">{ship.max_burn}</td><td>{ship.field3}</td><td style="text-align:right;">{ship.shield_efficiency}</td></tr><tr><td></td><td style="text-align:right;"></td><td>燃料消耗(光年)</td><td style="text-align:right;">{ship.fuel_ly}</td><td>幅能容量</td><td style="text-align:right;">{ship.max_flux}</td></tr><tr><td></td><td style="text-align:right;"></td><td></td><td style="text-align:right;"></td><td>幅能耗散</td><td style="text-align:right;">{ship.flux_dissipation}</td></tr><tr><td>装配点数</td><td style="text-align:right;">{ship.ordnance_points}</td><td>被侦察范围</td><td style="text-align:right;">{ship.reconnaissance_range}</td><td>最高航速</td><td style="text-align:right;">{ship.max_speed}</td></tr><tr><td>战术系统</td><td style="text-align:right;">[{ship.system_name}](/shipsystems/{ship.system_id}.md)</td><td>探测范围</td><td style="text-align:right;">{ship.detection_range}</td><td></td><td style="text-align:right;"></td></tr><tr><td></td><td colspan="5">{ship.system_description}</td></tr><tr><td>特殊系统</td><td colspan="5">[{ship.special_system_name}](/shipsystems/{ship.special_system_id}.md)</td></tr><tr><td></td><td colspan="5">{ship.special_system_description}</td></tr><tr><td>安装槽位:</td><td colspan="5">{ship.installation_slot}</td></tr><tr><td>军备详情:</td><td colspan="5">{ship.armament_details}</td></tr><tr><td>船体插槽:</td><td colspan="5">{ship.hull_slot}</td></tr></tbody></table>
"""

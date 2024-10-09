import os

import pandas as pd

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
                        f"{num}x {slot_size_map[size]}{slot_type_map[slot_type]}"
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
    def create_list_md_file(ship_systemd, work_dir: str) -> None:
        ship_system_list_md = "# 战术系统\n"
        ship_system_list_md += "\n"
        ship_system_list_md += (
            """<div style="text-align:left;min-width:200px;min-height:0px;">"""
        )
        for ship_system in ship_systemd:
            ship_system_list_md += ship_system.__generate_list_item()
        ship_system_list_md += "</div>"
        with open(
            os.path.join(work_dir, "hulls.md"), "w", encoding="utf-8"
        ) as file:
            file.write(ship_system_list_md)

    def __generate_list_item(self) -> str:
        md_path = f"hulls/{self.id}.md"
        return f"""<div style="display:inline-block;text-align:center;min-width:150px;min-height:0px;padding-bottom: 15px;"><div style="text-align:center;">[<div style="display:inline-block;text-align:center"><img decoding="async"src="{self.img}"href="{md_path}"style="max-width:200px;max-height:200px;"/></div><br/>[{self.name}](hulls/{self.id}.md)]({md_path})</div></div>"""

    def __generate_md(self) -> str:
        result = ""
        result += f"# {self.name}-级 {self.designation}\n"
        result += "\n"
        result += page_utils.generate_description(self.description, self.img)
        result += "\n"
        result += page_utils.generate_other_info({})
        return result


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

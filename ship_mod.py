import os
from typing import Any

import pandas as pd

import constants
import page_utils
import utils


class ShipMod:
    def __init__(self, ship_mod_csv: pd.Series) -> None:
        self.id = ship_mod_csv["id"]
        self.name = ship_mod_csv["name"]
        self.ships = []

        self.desc = ship_mod_csv["desc"]
        self.short = ship_mod_csv["short"]
        self.sModDesc = ship_mod_csv["sModDesc"]
        self.description = ""
        if not pd.isna(self.desc) and self.desc:
            self.description += self.desc
        if not pd.isna(self.short) and self.short:
            self.description += "\n" + self.short
        if not pd.isna(self.sModDesc) and self.sModDesc:
            self.description += "\n" + self.sModDesc

        self.img = utils.get_img(ship_mod_csv["sprite"])
        self.tier = ship_mod_csv["tier"]
        self.rarity = ship_mod_csv["rarity"]
        self.tech_manufacturer = ship_mod_csv["tech/manufacturer"]
        self.tags = ship_mod_csv["tags"]
        if not utils.is_empty(ship_mod_csv["uiTags"]):
            self.uiTags = ship_mod_csv["uiTags"].split(", ")
        else:
            self.uiTags = ["无类型"]
        self.base_value = ship_mod_csv["base value"]
        self.unlocked = ship_mod_csv["unlocked"]
        self.hidden = ship_mod_csv["hidden"]
        self.hiddenEverywhere = ship_mod_csv["hiddenEverywhere"]
        self.cost_frigate = ship_mod_csv["cost_frigate"]
        self.cost_dest = ship_mod_csv["cost_dest"]
        self.cost_cruiser = ship_mod_csv["cost_cruiser"]
        self.cost_capital = ship_mod_csv["cost_capital"]
        self.script = ship_mod_csv["script"]

    def create_md_file(self, md_path: str, ship_id_map: dict[str, Any]) -> None:
        md = self.__generate_md(ship_id_map)
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(md)

    @staticmethod
    def create_list_md_file(ship_mods, work_dir: str) -> None:
        uitag_set = set()
        for ship_mod in ship_mods:
            for uitag in ship_mod.uiTags:
                uitag_set.add(uitag)
        ship_mod_list_md = "# 舰船插件\n"
        ship_mod_list_md += "\n"
        ship_mod_list_md += """<script>$(document).ready(function(){$('input[type="radio"]').change(function(){var filter=$(this).val();if(filter==='all'){$('.filter').show()}else{$('.filter').hide();$('.filter.'+filter).show()}});$('input[type="radio"][value="all"]').prop('checked',true);$('.filter').show()});</script>\n"""
        ship_mod_list_md += "\n"
        ship_mod_list_md += "<div>"
        ship_mod_list_md += """<div style="display:inline-block;padding:5px"><input type="radio"id="all"name="uitag"value="all"><label for="all">全部</label></div>"""
        for uitag in sorted(uitag_set):
            ship_mod_list_md += f"""<div style="display:inline-block;padding:5px"><input type="radio"id="{uitag}"name="uitag"value="{uitag}"><label for="{uitag}">{uitag}</label></div>"""
        ship_mod_list_md += "</div>\n"
        ship_mod_list_md += "\n"
        ship_mod_list_md += page_utils.generate_list_md(
            [
                (
                    ship_mod.name,
                    ship_mod.img,
                    f"/hullmods/{ship_mod.id}.md",
                    "filter " + " ".join(ship_mod.uiTags),
                )
                for ship_mod in ship_mods
            ],
            32,
        )
        with open(os.path.join(work_dir, "hullmods.md"), "w", encoding="utf-8") as file:
            file.write(ship_mod_list_md)

    def __generate_md(self, ship_id_map: dict[str, Any]) -> str:
        result = ""
        result += f"# {self.name}\n"
        result += "\n"
        result += page_utils.generate_description(self.description, self.img)
        result += "\n"
        if len(self.ships) > 0:
            result += generate_ships_list("被内置于", set(self.ships), ship_id_map)
        return result


def generate_ships_list(
    title: str, ship_ids: set[str], ship_id_map: dict[str, Any]
) -> str:
    ship_list_md = f"## {title}\n"
    ship_list_md += "\n"
    ships = [ship_id_map[id] for id in ship_ids if id in ship_id_map]
    for size, size_str in constants.HULL_SIZE_MAP.items():
        ships1 = [
            (ship.name, ship.img, f"/hulls/{ship.id}.md", "")
            for ship in ships
            if ship.size == size
        ]
        if len(ships1) > 0:
            ship_list_md += f"### {size_str}\n"
            ship_list_md += "\n"
            ship_list_md += page_utils.generate_list_md(ships1, 200)
            ship_list_md += "\n"
    return ship_list_md

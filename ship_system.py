import os
from typing import Any

import pandas as pd

import constants
import page_utils
import utils


class ShipSystem:
    def __init__(self, csv: pd.Series) -> None:
        self.id = csv["id"]
        self.name = csv["name"]
        self.description = utils.get_description(csv)
        self.short_description = utils.get_str(csv["text3"])
        self.flux_second = utils.get_str(csv["flux/second"])
        self.flux_second_rate = utils.get_str(csv["f/s (base rate)"])
        self.flux_second_cap = utils.get_str(csv["f/s (base cap)"])
        self.flux_use = utils.get_str(csv["flux/use"])
        self.flux_use_rate = utils.get_str(csv["f/u (base rate)"])
        self.flux_use_cap = utils.get_str(csv["f/u (base cap)"])
        self.cr_u = utils.get_str(csv["cr/u"])
        self.max_uses = csv["max uses"]
        if utils.is_empty(self.max_uses):
            self.max_uses = "无限"
        self.regen = utils.get_str(csv["regen"])
        self.charge_up = utils.get_str(csv["charge up"])
        self.active = utils.get_str(csv["active"])
        self.down = utils.get_str(csv["down"])
        self.cooldown = utils.get_str(csv["cooldown"])
        self.toggle = utils.get_bool(csv["toggle"])
        self.noDissipation = utils.get_bool(csv["noDissipation"])
        self.noHardDissipation = utils.get_bool(csv["noHardDissipation"])
        self.hardFlux = utils.get_bool(csv["hardFlux"])
        self.noFiring = utils.get_bool(csv["noFiring"])
        self.noTurning = utils.get_bool(csv["noTurning"])
        self.noStrafing = utils.get_bool(csv["noStrafing"])
        self.noAccel = utils.get_bool(csv["noAccel"])
        self.noShield = utils.get_bool(csv["noShield"])
        self.noVent = utils.get_bool(csv["noVent"])
        self.isPhaseCloak = utils.get_bool(csv["isPhaseCloak"])
        self.tags = utils.get_str(csv["tags"])
        self.img = utils.get_img(csv["icon"])
        self.ships = set()
        self.special_ships = set()

    def create_md_file(self, md_path: str, ship_id_map: dict[str, Any]) -> None:
        md = self.__generate_md(ship_id_map)
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(md)

    @staticmethod
    def create_list_md_file(ship_systems, work_dir: str) -> None:
        ship_system_list_md = "# 战术系统\n"
        ship_system_list_md += "\n"
        ship_system_list_md += page_utils.generate_list_md(
            [
                (ship_system.name, ship_system.img, f"/shipsystems/{ship_system.id}.md", "")
                for ship_system in ship_systems
            ],
            50,
        )
        with open(
            os.path.join(work_dir, "shipsystems.md"), "w", encoding="utf-8"
        ) as file:
            file.write(ship_system_list_md)

    def __generate_md(self, ship_id_map: dict[str, Any]) -> str:
        result = ""
        result += f"# {self.name}\n"
        result += "\n"
        result += page_utils.generate_description(self.description, self.img)
        result += "\n"
        result += page_utils.generate_other_info(
            {
                "ID": self.id,
                "系统维持(幅能/秒)": self.flux_second,
                "系统维持(幅能耗散比率/秒)": self.flux_second_rate,
                "系统维持(幅能容量比率/秒)": self.flux_second_cap,
                "激活消耗(幅能)": self.flux_use,
                "激活消耗(幅能耗散比率)": self.flux_use_rate,
                "激活消耗(幅能容量比率)": self.flux_use_cap,
                "激活消耗(CR)": self.cr_u,
                "充能次数": self.max_uses,
                "恢复速率(次/秒)": self.regen,
                "前摇时长": self.charge_up,
                "全功率激活时长": self.active,
                "后摇时长": self.down,
                "冷却时长": self.cooldown,
                "开关式的": self.toggle,
                "无法耗散幅能": self.noDissipation,
                "无法耗散硬幅能": self.noHardDissipation,
                "系统产生的幅能为硬幅能": self.hardFlux,
                "无法开火": self.noFiring,
                "无法转向": self.noTurning,
                "无法左右平移": self.noStrafing,
                "无法向前加速": self.noAccel,
                "法启动护盾或右键战术系统": self.noShield,
                "无法按V排散": self.noVent,
                "战术系统被认为是一种相位": self.isPhaseCloak,
                "Tags": self.tags,
            }
        )
        result += "\n"
        if len(self.ships) > 0:
            result += generate_ships_list("被用于战术系统", self.ships, ship_id_map)
            result += "\n"
        if len(self.special_ships) > 0:
            result += generate_ships_list(
                "被用于特殊系统", self.special_ships, ship_id_map
            )
            result += "\n"
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

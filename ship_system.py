import os

import pandas as pd

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

    def create_md_file(self, md_path: str) -> None:
        md = self.__generate_md()
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(md)

    @staticmethod
    def create_list_md_file(ship_systemd, work_dir: str) -> None:
        ship_system_list_md = "# 战术系统\n"
        ship_system_list_md += "\n"
        ship_system_list_md += (
            """<div style="text-align:left;min-width:150px;min-height:0px;">"""
        )
        for ship_system in ship_systemd:
            ship_system_list_md += ship_system.__generate_list_item()
        ship_system_list_md += "</div>"
        with open(
            os.path.join(work_dir, "shipsystems.md"), "w", encoding="utf-8"
        ) as file:
            file.write(ship_system_list_md)

    def __generate_list_item(self) -> str:
        md_path = f"shipsystems/{self.id}.md"
        return f"""<div style="display:inline-block;text-align:center;min-width:150px;min-height:0px;padding-bottom: 15px;"><div style="text-align:center;">[<div style="width:50px;display:inline-block;text-align:center"><img decoding="async"src="{self.img}"href="{md_path}"style="max-width:50px;max-height:50px;"/></div><br/>[{self.name}](shipsystems/{self.id}.md)]({md_path})</div></div>"""

    def __generate_md(self) -> str:
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
        return result

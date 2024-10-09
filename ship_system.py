import json

import pandas as pd

import utils


class ShipSystem:
    def __init__(self, csv: pd.Series) -> None:
        self.id = csv["id"]
        self.name = csv["name"]
        self.description = utils.get_description(csv)
        self.short_description = csv["text3"]
        self.flux_second = csv["flux/second"]
        self.flux_second_rate = csv["f/s (base rate)"]
        self.flux_second_cap = csv["f/s (base cap)"]
        self.flux_use = csv["flux/use"]
        self.flux_use_rate = csv["f/u (base rate)"]
        self.flux_use_cap = csv["f/u (base cap)"]
        self.cr_u = csv["cr/u"]
        self.max_uses = csv["max uses"]
        if utils.is_empty(self.max_uses):
            self.max_uses = "无限"
        self.regen = csv["regen"]
        self.charge_up = csv["charge up"]
        self.active = csv["active"]
        self.down = csv["down"]
        self.cooldown = csv["cooldown"]
        self.toggle = csv["toggle"]
        self.noDissipation = csv["noDissipation"]
        self.noHardDissipation = csv["noHardDissipation"]
        self.hardFlux = csv["hardFlux"]
        self.noFiring = csv["noFiring"]
        self.noTurning = csv["noTurning"]
        self.noStrafing = csv["noStrafing"]
        self.noAccel = csv["noAccel"]
        self.noShield = csv["noShield"]
        self.noVent = csv["noVent"]
        self.isPhaseCloak = csv["isPhaseCloak"]
        self.tags = utils.split_tags(csv["tags"])
        self.img = utils.get_img(csv["icon"])
        self.ships = set()
        self.special_ships = set()

    def create_md_file(self, md_path: str) -> None:
        md = self.__generate_md()
        with open(md_path, "w", encoding="utf-8") as file:
            file.write(md)

    def generate_list_item(self) -> str:
        return f"[{self.name}](shipsystems/{self.id}.md)\n"

    def __generate_md(self) -> str:
        result = ""
        result += f"# {self.name}\n"
        result += "\n"
        result += f"""```json
{json.dumps(list(self.ships), indent=4)}
```

```json
{json.dumps(list(self.special_ships), indent=4)}
```"""
        return result

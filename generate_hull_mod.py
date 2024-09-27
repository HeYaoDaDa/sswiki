import pandas as pd


def generate_hull_mod(hull_mod_csv):
    name = hull_mod_csv["name"]

    desc = hull_mod_csv["desc"]
    short = hull_mod_csv["short"]
    sModDesc = hull_mod_csv["sModDesc"]

    description = ''
    if not pd.isna(desc) and desc:
        description += desc
    if not pd.isna(short) and short:
        description += '\n\n' + short
    if not pd.isna(sModDesc) and sModDesc:
        description += '\n\n' + sModDesc

    sprite = f"/{hull_mod_csv["sprite"]}"

    tier = hull_mod_csv["tier"]
    rarity = hull_mod_csv["rarity"]
    tech_manufacturer = hull_mod_csv["tech/manufacturer"]
    tags = hull_mod_csv["tags"]
    uiTags = hull_mod_csv["uiTags"]
    base_value = hull_mod_csv["base value"]
    unlocked = hull_mod_csv["unlocked"]
    hidden = hull_mod_csv["hidden"]
    hiddenEverywhere = hull_mod_csv["hiddenEverywhere"]
    cost_frigate = hull_mod_csv["cost_frigate"]
    cost_dest = hull_mod_csv["cost_dest"]
    cost_cruiser = hull_mod_csv["cost_cruiser"]
    cost_capital = hull_mod_csv["cost_capital"]
    script = hull_mod_csv["script"]

    result = f"""# {name}

## 描述

<table class="table table-bordered" data-toggle="table" data-show-header="false"><thead style="display:none"><tr><th style="width:75%;text-align:left;vertical-align:top;">title</th><th style="width:25%;text-align:center;vertical-align:middle;"></th></tr></thead><tr><td style="width:75%;text-align:left;vertical-align:top;">{description}</td><td style="width:25%;text-align:center;vertical-align:middle;"><img decoding="async" src="{sprite}"></td></tr></tbody></table>

## 详细信息

"""
    return (result, name)

import pandas as pd

def generate_ship_system(ship_systems_csv):
    name = ship_systems_csv["name"]

    description = ''
    if not pd.isna(ship_systems_csv["text1"]):
        description += ship_systems_csv["text1"]
    if not pd.isna(ship_systems_csv["text2"]):
        description += '\n'+ship_systems_csv["text2"]
    if not pd.isna(ship_systems_csv["text3"]):
        description += '\n'+ship_systems_csv["text3"]
    if not pd.isna(ship_systems_csv["text4"]):
        description += '\n'+ship_systems_csv["text4"]

    flux_second = ship_systems_csv["flux/second"]

    flux_second_rate = ship_systems_csv["f/s (base rate)"]

    flux_second_cap = ship_systems_csv["f/s (base cap)"]

    flux_use = ship_systems_csv["flux/use"]

    flux_use_rate = ship_systems_csv["f/u (base rate)"]

    flux_use_cap = ship_systems_csv["f/u (base cap)"]

    cr_u = ship_systems_csv["cr/u"]

    max_uses = ship_systems_csv["max uses"]
    if pd.isna(max_uses):
        max_uses = '无限'

    regen = ship_systems_csv["regen"]

    charge_up = ship_systems_csv["charge up"]

    active = ship_systems_csv["active"]

    down = ship_systems_csv["down"]

    cooldown = ship_systems_csv["cooldown"]

    toggle = ship_systems_csv["toggle"]

    noDissipation = ship_systems_csv["noDissipation"]

    noHardDissipation = ship_systems_csv["noHardDissipation"]

    hardFlux = ship_systems_csv["hardFlux"]

    noFiring = ship_systems_csv["noFiring"]

    noTurning = ship_systems_csv["noTurning"]

    noStrafing = ship_systems_csv["noStrafing"]

    noAccel = ship_systems_csv["noAccel"]

    noShield = ship_systems_csv["noShield"]

    noVent = ship_systems_csv["noVent"]

    isPhaseCloak = ship_systems_csv["isPhaseCloak"]

    tags = ship_systems_csv["tags"]

    icon = f"/{ship_systems_csv["icon"]}"

    result = f"""# {name}

## 描述

<table class="table table-bordered" data-toggle="table" data-show-header="false"><thead style="display:none"><tr><th style="width:75%;text-align:left;vertical-align:top;">title</th><th style="width:25%;text-align:center;vertical-align:middle;"></th></tr></thead><tr><td style="width:75%;text-align:left;vertical-align:top;">{description}</td><td style="width:25%;text-align:center;vertical-align:middle;"><img decoding="async" src="{icon}"></td></tr></tbody></table>

## 详细信息

<table style="table table-bordered"><colgroup><col style="width: 21%"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"><col style="width: 20%;"><col style="width: 13%;"></colgroup><thead style="display:none"><tr><th>title</th><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody><tr><td>ID</td><td style="text-align:right;">{ship_systems_csv["id"]}</td><td>充能次数</td><td style="text-align:right;">{max_uses}</td><td>无法耗散硬幅能</td><td style="text-align:right;">{noHardDissipation}</td></tr><tr><td>系统维持(幅能/秒)</td><td style="text-align:right;">{flux_second}</td><td>恢复速率(次/秒)</td><td style="text-align:right;">{regen}</td><td>系统产生的幅能为硬幅能</td><td style="text-align:right;">{hardFlux}</td></tr><tr><td>系统维持(幅能耗散比率/秒)</td><td style="text-align:right;">{flux_second_rate}</td><td>前摇时长</td><td style="text-align:right;">{charge_up}</td><td>无法开火</td><td style="text-align:right;">{noFiring}</td></tr><tr><td>系统维持(幅能容量比率/秒)</td><td style="text-align:right;">{flux_second_cap}</td><td>全功率激活时长</td><td style="text-align:right;">{active}</td><td>无法转向</td><td style="text-align:right;">{noTurning}</td></tr><tr><td>激活消耗(幅能)</td><td style="text-align:right;">{flux_use}</td><td>后摇时长</td><td style="text-align:right;">{down}</td><td>无法左右平移</td><td style="text-align:right;">{noStrafing}</td></tr><tr><td>激活消耗(幅能耗散比率)</td><td style="text-align:right;">{flux_use_rate}</td><td>冷却时长</td><td style="text-align:right;">{cooldown}</td><td>无法向前加速</td><td style="text-align:right;">{noAccel}</td></tr><tr><td>激活消耗(幅能容量比率)</td><td style="text-align:right;">{flux_use_cap}</td><td>开关式的</td><td style="text-align:right;">{toggle}</td><td>无法启动护盾或右键战术系统</td><td style="text-align:right;">{noShield}</td></tr><tr><td>激活消耗(CR)</td><td style="text-align:right;">{cr_u}</td><td>无法耗散幅能</td><td style="text-align:right;">{noDissipation}</td><td>无法按V排散</td><td style="text-align:right;">{noVent}</td></tr><tr><td>战术系统被认为是一种相位</td><td style="text-align:right;">{isPhaseCloak}</td><td>Tags</td><td style="text-align:right;">{tags}</td><td></td><td style="text-align:right;"></td></tr></tbody></table>
"""
    return (result, name)

import math
from typing import Any


def generate_description(description: str, img: str) -> str:
    return f"""## 描述

<table class="table table-bordered" data-toggle="table" data-show-header="false"><thead style="display:none"><tr><th style="width:75%;text-align:left;vertical-align:top;">title</th><th style="width:25%;text-align:center;vertical-align:middle;"></th></tr></thead><tr><td style="width:75%;text-align:left;vertical-align:top;">{description}</td><td style="width:25%;text-align:center;vertical-align:middle;"><img decoding="async" src="{img}"></td></tr></tbody></table>
"""


def generate_other_info(map0: dict[str, Any]) -> str:
    result = """## 其他信息

<table><colgroup><col style="width: 30%"><col style="width: 20%;"><col style="width: 30%;"><col style="width: 20%;"></colgroup><thead style="display:none"><tr><th>title</th><th></th><th></th><th></th><th></th><th></th></tr></thead><tbody>"""
    map1 = []
    map2 = []
    limit = math.ceil(len(map0.keys()) / 2)
    i = 0
    for key, value in map0.items():
        if i < limit:
            map1.append((key, value))
        else:
            map2.append((key, value))
        i += 1
    for index, value1 in enumerate(map1):
        result += "<tr>"
        result += (
            f"""<td>{value1[0]}</td><td style="text-align:center;">{value1[1]}</td>"""
        )
        value2 = ("", "")
        if index < len(map2):
            value2 = map2[index]
        result += (
            f"""<td>{value2[0]}</td><td style="text-align:center;">{value2[1]}</td>"""
        )
        result += "</tr>"
    result += "</tbody></table>\n"
    return result


def generate_ship_list_md(ships) -> str:
    ship_list_md = """<div style="text-align:left;min-width:200px;min-height:0px;">"""
    for ship in ships:
        ship_list_md += generate_ship_list_item(ship)
    ship_list_md += "</div>\n"
    return ship_list_md


def generate_ship_list_item(ship) -> str:
    md_path = f"/hulls/{ship.id}.md"
    return f"""<div style="display:inline-block;text-align:center;min-width:150px;min-height:0px;padding-bottom:15px;"><div style="text-align:center;">[<div style="display:inline-block;text-align:center"><img decoding="async"src="{ship.img}"href="{md_path}"style="max-width:200px;max-height:200px;"/></div><br/>[{ship.name}]({md_path})]({md_path})</div></div>"""

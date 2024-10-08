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


def generate_list_md(items: list[tuple[str, str, str, str]], max_size: int) -> str:
    result = """<div style="text-align:left;min-width:200px;">"""
    for item in items:
        result += generate_list_item(*item, max_size)
    result += "</div>\n"
    return result


def generate_list_item(
    name: str, img: str, md_path: str, class_str: str, max_size: int
) -> str:
    return f"""<div class="{class_str}" style="display:inline-block;text-align:center;min-width:150px;padding-bottom:15px;"><div style="text-align:center;">[<div style="display:inline-block;text-align:center"><img decoding="async"src="{img}"href="{md_path}"style="max-width:{max_size}px;max-height:{max_size}px;"/></div><br/>[{name}]({md_path})]({md_path})</div></div>"""

# -*- coding: utf-8 -*-
"""
from petscan_list import text_bot

"""
from .wikitable import wiki_table
from . import petscan_bot as petscan
import wikitextparser as wtp


def fix_value(value):
    value = value.strip()
    # ---
    # if value looks  like this: (* item1\n* item2 ...) then make it list
    # ---
    if len(value.split("\n")) > 1 or value.startswith("*"):
        lista = [x.replace("*", "").strip() for x in value.split("\n")]
        return "%0D%0A".join(lista)
    # ---
    return value


def make_petscan_list(temp):
    # ---
    other_params = {}
    # ---
    petscan_params = {}
    for param in temp.arguments:
        name = str(param.name).strip()
        # ---
        value = str(param.value).strip()
        # ---
        if name.startswith("_"):
            other_params[name] = value

        if name == "ns":
            ns_list = [x.strip() for x in value.split(",")]
            for x in ns_list:
                petscan_params[f"ns%5B{x}%5D"] = 1
        else:
            value = fix_value(value)
            value = value.replace(" ", "_")
            petscan_params[name] = value
    # ---
    # petscan_params["lang"] = petscan_params.get("language") or petscan_params.get("lang") or ""
    # ---
    # print(petscan_params)
    # ---
    lista = petscan.make_petscan(petscan_params, return_dict=True)
    # ---
    return lista, other_params


def get_petscan_temp(text):
    prased = wtp.parse(text)
    # ---
    for temp in prased.templates:
        name = str(temp.normal_name()).strip().lower().replace("_", " ")
        if name == "petscan list":
            return temp

    return None


def change_list_to_text(p_list, other_params):
    # ---
    format_table = other_params.get("_result_", "").strip() == "table"
    # ---
    if format_table:
        return wiki_table(p_list)
    # ---
    text = "\n".join([f"# [[:{x}]]" for x in p_list])
    # ---
    text = "{{Div col|colwidth=20em}}" + "\n\n" + text + "\n\n{{Div col end}}"
    # ---
    return text


def change_it(text):
    newtext = text
    # ---
    temp = get_petscan_temp(text)
    # ---
    if not temp:
        return newtext
    # --
    p_list, other_params = make_petscan_list(temp)
    # ---
    if not p_list:
        return newtext
    # ---
    list_to_text = change_list_to_text(p_list, other_params)
    # ---
    newtext = temp.string + "\n\n== قائمة ==\n\n" + list_to_text
    # ---
    return newtext

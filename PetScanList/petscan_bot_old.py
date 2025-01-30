#!/usr/bin/python3
"""


"""
import sys
import requests
import urllib
import urllib.parse


Cate_NS = {"en": "Category", "commons": "Category", "ar": "تصنيف"}
Template_NS = {"en": "Template", "commons": "Template", "ar": "قالب"}

ns_text_tab = {
    "0": "",
    "1": "نقاش",
    "2": "مستخدم",
    "3": "نقاش المستخدم",
    "4": "ويكيبيديا",
    "5": "نقاش ويكيبيديا",
    "6": "ملف",
    "7": "نقاش الملف",
    "10": "قالب",
    "11": "نقاش القالب",
    "12": "مساعدة",
    "13": "نقاش المساعدة",
    "14": "تصنيف",
    "15": "نقاش التصنيف",
    "100": "بوابة",
    "101": "نقاش البوابة",
    "828": "وحدة",
    "829": "نقاش الوحدة",
    "2600": "موضوع",
    "1728": "فعالية",
    "1729": "نقاش الفعالية",
    }


def dec(x):
    fao = x
    fao = fao.replace(" ", "_")
    endash = False

    if fao.find("–") != -1:
        endash = True
        fao = fao.replace("–", "ioioioioio")

    try:
        fao = urllib.parse.quote(fao)
    except Exception as e:
        print(e)

    if endash:
        fao = fao.replace("ioioioioio", "%E2%80%93")

    return fao


def get_pet_tab_result(PET_TABLE):
    PET_TABLE["format"] = "json"

    PET_TABLE["combination"] = PET_TABLE.get("combination", "union")

    PET_TABLE["common_wiki"] = "cats"

    PET_TABLE["depth"] = PET_TABLE.get("depth", "0")

    url = "https://petscan.wmflabs.org/?doit=Do_it"  # &min_redlink_count=1&sparse=on

    for param, value in PET_TABLE.items():
        if value:
            url += f"&{param}={str(value)}"

    jso = {}

    if "printurl" in sys.argv:
        print(url)

    try:
        req = requests.Session().get(url, timeout=10)

        jso = req.json()
    except Exception as e:
        print(e)

    if not jso:
        print(url)
        return []

    return jso


def get_results(PET_TABLE, return_dict=False):
    pet_tab_result = get_pet_tab_result(PET_TABLE)

    if not pet_tab_result:
        if return_dict:
            return {}
        return []

    Lang = PET_TABLE.get("language") or "ar"

    tabe = {}
    num = 0

    tab = [x for x in pet_tab_result["*"][0]["a"]["*"]]

    print(f"len of pet_tab_result: {len(pet_tab_result)}")
    print(f"len of tab: {len(tab)}")

    for x in tab:
        num += 1
        tabe_num = {}
        tabe_num["touched"] = x.get("touched", "")
        tabe_num["Q"] = x.get("q", "")
        tabe_num["ns"] = x.get("namespace", "")
        tabe_num["len"] = x.get("len", 0)
        n_s = tabe_num["ns"]

        ns_text = x.get("nstext", "")
        title = x.get("title", "")

        if str(n_s) == "14":
            title = f"{Cate_NS[Lang]}:{title}"
        elif str(n_s) == "10":
            title = f"{Template_NS[Lang]}:{title}"

        elif ns_text_tab.get(str(n_s)):
            title = f"{ns_text_tab[str(n_s)]}:{title}"

        elif ns_text:
            title = f"{ns_text}:{title}"

        title = title.replace("_", " ")

        tabe_num["title"] = title

        tabe[title] = tabe_num

    tabe_list = [x for x in tabe.keys()]

    if return_dict:
        return tabe

    return tabe_list


def get_petscan_results(Tab, return_dict=False):
    return get_results(Tab, return_dict=return_dict)

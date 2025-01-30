# -*- coding: utf-8 -*-
"""
python3 core8/pwb.py petscan_list/bot
python3 I:\core\bots\new\petscan_list\bot.py
"""
from PetScanList import get_petscan_results, one_page


def start():
    Tab = {}
    Tab["templates_any"] = "petscan list"
    Tab["language"] = "ar"
    Tab["project"] = "wikipedia"
    # ---
    pages = get_petscan_results(Tab)

    for n, x in enumerate(pages):
        print("_______________")
        print(f"p: {n}/{len(pages)} title: {x}")
        one_page(x)


if __name__ == "__main__":
    start()

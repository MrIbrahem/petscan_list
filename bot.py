# -*- coding: utf-8 -*-
"""
www/python/venv/bin/python3 www/python/src/bot.py

python3 core8/pwb.py petscan_list/bot
python3 I:\core\bots\new\petscan_list\bot.py
"""
from PetScanList import get_petscan_results, one_site_pages
from PetScanList import valid_projects

def start():
    for project, langs in valid_projects.items():
        for lang in langs:
            Tab = {}
            # ---
            Tab["templates_any"] = "petscan list"
            # ---
            Tab["project"] = project
            Tab["language"] = lang
            # ---
            wiki = f"{lang}.{project}.org"
            # ---
            pages = get_petscan_results(Tab)
            # ---
            one_site_pages(pages, wiki)


if __name__ == "__main__":
    start()

# -*- coding: utf-8 -*-
"""
"""
from PetScanList import get_petscan_results


def get_all_pages(lang, project):
    # ---
    Tab = {}
    # ---
    Tab["templates_any"] = "petscan list"
    # ---
    Tab["project"] = project
    Tab["language"] = lang
    # ---
    # wiki = f"{lang}.{project}.org"
    # ---
    pages = get_petscan_results(Tab)
    # ---
    if not pages:
        return ["No pages found"]
    # ---
    return pages


if __name__ == "__main__":
    get_all_pages()

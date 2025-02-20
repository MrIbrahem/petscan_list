# -*- coding: utf-8 -*-
"""
"""
from PetScanList import get_petscan_results


def get_all_pages(lang, project, split_by_ns=False):
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
    pages = get_petscan_results(Tab, split_by_ns=split_by_ns)
    # ---
    if not pages:
        return ["No pages found"]
    # ---
    return pages


if __name__ == "__main__":
    # Example usage:
    pages = get_all_pages("en", "wikipedia")
    print(pages)

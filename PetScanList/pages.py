# -*- coding: utf-8 -*-
"""
This module retrieves and processes pages using PetScan.
"""

from PetScanList import get_petscan_results
from typing import List

def get_all_pages(lang: str, project: str, split_by_ns: bool = False) -> List[str]:
    """
    Retrieve all pages for the given language and project using PetScan.

    Parameters:
    lang (str): The language code.
    project (str): The project name.
    split_by_ns (bool): Whether to split results by namespace. Default is False.

    Returns:
    List[str]: A list of page titles. If no pages are found, returns ["No pages found"].
    """
    tab = {
        "templates_any": "petscan list",
        "project": project,
        "language": lang
    }

    try:
        pages = get_petscan_results(tab, split_by_ns=split_by_ns)
    except Exception as e:
        # Log the error
        print(f"Error retrieving pages: {e}")
        return ["No pages found"]

    if not pages:
        return ["No pages found"]

    return pages

if __name__ == "__main__":
    # Example usage:
    pages = get_all_pages("en", "wikipedia")
    print(pages)

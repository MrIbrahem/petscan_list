# -*- coding: utf-8 -*-
"""

python3 I:\core\bots\new\petscan_list\test.py

"""
from PetScanList import one_page

if __name__ == "__main__":
    title = "User:Mr. Ibrahem/جيدة"
    wiki = "ar.wikipedia.org"
    tab = one_page(title, wiki)
    print(tab)

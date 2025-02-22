# -*- coding: utf-8 -*-
"""

python3 I:\core\bots\new\petscan_list\test.py

"""
from PetScanList import one_page, add_result_to_text
import PetScanList.printe as printe

temp = """{{petscan list
| templates_any=لا مصدر
| language=ar
| project=wikipedia
| categories=الجزائر
| output_limit=10
| _result_ = table
}}"""
temp1 = """{{petscan list
| templates_any=لا مصدر
| language=ar
| project=wikipedia
| categories=اليمن
| output_limit=10
| _result_ = table
}}"""
temp_end = """{{petscan list end}}"""
results = """{| class="wikitable sortable"
|-
! #
! id
! الحجم
! n
! النطاق
! nstext
! معرف ويكي بيانات
! العنوان
! آخر تعديل
! wikidata
|-
! 1
| 1524200
| 917
| page
| 0
|
| {{Q|Q970381}}
| [[دائرة سقانة]]
| 2024-02-29 08:37:37
| Q970381
|}"""

text = f"{temp}\n{results}\n{temp_end}"
text += f"\n==2323==\n{temp1}\n{results}\n{temp_end}"


def test_add_text():
    new_text = add_result_to_text(text, "!!!s", temp, temp_end)
    # ---
    printe.showDiff(text, new_text)


def test_one_page():
    title = "User:Mr. Ibrahem/جيدة"
    wiki = "ar.wikipedia.org"
    tab = one_page(title, wiki)
    print(tab)


if __name__ == "__main__":
    test_add_text()

# -*- coding: utf-8 -*-
"""
from .one_page_bot import one_page
"""
import logging

logging.basicConfig(level=logging.WARNING)

import mwclient
from . import text_bot
from .account import username, password

season = {1: False, "csrftoken": False}

sites = {1: False}


def one_page(x):
    # ---
    x2 = x.lower().strip().replace("_", " ")
    # ---
    print("x2", x2)
    # ---
    if x2.find("petscan list") != -1:
        return "لا يمكن تحديث قالب:Petscan list!"
    # ---
    if not sites[1]:
        sites[1] = mwclient.Site("ar.wikipedia.org")
        sites[1].login(username, password)
    # ---
    page = sites[1].Pages[x]
    text = page.text()
    # ---
    if not text:
        print("no text")
        return "no text"
    # ---
    newtext = text_bot.change_it(text)
    # ---
    if text == newtext:
        print("no changes")
        return "no changes"
    # ---
    summary = "بوت: تحديث قائمة (تجريبي)"
    # ---
    save = page.save(newtext, summary=summary)
    # ---
    if isinstance(save, dict):
        # OrderedDict([('result', 'Success'), ('pageid', 9857018), ('title', 'ويكيبيديا:برنامج قراءة ويكيبيديا في الصف - اليمن 2/مقالات مقترحة/لا مصدر'), ('contentmodel', 'wikitext'), ('oldrevid', 69427827), ('newrevid', 69427829), ('newtimestamp', '2025-01-29T00:41:53Z')])
        if save.get("result") == "Success":
            te = "save success"
        else:
            te = str(save)
    else:
        te = f"save failed: {save}"
    # ---
    print(te)
    return te

# -*- coding: utf-8 -*-
"""
This module handles updating a single Wikipedia page using a bot.
"""

import logging
import mwclient
from . import text_bot
from .account import username, password

# Configure logging
logging.basicConfig(level=logging.WARNING)

# Global variables
sites = {1: False}

CLASS_ERROR = "danger"
CLASS_WARNING = "warning"
CLASS_SUCCESS = "success"


def initialize_site(wiki="ar.wikipedia.org"):
    """
    Initialize and log in to the Wikipedia site if not already done.
    """
    if not sites.get(wiki):
        sites[wiki] = mwclient.Site(wiki)
        try:
            sites[wiki].login(username, password)
        except mwclient.errors.LoginError as e:
            logging.error(f"Error logging in: {e}")
            return None
    return sites[wiki]


def is_petscan_list_page(page_title):
    """
    Check if the page title indicates it contains a `petscan list` template.
    """
    return "petscan list" in page_title.lower().strip().replace("_", " ")


def update_page_content(page_title, wiki):
    """
    Update the content of a Wikipedia page using the `text_bot.process_text` function.
    """
    # ---
    result_class = ""
    # ---
    if is_petscan_list_page(page_title):
        return "لا يمكن تحديث قالب:Petscan list!", CLASS_ERROR

    site = initialize_site(wiki)
    page = site.Pages[page_title]
    text = page.text()

    if not text:
        logging.warning(f"No text found for page: {page_title}")
        return "الصفحة فارغة أو غير موجودة!", CLASS_WARNING

    newtext, mssg = text_bot.process_text(text)
    if mssg != "":
        logging.info(mssg)
        return mssg

    if text == newtext:
        logging.info("No changes detected in the page content.")
        return "لا يوجد أي تغيير!", CLASS_WARNING

    summary = "بوت: تحديث قائمة (تجريبي)"

    try:
        save_result = page.save(newtext, summary=summary)
    except Exception as e:
        logging.error(f"Exception occurred while saving page: {e}")
        return str(e), CLASS_ERROR
    # ---
    if isinstance(save_result, dict):
        if save_result.get("result") == "Success":
            return "تم الحفظ بنجاح!", CLASS_SUCCESS
        else:
            return str(save_result), CLASS_ERROR
    else:
        return f"save failed: {save_result}", CLASS_ERROR


def one_page(page_title, wiki):
    """
    Main function to process and update a single Wikipedia page.
    """
    logging.info(f"Processing page: {page_title}")
    # ---
    result, result_class = update_page_content(page_title, wiki)
    # ---
    logging.info(result_class)
    logging.info(result)
    # ---
    # ---
    return result, result_class


# Example usage
if __name__ == "__main__":
    page_title = "ويكيبيديا:برنامج قراءة ويكيبيديا في الصف - اليمن 2/مقالات مقترحة/لا مصدر"
    result = one_page(page_title, "ar.wikipedia.org")
    print(result)

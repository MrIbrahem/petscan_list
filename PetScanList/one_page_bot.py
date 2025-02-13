# -*- coding: utf-8 -*-
"""
This module handles updating a single Wikipedia page using a bot.
"""

import logging
import mwclient
from . import text_bot
from .account import username, password
from .I18n import get_translations

translations = get_translations()

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
    if is_petscan_list_page(page_title):
        error = "pet_scan_page_error"
        return error, CLASS_ERROR

    site = initialize_site(wiki)
    page = site.Pages[page_title]
    text = page.text()
    ns = page.namespace
    if not text:
        logging.warning(f"Namespace 0 aren't Supported: {page_title}")
        return "ns0_not_supported", CLASS_WARNING
    if not text:
        logging.warning(f"No text found for page: {page_title}")
        return "empty_page", CLASS_WARNING

    newtext, mssg = text_bot.process_text(text)
    if mssg != "":
        logging.info(mssg)
        return mssg, CLASS_WARNING

    if text == newtext:
        logging.info("No changes detected in the page content.")
        return "no_changes", CLASS_WARNING

    summary = translations["summary"]

    try:
        save_result = page.save(newtext, summary=summary)
    except Exception as e:
        logging.error(f"Exception occurred while saving page: {e}")
        return str(e), CLASS_ERROR
    # ---
    if isinstance(save_result, dict):
        if save_result.get("result") == "Success":
            return "save_success", CLASS_SUCCESS
        else:
            return str(save_result), CLASS_ERROR
    else:
        # msg = translations["save_error"].format(error=str(save_result))
        msg = "save_error"
        return msg, CLASS_ERROR


def one_page(page_title, wiki):
    """
    Main function to process and update a single Wikipedia page.
    """
    logging.info(f"Processing page: {page_title}")
    # ---
    result, result_class = update_page_content(page_title, wiki)
    # ---
    if result == "By default, mwclient protects you from accidentally editing without being logged in. If you actually want to edit without logging in, you can set force_login on the Site object to False.":
        result = "save error, not logged in"
    # ---
    logging.info(result_class)
    logging.info(result)
    # ---
    return result, result_class


# Example usage
if __name__ == "__main__":
    page_title = "ويكيبيديا:برنامج قراءة ويكيبيديا في الصف - اليمن 2/مقالات مقترحة/لا مصدر"
    result = one_page(page_title, "ar.wikipedia.org")
    print(result)

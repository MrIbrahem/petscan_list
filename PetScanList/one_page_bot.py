# -*- coding: utf-8 -*-
"""
This module handles updating a single Wikipedia page using a bot.
"""

import logging
import mwclient
from . import text_bot
from .account import username, password
from .I18n import make_translations


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


def return_tab(result_text, result_class):

    return {
        "result_text": result_text,
        "result_class": result_class,
    }


def extract_lang_code(wiki_url: str) -> str:
    """Extract language code from wiki URL safely."""
    try:
        return wiki_url.split(".")[0].lower()
    except (AttributeError, IndexError):
        return "en"  # Default to English


def update_page_content(page_title, wiki):
    """
    Update the content of a Wikipedia page using the `text_bot.process_text` function.
    """
    # ---
    if is_petscan_list_page(page_title):
        error = "pet_scan_page_error"
        # ---
        return return_tab(error, CLASS_ERROR)

    site = initialize_site(wiki)

    if not site:
        logging.warning(f"Failed to initialize site: {wiki}")
        return return_tab("site_not_initialized", CLASS_WARNING)
    try:
        page = site.Pages[page_title]
        text = page.text()
        ns = page.namespace

    except mwclient.errors.PageError as e:
        logging.warning(f"Page not found: {e}")
        return return_tab("page_not_found", CLASS_WARNING)

    except Exception as e:
        logging.error(f"Exception occurred while fetching page: {e}")
        return return_tab("error", CLASS_ERROR)

    if str(ns) == "0":
        logging.warning(f"Namespace 0 is not supported: {page_title}")
        return return_tab("ns0_not_supported", CLASS_WARNING)
    if not text:
        logging.warning(f"No text found for page: {page_title}")
        return return_tab("empty_page", CLASS_WARNING)

    lang = extract_lang_code(wiki)

    new_tab, mssg = text_bot.process_text(text, lang)

    if mssg != "":
        logging.info(mssg)
        return return_tab(mssg, CLASS_WARNING)

    length = 0

    newtext = new_tab.get("text", "")
    length = new_tab.get("length", 0)

    if text == newtext:
        logging.info("No changes detected in the page content.")
        return return_tab("no_changes", CLASS_WARNING)

    if not newtext.strip():
        logging.info("No newtext generated....")
        return return_tab("no_changes", CLASS_WARNING)

    summary = make_translations("summary", lang) + f" ({length})"

    try:
        save_result = page.save(newtext, summary=summary)
    except Exception as e:
        logging.error(f"Exception occurred while saving page: {e}")
        return return_tab(str(e), CLASS_ERROR)
    # ---
    if not isinstance(save_result, dict):
        # msg = translations["save_error"].format(error=str(save_result))
        msg = "save_error"
        return return_tab(msg, CLASS_ERROR)
    # ---
    if save_result.get("result") != "Success":
        return return_tab(str(save_result), CLASS_ERROR)

    # print(save_result)
    # {'result': 'Success', 'pageid': 9868421, 'title': 'مستخدم:Mr. Ibrahem/جيدة', 'contentmodel': 'wikitext', 'oldrevid': 69634440, 'newrevid': 69634441, 'newtimestamp': '2025-02-20T01:10:50Z'}

    tab = {
        "result_text": "save_success",
        "result_class": CLASS_SUCCESS,
        "newrevid": save_result.get("newrevid"),
        "length" : length
    }
    return tab


def one_page(page_title, wiki):
    """
    Main function to process and update a single Wikipedia page.
    """
    logging.info(f"Processing page: {page_title}")
    # ---
    result = update_page_content(page_title, wiki)
    # ---
    result_class = result.get("result_class", "")
    result_text = result.get("result_text", "")
    # ---
    if result_text == "By default, mwclient protects you from accidentally editing without being logged in. If you actually want to edit without logging in, you can set force_login on the Site object to False.":
        result_text = "save error, not logged in"
    # ---
    logging.info(result_class)
    logging.info(result_text)
    # ---
    return result


# Example usage
if __name__ == "__main__":
    page_title = "User:Mr. Ibrahem/جيدة"
    result = one_page(page_title, "ar.wikipedia.org")
    print(result)

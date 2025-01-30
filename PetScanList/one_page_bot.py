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


def initialize_site():
    """
    Initialize and log in to the Wikipedia site if not already done.
    """
    if not sites[1]:
        sites[1] = mwclient.Site("ar.wikipedia.org")
        try:
            sites[1].login(username, password)
        except mwclient.errors.LoginError as e:
            logging.error(f"Error logging in: {e}")
            return None
    return sites[1]


def is_petscan_list_page(page_title):
    """
    Check if the page title indicates it contains a `petscan list` template.
    """
    return "petscan list" in page_title.lower().strip().replace("_", " ")


def update_page_content(page_title):
    """
    Update the content of a Wikipedia page using the `text_bot.process_text` function.
    """
    if is_petscan_list_page(page_title):
        return "لا يمكن تحديث قالب:Petscan list!"

    site = initialize_site()
    page = site.Pages[page_title]
    text = page.text()

    if not text:
        logging.warning(f"No text found for page: {page_title}")
        return "no text"

    newtext = text_bot.process_text(text)

    if text == newtext:
        logging.info("No changes detected in the page content.")
        return "no changes"

    summary = "بوت: تحديث قائمة (تجريبي)"
    try:
        save_result = page.save(newtext, summary=summary)
    except Exception as e:
        logging.error(f"Exception occurred while saving page: {e}")
        return str(e)

    return handle_save_result(save_result)


def handle_save_result(save_result):
    """
    Handle the result of the page save operation.
    """
    if isinstance(save_result, dict):
        if save_result.get("result") == "Success":
            return "save success"
        else:
            return str(save_result)
    else:
        return f"save failed: {save_result}"


def one_page(page_title):
    """
    Main function to process and update a single Wikipedia page.
    """
    logging.info(f"Processing page: {page_title}")
    result = update_page_content(page_title)
    logging.info(result)
    return result


# Example usage
if __name__ == "__main__":
    page_title = "ويكيبيديا:برنامج قراءة ويكيبيديا في الصف - اليمن 2/مقالات مقترحة/لا مصدر"
    result = one_page(page_title)
    print(result)

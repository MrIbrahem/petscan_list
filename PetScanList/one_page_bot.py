import sys
import logging
import mwclient
from .account import username, password
from .I18n import make_translations
from . import text_bot
from . import printe

LOGGING_LEVEL = logging.DEBUG
# LOGGING_LEVEL = logging.INFO
logging.basicConfig(level=LOGGING_LEVEL)


class WikiBot:
    CLASS_ERROR = "danger"
    CLASS_WARNING = "warning"
    CLASS_SUCCESS = "success"

    def __init__(self, username, password):
        self.sites = {}
        self.username = username
        self.password = password

    def initialize_site(self, wiki):
        if not self.sites.get(wiki):
            self.sites[wiki] = mwclient.Site(wiki)
            try:
                self.sites[wiki].login(self.username, self.password)
            except mwclient.errors.LoginError as e:
                logging.error(f"Error logging in: {e}")
                return None
        return self.sites[wiki]

    def return_tab(self, result_text, result_class):
        return {
            "result_text": result_text,
            "result_class": result_class,
        }

    def extract_lang_code(self, wiki_url: str) -> str:
        try:
            return wiki_url.split(".")[0].lower()
        except (AttributeError, IndexError):
            return "en"

    def save(self, page, newtext, summary):
        if "ask" in sys.argv:
            old_text = page.text()
            printe.showDiff(old_text, newtext)
            ask = input(f"Do you want to save the changes? (y/n): {summary=}")
            yess = ["", "y", "a"]
            if ask not in yess:
                return False
        # ---
        try:
            save_result = page.save(newtext, summary=summary)
            return save_result
        except Exception as e:
            return self.return_tab(str(e), self.CLASS_ERROR)

    def update_page_content(self, page_title, wiki):
        site = self.initialize_site(wiki)
        if not site:
            return self.return_tab("site_not_initialized", self.CLASS_WARNING)

        try:
            page = site.Pages[page_title]
            text = page.text()
            ns = page.namespace

        except mwclient.errors.PageError as e:
            return self.return_tab("page_not_found", self.CLASS_WARNING)
        except Exception as e:
            return self.return_tab("error", self.CLASS_ERROR)

        if ns == 0:
            return self.return_tab("ns0_not_supported", self.CLASS_WARNING)
        if not text:
            return self.return_tab("empty_page", self.CLASS_WARNING)

        lang = self.extract_lang_code(wiki)

        # if text.lower().find("{{petscan list end}}") == -1 and text.find("== قائمة ==") != -1:
        #     text = text.replace("== قائمة ==", "")
        #     text += "\n{{Petscan list end}}"
        #     save_result = self.save(page, text, summary="بوت: تعديل القائمة")
        #     return

        new_tab, mssg = text_bot.process_text(text, lang)

        if mssg:
            return self.return_tab(mssg, self.CLASS_WARNING)

        newtext = new_tab.get("text", "")
        length = new_tab.get("length", 0)

        if text == newtext or not newtext.strip():
            return self.return_tab("no_changes", self.CLASS_WARNING)

        summary = make_translations("summary", lang) + f" ({length})"
        try:
            save_result = self.save(page, newtext, summary=summary)
        except Exception as e:
            return self.return_tab(str(e), self.CLASS_ERROR)

        if not isinstance(save_result, dict) or save_result.get("result") != "Success":
            return self.return_tab("save_error", self.CLASS_ERROR)

        return {
            "result_text": "save_success",
            "result_class": self.CLASS_SUCCESS,
            "newrevid": save_result.get("newrevid"),
            "length": length
        }

    def one_page(self, page_title, wiki):
        logging.info(f"Processing page: {page_title}")
        result = self.update_page_content(page_title, wiki)
        result_text = result.get("result_text", "")

        if result_text.startswith('By default, mwclient'):
            result["result_text"] = "save error, not logged in"

        logging.info(result.get("result_class", ""))
        logging.info(result["result_text"])
        return result

    def many_pages(self, titles, wiki):
        # ---
        for n, x in enumerate(titles):
            print("_______________")
            print(f"p: {n}/{len(titles)} title: {x} ({wiki=})")
            # ---
            self.one_page(x, wiki)


def one_site_pages(titles, site):
    bot = WikiBot(username, password)
    bot.many_pages(titles, site)


def one_page(title, site):
    bot = WikiBot(username, password)
    result = bot.one_page(title, site)
    return result


if __name__ == "__main__":
    page_title = "User:Mr. Ibrahem/جيدة"
    result = one_page(page_title, "ar.wikipedia.org")
    print(result)

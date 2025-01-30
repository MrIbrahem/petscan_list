# -*- coding: utf-8 -*-
"""

from .make_template import MakeTemplate

"""
from urllib.parse import urlparse, parse_qs
from urllib.parse import ParseResult

false_params = [
    "interface_language",
    "active_tab",
    "format",
]


def MakeTemplate(url: str) -> str:
    """
    Create a template string for a 'petscan list' by processing a given URL.

    Args:
        url (str): A string representing a URL that contains query parameters.

    Returns:
        str: A string formatted as a 'petscan list' containing the parsed URL parameters.
    """
    temp = []
    # ---
    parsed_url: ParseResult = urlparse(url)
    if not parsed_url.query:
        raise ValueError("URL must contain query parameters")
    # ---
    # Parse URL then add keys and values to temp
    # ---
    query_params = parse_qs(urlparse(url).query)
    # ---
    for key, values in query_params.items():
        if key in false_params:
            continue
        # ---
        values = list(set([value.strip() for value in values if value.strip()]))
        # ---
        if not values:
            continue
        # ---
        value = values[0]
        # ---
        if len(value.split("\n")) > 1:
            value = "\n* " + "\n* ".join([x.strip() for x in value.split("\n") if x.strip()])
        # ---
        print(key, [value])
        # ---
        temp.append(f"{key}={value}")
    # ---
    params = "\n| ".join(temp)
    # ---
    temp = f"{{{{petscan list\n| {params}\n}}}}"
    # ---
    return temp


if __name__ == "__main__":
    url = "https://petscan.wmcloud.org/?referrer_url=&maxlinks=&sitelinks_yes=&langs_labels_no=&interface_language=en&negcats=&manual_list_wiki=enwiki&cb_labels_any_l=1&source_combination=&wikidata_item=no&sortorder=descending&links_to_all=&templates_any=&manual_list=Intergluteal+cleft%0D%0AIngrown+hair%0D%0ASacral+dimple&ores_prob_to=&referrer_name=&before=&minlinks=&ns%5B0%5D=1&sortby=size&outlinks_any=&wpiu=any&cb_labels_yes_l=1&labels_no=&active_tab=tab_other_sources&search_max_results=500&project=wikipedia&outlinks_no=&max_age=&search_query=&ores_type=any&language=en&depth=0&after=&edits%5Banons%5D=both&cb_labels_no_l=1&sitelinks_any=&search_filter=&ores_prob_from=&labels_yes=&outlinks_yes=&sitelinks_no=arwiki&sitelinks_no=arwiki&sitelinks_no=arwiki"
    print(MakeTemplate(url))

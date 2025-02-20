
# -*- coding: utf-8 -*-
"""
Script to create a template string for a 'petscan list' by processing a given URL.
"""

from urllib.parse import urlparse, parse_qs, ParseResult

FALSE_PARAMS = [
    "interface_language",
    "active_tab",
    "output_compatability",
    "format",
    "json-pretty",
]

def is_valid_line_format(line_format: str) -> bool:
    if not line_format:
        return False
    line_format = line_format.strip()
    return line_format != "$1" and "$1" in line_format

def make_template(url: str, request_form: dict) -> str:
    """
    Create a template string for a 'petscan list' by processing a given URL.

    Args:
        url (str): A string representing a URL that contains query parameters.
        request_form (dict): A dictionary containing form data.

    Returns:
        str: A string formatted as a 'petscan list' containing the parsed URL parameters.
    """
    line_format = request_form.get("_line_format_")
    parsed_url: ParseResult = urlparse(url)
    if not parsed_url.query:
        raise ValueError("URL must contain query parameters")

    query_params = parse_qs(parsed_url.query)
    temp = []

    if is_valid_line_format(line_format):
        temp.append(f"_line_format_={line_format}")

    for key, values in query_params.items():
        if key in FALSE_PARAMS:
            continue

        values = list({value.strip() for value in values if value.strip()})
        if not values:
            continue

        value = values[0]
        if len(value.split("\n")) > 1:
            value = "\n* " + "\n* ".join(x.strip() for x in value.split("\n") if x.strip())

        temp.append(f"{key}={value}")

    params = "\n| ".join(temp)
    template = f"{{{{petscan list\n| {params}\n}}}}"

    return template

if __name__ == "__main__":
    url = "https://petscan.wmcloud.org/?referrer_url=&maxlinks=&sitelinks_yes=&langs_labels_no=&interface_language=en&negcats=&manual_list_wiki=enwiki&cb_labels_any_l=1&source_combination=&wikidata_item=no&sortorder=descending&links_to_all=&templates_any=&manual_list=Intergluteal+cleft%0D%0AIngrown+hair%0D%0ASacral+dimple&ores_prob_to=&referrer_name=&before=&minlinks=&ns%5B0%5D=1&sortby=size&outlinks_any=&wpiu=any&cb_labels_yes_l=1&labels_no=&active_tab=tab_other_sources&search_max_results=500&project=wikipedia&outlinks_no=&max_age=&search_query=&ores_type=any&language=en&depth=0&after=&edits%5Banons%5D=both&cb_labels_no_l=1&sitelinks_any=&search_filter=&ores_prob_from=&labels_yes=&outlinks_yes=&sitelinks_no=arwiki&sitelinks_no=arwiki&sitelinks_no=arwiki"
    print(MakeTemplate(url))

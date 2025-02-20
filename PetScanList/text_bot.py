# -*- coding: utf-8 -*-
"""
This module processes text containing a `petscan list` template and generates a formatted list or table.
"""

from .wikitable import wiki_table
from . import petscan_bot as petscan
import wikitextparser as wtp
from .I18n import make_translations

# Constants
DEFAULT_SECTION_HEADER_KEY = "section_title"
NO_TEMPLATE_MESSAGE = "no_template"
NO_RESULT_MESSAGE = "no_result_petscan"

def fix_value(value):
    """
    Clean and format the value. If the value is a list (e.g., "* item1\n* item2"), convert it to a single string.
    """
    value = value.strip()
    if "\n" in value or value.startswith("*"):
        # Convert list-like values into a single string separated by "\r\n"
        lista = [item.replace("*", "").strip() for item in value.split("\n")]
        return "\r\n".join(lista)
    return value


false_params = [
    "interface_language",
    "active_tab",
    "output_compatability",
    "format",
    "json-pretty",
]


def make_petscan_list(template):
    """
    Extract parameters from the `petscan list` template and generate a PetScan query.
    """
    petscan_params = {}
    other_params = {}

    for param in template.arguments:
        name = str(param.name).strip()
        value = str(param.value).strip()

        if name.startswith("_"):
            # Handle special parameters (those starting with "_")
            other_params[name] = value
        elif name == "ns":
            # Handle namespace parameters (e.g., "ns=0,1,2")
            for ns in value.split(","):
                try:
                    ns = int(ns.strip())  # Validate namespace is a number
                    petscan_params[f"ns%5B{ns}%5D"] = 1
                except ValueError:
                    print(f"Warning: Invalid namespace value '{ns}'")
                    continue
        elif name not in false_params:
            # Fix and format the value for PetScan
            value = fix_value(value)
            value = value.replace(" ", "_")
            petscan_params[name] = value

    # Generate the PetScan list
    lista = petscan.get_petscan_results(petscan_params)

    return lista, other_params


def get_petscan_template(text):
    """
    Find and return the `petscan list` template from the given text.
    """
    parsed = wtp.parse(text)
    for template in parsed.templates:
        name = str(template.normal_name()).strip().lower().replace("_", " ")
        if name == "petscan list":
            return template
    return None


def format_list_as_text(p_list, other_params):
    """
    Format the list as either a wikitable or a bulleted list, depending on the parameters.
    """
    if other_params.get("_result_", "").strip() == "table":
        return wiki_table(p_list)

    line_format = "# [[:$1]]"

    _line_format_ = other_params.get("_line_format_", "").strip()

    if _line_format_.find("$1") != -1:
        line_format = _line_format_

    # Format as a bulleted list inside a Div col
    text = "\n".join([line_format.replace("$1", x) for x in p_list])
    return "{{Div col|colwidth=20em}}\n\n" + text + "\n\n{{Div col end}}"


def construct_section0(text, template_string):
    """
    Construct the section0 part of the text.
    """
    if text.find(template_string) != -1:
        return text.split(template_string)[0] + template_string
    return template_string


def process_text(text, lang):
    """
    Process the input text, find the `petscan list` template, and generate the formatted output.
    """
    template = get_petscan_template(text)
    if not template:
        return {}, NO_TEMPLATE_MESSAGE

    p_list, other_params = make_petscan_list(template)
    
    if not p_list:
        return {}, NO_RESULT_MESSAGE

    if isinstance(p_list, list) and p_list[0] == "":
        return {}, NO_RESULT_MESSAGE

    formatted_list = format_list_as_text(p_list, other_params)

    section0 = construct_section0(text, template.string)
    DEFAULT_SECTION_HEADER = make_translations(DEFAULT_SECTION_HEADER_KEY, lang)
    new_text = f"{section0}\n\n== {DEFAULT_SECTION_HEADER} ==\n\n{formatted_list}"

    tab = {
        "text": new_text,
        "length": len(p_list),
    }

    return tab, ""

# Example usage
if __name__ == "__main__":
    input_text = """
    {{petscan list
    |ns=0,1
    |title=Test
    |_result_=table
    }}
    """
    output_text, mssg = process_text(input_text, "ar")
    print(output_text)

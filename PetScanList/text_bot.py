# -*- coding: utf-8 -*-
"""
This module processes text containing a `petscan list` template and generates a formatted list or table.
"""

from .wikitable import wiki_table
from . import petscan_bot as petscan
import wikitextparser as wtp

DEFAULT_SECTION_HEADER = "قائمة"  # Arabic for "List"


def fix_value(value):
    """
    Clean and format the value. If the value is a list (e.g., "* item1\n* item2"), convert it to a single string.
    """
    value = value.strip()
    if "\n" in value or value.startswith("*"):
        # Convert list-like values into a single string separated by "%0D%0A"
        lista = [item.replace("*", "").strip() for item in value.split("\n")]
        return "%0D%0A".join(lista)
    return value


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
        else:
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

    # Format as a bulleted list inside a Div col
    text = "\n".join([f"# [[:{x}]]" for x in p_list])
    return "{{Div col|colwidth=20em}}\n\n" + text + "\n\n{{Div col end}}"


def process_text(text):
    """
    Process the input text, find the `petscan list` template, and generate the formatted output.
    """
    template = get_petscan_template(text)
    if not template:
        return text

    p_list, other_params = make_petscan_list(template)
    if not p_list:
        return text

    formatted_list = format_list_as_text(p_list, other_params)
    return f"{template.string}\n\n== {DEFAULT_SECTION_HEADER} ==\n\n{formatted_list}"


# Example usage
if __name__ == "__main__":
    input_text = """
    {{petscan list
    |ns=0,1
    |title=Test
    |_result_=table
    }}
    """
    output_text = process_text(input_text)
    print(output_text)

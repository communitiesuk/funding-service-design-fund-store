# import copy
# import json
import os

# from bs4 import BeautifulSoup


def determine_display_value_for_condition(condition_value, list_name, form_lists):
    if condition_value.casefold() == "true":
        return "Yes"
    elif condition_value.casefold() == "false":
        return "No"
    else:
        if list_name:
            list_values = next(
                lizt["items"] for lizt in form_lists if lizt["name"] == list_name
            )
            condition_text = next(
                item["text"] for item in list_values if item["value"] == condition_value
            )
            return condition_text
        return condition_value


def find_forms_dir(path_to_form_jsons, fund_short_name, round_short_name, lang):
    round_folder_path = os.path.join(
        path_to_form_jsons,
        f"{fund_short_name.casefold()}_{round_short_name.casefold()}",
    )
    if not os.path.isdir(round_folder_path):
        print(f"ERROR Could not find form_jsons at {round_folder_path}")

    path_with_lang = os.path.join(round_folder_path, lang)
    if not os.path.isdir(path_with_lang):
        return round_folder_path
    else:
        return path_with_lang


def determine_if_just_html_start_page(components):
    return all(
        [
            (c["type"].casefold() == "para" or c["type"].casefold() == "html")
            for c in components
        ]
    )


def remove_lowest_in_hierarchy(number_str: str):
    result = ""

    last_dot_idx = number_str.rfind(".")
    result = number_str[:last_dot_idx]

    return result


def increment_lowest_in_hierarchy(number_str: str):
    result = ""
    split_by_dots = number_str.split(".")
    if not split_by_dots[-1]:
        split_by_dots.pop()
    to_inc = int(split_by_dots[-1])
    split_by_dots.pop()
    to_inc += 1
    if split_by_dots:
        result = (".").join(split_by_dots)
        result += "."
    result += f"{to_inc}"
    return result


def strip_leading_numbers(text):
    result = text
    for char in text:
        if char == " ":
            break
        if char.isdigit() or char == ".":
            result = result[1:]  # strip this character
    return result.strip()

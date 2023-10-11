# import copy
# import json
import os

# from bs4 import BeautifulSoup


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


# def build_display_for_components(components):
#     results = []
#     for c in components:

#         text = []
#         if ("type" in c) and (
#             c["type"].casefold() == "html" or c["type"].casefold() == "para"
#         ):
#             text = [c["content"]]
#         elif "hint" in c:
#             soup = BeautifulSoup(c["hint"], "html.parser")
#             text = [e.text for e in soup.children]
#         component = {
#             "title": c["title"] if "title" in c else None,
#             "text": text,
#             "hide_title": c["options"]["hideTitle"]
#             if "hideTitle" in c["options"]
#             else False,
#         }

#         results.append(component)
#     return results


# def build_page_display(is_first_page, page):
#     results = {}
#     if is_first_page:
#         # Several forms start with a page full of guidance text, which we don't need to include here
#         is_just_html_start_page = determine_if_just_html_start_page(page["components"])
#         if is_just_html_start_page:
#             results["page_title"] = strip_leading_numbers(page["title"])
#             results["page_children"] = []
#             return results

#     results["page_title"] = page["title"]
#     results["page_children"] = build_display_for_components(page["components"])
#     return results


# def build_display_for_form(form_data: dict):

#     page_index = build_page_index(form_data)

#     display_index = {}
#     for idx, page in page_index.items():
#         display_index[idx] = build_page_display(
#             is_first_page=(str(idx) == "1"), page=page["page"]
#         )

#     return display_index


# def build_form(form_name: str, path_to_forms: str):
#     path_to_form = os.path.join(path_to_forms, f"{form_name}.json")
#     with open(path_to_form, "r") as f:
#         form_data = json.load(f)

#     return build_display_for_form(form_data)

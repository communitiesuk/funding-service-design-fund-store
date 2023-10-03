import json
import os


def evaluate_page(page, index, all_pages, results):
    next_page_path = page["next"][0]["path"]
    results[index] = page
    if next_page_path != "/summary":
        next_page = next(p for p in all_pages if p["path"] == next_page_path)
        evaluate_page(next_page, index + 1, all_pages, results)


def build_page_index(form_data):
    start_page = form_data["startPage"]
    first_page = next(p for p in form_data["pages"] if p["path"] == start_page)

    page_index = {}
    index = 1

    evaluate_page(
        page=first_page, index=index, all_pages=form_data["pages"], results=page_index
    )
    return page_index


def strip_leading_numbers(text):
    result = text
    for char in text:
        if char == " ":
            break
        if char.isdigit() or char == ".":
            result = result[1:]  # strip this character
    return result.strip()


def build_display_for_components(components):
    pass


def build_page_display(is_first_page, page):
    results = {}
    if is_first_page:
        is_just_html_start_page = all(
            [
                (c["type"].casefold() == "para" or c["type"].casefold() == "html")
                for c in page["components"]
            ]
        )
        if is_just_html_start_page:
            results["page_title"] = strip_leading_numbers(page["title"])
            results["page_children"] = []
            return results

    results["page_title"] = page["title"]
    results["page_children"] = build_display_for_components(page["components"])
    return results


def build_display_for_form(form_data: dict):

    page_index = build_page_index(form_data)

    display_index = {}
    for idx, page in page_index.items():
        display_index[idx] = build_page_display(is_first_page=(idx == 1), page=page)

    return display_index


def build_form(form_name: str, path_to_forms: str):
    path_to_form = os.path.join(path_to_forms, f"{form_name}.json")
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    return build_display_for_form(form_data)

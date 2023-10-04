import copy
import json
import os

from bs4 import BeautifulSoup


def get_all_child_nexts(page, child_nexts, all_pages):
    child_nexts.extend([n["path"] for n in page["next"]])
    for next_page_config in page["next"]:
        next_page = next(p for p in all_pages if p["path"] == next_page_config["path"])
        get_all_child_nexts(next_page, child_nexts, all_pages)


def find_highest_position_in_hierarchy(
    all_pages, page, results, parent_nexts: list, current_level, is_root, siblings
):
    if not is_root:
        if page["path"] in results.keys():
            existing_level_in_results = results[page["path"]]
            if current_level < existing_level_in_results:
                results[page["path"]] = current_level

        else:
            results[page["path"]] = current_level
    else:
        results[page["path"]] = current_level

    next_from_this_page = page["next"]

    for next_page_config in next_from_this_page:
        next_page_path = next_page_config["path"]
        # if this next page is also a next page from somewhere above this page in the hierarchy, skip it
        if next_page_path in parent_nexts:
            continue
        next_page = next(p for p in all_pages if p["path"] == next_page_path)

        # all the other options for next, that are siblings to this next page
        siblings_to_this_next_page = [
            n["path"] for n in next_from_this_page if n["path"] != next_page_path
        ]

        # add this layer of siblings to the all_parents list so that the next level down gets the right set
        all_parent_nexts = copy.copy(parent_nexts)
        all_parent_nexts.extend(siblings_to_this_next_page)

        # Get every child of every sibling to this next page
        all_child_nexts = []
        for sibling_page in [
            sp for sp in all_pages if sp["path"] in siblings_to_this_next_page
        ]:
            get_all_child_nexts(sibling_page, all_child_nexts, all_pages)

        # get every child of every sibling to the parent page
        all_cousins_children = []
        for sibling_page in [sp for sp in all_pages if sp["path"] in siblings]:
            get_all_child_nexts(sibling_page, all_cousins_children, all_pages)

        if next_page_path in all_child_nexts:
            next_level = current_level
        elif len(next_from_this_page) == 1 and next_page_path in all_cousins_children:
            next_level = current_level
        elif next_page_path in all_cousins_children:
            next_level = current_level - 1
        elif len(next_from_this_page) == 1:
            next_level = current_level
        else:
            next_level = current_level + 1

        find_highest_position_in_hierarchy(
            all_pages,
            next_page,
            results,
            all_parent_nexts,
            next_level,
            is_root=False,
            siblings=siblings_to_this_next_page,
        )


def build_hierarchy(form_data):
    results = {}
    all_pages = form_data["pages"]
    start_page = form_data["startPage"]
    first_page = next(p for p in form_data["pages"] if p["path"] == start_page)
    find_highest_position_in_hierarchy(
        all_pages=all_pages,
        page=first_page,
        results=results,
        parent_nexts=[],
        is_root=True,
        current_level=1,
        siblings=[],
    )
    return results
    # for page in form_data["pages"]:
    #     idx = 1


def determine_if_just_html_start_page(components):
    return all(
        [
            (c["type"].casefold() == "para" or c["type"].casefold() == "html")
            for c in components
        ]
    )


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


def evaluate_page(
    paths_to_do: list,
    conditions,
    page,
    index,
    all_pages,
    results,
    parent_paths,
    is_sub_page=False,
    is_sub_sub_page=False,
):
    if page["path"] in parent_paths:
        return
    results[index] = {"page": page}
    paths_to_do.remove(page["path"])
    if len(page["next"]) == 1:
        for next_page_config in page["next"]:
            next_page_path = next_page_config["path"]
            if is_sub_page and next_page_path in parent_paths:
                continue
            if next_page_path in paths_to_do and next_page_path != "/summary":
                next_page = next(p for p in all_pages if p["path"] == next_page_path)
                if determine_if_just_html_start_page(page["components"]):
                    new_index = f"{index}.0"
                else:
                    new_index = str(index)
                evaluate_page(
                    paths_to_do,
                    conditions,
                    next_page,
                    increment_lowest_in_hierarchy(new_index),
                    all_pages,
                    results,
                    parent_paths=[],
                    is_sub_page=False,
                )
    else:
        sub_page_idx = f"{index}.0"
        for next_page_config in page["next"]:
            if next_page_config["path"] in paths_to_do:
                # condition = next(c for c in conditions if c["name"] == next_page_config["name"])
                next_page = next(
                    p for p in all_pages if p["path"] == next_page_config["path"]
                )
                if is_sub_page:
                    this_parent_paths = parent_paths
                else:
                    this_parent_paths = [
                        p["path"]
                        for p in page["next"]
                        if p["path"] != next_page_config["path"]
                    ]
                sub_page_idx = increment_lowest_in_hierarchy(str(sub_page_idx))
                evaluate_page(
                    paths_to_do,
                    conditions,
                    next_page,
                    sub_page_idx,
                    all_pages,
                    results,
                    parent_paths=this_parent_paths,
                    is_sub_page=True,
                    is_sub_sub_page=is_sub_page,
                )


def build_page_index(form_data):
    start_page = form_data["startPage"]
    first_page = next(p for p in form_data["pages"] if p["path"] == start_page)

    page_index = {}
    index = "1"

    paths_to_pages = {page["path"]: page for page in form_data["pages"]}

    evaluate_page(
        paths_to_do=list(paths_to_pages.keys()),
        conditions=form_data["conditions"],
        page=first_page,
        index=index,
        all_pages=form_data["pages"],
        results=page_index,
        parent_paths=[],
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
    results = []
    for c in components:

        text = []
        if ("type" in c) and (
            c["type"].casefold() == "html" or c["type"].casefold() == "para"
        ):
            text = [c["content"]]
        elif "hint" in c:
            soup = BeautifulSoup(c["hint"], "html.parser")
            text = [e.text for e in soup.children]
        component = {
            "title": c["title"] if "title" in c else None,
            "text": text,
            "hide_title": c["options"]["hideTitle"]
            if "hideTitle" in c["options"]
            else False,
        }

        results.append(component)
    return results


def build_page_display(is_first_page, page):
    results = {}
    if is_first_page:
        # Several forms start with a page full of guidance text, which we don't need to include here
        is_just_html_start_page = determine_if_just_html_start_page(page["components"])
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
        display_index[idx] = build_page_display(
            is_first_page=(str(idx) == "1"), page=page["page"]
        )

    return display_index


def build_form(form_name: str, path_to_forms: str):
    path_to_form = os.path.join(path_to_forms, f"{form_name}.json")
    with open(path_to_form, "r") as f:
        form_data = json.load(f)

    return build_display_for_form(form_data)

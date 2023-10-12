import copy
import json
import os

from bs4 import BeautifulSoup
from bs4 import NavigableString
from db.models.section import Section
from scripts.all_questions.read_forms import determine_display_value_for_condition
from scripts.all_questions.read_forms import determine_if_just_html_start_page
from scripts.all_questions.read_forms import increment_lowest_in_hierarchy
from scripts.all_questions.read_forms import remove_lowest_in_hierarchy
from scripts.all_questions.read_forms import strip_leading_numbers


def get_all_child_nexts(page, child_nexts, all_pages):
    child_nexts.update([n for n in page["next_paths"]])
    for next_page_path in page["next_paths"]:
        next_page = next(p for p in all_pages if p["path"] == next_page_path)
        get_all_child_nexts(next_page, child_nexts, all_pages)


def get_all_possible_previous(page_path, results, all_pages):

    direct_prev = [
        prev["path"] for prev in all_pages if page_path in prev["next_paths"]
    ]
    results.update(direct_prev)
    for prev in direct_prev:
        get_all_possible_previous(prev, results, all_pages)


def generate_metadata(full_form_data):

    cutdown = {"start_page": full_form_data["startPage"], "all_pages": []}
    for page in full_form_data["pages"]:
        cp = {"path": page["path"], "next_paths": [p["path"] for p in page["next"]]}
        cutdown["all_pages"].append(cp)

    metadata = copy.deepcopy(cutdown)
    for p in metadata["all_pages"]:
        # everything that could come immediately before this page
        p["all_direct_previous"] = [
            prev["path"]
            for prev in cutdown["all_pages"]
            if p["path"] in prev["next_paths"]
        ]

        # all the immediate next paths of the direct previous (aka siblings)
        direct_next_of_direct_previous = set()
        for direct_prev in p["all_direct_previous"]:
            prev_page = next(
                prev for prev in cutdown["all_pages"] if prev["path"] == direct_prev
            )
            direct_next_of_direct_previous.update(prev_page["next_paths"])
        p["direct_next_of_direct_previous"] = list(direct_next_of_direct_previous)

        # get all the descendents (possible next anywhere after) of the siblings
        all_possible_next_of_siblings = set()
        for sibling in p["direct_next_of_direct_previous"]:
            sibling_page = next(
                page for page in cutdown["all_pages"] if page["path"] == sibling
            )
            get_all_child_nexts(
                sibling_page, all_possible_next_of_siblings, cutdown["all_pages"]
            )
        p["all_possible_next_of_siblings"] = list(all_possible_next_of_siblings)

        # everything that could come anywhere before this page
        all_possible_previous = set()
        get_all_possible_previous(
            p["path"], all_possible_previous, cutdown["all_pages"]
        )
        p["all_possible_previous"] = list(all_possible_previous)

        # get everything that is directly after all the possible previos to this page
        all_possible_previous_direct_next = set()
        for prev in p["all_possible_previous"]:
            prev_page = next(
                page for page in cutdown["all_pages"] if page["path"] == prev
            )
            all_possible_previous_direct_next.update(prev_page["next_paths"])
        p["all_possible_previous_direct_next"] = list(all_possible_previous_direct_next)

        # everything that could come after this page
        all_possible_after = set()
        get_all_child_nexts(
            page=p, child_nexts=all_possible_after, all_pages=cutdown["all_pages"]
        )
        p["all_possible_after"] = list(all_possible_after)

    return metadata


def generate_index(page, results: dict, idx, all_pages, start_page=False):
    current_level_in_results = results.get(page["path"], 9999)
    if idx < current_level_in_results:
        results[page["path"]] = idx

    for next_path in [n for n in page["next_paths"]]:
        # default is same level
        next_idx = idx
        next_page = next(p for p in all_pages if p["path"] == next_path)

        # if we have more than one possible next page, go to next level
        if len(page["next_paths"]) > 1 or start_page is True:
            next_idx = idx + 1

        # if this next path is also a next path of the immediate previous, go back a level
        elif next_path in page["direct_next_of_direct_previous"]:
            next_idx = idx - 1

        elif next_path in page["all_possible_previous_direct_next"]:
            next_idx = idx - 1

        # if this page and all it's siblings eventually go back to this same next page, go back a level
        elif (
            len(page["direct_next_of_direct_previous"]) <= 1
        ):  # and page["direct_next_of_direct_previous"][0] == page["path"]:
            pass
        elif len(next_page["all_direct_previous"]) == 1:
            pass
        else:
            is_in_descendents_of_all_siblings = True
            for sibling in page["direct_next_of_direct_previous"]:
                # don't look at this page
                if sibling == page["path"]:
                    continue
                sibling_page = next(p for p in all_pages if p["path"] == sibling)
                if next_path not in sibling_page["all_possible_after"]:
                    is_in_descendents_of_all_siblings = False

            if is_in_descendents_of_all_siblings:
                next_idx = idx - 1

        generate_index(next_page, results, next_idx, all_pages)


def strip_string_and_append_if_not_empty(string_to_check: str, list_to_append: list):
    """Uses `str.strip()` to remove leading/trailing whitespace from `string_to_check`.
    If the resulting string is not empty, appends this to `list_to_append`

    Args:
        string_to_check (str): String to strip and append
        list_to_append (list): List to append to
    """
    stripped = string_to_check.strip()
    if stripped:
        list_to_append.append(stripped)


def extract_from_html(soup, results: list):
    """
    Takes in a BeautifulSoup element, recursively iterates through it's children to generate text items
    for rendering in the all questions page.

    Any non-empty strings are stripped of leading/trailing spaces etc and appended to `results`.
    Any <ul> elements have their child <li> elements put into a separate list and that list is appended to `results`

    Args:
        soup (_type_): HTML to extract from
        results (list): results to append to
    """
    for element in soup.children:
        # If it's just a string, append that text
        if isinstance(element, NavigableString):
            strip_string_and_append_if_not_empty(element.text, results)
            continue

        # If it's a list, append the list items as another list
        if element.name == "ul":
            bullets = []
            for li in element.children:
                strip_string_and_append_if_not_empty(li.text, bullets)
            results.append(bullets)
            continue

        extract_from_html(element, results)


def build_components_from_page(
    full_page_json,
    include_html_components=True,
    form_lists=[],
    page_metadata={},
    form_conditions=[],
    index_of_printed_headers={},
):
    components_with_conditions = []
    for condition in form_conditions:
        components_with_conditions.extend(
            [value["field"]["name"] for value in condition["value"]["conditions"]]
        )

    components = []
    for c in full_page_json["components"]:
        text = []
        # skip details, eg about-your-org-cyp GNpQfE
        if c["type"].casefold() == "details":
            continue

        # Skip pages that are just html, eg about-your-org-cyp uLwBuz
        if (
            include_html_components
            and ("type" in c)
            and (c["type"].casefold() == "html" or c["type"].casefold() == "para")
        ):
            text = [c["content"]]
        elif "hint" in c:
            soup = BeautifulSoup(c["hint"], "html.parser")
            text = []
            extract_from_html(soup, text)

        if "list" in c:
            # include available options for lists
            list_id = c["list"]
            list_items = next(
                list["items"] for list in form_lists if list["name"] == list_id
            )
            list_display = [item["text"] for item in list_items]
            text.append(list_display)

        # If there are multiple options for the next page, include text about where to go next
        if c["name"] in components_with_conditions:  # len(full_page_json["next"]) > 1:

            # possible alternative approach if in fact not all conditions are meant to be listed
            # for condition in form_conditions:
            #     if c["name"] in [value["field"]["name"] for value in condition["value"]["conditions"]]:

            for next_config in full_page_json["next"]:
                if "condition" in next_config and next_config["path"] != "/summary":
                    condition_name = next_config["condition"]
                    condition_config = next(
                        fc for fc in form_conditions if fc["name"] == condition_name
                    )
                    destination = index_of_printed_headers[next_config["path"]][
                        "heading_number"
                    ]
                    # TODO use next to get correct condition instead of 0, use field name
                    condition_text = determine_display_value_for_condition(
                        condition_config["value"]["conditions"][0]["value"]["value"],
                        list_name=c["list"] if "list" in c else None,
                        form_lists=form_lists,
                    )
                    text.append(
                        f"If '{condition_text}', go to <strong>{destination}</strong>"
                    )

        component = {
            "title": c["title"] if "title" in c else None,
            "text": text,
            "hide_title": c["options"]["hideTitle"]
            if "hideTitle" in c["options"]
            else False,
        }
        components.append(component)
    return components


def generate_print_headings_for_page(
    page,
    form_metadata,
    this_idx,
    form_json_page,
    page_index,
    parent_hierarchy_level,
    pages_to_do,
    is_form_heading,
    place_in_siblings_list,
    index_of_printed_headers,
    form_lists,
):
    page_path = page["path"]
    # If we've already done this page, don't do it again
    if page_path not in pages_to_do:
        return

    title = strip_leading_numbers(form_json_page["title"])

    level_in_hrch = page_index[page_path]
    hierarchy_difference = level_in_hrch - parent_hierarchy_level

    # If we are going up a level in the hierarchy, and this isn't the last branch
    # that goes there, don't do it yet
    all_siblings = set(
        prev for prev in page["direct_next_of_direct_previous"] if prev != page_path
    )
    if pages_to_do.intersection(all_siblings) and hierarchy_difference < 0:
        return

    if (
        pages_to_do.intersection(page["all_direct_previous"])
        and hierarchy_difference < 0
    ):
        return

    base_heading_number = this_idx
    if not is_form_heading:
        if hierarchy_difference < 0:
            # go back a level
            base_heading_number = remove_lowest_in_hierarchy(base_heading_number)
        elif hierarchy_difference > 0:
            # increase level
            base_heading_number = f"{this_idx}.{place_in_siblings_list}"

    new_heading_number = increment_lowest_in_hierarchy(base_heading_number)

    index_of_printed_headers[page_path] = {
        "heading_number": new_heading_number,
        "is_form_heading": is_form_heading,
        "title": title,
        # "components": component_display,
    }
    pages_to_do.remove(page_path)

    sibling_tracker = 0
    for next_page_path in page["next_paths"]:
        next_page = next(
            p for p in form_metadata["all_pages"] if p["path"] == next_page_path
        )
        next_form_json_page = next(
            p
            for p in form_metadata["full_json"]["pages"]
            if p["path"] == next_page_path
        )
        generate_print_headings_for_page(
            page=next_page,
            form_metadata=form_metadata,
            this_idx=new_heading_number,
            form_json_page=next_form_json_page,
            page_index=page_index,
            parent_hierarchy_level=level_in_hrch,
            pages_to_do=pages_to_do,
            is_form_heading=False,
            place_in_siblings_list=sibling_tracker,
            index_of_printed_headers=index_of_printed_headers,
            form_lists=form_lists,
        )
        sibling_tracker += 1


def generate_print_headers_for_form(section_idx: int, form_metadata, form_idx):
    pages_to_do = set(
        p["path"] for p in form_metadata["all_pages"] if p["path"] != "/summary"
    )
    start_page_path = form_metadata["start_page"]
    index = form_metadata["index"]
    index_of_printed_headers = {}
    start_page = next(
        p for p in form_metadata["all_pages"] if p["path"] == start_page_path
    )
    form_json_page = next(
        p for p in form_metadata["full_json"]["pages"] if p["path"] == start_page_path
    )

    current_hierarchy_level = 0
    generate_print_headings_for_page(
        start_page,
        form_metadata,
        this_idx=f"{section_idx}.{form_idx}",
        form_json_page=form_json_page,
        page_index=index,
        parent_hierarchy_level=current_hierarchy_level,
        pages_to_do=pages_to_do,
        is_form_heading=True,
        place_in_siblings_list=0,
        index_of_printed_headers=index_of_printed_headers,
        form_lists=form_metadata["full_json"]["lists"],
    )
    for page_path in index_of_printed_headers.keys():
        full_json_page = next(
            p for p in form_metadata["full_json"]["pages"] if p["path"] == page_path
        )
        component_display = build_components_from_page(
            full_page_json=full_json_page,
            include_html_components=(
                not determine_if_just_html_start_page(full_json_page["components"])
            ),
            form_lists=form_metadata["full_json"]["lists"],
            page_metadata=next(
                p for p in form_metadata["all_pages"] if p["path"] == page_path
            ),
            form_conditions=form_metadata["full_json"]["conditions"],
            index_of_printed_headers=index_of_printed_headers,
        )
        index_of_printed_headers[page_path]["components"] = component_display
    return index_of_printed_headers


def build_section_header(section: Section, lang="en"):
    title = section.title_json[lang]
    title = strip_leading_numbers(title)
    anchor = title.casefold().replace(" ", "-")
    return anchor, title


def generate_section_headings(
    sections: list[Section], path_to_form_jsons: str, lang: str
):
    section_map = {}

    section_idx = 1
    for section in sections:
        anchor, text = build_section_header(section, lang=lang)
        # form_metadatas = []
        form_print_headings = {}
        form_idx = 0
        for child_form in section.children:
            form_name = child_form.form_name[0].form_name_json[lang]
            path_to_form = os.path.join(path_to_form_jsons, f"{form_name}.json")
            # Some forms live in the generic folder rather than fund-round specific
            if not os.path.exists(path_to_form):
                path_to_form = os.path.join(
                    path_to_form_jsons, "..", "generic", f"{form_name}.json"
                )
            with open(path_to_form, "r") as f:
                form_data = json.load(f)
                form_metadata = generate_metadata(form_data)
                form_index = {}

                first_page = next(
                    p
                    for p in form_metadata["all_pages"]
                    if p["path"] == form_metadata["start_page"]
                )
                generate_index(
                    page=first_page,
                    results=form_index,
                    idx=1,
                    all_pages=form_metadata["all_pages"],
                    start_page=True,
                )
                form_metadata["index"] = form_index
                form_metadata["full_json"] = form_data
                form_print_headings.update(
                    generate_print_headers_for_form(
                        section_idx=section_idx,
                        form_metadata=form_metadata,
                        form_idx=form_idx,
                    )
                )
                form_idx += 1
            # form_metadatas.append(form_metadata)
        section_map[anchor] = {
            "title_text": text,
            "form_print_headings": form_print_headings,
        }
        section_idx += 1
    return section_map

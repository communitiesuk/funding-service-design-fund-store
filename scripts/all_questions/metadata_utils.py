import copy


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

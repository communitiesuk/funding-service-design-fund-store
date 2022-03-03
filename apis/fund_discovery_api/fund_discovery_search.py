import warnings


def search(to_search: dict, words):
    warnings.warn(
        "Search function used in the fund store shouldn't be used in"
        " production",
        DeprecationWarning,
    )
    return_list = []
    word_list = words.split("-")
    for fund_data in to_search:
        for word in word_list:
            for data_point in fund_data:
                if word in fund_data[data_point]:
                    return_list.append(fund_data)
                    break
    return return_list

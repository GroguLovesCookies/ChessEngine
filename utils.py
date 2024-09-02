def any_in_list(l: list, condition):
    for item in l:
        if condition(item):
            return item

    return None
def flatten(iterable):
    rv = []
    if isinstance(iterable, (list, tuple, set)):
        for el in iterable:
            rv.extend(flatten(el))
    else:
        rv.append(iterable)
    return rv

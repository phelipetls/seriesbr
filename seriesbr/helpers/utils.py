def cat(something, sep):
    return sep.join(map(str, something)) if isiterable(something) else something


def isiterable(something):
    try:
        iter(something)
    except TypeError:
        return False
    return True

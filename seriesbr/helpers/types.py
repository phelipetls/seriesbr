def return_codes_and_names(*args):
    """
    Auxiliary function to return codes and names
    of the series.

    If it find a dictionary, it will use its keys
    as names and values as codes.

    Otherwise, it will just return the requested
    codes as names, so the column names will be
    the codes themselves.
    """
    for arg in args:
        if isinstance(arg, dict):
            return arg.values(), arg.keys()
    return args, args

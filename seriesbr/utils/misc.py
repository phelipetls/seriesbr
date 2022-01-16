from typing import Union, Any, Iterable


def parse_arguments(*args: Union[dict, int, str]):
    """
    Parse arguments into a dictionary.

    Returns
    -------
    tuple
        First element with codes and second element
        with names.

    Examples
    >>> utils.collect_args({"A": 1, "B": 2}, 100)
    {"A": 1, "B": 2, 100: 100}
    """
    d = {}
    for arg in args:
        if isinstance(arg, dict):
            d.update(arg)
        else:
            d.update({arg: arg})
    return d


def cat(something: Iterable, sep: str):
    """
    Join any iterable, except strings, by
    a custom delimiter.

    Parameters
    ----------
    something : list
        List to be joined.

    sep : str
        Delimiter.
    """
    return sep.join(map(str, something)) if is_iterable(something) else something


def is_iterable(something: Any) -> bool:
    """
    Test if it is an iterable other than
    a string.

    Returns
    -------
    bool
        True if an iterable other than str,
        False otherwise.
    """
    try:
        iter(something)
    except TypeError:
        return False
    return True and not isinstance(something, str)

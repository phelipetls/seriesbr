from typing import Union


def merge_into_dict(*args: Union[dict, int, str]) -> dict:
    """
    Parse arguments into a dictionary.

    Returns
    -------
    dict

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

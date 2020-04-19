from seriesbr.helpers.utils import quote_if_str


def contains(metadata, values, logical_operator=" or "):
    """
    Build contains operator for OData API query.

    Examples
    --------
    >>> url.contains("FNTNOME", ["A", "B"])
    "(contains('FNTNOME','A') or contains('FNTNOME','B'))"
    """

    if isinstance(values, (list, tuple)):
        filters = [f"contains({metadata},'{item}')" for item in values]
        joined_filters = logical_operator.join(filters)
        return f"({joined_filters})"

    return f"contains({metadata},'{values}')"


def equal(metadata, values, logical_operator=" or "):
    """
    Build equal operator for OData API query.

    Examples
    --------
    >>> url.equal("SERNUMERICA", [1, "A"])
    "('SERNUMERICA' eq 1 or 'SERNUMERICA', eq 'A')"
    """

    if isinstance(values, (list, tuple)):
        filters = [f"{metadata} eq {quote_if_str(item)}" for item in values]
        joined_filters = logical_operator.join(filters)
        return f"({joined_filters})"

    return f"{metadata} eq {quote_if_str(values)}"

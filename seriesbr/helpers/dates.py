import functools

from datetime import datetime
from dateutil.parser import parse

UNIX_EPOCH = datetime(1970, 1, 1)
LAST_DAY_OF_YEAR = datetime(year=datetime.today().year, month=12, day=31)

DATE_FORMATS = {
    "bcb": "%d/%m/%Y",
    "ipea": "%Y-%m-%dT00:00:00Z",
    "ibge": "%Y%m",
}

parse = functools.partial(parse, dayfirst=True)


def format_date(date, api):
    fmt = DATE_FORMATS[api]
    return date.strftime(fmt)


def parse_dates(start, end, api):
    start = parse_start_date(start, api)
    end = parse_end_date(end, api)
    return start, end


def parse_start_date(date, api):
    parsed = parse(date, default=UNIX_EPOCH) if date else UNIX_EPOCH
    return format_date(parsed, api)


def parse_end_date(date, api):
    parsed = parse(date, default=LAST_DAY_OF_YEAR) if date else datetime.today()
    return format_date(parsed, api)


def month_to_quarter(date, fmt=None):
    """
    Convert month to quarter, i.e.,
    12 -> 4, 6 -> 2, 7 -> 3 etc.

    Examples
    --------
    >>> dates.month_to_quarter(datetime(2019, 12, 1))
    datetime(2019, 4, 1, 0, 0)
    """
    if isinstance(date, str) and fmt:
        date = datetime.strptime(date, fmt)

    floor_division, remainder = divmod(date.month, 3)
    quarter = floor_division + bool(remainder)

    return date.replace(month=quarter)

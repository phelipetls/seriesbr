import datetime

year_format = ["%Y"]
month_year_format = ["%m/%y", "%m/%Y", "%M/%Y", "%b/%Y", "%b/%y", "%B/%Y", "%B/%y"]
day_month_year_format = ["%d/%m/%Y"]

slash_formats = year_format + month_year_format + day_month_year_format
dash_formats = [fmt.replace("/", "-") for fmt in slash_formats]
blank_formats = [fmt.replace("/", "") for fmt in slash_formats]

fmts = slash_formats + dash_formats + blank_formats


def parse_date(date_str, api, start=True):
    """
    Convert different dates strings to the format required by an API.

    Also, when it is an end date, if day is unspecificed,
    the day will be the last day of the month.
    Similarly, if month is not specified, the month must be 12.

    Note that the date string is assumed to start with day
    or month, to avoid ambiguity.

    Parameters
    ----------
    date_str : str
        String to be parsed.

    api : str
        Name of the api. Possible values are "ibge", "ipea" and "bcb".

    start : bool
        If it is a start date.

    Returns
    -------
    str
        Appropriate date string for a given API.

    Raises
    ------
    ValueError
        If the string could not be converted to a
        datetime.datetime object by strptime.

    Examples
    --------
    >>> dates.parse_date("012017", api="bcb")
    '01/01/2017'
    >>> dates.parse_date("01-2017", api="ipea")
    '2017-01-01T00:00:00-00:00'
    >>> dates.parse_date("01/2017", api="ibge")
    '201701'
    """
    assert isinstance(date_str, str), "You didn't give a string as a date."

    for fmt in fmts:
        try:
            date = datetime.datetime.strptime(date_str, fmt)
            if not start:
                # if an end date,
                # "2011"    -> "31-12-2011"
                # "01-2011" -> "31-01-2011"
                # "02-01-2011" -> "02-01-2011"
                date = date.replace(
                    month=12 if fmt in year_format else date.month,
                    day=last_day_of_month(date) if fmt.find("%d") == -1 else date.day,
                )
            return date_format(date, api)
        except ValueError:
            continue

    raise ValueError("Not a valid date format.")


def parse_dates(start, end, api):
    """
    Call date parsers.

    Returns
    -------
    str
        Date format as required by an API.
    """
    if start:
        start = parse_date(start, api, start=True)
    else:
        start = date_format(get_old_date(), api)

    if end:
        end = parse_date(end, api, start=False)
    else:
        end = date_format(get_today_date(), api)

    return start, end


def date_format(date, api):
    """
    Convert datetime.datetime object to string
    compatible with a given API.
    """
    if api == "ipea":
        return date.strftime("%Y-%m-%dT00:00:00") + "-00:00"
    if api == "bcb":
        return date.strftime("%d/%m/%Y")
    if api == "ibge":
        return date.strftime("%Y%m")


def last_day_of_month(date):
    """
    Return the last day of the month.

    See: https://stackoverflow.com/questions/42950/get-last-day-of-the-month
    """
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return (next_month - datetime.timedelta(days=next_month.day)).day


def get_old_date():
    """Return an arbitrary old date 01/01/1900."""
    return datetime.datetime(1900, 1, 1)


def get_today_date():
    """Return today's date."""
    return datetime.datetime.today()


def month_to_quarter(date, fmt=None):
    """
    Convert month to quarter, i.e.,
    12 -> 4, 6 -> 2, 7 -> 3 etc.

    Examples
    --------
    >>> dates.month_to_quarter(datetime.datetime(2019, 12, 1))
    datetime.datetime(2019, 4, 1, 0, 0)
    """
    if isinstance(date, str) and fmt:
        date = datetime.datetime.strptime(date, fmt)

    floor_division, remainder = divmod(date.month, 3)
    quarter = floor_division + bool(remainder)

    return date.replace(month=quarter)

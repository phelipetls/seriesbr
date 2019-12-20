import datetime

year_format = ["%Y"]
month_year_format = ["%m/%y", "%m/%Y", "%M/%Y", "%b/%Y", "%b/%y", "%B/%Y", "%B/%y"]
day_month_year_format = ["%d/%m/%Y"]

slash_formats = year_format + month_year_format + day_month_year_format
dash_formats = [fmt.replace("/", "-") for fmt in slash_formats]
blank_formats = [fmt.replace("/", "") for fmt in slash_formats]

allowed_fmts = slash_formats + dash_formats + blank_formats


def parse_date(date, api, start=True):
    """
    Auxiliary function to convert different dates formats
    to the required API format.

    Also, when it is an end date, if day is unspecificed,
    the day will be the last day of the month.
    Similarly, if month is not specified, the month must be 12.
    """
    assert isinstance(date, str), "You didn't give a string as a date."
    for fmt in allowed_fmts:
        try:
            if start:
                date_object = datetime.datetime.strptime(date, fmt)
            else:
                # if an end date,
                # "2011"    -> "31-12-2011"
                # "01-2011" -> "31-01-2011"
                # "02-01-2011" -> "02-01-2011"
                date = datetime.datetime.strptime(date, fmt)
                date_object = date.replace(
                    month=12 if fmt in year_format else date.month,
                    day=last_day_of_month(date) if fmt.find("%d") == -1 else date.day,
                )
            return api_date_format_of(date_object, api)
        except ValueError:
            continue
    raise ValueError("Not a valid date format.")


def parse_dates(start, end, api):
    """
    Auxiliary function to handle dates.

    Returns
    -------
    str
        Date format as required by an API.
    """
    if start:
        start = parse_date(start, api, start=True)
    else:
        start = api_date_format_of(very_old_date(), api)
    if end:
        end = parse_date(end, api, start=False)
    else:
        end = api_date_format_of(today_date(), api)
    return start, end


def api_date_format_of(date, api):
    """
    Auxiliary function to convert datetime.datetime
    object to string compatible with a given API.
    """
    if api == "ipeadata":
        return date.strftime("%Y-%m-%dT00:00:00") + "-00:00"  # 01-12-2010T00:00:00-00:00
    if api == "bcb":
        return date.strftime("%d/%m/%Y")  # 01/12/2010
    if api == "ibge":
        return date.strftime("%Y%m")  # 201901


def last_day_of_month(date):
    """
    Auxiliary function that returns the last day of the month,
    if no day is specified.

    See: https://stackoverflow.com/questions/42950/get-last-day-of-the-month
    """
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return (next_month - datetime.timedelta(days=next_month.day)).day


def very_old_date():
    """
    Returns very old date (01/01/1900).

    Returns
    -------
    datetime.datetime
    """
    return datetime.datetime(1900, 1, 1)


def today_date():
    """
    Returns today's date.

    Returns
    -------
    datetime.datetime
    """
    return datetime.datetime.today()


def month_to_quarter(date):
    """
    Convert month to quarter, i.e.,
    12 -> 4, 6 -> 2, 7 -> 3 etc.

    Parameters
    ----------
    date : datetime.datetime

    Returns
    -------
    datetime.datetime

    Examples
    --------
        >>> dates.month_to_quarter(datetime.datetime(2019, 12, 1))
        datetime.datetime(2019, 4, 1, 0, 0)
    """
    quarter = divmod(date.month, 3)[0] + bool(divmod(date.month, 3)[1])
    return date.replace(month=quarter)


def check_if_quarter(dates):
    """
    Check if month of a datetime
    object is less than 4, i.e., if
    it is a quarter.
    """
    months = [
        datetime.datetime.strptime(dt, "%Y%m").month for dt in dates if dt is not None
    ]
    return all([month <= 4 for month in months])

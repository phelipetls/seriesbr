import datetime

year_format = ["%Y"]
month_year_format = ["%m/%y", "%m/%Y", "%M/%Y"]
day_month_year_format = ["%d/%m/%Y"]

slash_formats = day_month_year_format + year_format + month_year_format
dash_formats = [fmt.replace("/", "-") for fmt in slash_formats]
blank_formats = [fmt.replace("/", "") for fmt in slash_formats]

allowed_fmts = slash_formats + dash_formats + blank_formats


def parse_date(date, api, start=True):
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
            return api_date_format_of(date_object, api)  # handle different api date formats
        except ValueError:
            continue
    raise ValueError("Not a valid date format.")


def parse_dates(start, end, api):
    """
    Auxiliary function to convert different date formats
    to %d/%m/%Y, which is required by the SGS API.
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
    if api == "ipeadata":
        utc_offset = get_utc_offset()
        return date.strftime("%Y-%m-%dT00:00:00") + utc_offset  # 01-12-2010T00:00:00-03:00
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


def get_utc_offset():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()[-6:]


def very_old_date():
    return datetime.datetime(1900, 1, 1)


def today_date():
    return datetime.datetime.today()

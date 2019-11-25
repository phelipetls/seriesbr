from datetime import datetime, timezone, timedelta

default = ["%d/%m/%Y"]
year_only = ["%Y", "%y"]
month_year_only = ["%m/%y", "%m/%Y", "%M/%Y", "%b/%Y", "%B/%y"]

all_formats = default + year_only + month_year_only
slash_formats = [fmt for fmt in all_formats]
dash_formats = [fmt.replace("/", "-") for fmt in all_formats]
blank_formats = [fmt.replace("/", "") for fmt in all_formats]

possible_fmts = slash_formats + dash_formats + blank_formats


def parse_date(date, api, start=True):
    assert isinstance(date, str), "You didn't give a string as a date."
    for fmt in possible_fmts:
        try:
            if start:
                date_object = datetime.strptime(date, fmt)
            else:
                # if an end date,
                # "2011"    -> "31-12-2011"
                # "01-2011" -> "31-01-2011"
                date = datetime.strptime(date, fmt)
                date_object = date.replace(
                    month=12 if fmt in year_only else date.month,
                    day=last_day_of_month(date) if fmt.find("%d") == -1 else date.day
                )
            return format_for_api(date_object, api)  # handle different api conversion
        except ValueError:
            continue
    raise ValueError


def parse_dates(start, end, api):
    """
    Auxiliary function to convert different date formats
    to %d/%m/%Y, which is required by the SGS API.
    """
    start = parse_date(start, api, start=True) if start else ""
    end = parse_date(end, api, start=False) if end else ""
    return start, end


def format_for_api(date, api):
    if api == "ipeadata":
        utc_offset = datetime.now(timezone.utc).astimezone().isoformat()[-6:]
        return date.strftime("%Y-%m-%dT00:00:00") + utc_offset  # 01-12-2010T00:00:00-03:00
    if api == "bcb":
        return date.strftime("%d/%m/%Y")  # 01/12/2010


def last_day_of_month(date):
    """
    Auxiliary function that returns the last day of the month,
    if no day is specified.

    See: https://stackoverflow.com/questions/42950/get-last-day-of-the-month
    """
    next_month = date.replace(day=28) + timedelta(days=4)
    return (next_month - timedelta(days=next_month.day)).day

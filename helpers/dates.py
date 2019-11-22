import datetime as dt

default = ["%d/%m/%Y"]
year_only = ["%Y", "%y"]
month_year_only = ["%m/%y", "%M/%Y", "%b/%Y", "%B/%y"]

all_formats = default + year_only + month_year_only
slash_formats = [fmt for fmt in all_formats]
dash_formats = [fmt.replace("/", "-") for fmt in all_formats]
blank_formats = [fmt.replace("/", "") for fmt in all_formats]


def parse_date(date, start=True):
    possible_fmts = slash_formats + dash_formats + blank_formats
    for fmt in possible_fmts:
        try:
            if start:
                parsed_date = dt.datetime.strptime(date, fmt)
            else:
                date = dt.datetime.strptime(date, fmt)
                parsed_date = date.replace(
                    month=12 if fmt in year_only else date.month,
                    day=last_day_of_month(date) if fmt.find("%d") == -1 else date.day
                )
            return parsed_date.strftime("%d/%m/%Y")
        except ValueError:
            continue
    raise ValueError


def last_day_of_month(date):
    """
    Auxiliary function that returns the last day of the month,
    if no day is specified.

    See: https://stackoverflow.com/questions/42950/get-last-day-of-the-month
    """
    next_month = date.replace(day=28) + dt.timedelta(days=4)
    return (next_month - dt.timedelta(days=next_month.day)).day

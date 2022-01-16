from datetime import datetime
from dateutil.parser import parse

UNIX_EPOCH = datetime(1970, 1, 1)
TODAY = datetime.today()
LAST_DAY_OF_YEAR = datetime(year=datetime.today().year, month=12, day=31)


def parse_start_date(date: str) -> datetime:
    return parse(date, default=UNIX_EPOCH)


def parse_end_date(date: str) -> datetime:
    return parse(date, default=LAST_DAY_OF_YEAR)

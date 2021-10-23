from uuid import uuid4
from pathlib import Path
import datetime

def get_uuid(short: bool = False) -> str:
    """ Wrap the ugly call to get a UUID string """
    uuid = str(uuid4())
    if short:
        return uuid[:8]
    else:
        return uuid

def get_year_fraction(date: datetime.datetime):
    start = datetime.date(date.year, 1, 1).toordinal()
    year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
    return date.year + float(date.toordinal() - start) / year_length


def get_date_range(file: Path, sep: str = " ", datefmt: bool = False):
    """ Date range and delta from date file (name and float) """
    with file.open('r') as fin:
        dates = [
            line.strip().split(sep)[1] for line in fin
        ]
        if datefmt:
            dates = [get_year_fraction(datetime.datetime.strptime(date, "%d/%m/%Y")) for date in dates]
        else:
            dates = [float(date) for date in dates]

    min_date, max_date = min(dates), max(dates)
    delta = max_date - min_date
    return max_date, min_date, delta
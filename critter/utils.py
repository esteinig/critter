from uuid import uuid4
from pathlib import Path
import datetime
from collections import Counter


NULL = ['-', 'none', 'null', 'missing', 'na', 'NA']


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

    counts = Counter(dates)

    min_date, max_date = min(dates), max(dates)
    delta = max_date - min_date
    return max_date, min_date, delta, counts


def get_float_dates(dates: dict) -> dict:

    return {
        name: get_year_fraction(
            datetime.datetime.strptime(date, "%d/%m/%Y")
        ) for name, date in dates.items()
    }


def read_dates(date_file: Path) -> dict:

    # Names always in column 1, dates always in column 2, no header
    with date_file.open("r") as date_file_input:
        dates = {
            line.strip().split()[0]: line.strip().split()[1] 
            for line in date_file_input
        } # name - date
    
    return dates


def dates_from_fasta(fasta: Path, date_file: Path, id_sep: str = "|", date_idx: int = 2,  datefmt: bool = False):

    with fasta.open("r") as fa_file, date_file.open("w") as da_file:
        for line in fa_file:
            if line.startswith(">"):
                content = line.strip().split(" ")
                identifier = content[0]
                data = identifier.split(id_sep)
                try:
                    seq_date = data[date_idx]  # not first usually
                except IndexError:
                    raise IndexError("Could not extract sequence name from sequence identifier")

                if datefmt:
                    date = get_year_fraction(datetime.datetime.strptime(seq_date, "%d/%m/%Y"))
                else:
                    date = float(seq_date)

                seq_name = identifier.replace(">", "")
                da_file.write(f"{seq_name}\t{date}\n")

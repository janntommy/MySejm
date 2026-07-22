import time

from api import get_data_format, get_voting
from saver import get_file_name, save


def download_json(year: int, month: int, term=10) -> None:
    try:
        date_from, date_to = get_data_format(year, month)
        voting_data = get_voting(term, date_from, date_to)
        file_name = get_file_name(year, month)

        save(voting_data, file_name)

    except ValueError as error:
        print(f"Validation error: {year}-{month:02d}: {error}")
    except RuntimeError as error:
        print(f"SEJM API error: {year}-{month:02d}: {error}")

def main():
    dates_to_download = [(2026, 6),
                         (2026, 5),
                         (2026, 4),
                         (2026, 3),
                         (2026, 2),
                         (2026, 1)]

    term = 10

    for year, month in dates_to_download:
        download_json(year, month)
        time.sleep(1)
        print(f"succesfully downloaded {year}-{month:02d} data.")

if __name__ == "__main__":
    main()
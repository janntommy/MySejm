import calendar
from datetime import datetime

import requests

SEJM_URL = "https://api.sejm.gov.pl/sejm"


def get_data_format(year: int, month: int) -> tuple[str, str]:
    current_year = datetime.now().year
    if year < 2023 or year > (current_year + 1):
        raise ValueError(f"Invalid year - {year} is out of range. Year must be at least 2023")

    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month - month must be a number between 1 and 12: {month}")

    last_month_day = calendar.monthrange(year, month)[1]
    date_from = f"{year}-{month:02d}-01"
    date_to = f"{year}-{month:02d}-{last_month_day}"
    return date_from, date_to


def get_voting(term: int, date_from: str, date_to: str) -> str:
    if term <= 0:
        raise ValueError(f"Term must be greater than 0: {term}")

    url = f"{SEJM_URL}/term{term}/votings/search"
    try:
        response = requests.get(url, params={"dateFrom": date_from, "dateTo": date_to}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise RuntimeError(f"Error occurred while connecting to SEJM API: {err}")

    return response.text
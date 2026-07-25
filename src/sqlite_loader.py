import sqlite3
import pandas as pd
from pathlib import Path

SILVER_DIR = Path(__file__).resolve().parents[1] / "data" / "silver"
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "sejm.db"


def get_table_name(year: int, month: int) -> str:
    return f"voting_{year}_{month:02d}"


def load_csv(year: int, month: int) -> pd.DataFrame:
    csv_path = SILVER_DIR / f"voting_{year}_{month:02d}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"DB LOADER - file {csv_path} not exists")
    return pd.read_csv(csv_path)


def load_to_table(year: int, month: int) -> None:
    df = load_csv(year, month)
    table_name = get_table_name(year, month)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(table_name, conn, index=False, if_exists="replace")
        conn.execute(f'CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_pk ON "{table_name}"(term, sitting, voting_number)')
        conn.commit()

    print(f"DB LOADER - table '{table_name}' loaded {len(df)} records")


def load_all_available() -> None:
    for csv_path in sorted(SILVER_DIR.glob("voting_*.csv")):
        _, year_str, month_str = csv_path.stem.split("_")
        load_to_table(int(year_str), int(month_str))

if __name__ == "__main__":
    load_all_available()
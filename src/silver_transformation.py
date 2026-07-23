from pathlib import Path

import numpy as np
import pandas as pd

BRONZE_DIR = Path(__file__).resolve().parents[1] / "data" / "bronze"
SILVER_DIR = Path(__file__).resolve().parents[1] / "data" / "silver"

RENAMED_COL_NAMES = {
    "majorityType": "majority_type",
    "majorityVotes": "majority_votes",
    "notParticipating": "not_participating",
    "sittingDay": "sitting_day",
    "totalVoted": "total_voted",
    "votingNumber": "voting_number",
}

COLUMNS = ["abstain", "against_all", "date", "description", "kind", "majority_type", "majority_votes", "no",
           "not_participating", "present", "sitting", "sitting_day", "term", "title", "topic", "total_voted",
           "voting_number", "yes"]

NUMERIC_COLUMNS = ["yes", "no", "abstain", "against_all", "not_participating", "present", "total_voted"]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["term", "sitting", "votingNumber", "date"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["date"])

    df.rename(columns=RENAMED_COL_NAMES, inplace=True)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    for col in NUMERIC_COLUMNS:
        df[col] = df[col].fillna(0).astype(int)

    for col in ["sitting_day", "majority_votes", "term", "sitting", "voting_number"]:
        df[col] = df[col].astype("Int64" if col in ("sitting_day", "majority_votes") else int)

    df["title"] = df["title"].fillna("").str.strip()
    df["kind"] = df["kind"].fillna("UNKNOWN")

    df = df.drop_duplicates(subset=["term", "sitting", "voting_number"])
    return df[COLUMNS]

def load_to_silver(year: int, month: int) -> None:
    bronze_file = BRONZE_DIR / f"voting_{year}_{month:02d}.json"

    if not bronze_file.exists():
        raise FileNotFoundError(f"File {bronze_file} does not exist")

    df_silver = clean_data(pd.read_json(bronze_file))

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    path = SILVER_DIR / f"voting_{year}_{month:02d}.csv"
    df_silver.to_csv(path, index=False, encoding="utf-8")
    print(f"SILVER - succesfully loaded into 'voting_{year}_{month:02d}.csv'.")
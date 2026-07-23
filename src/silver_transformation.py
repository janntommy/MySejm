from pathlib import Path

import numpy as np
import pandas as pd

BRONZE_DIR = Path(__file__).resolve().parent / "data" / "bronze"
SILVER_DIR = Path(__file__).resolve().parent / "data" / "silver"

RENAMED_COL_NAMES = {
    "majorityType": "majority_type",
    "majorityVotes": "majority_votes",
    "notParticipating": "not_participating",
    "sittingDay": "sitting_day",
    "totalVoted": "total_voted",
    "votingNumber": "voting_number",
}

COLUMNS = ["abstain", "against_all", "date", "description", "kind", "pdf_link", "majority_type", "majority_votes", "no",
           "not_participating", "present", "sitting", "sitting_day", "term", "title", "topic", "total_voted",
           "voting_number", "yes"]

NUMERIC_COLUMNS = ["yes", "no", "abstain", "against_all", "not_participating", "present", "total_voted"]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["term", "sitting", "votingNumber", "date"]).copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["date"])

    df = df.rename(columns=RENAMED_COL_NAMES, inplace=True)

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
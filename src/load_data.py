import pandas as pd
from sqlalchemy import text

from database import get_engine


INPUT_FILE = "data/processed/jobs_transformed.csv"


def load_data():
    """Load transformed job data into PostgreSQL."""

    print("\n===== LOADING DATA =====")

    df = pd.read_csv(INPUT_FILE)

    print(f"Records loaded from CSV: {len(df)}")

    engine = get_engine()

    # Convert pandas NaN values to None for PostgreSQL
    df = df.where(pd.notnull(df), None)

    with engine.begin() as connection:

        # Check existing records
        result = connection.execute(
            text("SELECT COUNT(*) FROM jobs")
        )

        existing_records = result.scalar()

        print(f"Records already in database: {existing_records}")

        if existing_records > 0:
            print("Database already contains data.")
            print("Skipping load to prevent duplicate records.")
            return

        df.to_sql(
            "jobs",
            connection,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

    print(f"Successfully loaded {len(df)} records into PostgreSQL.")


if __name__ == "__main__":
    load_data()
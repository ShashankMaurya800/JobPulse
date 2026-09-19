import pandas as pd

RAW_FILE = "data/raw/indian-job-market-dataset-2025.xlsx"
PROCESSED_FILE = "data/processed/jobs_ingested.csv"


def load_job_data():
    """Load raw job data from Excel."""
    print("Loading job market dataset...")

    df = pd.read_excel(RAW_FILE)

    print(f"Loaded {len(df)} job records.")

    return df


def save_ingested_data(df):
    """Save ingested data as CSV for downstream processing."""
    df.to_csv(PROCESSED_FILE, index=False)

    print(f"Saved ingested data to: {PROCESSED_FILE}")


if __name__ == "__main__":
    df = load_job_data()

    print("\nDataset shape:")
    print(df.shape)

    save_ingested_data(df)
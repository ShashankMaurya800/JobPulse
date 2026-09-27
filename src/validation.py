import pandas as pd

from logger import setup_logger


INPUT_FILE = "data/processed/jobs_transformed.csv"


def validate_data(df):
    """Run basic data quality checks on the transformed dataset."""

    logger = setup_logger()

    print("\n===== DATA QUALITY VALIDATION =====")

    # 1. Check total records
    total_records = len(df)
    print(f"Total records: {total_records}")
    logger.info(f"Total records: {total_records}")

    # 2. Check duplicate rows
    duplicate_rows = df.duplicated().sum()
    print(f"Duplicate rows: {duplicate_rows}")
    logger.info(f"Duplicate rows: {duplicate_rows}")

    # 3. Check duplicate job IDs
    duplicate_job_ids = df["job_id"].duplicated().sum()
    print(f"Duplicate job IDs: {duplicate_job_ids}")
    logger.info(f"Duplicate job IDs: {duplicate_job_ids}")

    # 4. Check missing job IDs
    missing_job_ids = df["job_id"].isna().sum()
    print(f"Missing job IDs: {missing_job_ids}")
    logger.info(f"Missing job IDs: {missing_job_ids}")

    # 5. Check missing job titles
    missing_titles = df["title"].isna().sum()
    print(f"Missing job titles: {missing_titles}")
    logger.info(f"Missing job titles: {missing_titles}")

    # 6. Check missing company names
    missing_companies = df["company_name"].isna().sum()
    print(f"Missing company names: {missing_companies}")
    logger.info(f"Missing company names: {missing_companies}")

    # 7. Check future-start jobs
    future_jobs = (
        df["posting_status"] == "Future Start"
    ).sum()

    print(f"Future-start jobs: {future_jobs}")
    logger.info(f"Future-start jobs: {future_jobs}")

    print("\n===== VALIDATION COMPLETE =====")

    critical_checks = {
    "duplicate_rows": duplicate_rows,
    "duplicate_job_ids": duplicate_job_ids,
    "missing_job_ids": missing_job_ids,
    "missing_titles": missing_titles,
    "missing_companies": missing_companies,
   }

    if any(value > 0 for value in critical_checks.values()):
        logger.error("Data validation failed.")
        raise ValueError("Critical data quality checks failed.")

    logger.info("Data validation completed successfully.")


def main():
    """Load transformed data and run validation checks."""

    logger = setup_logger()

    logger.info("Starting data validation.")

    df = pd.read_csv(INPUT_FILE)

    validate_data(df)


if __name__ == "__main__":
    main()
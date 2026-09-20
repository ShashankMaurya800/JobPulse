import pandas as pd

INPUT_FILE = "data/processed/jobs_ingested.csv"


def load_data():
    """Load the ingested job data."""
    print("Loading ingested job data...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded {len(df)} records.")

    return df


def remove_duplicate_rows(df):
    """Remove exact duplicates and redundant duplicate job records."""

    # Step 1: Remove completely identical rows
    before = len(df)

    df = df.drop_duplicates()

    exact_duplicates_removed = before - len(df)

    print(f"\nRemoved exact duplicate rows: {exact_duplicates_removed}")

    # Step 2: Handle the known redundant duplicate job record
    duplicate_job_id = 11025022950

    matching_rows = df[df["jobId"] == duplicate_job_id]

    if len(matching_rows) > 1:
        # Keep the record with the higher ReviewsCount
        df = df.sort_values(
            "ReviewsCount",
            ascending=False
        ).drop_duplicates(
            subset=["jobId"],
            keep="first"
        )

        print(
            f"Removed redundant duplicate record for jobId "
            f"{duplicate_job_id}"
        )

    print(f"Records after duplicate removal: {len(df)}")

    return df


def analyze_duplicate_job_ids(df):
    """Analyze whether duplicate job IDs contain different information."""

    duplicate_ids = df.loc[
        df["jobId"].duplicated(keep=False),
        "jobId"
    ]

    duplicate_data = df[
        df["jobId"].isin(duplicate_ids)
    ]

    print("\n===== DUPLICATE JOB ID ANALYSIS =====")

    print(
        f"Rows with repeated job IDs: "
        f"{len(duplicate_data)}"
    )

    print(
        f"Unique job IDs appearing multiple times: "
        f"{duplicate_data['jobId'].nunique()}"
    )

    columns_to_check = [
        "title",
        "companyName",
        "location",
        "tagsAndSkills",
        "salary",
        "jobDescription"
    ]

    for column in columns_to_check:

        different_values = (
            duplicate_data.groupby("jobId")[column]
            .nunique(dropna=False)
        )

        print(
            f"{column}: "
            f"{(different_values > 1).sum()} job IDs "
            f"have different values"
        )


def inspect_duplicate_job_ids(df):
    """Display important fields for records with duplicate job IDs."""

    duplicate_ids = df.loc[
        df["jobId"].duplicated(keep=False),
        "jobId"
    ]

    duplicate_data = df[
        df["jobId"].isin(duplicate_ids)
    ].sort_values("jobId")

    columns_to_show = [
        "jobId",
        "title",
        "companyName",
        "location",
        "salary",
        "minimumSalary",
        "maximumSalary",
        "minimumExperience",
        "maximumExperience"
    ]

    print("\n===== DUPLICATE JOB ID RECORDS =====")

    print(
        duplicate_data[columns_to_show]
        .to_string(index=False)
    )

def compare_duplicate_records(df):
    """Compare records that share the same job ID."""

    duplicate_ids = df.loc[
        df["jobId"].duplicated(keep=False),
        "jobId"
    ].unique()

    print("\n===== DETAILED DUPLICATE COMPARISON =====")

    for job_id in duplicate_ids:
        records = df[df["jobId"] == job_id]

        print(f"\nJob ID: {job_id}")
        print(f"Number of records: {len(records)}")

        for column in df.columns:
            unique_values = records[column].astype(str).unique()

            if len(unique_values) > 1:
                print(f"\n{column}:")
                for value in unique_values:
                    print(f"  - {value}")

def analyze_missing_values(df):
    """Analyze missing values after duplicate removal."""

    missing_count = df.isnull().sum()

    missing_percentage = (
        missing_count / len(df) * 100
    )

    missing_summary = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage
    })

    missing_summary = missing_summary[
        missing_summary["missing_count"] > 0
    ].sort_values(
        "missing_count",
        ascending=False
    )

    print("\n===== MISSING VALUE ANALYSIS =====")

    print(missing_summary)

def inspect_experience(df):
    """Inspect experience values and compare with experience ranges."""

    print("\n===== EXPERIENCE ANALYSIS =====")

    print("\nExperience values:")
    print(df["experience"].value_counts(dropna=False).head(20))

    print("\nExperience data type:")
    print(df["experience"].dtype)

    print("\nMinimum experience statistics:")
    print(df["minimumExperience"].describe())

    print("\nMaximum experience statistics:")
    print(df["maximumExperience"].describe())   

def analyze_missing_experience(df):
    """Check whether missing experience can be recovered from numeric fields."""

    missing_experience = df[df["experience"].isna()]

    print("\n===== MISSING EXPERIENCE ANALYSIS =====")

    print(f"Rows with missing experience: {len(missing_experience)}")

    print(
        "\nRows with missing experience AND available "
        "minimumExperience:"
    )
    print(
        missing_experience["minimumExperience"]
        .notna()
        .sum()
    )

    print(
        "\nRows with missing experience AND available "
        "maximumExperience:"
    )
    print(
        missing_experience["maximumExperience"]
        .notna()
        .sum()
    )

    print("\nSample of missing experience records:")

    columns = [
        "jobId",
        "title",
        "experience",
        "minimumExperience",
        "maximumExperience"
    ]

    print(
        missing_experience[columns]
        .head(10)
        .to_string(index=False)
    )

def fill_missing_experience(df):
    """Fill missing experience using numeric experience ranges."""

    missing_before = df["experience"].isna().sum()

    mask = (
        df["experience"].isna()
        & df["minimumExperience"].notna()
        & df["maximumExperience"].notna()
    )

    df.loc[mask, "experience"] = (
        df.loc[mask, "minimumExperience"].astype(int).astype(str)
        + "-"
        + df.loc[mask, "maximumExperience"].astype(int).astype(str)
        + " Yrs"
    )

    filled = missing_before - df["experience"].isna().sum()

    print("\n===== EXPERIENCE CLEANING =====")
    print(f"Missing experience before: {missing_before}")
    print(f"Experience values filled: {filled}")
    print(f"Missing experience remaining: {df['experience'].isna().sum()}")

    return df

def analyze_missing_salary(df):
    """Analyze salary fields and determine whether missing ranges can be recovered."""

    missing_min = df["minimumSalary"].isna()
    missing_max = df["maximumSalary"].isna()

    print("\n===== SALARY ANALYSIS =====")

    print(f"Missing minimumSalary: {missing_min.sum()}")
    print(f"Missing maximumSalary: {missing_max.sum()}")

    print(
        f"Rows with missing salary range: "
        f"{(missing_min & missing_max).sum()}"
    )

    print("\nSalary column data type:")
    print(df["salary"].dtype)

    print("\nSample salary values:")
    print(df["salary"].head(20).to_string(index=False))

    print("\nSample records with missing salary range:")

    columns = [
        "jobId",
        "title",
        "salary",
        "currency",
        "minimumSalary",
        "maximumSalary"
    ]

    print(
        df.loc[
            missing_min & missing_max,
            columns
        ].head(10).to_string(index=False)
    )

def inspect_missing_salary_formats(df):
    """Inspect salary formats where numeric salary ranges are missing."""

    missing_salary = df[
        df["minimumSalary"].isna()
        & df["maximumSalary"].isna()
    ]

    print("\n===== MISSING SALARY FORMAT ANALYSIS =====")

    print(
        f"Records with missing salary range: "
        f"{len(missing_salary)}"
    )

    print("\nSalary formats found:")

    print(
        missing_salary["salary"]
        .value_counts(dropna=False)
        .head(50)
        .to_string()
    )

def fill_missing_salary(df):
    """Recover salary ranges from monthly salary values."""

    missing_mask = (
        df["minimumSalary"].isna()
        & df["maximumSalary"].isna()
    )

    monthly_mask = (
        missing_mask
        & df["salary"].astype(str).str.contains(
            "/month",
            case=False,
            na=False
        )
    )

    # Extract numeric monthly salary
    monthly_salary = (
        df.loc[monthly_mask, "salary"]
        .str.replace(",", "", regex=False)
        .str.extract(r"([\d.]+)", expand=False)
        .astype(float)
    )

    # Convert monthly salary to annual salary
    annual_salary = monthly_salary * 12

    df.loc[monthly_mask, "minimumSalary"] = annual_salary
    df.loc[monthly_mask, "maximumSalary"] = annual_salary

    filled = monthly_mask.sum()

    print("\n===== SALARY CLEANING =====")
    print(f"Monthly salary records converted: {filled}")

    unpaid_count = (
        missing_mask
        & df["salary"].astype(str).str.strip().str.lower().eq("unpaid")
    ).sum()

    print(f"Unpaid records: {unpaid_count}")

    remaining = (
        df["minimumSalary"].isna()
        & df["maximumSalary"].isna()
    ).sum()

    print(f"Salary ranges still missing: {remaining}")

    return df

def clean_tags_and_skills(df):
    """Standardize missing skill information."""

    missing_before = df["tagsAndSkills"].isna().sum()

    df["tagsAndSkills"] = df["tagsAndSkills"].fillna("Not Specified")

    print("\n===== SKILLS CLEANING =====")
    print(f"Missing skills before: {missing_before}")
    print(
        f"Missing skills after: "
        f"{df['tagsAndSkills'].isna().sum()}"
    )

    return df

def inspect_missing_company_names(df):
    """Inspect records with missing company names."""

    missing_company = df[df["companyName"].isna()]

    print("\n===== MISSING COMPANY NAME ANALYSIS =====")
    print(f"Missing company names: {len(missing_company)}")

    columns = [
        "jobId",
        "title",
        "companyName",
        "location",
        "salary"
    ]

    print(
        missing_company[columns]
        .to_string(index=False)
    )

def clean_company_names(df):
    """Standardize missing company names."""

    missing_before = df["companyName"].isna().sum()

    df["companyName"] = df["companyName"].fillna("Unknown")

    print("\n===== COMPANY NAME CLEANING =====")
    print(f"Missing company names before: {missing_before}")
    print(
        f"Missing company names after: "
        f"{df['companyName'].isna().sum()}"
    )

    return df

def final_data_quality_check(df):
    """Run final validation checks after cleaning."""

    print("\n===== FINAL DATA QUALITY CHECK =====")

    print(f"Total records: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"Duplicate job IDs: {df['jobId'].duplicated().sum()}")

    print("\nRemaining missing values:")
    print(
        df.isnull()
        .sum()
        .sort_values(ascending=False)
    )

    print("\nData types:")
    print(df.dtypes)

def save_cleaned_data(df):
    """Save the cleaned dataset."""

    output_file = "data/processed/jobs_cleaned.csv"

    df.to_csv(output_file, index=False)

    print("\n===== CLEANED DATA SAVED =====")
    print(f"Output file: {output_file}")
    print(f"Records saved: {len(df)}")

if __name__ == "__main__":

    # Load data
    df = load_data()

    # Basic dataset information
    print("\nDataset shape:")
    print(df.shape)

    # Missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Duplicate rows before cleaning
    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    # Duplicate job IDs before cleaning
    print("\nDuplicate job IDs:")
    print(df["jobId"].duplicated().sum())

    # Remove exact duplicate rows
    df = remove_duplicate_rows(df)

    analyze_missing_values(df)

    df = fill_missing_experience(df)

    df = fill_missing_salary(df)

    df = clean_tags_and_skills(df)

    df = clean_company_names(df)

    final_data_quality_check(df)

    save_cleaned_data(df)

    inspect_missing_company_names(df)

    analyze_missing_salary(df)

    inspect_missing_salary_formats(df)

    inspect_experience(df)

    analyze_missing_experience(df)

    # Analyze repeated job IDs after removing exact duplicates
    analyze_duplicate_job_ids(df)

    # Display all repeated job ID records
    inspect_duplicate_job_ids(df)

    compare_duplicate_records(df)
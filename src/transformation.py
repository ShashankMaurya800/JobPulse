import pandas as pd


INPUT_FILE = "data/processed/jobs_cleaned.csv"
OUTPUT_FILE = "data/processed/jobs_transformed.csv"


def load_data():
    """Load the cleaned job dataset."""

    df = pd.read_csv(INPUT_FILE)

    print("\n===== DATA LOADED =====")
    print(f"Records: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    return df


def standardize_column_names(df):
    """Convert column names to consistent snake_case format."""

    df = df.rename(
        columns={
            "jobId": "job_id",
            "jobUploaded": "job_uploaded",
            "companyName": "company_name",
            "tagsAndSkills": "tags_and_skills",
            "companyId": "company_id",
            "ReviewsCount": "reviews_count",
            "AggregateRating": "aggregate_rating",
            "jobDescription": "job_description",
            "minimumSalary": "minimum_salary",
            "maximumSalary": "maximum_salary",
            "minimumExperience": "minimum_experience",
            "maximumExperience": "maximum_experience",
        }
    )

    print("\n===== COLUMN NAMES STANDARDIZED =====")
    print(df.columns.tolist())

    return df


def transform_job_uploaded(df):
    """
    Convert job posting information into useful
    analytical fields.
    """

    # Start with missing values
    df["days_since_posted"] = pd.NA

    # Extract days only from values containing "Days Ago"
    days_ago_mask = (
    df["job_uploaded"]
    .astype(str)
    .str.contains(r"\bDays? Ago\b", case=False, na=False)
)

    df.loc[days_ago_mask, "days_since_posted"] = (
        df.loc[days_ago_mask, "job_uploaded"
        ]
        .str.extract(r"(\d+)", expand=False)
    )

    # Recently posted jobs are treated as 0 days old
    recent_mask = df["job_uploaded"].isin(
        [
            "Few Hours Ago",
            "Just Now",
            "Today"
        ]
    )

    df.loc[recent_mask, "days_since_posted"] = 0

    # Convert to numeric
    df["days_since_posted"] = pd.to_numeric(
        df["days_since_posted"],
        errors="coerce"
    )

    # Identify future-start jobs
    df["posting_status"] = "Posted"

    future_mask = (
        df["job_uploaded"]
        .astype(str)
        .str.startswith("Starts")
    )

    df.loc[future_mask, "posting_status"] = "Future Start"

    print("\n===== JOB POSTING AGE TRANSFORMATION =====")

    print(
        f"Valid values: "
        f"{df['days_since_posted'].notna().sum()}"
    )

    print(
        f"Missing values: "
        f"{df['days_since_posted'].isna().sum()}"
    )

    print(
        f"Recently posted values converted to 0 days: "
        f"{recent_mask.sum()}"
    )

    print(
        f"Future-start jobs: "
        f"{future_mask.sum()}"
    )

    return df

def transform_experience(df):
    """
    Convert experience ranges into numeric fields.
    """

    # Extract minimum and maximum experience
    experience_numbers = (
        df["experience"]
        .astype(str)
        .str.extract(r"(\d+)\s*-\s*(\d+)")
    )

    df["minimum_experience_years"] = pd.to_numeric(
        experience_numbers[0],
        errors="coerce"
    )

    df["maximum_experience_years"] = pd.to_numeric(
        experience_numbers[1],
        errors="coerce"
    )

    # Calculate average experience
    df["average_experience_years"] = (
        df["minimum_experience_years"]
        + df["maximum_experience_years"]
    ) / 2

    print("\n===== EXPERIENCE TRANSFORMATION =====")

    print(
        f"Minimum experience values: "
        f"{df['minimum_experience_years'].notna().sum()}"
    )

    print(
        f"Maximum experience values: "
        f"{df['maximum_experience_years'].notna().sum()}"
    )

    print(
        f"Average experience values: "
        f"{df['average_experience_years'].notna().sum()}"
    )

    print(
        f"Missing experience ranges: "
        f"{df['average_experience_years'].isna().sum()}"
    )

    return df

def transform_salary(df):
    """
    Create an average salary field while distinguishing
    undisclosed salaries from genuine zero-value ranges.
    """

    # Identify salaries that were not disclosed
    not_disclosed_mask = (
        df["salary"]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("not disclosed")
    )

    # Salary is unknown when it was not disclosed
    df.loc[not_disclosed_mask, "minimum_salary"] = pd.NA
    df.loc[not_disclosed_mask, "maximum_salary"] = pd.NA

    # Calculate average salary only when salary boundaries exist
    df["average_salary"] = (
        df["minimum_salary"]
        + df["maximum_salary"]
    ) / 2

    print("\n===== SALARY TRANSFORMATION =====")

    print(
        f"Not disclosed salaries: "
        f"{not_disclosed_mask.sum()}"
    )

    print(
        f"Average salary values: "
        f"{df['average_salary'].notna().sum()}"
    )

    print(
        f"Missing average salary values: "
        f"{df['average_salary'].isna().sum()}"
    )

    return df

def save_transformed_data(df):
    """Save the transformed dataset."""

    df.to_csv(OUTPUT_FILE, index=False)

    print("\n===== TRANSFORMED DATA SAVED =====")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Records saved: {len(df)}")


def main():
    df = load_data()

    df = standardize_column_names(df)

    df = transform_job_uploaded(df)

    df = transform_experience(df)

    df = transform_salary(df)

    save_transformed_data(df)

if __name__ == "__main__":
    main()
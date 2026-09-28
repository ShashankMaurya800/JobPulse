import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import text


# =========================
# Add project root to Python path
# =========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.database import get_engine


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="JobPulse Dashboard",
    page_icon="assets/jobpulse_icon.png",
    layout="wide"
)


# =========================
# Dashboard Header
# =========================

# =========================
# Dashboard Header
# =========================

col1, col2 = st.columns([1, 12])

with col1:
    st.markdown(
        "<div style='padding-top: 28px;'>",
        unsafe_allow_html=True
    )

    st.image(
        "dashboard/assets/jobpulse_icon.png",
        width=140
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

with col2:
    st.title("JobPulse — Job Market Dashboard")

st.write("Explore job market data stored in PostgreSQL.")


# =========================
# Load Data
# =========================

@st.cache_data
def load_data():
    """Load job data from PostgreSQL."""

    engine = get_engine()

    query = text("""
        SELECT *
        FROM jobs
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df


df = load_data()

st.success(f"Successfully loaded {len(df):,} job records.")


# =========================
# Key Performance Indicators
# =========================

total_jobs = len(df)

remote_jobs = (
    df["location"]
    .astype(str)
    .str.lower()
    .str.contains("remote", na=False)
    .sum()
)

future_jobs = (
    df["posting_status"] == "Future Start"
).sum()

companies = df["company_name"].nunique()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Jobs",
    f"{total_jobs:,}"
)

col2.metric(
    "Remote Jobs",
    f"{remote_jobs:,}"
)

col3.metric(
    "Future Start Jobs",
    f"{future_jobs:,}"
)

col4.metric(
    "Companies",
    f"{companies:,}"
)


# =========================
# Dashboard Charts
# =========================


# -------------------------
# Row 1: Locations + Companies
# -------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("Top Job Locations")

    top_locations = (
        df["location"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_locations.columns = ["location", "jobs"]

    location_chart = (
        alt.Chart(top_locations)
        .mark_bar()
        .encode(
            x=alt.X(
                "jobs:Q",
                title="Job Postings"
            ),
            y=alt.Y(
                "location:N",
                sort="-x",
                title=None
            ),
            tooltip=[
                alt.Tooltip("location:N", title="Location"),
                alt.Tooltip("jobs:Q", title="Job Postings")
            ]
        )
        .properties(
            height=320
        )
    )

    st.altair_chart(
        location_chart,
        use_container_width=True
    )


with col2:

    st.subheader("Top Companies by Job Postings")

    top_companies = (
        df["company_name"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_companies.columns = ["company", "jobs"]

    company_chart = (
        alt.Chart(top_companies)
        .mark_bar()
        .encode(
            x=alt.X(
                "jobs:Q",
                title="Job Postings"
            ),
            y=alt.Y(
                "company:N",
                sort="-x",
                title=None
            ),
            tooltip=[
                alt.Tooltip("company:N", title="Company"),
                alt.Tooltip("jobs:Q", title="Job Postings")
            ]
        )
        .properties(
            height=320
        )
    )

    st.altair_chart(
        company_chart,
        use_container_width=True
    )


# -------------------------
# Row 2: Salary + Experience
# -------------------------

col1, col2 = st.columns(2)


# -------------------------
# Salary Distribution
# -------------------------

with col1:

    st.subheader("Salary Distribution")

    salary_data = (
        df["average_salary"]
        .dropna()
    )

    salary_bands = pd.cut(
        salary_data,
        bins=[
            0,
            300000,
            600000,
            1000000,
            1500000,
            float("inf")
        ],
        labels=[
            "Below ₹3 Lakh",
            "₹3–6 Lakh",
            "₹6–10 Lakh",
            "₹10–15 Lakh",
            "Above ₹15 Lakh"
        ]
    )

    salary_distribution = (
        salary_bands
        .value_counts()
        .sort_index()
        .reset_index()
    )

    salary_distribution.columns = ["salary_band", "jobs"]

    salary_chart = (
        alt.Chart(salary_distribution)
        .mark_bar()
        .encode(
            x=alt.X(
                "jobs:Q",
                title="Job Postings"
            ),
            y=alt.Y(
                "salary_band:N",
                sort=None,
                title=None
            ),
            tooltip=[
                alt.Tooltip(
                    "salary_band:N",
                    title="Salary Range"
                ),
                alt.Tooltip(
                    "jobs:Q",
                    title="Job Postings"
                )
            ]
        )
        .properties(
            height=320
        )
    )

    st.altair_chart(
        salary_chart,
        use_container_width=True
    )

# -------------------------
# Experience Requirements
# -------------------------

with col2:

    st.subheader("Experience Requirements")

    experience_data = (
        df["experience"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )

    experience_data.columns = ["experience", "jobs"]

    experience_chart = (
        alt.Chart(experience_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "jobs:Q",
                title="Job Postings"
            ),
            y=alt.Y(
                "experience:N",
                sort="-x",
                title=None
            ),
            tooltip=[
                alt.Tooltip(
                    "experience:N",
                    title="Experience"
                ),
                alt.Tooltip(
                    "jobs:Q",
                    title="Job Postings"
                )
            ]
        )
        .properties(
            height=320
        )
    )

    st.altair_chart(
        experience_chart,
        use_container_width=True
    )


# -------------------------
# Row 3: Remote + Posting Status
# -------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("Remote vs Non-Remote Jobs")

    work_type = (
        df["location"]
        .astype(str)
        .apply(
            lambda x:
            "Remote"
            if "remote" in x.lower()
            else "Non-Remote"
        )
    )

    work_type_counts = (
        work_type
        .value_counts()
        .reset_index()
    )

    work_type_counts.columns = ["work_type", "jobs"]

    work_type_chart = (
        alt.Chart(work_type_counts)
        .mark_bar()
        .encode(
            x=alt.X(
                "jobs:Q",
                title="Job Postings"
            ),
            y=alt.Y(
                "work_type:N",
                sort="-x",
                title=None
            ),
            tooltip=[
                alt.Tooltip(
                    "work_type:N",
                    title="Work Type"
                ),
                alt.Tooltip(
                    "jobs:Q",
                    title="Job Postings"
                )
            ]
        )
        .properties(
            height=280
        )
    )

    st.altair_chart(
        work_type_chart,
        use_container_width=True
    )


with col2:

    st.subheader("Job Posting Status")

    posting_status = (
        df["posting_status"]
        .value_counts()
        .reset_index()
    )

    posting_status.columns = ["status", "jobs"]

    posting_status_chart = (
        alt.Chart(posting_status)
        .mark_bar()
        .encode(
            x=alt.X(
                "jobs:Q",
                title="Job Postings"
            ),
            y=alt.Y(
                "status:N",
                sort="-x",
                title=None
            ),
            tooltip=[
                alt.Tooltip(
                    "status:N",
                    title="Posting Status"
                ),
                alt.Tooltip(
                    "jobs:Q",
                    title="Job Postings"
                )
            ]
        )
        .properties(
            height=280
        )
    )

    st.altair_chart(
        posting_status_chart,
        use_container_width=True
    )
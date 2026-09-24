import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_engine():
    """Create and return a PostgreSQL database engine."""

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set.")

    engine = create_engine(DATABASE_URL)

    return engine


if __name__ == "__main__":
    engine = get_engine()

    with engine.connect() as connection:
        print("Successfully connected to PostgreSQL.")
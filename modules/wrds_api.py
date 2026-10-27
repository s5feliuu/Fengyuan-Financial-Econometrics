import wrds  # install it if you use it for the first time
from dotenv import load_dotenv
import os
import datetime as dt

# get wrds info once at the beginning on every day
CURRENT_DATE = dt.datetime.now().strftime("%Y-%m-%d")
print(f"Querying WRDS data for {CURRENT_DATE}")

load_dotenv()

wrds_username = os.getenv("fengyuanliu")
wrds_password = os.getenv("Jz&SSie#ezeP4Rb")


def initialize_wrds_connection():
    """Initialize and return a WRDS connection using credentials from environment variables."""
    if wrds_password:
        db = wrds.Connection(wrds_username=wrds_username, wrds_password=wrds_password)
    else:
        db = wrds.Connection(wrds_username=wrds_username)
    return db


def query_quarterly_fundamentals(db, date):
    """Query quarterly fundamentals data for the timeperiod after the given date."""
    query = f"""
        SELECT gvkey, datadate, fyearq, fqtr, atq, ltq, ceqq
        FROM comp_na_daily_all.fundq -- you can find this name via the data end point on WRDS https://wrds-api.wharton.upenn.edu/endpoints/
        WHERE datadate > '{date}'
    """
    df = db.raw_sql(query)
    return df


if __name__ == "__main__":
    # Initialize WRDS connection
    db = initialize_wrds_connection()

    # Query quarterly fundamentals data after 2025-09-01
    fundamentals_df = query_quarterly_fundamentals(db, "2025-09-01")

    print(fundamentals_df.head())

import os
import logging

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from io import StringIO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def create_database_engine():
    database_url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return create_engine(database_url)


def read_taxi_data(file_path):
    logger.info("reading taxi data from %s", file_path)

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".parquet"):
        df = pd.read_parquet(file_path)

    else:
        raise ValueError("file format not supported. use CSV or Parquet.")

    logger.info(
        "Loaded %s rows and %s columns",
        len(df),
        len(df.columns),
    )

    return df


def standardize_column_names(df):
    rename_mapping = {
        "VendorID": "vendor_id",
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        "passenger_count": "passenger_count",
        "trip_distance": "trip_distance",
        "RatecodeID": "ratecode_id",
        "store_and_fwd_flag": "store_and_fwd_flag",
        "PULocationID": "pickup_location_id",
        "DOLocationID": "dropoff_location_id",
        "payment_type": "payment_type",
        "fare_amount": "fare_amount",
        "extra": "extra",
        "mta_tax": "mta_tax",
        "tip_amount": "tip_amount",
        "tolls_amount": "tolls_amount",
        "improvement_surcharge": "improvement_surcharge",
        "total_amount": "total_amount",
        "congestion_surcharge": "congestion_surcharge",
    }

    return df.rename(columns=rename_mapping)


def select_database_columns(df):
    columns = [
        "vendor_id",
        "pickup_datetime",
        "dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "ratecode_id",
        "store_and_fwd_flag",
        "pickup_location_id",
        "dropoff_location_id",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount",
        "congestion_surcharge",
    ]

    existing_columns = [
        column
        for column in columns
        if column in df.columns
    ]

    return df[existing_columns]



def load_to_postgres(
    df,
    engine,
    table_name="yellow_taxi_trips",
):
    logger.info(
        "Loading %s rows into PostgreSQL using COPY",
        len(df),
    )

    buffer = StringIO()

    df.to_csv(
        buffer,
        index=False,
        header=False,
        na_rep="\\N",
    )

    buffer.seek(0)

    connection = engine.raw_connection()

    try:
        cursor = connection.cursor()
        
        cursor.execute("TRUNCATE TABLE raw.yellow_taxi_trips;")

        columns = ", ".join(df.columns)

        copy_sql = f"""
            COPY raw.{table_name} ({columns})
            FROM STDIN
            WITH (
                FORMAT CSV,
                NULL '\\N'
            )
        """

        cursor.copy_expert(
            copy_sql,
            buffer,
        )

        connection.commit()

        cursor.close()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

    logger.info(
        "database load completed"
    )






def run_pipeline(file_path):
    logger.info("starting nyc taxi ingestion pipeline")

    engine = create_database_engine()

    df = read_taxi_data(file_path)

    df = standardize_column_names(df)

    df = select_database_columns(df)

    load_to_postgres(
        df,
        engine,
    )

    logger.info("pipeline finished successfully")


if __name__ == "__main__":

    FILE_PATH = "data/yellow_tripdata_2016-01.csv"

    try:
        run_pipeline(FILE_PATH)

    except Exception:
        logger.exception("pipeline failed")
        raise
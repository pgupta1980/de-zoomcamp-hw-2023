from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials



@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    # if randint(0, 1) > 0:
    #     raise Exception

    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    # df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
    # df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
    # print(df.head(2))
    # print(f"columns: {df.dtypes}")
    # print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    data_path = Path(f'../data/{color}')
    data_path.mkdir(parents=True, exist_ok=True)
    path = Path(f"{data_path}/{dataset_file}.parquet")
    
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def etl_web_to_gcs(color: str, year: int, month: int) -> None:
    """Web to GCS"""

    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../")
    return Path(f"../{gcs_path}")


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="de-zoomcamp-2023-375514",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_web_to_gcs_to_bq(year: int, month: int, color: str) -> int:
    """Main ETL flow to load data into Big Query"""
    # color = "yellow"
    # year = 2021
    # month = 1
    etl_web_to_gcs(color, year, month)
    path = extract_from_gcs(color, year, month)
    df = pd.read_parquet(path)
    write_bq(df)
    # row_count = df.count()
    row_count = len(df)
    return (row_count)

@flow(log_prints=True)
def ans3_flow(
    months: list[int] = [2, 3], year: int = 2019, color: str = "yellow"
):
    total_count = 0
    for month in months:
        row_count = etl_web_to_gcs_to_bq(year, month, color)
        print(f"""dataframe count for {color}, {year}, {month}: {row_count}""")
        total_count = total_count + row_count

    print(f"""Total row count: {total_count}""")

if __name__ == "__main__":
    color = "yellow"
    months = [2, 3]
    year = 2019
    ans3_flow(months, year, color)

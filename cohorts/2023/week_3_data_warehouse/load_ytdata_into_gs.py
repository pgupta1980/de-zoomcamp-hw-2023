from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.filesystems import GitHub
import os, requests

# github_block = GitHub.load("de-zoomcamp")

@task(log_prints = True, retries = 3)
def download_file(dataset_url: str) -> str:
    get_response = requests.get(dataset_url, stream = True)
    file_name  = dataset_url.split("/")[-1]
    data_path = f'../data/fhv/'
    Path(data_path).mkdir(parents=True, exist_ok=True)
    download_path = data_path + file_name
    with open(download_path, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size = 1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print(download_path)
    return download_path

@task()
def write_gcs(path: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("de-zoomcamp-week3")
    from_path = Path(f"""{path}""")
    to_path = Path(f"""{path.replace('../', '')}""")
    gcs_block.upload_from_path(from_path = from_path, to_path = to_path)
    return

@flow(log_prints=True)
def etl_web_to_gcs(year: int) -> None:
    """The main ETL function"""
    # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
    month_list = [f'{i:>02}' for i in range(1, 13)] 
    for month in month_list:
        dataset_file = f"fhv_tripdata_{year}-{month}"
        dataset_url  = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}.csv.gz"

        path_str = download_file(dataset_url)
        write_gcs(path_str)
        print(f"""downloaded file written into {path_str}""")


if __name__ == "__main__":
    etl_web_to_gcs()

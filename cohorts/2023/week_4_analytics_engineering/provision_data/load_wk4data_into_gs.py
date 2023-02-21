from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.filesystems import GitHub
import os, requests

# github_block = GitHub.load("de-zoomcamp")

@task(log_prints = True, retries = 3)
def download_file(dataset_url_with_file: str) -> str:
    get_response = requests.get(dataset_url_with_file, stream = True)
    file_name  = dataset_url_with_file.split("/")[-1]
    data_subpath = dataset_url_with_file.split("/")[-2]
    data_path = f'../data/{data_subpath}/'
    Path(data_path).mkdir(parents=True, exist_ok=True)
    download_path = data_path + file_name
    with open(download_path, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size = 1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    print(f"""dataset_url_with_file :: {dataset_url_with_file}""")
    print(f"""file_name :: {file_name}""")
    print(f"""data_subpath :: {data_subpath}""")
    print(f"""data_path :: {data_path}""")
    print(f"""download_path :: {download_path}""")

    return download_path

@task()
def write_gcs(path: str) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("de-zoomcamp-week4")
    from_path = Path(f"""{path}""")
    to_path = Path(f"""{path.replace('../', '')}""")
    gcs_block.upload_from_path(from_path = from_path, to_path = to_path)
    return

""" @flow(log_prints=True)
def etl_web_to_gcs_wrapper(data_list: list) -> None:
    for data_dict in data_list:
        dataset_url = data_dict['dataset_url']
        dataset_file_prefix = data_dict['dataset_file_prefix']
        year = data_dict['year']
        etl_web_to_gcs(dataset_url, dataset_file_prefix, year) """

# @task(log_prints = True, retries = 3)
@flow(log_prints=True)
def etl_web_to_gcs(dataset_url: str, dataset_file_prefix: str, year: int) -> None:
    """The main ETL function"""
    # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
    month_list = [f'{i:>02}' for i in range(1, 13)] 
    for month in month_list:
        dataset_file = f"{dataset_file_prefix}{year}-{month}"
        dataset_url_with_file  = f"{dataset_url}/{dataset_file}.csv.gz"

        path_str = download_file(dataset_url_with_file)
        write_gcs(path_str)
        print(f"""downloaded file written into {path_str}""")


if __name__ == "__main__":
    etl_web_to_gcs()

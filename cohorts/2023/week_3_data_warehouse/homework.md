## Week 3 Homework
<b><u>Important Note:</b></u> <p>You can load the data however you would like, but keep the files in .GZ Format. 
If you are using orchestration such as Airflow or Prefect do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>
<u>NOTE:</u> You can use the CSV option for the GZ files when creating an External Table</br>

<b>SETUP:</b></br>
Create an external table using the fhv 2019 data. </br>
Create a table in BQ using the fhv 2019 data (do not partition or cluster this table). </br>
Data can be found here: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>

**Ans:-**

**1. Created python code to download files from above url and then upload into gcs and ran it via prefect.**

<b>gcs bucket block :- </b>

![image](https://user-images.githubusercontent.com/6199261/218431883-039201f3-241b-4f12-8dbb-e7afa9802c32.png)

<b>main file :- </b>
https://github.com/pgupta1980/de-zoomcamp-hw-2023/blob/ec93cd611bbf54efe4c172eb3f186c6c36058465/cohorts/2023/week_3_data_warehouse/load_ytdata_into_gs.py

<b>Prefect Commands :- </b>

```
prefect deployment build ./load_ytdata_into_gs.py:etl_web_to_gcs -n "ytd_to_gs" -a
prefect deployment run etl-web-to-gcs/ytd_to_gs --params '{"year":2019}'
```
<b>Result :- </b>
![image](https://user-images.githubusercontent.com/6199261/218433663-d3368a27-4450-4b06-9d3e-2e78e0e147fe.png)

**2. Created external table in bq.**
```
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-2023-375514.nytaxi.fhv_td_2019_ext`
OPTIONS (
  format = 'CSV',
  uris = ['gs://week3_bq/data/fhv/fhv_tripdata_2019-*.csv.gz']
);

```
![image](https://user-images.githubusercontent.com/6199261/218434675-0aea8ed7-b622-451e-8b2d-55cbba90bb17.png)

**3. Created a non partitioned table from external table.**
```
CREATE OR REPLACE TABLE de-zoomcamp-2023-375514.nytaxi.fhv_td_2019_np AS
SELECT * FROM de-zoomcamp-2023-375514.nytaxi.fhv_td_2019_ext;
```
![image](https://user-images.githubusercontent.com/6199261/218436639-a42d075a-60c4-4c64-9edc-29ab3fc28ac0.png)


## Question 1:
What is the count for fhv vehicle records for year 2019?
- 65,623,481
- 43,244,696
- 22,978,333
- 13,942,414

**Ans:-** - 43,244,696

```
SELECT count(1) FROM `de-zoomcamp-2023-375514.nytaxi.fhv_td_2019_ext`

43244696
```
![image](https://user-images.githubusercontent.com/6199261/218435355-97a7cee7-af8a-41ec-8dfe-ed2203dce657.png)


## Question 2:
Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.</br> 
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- 25.2 MB for the External Table and 100.87MB for the BQ Table
- 225.82 MB for the External Table and 47.60MB for the BQ Table
- 0 MB for the External Table and 0MB for the BQ Table
- 0 MB for the External Table and 317.94MB for the BQ Table 

**Ans:-**
- 0 MB for the External Table and 317.94MB for the BQ Table 

**External Table -**
```
SELECT COUNT(DISTINCT(affiliated_base_number)) FROM `de-zoomcamp-2023-375514.nytaxi.fhv_td_2019_ext`;
Bytes processed : 0 B (results cached)
```
![image](https://user-images.githubusercontent.com/6199261/218437228-ecdb19cf-4250-42a0-889e-51e9c0349855.png)
![image](https://user-images.githubusercontent.com/6199261/218437679-dab4b7dc-10db-4239-8d5e-37ebb5bf4d45.png)

**Non-partitioned bq table -**

```
SELECT COUNT(DISTINCT(affiliated_base_number)) FROM `de-zoomcamp-2023-375514.nytaxi.fhv_td_2019_np`;
Bytes processed : 317.94 MB
```
![image](https://user-images.githubusercontent.com/6199261/218438031-72310253-45ff-4d3c-ac59-ad571f52179f.png)
![image](https://user-images.githubusercontent.com/6199261/218438141-64bafb2b-a548-4a3f-9353-9604bb0361eb.png)


## Question 3:
How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?
- 717,748
- 1,215,687
- 5
- 20,332

## Question 4:
What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?
- Cluster on pickup_datetime Cluster on affiliated_base_number
- Partition by pickup_datetime Cluster on affiliated_base_number
- Partition by pickup_datetime Partition by affiliated_base_number
- Partition by affiliated_base_number Cluster on pickup_datetime

## Question 5:
Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).</br> 
Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches.
- 12.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table
- 582.63 MB for non-partitioned table and 0 MB for the partitioned table
- 646.25 MB for non-partitioned table and 646.25 MB for the partitioned table


## Question 6: 
Where is the data stored in the External Table you created?

- Big Query
- GCP Bucket
- Container Registry
- Big Table


## Question 7:
It is best practice in Big Query to always cluster your data:
- True
- False


## (Not required) Question 8:
A better format to store these files may be parquet. Create a data pipeline to download the gzip files and convert them into parquet. Upload the files to your GCP Bucket and create an External and BQ Table. 


Note: Column types for all files used in an External Table must have the same datatype. While an External Table may be created and shown in the side panel in Big Query, this will need to be validated by running a count query on the External Table to check if any errors occur. 
 
## Submitting the solutions

* Form for submitting: https://forms.gle/rLdvQW2igsAT73HTA
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 13 February (Monday), 22:00 CET


## Solution

We will publish the solution here

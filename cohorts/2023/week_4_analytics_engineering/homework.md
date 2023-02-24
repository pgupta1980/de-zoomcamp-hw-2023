## Week 4 Homework 

In this homework, we'll use the models developed during the week 4 videos and enhance the already presented dbt project using the already loaded Taxi data for fhv vehicles for year 2019 in our DWH.

This means that in this homework we use the following data [Datasets list](https://github.com/DataTalksClub/nyc-tlc-data/)
* Yellow taxi data - Years 2019 and 2020
* Green taxi data - Years 2019 and 2020 
* fhv data - Year 2019. 

We will use the data loaded for:

* Building a source table: `stg_fhv_tripdata`
* Building a fact table: `fact_fhv_trips`
* Create a dashboard 

If you don't have access to GCP, you can do this locally using the ingested data from your Postgres database
instead. If you have access to GCP, you don't need to do it for local Postgres -
only if you want to.

> **Note**: if your answer doesn't match exactly, select the closest option 

### Question 1: 

**What is the count of records in the model fact_trips after running all models with the test run variable disabled and filtering for 2019 and 2020 data only (pickup datetime)?** 

You'll need to have completed the ["Build the first dbt models"](https://www.youtube.com/watch?v=UVI30Vxzd6c) video and have been able to run the models via the CLI. 
You should find the views and models for querying in your DWH.

- 41648442
- 51648442
- 61648442
- 71648442

**Ans:-** 61648442

**My prepared dashboards (Screenshot below) :**
* Page 1 - FHV Trips Analysis
* Page 2 - Green and Yellow Trips Analysis (as per the tutorial)

![image](https://user-images.githubusercontent.com/6199261/221273759-d5341533-c537-4a06-9699-322d3531c6e7.png)
**Answer as per record count in Page 2**

![image](https://user-images.githubusercontent.com/6199261/221271853-69de0979-d1e0-4a9f-b8e4-955c24c74a29.png)

### Question 2: 

**What is the distribution between service type filtering by years 2019 and 2020 data as done in the videos?**

You will need to complete "Visualising the data" videos, either using [google data studio](https://www.youtube.com/watch?v=39nLTs74A3E) or [metabase](https://www.youtube.com/watch?v=BnLkrA7a6gM). 

- 89.9/10.1
- 94/6
- 76.3/23.7
- 99.1/0.9

**Ans:-** 89.9/10.1 - **As per Service Type Distribution filtering in Page 2 - Green and Yellow Trips Analysis in the screenshot below.**

![image](https://user-images.githubusercontent.com/6199261/221272476-d563c7d3-3a6f-4301-b24a-6879a9925d41.png)



### Question 3: 

**What is the count of records in the model stg_fhv_tripdata after running all models with the test run variable disabled (:false)?**  

Create a staging model for the fhv data for 2019 and do not add a deduplication step. Run it via the CLI without limits (is_test_run: false).
Filter records with pickup time in year 2019.

- 33244696
- 43244696
- 53244696
- 63244696

**Ans:-** 43244696
```
Query used - SELECT count(1) FROM `de-zoomcamp-2023-375514.dbt_pgupta1980.stg_fhv_tripdata` 
where EXTRACT(YEAR FROM pickup_datetime) = 2019;
```
**Screenshot below : **

![image](https://user-images.githubusercontent.com/6199261/221270514-8ae929e2-0311-4997-bb62-52f0fa96474d.png)

### Question 4: 

**What is the count of records in the model fact_fhv_trips after running all dependencies with the test run variable disabled (:false)?**  

Create a core model for the stg_fhv_tripdata joining with dim_zones.
Similar to what we've done in fact_trips, keep only records with known pickup and dropoff locations entries for pickup and dropoff locations. 
Run it via the CLI without limits (is_test_run: false) and filter records with pickup time in year 2019.

- 12998722
- 22998722
- 32998722
- 42998722

**Ans:-** 22998722 - **As per Record Count in Page 1 - FHV Trips Analysis in the screenshot below.**

![image](https://user-images.githubusercontent.com/6199261/221274088-ad11adf3-7cdd-4273-9ca8-0c1ad70fd0e3.png)

### Question 5: 

**What is the month with the biggest amount of rides after building a tile for the fact_fhv_trips table?**

Create a dashboard with some tiles that you find interesting to explore the data. One tile should show the amount of trips per month, as done in the videos for fact_trips, based on the fact_fhv_trips table.

- March
- April
- January
- December

**Ans:-** January - **As per Trips per Month tile in Page 1 - FHV Trips Analysis in the screenshot below.**

![image](https://user-images.githubusercontent.com/6199261/221274218-ffef4053-832c-459f-bac0-9710cfd3a55d.png)

## Submitting the solutions

* Form for submitting: https://forms.gle/6A94GPutZJTuT5Y16
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 25 February (Saturday), 22:00 CET


## Solution

We will publish the solution here

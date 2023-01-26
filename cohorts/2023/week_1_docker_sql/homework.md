## Week 1 Homework

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command

Which tag has the following text? - *Write the image ID to the file* 

- `--imageid string`
- `--iidfile string` - this has the text *Write the image ID to the file* 
- `--idimage string`
- `--idfile string`


## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list). 
How many python packages/modules are installed?

- 1
- 6
- 3 - packages installed
- 7

```(base) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023$ docker run -it --entrypoint=bash python:3.9
Unable to find image 'python:3.9' locally
3.9: Pulling from library/python
bbeef03cda1f: Pull complete 
f049f75f014e: Pull complete 
56261d0e6b05: Pull complete 
9bd150679dbd: Pull complete 
5b282ee9da04: Pull complete 
03f027d5e312: Pull complete 
79903339cfdb: Pull complete 
efbad12427dd: Pull complete 
862894708010: Pull complete 
Digest: sha256:7af616b934168e213d469bff23bd8e4f07d09ccbe87e82c464cacd8e2fb244bf
Status: Downloaded newer image for python:3.9
root@249bbb001953:/# pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
```

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


## Question 3. Count records 

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20689
- 20530 - Answer
- 17630
- 21090

Query
```
select count(1) from public.green_trip_data where 
to_char(lpep_pickup_datetime, 'yyyy-MM-dd') = '2019-01-15'
and to_char(lpep_dropoff_datetime, 'yyyy-MM-dd') = '2019-01-15';
```

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-18
- 2019-01-28
- 2019-01-15 - Ans
- 2019-01-10

Query
```
select trip_distance, to_char(lpep_pickup_datetime, 'yyyy-MM-dd') lpep_pickup_datetime  
from public.green_trip_data order by trip_distance desc limit 1; 
```

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?
 
- 2: 1282 ; 3: 266
- 2: 1532 ; 3: 126
- 2: 1282 ; 3: 254 - Ans
- 2: 1282 ; 3: 274

Query
```select *  from (select passenger_count, count(1) from public.green_trip_data where 
to_char(lpep_pickup_datetime, 'yyyy-MM-dd') = '2019-01-01'
or to_char(lpep_dropoff_datetime, 'yyyy-MM-dd') = '2019-01-01'
group by passenger_count) pc where passenger_count in (2,3) ;
```


## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- South Ozone Park
- Long Island City/Queens Plaza - Ans

Query
```select doz."Zone"  from 
green_trip_data td,
zones puz,
zones doz
where td."PULocationID" = puz."LocationID"
and td."DOLocationID" = doz."LocationID"
and puz."Zone" = 'Astoria'
order by tip_amount desc limit 1;
```


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Thursday), 22:00 CET


## Solution

We will publish the solution here

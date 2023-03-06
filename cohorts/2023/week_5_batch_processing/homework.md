## Week 5 Homework 

In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the FHVHV 2021-06 data found here. [FHVHV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhvhv/fhvhv_tripdata_2021-06.csv.gz )


### Question 1: 

**Install Spark and PySpark** 

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?
- 3.3.2
- 2.1.4
- 1.2.3
- 5.4
</br></br>

### Ans:
3.3.2

```
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

spark.version

```
**Screenshot:**

![image](https://user-images.githubusercontent.com/6199261/223182636-4b33cd09-c353-4a08-ae19-e619dfcf7c0a.png)

### Question 2: 

**HVFHW June 2021**

Read it with Spark using the same schema as we did in the lessons.</br> 
We will use this dataset for all the remaining questions.</br>
Repartition it to 12 partitions and save it to parquet.</br>
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.</br>


- 2MB
- 24MB
- 100MB
- 250MB
</br></br>

### Ans:
24MB

```
!ls -l /home/pgupta/data/pq/fhvhv/2021/06/ --block-size=M
total 271M
-rw-r--r-- 1 pgupta pgupta  0M Mar  6 17:22 _SUCCESS
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00000-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00001-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00002-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00003-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00004-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00005-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00006-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00007-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00008-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00009-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00010-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
-rw-r--r-- 1 pgupta pgupta 23M Mar  6 17:22 part-00011-1394a35a-758a-4077-a240-c3228c7feb3f-c000.snappy.parquet
```
**Screenshot:**

![image](https://user-images.githubusercontent.com/6199261/223184703-31b36e5d-f53d-4fd6-b556-169739a988cf.png)

### Question 3: 

**Count records**  

How many taxi trips were there on June 15?</br></br>
Consider only trips that started on June 15.</br>

- 308,164
- 12,856
- 452,470
- 50,982
</br></br>

### Ans:
452,470

```
df.withColumn('pickup_date', F.to_date(df.pickup_datetime)) \
    .filter("pickup_date = '2021-06-15'") \
    .count()
    
452470
```
**Screenshot:**

![image](https://user-images.githubusercontent.com/6199261/223185628-0182c042-e8b9-47dd-a4ba-8c55c811ee5f.png)

### Question 4: 

**Longest trip for each day**  

Now calculate the duration for each trip.</br>
How long was the longest trip in Hours?</br>

- 66.87 Hours
- 243.44 Hours
- 7.68 Hours
- 3.32 Hours
</br></br>

### Ans:
452,470

```
df.withColumn('trip_duration_in_hrs', \
              (F.col("dropoff_datetime").cast("long") - F.col('pickup_datetime').cast("long"))/3600) \
.select(F.col('trip_duration_in_hrs')).sort(F.col('trip_duration_in_hrs').desc()).limit(1).show()
    
+--------------------+
|trip_duration_in_hrs|
+--------------------+
|    66.8788888888889|
+--------------------+
```
**Screenshot:**

![image](https://user-images.githubusercontent.com/6199261/223186007-9c424638-ee87-477f-8ad8-8d66339bc877.png)

### Question 5: 

**User Interface**

 Spark’s User Interface which shows application's dashboard runs on which local port?</br>

- 80
- 443
- 4040
- 8080
</br></br>

### Ans:
4040

**Screenshot:**

![image](https://user-images.githubusercontent.com/6199261/223186980-9b5b2960-cf1c-425d-ba82-f337c679aeeb.png)


### Question 6: 

**Most frequent pickup location zone**

Load the zone lookup data into a temp view in Spark</br>
[Zone Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv)</br>

Using the zone lookup data and the fhvhv June 2021 data, what is the name of the most frequent pickup location zone?</br>

- East Chelsea
- Astoria
- Union Sq
- Crown Heights North
</br></br>

### Ans:
Crown Heights North

```
spark.read \
    .option("header", "true") \
    .csv('/home/pgupta/data/ny_taxi_data/taxi+_zone_lookup.csv').createOrReplaceTempView("taxi_lookup_v")

df.createOrReplaceTempView("fhvhv_2021_06_v")

spark.sql("""select b.Zone as zone, count(1) as count from
fhvhv_2021_06_v a,
taxi_lookup_v b
where a.PULocationID = b.LocationID
group by zone""").sort(F.col('count').desc()).limit(1).show()

+-------------------+------+
|               zone| count|
+-------------------+------+
|Crown Heights North|231279|
+-------------------+------+

```

**Screenshot:**

![image](https://user-images.githubusercontent.com/6199261/223187892-ee766056-42c2-4aef-a2e1-f9c3eb74edb9.png)

## Submitting the solutions

* Form for submitting: https://forms.gle/EcSvDs6vp64gcGuD8
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 06 March (Monday), 22:00 CET


## Solution

We will publish the solution here

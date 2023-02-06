## Week 2 Homework

The goal of this homework is to familiarise users with workflow orchestration and observation. 


## Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

* 447,770
* 766,792
* 299,234
* 822,132

<b>Ans:-</b>

The file ans1.py contains the code for this solution, result - 447770

<b>Log File Statement : </b> 06:55:05.166 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770

<b>Complete Log : </b>
```
python cohorts/2023/week_2/ans1.py 
06:55:02.309 | INFO    | prefect.engine - Created flow run 'practical-seal' for flow 'etl-web-to-gcs'
06:55:02.485 | INFO    | Flow run 'practical-seal' - Created task run 'fetch-b4598a4a-0' for task 'fetch'
06:55:02.487 | INFO    | Flow run 'practical-seal' - Executing 'fetch-b4598a4a-0' immediately...
06:55:04.868 | INFO    | Task run 'fetch-b4598a4a-0' - Finished in state Completed()
06:55:04.905 | INFO    | Flow run 'practical-seal' - Created task run 'clean-b9fd7e03-0' for task 'clean'
06:55:04.906 | INFO    | Flow run 'practical-seal' - Executing 'clean-b9fd7e03-0' immediately...
06:55:05.166 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770
06:55:05.203 | INFO    | Task run 'clean-b9fd7e03-0' - Finished in state Completed()
06:55:05.244 | INFO    | Flow run 'practical-seal' - Created task run 'write_local-f322d1be-0' for task 'write_local'
06:55:05.246 | INFO    | Flow run 'practical-seal' - Executing 'write_local-f322d1be-0' immediately...
06:55:06.738 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
06:55:06.773 | INFO    | Flow run 'practical-seal' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
06:55:06.775 | INFO    | Flow run 'practical-seal' - Executing 'write_gcs-1145c921-0' immediately...
06:55:06.915 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'prefect-de-zoomcamp-bucket-2299'.
06:55:07.380 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('../data/green/green_tripdata_2020-01.parquet') to the bucket 'prefect-de-zoomcamp-bucket-2299' path '../data/green/green_tripdata_2020-01.parquet'.
06:55:11.125 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
06:55:11.162 | INFO    | Flow run 'practical-seal' - Finished in state Completed('All states completed.')
```

## Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows. 

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

- `0 5 1 * *`
- `0 0 5 1 *`
- `5 * 1 0 *`
- `* * 5 1 0`

<b>Ans:-</b>
- `0 5 1 * *`

<b>Screenshot : </b> 

![ans2](https://user-images.githubusercontent.com/6199261/216910409-008c58bd-7e94-4fc6-9fa9-1bcbf486eaf9.png)


<b>Complete Log : </b>
```
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ prefect deployment build ./ans2.py:etl_web_to_gcs -n ans2_cron --cron "0 5 1 * *"
Found flow 'etl-web-to-gcs'
Deployment YAML created at '/home/pgupta/de-zoomcamp-hw-2023/cohorts/2023/week_2/etl_web_to_gcs-deployment.yaml'.
Deployment storage None does not have upload capabilities; no files uploaded.  Pass --skip-upload to suppress this warning.
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ prefect deployment apply ./etl_web_to_gcs-deployment.yaml 
Successfully loaded 'ans2_cron'
Deployment 'etl-web-to-gcs/ans2_cron' successfully created with id '9ccb508d-45e5-49a2-a574-a31365d4a6cb'.
View Deployment in UI: http://127.0.0.1:4200/deployments/deployment/9ccb508d-45e5-49a2-a574-a31365d4a6cb

To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ 
```

## Question 3. Loading data to BigQuery 

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color. 

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

- 14,851,920
- 12,282,990
- 27,235,753
- 11,338,483

<b>Ans:-</b>
14,851,920

Code for printing total count in ans3.py

```

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

```

<b>Command Line :</b>

```

[(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ prefect deployment build ./ans3.py:ans3_flow -n "ans3"
Found flow 'ans3-flow'
Deployment YAML created at '/home/pgupta/de-zoomcamp-hw-2023/cohorts/2023/week_2/ans3_flow-deployment.yaml'.
Deployment storage None does not have upload capabilities; no files uploaded.  Pass --skip-upload to suppress this warning.
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ prefect deployment apply ./ans3_flow-deployment.yaml 
Successfully loaded 'ans3'
Deployment 'ans3-flow/ans3' successfully created with id '1ba02425-f62a-4b1a-bc07-ba5047a96036'.
View Deployment in UI: http://127.0.0.1:4200/deployments/deployment/1ba02425-f62a-4b1a-bc07-ba5047a96036

To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ prefect deployment run ans3-flow/ans3 --params '{"months": [2,3], "color": "yellow", "year":2019}'
Creating flow run for deployment 'ans3-flow/ans3'...
Created flow run 'tacky-toad'.
└── UUID: abc39c37-a26f-45da-8423-b362472b3b19
└── Parameters: {'months': [2, 3], 'color': 'yellow', 'year': 2019}
└── Scheduled start time: 2023-02-06 05:37:55 UTC (now)
└── URL: http://127.0.0.1:4200/flow-runs/flow-run/abc39c37-a26f-45da-8423-b362472b3b19
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/cohorts/2023/week_2$ ](url)

```

<b>Log Screenshot : </b>

![image](https://user-images.githubusercontent.com/6199261/216911820-32e4672c-6ca6-415f-805a-6f0f0d10a32d.png)


## Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image. 

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

- 88,019
- 192,297
- 88,605
- 190,225

<b>Ans:-</b>

<b>Github Storage Block - make_github_block.py</b>

```

from prefect.filesystems import GitHub

block = GitHub(
    repository="https://github.com/pgupta1980/de-zoomcamp-hw-2023.git"
)
block.save("de-zoomcamp-github", overwrite=True)

```

<b>Git Commit Steps : </b>

```

git add .
git commit -m "week 2"
git push

```

<b>Command Line : </b>

```

(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023$ prefect deployment build cohorts/2023/week_2/ans4.py:etl_web_to_gcs  -n ans4-github  -sb github/de-zoomcamp-github  --apply
Found flow 'etl-web-to-gcs'
Deployment YAML created at '/home/pgupta/de-zoomcamp-hw-2023/etl_web_to_gcs-deployment.yaml'.
Deployment storage GitHub(repository='https://github.com/pgupta1980/de-zoomcamp-hw-2023.git', reference=None, access_token=None) does not have 
upload capabilities; no files uploaded.  Pass --skip-upload to suppress this warning.
Deployment 'etl-web-to-gcs/ans4-github' successfully created with id '9e165fef-800f-4001-9bfc-cbe1be4af8fd'.

To execute flow runs from this deployment, start an agent that pulls work from the 'default' work queue:
$ prefect agent start -q 'default'
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023$ prefect deployment run 'etl-web-to-gcs/github-deploy' -p color='green' -p year=2020 -p month=11Creating flow run for deployment 'etl-web-to-gcs/github-deploy'...
Created flow run 'boisterous-koel'.
└── UUID: 03e3450f-42e3-44ce-88b8-8ba6197f2885
└── Parameters: {'color': 'green', 'year': 2020, 'month': 11}
└── Scheduled start time: 2023-02-06 07:52:32 UTC (now)
└── URL: http://127.0.0.1:4200/flow-runs/flow-run/03e3450f-42e3-44ce-88b8-8ba6197f2885
(zoomcamp) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023$ 

```
Count of rows processed from log file : 

```
07:56:55.002 | INFO    | Flow run 'aquamarine-baboon' - dataframe count for green, 2020, 11: 88605
```

<b>Log Screenshot : </b>
![image](https://user-images.githubusercontent.com/6199261/216916332-a84b7c31-ef47-4d43-b3d4-bd5b5af7d960.png)



## Question 5. Email or Slack notifications

Q5. It’s often helpful to be notified when something with your dataflow doesn’t work as planned. Choose one of the options below for creating email or slack notifications.

The hosted Prefect Cloud lets you avoid running your own server and has Automations that allow you to get notifications when certain events occur or don’t occur. 

Create a free forever Prefect Cloud account at app.prefect.cloud and connect your workspace to it following the steps in the UI when you sign up. 

Set up an Automation that will send yourself an email when a flow run completes. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see the notification.

Alternatively, use a Prefect Cloud Automation or a self-hosted Orion server Notification to get notifications in a Slack workspace via an incoming webhook. 

Join my temporary Slack workspace with [this link](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 people can use this link and it expires in 90 days. 

In the Prefect Cloud UI create an [Automation](https://docs.prefect.io/ui/automations) or in the Prefect Orion UI create a [Notification](https://docs.prefect.io/ui/notifications/) to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: https://hooks.slack.com/services/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

Test the functionality.

Alternatively, you can grab the webhook URL from your own Slack workspace and Slack App that you create. 


How many rows were processed by the script?

- `125,268`
- `377,922`
- `728,390`
- `514,392`

<b>Ans :- </b>
514,392 is the answer

```
08:14:01.183 | INFO    | Flow run 'attentive-wren' - dataframe count for green, 2019, 4: 514392
```

<b>Notification Setup </b>
![image](https://user-images.githubusercontent.com/6199261/216917316-f84ce87d-fd25-4201-b2d7-3b845f310b95.png)
![image](https://user-images.githubusercontent.com/6199261/216917422-20670747-2ed9-4c74-818d-d9d99ec4f392.png)

<b>Slack App Setup </b>
![image](https://user-images.githubusercontent.com/6199261/216917679-a20e8aae-df21-484a-96c2-5b16ad35aceb.png)

<b>Notification Received : </b>
![image](https://user-images.githubusercontent.com/6199261/216918039-a0db27a6-5ef5-4748-973c-3b48e780c596.png)

<b>Log :</b>
![image](https://user-images.githubusercontent.com/6199261/216919232-0c8677e6-b42c-4c5b-9e46-7a20bffd6331.png)

## Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks (*) on the next page of the UI?

- 5
- 6
- 8
- 10

<b>Ans:- </b>
8

<b>Secret Configuration Screenshots :- </b>
![image](https://user-images.githubusercontent.com/6199261/216919802-76a72d28-fe42-4717-9ae5-7e30d2394e9f.png)
![image](https://user-images.githubusercontent.com/6199261/216919972-c840df29-450d-4727-8574-31d4b6e33661.png)


## Submitting the solutions

* Form for submitting: https://forms.gle/PY8mBEGXJ1RvmTM97
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 6 February (Monday), 22:00 CET


## Solution

We will publish the solution here

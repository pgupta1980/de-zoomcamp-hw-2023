## Week 1 Homework

In this homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP install Terraform. Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 1. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Result
```
(base) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/week1/1_terraform_gcp/terraform$ terraform plan -var="project=dtc-de-375810"
google_storage_bucket.data-lake-bucket: Refreshing state... [id=dtc_data_lake_dtc-de-375810]
google_bigquery_dataset.dataset: Refreshing state... [id=projects/dtc-de-375810/datasets/trips_data_all]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # google_storage_bucket.data-lake-bucket must be replaced
-/+ resource "google_storage_bucket" "data-lake-bucket" {
      - default_event_based_hold    = false -> null
      ~ id                          = "dtc_data_lake_dtc-de-375810" -> (known after apply)
      - labels                      = {} -> null
      ~ name                        = "dtc_data_lake_dtc-de-375810" -> "dtc_data_lake_dtc-de-375810_de-zoomcamp-hw-2023-pg1" # forces replacement
      ~ project                     = "dtc-de-375810" -> (known after apply)
      ~ public_access_prevention    = "inherited" -> (known after apply)
      - requester_pays              = false -> null
      ~ self_link                   = "https://www.googleapis.com/storage/v1/b/dtc_data_lake_dtc-de-375810" -> (known after apply)
      ~ storage_class               = "REGIONAL" -> "STANDARD"
      ~ url                         = "gs://dtc_data_lake_dtc-de-375810" -> (known after apply)
        # (3 unchanged attributes hidden)

      ~ lifecycle_rule {

          - condition {
              - age                        = 30 -> null
              - days_since_custom_time     = 0 -> null
              - days_since_noncurrent_time = 0 -> null
              - matches_prefix             = [] -> null
              - matches_storage_class      = [] -> null
              - matches_suffix             = [] -> null
              - num_newer_versions         = 0 -> null
              - with_state                 = "ANY" -> null
            }
          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }

            # (1 unchanged block hidden)
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }

        # (1 unchanged block hidden)
    }

Plan: 1 to add, 0 to change, 1 to destroy.

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply"
now.
(base) pgupta@de-zoomcamp:~/de-zoomcamp-hw-2023/week1/1_terraform_gcp/terraform$ terraform apply -var="project=dtc-de-375810"
google_storage_bucket.data-lake-bucket: Refreshing state... [id=dtc_data_lake_dtc-de-375810]
google_bigquery_dataset.dataset: Refreshing state... [id=projects/dtc-de-375810/datasets/trips_data_all]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # google_storage_bucket.data-lake-bucket must be replaced
-/+ resource "google_storage_bucket" "data-lake-bucket" {
      - default_event_based_hold    = false -> null
      ~ id                          = "dtc_data_lake_dtc-de-375810" -> (known after apply)
      - labels                      = {} -> null
      ~ name                        = "dtc_data_lake_dtc-de-375810" -> "dtc_data_lake_dtc-de-375810_de-zoomcamp-hw-2023-pg1" # forces replacement
      ~ project                     = "dtc-de-375810" -> (known after apply)
      ~ public_access_prevention    = "inherited" -> (known after apply)
      - requester_pays              = false -> null
      ~ self_link                   = "https://www.googleapis.com/storage/v1/b/dtc_data_lake_dtc-de-375810" -> (known after apply)
      ~ storage_class               = "REGIONAL" -> "STANDARD"
      ~ url                         = "gs://dtc_data_lake_dtc-de-375810" -> (known after apply)
        # (3 unchanged attributes hidden)

      ~ lifecycle_rule {

          - condition {
              - age                        = 30 -> null
              - days_since_custom_time     = 0 -> null
              - days_since_noncurrent_time = 0 -> null
              - matches_prefix             = [] -> null
              - matches_storage_class      = [] -> null
              - matches_suffix             = [] -> null
              - num_newer_versions         = 0 -> null
              - with_state                 = "ANY" -> null
            }
          + condition {
              + age                   = 30
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }

            # (1 unchanged block hidden)
        }

      + website {
          + main_page_suffix = (known after apply)
          + not_found_page   = (known after apply)
        }

        # (1 unchanged block hidden)
    }

Plan: 1 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_storage_bucket.data-lake-bucket: Destroying... [id=dtc_data_lake_dtc-de-375810]
google_storage_bucket.data-lake-bucket: Destruction complete after 0s
google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dtc_data_lake_dtc-de-375810_de-zoomcamp-hw-2023-pg1]
```

Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/S57Xs3HL9nB3YTzj9)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 26 January (Thursday), 22:00 CET


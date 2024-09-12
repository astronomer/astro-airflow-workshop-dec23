## Design Review - Introduction to Airflow and Astro

Welcome! 🚀

This project is an end-to-end pipeline showing how to implement an ELT pattern with [Apache Airflow®](https://airflow.apache.org/), intended for the demo as part of an Intro to Airflow or Intro to Astro design review. 

The pipeline extracts data from a mocked internal API, loads the raw data into [AWS S3](https://aws.amazon.com/s3/), and then loads the data into a Snowflake table to run transformations creating reporting tables for a [Streamlit dashboard](https://www.streamlit.io/). The pipeline also includes data quality checks that send a notification to [Slack](https://slack.com/) if they fail.


## Tools used

- [Apache Airflow®](https://airflow.apache.org/docs/apache-airflow/stable/index.html) running on [Astro](https://www.astronomer.io/product/). A [free trial](http://qrco.de/bfHv2Q) is available.
- [AWS S3](https://aws.amazon.com/s3/) for storing and archiving raw data.
- [Snowflake](https://www.snowflake.com/en/) for storing and querying transformed data.

Optional:

One of the DAGs contains data quality checks that send notifications to Slack if they fail. If you don't want to use Slack, remove the `on_failure_callback` from the `additional_data_quality_checks` task group in the [`load_to_snowflake](dags/load_to_snowflake.py) DAG on line 208.

- A [Slack](https://slack.com/) workspace with permissions to add a new app is needed for the Slack notification tasks.

## How to setup the demo environment

This demo is running on Astro - reach out to the DevRel team for more info. If you need to set up the demo locally, follow the steps below.

1. Install Astronomer's open-source local Airflow development tool, the [Astro CLI](https://www.astronomer.io/docs/astro/cli/overview).
2. Log into your AWS account and create [a new empty S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html). Make sure you have a set of [AWS credentials](https://docs.aws.amazon.com/iam/) with `AmazonS3FullAccess` for this new bucket.
3. Sign up for a [free trial](https://trial.snowflake.com/?owner=SPN-PID-365384) of Snowflake. Create a database called `design_reviews` with a schema called `dev`, as well as a warehouse called `my_wh`. You can use the following SQL commands to create these objects:

```sql
CREATE WAREHOUSE MY_WH;
CREATE DATABASE IF NOT EXISTS DESIGN_REVIEWS;
CREATE SCHEMA IF NOT EXISTS DESIGN_REVIEWS.DEV;
```

4. Create a role and give it the necessary permissions to access the Snowflake objects. You can use the following SQL commands to create the role and grant the necessary permissions:

```sql
CREATE ROLE my_demo_role;

GRANT USAGE ON WAREHOUSE MY_WH TO ROLE my_demo_role;
GRANT USAGE ON DATABASE DESIGN_REVIEWS TO ROLE my_demo_role;
GRANT USAGE ON SCHEMA DESIGN_REVIEWS.DEV TO ROLE my_demo_role;

GRANT ALL PRIVILEGES ON SCHEMA DESIGN_REVIEWS.DEV TO ROLE my_demo_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA DESIGN_REVIEWS.DEV TO ROLE my_demo_role;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA DESIGN_REVIEWS.DEV TO ROLE my_demo_role;
GRANT ALL PRIVILEGES ON ALL STAGES IN SCHEMA DESIGN_REVIEWS.DEV TO ROLE my_demo_role;
GRANT ALL PRIVILEGES ON FUTURE STAGES IN SCHEMA DESIGN_REVIEWS.DEV TO ROLE my_demo_role;
```

5. Create a key-pair by running the following command in your CLI. (If you are a Windows user you might need to install ssh-keygen or use a different tool, see the [Microsoft documentation](https://learn.microsoft.com/en-us/viva/glint/setup/sftp-ssh-key-gen).)

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f ~/.ssh/snowflake_rsa_key
```

6. Create a user for the demo and set your public key. You can do this by running the following SQL commands.

```sql
CREATE USER my_demo_user
    PASSWORD = '<PW>'
    DEFAULT_ROLE = my_demo_role
    MUST_CHANGE_PASSWORD = FALSE;

GRANT ROLE my_demo_role TO USER my_demo_user;

ALTER USER my_demo_user SET RSA_PUBLIC_KEY='<PUBLIC KEY>';
```

7. Create your stage in Snowflake. You can do this by running the following SQL command. Make sure to replace the placeholders with your own values.

```sql
USE DATABASE DESIGN_REVIEWS;
USE SCHEMA DEV;

CREATE OR REPLACE STAGE DEMO_STAGE
URL='s3://<YOUR BUCKET NAME>/my-stage/'
CREDENTIALS=(AWS_KEY_ID='<YOUR AWS ACCESS KEY>', AWS_SECRET_KEY='<YOUR AWS SECRET KEY')
FILE_FORMAT = (TYPE = 'CSV');

GRANT ALL PRIVILEGES ON ALL STAGES IN SCHEMA etl_demo.dev TO ROLE etl_demo_role;
```

8. Fork this repository and clone the code locally.

9. (Optional) Create a new Slack app and install it in your workspace. You can follow the instructions in the [Slack API documentation](https://api.slack.com/start). And retrieve an API token for the app.

### Run the project locally

1. Create a new file called `.env` in the root of the cloned repository and copy the contents of [.env_example](.env_example) into it. Fill out the placeholders with your own credentials for Snowflake, AWS, and Slack.

2. In the root of the repository, run `astro dev start` to start up the following Docker containers. 

3. Access the Airflow UI at `localhost:8080` and follow the DAG running instructions in the [Running the DAGs](#running-the-dags) section of this README.

## Running the DAGs

1. Unpause all DAGs in the Airflow UI by clicking the toggle to the left of the DAG name.
2. The `extract_from_api` DAG will start its first run automatically. All other DAGs are scheduled based on Datasets to run as soon as the required data is available.

Optional: Set up a streamlit app in Snowflake using the script in [include/streamlit_app.py](include/streamlit_app.py) to visualize the data.

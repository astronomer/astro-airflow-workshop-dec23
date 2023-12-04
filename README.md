Overview
========

This workshop is designed to give users an intro to Astro, Astronomer's flagship cloud product, as well as familiarize users with the latest features available in Airflow.

## Getting started

Ensure you have v1.19 of the Astronomer CLI installed. To complete the exercises, start Airflow on your local machine by running `astro dev start`. 

Refer to the instructions below for each exercise. All DAGs can run locally and on Astro without connecting to external systems. Possible solutions for DAG-related exercises can be found in the `solutions` folder, although for some exercises there are multiple ways to implement.

Consider using [Ask Astronomer](ask.astronomer.io) if you need additional guidance with any of the exercises.

## Part 1: Creating Deployments
In this section you will create multiple environments on Astro, from the Cloud UI and the API.

Feel free to use the following resources:

- [Create a deployment](https://docs.astronomer.io/astro/create-deployment)
- [Manage Deployments programmatically using deployment files](https://docs.astronomer.io/astro/manage-deployments-as-code#create-a-deployment-from-a-template-file)

### Exercise 1: Create a deployment from the Astro Cloud UI

Creating a Deployment only takes a couple of clicks in the Astro UI. Go to cloud.astronomer.io, sign in, and go to the `Data` workspace.

> Task: Create a new Airflow Deployment with a unique name. Use the default settings for sizing.

### Exercise 2: Update a deployment programmatically

You can also create and configure Deployments programmatically using Deployment files and Deployment template files. Deployment files are used to update the same Deployment programmatically, and Deployment template files are used to create new Deployments based on a single template. Managing Deployments with files is essential to automating Deployment management at scale.

> Task: Create a new Deployment file based on the Deployment you created in the previous step. Make a small change to the Deployment file and update your Deployment using the new configuration.


## Part 2: Airflow Deep Dive
In this section you will explore the newest features in Airflow, emphasizing datasets (Airflow 2.4) and setup/teardown tasks (Airflow 2.7). Make sure you have Airflow running locally using the Astro CLI before starting this section.

Feel free to use the following resources:

- [Datasets and Data-Aware Scheduling in Airflow guide](https://www.astronomer.io/guides/airflow-datasets/)
- [Setup/teardown tasks guide](https://docs.astronomer.io/learn/airflow-setup-teardown)

### Exercise 3: Use datasets to break up a monolithic DAG

In `dags/datasets` you will find a DAG called `exercise_3_datasets_mono_dag` (tagged with `exercise_3` in the Airflow UI) which suggests a weekend activity for you.

> Task: Break the monolithic DAG up into 2 (or more) seperate DAGs. Maintain the current dependencies using datasets.


### Exercise 4: Schedule a DAG using multiple datasets

In `dags/datasets` you will find the following DAGs (tagged with `exercise_4` in the Airflow UI):

- `exercise_4_datasets_producer_fast`: A DAG scheduled every 2 minutes writing a random number to a local file.
- `exercise_4_datasets_producer_slow`: A DAG scheduled to run every 5 minutes writing your estimated age (based on your name) to a local file.
- `exercise_4_datasets_consumer`: A DAG that should only run after both local files were updated to get a math fact!

> Task: Use datasets to schedule the dependencies between the DAGs. What happens when the faster producer DAG runs twice before the slower producer DAG runs?

### Exercise 5: Using setup/teardown tasks to clean up files

In `dags/setup-teardown` there is one DAG for exercise 6 (tagged `exercise_6` in the Airflow UI):

- `exercise_5_setup_teardown`: This DAG creates a local CSV, loads data to it, aggregates the data mimicing calculating a KPI, and then deletes the intermediate CSV. The DAG is parameterized with a `fetch_bad_data` so the user can mimic what happens to the workflow when bad data is loaded.

> Task: Update the DAG to use setup/teardown tasks so the CSV is cleaned up no matter what happens with the data that is loaded. Try running the DAG with `fetch_bad_data` toggled off and on both before and after you update with setup/teardown tasks to see how the behavior changes.

## Part 3: Deploying Code
In this section we'll go through the process of deploying code and the different options available for doing so.

Feel free to use the following docs as resources:

- [Deploy code to Astro](https://docs.astronomer.io/astro/deploy-code)


### Exercise 6: Deploy your local project to Astro
For this workshop, you'll use the Astro CLI to deploy code. Note that in a production setting, you will likely use CICD to deploy.

> Task: Deploy your local project to the Astro Airflow Deployment you created in Part 1 using the Astro CLI.

## Part 4: Cloud IDE

The Astro Cloud IDE is a cloud-based notebook-inspired IDE for writing and testing Airflow DAGs. It is useful for iterative development, data exploration, and writing DAGs without worrying about Airflow boilerplate code or local setup.

Feel free to use the following docs as resources:

- [Astro Cloud IDE overview](https://docs.astronomer.io/astro/cloud-ide)
- [Deploy a Cloud IDE project to Astro](https://docs.astronomer.io/astro/cloud-ide/deploy-project)

### Exercise 7: Develop an ETL pipeline with the Cloud IDE

> Task: Develop an ETL pipeline that analyzes endangered species data using the Cloud IDE. When you are finished, deploy the pipeline to your Astro Airflow Deployment using a dag-only deploy. You can find full instructions in `exercise-solutions/exercise_7_cloud_ide.md`.

## Part 5: Day 2 DAG Operations
Now that DAGs are deployed, we'll cover some of the Day 2 operations that Astro enables.

Feel free to use the following resources:

- [Astro alerts](https://docs.astronomer.io/astro/alerts)
- [Create Airflow connections in the Cloud UI](https://docs.astronomer.io/astro/create-and-link-connections)
- [Roll back to a previous deployment](https://docs.astronomer.io/astro/deploy-history)

### Exercise 8: Create an Astro alert

Astro alerts provide an additional layer of observability over Airflow's built-in alerting system. In the `dags/day-2-ops` folder you will find two DAGs to help highlight this functionality:

- `exercise_8_slow_failures`: This DAG is parameterized to run with user input. You can choose when you run the DAG to have a task fail, or another task miss an SLA.
- `exercise_8_alerts`: This DAG is the one we want to run if `exercise_8_slow_failures` has an issue. Note that while we are using a DAG Trigger to show alerts for this example, you can also configure other communication channels like Slack or Email.

> Task: Set up two alerts in your Astro deployment: a DAG failure alert for the `exercise_8_slow_failures`, and a task duration alert for the `sleep_for_minutes` task in `exercise_8_slow_failures`. For both alerts, trigger the `exercise_8_alerts` DAG as the communication channel. Try out the alerts by running the `exercise_8_slow_failures` with the `fail_dag` and `miss_sla` params.


### Exercise 9: Create a connection

The Astro connection management feature allows you to create Airflow connections in the Cloud UI that can be used across all your Airflow deployments. 

> Task: Create an HTTP connection called `http_<your-name>` in the workspace Environment, using the `generic` connection type and apply it to your deployment. In the host field, enter `http://api.open-notify.org/astros.json`. Next, override this connection for the `astronomer-deployment` with a different API host (`https://manateejokesapi.herokuapp.com/manatees/random/` is a good option that does not require a key). Use the `exercise_9_connection` DAG to test the connection in your deployment (note that you will need to update the connection name in the DAG).

### Exercise 10: Roll back a deployment

Let's say there was an issue with the DAG you deployed in Exercise 7 that could jeapradize your production instance. You need to remove the DAG from your Deployment while you figure out what the issue is. Deployment rollbacks can be used for this purpose.

> Task: Roll back your deployment to the version prior to deploying the DAG you wrote in the Cloud IDE in Exercise 7.


> Note: Deployment rollbacks are intended as a last resort if something goes wrong, and can be disruptive. Make sure to read [what happens during a deploy rollback](https://docs.astronomer.io/astro/deploy-history#what-happens-during-a-deploy-rollback) before initiating one to understand any potential consequences.

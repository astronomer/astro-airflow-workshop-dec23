"""Make this DAG into a DAG with a producing task."""

from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime
import requests

# Add your S3 Bucket and name
YOUR_NAME = "YOURNAME"

API = f"https://api.agify.io/?name={YOUR_NAME}"

age_estimate_dataset = Dataset("include/ex_2/age_estimate.txt")

with DAG(
    dag_id="exercise_2_solution_producer_slow",
    start_date=datetime(2022, 10, 1),
    schedule="*/5 * * * *",
    tags=["exercise_2", "datasets"],
    catchup=False
):

    @task
    def get_age_estimate():
        r = requests.get(API)
        return r.json()["age"]

    @task(outlets=[age_estimate_dataset])
    def create_object_locally(age_estimate):
        f = open("include/ex_2/age_estimate.txt", "w")
        f.write(f"{age_estimate}")
        f.close()

    create_object_locally(get_age_estimate())
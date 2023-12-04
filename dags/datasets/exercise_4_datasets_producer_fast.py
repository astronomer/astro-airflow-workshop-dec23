"""Make this DAG into a DAG with a producing task."""

from airflow import DAG, Dataset
from airflow.decorators import task
from datetime import datetime
import random

with DAG(
    dag_id="exercise_4_datasets_producer_fast",
    start_date=datetime(2022, 10, 1),
    schedule="*/2 * * * *",
    tags=["exercise_2", "datasets"],
    catchup=False
):

    @task
    def create_random_number():
        random_number = random.randint(0,100)
        return random_number

    @task
    def create_object_locally(random_number):
        f = open("include/ex_2/random_number.txt", "w")
        f.write(f"{random_number}")
        f.close()


    create_object_locally(create_random_number())

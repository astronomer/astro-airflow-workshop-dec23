"""Schedule this DAG on Datasets."""

from airflow import DAG, Dataset, XComArg
from airflow.decorators import task
import requests
from datetime import datetime
from os import listdir
from os.path import isfile, join

API = "http://numbersapi.com/"

age_estimate_dataset = Dataset("include/ex_2/age_estimate.txt")
random_number_dataset = Dataset("include/ex_2/random_number.txt")

with DAG(
    dag_id="exercise_4_solution_consumer",
    start_date=datetime(2022, 10, 1),
    schedule=[age_estimate_dataset, random_number_dataset],
    tags=["exercise_4", "datasets"],
    catchup=False
):

    @task
    def list_files_locally():
        filenames = [
            f for f in listdir("include/ex_2") 
            if isfile(join("include/ex_2", f))
        ]
        return filenames

    @task 
    def read_files_locally(filenames):
        num_sum = 0
        for filename in filenames:
            f = open(f"include/ex_2/{filename}", "r")
            file_content = f.read()
            num_sum += int(file_content)
            f.close()
        return num_sum

    @task
    def get_a_number_fact(num_sum):
        print(str(num_sum))
        r = requests.get(API + str(num_sum) + "/math")
        return r.text

    get_a_number_fact(read_files_locally(list_files_locally()))
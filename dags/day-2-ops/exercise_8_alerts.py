from airflow.decorators import dag, task
from datetime import datetime
import time


@dag(
    schedule_interval=None, 
    start_date=datetime(2022, 1, 1),
    catchup=False,
)
def exercise_8_alerts():

    @task
    def print_alert(**context):
        print("Something failed or took too long!")          

    print_alert = print_alert()

exercise_8_alerts()
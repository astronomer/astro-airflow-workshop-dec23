"""
Generate a report with the weather forecast for the cities and the population information.
"""

from airflow.decorators import dag, task
from airflow.models.dataset import Dataset
from airflow.timetables.datasets import DatasetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable
from pendulum import datetime

@dag(
    ### EXERCISE ###
    # Define a display name for this DAG.
    ### START CODE HERE ###

    ### END CODE HERE ###

    start_date=datetime(2024, 6, 1),

    ### EXERCISE ###
    # Define a schedule for this DAG to run both, every day at midnight UTC. 
    # AND whenever the Dataset("weather_data") AND Dataset("population_info") are updated.
    ### START CODE HERE ###

    schedule=None, 

    ### END CODE HERE ###

    catchup=False,
    doc_md=__doc__,

    ### EXERCISE ###
    # Define the default arguments for this DAG. Give it an owner and set the number of retries.

    ### START CODE HERE ###

    ### END CODE HERE ###
    tags=["exercise"],
)
def downstream_dag_ex():

    @task
    def get_cities_weather_table(**context):

        df = context["ti"].xcom_pull(
            dag_id="upstream_dag_1",
            task_ids="create_forecast_table",
            include_prior_dates=True,
        )

        return df

    @task
    def get_population_info(**context):

        pop_info = context["ti"].xcom_pull(
            dag_id="upstream_dag_2",
            task_ids="get_pop_birth_year",
            include_prior_dates=True,
        )

        return pop_info

    @task
    def generate_report(weather, pop_info):
        from tabulate import tabulate

        country = pop_info["country"]
        pop = pop_info["population"]
        year = pop_info["year"]

        print("Tomorrow's weather forecast for your cities:")
        print(tabulate(weather, headers="keys", tablefmt="grid", showindex=False))
        print(f"The population of {country} was {pop} in {year}.")

    weather = get_cities_weather_table()
    pop_info = get_population_info()

    generate_report(weather, pop_info)


downstream_dag_ex()

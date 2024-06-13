"""
Retrieve the population of a country in a specific year.
"""

from airflow.decorators import dag, task
from airflow.providers.http.operators.http import HttpOperator
from airflow.models.baseoperator import chain
from airflow.models.param import Param
from airflow.datasets import Dataset
from pendulum import datetime, duration
import logging

t_log = logging.getLogger("airflow.task")


@dag(
    dag_display_name="Upstream DAG 🌍",
    start_date=datetime(2024, 6, 1),
    schedule=None,
    max_consecutive_failed_dag_runs=10,
    catchup=False,
    doc_md=__doc__,
    default_args={
        "owner": "Astro",
        "retries": 3,
        "retry_delay": duration(minutes=1),
        "retry_exponential_backoff": True,
    },
    params={
        "my_country": Param(
            "United States",
            type="string",
            title="Country of interest:",
            description="Enter the country you want to retrieve population numbers for.",
        ),
        "my_year_of_birth": Param(
            1994,
            type="number",
            title="Year of birth",
            description="Enter your year of birth.",
        ),
        "simulate_task_delay": Param(
            0,
            type="number",
            title="Simulate task delay",
            description="Set the number of seconds to delay the last task of this DAG.",
        ),
    },
    tags=["example"],
)
def upstream_dag_2():

    get_country_info = HttpOperator(
        task_id="get_country_info",
        endpoint="countries/population",
        method="POST",
        http_conn_id="country_api_conn",
        log_response=True,
        data={
            "country": "{{ params.my_country }}",
        },
    )

    @task(outlets=[Dataset("population_info")])
    def get_pop_birth_year(country_info, **context):
        import json
        import time

        time.sleep(context["params"]["simulate_task_delay"])

        year_of_birth = context["params"]["my_year_of_birth"]
        data = json.loads(country_info)["data"]
        country = data["country"]
        pop_counts = data["populationCounts"]

        for entry in pop_counts:
            if entry["year"] == year_of_birth:
                print(f"Population of {country} in {year_of_birth}: {entry['value']}")
                return {
                    "country": country,
                    "population": entry["value"],
                    "year": year_of_birth,
                }
        print(f"No population data found for {country} in {year_of_birth}")
        return None

    chain(get_country_info, get_pop_birth_year(get_country_info.output))


upstream_dag_2()

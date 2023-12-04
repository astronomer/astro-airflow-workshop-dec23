from airflow.decorators import dag, task
from airflow.models.param import Param
from datetime import datetime
import time


@dag(
    schedule_interval=None, 
    start_date=datetime(2022, 1, 1),
    catchup=False,
    params= {"fail_dag": Param(False, type="boolean"),
            "miss_sla": Param(False, type="boolean")},
)
def exercise_8_slow_failures():

    @task
    def sleep_for_minutes(**context):
        miss_sla = context["params"]["miss_sla"]
        if miss_sla:
            time.sleep(300)
        else:
            return "DAG was fast!"

    @task
    def succeed_or_fail(**context):
        fail_dag = context["params"]["fail_dag"]
        if fail_dag:
            raise ValueError('Task failed')
        else:
            return 'DAG succeeded'
            

    sleep_task = sleep_for_minutes()
    succeed_or_fail = succeed_or_fail()

exercise_8_slow_failures()
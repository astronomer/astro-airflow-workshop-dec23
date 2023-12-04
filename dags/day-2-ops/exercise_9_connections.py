from airflow.decorators import dag
from airflow.providers.http.operators.http import SimpleHttpOperator
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.from_format("2023-06-29", "YYYY-MM-DD").in_tz("UTC"),
    catchup=False,
)
def exercise_9_connection():

    get_an_http_response = SimpleHttpOperator(
        method="GET",
        http_conn_id="http_default",
        log_response=True,
        task_id="get_an_http_response",
    )

dag_obj = exercise_9_connection()
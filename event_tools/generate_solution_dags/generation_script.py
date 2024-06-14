"""
Generates solutions DAGs with different DAG IDs.
"""

import os
import shutil
import fileinput

NUMBER_OF_SETS_TO_GENERATE = 3

template_upstream_dag_1_path = (
    f"{os.path.dirname(__file__)}/dag_templates/upstream_dag_1_template.py"
)
template_upstream_dag_2_path = (
    f"{os.path.dirname(__file__)}/dag_templates/upstream_dag_2_template.py"
)
template_downstream_dag_path = (
    f"{os.path.dirname(__file__)}/dag_templates/downstream_dag_template.py"
)

os.makedirs(f"{os.path.dirname(__file__)}/generated_solution_dags", exist_ok=True)

for i in range(NUMBER_OF_SETS_TO_GENERATE):
    os.makedirs(
        f"{os.path.dirname(__file__)}/generated_solution_dags/set_{i+1}", exist_ok=True
    )

    upstream_dag_1_id = f"upstream_dag_1_set_{i+1}"
    upstream_dag_2_id = f"upstream_dag_2_set_{i+1}"
    downstream_dag_id = f"downstream_dag_set_{i+1}"

    set_number = f"set_{i+1}"

    # Upstream DAG 1 file
    new_filepath_upstream_dag_1 = f"{os.path.dirname(__file__)}/generated_solution_dags/set_{i+1}/{upstream_dag_1_id}.py"
    shutil.copyfile(template_upstream_dag_1_path, new_filepath_upstream_dag_1)
    for line in fileinput.input(new_filepath_upstream_dag_1, inplace=True):
        line = line.replace("UPSTREAM_DAG_ID_1_TO_REPLACE", upstream_dag_1_id)
        line = line.replace("UPSTREAM_DAG_ID_2_TO_REPLACE", upstream_dag_2_id)
        line = line.replace("DOWNSTREAM_DAG_ID_TO_REPLACE", downstream_dag_id)
        line = line.replace("SET_NUMBER", set_number)
        print(line, end="")

    # Upstream DAG 2 file
    new_filepath_upstream_dag_2 = f"{os.path.dirname(__file__)}/generated_solution_dags/set_{i+1}/{upstream_dag_2_id}.py"
    shutil.copyfile(template_upstream_dag_2_path, new_filepath_upstream_dag_2)
    for line in fileinput.input(new_filepath_upstream_dag_2, inplace=True):
        line = line.replace("UPSTREAM_DAG_ID_1_TO_REPLACE", upstream_dag_1_id)
        line = line.replace("UPSTREAM_DAG_ID_2_TO_REPLACE", upstream_dag_2_id)
        line = line.replace("DOWNSTREAM_DAG_ID_TO_REPLACE", downstream_dag_id)
        line = line.replace("SET_NUMBER", set_number)
        print(line, end="")

    # Downstream DAG file
    new_filepath_upstream_dag_1 = f"{os.path.dirname(__file__)}/generated_solution_dags/set_{i+1}/{downstream_dag_id}.py"
    shutil.copyfile(template_downstream_dag_path, new_filepath_upstream_dag_1)
    for line in fileinput.input(new_filepath_upstream_dag_1, inplace=True):
        line = line.replace("UPSTREAM_DAG_ID_1_TO_REPLACE", upstream_dag_1_id)
        line = line.replace("UPSTREAM_DAG_ID_2_TO_REPLACE", upstream_dag_2_id)
        line = line.replace("DOWNSTREAM_DAG_ID_TO_REPLACE", downstream_dag_id)
        line = line.replace("SET_NUMBER", set_number)
        print(line, end="")

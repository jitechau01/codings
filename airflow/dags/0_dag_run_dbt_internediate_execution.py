from airflow import DAG
import os
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable

dbt_project_dir = Variable.get("dbt_project_dir", default_var=None)

PROJECT_DIR=dbt_project_dir
PROFILES_DIR='~/.dbt'


with DAG(
    dag_id='0_dag_run_dbt_internediate_execution',
    catchup=False,
    schedule=None,
    #schedule_interval='@once',
) as dag:
    
    with TaskGroup(group_id='dbt_tasks') as dbt_tasks:
        dbt_run = BashOperator(
            task_id='dbt_run',
            bash_command=f"""dbt run --project-dir {PROJECT_DIR} --profiles-dir {PROFILES_DIR}"""
        )
        
        dbt_run
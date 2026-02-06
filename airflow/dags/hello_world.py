from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


def print_hello():
    return 'Hello World!' 

with DAG(
    dag_id='hello_world', 
    catchup=False
    ) as dag:
    
    hello_python_task = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello
    )       
    
    hello_bash_task = BashOperator(
        task_id='bash_hello',
        bash_command='echo "Hello from Bash!"'
    )
    
    hello_python_task >> hello_bash_task
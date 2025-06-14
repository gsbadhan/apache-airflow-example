from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

## Testing failed task behaviour. Task-2 would be failed.

def task1():
    print(f"task-1 work done")

def task2():
    #breaking the flow
    c = (11/0)
    print(f"task-2 work done")

def task3():
    print(f"task-3 work done")    


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 2,
    "retry_delay": timedelta(minutes=2)
}


# Define the DAG
with DAG(
    dag_id='testing_failed_task',
    default_args=default_args,
    description='A simple DAG to perform math oprations on two numbers',
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=['example'],
) as dag:
    
    # Task 1
    task_1 = PythonOperator(
        task_id='task-1',
        python_callable=task1,
        op_kwargs={},  
    )

    # Task 2
    task_2 = PythonOperator(
        task_id='task-2',
        python_callable=task2,
        op_kwargs={},  
    )

    # Task 3
    task_3 = PythonOperator(
        task_id='task-3',
        python_callable=task3,
        op_kwargs={},  
    )


#  Define task dependencies (if you add more tasks)
task_1 >> task_2 >> task_3 
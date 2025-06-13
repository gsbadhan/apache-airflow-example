from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define the function to add numbers
def add_numbers(num1, num2):
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
    return result

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='add_two_numbers',
    default_args=default_args,
    description='A simple DAG to add two numbers',
    schedule_interval=None,  # Manual trigger only
    catchup=False,
    tags=['example'],
) as dag:

    # Task to add numbers
    add_task = PythonOperator(
        task_id='add_numbers_task',
        python_callable=add_numbers,
        op_kwargs={'num1': 5, 'num2': 3},  # Pass arguments here
    )

# Optional: Define task dependencies (if you add more tasks)
# add_task >> another_task
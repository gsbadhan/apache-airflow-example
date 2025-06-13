from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

## Create DAG of 4 tasks and send output to dependant tasks as input.
## div_task depends on add_task & mul_task
## sub_task depends on mul_task & div_task


# Define the function to add numbers
def add_numbers(**context):
    num1 = context["num1"]
    num2 = context["num2"]
    result = num1 + num2
    print(f"{num1} + {num2} = {result}")
    context['ti'].xcom_push(key='n1', value=result)
    return result

 #Define the function to multiple numbers
def mul_numbers(**context):
    num1 = context["num1"]
    num2 = context["num2"]
    result = num1 * num2
    print(f"{num1} * {num2} = {result}")
    context['ti'].xcom_push(key='n2', value=result)
    return result

#Define the function to divide numbers
def div_numbers(**context):
    num1 = context['ti'].xcom_pull(task_ids='add_task', key='n1')
    num2 = context['ti'].xcom_pull(task_ids='mul_task', key='n2')
    result = num1 / num2
    print(f"{num1} / {num2} = {result}")
    context['ti'].xcom_push(key='n1', value=result)
    return result

#Define the function to subtract numbers
def sub_numbers(**context):
    num1 = context['ti'].xcom_pull(task_ids='mul_task', key='n2')
    num2 = context['ti'].xcom_pull(task_ids='div_task', key='n1')
    result = num1 - num2
    print(f"{num1} - {num2} = {result}")
    return result

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='math_operations',
    default_args=default_args,
    description='A simple DAG to perform math oprations on two numbers',
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=['example'],
) as dag:

    # Task to add numbers
    add_task = PythonOperator(
        task_id='add_task',
        python_callable=add_numbers,
        op_kwargs={'num1': 5, 'num2': 3},  
    )


    # Task to multiplication numbers
    mul_task = PythonOperator(
        task_id='mul_task',
        python_callable=mul_numbers,
        op_kwargs={'num1': 6, 'num2': 4},  
    )

    # Task to divide numbers
    div_task = PythonOperator(
        task_id='div_task',
        python_callable=div_numbers
    )

    # Task to divide numbers
    sub_task = PythonOperator(
        task_id='sub_task',
        python_callable=sub_numbers
    )


#  Define task dependencies (if you add more tasks)
add_task >> div_task 
mul_task >> div_task

mul_task >> sub_task
div_task >> sub_task
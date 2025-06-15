from airflow.decorators import dag, task
from datetime import datetime

## Using airflow.decorators like @task, @dag etc.
## Create DAG of 4 tasks and send output to dependant tasks as input.
## div_numbers depends on add_numbers & mul_numbers
## sub_numbers depends on mul_numbers & div_numbers

default_args = {
    'owner': 'airflow',
    'retries': 2,  
    'start_date': datetime(2024, 1, 1),
}

@dag(
    dag_id='math_operations_decorator',
    default_args = default_args,
    schedule=None,
    catchup=False,
    tags=['example'],
)
def math_pipeline():

    @task(retries=default_args['retries'])
    def add_numbers(num1: int, num2: int) -> int:
        """Task 1: Add two static numbers"""
        result = num1 + num2
        print(f"ADD: {num1} + {num2} = {result}")
        return result

    @task(retries=default_args['retries'])
    def multiply_numbers(num1: int, num2: int) -> int:
        """Task 2: Multiply two static numbers"""
        result = num1 * num2
        print(f"MULTIPLY: {num1} * {num2} = {result}")
        return result

    @task(retries=default_args['retries'])
    def divide_numbers(add_result: int, multiply_result: int) -> float:
        """Task 3: Divide results from Task 1 & Task 2"""
        if multiply_result == 0:
            raise ValueError("Cannot divide by zero")
        result = add_result / multiply_result
        print(f"DIVIDE: {add_result} / {multiply_result} = {result}")
        return result

    @task(retries=default_args['retries'])
    def subtract_numbers(multiply_result: int, divide_result: float) -> float:
        """Task 4: Subtract results from Task 2 & Task 3"""
        result = multiply_result - divide_result
        print(f"SUBTRACT: {multiply_result} - {divide_result} = {result}")
        return result

    # Define workflow
    sum_result = add_numbers(5,3)
    product_result = multiply_numbers(5,3)
    division_result = divide_numbers(sum_result, product_result)
    final_result = subtract_numbers(product_result, division_result)

math_dag = math_pipeline()
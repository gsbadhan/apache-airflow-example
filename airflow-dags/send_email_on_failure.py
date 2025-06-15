from airflow.decorators import dag, task
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

## Using airflow.decorators like @task, @dag etc.
## Create DAG of 4 tasks and send output to dependant tasks as input.
## div_numbers depends on add_numbers & mul_numbers
## sub_numbers depends on mul_numbers & div_numbers

### add your own smtp configs in airflow.cfg
# [smtp]
# smtp_host = smtp.gmail.com
# smtp_starttls = True
# smtp_ssl = False
# smtp_user = your.email@gmail.com  # Your full Gmail address
# smtp_password = your_app_password  # See note below
# smtp_port = 587
# smtp_mail_from = your.email@gmail.com  # Same as smtp_user


default_args = {
    'owner': 'airflow',
    'retries': 2,  
    'start_date': datetime(2024, 1, 1),
    'on_retry_callback': None,
    "retry_delay": timedelta(minutes=2),
}

@dag(
    dag_id='send_email_on_failure',
    default_args = default_args,
    schedule=None,
    catchup=False,
    tags=['example'],
)
def math_pipeline():

    # Email task to be called on failures
    email_alert = EmailOperator(
        task_id='email_on_failure',
        to='gurpreet.badhan.28@gmail.com.',
        subject='ALert - Airflow Task Failed',
        html_content="""<h2>Task Failed</h2>
        <p>Task {{ ti.task_id }} failed after {{ ti.max_tries + 1 }} attempts.</p>
        <p>Execution Date: {{ ds }}</p>""",
        trigger_rule='one_failed'  # Runs if any upstream task fails
    )

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
    product_result = multiply_numbers(5,0)
    division_result = divide_numbers(sum_result, product_result)
    final_result = subtract_numbers(product_result, division_result)

    # Set email dependency
    [sum_result, product_result, division_result, final_result] >> email_alert

math_dag = math_pipeline()
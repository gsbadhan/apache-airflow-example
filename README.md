# apache-airflow-example
apache airflow examples


# install airflow with uv tool on mac
1. brew install uv
2. create folder in ~/ directory: mkdir airflow 
3. uv venv --python 3.11
4. source .venv/bin/activate
5. uv pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.11.txt"
6. start : airflow standalone
7. create dags folder in ~/airflow/ directory if not created by default : mkdir dags


# airflow access
1. UI : http://localhost:8080 


# how to deploy airflow code
1. Write DAG code(.py) in any IDE
2. Copy/Paste same DAG code(.py) file into ~/airflow/dags folder
3. Airflow automattically load new code, you can cross verify on airflow UI




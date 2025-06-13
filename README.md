# apache-airflow-example
apache airflow examples


# install airflow with uv tool on mac
1. brew install uv
2. create folder in ~/ directory: mkdir airflow 
3. uv venv --python 3.11
4. source .venv/bin/activate
5. uv pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.11.txt"
6. start : airflow standalone


# airflow access
1. UI : http://localhost:8080 



# for local development
1. Create folder venv : python -m venv venv
2. Activate the virtual environment on mac : source venv/bin/activate
3. Install dependencies : pip install -r requirements.txt
# apache-airflow-example
apache airflow examples


# install airflow with minikube and helm
1. minikube start --vm-driver=hyperkit --cpus 6 --memory 8192
2. kubectl create namespace airflow
3. helm install airflow apache-airflow/airflow --namespace airflow --set executor=LocalExecutor --set redis.enabled=false
4. kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow


# airflow access
1. UI : http://localhost:8080 


# uninstall 
1. helm uninstall airflow -n airflow
2. minikube delete


# for local development
1. Create folder venv : python -m venv venv
2. Activate the virtual environment on mac : source venv/bin/activate
3. Install dependencies : pip install -r requirements.txt
# FROM python:slim
FROM apache/airflow:latest
RUN 
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "elt_script.py"]
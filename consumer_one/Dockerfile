FROM python:3.10-slim-buster
WORKDIR /consumer_one
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer_one.py .
CMD ["python", "./consumer_one.py"]
FROM python:3.10-slim-buster
WORKDIR /consumer_four
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer_four.py .
CMD ["python", "./consumer_four.py"]
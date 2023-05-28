FROM python:3.10-slim-buster
WORKDIR /consumer_two
COPY . /consumer_two
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "consumer_two.py"]
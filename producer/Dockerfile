FROM python:3.10-slim-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
ENV FLASK_APP=producer.py
CMD ["flask", "run", "--host=0.0.0.0"]
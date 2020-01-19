FROM python:slim

COPY . /app
WORKDIR /app

RUN apt-get update -y && apt-get install python3 -y &&\
    apt-get install -y python-pip python-dev
RUN pip install -r requirements.txt
RUN flask db migrate
RUN flask db upgrade


CMD ["python3", "app.py"]
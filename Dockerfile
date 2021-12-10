FROM python:3.8.6-buster

COPY . /app
WORKDIR /app

RUN pip3 install --upgrade -r /app/requirements.txt

ENTRYPOINT ["python", "run.py"]

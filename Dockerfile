FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY ./app /code/app
COPY ./requirements.txt /code/requirements.txt
COPY ./corp_system.db /code/corp_system.db
COPY ./.env /code/.env
COPY ./venv /code/venv

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

EXPOSE 8000

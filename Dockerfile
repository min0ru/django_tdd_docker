FROM python:3.9.1-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update -y && \
    apt-get install -y netcat && \
    apt-get clean

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pipenv install --system --dev

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
FROM python:3.10.8-alpine3.17

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev curl

WORKDIR /usr/src/app/etl

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
CMD python main.py

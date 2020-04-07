FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt

#COPY . /usr/src/app
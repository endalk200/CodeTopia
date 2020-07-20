
FROM python:3

LABEL Author="CodeTopia"

ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app

ADD requirement.txt /usr/src/app

RUN pip install -r requirement.txt

ADD . /usr/src/app

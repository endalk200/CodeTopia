<<<<<<< HEAD
FROM python:3

# set work directory
WORKDIR /usr/src/app

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install pillow dependencies
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

# install psql client
RUN apk --update add postgresql-client

# install git
RUN apk add git

# install dependencies
RUN pip install --upgrade pip

RUN pip install pipenv

ADD Pipfile* ./
RUN pipenv lock --requirements > requirements.txt

RUN pip install -r requirements.txt

# copy project
ADD . .

# run docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
=======
FROM python:3

# USER app
ENV PYTHONUNBUFFERED 1
# RUN mkdir /db
#RUN chown app:app -R /db

RUN mkdir /code
WORKDIR /code

RUN pip install pipenv

ADD Pipfile* /code/
RUN pipenv lock --requirements > requirements.txt

RUN pip install -r requirements.txt
ADD . /code/
>>>>>>> master

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
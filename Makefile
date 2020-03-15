

server:
	python manage.py runserver

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

migrate_all: makemigrations
	python manage.py migrate

compile_sass:
	sass ./static/scss/main.scss ./static/scss/main.css --style=compressed

compile_ts:
	npm run webpack

minify_js:
	npm run compile_mini_ts

local_test:
	coverage erase
	flake8
	coverage run manage.py test
	coverage report
	coverage html

travis_test:
	flake8
	python manage.py test

dump_data:
	python manage.py dumpdata --all --force-color --indent 4 --output dumped_data.json

load_data:
	python manage.py loaddata dumped_data.json --format=json

createsuperuser:
	python manage.py createsuperuser --username root --email example@gmail.com
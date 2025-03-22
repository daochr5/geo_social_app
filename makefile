save-requirements:
	pip freeze > requirements.txt

run-server:
	python manage.py runserver
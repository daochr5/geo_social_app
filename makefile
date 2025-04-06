save-requirements:
	pip freeze > requirements.txt

install-requirements:
	pip install -r requirements.txt

run-server:
	python manage.py runserver
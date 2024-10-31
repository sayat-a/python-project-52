runserver_render:
	poetry run python3 manage.py migrate && poetry run python3 manage.py runserver 0.0.0.0:$(PORT)

runserver:
	poetry run python3 manage.py runserver

test:
	poetry run python3 manage.py test

translate:
	poetry run django-admin makemessages -l ru

complile_translation:
	poetry run python manage.py compilemessages

runserver_render:
	poetry run python3 manage.py runserver 0.0.0.0:$(PORT)

runserver:
	poetry run python3 manage.py runserver

test:
	poetry run python3 manage.py test
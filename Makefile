test:
	source venv/bin/activate && py.test tests

start:
	source venv/bin/activate && FLASK_APP=main/main.py flask run

db:
	docker run --name postgres-d -p 5432:5432 -e POSTGRES_DB='cajitos' -e POSTGRES_PASSWORD='password' -d postgres:9.5.6

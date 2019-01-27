test:
	source venv/bin/activate && py.test tests

start:
	source venv/bin/activate && FLASK_APP=cajitos_site flask run

start_debug:
	source venv/bin/activate && python app.py

init_test_env:
	docker-compose -f docker-compose-test.yml up -d
	sleep 1
	docker-compose -f docker-compose-test.yml exec postgres psql -U postgres -c 'CREATE DATABASE "test"' || true

stop_test_env:
	docker-compose -f docker-compose-test.yml stop

remove_test_env:
	docker-compose -f docker-compose-test-env.yml down

init_db:
	source venv/bin/activate && python init_db.py

db:
	docker run --name postgres-cajitos -p 5432:5432 -e POSTGRES_DB='cajitos' -e POSTGRES_PASSWORD='password' -d postgres:9.5.6

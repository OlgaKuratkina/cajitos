test:
	CONFIG=app.settings.tests source venv/bin/activate && py.test

start:
	source venv/bin/activate && FLASK_APP=cajitos_site flask run

babel_gen:
	source venv/bin/activate && pybabel extract -F babel.cfg -k _l -o translate_mapping.pot .

babel_translate:
	source venv/bin/activate && pybabel init -i translate_mapping.pot -d cajitos_site/translations -l ru
	source venv/bin/activate && pybabel init -i translate_mapping.pot -d cajitos_site/translations -l es

babel_update:
	source venv/bin/activate && pybabel update -i translate_mapping.pot -d cajitos_site/translations

babel_compile:
	source venv/bin/activate && pybabel compile -d cajitos_site/translations

start_debug:
	source venv/bin/activate && python app.py

init_test_env:
	docker-compose -f docker-compose-test.yml up -d
	sleep 1
	docker-compose -f docker-compose-test.yml exec postgres psql -U postgres -c 'CREATE DATABASE "postgres"' || true

stop_test_env:
	docker-compose -f docker-compose-test.yml stop

remove_test_env:
	docker-compose -f docker-compose-test-env.yml down

init_db:
	source venv/bin/activate && python init_db.py

db:
	docker run --name postgres-cajitos -p 5432:5432 -e POSTGRES_DB='postgres' -e POSTGRES_PASSWORD='password' -d postgres:9.5.6

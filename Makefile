run:
	docker-compose up --build -d
	docker-compose exec api python -m alembic upgrade head

stop:
	docker-compose stop
	docker-compose rm

test-base:
	docker-compose -f docker-compose-test.yaml up --build -d
	export TEST=1
	python -m alembic upgrade head

stop-test-base:
	docker-compose -f docker-compose-test.yaml stop
	docker-compose -f docker-compose-test.yaml rm
	unset TEST


test: test-base
	python -m pytest
	stop-test-base


logs:
	docker-compose logs api


.PHONY: run stop test logs
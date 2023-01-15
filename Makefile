run:
	docker-compose up --build -d
	docker-compose exec api python -m alembic upgrade head

stop:
	docker-compose stop
	docker-compose rm

test-base:
	docker-compose -f docker-compose-test.yaml up --build -d


stop-test-base:
	docker-compose -f docker-compose-test.yaml stop
	docker-compose -f docker-compose-test.yaml rm

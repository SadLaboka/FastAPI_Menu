run:
	docker-compose up --build -d

stop:
	docker-compose stop
	docker-compose rm


test:
	docker-compose -f docker-compose-test.yaml up --build


logs:
	docker-compose logs api


.PHONY: run stop test logs

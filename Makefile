build:
	docker-compose up --build

cache-clear:
	docker-compose rm -f

down:
	docker-compose down

run:
	docker-compose up

list:
	docker-compose ps

log:
	docker-compose logs
.PHONY: help

help:
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "\033[36m%-22s\033[0m %s\n", $$1, $$NF }' $(MAKEFILE_LIST)

.PHONY: build up down bash production console db migrate seed clean-all clean-volumes

build:         docker/build         ## docker-compose build
up:            docker/up            ## docker-compose up -d
down:          docker/down          ## docker-compose down
bash:          docker/bash          ## docker-compose exec app bash
production:    docker/production    ## docker-compose for pruduction ready
console:       django/shell         ## python manage.py shell
db:	   		   db/shell				## psql
migrate:       django/migrate       ## python manage.py migrate
seed:          django/seed          ## python manage.py loaddata
flush:         django/flush         ## python manage.py flush --no-input
clean-all:     docker/clean-all     ## docker-compose down --rmi all --volumes
clean-volumes: docker/clean-volumes ## docker-compose down --volumes

# If projects docker network exists
# NETWORK_NAME = example
# And add below command in 'docker/up'
# @if [ -z "`docker network ls | grep $(NETWORK_NAME)`" ]; then docker network create $(NETWORK_NAME); fi
# And add below command in 'docker/down'
# @if [ -n "`docker network inspect $(NETWORK_NAME) | grep \"\\"Containers\\": {}\"`" ]; then docker network rm $(NETWORK_NAME); fi


docker/build:
	@docker-compose build --no-cache

docker/clean-all:
	@docker-compose down --rmi all --volumes

docker/clean-volumes:
	@docker-compose down --volumes

docker/up:
	@docker-compose up -d

docker/down:
	@docker-compose down

docker/bash: docker/up
	@docker-compose exec app bash

docker/production:
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec -T app python manage.py migrate
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec -T app python manage.py collectstatic --noinput
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

django/migrate: docker/up
	@docker-compose exec app python manage.py migrate

django/seed: docker/up
	@docker-compose exec app python manage.py loaddata fixtures/fixtures.json

django/flush: docker/up
	@docker-compose exec app python manage.py flush --no-input

django/shell: docker/up
	@docker-compose exec app python manage.py shell

db/shell: docker/up
	@docker-compose exec db bash -c 'psql -H $$DATABASE_HOST -U $$POSTGRES_USER -d $$POSTGRES_DB'

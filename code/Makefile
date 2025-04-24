testing:
	python eda/explore_dataset.py
test2:
	python eda/test.py
#just tells to run command instead of looking for a specific cli file
#TODO: figure this out
.PHONY: cli
cli:
	python -m backend.app.main.py

sql:
	psql -U craivings_user -d db_craivings #-f /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/schema/schema.sql

down:
	docker-compose down

backend:
	docker-compose build backend
	docker-compose up backend

#figure this out with dockerfile in backend

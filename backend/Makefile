PYTHON = python3
SCRIPT_PATH = backend/app/db/load_json.py
PROJECT_ROOT = $(shell pwd)
NEON="postgresql://neondb_owner:npg_2Ul5ykzTcRNX@ep-round-wave-a4ppyklf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
##npx create-next-app frontend
#http://127.0.0.1:8000/
reload:
	uvicorn main:app --reload


#export local to json/csv
csv:
	psql -h localhost -U craivings_user -d db_craivings -f /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/to_csv.sql

import:
	psql $(NEON) -f /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/to_neon.sql


#neon
#psql database related shortcuts
db:
	psql $(NEON)

db-new:
	psql $(NEON) -f backend/app/db/schema.sql

trigger:
	psql $(NEON) -f backend/app/db/triggers.sql

db-data:
	 PYTHONPATH=/Users/rheekang/docker_projects/crAIvings/code python /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/load_json.py

db-size:
	 du -sh /Users/rheekang/docker_projects/crAIvings/code/data/clean/all_data.json


#local psql db
local:
	psql -U craivings_user -d db_craivings

local-db-new:
	psql -U craivings_user -d db_craivings -f /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/schema.sql

local-db-data:
	PYTHONPATH=/Users/rheekang/docker_projects/crAIvings/code python /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/load_json.py


#frontend
#npm init -y
#npm install react react-dom react-router-dom
#npm install axios

start:
	npm start




#docker related shortcuts
down:
	docker-compose down

backend:
	docker-compose build backend



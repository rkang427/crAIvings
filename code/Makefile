PYTHON = python3
SCRIPT_PATH = backend/app/db/load_json.py
PROJECT_ROOT = $(shell pwd)

#psql database related shortcuts
db-up:
	psql "postgresql://neondb_owner:npg_2Ul5ykzTcRNX@ep-round-wave-a4ppyklf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require" -f backend/app/db/schema.sql

trigger:
	psql "postgresql://neondb_owner:npg_2Ul5ykzTcRNX@ep-round-wave-a4ppyklf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require" -f backend/app/db/triggers.sql

db:
	psql "postgresql://neondb_owner:npg_2Ul5ykzTcRNX@ep-round-wave-a4ppyklf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

db-data:
	PYTHONPATH=. python backend/app/db/load_json.py


#docker related shortcuts

down:
	docker-compose down

backend:
	docker-compose build backend

#figure this out with dockerfile in backend



#app related shortcuts
reload:
	uvicorn code.backend.app.main:app --reload
local-sql:
	psql -U craivings_user -d db_craivings #-f /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/schema/schema.sql


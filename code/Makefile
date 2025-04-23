testing:
	python eda/explore_dataset.py
test2:
	python eda/test.py
#just tells to run command instead of looking for a specific cli file
.PHONY: cli
cli:
	docker compose run --rm backend

sql:
	psql -U craivings_user -d db_craivings

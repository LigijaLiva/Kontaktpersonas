.PHONY: init_db migrate_db test run

init_db:
	python main.py

migrate_db:
	mysql -u$(user) -p$(password) $(database) < migrations/create_contacts_table.sql

test:
	pytest tests/

run:
	python main.py

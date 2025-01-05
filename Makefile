.PHONY: init_db migrate_db test

init_db:
    python main.py

migrate_db:
    python migrate.py

test:
    pytest tests/

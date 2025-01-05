.PHONY: init_db test

init_db:
	python main.py

test:
	pytest tests/

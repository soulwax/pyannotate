# File: Makefile

.PHONY: format lint test

format:
	black .

lint:
	pylint src/pyannotate tests > pylint.txt

test:
	pytest --cov=pyannotate tests/ > pytest.txt

check: format lint test

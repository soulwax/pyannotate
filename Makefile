# File: Makefile

.PHONY: format lint test

format:
	black .

lint:
	pylint src/annot8 tests > pylint.txt

test:
	pytest --cov=annot8 tests/ > pytest.txt

check: format lint test

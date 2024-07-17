install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

PyYAML:
	pip install PyYAML

dependencies:
	pip install pytest
	pip install pytest-cov
	python3 -m pip install coverage

package-install:
	python3 -m pip install --user dist\hexlet_code-0.1.0-py3-none-any.whl

test-coverage:
	pytest --cov=gendiff tests/

lint:
	poetry run flake8 gendiff
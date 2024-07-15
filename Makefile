install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

dependencies:
	pip install PyYAML
	pip install pytest
	pip install pytest-cov

package-install:
	python3 -m pip install --user dist\hexlet_code-0.1.0-py3-none-any.whl

test-coverage:
	pytest --cov=gendiff tests/

lint:
	poetry run flake8 gendiff
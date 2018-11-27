init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	# Run unit tests, fail if coverage falls below 85%
	pipenv run pytest --cov serverlessrepo --cov-report term-missing --cov-fail-under 85 tests/unit

flake:
	# Make sure code conforms to PEP8 standards
	pipenv run flake8 serverlessrepo
	# Ignore missing docstring errors for tests
	pipenv run flake8 tests --ignore=D100,D101,D102,D103,D104

lint:
	# Linter performs static analysis to catch latent bugs
	pipenv run pylint --rcfile .pylintrc serverlessrepo
	# Ignore missing docstring errors for tests
	pipenv run pylint --rcfile .pylintrc tests --disable=C0111

# Command to run everytime you make changes to verify everything works
build: flake lint test

# Verifications to run before sending a pull request
pr: init build

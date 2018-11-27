init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	# Run unit tests, fail if coverage falls below 95%
	pipenv run pytest --cov serverlessrepo --cov-report term-missing --cov-fail-under 95 tests/unit

flake:
	# Make sure code conforms to PEP8 standards
	pipenv run flake8 serverlessrepo
	pipenv run flake8 tests

lint:
	# Linter performs static analysis to catch latent bugs
	pipenv run pylint --rcfile .pylintrc serverlessrepo

# Command to run everytime you make changes to verify everything works
build: flake lint test

# Verifications to run before sending a pull request
pr: init build

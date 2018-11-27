## AWS Serverless Application Repository - Python

A Python library with convenience helpers for working with the [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/).

## Installation
* Simply use pip to install the library:
    * `pip install serverlessrepo`

## Basic Usage
### Publish Applications
* publish_application - Given an [AWS Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md) template, it publishes a new application using the specified metadata in AWS Serverless Application Repository. If the application already exists, it publishes a new application version.
* publish_application_metadata - Parses the application metadata from the SAM template and updates the application.

### Manage Application Permissions
* make_application_public - Makes an application public so that it's visible to everyone.
* make_application_private - Makes an application private so that it's only visible to the owner.
* share_application_with_accounts - Shares the application with specified AWS accounts.

## Development
* Clone the project to your local:
    * `git clone https://github.com/awslabs/aws-serverlessrepo-python.git`
* Set up the environment: `make init`
    * It installs [Pipenv](https://github.com/pypa/pipenv) to manage package dependencies. Then it creates a virtualenv and installs dependencies from [Pipfile](./Pipfile) (including dev).
* Install new packages: `pipenv install [package names]`
    * Pipenv will automatically update [Pipfile](./Pipfile) and [Pipfile.lock](./Pipfile.lock) for you.
    * Add new dependencies to [setup.py](./setup.py) install_requires if they are needed for consumers of this library.
* Verfiy that everything works: `make build`
    * You can run `make tests` separately to verify that tests pass.
    * Check code style with `make flake` and `make lint`.
* Make code changes, run all verifications again before sending a Pull Request: `make pr`

## License

This library is licensed under the Apache 2.0 License.

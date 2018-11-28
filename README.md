# AWS Serverless Application Repository - Python

A Python library with convenience helpers for working with the [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/).

## Installation
* Simply use pip to install the library:
    * `pip install serverlessrepo`

## Basic Usage
The serverlessrepo module provides a simple interface for publishing applications and managing application permissions. To get started, import the serverlessrepo module:
```
import serverlessrepo
```

### Publish Applications
#### publish_application(template)
Given an [AWS Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md) template, it publishes a new application using the specified metadata in AWS Serverless Application Repository. If the application already exists, it publishes a new application version.

#### publish_application_metadata(template, application_id)
Parses the application metadata from the SAM template and updates the application.

#### Examples
Publish an application using local file template.yaml:
```
from serverlessrepo import publish_application

with open('template.yaml', 'r') as f:
    template = f.read()
    publish_application(template)
```

Or updates the application's metadata using template.yaml:
```
from serverlessrepo import publish_application_metadata

with open('template.yaml', 'r') as f:
    template = f.read()
    application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'
    publish_application_metadata(template, application_id)
```

### Manage Application Permissions
#### make_application_public(application_id)
Makes an application public so that it's visible to everyone.

#### make_application_private(application_id)
Makes an application private so that it's only visible to the owner.

#### share_application_with_accounts(application_id, account_ids)
Shares the application with specified AWS accounts.

#### Examples
```
from serverlessrepo import (
    make_application_public,
    make_application_private,
    share_application_with_accounts
)

application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'

# Share an application publicly
make_application_public(application_id)

# Make an application private
make_application_private(application_id)

# Share an application with other AWS accounts
share_application_with_accounts(application_id, ['123456789013', '123456789014'])
```

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

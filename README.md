# AWS Serverless Application Repository - Python

A Python library with convenience helpers for working with the [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/).

## Installation

Simply use pip to install the library:

```text
pip install serverlessrepo
```

## Basic Usage

The serverlessrepo module provides a simple interface for publishing applications and managing application permissions. To get started, import the serverlessrepo module:

```python
import serverlessrepo
```

### Publish Applications

#### publish_application(template, sar_client)

Given an [AWS Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md) template, it publishes a new application using the specified metadata in AWS Serverless Application Repository. If the application already exists, it updates metadata of the application and publishes a new version if specified in the template.

For example:

```python
import boto3
from serverlessrepo import publish_application

sar_client = boto3.client('serverlessrepo', region_name='us-east-1')

with open('template.yaml', 'r') as f:
    template = f.read()
    # if sar_client is not provided, we will initiate the client using region inferred from aws configurations
    output = publish_application(template, sar_client)
    print (output)
```

The output of `publish_application` has the following structure:

```text
{
    'application_id': 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app',
    'actions': ['CREATE_APPLICATION'],
    'details': {
        'Author': 'user1',
        'Description': 'hello',
        'Name': 'hello-world',
        'SemanticVersion': '0.0.1',
        'SourceCodeUrl': 'https://github.com/hello'}
    }
}
```

There are three possible values for the `actions` field:

* `['CREATE_APPLICATION']` - Created a new application.
* `['UPDATE_APPLICATION']` - Updated metadata of an existing application.
* `['UPDATE_APPLICATION', 'CREATE_APPLICATION_VERSION']` - Updated metadata of an existing application and created a new version, only applicable if a new SemanticVersion is provided in the input template.

`details` has different meaning based on the `actions` taken:

* If a new application is created, it shows metadata values used to create the application.
* If application is updated, it shows updated metadata values.
* If application is updated and new version is created, it shows updated metadata values as well as the new version number.

#### update_application_metadata(template, application_id, sar_client)

Parses the application metadata from the SAM template and only updates the metadata.

For example:

```python
import boto3
from serverlessrepo import update_application_metadata

sar_client = boto3.client('serverlessrepo', region_name='us-east-1')

with open('template.yaml', 'r') as f:
    template = f.read()
    application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'
    # if sar_client is not provided, we will initiate the client using region inferred from aws configurations
    update_application_metadata(template, application_id, sar_client)
```

### Manage Application Permissions

#### make_application_public(application_id, sar_client)

Makes an application public so that it's visible to everyone.

#### make_application_private(application_id, sar_client)

Makes an application private so that it's only visible to the owner.

#### share_application_with_accounts(application_id, account_ids, sar_client)

Shares the application with specified AWS accounts.

#### Examples

```python
import boto3
from serverlessrepo import (
    make_application_public,
    make_application_private,
    share_application_with_accounts
)

application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'
sar_client = boto3.client('serverlessrepo', region_name='us-east-1')

# Share an application publicly
make_application_public(application_id, sar_client)

# Make an application private
make_application_private(application_id, sar_client)

# Share an application with other AWS accounts
share_application_with_accounts(application_id, ['123456789013', '123456789014'], sar_client)
```

## Development

* Fork the repository, then clone to your local:
  * `git clone https://github.com/<username>/aws-serverlessrepo-python.git`
* Set up the environment: `make init`
  * It installs [Pipenv](https://github.com/pypa/pipenv) to manage package dependencies. Then it creates a virtualenv and installs dependencies from [Pipfile](./Pipfile) (including dev).
* Install new packages: `pipenv install [package names]`
  * Pipenv will automatically update [Pipfile](./Pipfile) and [Pipfile.lock](./Pipfile.lock) for you.
  * Add new dependencies to [setup.py](./setup.py) install_requires if they are needed for consumers of this library.
* Verify that everything works: `make build`
  * You can run `make tests` separately to verify that tests pass.
  * Check code style with `make flake` and `make lint`.
* Make code changes, run all verifications again before sending a Pull Request: `make pr`

## License

This library is licensed under the Apache 2.0 License.

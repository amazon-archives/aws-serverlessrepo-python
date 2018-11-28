import boto3
from botocore.exceptions import ClientError

from .parser import parse_template, get_app_metadata, parse_application_id

SERVERLESSREPO = boto3.client('serverlessrepo')


def publish_application(template):
    """
    This function publishes the application

    :param template: A packaged YAML or JSON SAM template
    :type template: str
    :return: Dictionary containing application id and version
    :rtype: dict
    :raises ValueError
    """
    if not template:
        raise ValueError('Require SAM template to publish the application')

    template_dict = parse_template(template)
    app_metadata = get_app_metadata(template_dict)

    try:
        request = _create_application_request(app_metadata, template)
        response = SERVERLESSREPO.create_application(**request)
        application_id = response['ApplicationId']
    except ClientError as e:
        if not _is_conflict_exception(e):
            raise

        # Update the application if it already exists
        error_message = e.response['Error']['Message']
        application_id = parse_application_id(error_message)
        request = _update_application_request(app_metadata, application_id)
        SERVERLESSREPO.update_application(**request)

        # Create an application version
        request = _create_application_version_request(app_metadata, application_id, template)
        SERVERLESSREPO.create_application_version(**request)

    return {
        'application_id': application_id,
        'semantic_version': app_metadata.semantic_version
    }


def publish_application_metadata(template, application_id):
    """
    This function updates the application metadata

    :param template: A packaged YAML or JSON SAM template
    :type template: str
    :param application_id: The Amazon Resource Name (ARN) of the application
    :type application_id: str
    :raises ValueError
    """
    if not template or not application_id:
        raise ValueError('Require SAM template and application ID to update application metadata')

    template_dict = parse_template(template)
    app_metadata = get_app_metadata(template_dict)
    request = _update_application_request(app_metadata, application_id)
    SERVERLESSREPO.update_application(**request)


def _create_application_request(app_metadata, template):
    """
    This function constructs the request body to create application

    :param app_metadata: Object containing app metadata
    :type app_metadata: ApplicationMetadata
    :param template: A packaged YAML or JSON SAM template
    :type template: str
    :return: SAR CreateApplication request body
    :rtype: dict
    """
    app_metadata.validate(['author', 'description', 'name'])
    request = {
        'Author': app_metadata.author,
        'Description': app_metadata.description,
        'HomePageUrl': app_metadata.home_page_url,
        'Labels': app_metadata.labels,
        'LicenseUrl': app_metadata.license_url,
        'Name': app_metadata.name,
        'ReadmeUrl': app_metadata.readme_url,
        'SemanticVersion': app_metadata.semantic_version,
        'SourceCodeUrl': app_metadata.source_code_url,
        'SpdxLicenseId': app_metadata.spdx_license_id,
        'TemplateBody': template
    }
    # Remove None values
    return {k: v for k, v in request.items() if v}


def _update_application_request(app_metadata, application_id):
    """
    This function constructs the request body to update application

    :param app_metadata: Object containing app metadata
    :type app_metadata: ApplicationMetadata
    :param application_id: The Amazon Resource Name (ARN) of the application
    :type application_id: str
    :return: SAR UpdateApplication request body
    :rtype: dict
    """
    request = {
        'ApplicationId': application_id,
        'Author': app_metadata.author,
        'Description': app_metadata.description,
        'HomePageUrl': app_metadata.home_page_url,
        'Labels': app_metadata.labels,
        'ReadmeUrl': app_metadata.readme_url
    }
    return {k: v for k, v in request.items() if v}


def _create_application_version_request(app_metadata, application_id, template):
    """
    This function constructs the request body to create application version

    :param app_metadata: Object containing app metadata
    :type app_metadata: ApplicationMetadata
    :param application_id: The Amazon Resource Name (ARN) of the application
    :type application_id: str
    :param template: A packaged YAML or JSON SAM template
    :type template: str
    :return: SAR CreateApplicationVersion request body
    :rtype: dict
    """
    app_metadata.validate(['semantic_version'])
    request = {
        'ApplicationId': application_id,
        'SemanticVersion': app_metadata.semantic_version,
        'SourceCodeUrl': app_metadata.source_code_url,
        'TemplateBody': template
    }
    return {k: v for k, v in request.items() if v}


def _is_conflict_exception(e):
    """
    This function checks whether the boto3 ClientError is ConflictException

    :param e: boto3 exception
    :type e: ClientError
    :return: True if e is ConflictException
    """
    error_code = e.response['Error']['Code']
    return error_code == 'ConflictException'

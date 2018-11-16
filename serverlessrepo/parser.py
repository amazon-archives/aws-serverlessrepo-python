from .application_metadata import ApplicationMetadata
from .exceptions import ApplicationMetadataNotFoundError

METADATA = 'Metadata'
SERVERLESS_REPO_APPLICATION = 'AWS::ServerlessRepo::Application'


def parse_template(template_str):
    """
    This function parses the SAM template

    :param template_str: A packaged YAML or json CloudFormation template
    :type template_str: str
    :return: Dictionary with keys defined in the template
    :rtype: dict
    """
    return {}


def get_app_metadata(template_dict):
    """
    This function gets the application metadata from a SAM template

    :param template_dict: SAM template as a dictionary
    :type template_dict: dict
    :return: Application metadata as defined in the template
    :rtype: ApplicationMetadata
    """
    if METADATA in template_dict and SERVERLESS_REPO_APPLICATION in template_dict[METADATA]:
        app_metadata_dict = template_dict[METADATA][SERVERLESS_REPO_APPLICATION]
        return ApplicationMetadata(app_metadata_dict)
    else:
        raise ApplicationMetadataNotFoundError(
            error_message='missing {} section in template Metadata'.format(SERVERLESS_REPO_APPLICATION))

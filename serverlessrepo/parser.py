from .application_metadata import ApplicationMetadata
from .exceptions import ApplicationMetadataNotFoundError

METADATA = 'Metadata'
SERVERLESS_REPO_APPLICATION = 'AWS::ServerlessRepo::Application'


def parse_sam_template(template):
    """
    This function parses the SAM template

    :param template: A packaged YAML or json SAM template
    :type template: str
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
    try:
        app_metadata_dict = template_dict[METADATA][SERVERLESS_REPO_APPLICATION]
        return ApplicationMetadata(app_metadata_dict)
    except KeyError as e:
        raise ApplicationMetadataNotFoundError(
            error_message='missing {} section'.format(e.args[0]))

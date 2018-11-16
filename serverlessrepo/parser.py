"""
Helper to parse JSON/YAML SAM template and dump YAML files
"""

import json
import six
import yaml
from yaml.resolver import ScalarNode, SequenceNode

from .application_metadata import ApplicationMetadata
from .exceptions import ApplicationMetadataNotFoundError

METADATA = 'Metadata'
SERVERLESS_REPO_APPLICATION = 'AWS::ServerlessRepo::Application'


def intrinsics_multi_constructor(loader, tag_prefix, node):
    """
    YAML constructor to parse CloudFormation intrinsics.
    This will return a dictionary with key being the instrinsic name
    """

    # Get the actual tag name excluding the first exclamation
    tag = node.tag[1:]

    # Some intrinsic functions doesn't support prefix "Fn::"
    prefix = 'Fn::'
    if tag in ['Ref', 'Condition']:
        prefix = ''

    cfntag = prefix + tag

    if tag == 'GetAtt' and isinstance(node.value, six.string_types):
        # ShortHand notation for !GetAtt accepts Resource.Attribute format
        # while the standard notation is to use an array
        # [Resource, Attribute]. Convert shorthand to standard format
        value = node.value.split('.', 1)

    elif isinstance(node, ScalarNode):
        # Value of this node is scalar
        value = loader.construct_scalar(node)

    elif isinstance(node, SequenceNode):
        # Value of this node is an array (Ex: [1,2])
        value = loader.construct_sequence(node)

    else:
        # Value of this node is an mapping (ex: {foo: bar})
        value = loader.construct_mapping(node)

    return {cfntag: value}


def yaml_dump(dict_to_dump):
    """
    This function dumps the dictionary as a YAML document
    :param dict_to_dump: Data to be serialized as YAML
    :type dict_to_dump: dict
    :return: YAML document
    :rtype: str
    """
    return yaml.safe_dump(dict_to_dump, default_flow_style=False)


def parse_template(template_str):
    """
    This function parses the SAM template

    :param template_str: A packaged YAML or json CloudFormation template
    :type template_str: str
    :return: Dictionary with keys defined in the template
    :rtype: dict
    """
    try:
        # PyYAML doesn't support json as well as it should, so if the input
        # is actually just json it is better to parse it with the standard
        # json parser.
        return json.loads(template)
    except ValueError:
        yaml.SafeLoader.add_multi_constructor('!', intrinsics_multi_constructor)
        return yaml.safe_load(template)


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

def parse_app_metadata(template):
    """
    This function parses the SAM template, checks that it contains "AWS::ServerlessRepo::Application"
    under the "Metadata" section, and that the application metadata format is valid.

    :param template: A packaged YAML or json SAM template
    :type template: str
    :return: Object containing application metadata
    :rtype: ApplicationMetadata
    :raises: KeyError, AttributeError, InvalidAppMetadataException
    """
    pass

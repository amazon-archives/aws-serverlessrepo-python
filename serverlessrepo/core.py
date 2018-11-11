def publish(template):
    """
    This function reads the SAM template and publishes an application

    :param template: A packaged YAML or JSON SAM template
    :type template: str
    :return: Dictionary containing applicationId and semanticVersion
    :rtype: dict
    """
    pass

def make_application_public():
    """
    This function sets the application to be public

    :return: True, if the request succeeded
    """
    pass

def make_application_private():
    """
    This function sets the application to be private

    :return: True, if the request succeeded
    """
    pass

def share_application_with_accounts(account_ids):
    """
    This function shares the application privately with given AWS account ids

    :param account_ids: Comma-separated list of AWS account ids
    :type account_ids: str
    :return: True, if the request succeeded
    """
    pass

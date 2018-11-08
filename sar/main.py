def create_or_update_application(template):
    """
    The main function to be used by other libraries. It reads the SAM template and creates/updates an application

    :param template: A packaged YAML or json SAM template
    :type template: str
    :return: Dictionary structured as SAR `Application`_ response model if succeeded or `Exception`_ model if failed
    :rtype: dict

    .. _Application:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications-applicationid.html#applications-applicationid-response-body-application-example
    .. _Exception:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications-applicationid.html#applications-applicationid-response-body-badrequestexception-example
    """
    pass

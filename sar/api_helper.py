def create_application(app_metadata):
    """
    This function calls SAR CreateApplication API to create a new application

    :param app_metadata: Object containing application metadata
    :type app_metadata: ApplicationMetadata
    :return: Dictionary structured as SAR `Application`_ response model if the request succeeded or `Exception`_ model if failed
    :rtype: dict

    .. _Application:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications.html#applications-response-body-application-example
    .. _Exception:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications.html#applications-response-body-badrequestexception-example
    """
    pass

def update_application(app_metadata):
    """
    This function calls SAR UpdateApplication API to update an existing application

    :param app_metadata: Object containing application metadata
    :type app_metadata: ApplicationMetadata
    :return: Dictionary structured as SAR `Application`_ response model if the request succeeded or `Exception`_ model if failed
    :rtype: dict

    .. _Application:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications-applicationid.html#applications-applicationid-response-body-application-example
    .. _Exception:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications-applicationid.html#applications-applicationid-response-body-badrequestexception-example
    """
    pass

def create_application_version(app_metadata):
    """
    This function calls SAR CreateApplicationVersion API to create a new version under an existing application

    :param app_metadata: Object containing application metadata
    :type app_metadata: ApplicationMetadata
    :return: Dictionary structured as SAR `Version`_ response model if the request succeeded or `Exception`_ model if failed
    :rtype: dict

    .. _Version:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications-applicationid-versions-semanticversion.html#applications-applicationid-versions-semanticversion-response-body-version-example
    .. _Exception:
    https://docs.aws.amazon.com/serverlessrepo/latest/devguide/applications-applicationid-versions-semanticversion.html#applications-applicationid-versions-semanticversion-response-body-badrequestexception-example
    """
    pass

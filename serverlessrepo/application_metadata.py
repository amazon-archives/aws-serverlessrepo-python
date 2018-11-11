# SAM template SAR metadata properties
NAME = 'Name'
DESCRIPTION = 'Description'
AUTHOR = 'Author'
SPDX_LICENSE_ID = 'SpdxLicenseId'
LICENSE_URL = 'LicenseUrl'
README_URL = 'ReadmeUrl'
LABELS = 'Labels'
HOMEPAGE_URL = 'HomepageUrl'
SEMANTIC_VERSION = 'SemanticVersion'
SOURCE_CODE_URL = 'SourceCodeUrl'

class ApplicationMetadata:
    """
    Class representing SAR metadata
    """

    def __init__(self, app_metadata):
        """
        Initializes the object given SAR metadata properties

        :param app_metadata: Dictionary containing SAR metadata properties
        :type app_metadata: dict
        """
        self.app_metadta = app_metadata

    def valid(self):
        """
        Checks if the required properties for application metadata have been populated

        :return: True, if the metadata is valid
        """
        return True

    def to_create_application_request(self):
        """
        Converts CloudFormation properties to SAR CreateApplication API request body

        :return: Dictionary containing fields needed by CreateApplication
        :rtype: dict
        """
        pass

    def to_update_application_request(self):
        """
        Converts CloudFormation properties to SAR UpdateApplication API request body

        :return: Dictionary containing fields needed by UpdateApplication
        :rtype: dict
        """
        pass

    def to_create_application_version_request(self):
        """
        Converts CloudFormation properties to SAR CreateApplicationVersion API request body

        :return: Dictionary containing fields needed by CreateApplicationVersion
        :rtype: dict
        """
        pass

from enum import Enum

class ApplicationMetadata(object):
    """
    Class representing SAM template application metadata
    """
    def __init__(self, app_metadata):
        """
        Initializes the object given a dictionary of application metadata structured as `Doc Placeholder`

        :param app_metadata: Dictionary representing the application metadata
        :type app_metadata: dict

        .. _Doc Placeholder:
        https://xxxx.xxx.xxx
        """
        self.app_metadta = app_metadata

    def valid(self):
        """
        Checks if the required properties for application metadata have been populated

        :return: True, if the metadata is valid
        """
        return True

    def to_SAR_payload(self):
        """
        Converts CloudFormation properties to the matching SAR request payload fields

        :return: Dictionary containing metadata for interacting with SAR APIs
        :rtype: dict
        """
        pass

class ApplicationMetadataProperty(Enum):
    """
    Enum of supported application metadata properties
    """

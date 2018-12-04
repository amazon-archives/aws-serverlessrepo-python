"""Module containing class to store SAR application metadata."""

from .exceptions import InvalidApplicationMetadataError


class ApplicationMetadata(object):
    """Class representing SAR metadata."""

    # SAM template SAR metadata properties
    _NAME = 'Name'
    _DESCRIPTION = 'Description'
    _AUTHOR = 'Author'
    _SPDX_LICENSE_ID = 'SpdxLicenseId'
    _LICENSE_URL = 'LicenseUrl'
    _README_URL = 'ReadmeUrl'
    _LABELS = 'Labels'
    _HOMEPAGE_URL = 'HomepageUrl'
    _SEMANTIC_VERSION = 'SemanticVersion'
    _SOURCE_CODE_URL = 'SourceCodeUrl'

    def __init__(self, app_metadata):
        """
        Initialize the object given SAR metadata properties.

        :param app_metadata: Dictionary containing SAR metadata properties
        :type app_metadata: dict
        """
        self.name = app_metadata.get(self._NAME)
        self.description = app_metadata.get(self._DESCRIPTION)
        self.author = app_metadata.get(self._AUTHOR)
        self.spdx_license_id = app_metadata.get(self._SPDX_LICENSE_ID)
        self.license_url = app_metadata.get(self._LICENSE_URL)
        self.readme_url = app_metadata.get(self._README_URL)
        self.labels = app_metadata.get(self._LABELS)
        self.home_page_url = app_metadata.get(self._HOMEPAGE_URL)
        self.semantic_version = app_metadata.get(self._SEMANTIC_VERSION)
        self.source_code_url = app_metadata.get(self._SOURCE_CODE_URL)

    def __eq__(self, other):
        """Return whether two ApplicationMetadata objects are equal."""
        return isinstance(other, type(self)) and self.__dict__ == other.__dict__

    def validate(self, required_props):
        """
        Check if the required application metadata properties have been populated.

        :param required_props: List of required properties
        :type required_props: list
        :return: True, if the metadata is valid
        :raises: InvalidApplicationMetadataError
        """
        missing_props = [p for p in required_props if not getattr(self, p)]
        if missing_props:
            missing_props_str = ', '.join(sorted(missing_props))
            raise InvalidApplicationMetadataError(properties=missing_props_str)
        return True

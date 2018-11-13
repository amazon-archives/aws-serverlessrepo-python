import boto3

from parser import parse_sam_template
from application_metadata import ApplicationMetadata
from exceptions import ApplicationMetadataNotFoundError


class Application(object):
    """
    Class representing SAR application
    """

    _METADATA = 'Metadata'
    _SERVERLESS_REPO_APPLICATION = 'AWS::ServerlessRepo::Application'

    def __init__(self, template=None, application_id=None):
        """
        Initializes the class

        :param template: A packaged YAML or JSON SAM template
        :type template: str
        :param application_id: The Amazon Resource Name (ARN) of the application.
        :type application_id: str
        :raises ApplicationMetadataNotFoundError
        """
        self.template = template
        if template is not None:
            self.template_dict = parse_sam_template(template)
            try:
                app_metadata_dict = self.template_dict[self._METADATA][self._SERVERLESS_REPO_APPLICATION]
                self.app_metadata = ApplicationMetadata(app_metadata_dict)
            except KeyError as e:
                raise ApplicationMetadataNotFoundError(
                    error_message='missing {} section'.format(e.args[0]))
        self.application_id = application_id
        self.serverless_repo = boto3.client('serverlessrepo')

    def publish(self):
        """
        This function publishes the application

        :return: Dictionary containing applicationId and semanticVersion
        :rtype: dict
        :raises ValueError
        """
        if not self.template or not self.app_metadata:
            raise ValueError('Require SAM template and application metadata to publish the app')
        else:
            pass

    def deploy(self,
               stack_name,
               semantic_version=None,
               parameter_overrides=None):
        """
        This function deploys the application

        :return: True, if the request succeeded
        :raises ValueError
        """
        if not self.application_id or not stack_name:
            raise ValueError('Require application id and stack name to deploy the app')
        else:
            pass

    def make_public(self):
        """
        This function sets the application to be public

        :return: True, if the request succeeded
        :raises ValueError
        """
        if not self.application_id:
            raise ValueError('Require application id to make the app public')
        else:
            pass

    def make_private(self):
        """
        This function sets the application to be private

        :return: True, if the request succeeded
        :raises ValueError
        """
        if not self.application_id:
            raise ValueError('Require application id to make the app private')
        else:
            pass

    def share_application_with_accounts(self, account_ids):
        """
        This function shares the application privately with given AWS account ids

        :param account_ids: Comma-separated list of AWS account ids
        :type account_ids: str
        :return: True, if the request succeeded
        :raises ValueError
        """
        if not self.application_id or not account_ids:
            raise ValueError('Require application id and list of AWS account ids to make the app public')
        else:
            pass

    def _construct_create_application_payload(self):
        return {
            'Author': self.app_metadata.author,
            'Description': self.app_metadata.description,
            'HomePageUrl': self.app_metadata.home_page_url,
            'Labels': self.app_metadata.labels,
            'LicenseUrl': self.app_metadata.license_url,
            'Name': self.app_metadata.name,
            'ReadmeUrl': self.app_metadata.readme_url,
            'SemanticVersion': self.app_metadata.semantic_version,
            'SourceCodeUrl': self.app_metadata.source_code_url,
            'SpdxLicenseId': self.app_metadata.spdx_license_id,
            'TemplateBody': self.template
        }

    def _construct_update_application_payload(self):
        return {
            'ApplicationId': self.application_id,
            'Author': self.app_metadata.author,
            'Description': self.app_metadata.description,
            'HomePageUrl': self.app_metadata.home_page_url,
            'Labels': self.app_metadata.labels,
            'ReadmeUrl': self.app_metadata.readme_url
        }

    def _construct_create_application_version_payload(self):
        return {
            'ApplicationId': self.application_id,
            'SemanticVersion': self.app_metadata.semantic_version,
            'SourceCodeUrl': self.app_metadata.source_code_url,
            'TemplateBody': self.template
        }

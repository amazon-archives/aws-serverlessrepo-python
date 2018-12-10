from unittest import TestCase
from mock import patch, Mock
from botocore.exceptions import ClientError

from serverlessrepo import publish_application, update_application_metadata
from serverlessrepo.exceptions import InvalidApplicationMetadataError
from serverlessrepo.parser import parse_template, get_app_metadata
from serverlessrepo.publish import (
    CREATE_APPLICATION,
    UPDATE_APPLICATION,
    CREATE_APPLICATION_VERSION
)


class TestPublishApplication(TestCase):

    def setUp(self):
        patcher = patch('serverlessrepo.publish.boto3')
        self.addCleanup(patcher.stop)
        self.boto3_mock = patcher.start()
        self.serverlessrepo_mock = Mock()
        self.boto3_mock.client.return_value = self.serverlessrepo_mock
        self.template = """
        {
            "Metadata": {
                'AWS::ServerlessRepo::Application': {
                    'Name': 'test-app',
                    'Description': 'hello world',
                    'Author': 'abc',
                    'LicenseUrl': 's3://test-bucket/LICENSE',
                    'ReadmeUrl': 's3://test-bucket/README.md',
                    'Labels': ['test1', 'test2'],
                    'HomePageUrl': 'https://github.com/abc/def',
                    'SourceCodeUrl': 'https://github.com/abc/def',
                    'SemanticVersion': '1.0.0'
                }
            }
        }
        """
        self.application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'
        self.application_exists_error = ClientError(
            {
                'Error': {
                    'Code': 'ConflictException',
                    'Message': 'Application with id {} already exists'.format(self.application_id)
                }
            },
            'create_application'
        )
        self.not_conflict_exception = ClientError(
            {
                'Error': {'Code': 'BadRequestException'}
            },
            'create_application'
        )

    def test_publish_empty_template(self):
        with self.assertRaises(ValueError) as context:
            publish_application('')

        message = str(context.exception)
        expected = 'Require SAM template to publish the application'
        self.assertEqual(expected, message)
        self.serverlessrepo_mock.create_application.assert_not_called()

    def test_publish_new_application_should_create_application(self):
        self.serverlessrepo_mock.create_application.return_value = {
            'ApplicationId': self.application_id
        }

        actual_result = publish_application(self.template)
        app_metadata_template = get_app_metadata(parse_template(self.template)).template_dict
        expected_result = {
            'application_id': self.application_id,
            'actions': [CREATE_APPLICATION],
            'details': app_metadata_template
        }
        self.assertEqual(expected_result, actual_result)

        expected_request = dict({'TemplateBody': self.template}, **app_metadata_template)
        self.serverlessrepo_mock.create_application.assert_called_once_with(**expected_request)
        # publish a new application will only call create_application
        self.serverlessrepo_mock.update_application.assert_not_called()
        self.serverlessrepo_mock.create_application_version.assert_not_called()

    def test_publish_exception_when_validate_create_application_request(self):
        template_without_app_name = self.template.replace("'Name': 'test-app',", '')
        with self.assertRaises(InvalidApplicationMetadataError) as context:
            publish_application(template_without_app_name)

        message = str(context.exception)
        self.assertEqual("Required application metadata properties not provided: 'name'", message)
        # create_application shouldn't be called if application metadata is invalid
        self.serverlessrepo_mock.create_application.assert_not_called()

    def test_publish_exception_when_serverlessrepo_create_application(self):
        self.serverlessrepo_mock.create_application.side_effect = self.not_conflict_exception

        # should raise exception if it's not ConflictException
        with self.assertRaises(ClientError):
            publish_application(self.template)

        # shouldn't call the following APIs if the exception isn't application already exists
        self.serverlessrepo_mock.update_application.assert_not_called()
        self.serverlessrepo_mock.create_application_version.assert_not_called()

    def test_publish_existing_application_should_update_application_if_version_not_specified(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error
        template_without_version = self.template.replace("'SemanticVersion': '1.0.0'", '')

        actual_result = publish_application(template_without_version)
        expected_result = {
            'application_id': self.application_id,
            'actions': [UPDATE_APPLICATION],
            'details': {
                # Name, LicenseUrl and SourceCodeUrl shouldn't show up
                'Description': 'hello world',
                'Author': 'abc',
                'ReadmeUrl': 's3://test-bucket/README.md',
                'Labels': ['test1', 'test2'],
                'HomePageUrl': 'https://github.com/abc/def'
            }
        }
        self.assertEqual(expected_result, actual_result)

        self.serverlessrepo_mock.create_application.assert_called_once()
        # should continue to update application if the exception is application already exists
        expected_request = dict({'ApplicationId': self.application_id}, **expected_result['details'])
        self.serverlessrepo_mock.update_application.assert_called_once_with(**expected_request)
        # create_application_version shouldn't be called if version is not provided
        self.serverlessrepo_mock.create_application_version.assert_not_called()

    def test_publish_existing_application_should_update_application_if_version_exists(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error
        self.serverlessrepo_mock.create_application_version.side_effect = ClientError(
            {'Error': {'Code': 'ConflictException'}},
            'create_application_version'
        )

        actual_result = publish_application(self.template)
        expected_result = {
            'application_id': self.application_id,
            'actions': [UPDATE_APPLICATION],
            'details': {
                # Name, LicenseUrl and SourceCodeUrl shouldn't show up
                'Description': 'hello world',
                'Author': 'abc',
                'Labels': ['test1', 'test2'],
                'HomePageUrl': 'https://github.com/abc/def',
                'ReadmeUrl': 's3://test-bucket/README.md'
            }
        }
        self.assertEqual(expected_result, actual_result)

        self.serverlessrepo_mock.create_application.assert_called_once()
        self.serverlessrepo_mock.update_application.assert_called_once()
        self.serverlessrepo_mock.create_application_version.assert_called_once()

    def test_publish_new_version_should_create_application_version(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error

        actual_result = publish_application(self.template)
        expected_result = {
            'application_id': self.application_id,
            'actions': [UPDATE_APPLICATION, CREATE_APPLICATION_VERSION],
            'details': {
                # Name and LicenseUrl shouldn't show up since they can't be updated
                'Description': 'hello world',
                'Author': 'abc',
                'ReadmeUrl': 's3://test-bucket/README.md',
                'Labels': ['test1', 'test2'],
                'HomePageUrl': 'https://github.com/abc/def',
                'SourceCodeUrl': 'https://github.com/abc/def',
                'SemanticVersion': '1.0.0'
            }
        }
        self.assertEqual(expected_result, actual_result)

        self.serverlessrepo_mock.create_application.assert_called_once()
        self.serverlessrepo_mock.update_application.assert_called_once()
        # should continue to create application version
        expected_request = {
            'ApplicationId': self.application_id,
            'SourceCodeUrl': 'https://github.com/abc/def',
            'SemanticVersion': '1.0.0',
            'TemplateBody': self.template
        }
        self.serverlessrepo_mock.create_application_version.assert_called_once_with(**expected_request)

    def test_publish_exception_when_serverlessrepo_create_application_version(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error
        self.serverlessrepo_mock.create_application_version.side_effect = self.not_conflict_exception

        # should raise exception if it's not ConflictException
        with self.assertRaises(ClientError):
            publish_application(self.template)

    def test_create_application_with_passed_in_sar_client(self):
        sar_client = Mock()
        sar_client.create_application.return_value = {
            'ApplicationId': self.application_id
        }
        publish_application(self.template, sar_client)

        sar_client.create_application.assert_called_once()
        sar_client.update_application.assert_not_called()
        sar_client.create_application_version.assert_not_called()

        # the self initiated boto3 client shouldn't be used
        self.serverlessrepo_mock.create_application.assert_not_called()
        self.serverlessrepo_mock.update_application.assert_not_called()
        self.serverlessrepo_mock.create_application_version.assert_not_called()

    def test_update_application_with_passed_in_sar_client(self):
        sar_client = Mock()
        sar_client.create_application.side_effect = self.application_exists_error
        publish_application(self.template, sar_client)

        sar_client.create_application.assert_called_once()
        sar_client.update_application.assert_called_once()
        sar_client.create_application_version.assert_called_once()

        # the self initiated boto3 client shouldn't be used
        self.serverlessrepo_mock.create_application.assert_not_called()
        self.serverlessrepo_mock.update_application.assert_not_called()
        self.serverlessrepo_mock.create_application_version.assert_not_called()


class TestUpdateApplicationMetadata(TestCase):
    def setUp(self):
        patcher = patch('serverlessrepo.publish.boto3')
        self.addCleanup(patcher.stop)
        self.boto3_mock = patcher.start()
        self.serverlessrepo_mock = Mock()
        self.boto3_mock.client.return_value = self.serverlessrepo_mock
        self.template = """
        {
            "Metadata": {
                'AWS::ServerlessRepo::Application': {
                    'Name': 'test-app',
                    'Description': 'hello world',
                    'Author': 'abc',
                    'SemanticVersion': '1.0.0'
                }
            }
        }
        """
        self.application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'

    def test_empty_template_throw_exception(self):
        with self.assertRaises(ValueError) as context:
            update_application_metadata('', self.application_id)

        message = str(context.exception)
        expected = 'Require SAM template and application ID to update application metadata'
        self.assertEqual(expected, message)
        self.serverlessrepo_mock.update_application.assert_not_called()

    def test_empty_application_id_throw_exception(self):
        with self.assertRaises(ValueError) as context:
            update_application_metadata(self.template, '')

        message = str(context.exception)
        expected = 'Require SAM template and application ID to update application metadata'
        self.assertEqual(expected, message)
        self.serverlessrepo_mock.update_application.assert_not_called()

    def test_update_application_metadata_ignore_irrelevant_fields(self):
        update_application_metadata(self.template, self.application_id)
        # SemanticVersion in the template should be ignored
        expected_request = {
            'ApplicationId': self.application_id,
            'Author': 'abc',
            'Description': 'hello world'
        }
        self.serverlessrepo_mock.update_application.assert_called_once_with(**expected_request)

    def test_update_application_metadata_with_passed_in_sar_client(self):
        sar_client = Mock()
        update_application_metadata(self.template, self.application_id, sar_client)

        # the self initiated boto3 client shouldn't be used
        self.serverlessrepo_mock.update_application.assert_not_called()
        sar_client.update_application.assert_called_once()

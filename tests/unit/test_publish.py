from unittest import TestCase
from mock import patch
from botocore.exceptions import ClientError

from serverlessrepo import publish_application, publish_application_metadata
from serverlessrepo.exceptions import InvalidApplicationMetadataError


class TestPublishApplication(TestCase):

    def setUp(self):
        patcher = patch('serverlessrepo.publish.SERVERLESSREPO')
        self.addCleanup(patcher.stop)
        self.serverlessrepo_mock = patcher.start()
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
        self.application_exists_error = ClientError(
            {
                'Error': {
                    'Code': 'ConflictException',
                    'Message': 'Application with id {} already exists'.format(self.application_id)
                }
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
        expected_result = {
            'application_id': self.application_id,
            'semantic_version': '1.0.0'
        }
        self.assertEqual(expected_result, actual_result)

        expected_request = {
            'Author': 'abc',
            'Description': 'hello world',
            'Name': 'test-app',
            'SemanticVersion': '1.0.0',
            'TemplateBody': self.template
        }
        self.serverlessrepo_mock.create_application.assert_called_once_with(**expected_request)
        # publish a new application will only call create_application
        self.serverlessrepo_mock.update_application.assert_not_called()
        self.serverlessrepo_mock.create_application_version.assert_not_called()

    def test_publish_exception_when_validate_create_application_request(self):
        template_without_app_name = """
        {
            "Metadata": {
                'AWS::ServerlessRepo::Application': {
                    'Description': 'hello world',
                    'Author': 'abc',
                    'SemanticVersion': '1.0.0'
                }
            }
        }
        """
        with self.assertRaises(InvalidApplicationMetadataError) as context:
            publish_application(template_without_app_name)

        message = str(context.exception)
        self.assertEqual("Required application metadata properties not provided: 'name'", message)
        # create_application shouldn't be called if application metadata is invalid
        self.serverlessrepo_mock.create_application.assert_not_called()

    def test_publish_exception_when_serverlessrepo_create_application(self):
        self.serverlessrepo_mock.create_application.side_effect = ClientError(
            {'Error': {'Code': 'BadRequestException'}},
            'create_application'
        )
        with self.assertRaises(ClientError):
            publish_application(self.template)

        # shouldn't call the following APIs if the exception isn't application already exists
        self.serverlessrepo_mock.update_application.assert_not_called()
        self.serverlessrepo_mock.create_application_version.assert_not_called()

    def test_publish_existing_application_should_update_application(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error
        publish_application(self.template)
        self.serverlessrepo_mock.create_application.assert_called_once()
        # should continue to update application if the exception is application already exists
        expected_request = {
            'ApplicationId': self.application_id,
            'Author': 'abc',
            'Description': 'hello world'
        }
        self.serverlessrepo_mock.update_application.assert_called_once_with(**expected_request)

    def test_publish_existing_application_should_create_application_version(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error

        actual_result = publish_application(self.template)
        expected_result = {
            'application_id': self.application_id,
            'semantic_version': '1.0.0'
        }
        self.assertEqual(expected_result, actual_result)

        self.serverlessrepo_mock.create_application.assert_called_once()
        self.serverlessrepo_mock.update_application.assert_called_once()
        # should continue to create application version
        expected_request = {
            'ApplicationId': self.application_id,
            'SemanticVersion': '1.0.0',
            'TemplateBody': self.template
        }
        self.serverlessrepo_mock.create_application_version.assert_called_once_with(**expected_request)

    def test_publish_existing_application_should_throw_exception_if_version_not_specified(self):
        self.serverlessrepo_mock.create_application.side_effect = self.application_exists_error
        template_without_semantic_version = """
        {
            "Metadata": {
                'AWS::ServerlessRepo::Application': {
                    'Name': 'test-app',
                    'Description': 'new description',
                    'Author': 'new author',
                }
            }
        }
        """
        with self.assertRaises(InvalidApplicationMetadataError) as context:
            publish_application(template_without_semantic_version)

        message = str(context.exception)
        self.assertEqual("Required application metadata properties not provided: 'semantic_version'", message)

        self.serverlessrepo_mock.create_application.assert_called_once()
        self.serverlessrepo_mock.update_application.assert_called_once()
        # create_application_version shouldn't be called if version is not provided
        self.serverlessrepo_mock.create_application_version.assert_not_called()


class TestPublishApplicationMetadata(TestCase):
    def setUp(self):
        patcher = patch('serverlessrepo.publish.SERVERLESSREPO')
        self.addCleanup(patcher.stop)
        self.serverlessrepo_mock = patcher.start()
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
            publish_application_metadata('', self.application_id)

        message = str(context.exception)
        expected = 'Require SAM template and application ID to update application metadata'
        self.assertEqual(expected, message)
        self.serverlessrepo_mock.update_application.assert_not_called()

    def test_empty_application_id_throw_exception(self):
        with self.assertRaises(ValueError) as context:
            publish_application_metadata(self.template, '')

        message = str(context.exception)
        expected = 'Require SAM template and application ID to update application metadata'
        self.assertEqual(expected, message)
        self.serverlessrepo_mock.update_application.assert_not_called()

    def test_publish_application_metadata_ignore_irrelevant_fields(self):
        publish_application_metadata(self.template, self.application_id)
        # SemanticVersion in the template should be ignored
        expected_request = {
            'ApplicationId': self.application_id,
            'Author': 'abc',
            'Description': 'hello world'
        }
        self.serverlessrepo_mock.update_application.assert_called_once_with(**expected_request)

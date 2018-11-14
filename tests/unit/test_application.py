from unittest import TestCase

from serverlessrepo.application import Application
from serverlessrepo.application_metadata import ApplicationMetadata
from serverlessrepo.parser import parse_sam_template
from serverlessrepo.exceptions import ApplicationMetadataNotFoundError


class TestApplication(TestCase):

    def test_init(self):
        yaml_with_app_metadata = """
        Metadata:
            AWS::ServerlessRepo::Application:
                Name: name
                Description: description
                Author: author
        """

        app_metadata_dict = {
            'Name': 'name',
            'Description': 'description',
            'Author': 'author'
        }
        expected_template_dict = {
            'Metadata': {
                'AWS::ServerlessRepo::Application': app_metadata_dict
            }
        }
        expected_app_metadata = ApplicationMetadata(app_metadata_dict)

        application = Application(template=yaml_with_app_metadata, application_id='123')
        self.assertEqual(application.template, yaml_with_app_metadata)
        self.assertEqual(application.application_id, '123')
        self.assertEqual(application.template_dict, expected_template_dict)
        self.assertEqual(application.app_metadata, expected_app_metadata)

    def test_init_using_template_without_metadata(self):
        yaml_without_metadata = """
        RandomKey:
            Key1: Something
        """

        with self.assertRaises(ApplicationMetadataNotFoundError) as context:
            Application(template=yaml_without_metadata)

        message = str(context.exception)
        expected = 'missing Metadata section'
        self.assertTrue(expected in message)

    def test_init_using_template_without_app_metadata(self):
        yaml_without_app_metadata = """
        Metadata:
            Key1: Something
        """

        with self.assertRaises(ApplicationMetadataNotFoundError) as context:
            Application(template=yaml_without_app_metadata)

        message = str(context.exception)
        expected = 'missing AWS::ServerlessRepo::Application section'
        self.assertTrue(expected in message)

    def test_init_without_template_do_not_raise_error(self):
        application = Application()
        self.assertEquals(application.template, None)
        self.assertEquals(application.application_id, None)

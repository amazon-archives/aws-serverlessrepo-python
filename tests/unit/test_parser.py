from unittest import TestCase

from serverlessrepo.exceptions import ApplicationMetadataNotFoundError
from serverlessrepo.application_metadata import ApplicationMetadata
from serverlessrepo.parser import parse_template, yaml_dump, get_app_metadata


class TestParser(TestCase):

    yaml_with_tags = """
    Resource:
        Key1: !Ref Something
        Key2: !GetAtt Another.Arn
        Key3: !FooBar [!Baz YetAnother, "hello"]
        Key4: !SomeTag {"a": "1"}
        Key5: !GetAtt OneMore.Outputs.Arn
        Key6: !Condition OtherCondition
    """

    parsed_yaml_dict = {
        "Resource": {
            "Key1": {
                "Ref": "Something"
            },
            "Key2": {
                "Fn::GetAtt": ["Another", "Arn"]
            },
            "Key3": {
                "Fn::FooBar": [
                    {"Fn::Baz": "YetAnother"},
                    "hello"
                ]
            },
            "Key4": {
                "Fn::SomeTag": {
                    "a": "1"
                }
            },
            "Key5": {
                "Fn::GetAtt": ["OneMore", "Outputs.Arn"]
            },
            "Key6": {
                "Condition": "OtherCondition"
            }
        }
    }

    def test_parse_yaml_with_tags(self):
        output = parse_template(self.yaml_with_tags)
        self.assertEquals(self.parsed_yaml_dict, output)

        # Make sure formatter and parser work well with each other
        formatted_str = yaml_dump(output)
        output_again = parse_template(formatted_str)
        self.assertEquals(output, output_again)

    def test_yaml_getatt(self):
        # This is an invalid syntax for !GetAtt. But make sure the code does not crash when we encouter this syntax
        # Let CloudFormation interpret this value at runtime
        input = """
        Resource:
            Key: !GetAtt ["a", "b"]
        """

        output = {
            "Resource": {
                "Key": {
                    "Fn::GetAtt": ["a", "b"]
                }
            }
        }

        actual_output = parse_template(input)
        self.assertEquals(actual_output, output)

    def test_parse_json_with_tabs(self):
        template = '{\n\t"foo": "bar"\n}'
        output = parse_template(template)
        self.assertEqual(output, {'foo': 'bar'})

    def test_parse_yaml_preserve_elements_order(self):
        input_template = """
        B_Resource:
            Key2:
                Name: name2
            Key1:
                Name: name1
        A_Resource:
            Key2:
                Name: name2
            Key1:
                Name: name1
        """
        output_dict = parse_template(input_template)
        expected_dict = {
            'B_Resource': {
                'Key2': {'Name': 'name2'},
                'Key1': {'Name': 'name1'}
            },
            'A_Resource': {
                'Key2': {'Name': 'name2'},
                'Key1': {'Name': 'name1'}
            }
        }
        self.assertEqual(expected_dict, output_dict)
        output_template = yaml_dump(output_dict)
        # yaml dump changes indentation, remove spaces and new line characters to just compare the text
        self.assertEqual(input_template.translate(None, '\n '),
                         output_template.translate(None, '\n '))

    def test_get_app_metadata_missing_metadata(self):
        template_dict_without_metadata = {
            'RandomKey': {
                'Key1': 'Something'
            }
        }
        with self.assertRaises(ApplicationMetadataNotFoundError) as context:
            get_app_metadata(template_dict_without_metadata)

        message = str(context.exception)
        expected = 'missing AWS::ServerlessRepo::Application section in template Metadata'
        self.assertTrue(expected in message)

    def test_get_app_metadata_missing_app_metadata(self):
        template_dict_without_app_metadata = {
            'Metadata': {
                'Key1': 'Something'
            }
        }
        with self.assertRaises(ApplicationMetadataNotFoundError) as context:
            get_app_metadata(template_dict_without_app_metadata)

        message = str(context.exception)
        expected = 'missing AWS::ServerlessRepo::Application section in template Metadata'
        self.assertTrue(expected in message)

    def test_get_app_metadata_return_metadata(self):
        app_metadata = {
            'Name': 'name',
            'Description': 'description',
            'Author': 'author'
        }

        template_dict = {
            'Metadata': {
                'AWS::ServerlessRepo::Application': dict(app_metadata)
            }
        }

        expected = ApplicationMetadata(app_metadata)
        actual = get_app_metadata(template_dict)
        self.assertEqual(expected, actual)

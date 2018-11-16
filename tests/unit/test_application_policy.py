from unittest import TestCase

from serverlessrepo.application_policy import ApplicationPolicy
from serverlessrepo.exceptions import InvalidApplicationPolicyError


class TestApplicationPolicy(TestCase):

    def test_init(self):
        app_policy = ApplicationPolicy('1 2 3 ', 'a b c')
        self.assertEqual(app_policy.principals, '123')
        self.assertEqual(app_policy.actions, 'abc')

    def test_valid_principals_actions(self):
        principals = '123456789011, 123456789012'
        actions = '{}, {}'.format(ApplicationPolicy.DEPLOY, ApplicationPolicy.GET_APPLICATION)
        app_policy = ApplicationPolicy(principals, actions)
        self.assertTrue(app_policy.validate())

    def test_empty_principals(self):
        app_policy = ApplicationPolicy('', ApplicationPolicy.DEPLOY)
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            app_policy.validate()

        message = str(context.exception)
        expected = 'principals not provided'
        self.assertTrue(expected in message)

    def test_not_12_digits_principals(self):
        app_policy = ApplicationPolicy('123', ApplicationPolicy.DEPLOY)
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            app_policy.validate()

        message = str(context.exception)
        expected = 'principals should be comma separated 12-digit numbers'
        self.assertTrue(expected in message)

    def test_not_comma_separated_principals(self):
        app_policy = ApplicationPolicy('123456789012-123456789012', ApplicationPolicy.DEPLOY)
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            app_policy.validate()

        message = str(context.exception)
        expected = 'principals should be comma separated 12-digit numbers'
        self.assertTrue(expected in message)

    def test_empty_actions(self):
        app_policy = ApplicationPolicy('123456789012', '')
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            app_policy.validate()

        message = str(context.exception)
        expected = 'actions not provided'
        self.assertTrue(expected in message)

    def test_not_supported_actions(self):
        app_policy = ApplicationPolicy('123456789012', 'RandomActionA,RandomActionB')
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            app_policy.validate()

        message = str(context.exception)
        expected = 'RandomActionA, RandomActionB not supported'
        self.assertTrue(expected in message)

    def test_not_comma_separated_actions(self):
        actions = '{}-{}'.format(ApplicationPolicy.DEPLOY, ApplicationPolicy.GET_APPLICATION)
        app_policy = ApplicationPolicy('123456789012', actions)
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            app_policy.validate()

        message = str(context.exception)
        expected = 'actions should be comma separated'
        self.assertTrue(expected in message)

    def test_to_statement(self):
        app_policy = ApplicationPolicy('1, 2', 'actionA, actionB')
        expected_statement = {
            'Principals': ['1', '2'],
            'Actions': ['actionA', 'actionB']
        }
        self.assertEqual(app_policy.to_statement(), expected_statement)

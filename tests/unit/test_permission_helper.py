from unittest import TestCase
from mock import Mock, patch

import serverlessrepo.permission_helper as permission_helper
from serverlessrepo.application_policy import ApplicationPolicy
from serverlessrepo.exceptions import InvalidApplicationPolicyError


class TestPermissionHelper(TestCase):

    def setUp(self):
        self.patcher = patch('serverlessrepo.permission_helper.boto3')
        self.boto3_mock = self.patcher.start()
        self.serverlessrepo_mock = Mock()
        self.boto3_mock.client.return_value = self.serverlessrepo_mock
        self.application_id = 'arn:aws:serverlessrepo:us-east-1:123456789012:applications/test-app'
        self.account_ids = ['123456789012']

    def test_make_application_public_succeeded(self):
        result = permission_helper.make_application_public(self.application_id)
        self.assertTrue(result)
        self.serverlessrepo_mock.put_application_policy.assert_called_with(
            ApplicationId=self.application_id,
            Statements=[{
                'Principals': ['*'],
                'Actions': [ApplicationPolicy.DEPLOY]
            }]
        )

    def test_make_application_public_exception_with_empty_application_id(self):
        with self.assertRaises(ValueError) as context:
            permission_helper.make_application_public('')

        message = str(context.exception)
        expected = 'Require application id to make the app public'
        self.assertEqual(expected, message)

    def test_make_application_private_succeeded(self):
        result = permission_helper.make_application_private(self.application_id)
        self.assertTrue(result)
        self.serverlessrepo_mock.put_application_policy.assert_called_with(
            ApplicationId=self.application_id,
            Statements=[]
        )

    def test_make_application_private_exception_with_empty_application_id(self):
        with self.assertRaises(ValueError) as context:
            permission_helper.make_application_private('')

        message = str(context.exception)
        expected = 'Require application id to make the app private'
        self.assertEqual(expected, message)

    def test_share_application_with_accounts_succeeded(self):
        result = permission_helper.share_application_with_accounts(self.application_id, self.account_ids)
        self.assertTrue(result)
        self.serverlessrepo_mock.put_application_policy.assert_called_with(
            ApplicationId=self.application_id,
            Statements=[{
                'Principals': self.account_ids,
                'Actions': [ApplicationPolicy.DEPLOY]
            }]
        )

    def test_share_application_with_accounts_exception_with_empty_application_id(self):
        with self.assertRaises(ValueError) as context:
            permission_helper.share_application_with_accounts('', self.account_ids)

        message = str(context.exception)
        expected = 'Require application id and list of AWS account IDs to share the app'
        self.assertEqual(expected, message)

    def test_share_application_with_accounts_exception_with_empty_account_ids(self):
        with self.assertRaises(ValueError) as context:
            permission_helper.share_application_with_accounts(self.application_id, [])

        message = str(context.exception)
        expected = 'Require application id and list of AWS account IDs to share the app'
        self.assertEqual(expected, message)

    def test_share_application_with_accounts_exception_with_invalid_account_ids(self):
        with self.assertRaises(InvalidApplicationPolicyError) as context:
            permission_helper.share_application_with_accounts(self.application_id, ['123', '456'])

        message = str(context.exception)
        expected = 'principal should be 12-digit AWS account ID or "*"'
        self.assertTrue(expected in message)

    def tearDown(self):
        self.patcher.stop()

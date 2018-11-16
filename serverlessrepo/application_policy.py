import re

from .exceptions import InvalidApplicationPolicyError


class ApplicationPolicy(object):
    """
    Class representing SAR application policy
    """

    # Supported actions for setting SAR application permissions
    GET_APPLICATION = 'GetApplication'
    CREATE_CLOUD_FORMATION_CHANGE_SET = 'CreateCloudFormationChangeSet'
    CREATE_CLOUD_FORMATION_TEMPLATE = 'CreateCloudFormationTemplate'
    LIST_APPLICATION_VERSIONS = 'ListApplicationVersions'
    SEARCH_APPLICATIONS = 'SearchApplications'
    DEPLOY = 'Deploy'

    SUPPORTED_ACTIONS = [
        GET_APPLICATION,
        CREATE_CLOUD_FORMATION_CHANGE_SET,
        CREATE_CLOUD_FORMATION_TEMPLATE,
        LIST_APPLICATION_VERSIONS,
        SEARCH_APPLICATIONS,
        DEPLOY
    ]

    def __init__(self, principals, actions):
        """
        Initializes the object given the principals and actions

        :param principals: Comma-separated list of AWS account IDs, or *
        :type principals: str
        :param actions: Comma-separated list of actions supported by SAR
        :type actions: str
        """
        self.principals = principals.replace(' ', '')
        self.actions = actions.replace(' ', '')

    def validate(self):
        """
        Checks if the formats of principals and actions are valid

        :return: True, if the policy is valid
        :raises: InvalidApplicationPolicyError
        """
        if not self.principals:
            raise InvalidApplicationPolicyError(error_message='principals not provided')

        if not self.actions:
            raise InvalidApplicationPolicyError(error_message='actions not provided')

        principals_pattern = re.compile('^[0-9]{12}(,[0-9]{12})*$')
        if not principals_pattern.match(self.principals):
            raise InvalidApplicationPolicyError(
                error_message='principals should be comma separated 12-digit numbers')

        actions_pattern = re.compile('^[a-zA-Z]+(,[a-zA-Z]+)*$')
        if not actions_pattern.match(self.actions):
            raise InvalidApplicationPolicyError(
                error_message='actions should be comma separated')

        unsupported_actions = sorted(set(self.actions.split(',')) - set(self.SUPPORTED_ACTIONS))
        if len(unsupported_actions) > 0:
            raise InvalidApplicationPolicyError(
                error_message='{} not supported'.format(', '.join(unsupported_actions)))

        return True

    def to_statement(self):
        """
        Converts to a policy statement dictionary

        :return: Dictionary containing Actions and Principals
        :rtype: dict
        """
        return {
            'Principals': self.principals.split(','),
            'Actions': self.actions.split(',')
        }

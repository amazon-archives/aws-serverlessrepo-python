# Supported actions for setting SAR application permissions
GET_APPLICATION = 'GetApplication'
CREATE_CLOUD_FORMATION_CHANGE_SET = 'CreateCloudFormationChangeSet'
CREATE_CLOUD_FORMATION_TEMPLATE = 'CreateCloudFormationTemplate'
LIST_APPLICATION_VERSIONS = 'ListApplicationVersions'
SEARCH_APPLICATIONS = 'SearchApplications'
DEPLOY = 'Deploy'

class ApplicationPolicy:
    """
    Class representing SAR application policy
    """

    def __init__(self, principals, actions):
        """
        Initializes the object given the principals and actions

        :param principals: Comma-separated list of AWS account IDs, or *
        :type principals: str
        :param actions: Comma-separated list of actions supported by SAR
        :type actions: str
        """
        self.principals = principals
        self.actions = actions

    def valid(self):
        """
        Checks if the formats of principals and actions are valid

        :return: True, if the policy is valid
        """
        return True

    def to_put_application_policy_request(self):
        """
        Converts to SAR PutApplicationPolicy API request body

        :return: Dictionary containing fields needed by PutApplicationPolicy
        :rtype: dict
        """
        pass

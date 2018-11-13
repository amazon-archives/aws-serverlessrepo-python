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

    def is_valid(self):
        """
        Checks if the formats of principals and actions are valid

        :return: True, if the policy is valid
        """
        return True

    def to_statement(self):
        """
        Converts to a policy statement dictionary

        :return: Dictionary containing Actions and Principals
        :rtype: dict
        """
        pass

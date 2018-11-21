import boto3

from .application_policy import ApplicationPolicy


def make_application_public(application_id):
    """
    This function sets the application to be public
    :raises ValueError
    """
    if not application_id:
        raise ValueError('Require application id to make the app public')

    application_policy = ApplicationPolicy(['*'], [ApplicationPolicy.DEPLOY])
    application_policy.validate()
    boto3.client('serverlessrepo').put_application_policy(
        ApplicationId=application_id,
        Statements=[application_policy.to_statement()]
    )


def make_application_private(application_id):
    """
    This function sets the application to be private
    :raises ValueError
    """
    if not application_id:
        raise ValueError('Require application id to make the app private')

    boto3.client('serverlessrepo').put_application_policy(
        ApplicationId=application_id,
        Statements=[]
    )


def share_application_with_accounts(application_id, account_ids):
    """
    This function shares the application privately with given AWS account IDs
    :param account_ids: List of AWS account IDs, or *
    :type account_ids: list of str
    :raises ValueError
    """
    if not application_id or not account_ids:
        raise ValueError('Require application id and list of AWS account IDs to share the app')

    application_policy = ApplicationPolicy(account_ids, [ApplicationPolicy.DEPLOY])
    application_policy.validate()
    boto3.client('serverlessrepo').put_application_policy(
        ApplicationId=application_id,
        Statements=[application_policy.to_statement()]
    )

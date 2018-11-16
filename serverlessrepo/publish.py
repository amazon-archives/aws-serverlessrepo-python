def publish_application(template):
    """
    This function publishes the application

    :param template: A packaged YAML or JSON SAM template
    :type template: str
    :raises ValueError
    """
    if not template:
        raise ValueError('Require SAM template to publish the app')


def _create_application_request(app_metadata, template):
    return {
        'Author': app_metadata.author,
        'Description': app_metadata.description,
        'HomePageUrl': app_metadata.home_page_url,
        'Labels': app_metadata.labels,
        'LicenseUrl': app_metadata.license_url,
        'Name': app_metadata.name,
        'ReadmeUrl': app_metadata.readme_url,
        'SemanticVersion': app_metadata.semantic_version,
        'SourceCodeUrl': app_metadata.source_code_url,
        'SpdxLicenseId': app_metadata.spdx_license_id,
        'TemplateBody': template
    }


def _update_application_request(app_metadata, application_id):
    return {
        'ApplicationId': application_id,
        'Author': app_metadata.author,
        'Description': app_metadata.description,
        'HomePageUrl': app_metadata.home_page_url,
        'Labels': app_metadata.labels,
        'ReadmeUrl': app_metadata.readme_url
    }


def _create_application_version_request(app_metadata, application_id, template):
    return {
        'ApplicationId': application_id,
        'SemanticVersion': app_metadata.semantic_version,
        'SourceCodeUrl': app_metadata.source_code_url,
        'TemplateBody': template
    }

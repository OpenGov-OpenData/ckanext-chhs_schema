from ckan.plugins.toolkit import check_ckan_version

IS_CKAN_29_OR_HIGHER = check_ckan_version(min_version='2.9.0')

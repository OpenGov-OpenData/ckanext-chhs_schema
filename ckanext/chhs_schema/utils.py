import unicodecsv as csv

import ckan.model as model
from ckan.common import config
from ckan.plugins.toolkit import (
    ObjectNotFound,
    NotAuthorized,
    get_action,
    abort,
    c,
    _
)

from ckanext.scheming import helpers
from ckanext.chhs_schema.constants import IS_CKAN_29_OR_HIGHER


def metadata_download(package_id, response):
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user
    }

    data_dict = {
        'id': package_id
    }
    try:
        result = get_action('package_show')(context, data_dict)
    except (ObjectNotFound, NotAuthorized):
        abort(404, _('Package not found'))

    dataset_fields = helpers.scheming_get_dataset_schema("dataset")['dataset_fields']

    if hasattr(response, u'headers'):
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = \
            'attachment; filename="{name}-metadata.csv"'.format(name=package_id)

    if IS_CKAN_29_OR_HIGHER:
        wr = csv.writer(response.stream, encoding='utf-8')
    else:
        wr = csv.writer(response, encoding='utf-8')

    header = ['Field', 'Value']
    wr.writerow(header)

    for field in dataset_fields:
        if field['field_name'] == 'tag_string':
            value = get_package_tags(result.get('tags'))
            wr.writerow([
                helpers.scheming_language_text(field['label']),
                value
            ])
        elif field['field_name'] == 'owner_org':
            org_alias = str(config.get('ckan.organization_alias', 'Organization'))
            wr.writerow([
                org_alias,
                result['organization']['title']
            ])
        elif field['field_name'] == 'groups':
            group_alias = str(config.get('ckan.group_alias', 'Group'))+'s'
            value = get_package_groups(result.get('groups'))
            wr.writerow([
                group_alias,
                value
            ])
        elif helpers.scheming_field_choices(field):
            value = helpers.scheming_choices_label(
                helpers.scheming_field_choices(field),
                result.get(field['field_name'])
            )
            wr.writerow([
                helpers.scheming_language_text(field['label']),
                value
            ])
        else:
            wr.writerow([
                helpers.scheming_language_text(field['label']),
                result.get(field['field_name'])
            ])

    return response


def get_package_groups(groups_dict):
    """
    Build out the group names comma separated string
    """
    groups = [group.get('display_name') for group in groups_dict]
    return ",".join(groups)


def get_package_tags(tags_dict):
    """
    Build out the tag names comma separated string
    """
    tags = [tag.get('display_name') for tag in tags_dict]
    return ",".join(tags)


def get_package_extrafields(extras_list):
    """
    Build out the dict object of the custom fields ie key and value
    """
    custom_fields = {}
    for custom_field in extras_list:
        custom_fields[custom_field["key"]] = custom_field["value"]
    return custom_fields

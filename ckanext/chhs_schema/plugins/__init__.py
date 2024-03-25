from packaging.version import Version

from ckan import plugins as p
from ckan.lib.plugins import DefaultTranslation

if p.toolkit.check_ckan_version(u'2.9'):
    from ckanext.chhs_schema.plugins.flask_plugin import MixinPlugin
else:
    from ckanext.chhs_schema.plugins.pylons_plugin import MixinPlugin


def is_data_dict_active(ddict):
    """"Returns True if data dictionary is populated"""
    for col in ddict:
        info = col.get('info', {})
        if info.get('label') or info.get('notes'):
            return True
    return False


def version_builder(text_version):
    return Version(text_version)


class chhsSchema(MixinPlugin, p.SingletonPlugin, DefaultTranslation):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config):
        p.toolkit.add_template_directory(config, "../templates")
        p.toolkit.add_resource('../assets', 'chhs_schema')

        config['scheming.presets'] = """
ckanext.scheming:presets.json
ckanext.chhs_schema:schemas/presets.yaml
"""

        config['scheming.dataset_schemas'] = """
ckanext.chhs_schema:schemas/dataset.yaml
"""
    
    # ITemplateHelpers
    def get_helpers(self):
        return {
            'chhs_schema_is_data_dict_active': is_data_dict_active,
            'chhs_schema_ckan_version': version_builder
        }

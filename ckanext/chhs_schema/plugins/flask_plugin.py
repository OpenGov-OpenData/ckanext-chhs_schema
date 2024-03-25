import ckan.plugins as p
import ckanext.chhs_schema.views as views


class MixinPlugin(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    # IBlueprint
    def get_blueprint(self):
        return views.get_blueprints()

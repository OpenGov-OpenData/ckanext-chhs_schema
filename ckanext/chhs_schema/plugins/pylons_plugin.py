import ckan.plugins as p


class MixinPlugin(p.SingletonPlugin):
    p.implements(p.IRoutes, inherit=True)

    # IRoutes
    def before_map(self,m):
        m.connect(
            '/metadata_download/{package_id}',
            controller='ckanext.chhs_schema.controller:ChhsSchemaController',
            action='metadata_download'
        )
        return m

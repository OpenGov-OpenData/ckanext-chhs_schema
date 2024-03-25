from ckan.lib.base import BaseController
from ckan.common import response
import ckanext.chhs_schema.utils as utils


class ChhsSchemaController(BaseController):
    def metadata_download(self, package_id):
        return utils.metadata_download(package_id, response)

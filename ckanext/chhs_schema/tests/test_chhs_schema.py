import pytest
import six

from ckan import plugins as p
from ckan.tests import factories, helpers

from ckanext.chhs_schema.constants import IS_CKAN_29_OR_HIGHER


@pytest.mark.usefixtures('with_plugins', 'clean_db', 'clean_index')
class TestChhsSchema(object):

    def test_dataset_with_schema(self):
        '''
        Check schema saves data to the DB.
        '''
        sysadmin = factories.Sysadmin()
        owner_org = factories.Organization()
        dataset = factories.Dataset(
            owner_org=owner_org['id'],
            title='Test CHHS Dataset',
            name='test-chhs-dataset',
            notes='Some notes',
            tag_string='test',
            contact_email='opendata@oshpd.ca.gov',
            author='Office of Statewide Health Planning and Development',
            program_web_page='https://www.google.com',
            temporal_coverage='2022',
            geo_coverage='California',
            geographic_granularity='statewide',
            language='English',
            accrual_periodicity='daily',
            data_license='Terms of Use',
            limitations='Limitations'
        )

        env = {'REMOTE_USER': sysadmin['name'].encode('ascii')}

        pkg_response = helpers.call_action('package_show', id=dataset['id'])
        assert pkg_response['name'] == 'test-chhs-dataset'
        assert pkg_response['contact_email'] == 'opendata@oshpd.ca.gov'
        assert pkg_response['author'] == 'Office of Statewide Health Planning and Development'
        assert pkg_response['program_web_page'] == 'https://www.google.com'
        assert pkg_response['accrual_periodicity'] == 'daily'

    def test_resource_with_accept_popup_field(self):
        sysadmin = factories.Sysadmin()
        owner_org = factories.Organization()
        dataset = factories.Dataset(
            owner_org=owner_org['id'],
            title='Test Dataset with accept_popup',
            name='test-dataset-with-accept-popup',
            notes='Some notes',
            tag_string='test',
            contact_email='opendata@oshpd.ca.gov',
            author='Office of Statewide Health Planning and Development',
            program_web_page='https://www.google.com',
            temporal_coverage='2022',
            geo_coverage='California',
            geographic_granularity='statewide',
            language='English',
            accrual_periodicity='daily',
            data_license='Terms of Use',
            limitations='Limitations'
        )
        resource = factories.Resource(
            package_id=dataset['id'],
            name='Test Resource with accept_popup',
            accept_popup=['Display']
        )

        env = {'REMOTE_USER': sysadmin['name'].encode('ascii')}

        pkg_response = helpers.call_action('package_show', id=dataset['id'])
        assert pkg_response['name'] == 'test-dataset-with-accept-popup'

        res_response = helpers.call_action('resource_show', id=resource['id'])
        assert res_response['name'] == 'Test Resource with accept_popup'
        assert res_response['accept_popup'] == ['Display']

    def test_metadata_download(self, app):
        '''
        Check if metadata file is created for download
        '''
        sysadmin = factories.Sysadmin()
        owner_org = factories.Organization()
        dataset = factories.Dataset(
            owner_org=owner_org['id'],
            title='Test Metadata Download',
            name='test-metadata-download',
            notes='Some notes',
            tag_string='test',
            contact_email='opendata@oshpd.ca.gov',
            author='Office of Statewide Health Planning and Development',
            program_web_page='https://www.google.com',
            temporal_coverage='2022',
            geo_coverage='California',
            geographic_granularity='statewide',
            language='English',
            accrual_periodicity='daily',
            data_license='Terms of Use',
            limitations='Limitations'
        )

        env = {'REMOTE_USER': sysadmin['name'].encode('ascii')}

        pkg_response = helpers.call_action('package_show', id=dataset['id'])
        assert pkg_response['name'] == 'test-metadata-download'

        response = app.get("/metadata_download/{0}".format(str(dataset['id'])))
        if IS_CKAN_29_OR_HIGHER:
            content = six.ensure_text(response.data)
        else:
            content = response.body.decode('utf-8')
        assert (
            "Field,Value\r\n"
            "Title,Test Metadata Download\r\n"
            "URL,test-metadata-download\r\n" in content
        )
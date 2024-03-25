#!/usr/bin/env/python
from setuptools import setup

setup(
    name='ckanext-chhs_schema',
    version='0.1',
    description='',
    license='AGPL3',
    author='',
    author_email='',
    url='',
    namespace_packages=['ckanext'],
    packages=['ckanext.chhs_schema'],
    zip_safe=False,
    entry_points = """
        [ckan.plugins]
        chhs_schema = ckanext.chhs_schema.plugins:chhsSchema
    """
)

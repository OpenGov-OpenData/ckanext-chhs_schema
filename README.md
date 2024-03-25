CHHS Schema
===========

Requirements
------------
Requires [ckanext-scheming](https://github.com/ckan/ckanext-scheming)


Installation
------------
To install ckanext-chhs_schema for development, activate your CKAN virtualenv and do::

    git clone https://github.com/OpenGov-OpenData/ckanext-chhs_schema.git
    cd ckanext-chhs_schema
    python setup.py develop
    pip install -r requirements.txt


Config settings
---------------
```ini

ckan.plugins = ... chhs_schema scheming_datasets
```

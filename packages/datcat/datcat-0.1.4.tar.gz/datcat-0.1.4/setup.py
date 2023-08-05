# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datcat',
 'datcat.adapters',
 'datcat.domain',
 'datcat.entrypoints',
 'datcat.service_layer']

package_data = \
{'': ['*']}

install_requires = \
['Flask-API>=2.0,<3.0',
 'Flask>=1.1.2,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'python-decouple>=3.4,<4.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'datcat',
    'version': '0.1.4',
    'description': 'Simple Data Catalogue API',
    'long_description': '## DatCat\n***\n_Please note this is an alpha version and still in active development. Naturally all feedback is welcome._\n***\nDatcat is a simple and lightweight data catalogue api for big query.\nDatcat loads your .json schema files to memory for use with either your own synchronisation service or [catasyn](https://github.com/antonio-one/catasyn) - it\'s sibling application.\nLook into the example_catalogue directory or [here](https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file) to find out how to define your bigquery schemas.\nHere\'s a quick snippet if you are as lazy as I am:\n\n```json\n[\n  {\n    "description": "Unique Identifier",\n    "mode": "REQUIRED",\n    "name": "MY_UNIQUE_ID",\n    "type": "INT64"\n  },  {\n    "description": "Favourite Colour",\n    "mode": "REQUIRED",\n    "name": "MY_FAVOURITE_COLOUR",\n    "type": "STRING"\n  }\n]\n```\n\nCurrently, datcat supports partition generation and pii identification via tagging the relevant column\'s description with `{"partition": true}` and/or `{"pii": true}`.\n```json\n[\n  {\n    "description": "{\\"pii\\": true}",\n    "mode": "REQUIRED",\n    "name": "col_4",\n    "type": "STRING"\n  },\n  {\n    "description": "{\\"partition\\": true}",\n    "mode": "REQUIRED",\n    "name": "date",\n    "type": "DATE"\n  }\n]\n```\n\nIn addition to serving schema definitions via its api, it  creates a basic mapping between a schema - topic - subscriber that is later used to create the relevant infrastructure [[1]](#footnote-1) from the schema definition.\nAfter the schemas are defined run `python -m datcat.service_layer.mappings` to create those mappings. The naming conventions are basic, with each topic containing all versions of an event and each topic having only one subscriber for the purposes of data lake ingestion alone.\n\n```json\n//schema_topic_subscription.json\n{\n  "login_v1": {\n    "schema_class_name": "login",\n    "topic_name": "login_topic",\n    "subscription_name": "login_subscription"\n  }\n}\n```\nCI/CD is your gig but if you fancy seeing datcat in action in your local docker run `./docker-docker-build.sh` and go to: http://0.0.0.0:50000\n\n#### Footnote 1\nIAM and general permissions are out of scope in this project. It\'s up to you to ensure your service account has all the necessary roles/permissions to create bigquery tables and topics/subscribers. Check [this](https://cloud.google.com/iam/docs/understanding-roles) for a reminder.\n',
    'author': 'Antonio',
    'author_email': 'antonio.one@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/antonio-one/datcat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

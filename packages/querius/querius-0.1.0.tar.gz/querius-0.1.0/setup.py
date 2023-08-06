# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['querius']

package_data = \
{'': ['*']}

install_requires = \
['google-auth>=1.5,<2.0',
 'google-cloud-bigquery>=1.5.0,<=2',
 'loguru>=0.5,<0.6',
 'wrapt-timeout-decorator>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'querius',
    'version': '0.1.0',
    'description': 'Client library for connecting with the Querius API',
    'long_description': 'Querius Client\n---\nClient code for interacting with the [Querius](https://getquerius.com) API.\n\n### Install\n```bash\npip install querius\n```\n\n### Usage\n\n```python\nfrom google.cloud import bigquery\nfrom querius import QueriusClient, patch_bq_client_with_querius_client\nfrom pathlib import Path\n\nbq_client = bigquery.Client()\nq_client = QueriusClient.from_service_account_path(\n    api_url="<querius-url>",\n    service_account_path=Path(\'path/to/key.json\'),\n    customer_id="<querius-customer-id>",\n    timeout_seconds=2\n)\npatch_bq_client_with_querius_client(bq_client, q_client)\n```',
    'author': 'Theo Windebank',
    'author_email': 'theo@getquerius.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://getquerius.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)

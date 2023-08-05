# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_pretty_exception_handler']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>=3.10,<4.0']

setup_kwargs = {
    'name': 'drf-pretty-exception-handler',
    'version': '0.1.2',
    'description': 'Django Rest Framework pretty exception handler',
    'long_description': None,
    'author': 'Denis Ivlev',
    'author_email': 'di-erz@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

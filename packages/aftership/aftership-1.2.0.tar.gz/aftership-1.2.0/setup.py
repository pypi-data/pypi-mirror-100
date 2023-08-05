# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aftership']

package_data = \
{'': ['*']}

modules = \
['CHANGELOG', 'README', 'LICENSE']
install_requires = \
['requests']

setup_kwargs = {
    'name': 'aftership',
    'version': '1.2.0',
    'description': 'The python SDK of AfterShip API',
    'long_description': None,
    'author': 'AfterShip',
    'author_email': 'support@aftership.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)

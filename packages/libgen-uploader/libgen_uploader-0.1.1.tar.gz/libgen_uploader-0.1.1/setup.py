# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libgen_uploader']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0', 'returns==0.16.0', 'robobrowser>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'libgen-uploader',
    'version': '0.1.1',
    'description': 'A Library Genesis ebook uploader',
    'long_description': None,
    'author': 'Francesco Truzzi',
    'author_email': 'francesco@truzzi.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

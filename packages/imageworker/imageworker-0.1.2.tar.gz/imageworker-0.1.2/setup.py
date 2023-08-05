# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imageworker']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'keras_preprocessing>=1.1.2,<2.0.0',
 'numpy>=1.15.4,<2.0.0',
 'qiniu>=7.3.1,<8.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'imageworker',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'kula',
    'author_email': 'kula@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

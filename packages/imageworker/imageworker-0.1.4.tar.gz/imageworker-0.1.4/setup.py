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
    'version': '0.1.4',
    'description': 'Lightweight image library',
    'long_description': 'Usage\n========\n\n\nfile to ndarray\n-------------------\n\ncode::\n    from imageworker import file_to_array\n    data = file_to_array("test.jpg")\n\n\nurl to ndarray\n-------------------\n\ncode::\n    from imageworker import url_to_array\n    data = url_to_array("https://n.sinaimg.cn/spider2021326/106/w1024h682/20210326/5927-kmvwsvy1040641.jpg")\n\nupload ndarray to qiniu cdn\n------------------------------\n\ncode::\n    key = QINIU_KEY\n    secret = QINIU_SECRET\n    domain = HOST\n    bucket = QINIU_BUCKET\n    url = put_qiniu(data,key,secret,domain,bucket) \n\n\n\n\n',
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

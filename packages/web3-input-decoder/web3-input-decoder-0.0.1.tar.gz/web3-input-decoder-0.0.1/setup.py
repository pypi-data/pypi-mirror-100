# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web3_input_decoder']

package_data = \
{'': ['*']}

install_requires = \
['eth-abi>=2.1.1,<3.0.0', 'eth-utils>=1.10.0,<2.0.0', 'pysha3>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'web3-input-decoder',
    'version': '0.0.1',
    'description': 'Offline web3 transaction input decoder for functions and constructors',
    'long_description': None,
    'author': 'Weiliang Li',
    'author_email': 'to.be.impressive@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

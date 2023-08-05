# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idesyde', 'idesyde.identification', 'idesyde.minizinc']

package_data = \
{'': ['*']}

install_requires = \
['forsyde-io-python>=0.2,<0.3',
 'minizinc>=0.4,<0.5',
 'numpy>=1.20,<2.0',
 'sympy>=1.7,<2.0']

setup_kwargs = {
    'name': 'idesyde',
    'version': '0.1.6',
    'description': 'Generic Design Space Exploration for models based system design',
    'long_description': None,
    'author': 'jordao',
    'author_email': 'jordao@kth.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

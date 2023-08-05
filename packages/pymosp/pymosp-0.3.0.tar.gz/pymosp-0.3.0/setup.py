# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymosp']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pymosp',
    'version': '0.3.0',
    'description': 'Python Library to access MOSP.',
    'long_description': '# PyMOSP\n\nPyMOSP is a Python library to access [MOSP](https://github.com/CASES-LU/MOSP).\n\n\n## Installation\n\n```bash\n$ pipx install PyMOSP\n✨🐍✨\n```\n\nor via the Git repository:\n\n```bash\n$ git clone https://github.com/CASES-LU/PyMOSP\n$ cd PyMOSP\n$ poetry install\n$ poetry run nose2 -v --pretty-assert\n```\n\n\n## Examples\n\nSee the examples in the file [example.py](example.py) or in the tests folder.\n\n\n## License\n\nThis software is licensed under\n[GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.html).\n\n* Copyright (C) 2019-2021 Cédric Bonhomme\n* Copyright (C) 2019-2021 SMILE gie securitymadein.lu\n\nFor more information, [the list of authors and contributors](AUTHORS.md)\nis available.\n',
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CASES-LU/PyMOSP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

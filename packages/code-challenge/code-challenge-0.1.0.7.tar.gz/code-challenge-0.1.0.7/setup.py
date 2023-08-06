# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_challenge']

package_data = \
{'': ['*']}

install_requires = \
['altgraph==0.17',
 'certifi==2020.12.5',
 'cffi==1.14.5',
 'chardet==4.0.0',
 'colorama==0.4.4',
 'cryptography==3.4.7',
 'firebase==3.0.1',
 'future==0.18.2',
 'gcloud==0.18.3',
 'googleapis-common-protos==1.53.0',
 'httplib2==0.19.0',
 'idna==2.10',
 'importlib-metadata==3.9.1',
 'jwcrypto==0.8',
 'oauth2client==4.1.3',
 'pefile==2019.4.18',
 'protobuf==3.15.6',
 'pyasn1-modules==0.2.8',
 'pyasn1==0.4.8',
 'pycparser==2.20',
 'pycryptodome==3.10.1',
 'pyparsing==2.4.7',
 'python-jwt==3.3.0',
 'pywin32-ctypes==0.2.0',
 'requests-toolbelt==0.9.1',
 'requests==2.25.1',
 'rsa==4.7.2',
 'six==1.15.0',
 'sseclient==0.0.27',
 'typing-extensions==3.7.4.3',
 'urllib3==1.26.4',
 'wincertstore==0.2',
 'zipp==3.4.1']

entry_points = \
{'console_scripts': ['code-challenge = code_challenge.main:main']}

setup_kwargs = {
    'name': 'code-challenge',
    'version': '0.1.0.7',
    'description': 'Coding interview CLI that directs the user to answer timed coding interview questions in Python, JS, or C++',
    'long_description': None,
    'author': 'Andrew Peng',
    'author_email': 'andrewpeng02@Gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

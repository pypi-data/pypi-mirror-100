# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['everstone', 'everstone.sql']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'everstone',
    'version': '0.1.2',
    'description': 'Simple Database Query Generator',
    'long_description': '# everstone\n\nA simple database query generator.\n\n\n### This project is still in active develpment and is not ready of usage.\n\n## Installation\n```sh\npip install everstone\n```\n\n**Requires Python 3.9.0+**\n\n## Usage\n\n### Connecting a Database\n```py\nfrom everstone import db\n\ndb.connect("test_database", "user_one", "abcd5432")\n```\n\n### Creating a Schema:\n\n```python\nfrom everstone import db\n\nauth_schema = db.Schema("auth")\nawait auth_schema.create()\n```\n#### Resulting SQL\n```sql\nCREATE TABLE user (user_id INTEGER PRIMARY KEY, name TEXT);\n```\n\n### Creating a Table:\n\n```py\nfrom everstone import constraints, db, types\nfrom everstone import Column\nuser_table = db.Table("user")\nuser_table.add_columns(\n    Column("user_id", types.Integer, constraints.PrimaryKey),\n    Column("name", types.Text)\n)\nawait user_table.create()\n```\n#### Resulting SQL\n```sql\nCREATE TABLE user (user_id INTEGER PRIMARY KEY, name TEXT);\n```\n',
    'author': 'scragly',
    'author_email': '29337040+scragly@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scragly/everstone',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

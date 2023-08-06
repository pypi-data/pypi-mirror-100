# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_type_checking']

package_data = \
{'': ['*']}

install_requires = \
['flake8']

entry_points = \
{'flake8.extension': ['TCH100 = flake8_type_checking:Plugin']}

setup_kwargs = {
    'name': 'flake8-type-checking',
    'version': '0.1.0',
    'description': 'A flake8 plugin to flag imports exclusively used for type annotations',
    'long_description': '<a href="https://pypi.org/project/flake8-type-checking/">\n    <img src="https://img.shields.io/pypi/v/flake8-type-checking.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/sondrelg/flake8-type-checking">\n    <img src="https://codecov.io/gh/sondrelg/flake8-type-checking/branch/master/graph/badge.svg" alt="Code coverage">\n</a>\n<a href="https://pypi.org/project/flake8-type-checking/">\n    <img src="https://github.com/sondrelg/flake8-type-checking/actions/workflows/testing.yml/badge.svg" alt="Test status">\n</a>\n<a href="https://pypi.org/project/flake8-type-checking/">\n    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">\n</a>\n<a href="http://mypy-lang.org/">\n    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n</a>\n\n# flake8-type-checking\n\nLets you know which imports to put inside type-checking blocks,\nand helps you manage forward references.\n\nSee the [typing.TYPE_CHECKING](https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING) docs for context.\n\n## Codes\n\n### Primary codes\n\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TCH001 | Move import into a type-checking block  |\n| TCH101 | Move third-party import into a type-checking block |\n| TCH102 | Found multiple type checking blocks |\n\n### Secondary codes\n\nChoose `TCHA` or `TCHB` as they are incompatible (but both valid).\n\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TCHA001 | Add \'from \\_\\_future\\_\\_ import annotations\' import |\n| TCHA002 | Annotation does not need to be a string literal |\n\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TCHB001 | Annotation needs to be made into a string literal |\n| TCHB002 | Annotation does not need to be a string literal |\n\n## Rationale\n\nWe generally want to use `TYPE_CHECKING` blocks for imports where we can, to guard\nagainst [import cycles](https://mypy.readthedocs.io/en/stable/runtime_troubles.html?highlight=TYPE_CHECKING#import-cycles).\nAn added bonus is that guarded imports are not loaded when you start your app, so\ntheoretically you should get a slight performance boost there as well.\n\nOnce imports are guarded, type hints should be treated as [forward references](https://mypy.readthedocs.io/en/stable/runtime_troubles.html?highlight=TYPE_CHECKING#class-name-forward-references).\nRemaining error codes are there to help manage that,\neither by telling your to use string literals where needed, or by enabling\n[postponed evaluation of annotations](https://www.python.org/dev/peps/pep-0563/).\n\nThe error code series `TCHA` and `TCHB` should therefore be considered\nmutually exclusive, as they represent two different ways of solving the same problem.\n\nSee [this](https://stackoverflow.com/a/55344418/8083459) excellent stackoverflow answer for a\nquick explanation of forward references.\n\n## Installation\n\n```shell\npip install flake8-type-checking\n```\n\n## Examples\n\n**Bad code**\n\n`models/a.py`\n```python\nfrom models.b import B\n\nclass A(Model):\n    def foo(self, b: B): ...\n```\n\n`models/b.py`\n```python\nfrom models.a import A\n\nclass B(Model):\n    def bar(self, a: A): ...\n```\n\nWill result in these errors\n\n```shell\n>> a.py: TCH101: Move third-party import \'models.b.B\' into a type-checking block\n>> b.py: TCH101: Move third-party import \'models.a.A\' into a type-checking block\n```\n\nand consequently trigger these errors if imports are purely moved into type-checking block, without proper forward reference handling\n\n```shell\n>> a.py: TCHA001: Add \'from __future__ import annotations\' import\n>> b.py: TCHA001: Add \'from __future__ import annotations\' import\n```\n\nor\n\n```shell\n>> a.py: TCHB001: Annotation \'B\' needs to be made into a string literal\n>> b.py: TCHB001: Annotation \'A\' needs to be made into a string literal\n```\n\n**Good code**\n\n`models/a.py`\n```python\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from models.b import B\n\nclass A(Model):\n    def foo(self, b: \'B\'): ...\n```\n`models/b.py`\n```python\n# TCHA\nfrom __future__ import annotations\n\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from models.a import A\n\nclass B(Model):\n    def bar(self, a: A): ...\n```\n\nor\n\n```python\n# TCHB\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from models.a import A\n\nclass B(Model):\n    def bar(self, a: \'A\'): ...\n```\n\n## As a pre-commit hook\n\nYou can run this flake8 plugin as a [pre-commit](https://github.com/pre-commit/pre-commit) hook:\n\n```yaml\n- repo: https://gitlab.com/pycqa/flake8\n  rev: 3.7.8\n  hooks:\n    - id: flake8\n      additional_dependencies: [ flake8-type-checking ]\n```\n\n## Supporting the project\n\nLeave a ✯ if this project helped you!\n\nContributions are always welcome 👏\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sondrelg/flake8-type-checking',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

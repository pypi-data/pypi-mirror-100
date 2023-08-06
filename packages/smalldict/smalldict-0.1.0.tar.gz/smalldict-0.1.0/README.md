# SmallDict

SmallDict: Python package to slim down a dict read from JSON or YAML to check the contents

[![Python version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)](https://pypi.org/project/smalldict/)
[![PyPI version](https://badge.fury.io/py/smalldict.svg)](https://badge.fury.io/py/smalldict)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Minyus/smalldict/blob/master/LICENSEj)
[![Documentation](https://readthedocs.org/projects/smalldict/badge/?version=latest)](https://smalldict.readthedocs.io/)


## Overview

When you open a big JSON or YAML file, the text viewer often freezes.
You can extract a small subset of a Python dict read from a JSON or YAML file to check the contents.


## Install

### [Option 1] Install from the PyPI

```bash
pip install smalldict
```

### [Option 2] Development install 

This is recommended only if you want to modify the source code of SmallDict.

```bash
git clone https://github.com/Minyus/smalldict.git
cd smalldict
python setup.py develop
```


## How to use

Example:

```python
from smalldict import SmallDict

d = {
    "key_1": ["value_1", "value_2", "value_3"],
    "key_2": {"key_1": "value", "key_2": "value", "key_3": "value"},
    "key_3": "value",
}


def test_no_limit():
    assert SmallDict(d).get() == d


def test_limit():
    assert SmallDict(d).get(
        dict_limit=2, list_limit=1, str_limit=3, json_out=None, yaml_out=None
    ) == {
        "key_1": ["val"],
        "key_2": {"key_1": "val", "key_2": "val"},
    }
```

JSON/YAML file input/output is supported.
- Input: Specify the path, either JSON (`.json`) or YAML (`.yaml`, `.yml`), as `d` argument for `SmallDict`.
- Output: Specify the path as `json_out` or `yaml_out` argument for `SmallDict.get` method.

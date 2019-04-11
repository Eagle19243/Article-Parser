# Article parser

## Creation of packages
Run `python3 setup.py sdist bdist_wheel`. This command will create two files in the `dist` folder,
one is a wheel binary package and the other is a source package. Both are compatible with `pip`.
Wheel packages are recommended but with older versions of pip it might be better to use a source package.

## Installation
To use this module in a different project, the package has to be installed with pip:
`pip install file_path_for_wheel_distribution_file`
After this you can import it like this:
```python
from article_parser import parse, transform
```

## Dependencies
This package doesn't have third party dependencies, only depends on `json` and `html.parser` from the
standard library (no installation required)

## Testing
From the package folder run `python3 -m pytest tests/test.py`

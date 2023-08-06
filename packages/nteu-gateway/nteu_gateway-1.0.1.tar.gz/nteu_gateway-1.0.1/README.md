# NTEU Gateway

## Upload package to Pypi

### Install dependencies
```BASH
pip install wheel
pip install twine
```

### Create package
```
python setup.py sdist bdist_wheel
```

## Upload package
```
python -m twine upload dist/*
```
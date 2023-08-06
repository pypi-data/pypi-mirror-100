### package code to install
python setup.py sdist
### show
tree .

###  use twine upload to pypi
pip install twine  

twine upload dist/*

### install package
python setup.py install
### build cython package
easy-to-python-build build_ext
### remove origin files, replace cython files
easy-to-python-release

### reference resources
https://blog.csdn.net/u012419550/article/details/105967006/
https://blog.csdn.net/lslxdx/article/details/73131664
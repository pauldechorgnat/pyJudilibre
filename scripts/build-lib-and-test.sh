#! /usr/bin/bash

python -m venv venv-build
source venv-build/bin/activate

# # Building the lib
pip install '.[build]' 
python -m build
twine check dist/*

# # Setting parameters
set -o allexport
source .env
set +o allexport

VERSION=$(pip show pyjudilibre | grep -i version | awk '{print $2}')


# # TestPyPI first:
twine upload \
 --password $JUDILIBRE_TEST_PYPI_TOKEN \
 --user '__token__' \
 --repository-url https://test.pypi.org/legacy/ dist/pyjudilibre-$VERSION-*
#  --verbose \


deactivate
rm -r venv-build

sleep 20

# Verify install in fresh venv:
python -m venv venv-test
source venv-test/bin/activate
pip install \
 --index-url https://test.pypi.org/simple/ \
 --extra-index-url https://pypi.org/simple \
 --no-cache-dir "pyjudilibre[test]==$VERSION"
python -c "from pyjudilibre import JudilibreClient; print('ok', JudilibreClient)"
python -m pytest tests

# cleaning
deactivate
rm -r venv-test
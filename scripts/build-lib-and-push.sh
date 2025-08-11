#! /usr/bin/bash

python -m venv venv-build
source venv-build/bin/activate

# # Building the lib
pip install '.[build]' 
python -m build
twine check dist/pyjudilibre-$VERSION*

# # Setting parameters
set -o allexport
source .env
set +o allexport

VERSION=$(pip show pyjudilibre | grep -i version | awk '{print $2}')

# Upload on PyPI:
twine upload \
 --verbose \
 --password $JUDILIBRE_PYPI_TOKEN \
 --user '__token__' \
 dist/pyjudilibre-$VERSION*

deactivate
rm -r venv-build

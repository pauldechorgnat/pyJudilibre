#! /usr/bin/bash


set -o allexport
source .env
set +o allexport

# pip install '.[dev]'
# python -m build
# twine check dist/*


# TestPyPI first:
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --password $JUDILIBRE_TEST_PYPI_TOKEN --user '__token__' 

# Verify install in fresh venv:
python -m venv /tmp/jcli && source /tmp/jcli/bin/activate
pip install -i https://test.pypi.org/simple/ pyjudilibre
python -c "from pyjudilibre import JudilibreClient; print('ok', Client)"


# Push to PyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/* --password $JUDILIBRE_PYPI_TOKEN --user '__token__' 

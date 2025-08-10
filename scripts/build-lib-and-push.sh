#! /usr/bin/bash
pip install './lib[dev]'
python -m build          
twine check dist/*
# TestPyPI first:
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Verify install in fresh venv:
# python -m venv /tmp/jcli && source /tmp/jcli/bin/activate
# pip install -i https://test.pypi.org/simple/ pyjudilibre
# python -c "from pyjudilibre import JudilibreClient; print('ok', Client)"

#! /usr/bin/bash
source venv/bin/activate
echo "Installing latest version of the library"
pip install -e . --no-deps -q

default_value="tests"
test_files=${1:-$default_value}

echo Testing $test_files
python3 -m pytest $test_files -vv --disable-warnings
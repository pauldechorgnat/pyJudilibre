#! /usr/bin/bash
source venv/bin/activate
echo "Installing latest version of the library"
pip install -e . --no-deps -q

test_files=${1:tests}
echo Testing $test_files
python3 -m pytest $test_files -vv --disable-warnings
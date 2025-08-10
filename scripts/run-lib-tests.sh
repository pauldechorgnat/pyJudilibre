#! /usr/bin/bash
source venv/bin/activate
pip install -e ./lib --config-settings editable_mode=strict --no-deps

test_files=${1:tests}
echo Testing $test_files
python3 -m pytest $test_files -vv --disable-warnings
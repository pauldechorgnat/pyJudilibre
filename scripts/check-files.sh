#! /usr/bin/bash
source venv/bin/activate

echo Sorting imports
python3 -m isort tests lib --trailing-comma

echo Formatting 
ruff format tests lib --line-length 120

echo Checking types
python3 -m mypy tests lib
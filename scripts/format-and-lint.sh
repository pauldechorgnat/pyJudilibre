echo Sorting imports
python3 -m isort tests lib --trailing-comma

echo Formatting 
ruff format tests lib --line-length 120
#! /usr/bin/bash

source venv/bin/activate

default_value="patch"
update_option=${1:-$default_value}

bump-my-version bump $update_option lib/pyjudilibre/pyjudilibre.py  docs/index.md -v
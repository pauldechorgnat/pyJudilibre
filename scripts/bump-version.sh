#! /usr/bin/bash

source venv/bin/activate

update_option=${1:patch}

bump-my-version bump $(update_option) lib/pyjudilibre/pyjudilibre.py
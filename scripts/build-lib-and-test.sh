#! /usr/bin/bash
set -euo pipefail

# Usage: retry MAX_RETRIES SLEEP_SECONDS command [args...]
retry() {
  local max="${1:-5}"
  local sleep_s="${2:-5}"
  shift 2
  local attempt=0
  echo "Waiting for command to succeed: $*"
  until "$@"; do
    attempt=$((attempt+1))
    if (( attempt >= max )); then
      echo "Command failed after ${attempt}/${max} attempts: $*" >&2
      return 1
    fi
    echo "Attempt ${attempt}/${max} failed. Retrying in ${sleep_s}s..."
    sleep "${sleep_s}"
  done
  echo "Command succeeded: $*"
}


# Creating a building virtual environment
python -m venv venv-build
source venv-build/bin/activate

# Building the lib
pip install '.[build]'
VERSION=$(pip show pyjudilibre | awk '/^Version:/{print $2}')
python -m build
twine check dist/pyjudilibre-${VERSION}*

# Setting parameters
set -o allexport
source .env
set +o allexport


# TestPyPI upload
twine upload \
  --verbose \
  --password "$JUDILIBRE_TEST_PYPI_TOKEN" \
  --user '__token__' \
  --repository-url https://test.pypi.org/legacy/ \
  "dist/pyjudilibre-${VERSION}-"*

# Removing building virtual environment
deactivate
rm -r venv-build


# Creating testing virtual environment
python -m venv venv-test
source venv-test/bin/activate

RETRIES=12
SLEEP=10

# Retry install from TestPyPI (propagation can take a bit)
retry "$RETRIES" "$SLEEP" pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  --no-cache-dir "pyjudilibre==${VERSION}"

python -c "from pyjudilibre import JudilibreClient; print('ok', JudilibreClient)"

pip install pytest==8.4.1 python-dotenv==1.1.1
python -m pytest tests

# Removing testing virtual environment
deactivate
rm -r venv-test

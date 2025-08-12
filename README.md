# pyJudilibre

`pyJudilibre` is a small Python wrapper to query the `JUDILIBRE` API from the French Supreme Court, la Cour de cassation. `JUDILIBRE` aims to give access to judiciary decisions.

<div style="align=center">
<img src="/docs/images/logo-white.svg" alt="Logo de pyjudilibre ?" width="200"/>
</div>

## Documentation

The documentation is [here](https://pyjudilibre.readthedocs.io/en/latest/).


## Requirements

This library relies on `pydantic` and `httpx` to perform queries to JUDILIBRE and to validate inputs and outputs.
You also need credentials from [PISTE](https://piste.gouv.fr).

## Installation

You can install it from `pyjudilibre`.

```sh
pip install pyjudilibre
```

## Simple usage

To instantiate the main class, `JudilibreClient`, you need to use your JUDILIBRE API key (see [here](https://pyjudilibre.readthedocs.io/en/latest/piste-set-up/)).

```python
import logging
from pyjudilibre import JudilibreClient

JUDILIBRE_API_KEY = "***"
client = JudilibreClient(
    judilibre_api_key=JUDILIBRE_API_KEY,
    logging_level=logging.DEBUG,
)
```

To get a decision, you need to provide its ID: 

```python
DECISION_ID = "667e51a56430c94f3afa7d0e"
decision = client.decision(decision_id=DECISION_ID)
```

## Description of the source code

The code of the library is in [lib/pyjudilibre](/lib/pyjudilibre/):

- the main class and its method are in `pyjudilibre.py`
- the enums are in `enums.py`
- the pydantic models are in `models.py`
- spectific exceptions are defined in `exceptions.py`
- `decorators.py` contains one decorator

Other folders are as follow:
- [tests](/tests) contains unit tests.
- [docs](/docs) contains documentation files.
- [scripts](/scripts/) contains useful scripts to develop the library

## Development setup

To set up a development environment, you should create a virtual environment named `venv`:

```sh
python3 -m venv venv
source venv/bin/activate

pip install '.[dev,build,doc,test]'
```

In `scripts`, you can use:

- [refresh-lib.sh](/scripts/refresh-lib.sh): To reinstall the latest local version of the library
- [check-files.sh](/scripts/check-files.sh): To run `isort`, `ruff` and `mypy` on the files
- [run-doc-server.sh](/scripts/run-doc-server.sh): To serve the doc on a live local server
- [run-lib-tests.sh](/scripts/run-lib-tests.sh): To run every unit test
- [bump-version.sh](/scripts/bump-version.sh): To bump versions in `pyproject.toml`, in the library files and in the documentation files.
- [build-and-test.sh](/scripts/build-and-test.sh): To build the library, push it to [Test-PyPI](https://test.pypi.org/project/pyjudilibre/), pull it in a test environment and run tests.
- [build-and-push.sh](/scripts/build-and-push.sh): To build the library, push it to [PyPI](https://pypi.org/project/pyjudilibre/).

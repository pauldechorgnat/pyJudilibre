# pyJudilibre

``pyJudilibre` is a small Python wrapper to query the `JUDILIBRE` API from the French Supreme Court, la Cour de cassation. `JUDILIBRE` aims to give access to judiciary decisions.

## 01 - Requirements

In order to use this library, you need credentials from [https://piste.gouv.fr/](https://piste.gouv.fr/). You can find tutorials [here](https://github.com/cour-de-cassation/judilibre-tutoriels) on how to get them.

## 02 - Installation

To install `pyJudilibre`, you can use `pip`: 

```sh
pip install pyjudilibre
```

It has three different extras:
- `[dev]` with development libraries
- `[test]` with test libraries
- `[build]` with build libraries

## 03 - Usage

The main class of this library is `JudilibreClient`. It serves as an interface for the whole API.
It has the following methods:

- `healthcheck`: returns the availability of the API
- `decision`: returns a decision based on its ID
- `search`: returns a list of search results based on a plain text search
- `export`: returns a list of decisions
- `stats`: returns aggregated data
- `transaction_history`: @TODO
- `scan`: @TODO



### 03.1 - Client initialization

To instantiate `JudilibreClient`, you need to pass the URL of the API and the key of the API:

```python

from pyjudilibre import JudilibreClient

client = JudilibreClient(
    judilibre_api_url=JUDILIBRE_API_URL,
    judilibre_api_url=JUDILIBRE_API_KEY,
)

```

### 03.2 - Healthcheck

The `.healthcheck` method queries the `GET /healthcheck`. This method will return `True` if the API is available or `False` if not.

```python

healthcheck: bool = client.healthcheck()
print(healthchek)

```

## 03.3 - Decision

The main endpoint of the API, `GET /decision` is available through the `.decision` method. It returns a [`JudilibreDecision`](/lib/pyjudilibre/models.py) if a decision ID is provided:

```python

DECISION_ID = "5fca9e9f7fceed9498daf2cf"

decision = client.decision(decision_id=DECISION_ID)
print(
    decision.jurisdiction,
    decision.date_decision,
)

```

## 03.4 - Stats

## 03.5 - Search

## 03.6 - Export


## 04 - Development

To work on the library, you can use a virtual environment and install all the extras:

```sh
git clone https://github.com/pauldechorgnat/pyJudilibre.git
cd pyJudilibre

python3 -m venv venv
pip install .[dev,test,build]
```


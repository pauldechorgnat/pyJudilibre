# First steps

Once you have set up your [PISTE](/set-up-piste) account and retrieved an API Key, you can instantiate the main class of this library: `JudilibreClient`. 

## JudilibreClient

`JudilibreClient` takes one argument: `judilibre_api_key`. If you do not wish to provide it in the code, you can set the `JUDILIBRE_API_KEY` environment key.

```python
from pyjudilibre import JudilibreClient

JUDILIBRE_API_KEY = "***"

client = JudilibreClient(
    judilibre_api_key=JUDILIBRE_API_KEY,
)
```

## Methods

`JudilibreClient` is the main entrypoint of the Judilibre API in `pyJudilibre`. You can access the different endpoint through it:

- `client.healthcheck(...)`: `GET /healthcheck`
- `client.decision(...)`: `GET /decision`
- `client.taxonomy(...)`: `GET /taxonomy`
- `client.search(...)`: `GET /search`
- `client.export(...)`: `GET /export`
- `client.transactional_history(...)`: `GET /transactionalhistory`

We have created other methods that can help paginate through `search`, `export` and `transactional_history` results:

- `client.paginate_search(...)`
- `client.paginate_export(...)`
- `client.paginate_transactional_history(...)`

## Models and Enums

Data is typed using pydantic in this pyJudilibre. You can find all the models in `pyjudilibre.models` and the enumerations in `pyjudilibre.enums`.

```python
from pyjudilibre.models import (
    JudilibreDecision,
    JudilibreSearchResult,
)
from pyjudilibre.enums import (
    JurisdictionEnum,
    LocationCAEnum,
    LocationTJEnum,
    LocationTCOMEnum,
)
```

Enums are used to give a developper friendly experience of internal values. For example, the `Tribunal judiciaire de Paris` will be modeled by `LocationTJEnum.tj_paris`. When used in a query, it will be transformed into `tj75056`, its technical ID.
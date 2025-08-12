# pyJudilibre `0.6.0`

## Presentation

`pyJudilibre` is a Python Wrapper for the Judilibre API. Judilibre is a REST API maintained by the French Cour de cassation, the French Supreme Court that serves court decisions from the French judiciary system. 

Judilibre is the back end to the [Cour de cassation Search Engine](https://www.courdecassation.fr/acces-rapide-judilibre).

This library aims to ease the use of this API for Python developpers. Arguments are checked, outputs are typed.

## Set up

To install `pyJudilibre`, you can follow the directions in [Get Started](/installation)

In order to use `pyjudilibre`, you need to have an active PISTE account that is set to accept the Terms of Service of Judilibre. You can click on [Credentials](/piste-set-up) to get instructions on how to get your credentials.

Finally, some examples are available at [First steps](/first-steps).


## API Presentation

### JudilibreClient

`JudilibreClient` is the main entrypoint of the Judilibre API in `pyJudilibre`. It only takes one required argument: `judilibre_api_key` which should be the value of your PISTE API key. If you do not wish to provide it in the code, you can set the `JUDILIBRE_API_KEY` environment variable.

```python
from pyjudilibre import JudilibreClient

JUDILIBRE_API_KEY = "***"

client = JudilibreClient(
    judilibre_api_key=JUDILIBRE_API_KEY,
)
```

### Methods

 You can access the different endpoint through `JudilibreClient`:

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

### Models and Enums

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


## Useful Links

- [PyPI](https://pypi.org/project/pyjudilibre/)
- [Github](https://github.com/pauldechorgnat/pyJudilibre)
- [ReadTheDocs](https://pyjudilibre.readthedocs.io/en/latest/)
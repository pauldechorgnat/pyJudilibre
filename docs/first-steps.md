# First steps

In this part, we will assume that the PISTE API key is set to `JUDILIBRE_API_KEY`.

## Initialization of the client

To instantiate `JudilibreClient`, we need to pass the local variable `JUDILIBRE_API_KEY`:

```python
import logging
from pyjudilibre import JudilibreClient

JUDILIBRE_API_KEY = "***"
client = JudilibreClient(
    judilibre_api_key=JUDILIBRE_API_KEY,
    logging_level=logging.DEBUG,
)
```

If you want less logs, you can use `logging.INFO`.

## Availability of the API

To check the availability of the app, we can use `.healthcheck(...)` that will return `True` if the API is available, `False`.

```python
api_is_available = client.healthcheck()
```

This can be used to create a function that will wait until the API is up:

```python
import time

while client.healthcheck() is False:
    time.sleep(5)

```

## Getting a particular decision

The Judilibre API is about retrieving judiciary decisions. In order to get one, we need to provide the ID of a decision to `.decision(...)`:

```python
DECISION_ID = "667e51a56430c94f3afa7d0e"

decision = client.decision(decision_id=DECISION_ID)

```

This will return a `JudilibreDecision` object. You can access its different attributes:

```python
print(
    decision.id,
    decision.jurisdiction,
    decision.decision_date,
    decision.number,
)
print(r.text)

```

## Searching decisions

You can perform a plain text search using Judilibre. The `.search(...)` will return a short version of the decision with some attributes missing but highlighted elements of the text.

```python

page_number = 0 # number of the page
page_size = 10 # number of results per page

query = "Au nom du peuple français"

total, results = client.search(
    query=query,
    page_number=page_number,
    page_size=page_size,
)
```
It also returns the total number of elements matching a particular query.

You can limit your results to certain jurisdiction (Cour de cassation, cours d'appel, tribunaux judiciaires, tribunaux de commerce) or to certain locations (courts). To do so, you can use enums:

```python
from pyjudilibre.enums import (
    JurisdictionEnum, 
    LocationCAEnum,
)

page_number = 0 # number of the page
page_size = 10 # number of results per page

query = "Au nom du peuple français"

total, results = client.search(
    query=query,
    page_number=page_number,
    page_size=page_size,
    jurisdictions=[JurisdictionEnum.cours_dappel],
    locations=[LocationCAEnum.ca_paris, Location.ca_aix_provence],
)

for index, r in enumerate(results):
    print(f"{index:02} ({r.score})")
    print(f"{r.jurisdiction} {r.decision_date} {r.number}")
    print(r.highlights.text)

```

Using the `page_number` parameter, you can paginate through the pages of results.

## Getting all search results

If you do not want to paginate through the results, you can let the client do it for you using `.paginate_search(...)`:


```python
results = client.paginate_search(
    query=query,
    jurisdictions=[JurisdictionEnum.cours_dappel],
    locations=[LocationCAEnum.ca_paris, Location.ca_aix_provence],
)
```

You can specify a `max_results` if you want only some of the total results. Note that this function does not return the number of results.

> Be aware that results are limited to the first 10 000 results of a query.

## Getting decision by batch

If you want to query decisions without using a plain text query, you can use only metadata with the `.export(...)` method. This method is also paginated and will return decisions as `JudilibreDecision` in batches:

```python
import datetime
from pyjudilibre.enums import LocationTCOMEnum

batch_number = 0
batch_size = 500

total, decisions = client.export(
    batch_number=batch_number,
    batch_size=batch_size,
    date_start=datetime.date(day=2025, month=1, day=1),
    date_end=datetime.date(day=2025, month=2, day=1),
    locations=[LocationTCOMEnum.tae_paris],
)
```
Another way to get theses decisions is to use `.scan(...)` and to provide an id:

```python
metadata_params = {}
total, decisions_batch1, search_after_id1 = client.scan(
    **metadata_params, 
    search_after=None,
)

total, decisions_batch2, search_after_id2 = client.scan(
    **metadata_params, 
    search_after=search_after_id1,
)
```

It also returns the total number of results.

## Paginating decisions by metadata

You can also use `.paginate_export(...)` to avoid paginating `batch_number` yourself:

```python
decisions = client.paginate_export(
    date_start=datetime.date(day=2025, month=1, day=1),
    date_end=datetime.date(day=2025, month=2, day=1),
    locations=[LocationTCOMEnum.tae_paris],
)

```

> Be aware that results are limited to the first 10 000 results of a query.

You can also use `.paginate_scan(...)`. This one is not limited to 10 000 results.

```python
decisions = client.paginate_scan(
    date_start=datetime.date(day=2025, month=1, day=1),
    date_end=datetime.date(day=2025, month=2, day=1),
    locations=[LocationTCOMEnum.tae_paris],
)

```

> This one is not limited to the first 10 000 results.

## Transactional history

Judilibre exposes an endpoint that allows you to track changes within the available data: `.transactional_history(...)`. If you want to get the information from a particular date, you can do:

```python
start_date = datetime.datetime.now() - datetime.timedelta(days=2)

total, transactions, from_id = client.transactional_history(
    date_start=start_date,
)

```

`total` is the total number of transactions. `from_id` is an ID that you can feed `.transactional_history(...)` to paginate through the results. 
You can also use `.paginate_transactional_history(...)` to get every transaction.


## Getting information on values

Judilibre gives the possibility to retrieve technical values for some variables. This is achieved via `.taxonomy(...)`. You need to give it a `taxon_id`:

```python
from pyjudilibre.enums import JudilibreTaxonEnum, JurisdictionEnum

taxons = client.taxonomy(
    taxon_id=JudilibreTaxonEnum.text_query_field,
    context=JurisdictionEnum.cour_de_cassation,
)

```


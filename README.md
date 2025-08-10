# pyJudilibre

`pyJudilibre` est une librairie Python qui permet de simplifier l'utilisation de l'API Judilibre avec Python. Le client reprend les différents endpoints de l'API tout en simplifiant certains aspects de cette utilisation, notamment la pagination des résultats.


## Initialiser le client

Pour créer le client, il faut possèder une clef d'API et renseigner l'URL de l'API:

```python
from pyjudilibre import JudilibreCient

JUDILIBRE_JUDILIBRE_API_URL = "https://api.piste.gouv.fr/cassation/judilibre/v1.0"
JUDILIBRE_API_KEY = "**************************************************"

client = JudilibreClient(
    judilibre_api_key=JUDILIBRE_API_KEY,
    api_url=JUDILIBRE_JUDILIBRE_API_URL,
)
```

## Méthodes

### Healthcheck

Ce client permet de vérifier si l'API est atteignable en interrogeant le endpoint `GET /healthcheck`.

```python
response = client.healthcheck()
print(response)
```

Cette méthode renvoie un booléen qui vaut `True` si l'API est atteignable et `False` sinon.

### Decision

Nous pouvons aussi récupérer une décision en utilisant le endpoint `GET /decision` et en fournissant un `id`.

```python
decision = client.get(decision_id="5fca56cd0a790c1ec36ddc07")
print(decision)
```

Les décisions renvoyées sont normalisées selon un modèle contrôlé par `pydantic`: [`JudilibreDecision`](/pyjudilibre/models/models.py#153).

### Search


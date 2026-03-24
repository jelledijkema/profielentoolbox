# Profielentoolbox

Een Python toolbox met de volgende tools voor de Profielentool:
  1. Extract GEF: Uitpakken .GEF bestand en teruggeven als lijst van dictionaries

## Vereisten

- Python 3.12

## Installatie

```bash
pip install -e .
```

---

## Tools

### ExtractGEF

Leest een `.gef` bestand en geeft een gestructureerd diepteprofiel terug met georeferentie-attributen, geschikt voor gebruik in FME.

```python
from profielentoolbox.extract_gef import parse_gef

profile = parse_gef("pad/naar/bestand.gef")
records = profile.to_records()  # lijst van dicts, één per dieptemeting
```

Elke record bevat de georeferentie-attributen uit de header (`x`, `y`, `z`, `coordinate_system`, etc.) gecombineerd met de meetreeks in het gef bestand.

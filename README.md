# Profielentoolbox

Een Python toolbox met tools voor de Profielentool:
  - Uitpakken .GEF bestanden en teruggeven aan FME Form

## Vereisten

- Python 3.12
- Git

## Aan de slag

### 1. Repository ophalen

```bash
git clone https://github.com/jelledijkema/profielentoolbox.git
cd profielentoolbox
```

### 2. Virtuele omgeving aanmaken

```bash
python3.12 -m venv .venv
```

Activeren:

- **Linux / macOS**
  ```bash
  source .venv/bin/activate
  ```
- **Windows**
  ```bash
  .venv\Scripts\activate
  ```

### 3. Afhankelijkheden installeren

```bash
pip install -r requirements-dev.txt
pip install -e .
```

### 4. Installatie controleren

```bash
pytest
```

Alle tests zouden moeten slagen.

---

## Tools

### ExtractGEF

Leest een `.gef` bestand en geeft een gestructureerd diepteprofiel terug met georeferentie-attributen, geschikt voor gebruik in FME.

```python
from profielentoolbox.extract_gef import parse_gef

profile = parse_gef("pad/naar/bestand.gef")
records = profile.to_records()  # lijst van dicts, één per dieptemeting
```

Elke record bevat de georeferentie-attributen uit de header (`x`, `y`, `z`, `coordinate_system`, etc.) gecombineerd met de meetwaarden op die diepte.

---

## Afhankelijkheden beheren

Afhankelijkheden worden beheerd met [pip-tools](https://github.com/jazzband/pip-tools).

- Voeg een runtime-afhankelijkheid toe aan `requirements.in`
- Voeg een ontwikkelafhankelijkheid toe aan `requirements-dev.in`
- Opnieuw compileren:
  ```bash
  pip-compile requirements.in -o requirements.txt
  pip-compile requirements-dev.in -o requirements-dev.txt
  ```
- Opnieuw installeren:
  ```bash
  pip install -r requirements-dev.txt
  ```

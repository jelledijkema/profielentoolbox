# Bijdragen aan Profielentoolbox

## Ontwikkelomgeving opzetten

### 1. Repository ophalen

```bash
git clone https://github.com/jelledijkema/profielentoolbox.git
cd profielentoolbox
```

### 2. Virtuele omgeving aanmaken en activeren

```bash
python3.12 -m venv .venv
```

- **Linux / macOS:** `source .venv/bin/activate`
- **Windows:** `.venv\Scripts\activate`

### 3. Afhankelijkheden installeren

```bash
pip install -r requirements-dev.txt
pip install -e .
```

---

## Voor het committen

### Tests draaien

```bash
pytest
```

Alle tests moeten slagen.

### Linter draaien

```bash
ruff check src/ tests/
```

Automatisch herstelbare problemen oplossen:

```bash
ruff check --fix src/ tests/
```

Los eventuele resterende fouten handmatig op voor je commit.

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

# Profielentoolbox

Een Python toolbox voor de Profielentool met de volgende tools:
1. **ExtractGEF** — leest een `.gef` bestand en geeft de data terug als lijst van dictionaries, geschikt voor gebruik in FME.

---

## Aan de slag

Volg de stappen hieronder om de toolbox lokaal te installeren en te controleren dat alles werkt.

### Stap 1 — Vereisten

Zorg dat het volgende geïnstalleerd is:

- **Python 3.12** — controleren met `python3 --version`
- **Git** — controleren met `git --version`

### Stap 2 — Repository ophalen

Open een terminal en voer uit:

```bash
git clone https://github.com/jelledijkema/profielentoolbox.git
cd profielentoolbox
```

### Stap 3 — Virtuele omgeving aanmaken

```bash
python3.12 -m venv .venv
```

Activeren:

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

Na het activeren zie je `(.venv)` voor je promptregel staan.

### Stap 4 — Toolbox installeren

```bash
pip install -e .
```

### Stap 5 — Controleren of alles werkt

Voer de tests uit:

```bash
pytest
```

Verwachte uitvoer:

Als alle tests slagen is de installatie geslaagd.

---

## Tools

### ExtractGEF

Leest een `.gef` bestand en geeft een gestructureerd diepteprofiel terug met georeferentie-attributen.

```python
from profielentoolbox.extract_gef import parse_gef

profile = parse_gef("pad/naar/bestand.gef")
records = profile.to_records()  # lijst van dicts, één per dieptemeting
```

Elke record bevat de georeferentie-attributen uit de header (`x`, `y`, `z`, `coordinate_system`, etc.) gecombineerd met de meetreeks in het gef bestand.

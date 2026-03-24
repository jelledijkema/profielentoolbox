import sys
import os
from pathlib import Path
import pytest

# Make fme/fmeobjects stubs importable when running outside FME
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "stubs"))


@pytest.fixture
def sample_gef_path() -> Path:
    """Path to the shared sample GEF fixture file."""
    return Path(__file__).parent / "fixtures" / "sample.gef"

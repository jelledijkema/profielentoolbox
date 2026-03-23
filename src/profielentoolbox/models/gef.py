"""Data models for GEF files."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GEFHeader:
    """Georeferencing and metadata extracted from the GEF header."""

    x: float | None = None
    y: float | None = None
    z: float | None = None
    coordinate_system: str | None = None
    file_date: str | None = None
    report_code: str | None = None
    company: str | None = None
    test_id: str | None = None


@dataclass
class GEFProfile:
    """A parsed GEF file: header metadata + depth profile rows."""

    header: GEFHeader = field(default_factory=GEFHeader)
    column_names: list[str] = field(default_factory=list)
    rows: list[dict] = field(default_factory=list)

    def to_records(self) -> list[dict]:
        """Return profile rows enriched with georeference attributes.

        Each record is a flat dict suitable for use in FME or other consumers.
        """
        geo = {
            "x": self.header.x,
            "y": self.header.y,
            "z": self.header.z,
            "coordinate_system": self.header.coordinate_system,
            "file_date": self.header.file_date,
            "report_code": self.header.report_code,
            "company": self.header.company,
            "test_id": self.header.test_id,
        }
        return [{**geo, **row} for row in self.rows]

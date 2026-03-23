"""ExtractGEF — parse a GEF file and return structured geotechnical data."""

from __future__ import annotations

import re
from pathlib import Path

from profielentoolbox.models.gef import GEFHeader, GEFProfile


def parse_gef(path: str | Path) -> GEFProfile:
    """Parse a GEF file and return a :class:`GEFProfile`.

    Args:
        path: Path to the .gef file.

    Returns:
        A GEFProfile with header metadata and depth profile rows.
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="replace")

    header_text, _, data_text = text.partition("#EOH=") # Split header and data at the #EOH= marker

    header = _parse_header(header_text)
    column_names, column_voids = _parse_column_info(header_text)
    separator = _parse_separator(header_text)
    rows = _parse_data(data_text, column_names, column_voids, separator)

    return GEFProfile(header=header, column_names=column_names, rows=rows)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_header(header_text: str) -> GEFHeader:
    h = GEFHeader() # Start with an empty header and fill in fields as we find them

    if m := re.search(r"#XYID\s*=\s*[^,]*,\s*([\d.+-]+)\s*,\s*([\d.+-]+)", header_text, re.IGNORECASE):
        h.x = float(m.group(1))
        h.y = float(m.group(2))

    if m := re.search(r"#XYID\s*=\s*(\d+)", header_text, re.IGNORECASE):
        h.coordinate_system = m.group(1)

    if m := re.search(r"#ZID\s*=\s*[^,]*,\s*([\d.+-]+)", header_text, re.IGNORECASE):
        h.z = float(m.group(1))

    if m := re.search(r"#FILEDATE\s*=\s*(.+)", header_text, re.IGNORECASE):
        h.file_date = m.group(1).strip()

    if m := re.search(r"#REPORTCODE\s*=\s*(.+)", header_text, re.IGNORECASE):
        h.report_code = m.group(1).strip()

    if m := re.search(r"#COMPANYID\s*=\s*(.+)", header_text, re.IGNORECASE):
        h.company = m.group(1).strip()

    if m := re.search(r"#TESTID\s*=\s*(.+)", header_text, re.IGNORECASE):
        h.test_id = m.group(1).strip()

    return h


def _parse_column_info(header_text: str) -> tuple[list[str], dict[int, str]]:
    """Return (column_names, column_voids) from #COLUMNINFO and #COLUMNVOID.

    Format: #COLUMNINFO= col_nr, unit, name, ...
    column_names is a list indexed by column position (0-based).
    column_voids maps col_nr (1-based) to its void string value.
    """
    columns: dict[int, str] = {}
    voids: dict[int, str] = {}

    for m in re.finditer(
        r"#COLUMNINFO\s*=\s*(\d+)\s*,\s*[^,]+\s*,\s*([^,\r\n]+)",
        header_text,
        re.IGNORECASE,
    ):
        col_nr = int(m.group(1))
        name = m.group(2).strip().replace(" ", "_").lower()
        columns[col_nr] = name

    for m in re.finditer(
        r"#COLUMNVOID\s*=\s*(\d+)\s*,\s*([^\r\n]+)", header_text, re.IGNORECASE
    ):
        col_nr = int(m.group(1))
        voids[col_nr] = m.group(2).strip()

    if not columns:
        return [], {}

    max_col = max(columns)
    names = [columns.get(i, f"col_{i}") for i in range(1, max_col + 1)]
    return names, voids


def _parse_separator(header_text: str) -> str:
    """Return the column separator character defined in the header (default: comma)."""
    if m := re.search(r"#COLUMNSEPARATOR\s*=\s*(.+)", header_text, re.IGNORECASE):
        return m.group(1).strip()
    return ","


def _parse_data(
    data_text: str,
    column_names: list[str],
    column_voids: dict[int, str],
    separator: str = ",",
) -> list[dict]:
    """Parse data rows after #EOH=.

    Values matching a column's void value are returned as None.
    Record separator characters (e.g. '!') at the end of a line are ignored.
    """
    rows = []
    for line in data_text.splitlines():
        line = line.strip().rstrip("!")  # strip record separator
        line = line.rstrip(separator).strip()  # strip trailing separator
        if not line:
            continue
        values = [v.strip() for v in line.split(separator)]
        row = {}
        for i, val in enumerate(values):
            col_name = column_names[i] if i < len(column_names) else f"col_{i + 1}"
            void_val = column_voids.get(i + 1)
            if void_val and val == void_val:
                row[col_name] = None
            else:
                try:
                    row[col_name] = float(val)
                except ValueError:
                    row[col_name] = val
        rows.append(row)
    return rows

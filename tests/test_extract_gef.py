"""Tests for ExtractGEF."""

import pytest

from profielentoolbox.extract_gef import parse_gef


def test_header_coordinates(sample_gef_path):
    """Test dat de georeferentiecoördinaten correct worden uitgelezen uit de header.
    We gebruiken de pytest.approx-functie om te controleren of de waarden van x, y en z
    in de header van het profiel overeenkomen met de verwachte waarden (letterlijk uit het SAMPLE_GEF),
    binnen een redelijke foutmarge (approx)"""

    profile = parse_gef(sample_gef_path)
    assert profile.header.x == pytest.approx(216320.000)
    assert profile.header.y == pytest.approx(464599.000)
    assert profile.header.z == pytest.approx(11.430)


def test_header_metadata(sample_gef_path):
    """Test dat andere metadatavelden correct worden uitgelezen uit de header."""
    profile = parse_gef(sample_gef_path)
    assert profile.header.company == "TestBedrijf"
    assert profile.header.test_id == "CPT000000028048"
    assert profile.header.report_code == "GEF-CPT-Report, 1, 1, 2"


def test_column_names(sample_gef_path):
    """Test dat de belangrijkste kolomnamen correct worden uitgelezen."""
    profile = parse_gef(sample_gef_path)
    assert "sondeertrajectlengte" in profile.column_names
    assert "conusweerstand" in profile.column_names
    assert "wrijvingsgetal" in profile.column_names


def test_data_rows(sample_gef_path):
    """Test dat de data-rijen correct worden uitgelezen en geconverteerd naar numerieke waarden"""
    profile = parse_gef(sample_gef_path)
    assert len(profile.rows) == 6 #Na #EOH= zijn er 6 datarijen (inclusief void-rij)
    # We controleren de waarden van de eerste rij tegen de verwachte waarden uit SAMPLE_GEF,
    assert profile.rows[0]["sondeertrajectlengte"] == pytest.approx(0.100)
    assert profile.rows[0]["conusweerstand"] == pytest.approx(29.610)
    assert profile.rows[0]["wrijvingsgetal"] == pytest.approx(0.8)


def test_void_values_become_none(sample_gef_path):
    """Test dat een void-waarde (999.999) wordt omgezet naar None."""
    profile = parse_gef(sample_gef_path)
    assert profile.rows[5]["conusweerstand"] is None # In de 6e rij (index 5) is conusweerstand 999.999, dus moet None zijn


def test_to_records_includes_georeference(sample_gef_path):
    """Test dat to_records() georeferentie-attributen toevoegt aan elke rij."""
    profile = parse_gef(sample_gef_path)
    records = profile.to_records()
    assert records[0]["x"] == pytest.approx(216320.000)
    assert records[0]["sondeertrajectlengte"] == pytest.approx(0.100)


def test_eerste_rij_output(sample_gef_path):
    """Laat zien hoe de eerste rij van de output eruitziet na parsing.

    Verwachte output eerste rij:
    {'sondeertrajectlengte': 0.1, 'conusweerstand': 29.61,
     'plaatselijke_wrijving': 0.255, 'wrijvingsgetal': 0.8}
    """
    profile = parse_gef(sample_gef_path)
    eerste_rij = profile.rows[0]

    assert eerste_rij["sondeertrajectlengte"] == pytest.approx(0.1)
    assert eerste_rij["conusweerstand"] == pytest.approx(29.61)
    assert eerste_rij["plaatselijke_wrijving"] == pytest.approx(0.255)
    assert eerste_rij["wrijvingsgetal"] == pytest.approx(0.8)

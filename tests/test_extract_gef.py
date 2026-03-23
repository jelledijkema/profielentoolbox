"""Tests for ExtractGEF."""

from pathlib import Path

import pytest

from profielentoolbox.extract_gef import parse_gef, GEFHeader, GEFProfile


SAMPLE_GEF = ("""
    #GEFID= 1, 1, 0
    #COLUMN= 4
    #COLUMNINFO= 1, m (meter), sondeertrajectlengte, 1
    #COLUMNINFO= 2, MPa (megaPascal), conusweerstand, 2
    #COLUMNINFO= 3, MPa (megaPascal), plaatselijke wrijving, 3
    #COLUMNINFO= 4, % (procent; MPa/MPa), wrijvingsgetal, 4
    #COLUMNSEPARATOR= ;
    #COLUMNTEXT= 1, aan
    #COLUMNVOID= 1, 999.999
    #COLUMNVOID= 2, 999.999
    #COLUMNVOID= 3, 9.999
    #COLUMNVOID= 4, 999.9
    #COMPANYID= TestBedrijf
    #FILEDATE= 2026, 01, 09
    #FILEOWNER= Basisregistratie Ondergrond
    #LASTSCAN= 139
    #MEASUREMENTTEXT= 4, ONBEKEND, conustype
    #MEASUREMENTTEXT= 5, ??&ZW, omschrijving sondeerapparaat
    #MEASUREMENTTEXT= 6, NEN 3680, sondeernorm en kwaliteitsklasse
    #MEASUREMENTTEXT= 9, maaiveld, lokaal verticaal referentiepunt
    #MEASUREMENTTEXT= 20, onbekend, signaalbewerking uitgevoerd
    #MEASUREMENTTEXT= 21, onbekend, bewerking onderbrekingen uitgevoerd
    #MEASUREMENTTEXT= 42, -, methode verticale positiebepaling
    #MEASUREMENTTEXT= 43, -, methode locatiebepaling
    #MEASUREMENTTEXT= 101, bronhouder, 50200097, -
    #MEASUREMENTTEXT= 102, archiefoverdracht, kader aanlevering
    #MEASUREMENTTEXT= 103, onbekend, kader inwinning
    #MEASUREMENTTEXT= 104, uitvoerder locatiebepaling, wordt niet uitgeleverd, -
    #MEASUREMENTTEXT= 105, 1988, 12, 13
    #MEASUREMENTTEXT= 106, uitvoerder verticale positiebepaling, wordt niet uitgeleverd, -
    #MEASUREMENTTEXT= 107, 1988, 12, 13
    #MEASUREMENTTEXT= 109, nee, dissipatietest uitgevoerd
    #MEASUREMENTTEXT= 110, onbekend, expertcorrectie uitgevoerd
    #MEASUREMENTTEXT= 111, onbekend, aanvullend onderzoek uitgevoerd
    #MEASUREMENTTEXT= 112, 2009, 08, 14
    #MEASUREMENTTEXT= 113, -, -, -
    #MEASUREMENTTEXT= 115, IMBRO/A, kwaliteitsregime
    #MEASUREMENTTEXT= 116, 2017, 01, 11, 23, 8, 49
    #MEASUREMENTTEXT= 117, voltooid, registratiestatus
    #MEASUREMENTTEXT= 118, 2017, 01, 11, 23, 8, 49
    #MEASUREMENTTEXT= 119, nee, gecorrigeerd
    #MEASUREMENTTEXT= 121, nee, in onderzoek
    #MEASUREMENTTEXT= 123, nee, uit registratie genomen
    #MEASUREMENTTEXT= 125, nee, weer in registratie genomen
    #MEASUREMENTTEXT= 127, 4258, 52.166138, 6.283483
    #MEASUREMENTTEXT= 128, RDNAPTRANS2008, toegepaste transformatie
    #MEASUREMENTVAR= 5, 100, mm (millimeter), afstand conus tot midden kleefmantel
    #MEASUREMENTVAR= 12, 0, -, sondeermethode
    #MEASUREMENTVAR= 13, 0.10, m (meter), voorgeboord tot
    #MEASUREMENTVAR= 16, 13.900, m (meter), einddiepte
    #MEASUREMENTVAR= 17, 0, -, stopcriterium
    #PROJECTID= BRO
    #RECORDSEPARATOR= !
    #REPORTCODE= GEF-CPT-Report, 1, 1, 2
    #STARTDATE= 1988, 12, 13
    #STARTTIME= -, -, -
    #TESTID= CPT000000028048
    #XYID= 28992, 216320.000, 464599.000
    #ZID= 31000, 11.430
    #EOH=
    0.100;29.610;0.255;0.8;!
    0.200;21.770;0.333;1.5;!
    0.300;12.540;0.218;1.7;!
    0.400;11.250;0.113;1.0;!
    0.500;7.950;0.054;0.6;!
    0.600;999.999;0.041;0.5;!
""")


@pytest.fixture
def gef_file(tmp_path: Path) -> Path:
    """Creert een tijdelijk .gef-bestand.
    Pytest herkent tmp_path als ingebouwde fixture die een tijdelijke directory aanmaakt voor de test. 
    We schrijven de SAMPLE_GEF-tekst naar een bestand in deze directory en geven het pad terug.
    """
    p = tmp_path / "test.gef" 
    p.write_text(SAMPLE_GEF)
    return p


def test_header_coordinates(gef_file):
    """Test dat de georeferentiecoördinaten correct worden uitgelezen uit de header.
    We gebruiken de pytest.approx-functie om te controleren of de waarden van x, y en z 
    in de header van het profiel overeenkomen met de verwachte waarden (letterlijk uit het SAMPLE_GEF), 
    binnen een redelijke foutmarge (approx)"""

    profile = parse_gef(gef_file)
    assert profile.header.x == pytest.approx(216320.000)
    assert profile.header.y == pytest.approx(464599.000)
    assert profile.header.z == pytest.approx(11.430)


def test_header_metadata(gef_file):
    """Test dat andere metadatavelden correct worden uitgelezen uit de header."""
    profile = parse_gef(gef_file)
    assert profile.header.company == "TestBedrijf"
    assert profile.header.test_id == "CPT000000028048"
    assert profile.header.report_code == "GEF-CPT-Report, 1, 1, 2"


def test_column_names(gef_file):
    """Test dat de belangrijkste kolomnamen correct worden uitgelezen."""
    profile = parse_gef(gef_file)
    assert "sondeertrajectlengte" in profile.column_names
    assert "conusweerstand" in profile.column_names
    assert "wrijvingsgetal" in profile.column_names


def test_data_rows(gef_file):
    """Test dat de data-rijen correct worden uitgelezen en geconverteerd naar numerieke waarden""" 
    profile = parse_gef(gef_file)
    assert len(profile.rows) == 6 #Na #EOH= zijn er 6 datarijen (inclusief void-rij)
    # We controleren de waarden van de eerste rij tegen de verwachte waarden uit SAMPLE_GEF,
    assert profile.rows[0]["sondeertrajectlengte"] == pytest.approx(0.100)
    assert profile.rows[0]["conusweerstand"] == pytest.approx(29.610)
    assert profile.rows[0]["wrijvingsgetal"] == pytest.approx(0.8)


def test_void_values_become_none(gef_file):
    """Test dat een void-waarde (999.999) wordt omgezet naar None."""
    profile = parse_gef(gef_file)
    assert profile.rows[5]["conusweerstand"] is None


def test_to_records_includes_georeference(gef_file):
    """Test dat to_records() georeferentie-attributen toevoegt aan elke rij."""
    profile = parse_gef(gef_file)
    records = profile.to_records()
    assert records[0]["x"] == pytest.approx(216320.000)
    assert records[0]["sondeertrajectlengte"] == pytest.approx(0.100)



#--- Code for testing ---
#--- This part is mocking the code that would be in a PythonCaller that calls the hello_world tool. ---
#--  Can be copied directly into a PythonCaller transformer ---


import fme # This imports the stub, not the actual library
from fme import BaseTransformer
import fmeobjects # This imports the stub, not the actual library
import sys
import os

import json

class FeatureProcessor(BaseTransformer):
    """Template Class Interface:
    When using this class, make sure its name is set as the value of the 'Class to Process Features'
    transformer parameter.

    This class inherits from 'fme.BaseTransformer'. For full details of this class, its methods, and
    expected usage, see https://docs.safe.com/fme/html/fmepython/api/fme.html#fme.BaseTransformer.
    """

    def __init__(self):
        """Base constructor for class members."""
        super().__init__()
        # Add path and import here
        path = r'/home/jelledijkema/Klanten/Profielentool/src/' # change this to the actual path of your repo's src directory
        if os.path.exists(path):
            sys.path.insert(0, path)
            try:
                from profielentoolbox.extract_gef import parse_gef
                print("Import successful")
                self.parse_gef = parse_gef
            except ImportError as e:
                print(f"ImportError: {e}")

    def has_support_for(self, support_type: int):
        """This method is called by FME to determine if the PythonCaller supports Bulk mode,
        which allows for significant performance gains when processing large numbers of features.
        """
        return support_type == fmeobjects.FME_SUPPORT_FEATURE_TABLE_SHIM

    def input(self, feature: fmeobjects.FMEFeature):
        """This method is called for each feature which enters the PythonCaller."""
        if self.parse_gef:
            try:
                # Haal locatie .gef bestand op
                gef_file_path = feature.getAttribute('fme_dataset')  # locatie van .gef bestand
                
                print(f"Processing GEF file: {gef_file_path}")
                
                profile = self.parse_gef(gef_file_path)
                print("Parse successful")
            
                
                # Set attributes on the feature from the profile
                feature.setAttribute('x_coordinate', profile.header.x)
                feature.setAttribute('y_coordinate', profile.header.y)
                feature.setAttribute('z_coordinate', profile.header.z)
                feature.setAttribute('file_date', profile.header.file_date)
                feature.setAttribute('report_code', profile.header.report_code)
                feature.setAttribute('company', profile.header.company)
                feature.setAttribute('test_id', profile.header.test_id)
                feature.setAttribute('coordinate_system', profile.header.coordinate_system)
                feature.setAttribute('column_names', ','.join(profile.column_names))
                feature.setAttribute('data', json.dumps((profile.rows))) # dump van de data
                
                # Example: Set the first row's data (adjust as needed)
                if profile.rows:
                    first_row = profile.rows[0]
                    for key, value in first_row.items():
                        feature.setAttribute(f'first_row_{key}', value)

                
            except Exception as e:
                print(f"Error processing feature: {e}")
                # Optionally: self.reject_feature(feature, "PARSE_ERROR", str(e))
        
        
        self.pyoutput(feature, output_tag="PYOUTPUT")

    def close(self):
        """This method is called once all the FME Features have been processed from input()."""
        pass

    def process_group(self):
        """This method is called by FME for each group when group processing mode is enabled."""
        pass

    def reject_feature(self, feature: fmeobjects.FMEFeature, code: str, message: str):
        """This method can be used to output a feature to the <Rejected> port."""
        feature.setAttribute("fme_rejection_code", code)
        feature.setAttribute("fme_rejection_message", message)
        self.pyoutput(feature, output_tag="<Rejected>")

# -- End of code ---

import pytest


# --- Tests ---

def test_import_extract_gef():
    """Test that the extract_gef module is imported and parse_gef is available on the processor."""
    processor = FeatureProcessor()
    assert hasattr(processor, 'parse_gef'), "parse_gef should be available after init"


def test_parse_gef(sample_gef_path):
    """Test that input() parses a GEF file and sets header attributes on the feature."""
    processor = FeatureProcessor()
    feature = fmeobjects.FMEFeature()
    feature.setAttribute('fme_dataset', str(sample_gef_path))

    processor.input(feature)

    # Feature should be passed to output
    assert len(processor._output_features) == 1
    assert processor._output_features[0] == (feature, "PYOUTPUT")

    # Header attributes
    assert feature.getAttribute('x_coordinate') == pytest.approx(216320.000)
    assert feature.getAttribute('y_coordinate') == pytest.approx(464599.000)
    assert feature.getAttribute('z_coordinate') == pytest.approx(11.430)
    assert feature.getAttribute('company') == "TestBedrijf"
    assert feature.getAttribute('test_id') == "CPT000000028048"
    assert feature.getAttribute('report_code') == "GEF-CPT-Report, 1, 1, 2"

    # First row attributes
    assert feature.getAttribute('first_row_sondeertrajectlengte') == pytest.approx(0.100)
    assert feature.getAttribute('first_row_conusweerstand') == pytest.approx(29.610)
    assert feature.getAttribute('first_row_wrijvingsgetal') == pytest.approx(0.8)


def test_data_is_valid_json(sample_gef_path):
    """Test that the 'data' attribute contains valid JSON."""
    processor = FeatureProcessor()
    feature = fmeobjects.FMEFeature()
    feature.setAttribute('fme_dataset', str(sample_gef_path))

    processor.input(feature)

    data_json = feature.getAttribute('data')
    try:
        data = json.loads(data_json)
        assert isinstance(data, list), "Data should be a list of rows"
        assert all(isinstance(row, dict) for row in data), "Each row should be a dict"
    except json.JSONDecodeError:
        pytest.fail("Data attribute is not valid JSON")
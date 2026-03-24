#--- Code for testing ---
#--- This part is mocking the code that would be in a PythonCaller that calls the hello_world tool. ---
#--  Can be copied directly into a PythonCaller transformer ---


import fme # This imports the stub, not the actual library
from fme import BaseTransformer
import fmeobjects # This imports the stub, not the actual library
import sys
import os


class FeatureProcessor(BaseTransformer):
    """Template Class Interface:
    When using this class, make sure its name is set as the value of the 'Class to Process Features'
    transformer parameter.

    This class inherits from 'fme.BaseTransformer'. For full details of this class, its methods, and
    expected usage, see https://docs.safe.com/fme/html/fmepython/api/fme.html#fme.BaseTransformer.
    """

    def __init__(self):
        """Base constructor for class members."""
        # Add path and import here
        path = r'/home/jelledijkema/Klanten/Profielentool/src' # verander dit pad naar de locatie van jouw profielentoolbox package
        if os.path.exists(path):
            sys.path.insert(0, path)
            try:
                from profielentoolbox.hello_world import hello_world # Dit importeert de daadwerkelijke hello_world functie, niet een stub
                print("Import successful")
                self.result = hello_world()
                print(f"Function call successful: {self.result}")
            except ImportError as e:
                print(f"ImportError: {e}")

    def has_support_for(self, support_type: int):
        """This method is called by FME to determine if the PythonCaller supports Bulk mode,
        which allows for significant performance gains when processing large numbers of features.
        """
        return support_type == fmeobjects.FME_SUPPORT_FEATURE_TABLE_SHIM

    def input(self, feature: fmeobjects.FMEFeature):
        """This method is called for each feature which enters the PythonCaller."""
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

# --- Tests ---

def test_hello_world():
    """This statement is only printed, not returned.
    """
    processor = FeatureProcessor()
    assert processor.result != "Hello world!" 

def test_hello_world_again():
    """This statement is returned by the function, and should be exactly "Hello world again!".
    """
    processor = FeatureProcessor()
    assert processor.result == "Hello world again!"
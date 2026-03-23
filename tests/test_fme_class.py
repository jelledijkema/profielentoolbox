import fme
from fme import BaseTransformer
import fmeobjects
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
        path = r'/home/jelledijkema/Klanten/Profielentool/src/'
        if os.path.exists(path):
            sys.path.insert(0, path)
            try:
                from profielentoolbox.hello_world import hello_world
                print("Import successful")
                result = hello_world()
                assert result == "Hello world again!", "Assertion gefaald: Uitkomst Hello World komt niet overeen."
                print(f"Function call successful: {result}")
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
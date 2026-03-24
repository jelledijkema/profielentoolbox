"""Stub for Safe Software's fme module, used for testing PythonCaller code outside FME."""


class BaseTransformer:
    def __init__(self):
        self._output_features = []

    def pyoutput(self, feature, output_tag="PYOUTPUT"):
        self._output_features.append((feature, output_tag))

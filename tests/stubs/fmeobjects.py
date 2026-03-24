"""Stub for Safe Software's fmeobjects module, used for testing PythonCaller code outside FME."""

FME_SUPPORT_FEATURE_TABLE_SHIM = 1


class FMEFeature:
    def __init__(self):
        self._attributes = {}

    def setAttribute(self, name, value):
        self._attributes[name] = value

    def getAttribute(self, name):
        return self._attributes.get(name)

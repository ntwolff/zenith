"""
Base classes for models
"""
from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item) # pylint: disable=no-value-for-parameter
        except ValueError:
            return False
        return True


class BaseEnum(str, Enum, metaclass=MetaEnum):
    """
    Iterable base class for Enum classes.

    ***

    Usage:
    - Ex. `if ("type" in ExampleEnum)`
    """
    pass # pylint: disable=unnecessary-pass


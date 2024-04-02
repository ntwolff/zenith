"""
Base models
"""

from enum import Enum, EnumMeta

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    """
    Iterable base class for Enum classes.

    ***

    Usage:
    - Ex. `if ("type" in ExampleEnum)`
    """
    
    pass

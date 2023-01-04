from enum import Enum


class SheetType(Enum):
    SOURCE = 'source'
    MASTER = 'master'
    UPDATE = 'compare'
    SAP = 'SAP'


class labeles(Enum):
    REFERENCE = "reference"
    NEW = "dew"
    Updated = "updated"

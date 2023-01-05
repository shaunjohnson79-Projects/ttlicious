from dataclasses import dataclass


@dataclass
class SheetType:
    source: str
    master: str
    compare: str
    sap: str


@dataclass
class StatusLabels:
    reference: str
    new: str
    updated: str


@dataclass
class ColumnLabels:
    date: str
    status: str
    search: str

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
    current: str
    change: str


@dataclass
class ColumnLabels:
    date: str
    status: str
    search: str
    partNumber: str


@dataclass
class Paths:
    log: str
    data: str
    settingsXML: str


@dataclass
class ProgramSettingsClass:
    sheetType: SheetType
    statusLabels: StatusLabels
    columnLabels: ColumnLabels
    paths: Paths

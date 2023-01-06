from dataclasses import dataclass


@dataclass
class Columns:
    partNumber: list
    ignore: list
    compare: list
    masterUpdate: list


@dataclass
class Sheet:
    name: str
    nameRow: int
    columns: Columns


@dataclass
class SettingsMaster:
    sheet: list[Sheet]
    debug: bool

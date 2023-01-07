from dataclasses import dataclass
from omegaconf import MISSING


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
class SheetSettingsClass:
    sheet: list[Sheet]

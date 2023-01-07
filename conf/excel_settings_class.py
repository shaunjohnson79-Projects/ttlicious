from dataclasses import dataclass
from hydra.core.config_store import ConfigStore


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
class ExcelSettingsLink:
    sheetType: SheetType
    statusLabels: StatusLabels
    columnLabels: ColumnLabels
    paths: Paths

    def __post_init__(self):
        print(f"post init")

    def __init__(self):
        print(f"init")


def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(
        name="excel_settings_class_schema",
        node=ExcelSettingsLink,
    )


register_configs()
print(f"EOF Excel")

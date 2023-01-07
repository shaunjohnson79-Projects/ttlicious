from dataclasses import dataclass
from hydra.core.config_store import ConfigStore


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
class SheetSettingsLink:
    sheet: list[Sheet]

    def __post_init__(self):
        print(f"asdasdasd")


def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(
        name="sheet_settings_class_schema",
        node=SheetSettingsLink,
    )


register_configs()
print(f"EOF Excel")

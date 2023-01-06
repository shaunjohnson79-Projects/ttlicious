import hydra
from hydra.core.config_store import ConfigStore
from settings.sheet_settings_classes import SettingsMaster


cs = ConfigStore.instance()
cs.store(group="db", name="sheet_settings", node=SettingsMaster)


@hydra.main(config_path="settings", config_name="sheet_settings", version_base=None)
def main(cfg: SettingsMaster) -> None:

    aa = cfg.settings.sheet[0].nameRow
    print(aa)
    bb = cfg.sheet[0]
    print(bb)


if __name__ == "__main__":
    main()

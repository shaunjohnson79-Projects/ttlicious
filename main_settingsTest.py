import hydra
from hydra.core.config_store import ConfigStore
from settings.program_settings_classes import ProgramSettingsClass
#from settings.sheet_settings_classes import SheetSettingsClass
from omegaconf import OmegaConf


cs = ConfigStore.instance()
cs.store(name="sheet_settings_schema", node=ProgramSettingsClass)
#cs.store(name="program_setting_schema", node=SheetSettingsClass)


with hydra.initialize(config_path='settings', version_base='1.3.1'):
    #hydra.main(config_path="settings", config_name="program_settings", version_base=None)
    #cfg1: MNISTConfig = hydra.compose(config_name="program_settings")
    cfg1 = hydra.compose(config_name="program_settings")

# with hydra.initialize(config_path='settings', version_base='1.3.1'):
#     #hydra.main(config_path="settings", config_name="sheet_settings", version_base=None)
#     #cfg2: MasterSettings = hydra.compose(config_name="sheet_settings")
#     cfg2 = hydra.compose(config_name="sheet_settings")


def main() -> None:
    # print(cfg1.statusLabels.new)
    # cfg1.columnLabels.date

    # print(
    aa = OmegaConf.to_yaml(cfg2)

    #aa = cfg2.values()
    # print(aa)
    # cfg2.

    pass

    # @hydra.main(config_path="settings", config_name="sheet_settings", version_base=None)
    # # @hydra.main(config_path="settings", config_name="program_settings", version_base=None)
    # def main(cfg: MasterSettings) -> None:
    #     print(cfg.settings.sheet[0].nameRow)
    #     print(cfg.settings.debug)

    #     bb = len(cfg.settings.sheet)

    #     print(bb)


if __name__ == "__main__":
    main()

import hydra
from hydra.core.config_store import ConfigStore
from settings.config_classes import MNISTConfig

import src.methods as methods
import src.classes as classes


#cs = ConfigStore.instance()
#cs.store(group="db", name="program_settings", node=MNISTConfig)


@hydra.main(config_path="settings", config_name="sheet_settings", version_base=None)
def main(cfg) -> None:

    aa = 1


if __name__ == "__main__":
    main()

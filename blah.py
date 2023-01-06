
import hydra
from settings.config_classes import MNISTConfig
with hydra.initialize(config_path='../../settings/', version_base=None):
    cfg: MNISTConfig = hydra.compose(config_name="program_settings")


def my_app():
    # MNISTConfig

    # cfg1 = hydra.compose(config_name="program_settings")
    # assert isinstance(cfg1, MNISTConfig)

    # cfg2 = MNISTConfig(hydra.compose(config_name="program_settings"))

    # cfg3: MNISTConfig = hydra.compose(config_name="program_settings", return_hydra_config=True)

    cfg4: MNISTConfig = hydra.compose(config_name="program_settings")

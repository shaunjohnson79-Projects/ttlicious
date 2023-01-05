import hydra
from omegaconf import OmegaConf


def my_app():
    cfg = hydra.compose(config_name="program_settings")
    print(OmegaConf.to_yaml(cfg))

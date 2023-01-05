import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import OmegaConf

from config_classes import MNISTConfig
import src.methods as methods
import src.classes as classes
import blah

cs = ConfigStore.instance()
cs.store(name="program_settings", node=MNISTConfig)


@hydra.main(config_path="settings", config_name="program_settings")
def main(cfg: MNISTConfig) -> None:

    blah.my_app()
    return

    print(cfg.columnLabels.date)
    print(cfg.paths.settingsXML)

    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': f'{cfg.paths.settingsXML}settings.xml'})
    #fileInfo.update({'XML': f'{cfg.paths.settingsXML}settingsQuick.xml'})
    fileInfo.update({'XLS_source': f'{cfg.paths.data}20210323 Hinterkipper_de en_finala.xlsx'})
    fileInfo.update({'XLS_master': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_master.xlsx'})

    # Get the filename to output
    tempFileName = fileInfo['XLS_source'].replace(".xls", ".compare.xls")
    fileInfo.update({'XLS_compare': tempFileName})

    # Read in the settings
    settings = classes.XMLSettings(fileInfo['XML'])

    # Read in the XLS
    XLSSource = classes.XLSSource(fileInfo['XLS_source'], settings)
    XLSMaster = classes.XLSMaster(fileInfo['XLS_master'], settings)

    # get the compared XLS
    XLSCompare = methods.compareSourceToMaster(XLSSource, XLSMaster, settings)

    # Write a file if changes were found
    if XLSCompare.modificationFound:
        methods.writeToXLS(XLSCompare, fileInfo['XLS_compare'], settings)
    else:
        print(f"No updates found in {fileInfo['XLS_source']}")


if __name__ == "__main__":
    main()

import hydra
from hydra.core.config_store import ConfigStore
from settings.config_classes import MNISTConfig

import src.classes as classes
import src.methods as methods

#import hydra
#from hydra.core.config_store import ConfigStore

cs = ConfigStore.instance()
cs.store(group="db", name="program_settings", node=MNISTConfig)


@hydra.main(config_path="settings", config_name="program_settings", version_base=None)
def main(cfg: MNISTConfig) -> None:

    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': f'{cfg.paths.settingsXML}settings.xml'})
    fileInfo.update({'XML': f'{cfg.paths.settingsXML}settingsQuick.xml'})
    fileInfo.update({'XLS_update': f'{cfg.paths.data}20210323 Hinterkipper_de en_finala.update.xlsx'})
    fileInfo.update({'XLS_masterRef': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_master.xlsx'})
    fileInfo.update({'XLS_masterWrite': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_masterv2.xlsx'})
    fileInfo.update({'XLS_SAP': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_SAP.xlsx'})

    # Read in the settings
    settings = classes.XMLSettings(fileInfo['XML'])
    # print(settings)

    # Read in the XLS
    XLSUpdate = classes.XLSUpdate(fileInfo['XLS_update'], settings)
    XLSMaster = classes.XLSMaster(fileInfo['XLS_masterRef'], settings)

    # Calculate the new master file
    XLSMaster = methods.updateMaster(XLSUpdate, XLSMaster)

    # Calculate the file to return to SAP
    XLSUpdate = methods.createSAPupdate(XLSUpdate)

    methods.writeToXLS(XLSMaster, fileInfo['XLS_masterWrite'], settings)
    methods.writeToXLS(XLSUpdate, fileInfo['XLS_SAP'], settings)


if __name__ == "__main__":
    main()

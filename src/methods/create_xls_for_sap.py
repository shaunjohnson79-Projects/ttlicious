from settings.program_settings_classes import MNISTConfig
import hydra
from .. import classes

import os
print(os.getcwd())


with hydra.initialize(config_path='../../settings/', version_base=None):
    cfg: MNISTConfig = hydra.compose(config_name="program_settings")


def createSAPupdate(XLSUpdate: classes.XLSUpdate) -> classes.XLSUpdate:

    XLSReturn = XLSUpdate
    #XLSReturn.type = "SAP"

    sheetList = XLSUpdate.getSheetList()
    for sheetName in sheetList:
        # Get the sheets manually
        update = XLSUpdate.getSheet(sheetName)
        print(sheetName)

        update.data = update.data.loc[update.data[cfg.columnLabels.status] == cfg.statusLabels.update]

        # Remove columns from print list
        removeList = [cfg.columnLabels.status, cfg.columnLabels.date, cfg.columnLabels.search]
        for tempValue in removeList:
            if tempValue in update.printList:
                update.printList.remove(tempValue)

        # Return the sheet
        XLSReturn.setSheet(sheetName, update)

    return XLSReturn

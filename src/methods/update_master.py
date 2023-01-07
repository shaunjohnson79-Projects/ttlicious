from .. import classes

import hydra
from settings.program_settings_classes import MNISTConfig
with hydra.initialize(config_path='../../settings/', version_base=None):
    cfg: MNISTConfig = hydra.compose(config_name="program_settings")


def updateMaster(XLSUpdate: classes.XLSUpdate, XLSMaster: classes.XLSMaster) -> classes.XLSMaster:
    """Update the master sheet with data that was flagged update"""

    # Define the return variable
    XLSreturn = XLSMaster

    sheetList = XLSUpdate.getSheetList()
    for sheetName in sheetList:
        # Get the sheets manually
        updateSheet = XLSUpdate.getSheet(sheetName)
        masterSheet = XLSMaster.getSheet(sheetName)
        returnSheet = masterSheet

        # Display to screen
        print("Update Sheet: {}".format(updateSheet.name))

        for UP, tempLine in updateSheet.data.iterrows():
            tempLine = tempLine.copy()

            if tempLine[cfg.columnLabels.status] == cfg.statusLabels.update:

                # get the searchIndex in the master file
                searchTerm = tempLine[cfg.columnLabels.search]
                MP = masterSheet.data.index[masterSheet.data[cfg.columnLabels.search] == searchTerm].values

                if len(MP) > 1:
                    # check for duplicates in master
                    raise Exception("Write code here")
                elif len(MP) == 0:
                    # Create pointer based on UP position
                    MP2 = UP+0.5
                    tempLine[cfg.columnLabels.status] = cfg.statusLabels.new
                elif len(MP) == 1:
                    # Get pointer for row to replace
                    MP2 = int(MP)
                    tempLine[cfg.columnLabels.status] = cfg.statusLabels.change
                else:
                    pass

                # Display to screen
                print(f"  Update Master: {searchTerm:25} {tempLine[cfg.columnLabels.status]}")

                # Update or add the line
                XLSreturn.modificationFound = True
                #returnSheet.data.loc[MP2] = tempLine

        # Reorder the index
        returnSheet.data = returnSheet.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSreturn.setSheet(sheetName, returnSheet)

    return XLSreturn

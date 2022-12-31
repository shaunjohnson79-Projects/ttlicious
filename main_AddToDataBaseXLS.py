import pandas as pd
import OBL
import ttliciousMethods


def main() -> None:
    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': 'settings.xml'})
    #fileInfo.update({'XML': 'settingsQuick.xml'})
    fileInfo.update({'XLS_update': '20210323 Hinterkipper_de en_finala.update.xlsx'})
    fileInfo.update({'XLS_masterRef': '20210323 Hinterkipper_de en_final_master.xlsx'})
    fileInfo.update({'XLS_masterWrite': '20210323 Hinterkipper_de en_final_masterv2.xlsx'})

    # Read in the settings
    settings = OBL.XMLSettings(fileInfo['XML'])
    # print(settings)

    # Read in the XLS
    XLSUpdate = OBL.XLSUpdate(fileInfo['XLS_update'], settings)
    XLSMaster = OBL.XLSMaster(fileInfo['XLS_masterRef'], settings)

    # Calculate the new master file
    XLSMaster = ttliciousMethods.updateMaster(XLSUpdate, XLSMaster)

    ttliciousMethods.writeToXLS(XLSMaster, fileInfo['XLS_masterWrite'], 'dataBase', settings)


if __name__ == "__main__":
    main()

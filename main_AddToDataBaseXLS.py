import pandas as pd
import objectXLS
import objectXMLSettings
import ttliciousProcess


def main() -> None:
    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': 'settings.xml'})
    #fileInfo.update({'XML': 'settingsQuick.xml'})
    fileInfo.update({'XLS_update': '20210323 Hinterkipper_de en_finala.update.xlsx'})
    fileInfo.update({'XLS_masterRef': '20210323 Hinterkipper_de en_final_master.xlsm'})
    fileInfo.update({'XLS_masterWrite': '20210323 Hinterkipper_de en_final_masterv2.xlsm'})

    # Read in the settings
    settings = objectXMLSettings.parseXML(fileInfo['XML'])
    # print(settings)

    # Read in the XLS
    XLSUpdate = objectXLS.readXLSUpdate(fileInfo['XLS_update'], settings)
    XLSMaster = objectXLS.readXLSMaster(fileInfo['XLS_masterRef'], settings)
    #assert isinstance(XLSUpdate, objectXLS.readXLSUpdate)
    #assert isinstance(XLSMaster, objectXLS.readXLSMaster)

    # Calculate the new master file
    XLSMaster = ttliciousProcess.updateMaster(XLSUpdate, XLSMaster)

    ttliciousProcess.writeToXLS(XLSMaster, fileInfo['XLS_masterWrite'], 'dataBase', settings)


if __name__ == "__main__":
    main()

import ttlicious.classes as classes
import ttlicious.methods as methods


def main() -> None:
    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': 'settings.xml'})
    #fileInfo.update({'XML': 'settingsQuick.xml'})
    fileInfo.update({'XLS_update': '20210323 Hinterkipper_de en_finala.update.xlsx'})
    fileInfo.update({'XLS_masterRef': '20210323 Hinterkipper_de en_final_master.xlsx'})
    fileInfo.update({'XLS_masterWrite': '20210323 Hinterkipper_de en_final_masterv2.xlsx'})
    fileInfo.update({'XLS_SAP': '20210323 Hinterkipper_de en_final_SAP.xlsx'})

    # Read in the settings
    settings = classes.XMLSettings(fileInfo['XML'])
    # print(settings)

    # Read in the XLS
    XLSUpdate = classes.XLSUpdate(fileInfo['XLS_update'], settings)
    XLSMaster = classes.XLSMaster(fileInfo['XLS_masterRef'], settings)

    # Calculate the new master file
    XLSMaster2 = methods.updateMaster(XLSUpdate, XLSMaster)

    # Calculate the file to return to SAP
    XLSUpdate2 = methods.createSAPupdate(XLSUpdate)

    methods.writeToXLS(XLSMaster2, fileInfo['XLS_masterWrite'], settings)
    methods.writeToXLS(XLSUpdate2, fileInfo['XLS_SAP'], settings)


if __name__ == "__main__":
    main()

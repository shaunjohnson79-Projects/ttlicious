import OBL
import ttliciousMethods


def main() -> None:
    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': 'settings.xml'})
    # fileInfo.update({'XML':'settingsQuick.xml'})
    fileInfo.update({'XLS_source': '20210323 Hinterkipper_de en_finala.xlsx'})
    fileInfo.update({'XLS_master': '20210323 Hinterkipper_de en_final_master.xlsx'})

    # Get the filename to output
    tempFileName = fileInfo['XLS_source'].replace(".xls", ".compare.xls")
    fileInfo.update({'XLS_compare': tempFileName})

    # Read in the settings
    settings = OBL.XMLSettings(fileInfo['XML'])
    # print(settings)

    # Read in the XLS
    XLSSource = OBL.XLSSource(fileInfo['XLS_source'], settings)
    XLSMaster = OBL.XLSMaster(fileInfo['XLS_master'], settings)

    # get the compared XLS
    XLSCompare = ttliciousMethods.compareSourceToMaster(XLSSource, XLSMaster, settings)

    # Write a file if changes were found
    if XLSCompare.modificationFound:
        ttliciousMethods.writeToXLS(XLSCompare, fileInfo['XLS_compare'], 'compare', settings)
    else:
        print(f"No updates found in {fileInfo['XLS_source']}")


if __name__ == "__main__":
    main()

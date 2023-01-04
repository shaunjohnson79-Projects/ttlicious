from .. import classes


def createSAPupdate(XLSUpdate: classes.XLSUpdate) -> classes.XLSUpdate:

    XLSReturn = XLSUpdate
    #XLSReturn.type = "SAP"

    sheetList = XLSUpdate.getSheetList()
    for sheetName in sheetList:
        # Get the sheets manually
        update = XLSUpdate.getSheet(sheetName)
        print(sheetName)

        update.data = update.data.loc[update.data['status'] == 'update']

        # Remove columns from print list
        removeList = ["status", "date", "searchIndex"]
        for tempValue in removeList:
            if tempValue in update.printList:
                update.printList.remove(tempValue)

        # Return the sheet
        XLSReturn.setSheet(sheetName, update)

    return XLSReturn

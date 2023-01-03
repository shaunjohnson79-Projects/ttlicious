from .. import classes


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

        print(updateSheet.data)

        # Display to screen
        print("Update Sheet: {}".format(updateSheet.name))

        for UP, tempLine in updateSheet.data.iterrows():
            tempLine = tempLine.copy()

            if tempLine['status'] == 'update':

                # get the searchIndex in the master file
                searchTerm = tempLine['searchIndex']
                MP = masterSheet.data.index[masterSheet.data['searchIndex'] == searchTerm].values

                if len(MP) > 1:
                    # check for duplicates in master
                    raise Exception("Write code here")
                elif len(MP) == 0:
                    # Create pointer based on UP position
                    MP2 = UP+0.5
                    tempLine['status'] = 'new'
                elif len(MP) == 1:
                    # Get pointer for row to replace
                    MP2 = int(MP)
                    tempLine['status'] = 'change'
                else:
                    pass

                # Display to screen
                print(f"  Update Master: {searchTerm:25} {tempLine['status']}")

                # Update or add the line
                XLSreturn.modificationFound = True
                #returnSheet.data.loc[MP2] = tempLine

        # Reorder the index
        returnSheet.data = returnSheet.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSreturn.setSheet(sheetName, returnSheet)

        print(updateSheet.data)
    return XLSreturn

from .. import classes


def updateMaster(XLSUpdate: classes.XLSUpdate, XLSMaster: classes.XLSMaster) -> classes.XLSMaster:
    """Update the master sheet with data that was flagged update"""

    # Define the return variable
    XLSreturn = XLSMaster

    sheetList = XLSUpdate.getSheetList()
    for sheetName in sheetList:
        # Get the sheets manually
        update = XLSUpdate.getSheet(sheetName)
        master = XLSMaster.getSheet(sheetName)

        # Display to screen
        print("Update Sheet: {}".format(update.name))

        for UP, updateLine in update.data.iterrows():
            if updateLine['status'] == 'update':

                # get the searchIndex in the master file
                searchTerm = updateLine['searchIndex']
                MP = master.data.index[master.data['searchIndex'] == searchTerm].values

                if len(MP) > 1:
                    # check for duplicates in master
                    raise Exception("Write code here")
                elif len(MP) == 0:
                    # Create pointer based on UP position
                    MP = UP+0.5
                    updateLine['status'] = 'new'
                    XLSreturn.modificationFound = True

                else:
                    # Get pointer for row to replace
                    MP = int(MP)
                    updateLine['status'] = 'change'
                    XLSreturn.modificationFound = True

                # Display to screen
                print(f"  Update Master: {searchTerm:25} {updateLine['status']}")

                # Update or add the line
                master.data.loc[MP] = updateLine
        # Reorder the index
        master.data = master.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSreturn.setSheet(sheetName, master)
    return XLSreturn

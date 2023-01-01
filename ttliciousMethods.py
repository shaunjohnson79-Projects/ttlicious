import pandas as pd
import OBL


def getListToUpdate(XLSUpdate: OBL.XLSUpdate) -> OBL.XLSUpdate:
    pass


def updateMaster(XLSUpdate: OBL.XLSUpdate, XLSMaster: OBL.XLSMaster) -> OBL.XLSMaster:
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


def compareSourceToMaster(XLSSource: OBL.XLSSource, XLSMaster: OBL.XLSMaster, settings: OBL.XMLSettings) -> OBL.XLSUpdate:
    """
    Return XLScompare after comparing sheets in source with the master
    """

    # Get the return variable
    XLSCompare = XLSSource
    XLSCompare.convertClass(OBL.XLSCompare)

    sheetList = XLSSource.getSheetList()
    for sheetName in sheetList:

        # Get the sheets manually
        source = XLSSource.getSheet(sheetName)
        master = XLSMaster.getSheet(sheetName)

        # Display to screen
        print("Compare Sheet: {}".format(source.name))

        # get list of columns to use for compare
        compareList = source.getCompareList(source.name, settings)
        indexS = source.data.columns.get_indexer(compareList)
        indexM = master.data.columns.get_indexer(compareList)
        # print(compareList)
        # print(indexM)
        # print(indexS)

        for SP, sourceLine in source.data.iterrows():
            # Get the search terms
            searchTerm = source.data.at[SP, 'searchIndex']
            MP = master.data.index[master.data['searchIndex'] == searchTerm].values

            if len(MP) > 1:
                # check for duplicates in master
                raise Exception("Write code here")
            elif len(MP) == 0:
                # check for data which is not in master
                source.data.at[SP, 'status'] = 'new'
                print("  {} New Line   : {}".format(SP, searchTerm))
                XLSCompare.modificationFound = True
                continue
            else:
                MP = int(MP)

            for compareColumn in compareList:
                tempSource = str(source.data.at[SP, compareColumn])
                tempMaster = str(master.data.at[MP, compareColumn])
                if tempSource != tempMaster:
                    source.data.at[SP, 'status'] = 'change'
                    print("  {} Line Change: {} {}".format(
                        SP, searchTerm, compareColumn))
                    rowToInsert = master.data.loc[MP]
                    source.data.loc[SP+0.5] = rowToInsert
                    XLSCompare.modificationFound = True

        # Reorder the index
        source.data = source.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSCompare.setSheet(sheetName, source)

    return XLSCompare


def writeToXLS(XLSData: OBL.XLSFile, fileName: str, TTfileType: str, settings: OBL.XMLSettings) -> bool:
    """
    Write XLS data to a file
    """

    # Check the filename
    fileName = fileName.replace(".xlsm", ".xlsx")

    # Prepare the data to write
    sheetList = XLSData.getSheetList()
    for sheetName in sheetList:

        # Get sheet data
        sheet = XLSData.getSheet(sheetName)

        # Update the data with the print columns only
        sheet.data = sheet.data[sheet.printList].copy()

        # Replace Duplicate Columns with Original Columns
        sheet.replaceDuplicateColumnsWithOriginalColumns()

        XLSData.setSheet(sheetName, sheet)

        str(XLSData.type).lower()

        # Define the colurs of the rows
        colour_new = False
        colour_change = False
        colour_reference = False
        match str(XLSData.type).lower():
            case 'compare':
                colour_new = '#FCF3CF'
                colour_change = '#D4E6F1'
                colour_reference = '#D1F2EB'
            case 'master':
                colour_new = '#FCF3CF'
                colour_change = '#D4E6F1'
            case _:
                pass

    # Write the data to file
    with pd.ExcelWriter(fileName, engine='xlsxwriter',) as writer:
        print(f"Write {fileName}")
        for sheetName in sheetList:
            # Get sheet data
            sheet = XLSData.getSheet(sheetName)

            # tempSheet=XLSCompare.sheet[SPS]
            rowOffSet = settings.getNameRow(sheetName)
            sheet.data.to_excel(writer, sheet_name=sheet.name, index=False, startrow=rowOffSet-1)
            print(f"  Sheet: {sheetName}")

            workbook = writer.book
            worksheet = writer.sheets[sheet.name]

            format_new = workbook.add_format({'bg_color': colour_new})
            format_change = workbook.add_format({'bg_color': colour_change})
            format_reference = workbook.add_format({'bg_color': colour_reference})

            status = sheet.data['status'].tolist()
            for i, tempStatus in enumerate(status):
                match str(tempStatus).lower():
                    case 'new':
                        worksheet.set_row(i+1+rowOffSet-1, cell_format=format_new)
                    case 'change':
                        worksheet.set_row(i+1+rowOffSet-1, cell_format=format_change)
                    case 'reference':
                        worksheet.set_row(i+1+rowOffSet-1, cell_format=format_reference)
                    case _:
                        pass
    return True

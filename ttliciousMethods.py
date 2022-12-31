import pandas as pd
import OBL


def updateMaster(XLSUpdate: OBL.XLSFile, XLSMaster: OBL.XLSFile) -> OBL.XLSMaster:
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
                else:
                    # Get pointer for row to replace
                    MP = int(MP)
                    updateLine['status'] = 'change'

                # Display to screen
                print(f"  Update Master: {searchTerm:25} {updateLine['status']}")

                # Update or add the line
                master.data.loc[MP] = updateLine
        # Reorder the index
        master.data = master.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSreturn.setSheet(sheetName, master)
    return XLSreturn


def compareSourceToMaster(XLSSource: OBL.XLSFile, XLSMaster: OBL.XLSFile, settings: OBL.XMLSettings) -> OBL.XLSSource:
    """
    Return XLScompare after comparing sheets in source with the master
    """

    # Define the return variable
    XLSreturn = XLSSource
    XLSreturn.modificationFound = False

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
                XLSreturn.modificationFound = True
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
                    XLSreturn.modificationFound = True

        # Reorder the index
        source.data = source.data.sort_index().reset_index(drop=True)

        # Add changed source data to XLSreturn
        XLSreturn.setSheet(sheetName, source)

    return XLSreturn


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

        originalColumns = sheet.columnMap['original'].tolist()
        match TTfileType:
            case 'compare':
                originalColumns.append('status')
            case 'dataBase':
                originalColumns.append('status')
                originalColumns.append('date')
                pass
            case _:
                pass

        updatedColumns = sheet.columnMap['updated'].tolist()
        match TTfileType:
            case 'compare':
                updatedColumns.append('status')
            case 'dataBase':
                updatedColumns.append('status')
                updatedColumns.append('date')
                pass
            case _:
                pass

        sheet.data = sheet.data[updatedColumns].copy()
        sheet.data.columns = originalColumns

        XLSData.setSheet(sheetName, sheet)

    # Write the data to file
    with pd.ExcelWriter(fileName, engine='xlsxwriter',) as writer:
        for sheetName in sheetList:
            # Get sheet data
            sheet = XLSData.getSheet(sheetName)

            # tempSheet=XLSCompare.sheet[SPS]
            rowOffSet = settings.getNameRow(sheetName)
            sheet.data.to_excel(writer, sheet_name=sheet.name, index=False, startrow=rowOffSet-1)

            workbook = writer.book
            worksheet = writer.sheets[sheet.name]

            match TTfileType:
                case 'compare':
                    format_new = workbook.add_format({'bg_color': '#FCF3CF'})
                    format_change = workbook.add_format({'bg_color': '#D4E6F1'})
                    format_reference = workbook.add_format({'bg_color': '#D1F2EB'})
                case 'dataBase':
                    format_new = workbook.add_format({'bg_color': '#FCF3CF'})
                    format_change = workbook.add_format({'bg_color': '#D4E6F1'})
                    format_reference = workbook.add_format({'bg_color': False})
                case _:
                    pass

            status = sheet.data['status'].tolist()
            for i, tempStatus in enumerate(status):
                if tempStatus == 'new':
                    worksheet.set_row(i+1+rowOffSet-1, cell_format=format_new)
                elif tempStatus == 'change':
                    worksheet.set_row(i+1+rowOffSet-1, cell_format=format_change)
                elif tempStatus == 'reference':
                    worksheet.set_row(i+1+rowOffSet-1, cell_format=format_reference)
                else:
                    pass
    return True

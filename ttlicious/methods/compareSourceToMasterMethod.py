from .. import classes


def compareSourceToMaster(XLSSource: classes.XLSSource, XLSMaster: classes.XLSMaster, settings: classes.XMLSettings) -> classes.XLSUpdate:
    """
    Return XLScompare after comparing sheets in source with the master
    """

    # Get the return variable
    XLSCompare = XLSSource
    XLSCompare.convertClass(classes.XLSCompare)

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

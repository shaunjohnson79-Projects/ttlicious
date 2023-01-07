from .. import classes
import os


import hydra
with hydra.initialize(config_path='../../conf', version_base=None):
    from conf.excel_settings_class import ExcelSettingsLink
    cfg: ExcelSettingsLink = hydra.compose(config_name="excel_settings")
    #from conf.sheet_settings_class import SheetSettingsLink
    #cfg2: SheetSettingsLink = hydra.compose(config_name="sheet_settings")


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

        # Get list of columns that match the compare from settings
        settingsCompareList = settings.getItemListFromName(sheetName, "compare")
        compareList = source.matchOriginalColumnsWithList(settingsCompareList)

        for SP, sourceLine in source.data.iterrows():
            # Get the search terms
            searchTerm = source.data.at[SP, cfg.columnLabels.search]

            # get the pointer to the master
            MP = master.data.index[master.data[cfg.columnLabels.search] == searchTerm].values

            if len(MP) > 1:
                # check for duplicates in master
                raise Exception("Write code here")
            elif len(MP) == 0:
                # check for data which is not in master
                source.data.at[SP, cfg.columnLabels.status] = cfg.statusLabels.new

                print("  {} New Line   : {}".format(SP, searchTerm))
                XLSCompare.modificationFound = True
                continue
            else:
                MP = int(MP)

            for compareColumn in compareList:
                tempSource = str(source.data.at[SP, compareColumn])
                tempMaster = str(master.data.at[MP, compareColumn])
                if tempSource != tempMaster:
                    source.data.at[SP, cfg.columnLabels.status] = cfg.statusLabels.change
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

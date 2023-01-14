# import pandas as pd
from datetime import datetime
from .. import utils
from .xls_sheet import XLSSheet

import hydra
with hydra.initialize(config_path='../../conf', version_base=None):
    from conf.excel_settings_class import ExcelSettingsLink
    cfg: ExcelSettingsLink = hydra.compose(config_name="excel_settings")
    #from conf.sheet_settings_class import SheetSettingsLink
    #cfg2: SheetSettingsLink = hydra.compose(config_name="sheet_settings")


class XLSFile():

    def __init__(self, xlsFileName, settings):
        self.type = None
        self.fileName = xlsFileName
        self.sheet = []

        # Load in the xls sheets
        for sheetName in settings.getSheetNames():
            tempSheet = XLSSheet(self.fileName, sheetName, settings)
            self.sheet.append(tempSheet)

    def getSheetList(self) -> list:
        return [x.getSheetName() for x in self.sheet]

    def getSheet(self, sheetName) -> XLSSheet:
        sheetList = self.getSheetList()
        index = utils.getIndices(sheetList, sheetName, 1)
        return self.sheet[index]

    def setSheet(self, sheetName, tempSheet) -> bool:
        sheetList = self.getSheetList()
        index = utils.getIndices(sheetList, sheetName, 1)
        self.sheet[index] = tempSheet
        return True

    def addColumn(self, columnName, columnValue) -> bool:
        returnFlag = False
        sheetList = self.getSheetList()
        for sheetName in sheetList:
            sheet = self.getSheet(sheetName)
            if columnName not in sheet.data.columns:
                sheet.data[columnName] = columnValue
                print('Add Column: {}'.format(columnName))
                self.setSheet(sheetName, sheet)
                returnFlag = True
        return returnFlag

    def addPrintList(self, columnName) -> bool:
        returnFlag = False
        sheetList = self.getSheetList()
        for sheetName in sheetList:
            sheet = self.getSheet(sheetName)
            if columnName not in sheet.printList:
                sheet.printList.append(columnName)
                print(f"Add To PrintList: {columnName}")
                self.setSheet(sheetName, sheet)
                returnFlag = True
        return returnFlag

    def convertClass(self, classType) -> bool:
        self.__class__ = classType
        assert isinstance(self, classType)
        self.conversion()

    def __repr__(self):
        returnString = ''
        returnString += f"XLS FILE\n"
        returnString += f"Filename: {self.fileName}\n"
        returnString += f"Type: {self.type}\n"
        for sheetName in self.getSheetList():
            returnString += f"  Sheet: {sheetName}\n"
        # import io
        # buffer = io.StringIO()
        # self.data.info(buf=buffer)
        # s = buffer.getvalue().strip()

        # returnString = ''
        # returnString = f"{returnString}Sheet Name: {self.name}\n"
        # returnString = f"{returnString}Sheet Data:\n"
        # returnString = f"{returnString}{s}\n"
        return returnString

    def setExcelFileType(self, sheetType: str):
        match sheetType:
            case cfg.sheetType.update:
                self.type = cfg.sheetType.update
                currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                self.addColumn(cfg.columnLabels.date, currentDateAndTime)
                self.addPrintList(cfg.columnLabels.date)
            case cfg.sheetType.source:
                self.type = cfg.sheetType.source
            case cfg.sheetType.master:
                self.type = cfg.sheetType.master
                self.addColumn(cfg.columnLabels.status, cfg.statusLabels.reference)
                self.addPrintList(cfg.columnLabels.status)
                currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                self.addColumn(cfg.columnLabels.date, currentDateAndTime)
                self.addPrintList(cfg.columnLabels.date)
                self.modificationFound = False
            case cfg.sheetType.compare:
                self.type = cfg.sheetType.compare
                self.addColumn(cfg.columnLabels.status, cfg.statusLabels.current)
                self.addPrintList(cfg.columnLabels.status)
                self.modificationFound = False
            case cfg.sheetType.sap:
                pass
            case _:
                raise exception("Unknown sheetType")
        return


class XLSUpdate(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = cfg.statusLabels.update
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(cfg.columnLabels.date, currentDateAndTime)
        self.addPrintList(cfg.columnLabels.date)


class XLSSource(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = cfg.sheetType.source


class XLSCompare(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = cfg.sheetType.compare
        self.addColumn(cfg.columnLabels.status, cfg.statusLabels.current)
        self.addPrintList(cfg.columnLabels.status)
        self.modificationFound = False


class XLSMaster(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = cfg.sheetType.master
        self.addColumn(cfg.columnLabels.status, cfg.statusLabels.reference)
        self.addPrintList(cfg.columnLabels.status)
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(cfg.columnLabels.date, currentDateAndTime)
        self.addPrintList(cfg.columnLabels.date)
        self.modificationFound = False


def debugXLSFile():
    from .xml_settings import XMLSettings
    settings = XMLSettings('settingsQuick.xml')
    settings = XMLSettings('settings.xml')

    fileName = '20210323 Hinterkipper_de en_finala.xlsx'
    source = XLSSource(fileName, settings)
    print(source.getSheetList())
    master = XLSMaster(fileName, settings)
    sheetList = master.getSheetList()
    for sheetName in sheetList:
        tempSheet = master.getSheet(sheetName)
        tempSheet.replaceDuplicateColumnsWithOriginalColumns()
        print(tempSheet)
        # source.setSheet(sheetName, tempSheet)

    return


if __name__ == '__main__':
    debugXLSFile()

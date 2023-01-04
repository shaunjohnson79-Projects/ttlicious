#import pandas as pd
from datetime import datetime
from .. import shaunMethods
from .XLSSheetClass import XLSSheet
from .classSettingsClass import ClassSettings

classSettings = ClassSettings()


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
        index = shaunMethods.getIndices(sheetList, sheetName, 1)
        return self.sheet[index]

    def setSheet(self, sheetName, tempSheet) -> bool:
        sheetList = self.getSheetList()
        index = shaunMethods.getIndices(sheetList, sheetName, 1)
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


class XLSUpdate(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Update'
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(classSettings.columnNamesDictionary["date"], currentDateAndTime)
        self.addPrintList(classSettings.columnNamesDictionary["date"])


class XLSSource(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Source'
        # self.addColumn(classSettings.columnNamesDictionary["status"], 'current')


class XLSCompare(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Compare'
        self.addColumn(classSettings.columnNamesDictionary["status"], 'current')
        self.addPrintList(classSettings.columnNamesDictionary["status"])
        self.modificationFound = False


class XLSMaster(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Master'
        self.addColumn('status', 'reference')
        self.addPrintList(classSettings.columnNamesDictionary["status"])
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(classSettings.columnNamesDictionary["date"], currentDateAndTime)
        self.addPrintList(classSettings.columnNamesDictionary["date"])
        self.modificationFound = False


def debugXLSFile():
    from .XMLSettingsClass import XMLSettings
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
        #source.setSheet(sheetName, tempSheet)

    return


if __name__ == '__main__':
    debugXLSFile()

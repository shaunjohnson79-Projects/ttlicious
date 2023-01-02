import pandas as pd
import shaunMethods.shaunScripts as shaunScripts
# import os.path
import os
from datetime import datetime
import errno
import OBL


# Settings for the objects
columnNamesDictionary = {
    "date": "date",
    "status": "status",
    "search": "searchIndex",
}


class XLSSheet():
    def __init__(self, fileName, sheetName, settings):
        # Define the variables
        self.name = str
        self.data = pd
        self.columnMap = pd
        self.rowOffSet = int
        self.printList = list

        # read in the data
        self.name = sheetName
        tempColumns = self._readFromFileColumns(fileName, sheetName, settings)
        self.data = self._readFromFileData(fileName, sheetName, settings)

        self.columnMap = self._createDuplicateMap(tempColumns)
        self._fixColumnNamesOnImport()

        # Get the print list
        self.printList = self.columnMap['updated'].tolist()

        # Create search index
        self._createSearchIndex(sheetName, settings)

    def replaceDuplicateColumnsWithOriginalColumns(self) -> None:
        updatedColumns = self.columnMap['updated'].tolist()
        originalColumns = self.columnMap['original'].tolist()

        columnlist = self.data.columns.tolist()
        for i, tempColumn in enumerate(columnlist):
            tp = shaunScripts.getIndices(updatedColumns, tempColumn)
            if isinstance(tp, int) == 1:
                columnlist[i] = originalColumns[tp]
        self.data.columns = columnlist

    def getCompareList(self, sheet, settings) -> list:
        """Create list of updated row names"""
        compareList = settings.getItemListFromName(sheet, 'compare')
        columnMap = self.columnMap
        reducedList = columnMap[columnMap['original'].isin(compareList)]
        compareList = list(reducedList['updated'])
        return compareList

    def _readFromFileColumns(self, fileName, sheet, settings) -> list:
        """Read sheet columns names"""
        self._checkFile(fileName)

        # read the columns
        headerRow = settings.getNameRow(sheet)-1
        columns = pd.read_excel(fileName, sheet_name=sheet, header=None, nrows=headerRow+1).values[headerRow].tolist()
        return columns

    def _readFromFileData(self, fileName, sheet, settings) -> pd:
        """Read sheet columns data"""
        self._checkFile(fileName)

        # read the data
        headerRow = settings.getNameRow(sheet)-1
        data = pd.read_excel(fileName, sheet_name=sheet, header=headerRow)

        # Print to screen
        print("Read {} : {}".format(fileName, sheet))

        return data

    def _checkFile(self, fileName) -> bool:
        # Check if file exists
        if os.path.isfile(fileName):
            return True
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), fileName)

    def _fixColumnNamesOnImport(self):
        """Fix the column names so there are no duplicates when loading the data"""

        # apply column names
        self.data.columns = list(self.columnMap["updated"])

    def _createSearchIndex(self, sheet, settings):
        """update the index according to the xml settings"""
        # create the search index
        partNumberList = settings.getItemListFromName(sheet, 'partNumber')
        self.data[columnNamesDictionary["search"]] = self.data[partNumberList].agg('-'.join, axis=1)
        # self.data=self.data.set_index(tempString)

    def _createDuplicateMap(self, columns) -> pd:
        """Create pandas to link column names"""
        returnColumns = pd.DataFrame(str, index=range(len(columns)), columns=['original', 'updated'])

        for i, column in enumerate(columns):
            returnColumns.at[i, 'original'] = column
            if columns.count(column) > 1:
                if i == 0:
                    raise Exception("Write code here")
                tempString = "{} {}".format(columns[i-1], columns[i])
                returnColumns.at[i, 'updated'] = tempString
            else:
                returnColumns.at[i, 'updated'] = column
        return returnColumns

    def getSheetName(self) -> str:
        return self.name

    def getColumnMap(self) -> pd:
        return self.columnMap

    def __repr__(self):
        import io
        buffer = io.StringIO()
        self.data.info(buf=buffer)
        s = buffer.getvalue().strip()

        returnString = ''
        returnString = f"{returnString}Sheet Name: {self.name}\n"
        returnString = f"{returnString}Sheet Data:\n"
        returnString = f"{returnString}{s}\n"
        return returnString


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
        index = shaunScripts.getIndices(sheetList, sheetName, 1)
        return self.sheet[index]

    def setSheet(self, sheetName, tempSheet) -> bool:
        sheetList = self.getSheetList()
        index = shaunScripts.getIndices(sheetList, sheetName, 1)
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
        self.addColumn(columnNamesDictionary["date"], currentDateAndTime)
        self.addPrintList(columnNamesDictionary["date"])


class XLSSource(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Source'
        # self.addColumn(columnNamesDictionary["status"], 'current')


class XLSCompare(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Compare'
        self.addColumn(columnNamesDictionary["status"], 'current')
        self.addPrintList(columnNamesDictionary["status"])
        self.modificationFound = False


class XLSMaster(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.conversion()

    def conversion(self) -> None:
        self.type = 'Master'
        self.addColumn('status', 'reference')
        self.addPrintList(columnNamesDictionary["status"])
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(columnNamesDictionary["date"], currentDateAndTime)
        self.addPrintList(columnNamesDictionary["date"])
        self.modificationFound = False


def debugXLS():
    settings = settings.
    .('settings.xml')
    settings = settings('settingsQuick.xml')
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
    # debugXML()
    debugXLS()

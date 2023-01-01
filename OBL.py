import pandas as pd
import shaunScripts
# import os.path
import os
from datetime import datetime
from lxml import etree
import errno

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


class XMLSettings(object):
    def __init__(self, xmlFileName) -> None:

        self.doc = etree.parse(xmlFileName)
        self.root = self.doc.getroot()

    def __repr__(self) -> str:
        etree.indent(self.doc, space="  ")
        returnString = etree.tostring(self.doc, pretty_print=True).decode()
        return returnString

    def __getSheetBranch(self, tree, sheetName) -> object:
        searchString = ".sheet/[name='{}']".format(sheetName)
        branch = tree.findall(searchString)
        if (len(branch) == 1):
            branch = branch[0]
        else:
            print('not able to find value')
            return
        return branch

    def __getColumnsBranch(self, tree, sheetName) -> object:
        branch = self.__getSheetBranch(tree, sheetName)
        branch = branch.find('columns')
        return branch

    def __getItemList(self, tree) -> list:
        itemList = []
        for tempItem in tree.iter('item'):
            itemList.append(tempItem.text)
        return itemList

    def getSheetNames(self) -> list:
        sheetNames = []
        for sheet in self.root.findall('sheet'):
            name = sheet.find('name').text
            sheetNames.append(name)
        return sheetNames

    def getNameRow(self, sheetName) -> int:
        rowNumber = None
        tempSheet = self.__getSheetBranch(self.root, sheetName)
        rowNumber = int(tempSheet.find('nameRow').text)
        return rowNumber

    def getPartNumberString(self, sheetName) -> list:
        tempColumn = self.__getColumnsBranch(self.root, sheetName)
        partNumber = tempColumn.find('partNumber')
        partNumberString = self.__getItemList(partNumber)
        return partNumberString

    def getItemListFromName(self, sheetName, itemName) -> list:
        tempColumn = self.__getColumnsBranch(self.root, sheetName)
        partNumber = tempColumn.find(itemName)
        partNumberString = self.__getItemList(partNumber)
        return partNumberString


def debugXML():
    fileName = 'settings.xml'
    settings = XMLSettings("settings.xml")
    sheetNames = settings.getSheetNames()
    print(sheetNames)
    for tempSheetName in sheetNames:
        print(tempSheetName)
        rowNumber = settings.getNameRow(tempSheetName)
        print("rowNumber={}".format(rowNumber))
        # partNumberString=settings.getPartNumberString(tempSheetName)
        # print(partNumberString)
        partNumberList = settings.getItemListFromName(
            tempSheetName, 'partNumber')
        print(partNumberList)

        print(settings)

        return


def debugXLS():
    settings = XMLSettings('settings.xml')
    settings = XMLSettings('settingsQuick.xml')
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

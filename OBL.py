import pandas as pd
import shaunScripts
import os.path
from datetime import datetime
from lxml import etree

columnNamesDictionary = {
    "date": "date",
    "status": "status",
    "search": "searchIndex",
}

print(columnNamesDictionary["status"])
# _columnName_date = "date"
# columnNamesDictionary["status"] = "status"
# _columnName_search = "searchIndex"


class XLSSheet():
    def __init__(self, fileName, sheet, settings) -> None:
        # Define the variables
        self.name = str
        self.data = pd
        self.columns = list
        self.columnMap = pd
        self.rowOffSet = int

        # Do initalisation steps
        self._addSheetName(sheet)
        self._readFromFile(fileName, sheet, settings)
        self._fixColumnNames()
        self._createSearchIndex(sheet, settings)

        # self.getCompareList(sheet,settings)

    def getCompareList(self, sheet, settings) -> list:
        """Create list of updated row names"""
        compareList = settings.getItemListFromName(sheet, 'compare')
        columnMap = self.columnMap
        reducedList = columnMap[columnMap['original'].isin(compareList)]
        compareList = list(reducedList['updated'])
        return compareList

    def _addSheetName(self, sheet):
        """Add the sheet name"""
        self.name = sheet

    def _readFromFile(self, fileName, sheet, settings):
        """Read sheet from XLS file"""
        # Check if file exists
        if os.path.isfile(fileName):
            print(f"File exist: {fileName}")
        else:
            tempText = f"File does not exist: {fileName}"
            print(tempText)
            raise Exception(print(tempText))

        # read the columns
        headerRow = settings.getNameRow(sheet)-1
        self.columns = pd.read_excel(fileName, sheet_name=sheet, header=None, nrows=headerRow+1).values[headerRow]
        self.columns = self.columns.tolist()

        # read the data
        self.data = pd.read_excel(fileName, sheet_name=sheet, header=headerRow)

        # Print to screen
        print("Read {} : {}".format(fileName, sheet))

    def _fixColumnNames(self):
        """Fix the column names so there are no duplicates"""
        # create unique list for column names
        self.columnMap = self.__fixDuplicateColumnNames(self.columns)

        # apply column names
        #self.data.columns = list(self.columnMap.keys())
        self.data.columns = list(self.columnMap["updated"])

    def _createSearchIndex(self, sheet, settings):
        """update the index according to the xml settings"""
        # create the search index
        partNumberList = settings.getItemListFromName(sheet, 'partNumber')
        self.data[columnNamesDictionary["search"]] = self.data[partNumberList].agg('-'.join, axis=1)
        # self.data=self.data.set_index(tempString)

    def __fixDuplicateColumnNames(self, columns) -> dict:
        """Create pandas to link column names"""
        returnColumns = pd.DataFrame(str, index=range(
            len(columns)), columns=['original', 'updated'])

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

    def getSheetData(self) -> pd:
        return self.data

    def setSheetData(self, data) -> bool:
        self.data = data
        return True

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
    _columnName_date = "date"
    _columnName_status = "status"
    _columnName_search = "searchIndex"

    def __init__(self, xlsFileName, settings) -> None:
        self.fileName = xlsFileName
        self.sheet = []

        # Load in the xls sheets
        for sheet in settings.getSheetNames():
            tempSheet = XLSSheet(self.fileName, sheet, settings)
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
        for i, sheet in enumerate(self.sheet):
            if columnName not in sheet.data.columns:
                sheet.data[columnName] = columnValue
                print('Add Column: {}'.format(columnName))
                self.sheet[i] = sheet
                returnFlag = True


class XLSUpdate(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.type = 'Update'
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(columnNamesDictionary["date"], currentDateAndTime)


class XLSSource(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.type = 'Source'
        self.addColumn(columnNamesDictionary["status"], 'current')


class XLSMaster(XLSFile):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.type = 'Master'
        self.addColumn('status', 'reference')
        currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        self.addColumn(columnNamesDictionary["date"], currentDateAndTime)


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
    settings = objectXMLSettings.parseXML('settings.xml')
    fileName = '20210323 Hinterkipper_de en_finala.xlsx'
    source = XLSSource(fileName, settings)
    print(source.getSheetList())
    # master=readXLSMaster(fileName,settings)
    sheetList = source.getSheetList()
    for sheetName in sheetList:
        tempSheet = source.getSheet(sheetName)
        print(tempSheet)
        source.setSheet(sheetName, tempSheet)

    return


if __name__ == '__main__':
    debugXML()
    # debugXLS()

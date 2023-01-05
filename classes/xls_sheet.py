import pandas as pd
import os
from datetime import datetime
import errno
from .. import utils
from .class_settings import ClassSettings


classSettings = ClassSettings()


class XLSSheet():
    def __init__(self, fileName, sheetName: str, settings):
        # Define the variables
        self.name = str
        self.data = pd
        self.rowOffSet = int
        self.printList = list

        # Define the sheetName
        self.name = sheetName

        # Get the columns from XLS
        columnsOriginal = self._readFromFileColumns(fileName, sheetName, settings)

        # get the data from XLS
        self.data = self._readFromFileData(fileName, sheetName, settings)

        # Get the columnMap
        self.columnMap = ColumnMapBlah(columnsOriginal)

        # Fix the column names in panda data
        self.listToDataColumns(self.columnMap.updated)

        # Define the print list
        self.printList = self.dataColumnsToList()

        # Create search index
        self._createSearchIndex(sheetName, settings)

        return

    def dataColumnsToList(self) -> list:
        tempList = self.data.columns.tolist()
        return tempList

    def listToDataColumns(self, tempList) -> None:
        self.data.columns = tempList
        return

    def getSheetName(self) -> str:
        return self.name

    def matchOriginalColumnsWithList(self, referenceList):
        returnList = list()
        updatedList = self.dataColumnsToList()
        for i, listValueUpdated in enumerate(updatedList):
            listValueOriginal = self.columnMap.convertToOriginal(listValueUpdated)
            if listValueOriginal[0] in referenceList:
                returnList.append(listValueUpdated)
        return returnList

    def _readFromFileColumns(self, fileName, sheetName, settings) -> list:
        """Read sheet columns names"""
        self._checkFile(fileName)

        # read the columns
        headerRow = settings.getNameRow(sheetName)-1
        columns = pd.read_excel(fileName, sheet_name=sheetName, header=None, nrows=headerRow+1).values[headerRow].tolist()
        return columns

    def _readFromFileData(self, fileName, sheetName, settings) -> pd:
        """Read sheet columns data"""
        self._checkFile(fileName)

        # Print to screen
        print("Read {} : {}".format(fileName, sheetName))

        # read the data
        headerRow = settings.getNameRow(sheetName)-1
        data = pd.read_excel(fileName, sheet_name=sheetName, header=headerRow)
        return data

    def _checkFile(self, fileName) -> bool:
        # Check if file exists
        if os.path.isfile(fileName):
            return True
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), fileName)

    def _createSearchIndex(self, sheet, settings):
        """update the index according to the xml settings"""
        # Get the part number list
        partNumberList = settings.getItemListFromName(sheet, 'partNumber')
        partNumberList = self.columnMap.convertToUpdated(partNumberList)

        # Add columns with for search
        self.data[classSettings.columnNamesDictionary["search"]] = self.data[partNumberList].agg('-'.join, axis=1)

    def __repr__(self):
        import io
        buffer = io.StringIO()
        self.data.info(buf=buffer)
        s = buffer.getvalue().strip()

        returnString = ''
        returnString += f"Sheet Name: {self.name}\n"
        returnString += f"Sheet Data:\n"
        returnString += f"{s}\n"
        return returnString


class ColumnMapBlah():
    def __init__(self, columnList) -> None:
        self._original = list
        self._updated = list

        self._original, self._updated = self._createDuplicateMap2(columnList)

    def _createDuplicateMap2(self, inputList: list) -> tuple[list, list]:
        original = list()
        updated = list()

        for i, listValue in enumerate(inputList):
            if inputList.count(listValue) > 1:
                if i == 0:
                    raise Exception("Write code here")
                tempString = "{} {}".format(inputList[i-1], inputList[i])
                original.append(listValue)
                updated.append(tempString)
            else:
                original.append(listValue)
                updated.append(listValue)

        return original, updated

    @property
    def original(self):
        pass

    @original.getter
    def original(self) -> float:
        return self._original

    @property
    def updated(self):
        pass

    @original.getter
    def updated(self) -> float:
        return self._updated

    def convertToOriginal(self, tempList):
        if isinstance(tempList, str):
            tempList = [tempList]
        for i, listValue in enumerate(tempList):
            tp = utils.getIndices(self.updated, listValue)
            if isinstance(tp, int) == 1:
                tempList[i] = self.original[tp]
        return tempList

    def convertToUpdated(self, tempList):
        if isinstance(tempList, str):
            tempList = [tempList]
        for i, listValue in enumerate(tempList):
            tp = utils.getIndices(self.original, listValue)
            if isinstance(tp, int) == 1:
                tempList[i] = self.updated[tp]
        return tempList


def debugXLSSheet():
    from .xml_settings import XMLSettings
    settings = XMLSettings('settingsQuick.xml')
    #settings = XMLSettings('settings.xml')

    from .xls_file import XLSSource, XLSMaster
    fileName = '20210323 Hinterkipper_de en_finala.xlsx'
    source = XLSSource(fileName, settings)
    print(source.getSheetList())
    master = XLSMaster(fileName, settings)
    sheetList = master.getSheetList()
    for sheetName in sheetList:
        tempSheet = master.getSheet(sheetName)
        print(tempSheet)
        #source.setSheet(sheetName, tempSheet)

    return


if __name__ == '__main__':
    debugXLSSheet()

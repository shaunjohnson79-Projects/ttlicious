from lxml import etree
from .class_settings import ClassSettings

classSettings = ClassSettings()


class XMLSettings():
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


if __name__ == '__main__':
    debugXML()

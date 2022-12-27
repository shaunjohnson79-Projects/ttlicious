import pandas as pd
from readXMLData import parseXML




class readXLSFile(object):
    def __init__(self,xlsFileName,settings):
        self.fileName=xlsFileName
        self.settings=settings
        self.sheet={}
        
        self=self.__loadSheets()
        
    
    def __loadSheets(self):
        sheetList=self.settings.getSheetNames()
        print(sheetList)
        
        for sheet in sheetList:
            tempSheet=readXLSSheet(self.fileName,sheet,self.settings)
            
class readXLSSheet(object):
    def __init__(self,fileName,sheet,settings):   
        #read the sheet
        self.name=sheet

        #read the columns
        fileToRead=fileName
        sheetToRead=sheet
        headerRow=settings.getNameRow(sheet)-1 
        self.columns=pd.read_excel(fileToRead, sheet_name=sheetToRead, header=None,nrows=headerRow+1).values[headerRow]
        
        #read the data
        self.data=pd.read_excel(fileToRead, sheet_name=sheetToRead, header=headerRow)
        
        #Print to screen
        print("Read {} : {}".format(fileToRead,sheetToRead))

    def __fixDuplicateColumnNames():
        """Create unique column names"""
        

        
def main():
    settings = parseXML('settings.xml')
    fileName='20210323 Hinterkipper_de en_finala.xlsx'
    source=readXLSFile(fileName,settings)

    return

if __name__ == '__main__':
    main()
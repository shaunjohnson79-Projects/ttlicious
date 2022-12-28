import pandas as pd
import numpy as np
from readXMLData import parseXML

class readXLSFile():
    def __init__(self,xlsFileName,settings):
        self.fileName=xlsFileName
        self.sheet=[]
        
        # Load in the xls sheets
        for sheet in settings.getSheetNames():
            tempSheet=readXLSSheet(self.fileName,sheet,settings)
            self.sheet.append(tempSheet)
        
    def findColumnsToCompare(self,sheet,settings):
        pass    
    
    def getSheetList(self):
        return [x.getSheetName() for x in self.sheet]

    def lenSheets(self):
        return len(self.sheet)

class readXLSSource(readXLSFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type='Source'
        
        self.__addStatusColumn()
        
    def __addStatusColumn(self):
        columnName='status'
        columnValue='current'
        for i, sheet in enumerate(self.sheet):
            if columnName not in sheet.data.columns:
                sheet.data[columnName]=columnValue
                print('Add Column: {}'.format(columnName))
                self.sheet[i]=sheet
    
class readXLSMaster(readXLSFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type='Master'
        

                
            



          
class readXLSSheet():
    def __init__(self,fileName,sheet,settings):   
        # Define the variables
        self.name=str
        self.data=pd
        self.columns=list
        self.columnMap=pd
        
        # Do initalisation steps
        self.__addSheetName(sheet)
        self.__readFromFile(fileName,sheet,settings)
        self.__fixColumnNames()
        self.__createSearchIndex(sheet,settings)
        
        #self.getCompareList(sheet,settings)
        
    def getCompareList(self,sheet,settings) -> list:
        """Create list of updated row names"""
        compareList=settings.getItemListFromName(sheet,'compare')
        columnMap=self.columnMap
        reducedList=columnMap[columnMap['original'].isin(compareList)]
        compareList=list(reducedList['updated'])
        return compareList
    
    def __addSheetName(self,sheet):
        """Add the sheet name"""
        self.name=sheet
    
    def __readFromFile(self,fileName,sheet,settings):
        """Read XLS from file"""
    
        #read the columns
        headerRow=settings.getNameRow(sheet)-1 
        self.columns=pd.read_excel(fileName, sheet_name=sheet, header=None,nrows=headerRow+1).values[headerRow]
        self.columns=self.columns.tolist()
        
        #read the data
        self.data=pd.read_excel(fileName, sheet_name=sheet, header=headerRow)
        
        #Print to screen
        print("Read {} : {}".format(fileName,sheet))
          
    def __fixColumnNames(self):
        """Fix the column names so there are no duplicates"""
        #create unique list for column names
        self.columnMap=self.__fixDuplicateColumnNames(self.columns)
        
        #apply column names 
        #self.data.columns = list(self.columnMap.keys())
        self.data.columns=list(self.columnMap["updated"])
    
    def __createSearchIndex(self,sheet,settings):
        """update the index according to the xml settings"""
        #create the search index
        tempString='searchIndex'
        partNumberList=settings.getItemListFromName(sheet,'partNumber') 
        self.data[tempString] = self.data[partNumberList].agg('-'.join, axis=1)
        self.data=self.data.set_index(tempString)

    def __fixDuplicateColumnNames(self,columns) -> dict:
        """Create pandas to link column names"""
        returnColumns = pd.DataFrame(str, index=range(len(columns)), columns=['original','updated'])
        
        for i, column in enumerate(columns):
            returnColumns.at[i,'original']=column
            if columns.count(column)>1:
                if i == 0:
                    raise Exception("Write code here")
                tempString="{} {}".format(columns[i-1],columns[i])
                returnColumns.at[i, 'updated']=tempString
            else:
                returnColumns.at[i, 'updated']=column
        return returnColumns
    
    def getSheetName(self):
        return self.name
    
    def getData(self):
        return self.data
    
    def getColumnMap(self):
        return self.columnMap
    
    
            

        
        
        

        
def main():
    settings = parseXML('settings.xml')
    fileName='20210323 Hinterkipper_de en_finala.xlsx'
    source=readXLSSource(fileName,settings)
    print(source.getSheetList())
    #master=readXLSMaster(fileName,settings)
    return

if __name__ == '__main__':
    main()
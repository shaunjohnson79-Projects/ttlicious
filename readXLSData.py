import pandas as pd
from readXMLData import parseXML



class readXLSFile(object):
    def __init__(self,xlsFileName,settings):
        self.fileName=xlsFileName
        self.settings=settings
        self.sheet=[]
        
        
        for sheet in self.settings.getSheetNames():
            tempSheet=readXLSSheet(self.fileName,sheet,self.settings)
            self.sheet.append(tempSheet)
            
            
class readXLSSheet(object):
    def __init__(self,fileName,sheet,settings):   
        #define the variables
        self.name=sheet
        self.data=pd
        self.columns=list
        
        self.__readFromFile(fileName,sheet,settings)
        self.__fixColumnNames()
        self.__createSearchIndex(sheet,settings)
    
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
        self.data.columns = list(self.columnMap.keys())
    
    def __createSearchIndex(self,sheet,settings):
        """update the index according to the xml settings"""
        #create the search index
        tempString='searchIndex'
        partNumberList=settings.getItemListFromName(sheet,'partNumber') 
        self.data[tempString] = self.data[partNumberList].agg('-'.join, axis=1)
        self.data=self.data.set_index(tempString)

    def __fixDuplicateColumnNames(self,columns) -> dict:
        """Create dict with unique column names"""
        returnColumns={}
        
        for i, column in enumerate(columns):
            if columns.count(column)>1:
                if i == 0:
                    raise Exception("Write code here")
                tempString="{} {}".format(columns[i-1],columns[i])
                returnColumns.update({tempString:column})
            else:
                returnColumns.update({column:column})
        return returnColumns
            

        
        
        

        
def main():
    settings = parseXML('settings.xml')
    fileName='20210323 Hinterkipper_de en_finala.xlsx'
    source=readXLSFile(fileName,settings)

    return

if __name__ == '__main__':
    main()
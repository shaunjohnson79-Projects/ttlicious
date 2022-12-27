from readXMLData import parseXML
import pandas as pd
import time


def main():
    print("Program Start")
    #define the filenames
    fileInfo={}
    fileInfo.update({'XML':'settingsQuick.xml'})
    fileInfo.update({'XLS_source':'20210323 Hinterkipper_de en_finala.xlsx'})
    fileInfo.update({'XLS_master':'20210323 Hinterkipper_de en_final_master.xlsm'})

    # Read in the settings
    settings = parseXML(fileInfo['XML'])
    #print(settings)
    
    
    
    # Read the source XLS
    XLSSource={}
    for sheet in settings.getSheetNames():
        #read the sheet
        fileToRead=fileInfo['XLS_source']
        sheetToRead=sheet
        headerRow=settings.getNameRow(sheet)-1
        tempSheet=pd.read_excel(fileToRead, sheet_name=sheetToRead, header=headerRow)
        
        #Add the search column
        partNumberList=settings.getItemListFromName(sheet,'partNumber') 
        tempSheet['search'] = tempSheet[partNumberList].agg('-'.join, axis=1)

        #Add to dictionary
        XLSSource.update({sheet:tempSheet})
        print("Read {} : {}".format(fileToRead,sheetToRead))
        
    # Read the master XLS
    XLSMaster={}
    for sheet in settings.getSheetNames():
        #read the sheet
        fileToRead=fileInfo['XLS_master']
        sheetToRead=sheet
        headerRow=settings.getNameRow(sheet)-1
        
        #cols = pd.read_excel(fileToRead,sheet_name=sheetToRead, header=None,nrows=1).values[headerRow] # read first row
        #tempSheet = pd.read_excel(fileToRead,sheet_name=sheetToRead, header=None, skiprows=headerRow+1) # skip 1 row
        #tempSheet.columns = cols
        tempSheet=pd.read_excel(fileToRead, sheet_name=sheetToRead, header=headerRow)
        
        #Add the search column
        partNumberList=settings.getItemListFromName(sheet,'partNumber') 
        tempSheet['search'] = tempSheet[partNumberList].agg('-'.join, axis=1)

        #Add the index
        tempSheet=tempSheet.set_index('search')

        #Add to dictionary
        XLSMaster.update({sheet:tempSheet})
        print("Read {} : {}".format(fileToRead,sheetToRead))
        


    # Look for code pairs
    for sheet in settings.getSheetNames():
        
        
        # get the data
        DFSource=XLSSource[sheet]
        DFSource['status']='current'
        DFMaster=XLSMaster[sheet]
        print(type(DFMaster))
        print(DFMaster.info)
        print(DFSource.info)
        
        #get the columns to compare
        compareList=settings.getItemListFromName(sheet,'compare') 
        bb=DFSource.columns.get_indexer(compareList)
        DFMaster.columns.get_indexer(compareList)
        
        aa=1
        #for compareColumn in compareList:        
        
        
        
        #get the columns to compare
        compareList=settings.getItemListFromName(sheet,'compare') 
        for compareColumn in compareList:
            if compareColumn not in DFSource.columns or compareColumn not in DFMaster.columns:
                compareList.remove(compareColumn)
                print("Remove the following coloum from compare list\n\t{}".format(compareColumn))
                time.sleep(5)
                
                
                
        
        
        #for SP, source in DFSource.iterrows():
        print(DFSource)
        for SP, source in DFSource.iterrows():
            # Get source and master
            if SP not in DFMaster.index:
                DFSource.at[SP,'status']='new'
                continue
            
            for compareColumn in compareList:
                tempSource=str(DFSource.at[SP,compareColumn])
                tempMaster=str(DFMaster.at[SP,compareColumn])
                if tempSource != tempMaster :
                    DFSource.at[SP,'status']='change'
                    
                
                
                
            #check the rows for 
            #print(master.info)
            quit()
            
            
            
            
            

                
            
            #sourceRow = source
            #print(sourceRow)

        
        
        
    

if __name__ == "__main__":
    main()
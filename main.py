from readXMLData import parseXML
from readXLSData import readXLSSource
from readXLSData import readXLSMaster
import pandas as pd
import time


def main() -> None:
    print("Program Start")
    #define the filenames
    fileInfo={}
    fileInfo.update({'XML':'settings.xml'})
    fileInfo.update({'XML':'settingsQuick.xml'})
    fileInfo.update({'XLS_source':'20210323 Hinterkipper_de en_finala.xlsx'})
    fileInfo.update({'XLS_master':'20210323 Hinterkipper_de en_final_master.xlsm'})

    # Read in the settings
    settings = parseXML(fileInfo['XML'])
    #print(settings)
    
    # Read in the XLS
    XLSSource=readXLSSource(fileInfo['XLS_source'],settings)
    XLSMaster=readXLSMaster(fileInfo['XLS_master'],settings)
    
    for SPS, sourceSheet in enumerate(XLSSource.sheet):
        
        # Get the sheets manually
        source=XLSSource.sheet[SPS]
        master=XLSMaster.sheet[SPS]
        
        #get list of columns to use for compare
        compareList=sourceSheet.getCompareList(sourceSheet.name,settings)
        indexS=source.data.columns.get_indexer(compareList)
        indexM=master.data.columns.get_indexer(compareList)
        print(compareList)
        print(indexM)
        print(indexS)    
        
        for SP, sourceLine in source.data.iterrows():
            # Get source and master
            if SP not in master.data.index:
                source.data.at[SP,'status']='new'
                print('new line')
                continue  
            
            for compareColumn in compareList:
                tempSource=str(source.data.at[SP,compareColumn])
                tempMaster=str(master.data.at[SP,compareColumn])
                if tempSource != tempMaster :
                    source.data.at[SP,'status']='change' 
                    print('change')
        
        
        
        
        #XLSSource.sheet[SPS]=sourceSheet
    
    # Create list of columns to compare
    #aa=XLSSource.sheet[0].data
    #print(aa)
    
    
def blah(): 
    
    
        


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
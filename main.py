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
            #get the search terms
            searchTerm=source.data.at[SP,'searchIndex']
            MS=master.data.index[master.data['searchIndex']==searchTerm].values
            if len(MS) > 1:
                raise Exception("Write code here")
            MS=int(MS)
            
            print(len(bb))
            print(bb)
            
        
    def bb():    
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
                    rowToInsert=master.data.loc[SP]

                    indexList=source.data.index.tolist()
                    aa=indexList.index(str(SP))
                    aa=aa+0.5
                    
                    source.data.loc[aa]=rowToInsert
                    
                    #print(indexList)
                    print(aa)
                    
                    #print(source.data)
                    bb=1
                    
    
                    
#                      df.loc[-1] = [2, 3, 4]  # adding a row
#  df.index = df.index + 1  # shifting index
#  df = df.sort_index()  # sorting by index
        


if __name__ == "__main__":
    main()
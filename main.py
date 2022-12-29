from readXMLData import parseXML 
from readXLSData import readXLSSource, readXLSMaster, readXLSSheet
#import xlsxwriter
import pandas as pd





def main() -> None:
    print(f"Program Start")
    #define the filenames
    fileInfo={}
    fileInfo.update({'XML':'settings.xml'})
    #fileInfo.update({'XML':'settingsQuick.xml'})
    fileInfo.update({'XLS_source':'20210323 Hinterkipper_de en_finala.xlsx'})
    fileInfo.update({'XLS_master':'20210323 Hinterkipper_de en_final_master.xlsm'})

    # Read in the settings
    settings = parseXML(fileInfo['XML'])
    #print(settings)
    
    # Read in the XLS
    XLSSource=readXLSSource(fileInfo['XLS_source'],settings)
    XLSMaster=readXLSMaster(fileInfo['XLS_master'],settings)
    
    #get the compared XLS
    XLSCompare=compareSourceToMaster(XLSSource,XLSMaster,settings) 
    assert isinstance(XLSCompare, readXLSSource)
    
    writeToXLS(XLSCompare)
    
    
def writeToXLS(XLSData) -> bool:   
    """
    Write XLS data to a file
    """
    
    sheetList=XLSData.getSheetList()
    for sheetName in sheetList:
        
        # Get sheet data
        sheet=XLSData.getSheet(sheetName)
        assert isinstance(sheet, readXLSSheet)
        
        originalColumns=sheet.columnMap['original'].tolist()
        originalColumns.append('status')
        
        
        updatedColumns=sheet.columnMap['updated'].tolist()
        updatedColumns.append('status')

        sheet.data = sheet.data[updatedColumns].copy()
        sheet.data.columns=originalColumns
        
        XLSData.setSheet(sheetName,sheet)
    
    with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
        for sheetName in sheetList:
            # Get sheet data
            sheet=XLSData.getSheet(sheetName)
            assert isinstance(sheet, readXLSSheet)

            #tempSheet=XLSCompare.sheet[SPS]    
            print(sheet.name)
            sheet.data.to_excel(writer, sheet_name=sheet.name,index=False) 

            workbook  = writer.book
            worksheet = writer.sheets[sheet.name]
            
            format_new = workbook.add_format({'bg_color': '#FCF3CF'})
            format_change = workbook.add_format({'bg_color': '#D4E6F1'})
            format_reference = workbook.add_format({'bg_color': '#D1F2EB'})
            
            status=sheet.data['status'].tolist()
            for i, tempStatus in enumerate(status):
                if tempStatus=='new':
                    worksheet.set_row(i+1, cell_format=format_new)
                elif tempStatus=='change':
                    worksheet.set_row(i+1, cell_format=format_change)
                elif tempStatus=='reference':
                    worksheet.set_row(i+1, cell_format=format_reference)
                else:
                    pass
    return True                  
    
def compareSourceToMaster(XLSSource,XLSMaster,settings) -> object:
    """
    Return XLScompare after comparing sheets in source with the master
    """
    
    # Define the return variable
    XLSreturn=XLSSource
    
    sheetList=XLSSource.getSheetList()
    for sheetName in sheetList:
        
        # Get the sheets manually
        source=XLSSource.getSheet(sheetName)
        master=XLSMaster.getSheet(sheetName) 
        assert isinstance(source, readXLSSheet) 
        assert isinstance(master, readXLSSheet)  
        
        # Display to screen
        print("Compare Sheet: {}".format(source.name))
        
        #get list of columns to use for compare
        compareList=source.getCompareList(source.name,settings)
        indexS=source.data.columns.get_indexer(compareList)
        indexM=master.data.columns.get_indexer(compareList)
        # print(compareList)
        # print(indexM)
        # print(indexS)   
         
        for SP, sourceLine in source.data.iterrows():
            # Get the search terms
            searchTerm=source.data.at[SP,'searchIndex']
            MP=master.data.index[master.data['searchIndex']==searchTerm].values
            
            if len(MP) > 1:
                #check for duplicates in master
                raise Exception("Write code here")
            elif len(MP) == 0:
                #check for data which is not in master
                source.data.at[SP,'status']='new'
                print("  {} New Line   : {}".format(SP,searchTerm))
                continue
            else:
                MP=int(MP)
            
            for compareColumn in compareList:
                tempSource=str(source.data.at[SP,compareColumn])
                tempMaster=str(master.data.at[MP,compareColumn])
                if tempSource != tempMaster :
                    source.data.at[SP,'status']='change' 
                    print("  {} Line Change: {} {}".format(SP,searchTerm,compareColumn))
                    rowToInsert=master.data.loc[MP]
                    source.data.loc[SP+0.5]=rowToInsert
                    
        # Reorder the index
        source.data=source.data.sort_index().reset_index(drop = True)  
        
        # Add changed source data to XLSreturn
        XLSreturn.setSheet(sheetName,source) 
    
    return XLSreturn
            


if __name__ == "__main__":
    main()
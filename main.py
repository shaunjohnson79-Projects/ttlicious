from readXMLData import parseXML 
from readXLSData import readXLSSource, readXLSMaster, readXLSSheet
import xlsxwriter
import pandas as pd





def main() -> None:
    print("Program Start")
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
    
    
    for SPS, sheet in enumerate(XLSCompare.sheet):
        assert isinstance(sheet, readXLSSheet)
        
        
        originalColumns=sheet.columnMap['original'].tolist()
        originalColumns.append('status')
        
        
        updatedColumns=sheet.columnMap['updated'].tolist()
        updatedColumns.append('status')
        
        
        sheet.data = sheet.data[updatedColumns].copy()
        sheet.data.columns=originalColumns
        

        
        
        NOC=len(sheet.data.columns)
        def highlight_rows(x):
            df = x.copy()
            mask1 = df['status'] == 'new'
            mask2= df['ATINN'] == 11355
            df.loc[mask1, :] = 'background-color: yellow'
            df.loc[mask2, :] = 'background-color: yellow'
            return df 
            # x
            # if x.status == 'new':
            #     return['background-color: pink']*NOC
            # else:
            #     return['background-color: blue']*NOC
        #sheet.data.style.apply(highlight_rows, axis = None)
        print(sheet.data)
        
        XLSSource.sheet[SPS]=sheet
    
    with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
        for SPS, sheet in enumerate(XLSCompare.sheet):
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
            


            
    
def compareSourceToMaster(XLSSource,XLSMaster,settings) -> object:
    """return XLScompare after comparing sheets in source with the master"""
    
    # Define the return variable
    XLSreturn=XLSSource
    
    for SPS, sourceSheet in enumerate(XLSSource.sheet):
        
        # Get the sheets manually
        source=XLSSource.sheet[SPS]
        master=XLSMaster.sheet[SPS]
        
        # Display to screen
        print("Compare Sheet: {}".format(source.name))
        
        #get list of columns to use for compare
        compareList=sourceSheet.getCompareList(sourceSheet.name,settings)
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
                    
        #reorder the index
        source.data=source.data.sort_index().reset_index(drop = True)  
        

        
        
        # Add changed source data to XLSreturn
        XLSreturn.sheet[SPS]=source
    
    return XLSreturn
            
        
                    
    
                    
#                      df.loc[-1] = [2, 3, 4]  # adding a row
#  df.index = df.index + 1  # shifting index
#  df = df.sort_index()  # sorting by index
        


if __name__ == "__main__":
    main()
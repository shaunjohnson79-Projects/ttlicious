from .. import classes
import pandas as pd


def writeToXLS(XLSData, fileName: str, settings: classes.XMLSettings) -> bool:
    """
    Write XLS data to a file
    """

    # Check the filename
    fileName = fileName.replace(".xlsm", ".xlsx")

    # Prepare the data to write
    sheetList = XLSData.getSheetList()
    for sheetName in sheetList:

        # Get sheet data
        sheet = XLSData.getSheet(sheetName)

        # Update the data with the print columns only
        sheet.data = sheet.data[sheet.printList].copy()

        # Replace Duplicate Columns with Original Columns
        sheet.replaceDuplicateColumnsWithOriginalColumns()

        XLSData.setSheet(sheetName, sheet)

        str(XLSData.type).lower()

        # Define the colurs of the rows
        colour_new = False
        colour_change = False
        colour_reference = False
        match str(XLSData.type).lower():
            case 'compare':
                colour_new = '#FCF3CF'
                colour_change = '#D4E6F1'
                colour_reference = '#D1F2EB'
            case 'master':
                colour_new = '#FCF3CF'
                colour_change = '#D4E6F1'
            case _:
                pass

    # Write the data to file
    with pd.ExcelWriter(fileName, engine='xlsxwriter',) as writer:
        print(f"Write {fileName}")
        for sheetName in sheetList:
            # Get sheet data
            sheet = XLSData.getSheet(sheetName)

            # tempSheet=XLSCompare.sheet[SPS]
            rowOffSet = settings.getNameRow(sheetName)
            sheet.data.to_excel(writer, sheet_name=sheet.name, index=False, startrow=rowOffSet-1)
            print(f"  Sheet: {sheetName}")

            workbook = writer.book
            worksheet = writer.sheets[sheet.name]

            format_new = workbook.add_format({'bg_color': colour_new})
            format_change = workbook.add_format({'bg_color': colour_change})
            format_reference = workbook.add_format({'bg_color': colour_reference})

            status = sheet.data['status'].tolist()
            for i, tempStatus in enumerate(status):
                match str(tempStatus).lower():
                    case 'new':
                        worksheet.set_row(i+1+rowOffSet-1, cell_format=format_new)
                    case 'change':
                        worksheet.set_row(i+1+rowOffSet-1, cell_format=format_change)
                    case 'reference':
                        worksheet.set_row(i+1+rowOffSet-1, cell_format=format_reference)
                    case _:
                        pass
    return True

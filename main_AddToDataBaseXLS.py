import src.classes as classes
import src.methods as methods
import hydra

with hydra.initialize(config_path='conf', version_base=None):
    from conf.excel_settings_class import ExcelSettingsLink
    cfg: ExcelSettingsLink = hydra.compose(config_name="excel_settings")
# from conf.sheet_settings_class import SheetSettingsLink
# cfg2: SheetSettingsLink = hydra.compose(config_name="sheet_settings")


@hydra.main(config_path="conf", config_name="excel_settings", version_base=None)
def main(cfg: ExcelSettingsLink) -> None:

    print(f"Program Start")
    # define the filenames
    fileInfo = {}
    fileInfo.update({'XML': f'{cfg.paths.settingsXML}settings.xml'})
    fileInfo.update({'XML': f'{cfg.paths.settingsXML}settingsQuick.xml'})
    fileInfo.update({'XLS_update': f'{cfg.paths.data}20210323 Hinterkipper_de en_finala.update.xlsx'})
    fileInfo.update({'XLS_masterRef': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_master.xlsx'})
    fileInfo.update({'XLS_masterWrite': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_masterv2.xlsx'})
    fileInfo.update({'XLS_SAP': f'{cfg.paths.data}20210323 Hinterkipper_de en_final_SAP.xlsx'})

    # Read in the settings
    settings = classes.XMLSettings(fileInfo['XML'])
    # print(settings)

    # Read in the XLS
    XLSUpdate = classes.XLSUpdate(fileInfo['XLS_update'], settings)
    XLSMaster = classes.XLSMaster(fileInfo['XLS_masterRef'], settings)

    # Calculate the new master file
    XLSMaster = methods.updateMaster(XLSUpdate, XLSMaster)

    # Calculate the file to return to SAP
    XLSUpdate = methods.createSAPupdate(XLSUpdate)

    methods.writeToXLS(XLSMaster, fileInfo['XLS_masterWrite'], settings)
    methods.writeToXLS(XLSUpdate, fileInfo['XLS_SAP'], settings)


if __name__ == "__main__":
    main()

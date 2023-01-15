import yaml
from omegaconf import OmegaConf

class YAMLSettings():
    def __init__(self, YAMLFileName) -> None:
        """Load the YAML file"""
        print(YAMLFileName)
        with open(YAMLFileName, 'r') as yamlFile:
            self.yaml = yaml.safe_load(yamlFile)
    
    def __repr__(self) -> str:
        return OmegaConf.to_yaml(self.yaml)


    @property
    def sheetNamesList(self) -> list :
        return self.__getSheetNamesList()
    
    def __getSheetNamesList(self) -> list:
        sheetNames = list()
        for i, sheet in enumerate(self.yaml['sheet']):
            name = sheet['name']
            sheetNames.append(name)
        return sheetNames
    
    @property
    def sheetNamesDict(self) -> dict :
        return self.__getSheetNamesDict()
    
    def __getSheetNamesDict(self) -> dict:
        sheetNames = dict()
        for i, sheet in enumerate(self.yaml['sheet']):
            name = sheet['name']
            sheetNames.update({name:i})
        return sheetNames
    
    def getNameRow(self, sheetName) -> int:
        sheetNumber=self.sheetNamesDict[sheetName]
        rowNumber=self.yaml['sheet'][sheetNumber]['nameRow']
        rowNumber=int(rowNumber)
        return rowNumber
    
    def getItemListFromName(self, sheetName, itemName) -> list:
        sheetNumber=self.sheetNamesDict[sheetName]
        returnList=self.yaml['sheet'][sheetNumber]['columns'][itemName]
        return returnList


    
def main():

    YAML_folder='settingYAML'
    YAML_fileName="settingsAA.yaml"
    fileNameYAML=f"../{YAML_folder}/{YAML_fileName}"  
    
    settings=YAMLSettings(fileNameYAML)
    print(settings)
    print(settings.sheetNamesList)
    tempSheetName=settings.sheetNamesList[0]
    print(tempSheetName)
    print(settings.sheetNamesDict)
    print(settings.getNameRow(tempSheetName))
    partNumberList = settings.getItemListFromName(tempSheetName,'partNumber')
    print(partNumberList)
    
if __name__ == "__main__":
    main()
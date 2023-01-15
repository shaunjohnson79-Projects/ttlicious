import yaml
import xmltodict
from xml.dom.minidom import parseString

def main():
    XML_folder='settingsXML'
    XML_fileName="settings.xml"
    
    YAML_folder='settingYAML'
    YAML_fileName="settingsTemp.yaml"

    fileNameXML=f"../{XML_folder}/{XML_fileName}"
    fileNameYAML=f"../{YAML_folder}/{YAML_fileName}"
    
    print(fileNameXML)
    print(fileNameYAML)
    with open(fileNameXML) as xmlFile:
        dictData = xmltodict.parse(xmlFile.read())
        
    with open(fileNameYAML, 'w') as yamlFile:
        yaml.dump(dictData, yamlFile, indent=4, sort_keys=False)


if __name__ == "__main__":
    main()
    
    
    
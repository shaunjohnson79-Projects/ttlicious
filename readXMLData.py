import xml.etree.ElementTree as ET

class parseXML(object):    
    def __init__(self,xmlFileName):
        self.doc=ET.parse(xmlFileName)
        self.root = self.doc.getroot()

    def getSheetNames(self) -> list:
        sheetNames=[]
        for sheet in self.root.findall('sheet'):  
            name=sheet.find('name')
            sheetNames.append(name.text)
        return sheetNames
    
    def         
    
    


def main():
    fileName='settings.xml'
    settings = parseXML("settings.xml")
    sheetNames=settings.getSheetNames()
    print(sheetNames)




if __name__ == '__main__':
    main()
    
    
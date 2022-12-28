
import numpy as np
from collections import UserList 



def mainOld() -> None:
    
    objectList=[]
    objectDict={}
    
    list = ['asd','sdf','dfg','fgh','fgh']
    for tempValue in list:
        tempLetter=letters(tempValue)
        objectList.append(tempLetter)
        objectDict.update({len(objectDict):tempLetter})
        

    results = [x.getSheetName() for x in objectList]
    print(results)


    #print(objectDict)
    #print(objectDict.get(0))
    tempLetter.append("asd")
    print(type(tempLetter))
    
    
    
 
  

class letters():
    def __init__(self,input):
        self.value="{}_{}".format(input,input)
        
    def getSheetName(self):
        return self.value

def mainNumpy() -> None:
    student_def = [("name","S10"),("roll","i8"),("marks","f8")]
    student_array = np.zeros((3),dtype=student_def)
    
    print(student_array)
    
    student_array[0] = ("Abhishek",1,95)
    student_array[1] =("Sahil",10,90)
    student_array[2] = ("Abhishek",1,95)
    
    student_array = np.zeros((10),dtype=student_def)
    
    #np.append(student_array,("Abhishek",1,95),0)

    print('---------')
    
    print(type(student_array))
    print(student_array)

if __name__ == "__main__":
    mainOld()
    
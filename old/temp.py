
import numpy as np
import pandas as pd
from collections import UserList
from datetime import datetime


def main1() -> None:

    objectList = []
    objectDict = {}

    list = ['asd', 'sdf', 'dfg', 'fgh', 'fgh']
    for tempValue in list:
        tempLetter = letters(tempValue)
        objectList.append(tempLetter)
        objectDict.update({len(objectDict): tempLetter})

    results = [x.getValue() for x in objectList]
    # print(results)
    bb = objectList[0].getValue()
    print(bb)


class letters():
    def __init__(self, input):
        self.value = "{}_{}".format(input, input)

    def getValue(self):
        return self.value

    def __repr__(self):
        rep = "Value={}".format(self.value)
        return rep


def main2() -> None:
    student_def = [("name", "S10"), ("roll", "i8"), ("marks", "f8")]
    student_array = np.zeros((3), dtype=student_def)

    print(student_array)

    student_array[0] = ("Abhishek", 1, 95)
    student_array[1] = ("Sahil", 10, 90)
    student_array[2] = ("Abhishek", 1, 95)

    student_array = np.zeros((10), dtype=student_def)

    # np.append(student_array,("Abhishek",1,95),0)

    print('---------')

    print(type(student_array))
    print(student_array)


def main3() -> None:

    aa = Test("joe", 23)
    aa = Test("kate", 16)
    aa = Test("adam", 56)

    print(aa)
    print(type(aa))

    print(aa.all_objects[0].name)


class Test():
    all_objects = []

    def __init__(self, name, age):
        self.name = name
        self.age = age
        Test.all_objects.append(self)


def main4():
    list = ['Shaun', 'edna', 'shaun', 'Shaun']

    aa = list.index('Shaun')
    print(aa)


def main5():
    currentDateAndTime = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    print(currentDateAndTime)


def main6():
    aa = Child()


class Parent(object):
    foobar = ['Hello']


class Child(Parent):
    foobar = Parent.foobar + ['world']


if __name__ == "__main__":
    main6()

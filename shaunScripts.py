def getIndices(tempList,searchValue,returnLength=None):
    index = [ind for ind, ele in enumerate(tempList) if ele == searchValue]
    if returnLength != None:
        if len(index) != returnLength:
            print(index)
            raise Exception('return index should be of length: {}'.format(returnLength))
    if len(index) == 1:
        index = index[0]
    return index 
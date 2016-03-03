import collections
import math

# ------------------------------------------------------------------------------------------
mCol = []
dataFrame = []
#-------------- Input-------------------------
noOfAttr = 5
classCol = 4
mode = 1
#---------------------------------------------

def calculatePesError(data):
        col = []
        for temp in data:
                col.append(temp[classCol])
        classColCount = generateCount(col)
        data = sorted(classColCount,key=lambda l:l[1], reverse=True)
        #print "Count class PER - ",classColCount
        return  classColCount[0][1]

#---------------------------------------------------------------

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
        self.isLeaf = False
        self.Gini = None
        self.value = None
        self.colIndex = None
        self.classType = None

    #----------------------------------------------------------------------
    def partition(self,value, colIndex):
        leftDataFrame = []
        rightDataFrame = []

        for row in self.data:
            if(row[colIndex]) <= value:
                leftDataFrame.append(row)
            else:
                rightDataFrame.append(row)
        wtGini = weightedAvgImpurity(leftDataFrame,rightDataFrame)

        return wtGini
    #----------------------------------------------------------------------
    def assignClass(self):
        col = []
        for temp in self.data:
            col.append(temp[classCol])
        classCount = generateCount(col)
        leafClass = classCount[len(classCount)-1][0]
        self.classType = leafClass
        return
    #----------------------------------------------------------------------
    def findSplit(self):
        gini = 0.0
        minGini = 100.0
        minColIndex = 100
        splitEle = 0.0

        if(len(self.data)<=1):
            self.isLeaf = True
            self.assignClass()
            #print 'Node : ',self.value
            #print 'ClassType: ',self.classType
            return None

        self.gini = calculateGiniForClass(self.data, classCol)

        if(self.gini)<0.03:
            self.isLeaf = True
            self.assignClass()
            #print 'Node : %f'%self.value+' ClassType:%d'%self.classType
            return None


        for i in range(noOfAttr):
            if i != classCol:
                colIndex = i
                col = []

                for temp in self.data:
                    col.append(temp[i])
                self.data = sorted(self.data,key=lambda l:l[colIndex], reverse=False)
                #self.data = sorted(self.data,key=lambda l:l[colIndex], reverse=False)
                # print self.data

                dataCount = generateCount(col)

                for ele in range(len(dataCount)-1):
                    currEle = dataCount[ele][0]
                    gini = self.partition(currEle,colIndex)
                    if minGini > gini:
                        minGini = gini
                        minColIndex = colIndex
                        splitEle = currEle
                        self.value = splitEle

        self.gini = minGini
        self.colIndex = minColIndex
        self.generateChildren()


        if not self.isLeaf == True:
            if self.left != None:
                self.left.findSplit()
            if self.right !=None:
                self.right.findSplit()

        return None

    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    def generateChildren(self):
        leftChildData = []
        rightChildData = []
        parentMaxOccuringClass = calculatePesError(self.data)
        parentMisClass = len(self.data) - parentMaxOccuringClass
        for row in self.data:
            if(row[self.colIndex]) <= self.value:
                leftChildData.append(row)
            else:
                rightChildData.append(row)

        leftChildMaxOccuringClass = calculatePesError(leftChildData)
        leftMisClass = len(leftChildData) - leftChildMaxOccuringClass
        rightChildMaxOccuringClass = calculatePesError(rightChildData)
        rightMisClass = len(rightChildData) - rightChildMaxOccuringClass

        pesError = parentMisClass -(leftMisClass + rightMisClass)

        if(pesError >= 1):
            if(len(leftChildData)>0):
                self.left = Node(leftChildData)
            if(len(rightChildData)>0):
                self.right = Node(rightChildData)
        else:
            self.isLeaf = True
        return

#---------------------------------------------------------------------------

def weightedAvgImpurity(left,right):
    if mode == 1:
        impurityLeft = calculateGiniForClass(left,classCol)
        impurityRight = calculateGiniForClass(right,classCol)
    if mode == 2:
        impurityLeft = calcEntropy(left,classCol)
        impurityRight = calcEntropy(right,classCol)

    dataFrameLength = len(left) + len(right)

    wtAvgGini = 1.0
    wtAvgGini -= ((float(len(left))/dataFrameLength)*impurityLeft + (float(len(right))/dataFrameLength)*impurityRight)
    return wtAvgGini
#--------------------------------------------------------------------------------------------------------------
def generateCount(col):
    dataCount = collections.Counter(col)
    dataCount = sorted(dataCount.iteritems())

    return dataCount

#---------------------------------------------------------------------------------------------------------------
def checkNumeric(attr):
    try:
        float(attr)
        return True
    except:
        return False
#---------------------------------------------------------------------------------------------------------------
def loadData(path):
    dataFrame= []
    dataFile = open(path, 'r')

    for dataLine in dataFile:
        ele = dataLine.split(',')
        ele[len(ele) - 1] = ele[len(ele) - 1].split('\n', 2)[0]
        #ele.pop(8)
        for x in range(len(ele)):
            if checkNumeric(ele[x]):
                ele[x] = float(ele[x])
            else:
                if not x in mCol:
				    mCol.append(x)
        dataFrame.append(ele)

    dataFile.close()
    return dataFrame
#-------------------------------------------------------------------------------------------------------------------
def displayData(dataSet):
    for i in range(len(dataSet)):
        print dataSet[i]
#-------------------------------------------------------------------------------------------------------------------
def inorder(node):
  if node != None:
      inorder(node.left)
      print(node.value)
      inorder(node.right)
#-------------------------------------------------------------------------------------------------------------------
def calculateGiniForClass(partition, attrCol):
    col = []
    for temp in partition:
        col.append(temp[attrCol])

    dataCount = collections.Counter(col)
    dataCount = sorted(dataCount.iteritems())
    gini = 1.0
    for dataVal in dataCount:
        gini -= math.pow((float(dataVal[1]) / len(partition)), 2)
    # print gini
    return gini
#-------------------------------------------------------------------------------------------------------------------
def calcEntropy(partition, attrCol):
    col = []
    entropy = 0.0
    for temp in partition:
        col.append(temp[attrCol])

    dataCount = collections.Counter(col)
    dataCount = sorted(dataCount.iteritems())

    for dataVal in dataCount:
        entropy += (float(dataVal[1]) / len(partition))*math.log((float(dataVal[1]) / len(partition)),2)
    # print gini
    return -entropy
#-------------------------------------------------------------------------------------------------------------------
def trainModel(training_data):

    root = Node(training_data)
    root.findSplit()

    return root
#-------------------------------------------------------------------------------------------------------------------
def testModel(root, test_data):
    currCol = 0
    listAccuracy = []
    matchCount = 0
    for row in test_data:
        node = root
        while node!=None and node.isLeaf!=True:
            if row[node.colIndex] <= node.value:
                node = node.left
            else:
                node = node.right
        #print row
        #print 'Predicted Class: ', node.classType
        if node!= None and row[classCol]==node.classType:
            matchCount+=1

    accuracy = float(matchCount)/len(test_data) * 100
    return accuracy

def convertToNumeric(dataSet, columnNumber):
    mapping = []
    for line in dataSet:
        if line[columnNumber] not in mapping:
            mapping.append(line[columnNumber])

        line[columnNumber] =  int(mapping.index(line[columnNumber]))

#----------------------------------------------------------------------------------------------------------
def validate():

    dataFrame = loadData('iris.data')
    dataSet = dataFrame
    for c in range(len(mCol)):
        convertToNumeric(dataSet, mCol[c])

    displayData(dataSet)
    listAccuracy = []

    k = 0
    print 'Building tree...'
    while k < len(dataSet):
        train_data = []
        test_data = []
        for i in range(len(dataSet)):
            if i>=k and i<=k+(len(dataSet)/10):
                test_data.append(dataSet[i])
            else:
                train_data.append(dataSet[i])
        root = trainModel(train_data)
        listAccuracy.append(testModel(root,test_data))
        k+=len(dataSet)/10
    print 'Testing Model....'

    sum = 0.0
    for acc in listAccuracy:
        sum+=acc
    finalAccuracy = sum/len(listAccuracy)

        print 'Tree Formed using Pessimistic Error Estimate approach!'
    return
# ----------------------------------------------------------------------------------------------------------------

validate()


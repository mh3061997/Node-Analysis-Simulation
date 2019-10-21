import numpy as np
import math


def numbers_to_strings(argument):
    switcher = {
        0: "zero",
        1: "one",
        2: "two",
    }


class Component:
    def __init__(self, Type, Node1, Node2, Value, InitialValue):
        self.Type = Type
        self.Node1 = Node1
        self.Node2 = Node2
        self.Value = Value
        self.InitialValue = InitialValue


def ParsingFile(FileName):
    f = open(FileName, "r")
    if f.mode == "r":  # check if file is open
        FileContents = f.readlines()  # read file line by line
    for i in range(np.shape(FileContents)[0] - 1):  # loop for the lines before last
        FileContents[i] = FileContents[i][0:len(FileContents[i]) - 1]
    mTimeStamp = FileContents[0]
    Dummy = FileContents[1]
    FileContents = FileContents[2:]
    nComponentList = []
    for i in range(np.shape(FileContents)[0]):
        Line = FileContents[i].split()
        nComponentList.append(Component(Line[0], Line[1], Line[2], Line[3], Line[4]))
    return nComponentList, mTimeStamp


def initmatg(matrixG, ComponentList):
    for component in ComponentList:
        if component.Type == "R":
            node1 = int(component.Node1[1])
            node2 = int(component.Node2[1])
            matrixG[node1][node1] += 1 / float(component.Value)
            matrixG[node2][node2] += 1 / float(component.Value)
            matrixG[node1][node2] = -1 / float(component.Value)  # leh msh += heya kman
            matrixG[node2][node1] = -1 / float(component.Value)


def initmatb(matrixb, ComponentList):
    for component in ComponentList:
        if component.Type == "Vsrc":
            for index, node in enumerate(matrixb):
                # print(index)
                pos = int(component.Node1[1])
                neg = int(component.Node2[1])
                if index == pos:
                    matrixb[index][0] = 1
                elif index == neg:
                    matrixb[index][0] = -1
                else:
                    matrixb[index][0] = 0


def initmatc(B):
    return B.transpose()


def IniMatA(G, B, C, D):
    UpperA = np.hstack((G, B))
    DownA = np.hstack((C, D))
    return np.vstack((UpperA, DownA))


def initmate(matrixe, ComponentList):
    for component in ComponentList:
        if component.Type == "Vsrc":
            volt = int(component.Value)
            for index, node in enumerate(matrixe):
                matrixe[index][0] = volt


def initmati(matrixi, ComponentList):
    for component in ComponentList:
        if component.Type == "Isrc":
            node1 = int(component.Node1[1])
            node2 = int(component.Node2[1])
            if node1 != 0:
                matrixi[node1][0] = float(component.Value)
            if node2 != 0:
                matrixi[node2][0] = float(component.Value)


def WriteToFile(FileName, Step, Values,n):
    f = open(FileName, "w+")
    for i in range(n):
        f.write("V%d\r\n" % (i + 1))
        f.write()
    f.close()


ComponentList = []
TimeStamp = 0
ComponentList, TimeStamp = ParsingFile("2.txt")
n = 0  # representing Number of Nodes
m = 0  # representing Number of ID voltage Source
for mComponent in ComponentList:
    n = max(n, int(mComponent.Node1[1]), int(mComponent.Node2[1]))  # To Get Number of Nodes
    if mComponent.Type == "Vsrc":  # Count The No. of Voltage src
        m = m + 1
n = n + 1

#                                   Mat A
# INITIALIZING the Matrices
print(n)
G = np.zeros((n, n))  # for A resistance
B = np.zeros((n, m))  # connection of the voltage sources
C = np.zeros((m, n))  # Transpose of B
D = np.zeros((m, m))  # is a zero matrix
initmatg(G, ComponentList)
initmatb(B, ComponentList)
C = initmatc(B)

print("MatG:\n", G)
print("MatB:\n", B)
print("MatC:\n", C)
print("MatD:\n", D)
A = IniMatA(G, B, C, D)
#                                 Mat X(Unknown)
V = np.zeros((n, 1))  # hold the unknown voltages at each node
J = np.zeros((m, 1))  # holds the unknown currents through the voltage sources.
X = np.vstack((V, J))
#                                  Mat Z
I = np.zeros((n, 1))
E = np.zeros((m, 1))
initmate(E, ComponentList)
initmati(I, ComponentList)
Z = np.vstack((I, E))
# Solving The AX=Z
print("MatA:", A, "\nMatZ", Z)
X = np.linalg.det(A)
X = np.linalg.solve(A, Z)
print("nnnn:", X)
# missing logic remove Node 0

FILE_LL = "ll.txt"
FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"

def readFile(filename):
    f=open(filename,"r")
    return f.readlines()

def extractLLnLR():
    content = readFile(FILE_INPUT)
    # Initialize LL and LR arrays
    LL = []
    LR = []

    # Loop through each line in the file
    for line in content:
        # Split the line into the table type and the input string
        table_type, input_string = line.strip().split(';')
        table_type=table_type.strip()
        input_string=input_string.strip()

        # Add the input string to the appropriate array
        if table_type == 'LL':
            LL.append(input_string)
        elif table_type == 'LR':
            LR.append(input_string)

    return LL,LR

def LRstatesNterminals():
    content = readFile(FILE_LR)
    Terminals=[]
    States=[]
    lr_table = [line.split(';') for line in content]
    for row in lr_table:
        # Skip the first row
        if row == lr_table[0]:
            continue

        if row[0].startswith("states"):
            for i in range(len(row)):
                if i == 0: continue
                Terminals.append(row[i].strip())
        if row[0].startswith("State"):
            States.append(row[0])

    return Terminals,States

def fillTable(Terminals,States):
    lrTable=[[0]*(len(Terminals)+1) for i in range(len(States)+1)]
    lrTable[0][0]="LR"
    for i in range(len(States)+1):
        if i == 0: continue
        lrTable[i][0]=States[i-1]
    for i in range(len(Terminals)+1):
        if i == 0: continue
        lrTable[0][i]=Terminals[i-1]

    content = readFile(FILE_LR)
    # split each string by ';'
    table = [row.split(';') for row in content]

    # remove leading/trailing whitespaces in each cell
    table = [[cell.strip() for cell in row] for row in table]

    # print the resulting 2D array
    return table
def parseString(inputStr):
    terminals,states=LRstatesNterminals()
    parsedInputStack = []

    for char in inputStr:
        # If the character is in the terminals array, add it to the split input list
        if char in terminals:
            parsedInputStack.append(char)

    return parsedInputStack

def StringifyArr(inputstr):
    stringifiedArr=""

    for elem in inputstr:
        stringifiedArr=stringifiedArr+elem

    return  stringifiedArr

def findTerminalIndex(terminal,table):
        for j in range(len(table[1])):
            if table[1][j] == terminal:
                return j

def findStateIndex(state,table):
    for i in range(len(table)):
            if table[i][0] == state:
                return i


def LR(inputStr):
    k=0
    stateStack=[]
    numberStateStack=[]
    stateStack.append(states[0])
    numberStateStack.append(states[0].removeprefix("State_"))
    table=fillTable(terminals,states)
    currentStack=""
    flag=True
    roundCount=0
    print("Processing input string ",inputStr," for LR(1) parsing table")
    print()
    print("NO | STATE STACK | READ | INPUT | ACTION ")
    while flag:
        roundCount+=1
        action=""
        read=inputStr[k]
        currentStack=stateStack[k]
        tableValue=table[findStateIndex(currentStack,table)][findTerminalIndex(read,table)]
        if tableValue.startswith("State"):
            action = "Shift to " + tableValue
        if not tableValue.startswith("State"):
            if tableValue == "Accept":
                action="ACCEPTED"
            else:
                action = "Reverse " + tableValue
        if tableValue == "":
            action = "REJECTED (",table[findStateIndex(currentStack,table)][0]," does not have an action/step for",read
            flag=False
        print(roundCount, "", "|", numberStateStack, "      |", read, "|", inputStr, "|",action)
        if tableValue != "":
            if tableValue == "Accept":
                flag = False
                break
            if not tableValue.startswith("State"):
                parsedValue=tableValue.strip().split("->")
                parsedString=parseString(parsedValue[1])
                stringifiedInput=StringifyArr(inputStr)
                stringifiedInput=stringifiedInput.replace(parsedValue[1],parsedValue[0])
                inputStr=parseString(stringifiedInput)
                for i in range(len(parsedString)):
                    stateStack.pop()
                    numberStateStack.pop()
                k=inputStr.index(parsedValue[0])


            if tableValue.startswith("State"):
                stateStack.append(tableValue)
                numberStateStack.append(tableValue.removeprefix("State_"))
                k += 1
        elif tableValue=="":
            flag=False


        




if __name__ == '__main__':
    LLinputs=[]
    LRinputs=[]
    terminals=[]
    states=[]
    LLinputs,LRinputs=extractLLnLR()
    terminals,states=LRstatesNterminals()
    LR(LRinputs[0])

# -- coding: utf-8 --
FILE_LL = "ll.txt"
FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"


def readFile(filename):
    f = open(filename, "r")
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
        table_type = table_type.strip()
        input_string = input_string.strip()

        # Add the input string to the appropriate array
        if table_type == 'LL':
            LL.append(input_string)
        elif table_type == 'LR':
            LR.append(input_string)

    return LL, LR


def LRstatesNterminals():
    content = readFile(FILE_LR)
    Terminals = []
    States = []
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
            States.append(row[0].strip())

    return Terminals, States


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
    
    table = [row.split(';') for row in content]


    table = [[cell.strip() for cell in row] for row in table]


    return table


def parseString(inputStr):
    terminals, states = LRstatesNterminals()
    parsedInputStack = []

    for char in inputStr:
        # If the character is in the terminals array, add it to the split input list
        if char in terminals and char != " ":
            parsedInputStack.append(char)

    return parsedInputStack


def StringifyArr(inputstr):
    stringifiedArr = ""

    for elem in inputstr:
        stringifiedArr = stringifiedArr + elem

    return stringifiedArr


def findTerminalIndex(terminal, table):
    for j in range(len(table[1])):
        if table[1][j] == terminal:
            return j


def findStateIndex(state, table):
    for i in range(len(table)):
        if table[i][0] == state:
            return i


def LR(inputStr):
    k = 0
    stateStack = []
    numberStateStack = []
    stateStack.append(states[0])
    numberStateStack.append(states[0].removeprefix("State_"))
    table = fillTable(terminals, states)
    currentStack = ""
    flag = True
    roundCount = 0
    print("Processing input string ", inputStr, " for LR(1) parsing table")
    print()
    print("NO | STATE STACK | READ | INPUT | ACTION ")
    while flag:
        roundCount += 1
        action = ""
        read = inputStr[k]
        currentStack = stateStack[k]
        tableValue = table[findStateIndex(currentStack, table)][findTerminalIndex(read, table)]
        if tableValue.startswith("State"):
            action = "Shift to " + tableValue
        if not tableValue.startswith("State"):
            if tableValue == "Accept":
                action = "ACCEPTED"
            else:
                action = "Reverse " + tableValue
        if tableValue == "":
            action = "REJECTED (", table[findStateIndex(currentStack, table)][
                0], " does not have an action/step for", read
            flag = False
        print(roundCount, "", "|", numberStateStack, "      |", read, "|", inputStr, "|", action)
        if tableValue != "":
            if tableValue == "Accept":
                flag = False
                break

            if not tableValue.startswith("State"):
                parsedValue = tableValue.strip().split("->")
                temp = ""
                for i in parsedValue[1]:
                    if i != " ":
                        temp += i
                parsedValue[1] = temp
            if not tableValue.startswith("State"):
                parsedValue = tableValue.strip().split("->")
                parsedString = parseString(parsedValue[1])
                stringifiedInput = StringifyArr(inputStr)
                stringifiedInput = stringifiedInput.replace(parsedValue[1], parsedValue[0])
                inputStr = parseString(stringifiedInput)
                for i in range(len(parsedString)):
                    stateStack.pop()
                    numberStateStack.pop()
                k = inputStr.index(parsedValue[0])

            if tableValue.startswith("State"):
                stateStack.append(tableValue)
                numberStateStack.append(tableValue.removeprefix("State_"))
                k += 1
        elif tableValue == "":
            flag = False


def LLTerminalsAndNonTerminals():
    content = readFile(FILE_LL)
    Terminals = []
    Nonterminals = []
    ll_table = [line.split(';') for line in content]
    for row in ll_table:
        if row[0].startswith("LL"):
            for i in range(len(row)):
                if i == 0: continue
                Terminals.append(row[i].strip())
        if row[0] != "LL":
            Nonterminals.append(row[0].strip())

    return Terminals, Nonterminals


def LLexpressions(Terminals, Nonterminals):
    llTable = [[0] * (len(Terminals) + 1) for i in range(len(Nonterminals) + 1)]
    llTable[0][0] = "LL"
    for i in range(len(Nonterminals) + 1):
        if i == 0: continue
        llTable[i][0] = Nonterminals[i - 1]
    for i in range(len(Terminals) + 1):
        if i == 0: continue
        llTable[0][i] = Terminals[i - 1]

    content = readFile(FILE_LL)
    # split each string by ';'
    table = [row.split(';') for row in content]

    # remove leading/trailing whitespaces in each cell
    table = [[cell.strip() for cell in row] for row in table]

    # print the resulting 2D array
    return table


def LLinputToStack(input_string):
    terminals, nonterminals = LLTerminalsAndNonTerminals()

    stack = []

    # Iterate through the input string in reverse order
    i = len(input_string) - 1
    while i >= 0:
        char = input_string[i]
        if char == 'd' and i > 0 and input_string[i - 1] == 'i':
            # If the character is 'd' and the previous character is 'i', it is an 'id' symbol
            stack.append('id')
            i -= 1  # Skip over the 'i' character
        elif char in terminals:
            # Append terminal symbol to the stack
            stack.append(char)
        i -= 1

    return stack


def LLreadExpression(input_string, stack):
    terminals, nonterminals = LLTerminalsAndNonTerminals()

    # Iterate through the input string in reverse order
    i = len(input_string) - 1
    while i >= 0:
        char = input_string[i]
        if char == 'd' and i > 0 and input_string[i - 1] == 'i':
            # If the character is 'd' and the previous character is 'i', it is an 'id' symbol
            stack.append('id')
            i -= 1  # Skip over the 'i' character
        elif char == "'" and i > 0 and input_string[i - 1] in nonterminals:
            # If the character is 'd' and the previous character is 'i', it is an 'id' symbol
            stack.append(input_string[i - 1] + "'")
            i -= 1  # Skip over the 'i' character
        elif char in terminals or char in nonterminals:
            # Append symbol to the stack
            stack.append(char)
        elif char == '':
            stack.append('')
        i -= 1

    return stack


def findLLTerminalIndex(terminal, table):
    for j in range(len(table[0])):
        if table[0][j] == terminal:
            return j


def findNonterminalIndex(nonterminal, table):
    for i in range(len(table)):
        if table[i][0] == nonterminal:
            return i


def LL(inputStr):
    flag = True
    roundCount = 1
    terminals, nonterminals = LLTerminalsAndNonTerminals()
    Table = LLexpressions(terminals, nonterminals)
    inputStack = LLinputToStack(inputStr)
    stack = []
    stack.append("$")
    startValue = Table[findNonterminalIndex(nonterminals[0], Table)][
        findLLTerminalIndex(inputStack[len(inputStack) - 1], Table)]
    action = startValue
    Value = startValue.strip().split("->")

    print("Processing input string ", inputStr, " for LL(1) parsing table")
    print()
    print("NO | STACK | READ | INPUT | ACTION ")

    if Value[0] == '':
        action = "REJECTED (", nonterminals[0], " does not have an action/step for ", inputStack[
            len(inputStack) - 1], ")"
        print(roundCount, " | ", stack, "| ", inputStack, " | ", action, )
        flag = False
    else:
        print(roundCount, " | ", stack, "| ", inputStack, " | ", action, )
        LLreadExpression(Value[1], stack)

    while flag:

        roundCount += 1
        read = inputStack.pop()
        # print(read)
        temp = stack.pop()

        if read != temp:
            stack.append(temp)
            inputStack.append(read)
            tableValue = Table[findNonterminalIndex(temp, Table)][findLLTerminalIndex(read, Table)]
            action = tableValue
            epsilonValue = action.strip().split("->")

            action = epsilonValue
            parsedValue = tableValue.strip().split("->")
            stack.pop()
            if parsedValue[0] == '':
                action = "REJECTED (", temp, " does not have an action/step for ", read, ")"
                flag = False
                print(roundCount, " | ", stack, "| ", inputStack, " | ", action, )
                break
            LLreadExpression(parsedValue[1], stack)
        elif temp == read:
            action = "Match and remove ", temp
        if temp == "$" and read == "$":
            action = "ACCEPTED"
            flag = False

        print(roundCount, " | ", stack, "| ", inputStack, " | ", action, )


if __name__ == '__main__':
    LLinputs, LRinputs = extractLLnLR()
    terminals,states=LRstatesNterminals()

    for i in range(len(LLinputs)):
        LL(LLinputs[i])

    for i in range(len(LRinputs)):
        LR(LRinputs[i])

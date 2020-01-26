pathForGcodeFile = (
    "D:/SMP/Singapore University of Technology and Design/Theo Victor Calais - Article/Article-2_Sleeve/Sleeve_Gcodes/191220_New Design of Gripper/191222/191220_New Design of Gripper/Sortaclear/walls.gcode")
# location of text file, note the different '/' and '\'

def RemoveExtraSpaceBetweenLines(pathForGcodeFile):
    print("Started removing irrelevant spaces")
    textFile = open(pathForGcodeFile, 'r').read()
    with open(pathForGcodeFile, "w") as f:
        lines = textFile.split('\n')
        # print(lines)
        for line in lines:
            # print(line)
            if line != "":
                f.write(line)
                f.write('\n')
                # print(line)
                #print("Working")

    print("Successful")

RemoveExtraSpaceBetweenLines(pathForGcodeFile)

def CleanRepetitiveM7M9(pathForGcodeFile):
    textArray = []
    textFile = open(pathForGcodeFile, 'r').read()
    with open(pathForGcodeFile, "w") as f:
        lines = textFile.split('\n')
        for line in lines:
            textArray.append(line)
            #print(line)
    print(textArray)

    with open(pathForGcodeFile, "w") as f:
        lines = textFile.split('\n')
        text = lines
        # print(lines[1])
        lineNumber = -1
        countM7 = 0
        countM9 = 0
        stop = 0
        for line in lines:
            f.write(line)
            f.write('\n')
            lineNumber = lineNumber + 1
            print(line)
            if ((line[0:2] == 'M9')):
                for i in range(lineNumber, len(textArray)):
                    if stop == 0:
                        if ((textArray[i]) == 'M7'):
                            countM7 = countM7 + 1
                            M7location = i
                            stop = stop + 1

                        elif((textArray[i]) == 'M9'):
                            countM9 = countM9 + 1
                            M9location = i
                            stop = stop + 1
                if (M7location < M9location):
                    print("Repetitive M9 between line number ", end = "")
                    print(M9location, end = " ")
                    print("and", end = " ")
                    print(M7location, end = " ")

#CleanRepetitiveM7M9(pathForGcodeFile)

def storeM7M9inArray(pathForGcodeFile):
    M7M9Array = []
    lineNumber = 0
    lineNumberArray = []
    textFile = open(pathForGcodeFile, 'r').read()
    with open(pathForGcodeFile, "w") as f:
        lines = textFile.split('\n')
        for line in lines:
            f.write(line)
            f.write('\n')
            lineNumber += 1
            if line[0:2] == 'M7':
                M7M9Array.append(line)
                lineNumberArray.append(lineNumber)
            if line[0:2] == 'M9':
                M7M9Array.append(line)
                lineNumberArray.append(lineNumber)
            #textArray.append(line)
            # print(line)
    #for elements in M7M9Array:
    for i in range(len(M7M9Array)-1):
        if M7M9Array[i] == M7M9Array[i+1]:
            if M7M9Array[i] == 'M7':
                print("Potential M9 missing between line number", end = " ")
                print(lineNumberArray[i], end = " ")
                print("and", end = " ")
                print(lineNumberArray[i+1])
            if M7M9Array[i] == 'M9':
                print("Potential M7 missing between line number", end=" ")
                print(lineNumberArray[i], end=" ")
                print("and", end=" ")
                print(lineNumberArray[i + 1])
        #print(M7M9Array[i])
    #print(M7M9Array)
    #print(lineNumberArray)

storeM7M9inArray(pathForGcodeFile)

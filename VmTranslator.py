import sys
from enum import Enum
import os


class CommandType(Enum):
    C_ARITHEMATIC = 1
    C_PUSH = 2
    C_POP = 3 
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9


class Parser():
    def __init__(self, filname):
        self.filename = filename
        self.f = open(filename, "r+")

        self.currentCommand = ""
        self.nextCommand = ""

    def CommandType(self):
        print(self.f.readlines())

    #also returns a comment if the line is empty
    def isComment(self, string):
        secondSlash = False
        for x in string:
            if x == "/" and secondSlash:
                return True
            elif x == "/":
                secondSlash = True
            elif not x.isspace():
                return False
        return True
    
    def __readNextCommand(self):
        temp = self.f.readline()
        temp = temp[0:-1]
        while(self.isComment(temp)):
            temp = self.f.readline()
            #EOF
            if(temp == ""):
                return temp
            temp = temp[0:-1]
        return temp

    def hasMoreCommands(self):
        if(self.nextCommand):
            return True
        nextCommand = self.__readNextCommand()
        if(nextCommand):
            self.nextCommand = nextCommand
            return True
        return False
    
    def advance(self):
        if(self.nextCommand):
            self.currentCommand = self.nextCommand
            self.nextCommand = ""
        else:
            self.currentCommand = self.__readNextCommand()
        self.spliceCommand()
        
    def spliceCommand(self):
        splicedCommand = self.currentCommand.split(" ")
        length = len(splicedCommand)
        if (length == 3):
            command = splicedCommand[0]
            if command == "push":
                self.commandType = CommandType.C_PUSH
            elif(command == "pop"):
                self.commandType = CommandType.C_POP

            self.arg1 = splicedCommand[1]
            self.arg2 = splicedCommand[2]
        elif(length == 1):
            self.commandType = CommandType.C_ARITHEMATIC
            self.arg1 = splicedCommand[0]
        


class CodeWriter():

    def __init__(self, filename):
        self.filename = filename
        self.f = open(filename + ".asm", "w+")
        self.labelcounter = 100
    
    def writeArithematic(self, command):
        print(command)
        if(command == "add"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=D+M")
        if(command == "sub"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=M-D")
        if(command == "neg"):
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=-M")
        if(command == "eq"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=M-D")
            
            trueLabel = self.generateLabel()
            falseLabel = self.generateLabel()
            self.write("D=M")
            self.write("@" + trueLabel)
            self.write("D; JEQ")

            self.write("@0")
            self.write("D=A")
            self.write("@" + falseLabel)
            self.write("0;JMP")

            self.write("(" + trueLabel + ")")
            self.write("@0")
            self.write("D=A-1")

            self.write("(" + falseLabel + ")")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=D")
        if(command == "gt"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=M-D")
            
            trueLabel = self.generateLabel()
            falseLabel = self.generateLabel()
            self.write("D=M")
            self.write("@" + trueLabel)
            self.write("D; JGT")

            self.write("@0")
            self.write("D=A")
            self.write("@" + falseLabel)
            self.write("0;JMP")

            self.write("(" + trueLabel + ")")
            self.write("@0")
            self.write("D=A-1")

            self.write("(" + falseLabel + ")")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=D")
        if(command == "lt"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=M-D")
            
            trueLabel = self.generateLabel()
            falseLabel = self.generateLabel()
            self.write("D=M")
            self.write("@" + trueLabel)
            self.write("D; JLT")

            self.write("@0")
            self.write("D=A")
            self.write("@" + falseLabel)
            self.write("0;JMP")

            self.write("(" + trueLabel + ")")
            self.write("@0")
            self.write("D=A-1")

            self.write("(" + falseLabel + ")")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=D")
        if(command == "and"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=D&M")
        if(command == "or"):
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=D|M")
        if(command == "not"):
            self.write("@SP")
            self.write("A=M-1")
            self.write("M=!M")

        


    def generateLabel(self):
        self.labelcounter+=1
        return  "LABEL" + str(self.labelcounter) 
    

    def writePushPop(self, command, segement, index):
        if command == CommandType.C_PUSH:
            if(segement == "constant"):
                #writes value to push to register 13
                self.write("@" + str(index))
                self.write("D=A")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

            elif(segement == "static"):
                #writes value to push to register 13
                self.write("@" + str(filename) + "." + str(index))
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()
            elif(segement == "local"):
                #writes value to push to register 13
                self.write("@LCL")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("A=D+A")
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

            elif(segement == "temp"):
                #writes value to push to register 13
                self.write("@5")
                self.write("D=A")
                self.write("@" + str(index))
                self.write("A=D+A")
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

            elif(segement == "argument"):
                #writes value to push to register 13
                self.write("@ARG")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("A=D+A")
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

            elif(segement == "this"):
                #writes value to push to register 13
                self.write("@THIS")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("A=D+A")
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

            elif(segement == "that"):
                #writes value to push to register 13
                self.write("@THAT")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("A=D+A")
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

            
            elif(segement == "pointer"):
                #writes value to push to register 13
                if(index == "0"):
                    self.write("@THIS")
                elif(index == "1"):
                    self.write("@THAT")
                self.write("D=M")
                self.write("@13")
                self.write("M=D")

                self.pushToStack()

        elif command == CommandType.C_POP:
            if(segement == "local"):
                #writes memory location to pop to register 13
                self.write("@LCL")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("D=D+A")
                self.write("@13")
                self.write("M=D")

                self.popAndWrite()

            elif(segement == "temp"):
                #writes memory location to pop to register 13
                self.write("@5")
                self.write("D=A")
                self.write("@" + str(index))
                self.write("D=D+A")
                self.write("@13")
                self.write("M=D")

                self.popAndWrite()

            elif(segement == "static"):
                #writes memory location to pop to register 13
                self.write("@" + str(filename) +  "." + str(index))
                self.write("D=A")
                self.write("@13")
                self.write("M=D")

                self.popAndWrite()

            elif(segement == "argument"):
                #writes memory location to pop to register 13
                self.write("@ARG")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("D=D+A")
                self.write("@13")
                self.write("M=D")

                self.popAndWrite()

            elif(segement == "this"):
                #writes memory location to pop to register 13
                self.write("@THIS")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("D=D+A")
                self.write("@13")
                self.write("M=D")

                self.popAndWrite()

            elif(segement == "that"):
                #writes memory location to pop to register 13
                self.write("@THAT")
                self.write("D=M")
                self.write("@" + str(index))
                self.write("D=D+A")
                self.write("@13")
                self.write("M=D")

                self.popAndWrite()

            elif(segement == "pointer"):

                # #writes memory location to pop to register 13
                # self.write("@ARG")
                # self.write("D=M")
                # self.write("@" + str(index))
                # self.write("D=D+A")
                # self.write("@13")
                # self.write("M=D")

                #get stackpointer and decrements
                self.write("@SP")
                self.write("M=M-1")
                self.write("D=M")

                #write to stack
                self.write("A=D")
                self.write("D=M")
                if(index == "0"):
                    self.write("@THIS")
                elif(index == "1"):
                    self.write("@THAT")
                self.write("M=D")

    #writes from memory adress 13 to stack
    def pushToStack(self):
        #get stackpointer and increments
        self.write("@SP")
        self.write("D=M")
        self.write("M=M+1")

        #write to stack
        self.write("@13")
        self.write("D=D+M")
        self.write("A=D-M")
        self.write("M=D-A")
    

    #pops from stack and writes to memory adress in location 13
    def popAndWrite(self):
        #get stackpointer and decrements
        self.write("@SP")
        self.write("M=M-1")
        self.write("D=M")

        #write to stack
        self.write("A=D")
        self.write("D=M")
        self.write("@13")
        self.write("A=M")
        self.write("M=D")




    
    def write(self, towrite):
        self.f.write(towrite + "\n")
            





if __name__ == "__main__":
    filename = sys.argv[1]
    parser = Parser(filename)
    ()
    coder = CodeWriter(os.path.splitext(filename)[0])
    # coder.writePushPop(CommandType.C_PUSH, "constant", 10)
    # coder.writePushPop(CommandType.C_PUSH, "constant", 100)
    # coder.writePushPop(CommandType.C_PUSH, "constant", 1000)
    # coder.writePushPop(CommandType.C_PUSH, "constant", 14)
    # coder.writePushPop(CommandType.C_PUSH, "constant", 1146)


    
    while(parser.hasMoreCommands()):
        parser.advance()
        if(parser.commandType == CommandType.C_PUSH or parser.commandType == CommandType.C_POP):
            coder.writePushPop(parser.commandType, parser.arg1, parser.arg2)
        elif(parser.commandType == CommandType.C_ARITHEMATIC):
            coder.writeArithematic(parser.arg1)


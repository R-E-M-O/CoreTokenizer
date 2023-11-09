from CoreScanner import CoreScanner
from abc import abstractmethod

global inputList
inputList = []

def initTokenizer(progFile, inputFile):
    global t, input
    t = CoreScanner(progFile)
    input = open(inputFile)
    for line in input:
        inputList.extend(line.split())
        

    



global prettyPrint
prettyPrint = "\t"

# program non-terminal class
class Prog():
    ds = None
    ss = None

    def parseProg(self):
        
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the program token
        if tokNo != 1:
            print("Error: Expected program, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the program's declaration sequence
        self.ds = DS()
        self.ds.parseDS()

        # error check for the begin token
        tokNo = t.getToken()
        if tokNo != 2:
            print("Error: Expected begin, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the program's statement sequence
        self.ss = SS()
        self.ss.parseSS()

        # error check for the end token
        tokNo = t.getToken()
        if tokNo != 3:
            print("Error: Expected end, got " + str(tokNo))
            exit(1)
        
        t.skipToken()

        # error check for the EOF token
        tokNo = t.getToken()
        if tokNo != 33:
            print("Error: Expected EOF, got " + str(tokNo))
            exit(1)
        
        return

    def printProg(self):
        print("program", end="")
        self.ds.printDS()
        print("begin ", end = "")
        self.ss.printSS()
        print("end", end = "")
    
    def execProg(self):
        self.ss.execSS()


class Assign():
    _id= None
    _exp = None

    def parseAssign(self):
        tokNo: int = None
        self._id = Id.parseId2()

        tokNo = t.getToken()

        # error check for the assignment token
        if tokNo != 14:
            print("Error: Expected =, got " + str(tokNo))
            exit(1)

        t.skipToken()

        self._exp = Exp()
        self._exp.parseExp()

        tokNo = t.getToken()

        # error check for the semicolon token
        if tokNo != 12:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)

        t.skipToken()

    
    def printAssign(self):
        self._id.printId()
        print(" = ", end="")
        self._exp.printExp()
        print(";\n", end= "")

    def execAssign(self):
        self._id.setIdVal(self._exp.evalExp())


class Stmt():
    altNo: int = 0
    # Assign
    s1 = None
    # If
    s2 = None
    # Loop
    s3 = None
    # Input
    s4 = None
    # Output
    s5 = None

    def parseStmt(self):
        tokNo: int = t.getToken()


        # error check for statement keywords
        if tokNo not in [5, 8, 32, 10, 11]:
            print("Error: Expected identifier, if, while, read, or write, got " + str(tokNo))
            exit(1)

        # check for assignment
        if tokNo == 32:
            self._altNo = 1
            self.s1 = Assign()
            self.s1.parseAssign()
        # check for if
        elif tokNo == 5:
            self.altNo = 2
            self.s2 = If()
            self.s2.parseIf()
        # check for loop
        elif tokNo == 8:
            self.altNo = 3
            self.s3 = Loop()
            self.s3.parseLoop()
        # check for input
        elif tokNo == 10:
            self.altNo = 4
            self.s4 = Input()
            self.s4.parseInput()
        # check for output
        elif tokNo == 11:
            self.altNo = 5
            self.s5 = Output()
            self.s5.parseOutput()

    def printStmt(self):
        if self.altNo == 1:
            self.s1.printAssign()
        elif self.altNo == 2:
            self.s2.printIf()
        elif self.altNo == 3:
            self.s3.printLoop()
        elif self.altNo == 4:
            self.s4.printInput()
        elif self.altNo == 5:
            self.s5.printOutput()


    def execStmt(self):
        if self.altNo == 1:
            self.s1.execAssign()
        elif self.altNo == 2:
            self.s2.execIf()
        elif self.altNo == 3:
            self.s3.execLoop()
        elif self.altNo == 4:
            self.s4.execInput()
        elif self.altNo == 5:
            self.s5.execOutput()

class SS():
    stmt = None
    ss = None
    
    def parseSS(self):
        self.stmt = Stmt()
        self.stmt.parseStmt()

        tokNo: int = None
        tokNo = t.getToken()

        if tokNo not in [5, 8, 10, 11, 32, 3, 7]:
            print("Error: Expected if, while, read, write, id, end, or else, got " + str(tokNo))
            exit(1)


        # check for another statement (if, while, id, read, write)  
        if tokNo in [5, 8, 32, 10, 11]:
            self.ss = SS()
            self.ss.parseSS()
            

    def printSS(self):
        self.stmt.printStmt()

        if self.ss is not None:
            self.ss.printSS()

    def execSS(self):
        self.stmt.execStmt()
        if self.ss is not None:
            self.ss.execSS()


class Loop():
    c = None
    ss = None

    def parseLoop(self):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the while token
        if tokNo != 8:
            print("Error: Expected while, got " + str(tokNo))
            exit(1)

        t.skipToken()
        
        # parse the condition of the loop
        self.c = Cond()
        self.c.parseCond()

        # error check for the loop token
        tokNo = t.getToken()
        if tokNo != 9:
            print("Error: Expected loop, got " + str(tokNo))
            exit(1)
        
        t.skipToken()

        # parse the statement sequence of the loop
        self.ss = SS()
        self.ss.parseSS()

        # error check for the end token
        tokNo = t.getToken()
        if tokNo != 3:
            print("Error: Expected end, got " + str(tokNo))
            exit(1)
        
        t.skipToken()


        # error check for the semicolon token
        tokNo = t.getToken()
        if tokNo != 12:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)

        t.skipToken()
        
    
    def printLoop(self):
        print("\nwhile ", end="")
        self.c.printCond()
        print(" loop {\n", end="")
        self.ss.printSS()
        print("}\nend;\n", end="")


    def execLoop(self):
        while self.c.evalCond():
            self.ss.execSS()


class If():
    _c= None
    _ss1 = None
    _ss2 = None
    
    def parseIf(self):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the if token
        if tokNo != 5:
            print("Error: Expected if, got " + str(tokNo))
            exit(1)
        
        tokNo = t.skipToken()

        # parse the if statement's condition
        self._c = Cond()
        self._c.parseCond()

        # error check for the then token
        tokNo = t.getToken()
        if tokNo != 6:
            print("Error: Expected then, got " + str(tokNo))
            exit(1)
        t.skipToken()

        # parse the if statement's first statement sequence
        self._ss1 = SS()
        self._ss1.parseSS()

        # check for the else token
        tokNo = t.getToken()
        if tokNo == 3:
            ## no else, contains "end;"
            t.skipToken()

            # check for the semicolon token
            tokNo = t.getToken()
            if tokNo != 12:
                print("Error: Expected ;, got " + str(tokNo))
                exit(1)

            t.skipToken()
            return
        elif tokNo != 7:
            # else error checking
            print("Error: Expected else, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the if statement's second statement sequence
        self._ss2 = SS()
        self._ss2.parseSS()

        # error check for the end token
        tokNo = t.getToken()
        if tokNo != 3:
            print("Error: Expected end, got " + str(tokNo))
            exit(1)
        else:
            t.skipToken()

            # error check for the semicolon token
            tokNo = t.getToken()
            if tokNo != 12:
                print("Error: Expected ;, got " + str(tokNo))
                exit(1)

            t.skipToken()
            return


    def printIf(self):
        print("if ", end="")
        self._c.printCond()
        print(" then {\n", end="")
        self._ss1.printSS()
        print("}\n", end="")

        # if ss2 is null from parsing, we know there is no else 
        if self._ss2 is not None:
            print("else {\n", end="")
            self._ss2.printSS()
            print("\n}\n", end="")
        
        print("end;\n", end="")


    def execIf(self):
        # if ss2 is not null from parsing, we can account for an else stmt, otherwise only account for if stmt
        if self._c.evalCond():
            self._ss1.execSS()
        elif self._ss2 is not None:
            self._ss2.execSS()


class Id():
    _name: str = None
    _val: int = None
    _declared: bool = None
    _initialized: bool = None

    eIds = {}
    idCount = 0

    def __init__(self, n: str):
        self._name = n
        self._declared = True
        self._initialized = False


    # this is for DS
    @classmethod
    def parseId1(cls):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the id token
        if tokNo != 32:
            print("Error: Expected id, got " + str(tokNo))
            exit(1)
        
        name: str = t.idName()

        t.skipToken()

        # check if the id is already in the dictionary
        if name in cls.eIds:
            # if it is, exit the program
            print("Error: Id already exists")
            exit(1)

        declaredId = Id(name)
        cls.eIds[name] = declaredId
        cls.idCount += 1

        return declaredId

    # This is for SS
    @classmethod
    def parseId2(cls):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the id token
        if tokNo != 32:
            print("Error: Expected id, got " + str(tokNo))
            exit(1)

        name: str = t.idName()
        t.skipToken()

        # check if the id is already in the dictionary
        if name not in Id.eIds:
            # if not, exit the program
            print("Error: Id does not exist")
            exit(1)
        
        return cls.eIds[name]

    def getIdVal(self) -> int:
        # val initialized check
        if not self._initialized:
            print("Error: Id has no value")
            exit(1)
        
        return self._val
    
    def setIdVal(self, v: int):
        #check if declared is true
        if not self._declared:
            print("Error: Id is not declared")
            exit(1)
        
        self._val = v
        self._initialized = True

    def printId(self):
        # make sure Id is declared
        if not self._declared:
            print("Error: Id is not declared")
            exit(1)

        print(self._name, end="")

    def readId(self):
        # make sure Id is declared
        if not self._declared:
            print("Error: Id is not declared")
            exit(1)

        val: str = ""

        # TODO: fix the recursion of this function being called. It is being called even though inputList is empty

        if len(val) <= 0:
            print("Error: Input file is empty")
            exit(1)

        #try catch casting val to int and setting to Id's value
        try:
            self._val = int(val)
        except ValueError:
            print("Error: Expected int, got " + val)
            exit(1)
        
        # set initialized to true
        self._initialized = True


class Cond():
    _c1 = None
    _c2 = None
    type: int = None

    def parseCond(self):
        tokNo: int = None
        tokNo = t.getToken()

        # error chceck for (, [, or !
        if tokNo not in [15, 16, 20]:
            print("Error: Expected (, [, or !, got " + str(tokNo))
            exit(1)
        
        # handle ( token
        if tokNo == 20:
            self.type = 1
            self._c1 = Comp()
            self._c1.parseComp()
            
        # handle ! token    
        elif tokNo == 15:
            t.skipToken()
            self.type = 2
            self._c1 = Cond()
            self._c1.parseCond()
        
        # handle [ token
        elif tokNo == 16:
            t.skipToken()
    
            self._c1 = Cond()
            self._c1.parseCond()
            
            # check for && or || operators
            tokNo = t.getToken()
            if tokNo not in [18, 19]:
                print("Error: Expected && or ||, got " + str(tokNo))
                exit(1)
            
            # set the type of the Cond
            if tokNo == 18:
                self.type = 3
            elif tokNo == 19:
                self.type = 4
            t.skipToken()

            # parse the second condition
            self._c2 = Cond()
            self._c2.parseCond()

            # error check for ] token
            tokNo = t.getToken()
            if tokNo != 17:
                print("Error: Expected ], got " + str(tokNo))
                exit(1)

            t.skipToken()

    def printCond(self):
        if self.type == 1:
            self._c1.printComp()
        elif self.type == 2:
            print("!", end="")
            self._c1.printCond()
        elif self.type == 3:
            print("[", end="")
            self._c1.printCond()
            print(" && ", end="")
            self._c2.printCond()
            print("]", end="")
        elif self.type == 4:
            print("[", end="")
            self._c1.printCond()
            print(" || ", end="")
            self._c2.printCond()
            print("]", end="")
    
    def evalCond(self) -> bool:
        if(self.type == 1):
            return self._c1.evalComp()
        elif(self.type == 2):
            return not self._c1.evalCond()
        elif(self.type == 3):
            return self._c1.evalCond() and self._c2.evalCond()
        elif(self.type == 4):
            return self._c1.evalCond() or self._c2.evalCond()
            

class IdList():
    _id: Id = None
    _idList = None

    def parseIdList(self, isDeclared):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the id token
        if tokNo != 32:
            print("Error: Expected id, got " + str(tokNo))
            exit(1)

        # different parsing if boolean already exists in IdList
        if isDeclared:
            self._id = Id.parseId1()
        else:
            self._id = Id.parseId2()

        tokNo = t.getToken()

        if tokNo not in [12, 13]:
            print("Error: Expected , or ;, got " + str(tokNo))
            exit(1)
        

        # check if the comma token or semi colon is next (semicolon indicates end of parsing the IdList)
        if tokNo == 13:
            t.skipToken()
            self._idList = IdList()
            self._idList.parseIdList(isDeclared)
        elif tokNo == 12:
            return


    def printIdList(self):
        self._id.printId()
        if self._idList is not None:
            print(", ", end="")
            self._idList.printIdList()
        

    def writeIdList(self):
        self._id.printId()
        print(" = ")
        print(str(self._id.getIdVal())+ "\n", end="")
        if self._idList is not None:
            self._idList.writeIdList()


    def readIdList(self):
        self._id.readId()
        if self._idList is not None:
            self._idList.readIdList()        


class DS():
    _decl = None
    _ds = None

    def parseDS(self):
        self._decl = Decl()
        self._decl.parseDecl()

        tokNo: int = None
        tokNo = t.getToken()

        # error check for int or begin token
        if tokNo not in [4, 2]:
            print("Error: Expected int or begin, got " + str(tokNo))
            exit(1)

        if tokNo == 4:
            self._ds = DS()
            self._ds.parseDS()


    def printDS(self):
        self._decl.printDecl()
        if self._ds is not None:
            self._ds.printDS()
        

class Decl():
    _idList = None

    def parseDecl(self):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the int token
        if tokNo != 4:
            print("Error: Expected int, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the id list
        self._idList = IdList()
        self._idList.parseIdList(True)

        tokNo = t.getToken()

        # error check for the semicolon token
        if tokNo != 12:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)

        t.skipToken()

    def printDecl(self):
        print(" int ", end="")
        self._idList.printIdList()
        print(";\n")

class Exp():

    fac = None
    exp = None
    type: int = None

    def parseExp(self):
        self.fac = Fac()
        self.fac.parseFac()

        tokNo: int = None
        tokNo = t.getToken()

        if tokNo not in [22, 23]:
            self.type = 1
            return
        
        if tokNo == 22:
            self.type = 2
        elif tokNo == 23:
            self.type = 3

        t.skipToken()

        self.exp = Exp()
        self.exp.parseExp()


    def printExp(self):
        self.fac.printFac()
        if self.type == 2:
            print(" + ")
            self.exp.printExp()
        elif self.type == 3:
            print(" - ")
            self.exp.printExp()


    def evalExp(self) -> int:
        if self.type == 1:
            return self.fac.evalFac()
        elif self.type == 2:
            return self.fac.evalFac() + self.fac.evalExp()
        elif self.type == 3:
            return self.fac.evalFac() - self.fac.evalExp()



class SumExp(Exp):
    _e1: Exp
    _e2: Exp

    def init(self, e: Exp, f:Exp):
        self._e1 = e
        self._e2 = f

    def evalExp(self) -> int:
        return self._e1.evalExp() + self._e2.evalExp()

    
    def printExp():
        pass



class Op():
    _intVal = None
    _id = None
    _exp = None 

    def parseOp(self):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for id, int, or (
        if tokNo not in [31, 32, 20]:
            print("Error: Expected int, id, or (, got " + str(tokNo))
            exit(1)

        if tokNo == 31:
            self._intVal = t.intVal()
            t.skipToken()

        elif tokNo == 32:
            self._id = Id.parseId2()

        elif tokNo == 20:
            t.skipToken()
            self._exp = Exp()
            self._exp.parseExp()
            tokNo = t.getToken()
            if tokNo != 21:
                print("Error: Expected ), got " + str(tokNo))
                exit(1)
            t.skipToken()

    def printOp(self):
        if self._intVal is not None:
            print(self._intVal, end="")
        elif self._id is not None:
            self._id.printId()
        elif self._exp is not None:
            print("(", end="")
            self._exp.printExp()
            print(")", end="")

    def evalOp(self) -> int:
        if self._intVal is not None:
            return self._intVal
        elif self._id is not None:
            return self._id.getIdVal()
        elif self._exp is not None:
            return self._exp.evalExp()

class Fac():
    op = None
    fac = None

    def parseFac(self):
        self.op = Op()
        self.op.parseOp()

        tokNo: int = None
        tokNo = t.getToken()

        if tokNo ==  24:
            t.skipToken()
            self.fac = Fac()
            self.fac.parseFac()


    def printFac(self):
        self.op.printOp()
        if self.fac is not None:
            print(" * ", end="")
            self.fac.printFac()


    def evalFac(self) -> int:
        if self.fac is None:
            return self.op.evalOp()
        else:
            return self.op.evalOp() * self.fac.evalFac()
        

class Comp():
    op1 = None
    op2 = None
    compOp = None

    def parseComp(self):
        tokNo: int = None
        tokNo = t.getToken()

        if tokNo != 20:
            print("Error: Expected (, got " + str(tokNo))
            exit(1)

        t.skipToken()

        self.op1 = Op()
        self.op1.parseOp()

        self.compOp = CompOp()
        self.compOp.parseCompOp()

        self.op2 = Op()
        self.op2.parseOp()

        tokNo = t.getToken()
        if tokNo != 21:
            print("Error: Expected ), got " + str(tokNo))
            exit(1)

        t.skipToken()


    def printComp(self):
        print("(", end="")
        self.op1.printOp()
        print(" ", end="")
        self.compOp.printCompOp()
        print(" ", end="")
        self.op2.printOp()
        print(")", end="")


    def evalComp(self) -> bool:
        op1 = self.op1.evalOp()
        op2 = self.op2.evalOp()
        compOp = self.compOp._type

        if compOp == 1:
            return op1 != op2
        elif compOp == 2:
            return op1 == op2
        elif compOp == 3:
            return op1 < op2
        elif compOp == 4:
            return op1 > op2
        elif compOp == 5:
            return op1 <= op2
        elif compOp == 6:
            return op1 >= op2
        
        

class CompOp():
    _type: int = None

    def parseCompOp(self):
        tokNo: int = None
        tokNo = t.getToken()

        if tokNo not in [25, 26, 27, 28, 29, 30]:
            print("Error: Expected !=, ==, <, >, <=, or >=, got " + str(tokNo))
            exit(1)

        t.skipToken()
        self._type = tokNo - 24

    def printCompOp(self):
        if self._type == 1:
            print("!=", end="")
        elif self._type == 2:
            print("==", end="")
        elif self._type == 3:
            print("<", end="")
        elif self._type == 4:
            print(">", end="")
        elif self._type == 5:
            print("<=", end="")
        elif self._type == 6:
            print(">=", end="")



class Input():

    _idList = None

    def parseInput(self):
        tokNo = None
        tokNo = t.getToken()

        # error check for the input token
        if tokNo != 10:
            print("Error: Expected read, got " + str(tokNo))
            exit(1)

        t.skipToken()

        self._idList = IdList()
        self._idList.parseIdList(False)

        tokNo = t.getToken()

        # error check for the semicolon token
        if tokNo != 12:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)

        t.skipToken()

    def printInput(self):
        print("read ", end="")
        self._idList.printIdList()
        print(";\n", end="")

    def execInput(self):
        self._idList.readIdList()


class Output():
    _idList = None

    def parseOutput(self):
        tokNo = None
        tokNo = t.getToken()

        # error check for the output token
        if tokNo != 11:
            print("Error: Expected write, got " + str(tokNo))
            exit(1)

        t.skipToken()

        self._idList = IdList()
        self._idList.parseIdList(False)

        tokNo = t.getToken()

        # error check for the semicolon token
        if tokNo != 12:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)

        t.skipToken()


    def printOutput(self):
        print("write ", end="")
        self._idList.printIdList()
        print(";\n", end="")


    def execOutput(self):
        self._idList.writeIdList()







    
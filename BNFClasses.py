import CoreScanner
from abc import abstractmethod


def initTokenizer(progFile, inputFile):
    global t, input
    t = CoreScanner(progFile)
    input = open(inputFile)


# program non-terminal class
class Prog():
    _ds = None
    _ss = None

    def parseProg(self):
        
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the program token
        if tokNo != 1:
            print("Error: Expected program, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the program's declaration sequence
        self._ds = DS(t)
        self._ds.parseDS()

        # error check for the begin token
        tokNo = t.getToken()
        if tokNo != 2:
            print("Error: Expected begin, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the program's statement sequence
        self._ss = SS(t)
        self._ss.parseSS()

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
        print("program")
        self._ds.printDS()
        print("begin")
        self._ss.printSS()
        print("end")
    
    def execProg(self):
        self._ds.execDS()
        self._ss.execSS()


class Assign():
    _id= None
    _exp = None

    def parseAssign(self):
        tokNo: int = None
        _id = Id.parseId2()

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
        if tokNo != 4:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)

        t.skipToken()

    
    def printAssign(self):
        self._id.printId()
        print(" = ")
        self._exp.printExp()
        print(";")

    def execAssign(self):
        self._id.setIdVal(self._exp.evalExp())


class Stmt():
    _altNo: int = 0
    # Assign
    _s1 = None
    # If
    _s2 = None
    # Loop
    _s3 = None
    # Input
    _s4 = None
    # Output
    _s5 = None

    def parseStmt(self, t: CoreScanner):
        tokNo: int = t.getToken()

        # check for assignment
        if tokNo == 32:
            self._s1 = Assign()
            self._s1.parseAssign(t)
            self._altNo = 1
        # check for if
        elif tokNo == 5:
            self._s2 = If()
            self._s2.parseIf(t)
            self._altNo = 2
        # check for loop
        elif tokNo == 7:
            self._s3 = Loop()
            self._s3.parseLoop(t)
            self._altNo = 3
        # check for input
        elif tokNo == 10:
            self._s4 = Input()
            self._s4.parseInput(t)
            self._altNo = 4
        # check for output
        elif tokNo == 11:
            self._s5 = Output()
            self._s5.parseOutput(t)
            self._altNo = 5
        else:
            print("Invalid token in Stmt")
            exit(1)
        

    def printStmt(self):
        if self._altNo == 1:
            self._s1.printAssign()
        elif self._altNo == 2:
            self._s2.printIf()
        elif self._altNo == 3:
            self._s3.printLoop()
        elif self._altNo == 4:
            self._s4.printInput()
        elif self._altNo == 5:
            self._s5.printOutput()


    def execStmt(self):
        if self._altNo == 1:
            self._s1.execAssign()
        elif self._altNo == 2:
            self._s2.execIf()
        elif self._altNo == 3:
            self._s3.execLoop()
        elif self._altNo == 4:
            self._s4.execInput()
        elif self._altNo == 5:
            self._s5.execOutput()

class SS():
    pass


class Loop():
    _c = None
    _ss1 = None

    def parseLoop(self, t: CoreScanner):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the while token
        if tokNo != 8:
            print("Error: Expected while, got " + str(tokNo))
            exit(1)

        t.skipToken()
        
        # parse the condition of the loop
        self._c = Cond(t)
        self._c.parseCond()

        # error check for the loop token
        tokNo = t.getToken()
        if tokNo != 9:
            print("Error: Expected loop, got " + str(tokNo))
            exit(1)
        
        t.skipToken()

        # parse the statement sequence of the loop
        self._ss1 = SS(t)
        self._ss1.parseSS()

        # error check for the end token
        tokNo = t.getToken()
        if tokNo != 3:
            print("Error: Expected end, got " + str(tokNo))
            exit(1)
        else:
            t.skipToken()
            t.skipToken()
            return
        
    
    def printLoop(self):
        print("while ")
        self._c.printCond()
        print(" loop")
        self._ss1.printSS()
        print("end;")


    def execLoop(self):
        while self._c.execCond():
            self._ss1.execSS()


class If():
    _c= None
    _ss1 = None
    _ss2 = None
    
    def parseIf(self, t: CoreScanner):
        tokNo: int = None
        tokNo = t.getToken()

        # error check for the if token
        if tokNo != 5:
            print("Error: Expected if, got " + str(tokNo))
            exit(1)
        
        tokNo = t.skipToken()

        # parse the if statement's condition
        self._c = Cond(t)
        self._c.parseCond()

        # error check for the then token
        tokNo = t.getToken()
        if tokNo != 6:
            print("Error: Expected then, got " + str(tokNo))
            exit(1)
        t.skipToken()

        # parse the if statement's first statement sequence
        self._ss1 = SS(t)
        self._ss1.parseSS()
        tokNo = t.getToken()
        if tokNo == 3:
            ## no else, contains "end;"
            t.skipToken()
            t.skipToken()
            return
        elif tokNo != 7:
            # else error checking
            print("Error: Expected else, got " + str(tokNo))
            exit(1)

        t.skipToken()

        # parse the if statement's second statement sequence
        self._ss2 = SS(t)
        self._ss2.parseSS()

        # error check for the end token
        tokNo = t.getToken()
        if tokNo != 3:
            print("Error: Expected end, got " + str(tokNo))
            exit(1)
        else:
            t.skipToken()
            t.skipToken()
            return


    def printIf(self):
        print("if ")
        self._c.printCond()
        print(" then")
        self._ss1.printSS()

        # if ss2 is null from parsing, we know there is no else 
        if self._ss2 is None:
            print("end;")
        else:
            print("else")
            self._ss2.printSS()
            print("end;")


    def execIf(self):
        # if ss2 is not null from parsing, we can account for an else stmt, otherwise only account for if stmt
        if self._ss2 is not None:
            if self._c.execCond():
                self._ss1.execSS()
            else:
                self._ss2.execSS()
        else:  
            if self._c.execCond():
                self._ss1.execSS()


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

        name: str = t.idName()

        # error check for the id token
        if tokNo != 32:
            print("Error: Expected id, got " + str(tokNo))
            exit(1)

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
        if self._val is None:
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

        print(self._name)

    def readId(self):
        # make sure Id is declared
        if not self._declared:
            print("Error: Id is not declared")
            exit(1)

        # read the input file
        readVal = input.readline()

        # check if the line is empty
        if readVal == "":
            print("Error: Input file is empty")
            exit(1)

        # check if the line is a number
        if not readVal.isdigit():
            print("Error: Input file is not a number")
            exit(1)

        # set the Id's value to the input
        self._val = int(readVal)
        self._initialized = True









class Cond():

    _c1 = None

    def parseCond(self):
        tokNo: int = None
        tokNo = t.getToken()

        # error chceck for (, [, or !
        if tokNo not in [15, 16, 17]:
            print("Error: Expected (, [, or !, got " + str(tokNo))
            exit(1)
        
        # handle ( token
        if tokNo == 20:
            t.skipToken()
            self._c1 = Comp()
            self._c1.parseComp()
            
        # handle ! token    
        elif tokNo == 15:
            t.skipToken()
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


        

        


    def printCond():
        pass

    def evalCond():
        pass



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

        # check if the comma token or semi colon is next (semicolon indicates end of parsing the IdList)
        if tokNo == 13:
            t.skipToken()
            self._idList = IdList()
            self._idList.parseIdList(isDeclared)
        elif tokNo == 12:
            return
        else:
            print("Error: Expected , or ;, got " + str(tokNo))
            exit(1)

    def printIdList(self):
        self._id.printId()
        if self._idList is not None:
            print(", ")
            self._idList.printIdList()
        else:
            # only 1 variable declared, no commas are in the DS
            return
        

    def writeIdList(self):
        self._id.printId()



        

class DS():
    _idList: IdList()

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

        # error check for the semicolon token
        tokNo = t.getToken()
        if tokNo != 12:
            print("Error: Expected ;, got " + str(tokNo))
            exit(1)
        
        t.skipToken()

    
    def printDecl(self):
        print("int ")
        self._idList.printIdList()
        print(";")
            

    

class Decl():
    pass

class Exp():

    @abstractmethod
    def parseExp(self):
        pass


    pass
    

class IntExp(Exp):
    _i: int = None
    
    def __init(self, j: int):
        self._i = j

    def evalExp(self) -> int:
        return self._i
    

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
    pass

class Fac():
    pass

class Comp():
    pass

class Input():
    def parseInput(self):
        tokNo = None
        tokNo = t.getToken()

        # error check for the input token
        if tokNo != 10:
            print("Error: Expected read, got " + str(tokNo))
            exit(1)

        t.skipToken()







    
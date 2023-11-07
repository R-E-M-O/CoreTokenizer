from bnf import Cond, SS
import CoreScanner

class If():
    _c: Cond = None
    _ss1: SS = None
    _ss2: SS = None
    
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



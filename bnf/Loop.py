from bnf import Cond
from bnf import SS
import CoreScanner


class Loop():
    _c: Cond = None
    _ss1: SS = None

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


from bnf import DS
from bnf import SS
import CoreScanner


class Prog():
    _ds: DS = None
    _ss: SS = None

    def parseProg(self, t: CoreScanner):
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



    
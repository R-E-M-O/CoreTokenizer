from bnf import Assign
from bnf import If
from bnf import Loop
from bnf import Input
from bnf import Output
import CoreScanner


class Stmt():
    _altNo: int = 0
    _s1: Assign = None
    _s2: If = None
    _s3: Loop = None
    _s4: Input = None
    _s5: Output = None

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



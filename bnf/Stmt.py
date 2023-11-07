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
        

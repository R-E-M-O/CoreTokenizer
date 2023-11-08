from bnf import Id, Exp
import CoreScanner

class Assign():
    _id: Id = None
    _exp: Exp = None

    def parseAssign(self, t: CoreScanner):
        # _id will be assigned the result of the Id class's static parseId() method
        self._id = Id
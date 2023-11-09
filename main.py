import sys
from BNFClasses import Prog
from BNFClasses import initTokenizer


def main(progFile, inputFile):

    initTokenizer(progFile, inputFile)

    prog = Prog()

    prog.parseProg()

    print("\n\n\n")
    print("Program:\n")
    prog.printProg()
    print("\n\n\n")

    
    print("\n\n\n")
    print("Program Output:\n")
    prog.execProg()
    print("\n\n\n")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
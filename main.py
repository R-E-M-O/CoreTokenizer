import sys
from CoreScanner import CoreScanner

def main(fileName):
    scanner = CoreScanner(fileName)
    parser = Parser()
    
    output_Number : int = None

    while (output_Number != 33) and (output_Number != 34):
        output_Number = scanner.getToken()
        print(output_Number)
        scanner.skipToken()
    




if __name__ == "__main__":
    main(sys.argv[1])
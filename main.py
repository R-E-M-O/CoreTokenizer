import sys
from CoreScanner import CoreScanner


def main(fileName):

    # initiate object
    scanner = CoreScanner(fileName)

    # get first token
    output_Number : int = None

    # loop through tokens
    while (output_Number != 33) and (output_Number != 34):
        output_Number = scanner.getToken()
        print(output_Number)
        scanner.skipToken()
    

if __name__ == "__main__":
    main(sys.argv[1])
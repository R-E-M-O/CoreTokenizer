



class Tokenizer():
    _program_tokens = []
    _program_tokens_counter = 0
    _parse_tree_counter = 0
    
    #private buffered reader
    _reader = None



    def __init__(self, fileName):
        # instantiate reader
        self._reader = open(fileName, "r")
        # tokenize
        self._tokenizeLine()

    def _tokenizeLine(self):
        line = self._reader.readline()
        while str.isspace(line):
            line = self._reader.readline()

        # tokenize line
        tokens = line.split()
        for token in tokens:
            # Once first iteration is working, come back here and add code to account for greedy tokenizing!
            # Will need: (counter of 2) or (until whitespace) if certain symbols are in the token. 
            token_and_number = (token,)
            token_and_number[1] = self.getToken(token_and_number[0])
        

        pass
        

    def getToken(token) -> int: 
        match token:
            # dont forget to add cases for all legal tokens. Reference the DFA homework!
            case "program":
                pass
            case "begin":
                pass
            case "end":
                pass
            case "int":
                pass
            case "if":
                pass
            case "then":
                pass
            case "else":
                pass
            case "while":
                pass
            case "loop":
                pass
            case "read":
                pass
            case "write":
                pass
            case ";"
                pass
            case ",":
                pass
            case "=":
                # here you will need to utilize greedy tokenizing
                pass
            case "!":
                # check if "=" folows. if true, need to use greedy tokenizing
                pass
            case "[":
                pass
            case "]":
                pass
            case "&&":
                pass
            case "||":
                pass
            case "(":
                # Time for recursive descent parsing!
                pass
            case "+":
                pass
            case "-":
                pass
            case "*":
                pass
            case "<":
                # check if "=" folows. if true, need to use greedy tokenizing
                pass
            case ">":
                # check if "=" folows. if true, need to use greedy tokenizing
                pass
            case _:
                return 34

    def skipToken():
        pass

    def intVal() -> int:
        pass

    def idName() -> str:
        pass
    
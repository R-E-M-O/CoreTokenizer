



class Tokenizer():
    # legal Core tokens
    _program_tokens = []

    #tokens that are scanned from the reader, not in cores proper manner (may contain "!=<==")
    _read_tokens = []

    # corresponding Core token numbers
    _program_token_numbers = []

    _program_tokens_index = 0
    _parse_tree_index = 0
    
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
        self._read_tokens = line.split()
        for token in self._read_tokens:
            tokenIndex = self._read_tokens.index(token)

            # Once first iteration is working, come back here and add code to account for greedy tokenizing!
            # Will need: (counter of 2) or (until whitespace) if certain symbols are in the token. 
            self._program_token_numbers.extend(self.getToken(token))

        pass


    def getToken(self, token) -> int: 
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
            case ";":
                pass
            case ",":
                pass
            case "=":
                # here you will need to utilize greedy tokenizing
                nextToken = self.tokenLookAhead()

                if nextToken == "=":
                    # greedy tokenizing
                    pass
                pass
            case "!":
                # check if "=" folows. if true, need to use greedy tokenizing
                nextToken = self.tokenLookAhead()
                if nextToken == "=":
                    # greedy tokenizing
                    pass
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
                nextToken = self.tokenLookAhead()
                if nextToken == "=":
                    # greedy tokenizing
                    pass
                pass
            case ">":
                # check if "=" folows. if true, need to use greedy tokenizing
                nextToken = self.tokenLookAhead()
                if nextToken == "=":
                    # greedy tokenizing
                    pass
                pass
            case _:
                return 34

    # token lookahead
    def tokenLookAhead(self) -> str:
        pass

    def skipToken(self):
        self._program_tokens_index += 1

    def intVal() -> int:
        pass

    def idName() -> str:
        pass
    
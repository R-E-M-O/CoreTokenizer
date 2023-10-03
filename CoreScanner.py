class CoreScanner():

    _core_keywords = {
        "program" : 1,
        "begin" : 2,
        "end" : 3,
        "int" : 4,
        "if" : 5,
        "then" : 6,
        "else" : 7,
        "while" : 8,
        "loop" : 9,
        "read" : 10,
        "write" : 11
    }

    _core_symbols = {
        ";" : 12,
        "," : 13,
        "=" : 14,
        "!" : 15,
        "[" : 16,
        "]" : 17,
        "&&" : 18,
        "||" : 19,
        "(" : 20,
        ")" : 21,
        "+" : 22,
        "-" : 23,
        "*" : 24,
        "!=" : 25,
        "==" : 26,
        "<" : 27,
        ">" : 28,
        "<=" : 29,
        ">=" : 30
    }


    def __init__(self, fileName):
        self._reader = open(fileName, "r")
        self._program_tokens = []
        self._token_cursor = 0

        # tokenize
        self._tokenizeLine()


    def _tokenizeLine(self):
        line = self._reader.readline()

        # add a space before and after each special symbol. better for reading
        for symbol in self._core_symbols:
            line = line.replace(symbol, " " + symbol + " ")

        # tokenize line
        lineTokens = line.split()

        i = 0
        while i < len(lineTokens):
            token = lineTokens[i]
            next_token = None
            if i+1 < len(lineTokens):
                next_token = lineTokens[i+1]

            # check if token is "!"
            if token in  ["!", "=", "<", ">"] and next_token == "=":
                # add the = to the element to the last program_tokens element
                token += next_token                      
                # pop the 2nd token off
                lineTokens.pop(i+1)

        
            # check if token is "&" or "|"
            elif token in ["&", "|"] and token == next_token:
                # append the token
                token += next_token                      
                # pop the 2nd token off
                lineTokens.pop(i+1)



            # append the token
            self._program_tokens.append(token)
            i += 1


    # returns an int corresponding to a keyword, integer, id, EOF, or error
    def getToken(self) -> int: 

        if self._token_cursor >= len(self._program_tokens):
            return 33

        token = self._program_tokens[self._token_cursor]

        if token in self._core_keywords:
            return self._core_keywords[token]
        # check if token is a symbol
        elif token in self._core_symbols:
            return self._core_symbols[token]
        # check if token is an integer
        elif token.isdigit():
            return 31
        # check if token is an id
        elif token[0].isupper() and all(c.isupper() or c.isdigit() for c in token):
            return 32
        # check if token is EOF
        elif token == None:
            return 33
        # token is an error
        else:
            return 34
            

    def skipToken(self):
        self._token_cursor += 1
        if self._token_cursor >= len(self._program_tokens):
            self._tokenizeLine()


    def intVal(self) -> int:
        return 31


    def idName(self) -> str:
        return self._program_tokens[self._token_cursor]
    
    
    def __del__(self):
        self._reader.close()


    
    
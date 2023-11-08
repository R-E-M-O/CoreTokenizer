class Id():
    name: str = None
    val: int = None
    declared: bool = None
    initialized: bool = None
    

    def __init__(self, n: str):
        self.name = n
        self.declared = False
        self.initialized = False

    



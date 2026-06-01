class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.user = None
        return cls._instance

    def login(self, user: dict):
        self.user = user

    def logout(self):
        self.user = None


session = Session()

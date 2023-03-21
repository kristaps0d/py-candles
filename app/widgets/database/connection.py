import sqlite3
from utils.environment import Environment

class DbConnection(Environment):

    def __init__(self, dbEnvKey):
        super().__init__()

        # private class variables
        self._dbUri = self.getenv(dbEnvKey)

    def Connect(self, dbUri):
        self.connection = sqlite3.connect(dbUri)
        return self.connection

    def Close(self): 
        return self.connection.close()

    def __enter__(self):
        return self.Connect(self._dbUri)

    def __exit__(self, type, value, traceback):
        return self.Close()
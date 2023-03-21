from ..table import Table

class Console(Table):

    def __init__(self, cursor):
        
        # private class variables
        _table = "console"
        _schema = """(
            id integer PRIMARY KEY,
            log text,
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""

        super().__init__(cursor, _table, _schema)

    def Insert(self, log:str):
        self._cursor.execute(f'INSERT INTO {self._table}(log) VALUES("{log}")')

    def InsertMany(self, logs):
        for log in logs:
            self._cursor.execute(f'INSERT INTO {self._table}(log) VALUES("{log}",)')
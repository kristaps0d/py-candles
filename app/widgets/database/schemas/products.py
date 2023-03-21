from ..table import Table

class Products(Table):

    def __init__(self, cursor):
        
        # private class variables
        _table = "products"
        _schema = """(
            id integer PRIMARY KEY,
            quality text NOT NULL,
            createdAt DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""

        super().__init__(cursor, _table, _schema)

    def Insert(self, quality:str):
        self._cursor.execute(f'INSERT INTO {self._table}(quality) VALUES("{quality}")')

    def InsertMany(self, queryId, universities):
        for uni in universities:
            self._cursor.execute(f'INSERT INTO {self._table}(quality) VALUES("{quality}",)')
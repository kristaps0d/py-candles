from utils.exceptions import ExceptionHandler

class Table(ExceptionHandler):

    def __init__(self, cursor, table, schema):
        super().__init__()

        # private class variables
        self._cursor = cursor
        self._table, self._schema = table, schema

        # select or create table
        self.TryExcept(self.SelectTable, self.CreateTable)

    def Select(self, column:str):
        return self._cursor.execute(f'SELECT {column} FROM {self._table}').fetchall()

    def SelectTable(self):
        return self.Select("*")

    def CreateTable(self):
        self._cursor.execute(f'CREATE TABLE {self._table}{self._schema}')
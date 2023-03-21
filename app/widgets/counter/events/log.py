from widgets.database.schemas.console import Console
from widgets.database.cursor import DbCursor

class LogEvent(object):
    def __new__(self, log, dbCon):
        # add new database entry
        with DbCursor(dbCon) as cur:
            ConsoleTable = Console(cur)
            ConsoleTable.Insert(log)
    
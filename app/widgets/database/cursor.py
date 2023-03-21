class DbCursor(object):
    def __init__(self, connection):
        
        # private class variables
        self._connection = connection

    def __enter__(self):
        return self._connection.cursor()

    def __exit__(self, type, value, traceback):
        self._connection.commit()
from PyQt5 import QtWidgets, uic
from widgets.database.connection import DbConnection

class RunGui(object):
    def __init__(self, App:callable, dbUri:str, src:any, args=[]):
        # app instance
        app = QtWidgets.QApplication(args)

        with DbConnection(dbUri) as con:
            ui = App(con, dbUri, src)
            app.exec_()
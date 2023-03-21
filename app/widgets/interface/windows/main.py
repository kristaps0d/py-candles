from PyQt5 import QtWidgets, QtCore, QtGui, uic
import multiprocessing, numpy as np

from widgets.counter import CounterModuleAsync

from widgets.database.cursor import DbCursor

from widgets.database.schemas.products import Products
from widgets.database.schemas.console import Console

class Main(QtWidgets.QMainWindow):
    def __init__(self, dbCon, dbUri, src):
        super().__init__()

        uic.loadUi('./app/assets/xml/main.xml', self)
        self.setWindowIcon(QtGui.QIcon('./app/assets/images/favicon.png'))

        self.setFixedSize(self.size())

        self._elements = {
            'buttons': {
                'ResetDefective': self.findChild(QtWidgets.QPushButton, "resetDefective"),
                'ResetGood': self.findChild(QtWidgets.QPushButton, "resetGood"),
                'ShowUnfiltered': self.findChild(QtWidgets.QPushButton, "unfilteredStreams"),
                'ShowFiltered': self.findChild(QtWidgets.QPushButton, "filteredStreams"),
                'ShowTracking': self.findChild(QtWidgets.QPushButton, "trackingStreams")
            }, 'checkboxes': {
                'EnableCounter': self.findChild(QtWidgets.QCheckBox, "enableCounter"),
            }, 'displays': {
                'DefectiveCounter': self.findChild(QtWidgets.QLCDNumber, "defectiveCount"),
                'GoodCounter': self.findChild(QtWidgets.QLCDNumber, "goodCount"),
                'Console': self.findChild(QtWidgets.QListWidget, 'console')
            }
        }

        # class variables
        self.counterThread = None

        # class private variables
        self._dbCon = dbCon
        self._thr_queue = multiprocessing.Queue()

        self.defectiveCount, self.goodCount = 0, 0
        self.good_min_key, self.defective_min_key = 0, 0

        self._src, self._dbUri = src, dbUri

        # Element events
        self._elements['buttons']['ResetDefective'].clicked.connect(self.ResetDefective)
        self._elements['buttons']['ResetGood'].clicked.connect(self.ResetGood)
        self._elements['checkboxes']['EnableCounter'].stateChanged.connect(self.checkBoxEnableCounterStateChange)

        self._elements['buttons']['ShowUnfiltered'].clicked.connect(self.EnableVisuals)
        self._elements['buttons']['ShowFiltered'].clicked.connect(self.EnableMask)
        self._elements['buttons']['ShowTracking'].clicked.connect(self.EnableMarkers)
        
        # app loop
        main_timer = QtCore.QTimer(self)
        main_timer.timeout.connect(self.updateValues)
        main_timer.start(200)

        secondary_timer = QtCore.QTimer(self)
        secondary_timer.timeout.connect(self.updateConsole)
        secondary_timer.start(3000)

        self.updateConsole()
        self.show()

    def EnableVisuals(self):
        self._thr_queue.put('visuals')
    
    def EnableMask(self):
        self._thr_queue.put('mask')

    def EnableMarkers(self):
        self._thr_queue.put('markers')

    def ResetDefective(self):
        # Get currently max db key
        with DbCursor(self._dbCon) as cur:
            ProductsTable = Products(cur)
            _res = ProductsTable.Select('id')
            _res = max(_res)[0]

            self.defectiveCount = 0
            self.defective_min_key = _res

            self.UpdateDisplays()
        
    def ResetGood(self):
        # Get currently max db key
        with DbCursor(self._dbCon) as cur:
            ProductsTable = Products(cur)
            _res = ProductsTable.Select('id')
            _res = max(_res)[0]

            self.goodCount = 0
            self.good_min_key = _res

            self.UpdateDisplays()

    def updateValues(self):
        with DbCursor(self._dbCon) as cur:
            ProductsTable = Products(cur)
            _col_id = ProductsTable.Select('id')
            _col_quality = ProductsTable.Select('quality')

            _defect, _good = 0, 0
            for i in range(len(_col_id)):

                if _col_id[i][0] > self.defective_min_key:
                    if _col_quality[i][0] == 'defective':
                        _defect += 1

                if _col_id[i][0] > self.good_min_key:
                    if _col_quality[i][0] == 'passed':
                        _good += 1

            self.defectiveCount = _defect
            self.goodCount = _good
            self.UpdateDisplays()


    def updateConsole(self):
        with DbCursor(self._dbCon) as cur:
            ConsoleTable = Console(cur)
            _res = ConsoleTable.Select('*')

            self._elements['displays']['Console'].clear()

            for i in np.flip(_res):
                (_id, _log, _date) = i
                self._elements['displays']['Console'].addItem(f'[{_date}]: {_log}')
                self._elements['displays']['Console'].repaint()
            

            
    def UpdateDisplays(self):
        self._elements['displays']['DefectiveCounter'].display(self.defectiveCount)
        self._elements['displays']['GoodCounter'].display(self.goodCount)

    def killCounterSubroutine(self):
        self.counterThread.terminate()
        self.counterThread.join()
        self.counterThread = None

    def startCounterSubroutine(self):
        self.counterThread = multiprocessing.Process(target=CounterModuleAsync, args=(self._thr_queue, self._src, self._dbUri))
        self.counterThread.start()

    def checkBoxEnableCounterStateChange(self, int):
        _state = self._elements['checkboxes']['EnableCounter'].isChecked()

        if _state is True:
            # start counter thread
            self.startCounterSubroutine()

        if _state is False:
            # kill counter thread
            self.killCounterSubroutine()

    def closeEvent(self, event):
        if self.counterThread is not None:
            self.killCounterSubroutine()

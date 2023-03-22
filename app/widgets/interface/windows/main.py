from PyQt5 import QtWidgets, QtCore, QtGui, uic
import multiprocessing, numpy as np
import hashlib

from widgets.counter import CounterModuleAsync

from widgets.database.cursor import DbCursor

from widgets.database.schemas.products import Products
from widgets.database.schemas.console import Console

from utils.environment import Environment

class Main(QtWidgets.QMainWindow):
    def __init__(self, dbCon, dbUri, src):
        super().__init__()

        self.envHandle = Environment()
        self.locked = True

        uic.loadUi('./app/assets/xml/main.xml', self)
        self.setWindowIcon(QtGui.QIcon('./app/assets/images/favicon.png'))

        self.setFixedSize(self.size())

        self._elements = {
            'buttons': {
                'ResetDefective': self.findChild(QtWidgets.QPushButton, "resetDefective"),
                'ResetGood': self.findChild(QtWidgets.QPushButton, "resetGood")
            }, 'checkboxes': {
                'EnableCounter': self.findChild(QtWidgets.QCheckBox, "enableCounter"),
                'VisualStream': self.findChild(QtWidgets.QCheckBox, "visualStream"),
                'MaskedStream': self.findChild(QtWidgets.QCheckBox, "maskedStream"),
                'TrackingStream': self.findChild(QtWidgets.QCheckBox, "trackingStream"),
                'authCheck': self.findChild(QtWidgets.QCheckBox, "authCheckbox")
            }, 'displays': {
                'DefectiveCounter': self.findChild(QtWidgets.QLCDNumber, "defectiveCount"),
                'GoodCounter': self.findChild(QtWidgets.QLCDNumber, "goodCount"),
                'Console': self.findChild(QtWidgets.QListWidget, 'console')
            }, 'inputs': {
                'authenticationInput': self.findChild(QtWidgets.QLineEdit, 'authInput')
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

        # cover password field
        self._elements['inputs']['authenticationInput'].setEchoMode(QtWidgets.QLineEdit.Password)

        # Element events
        self._elements['buttons']['ResetDefective'].clicked.connect(self.ResetDefective)
        self._elements['buttons']['ResetGood'].clicked.connect(self.ResetGood)
        self._elements['checkboxes']['EnableCounter'].stateChanged.connect(self.checkBoxEnableCounterStateChange)

        self._elements['checkboxes']['VisualStream'].stateChanged.connect(self.checkboxStateChangeVisuals)
        self._elements['checkboxes']['MaskedStream'].stateChanged.connect(self.checkboxStateChangeMask)
        self._elements['checkboxes']['TrackingStream'].stateChanged.connect(self.checkboxStateChangeMarkers)
        self._elements['checkboxes']['authCheck'].stateChanged.connect(self.checkboxStateChangeAuth)
        
        # simple reason for hashing
        # exam requires it, quite useless
        self.LockInterface()

        # app loop
        main_timer = QtCore.QTimer(self)
        main_timer.timeout.connect(self.updateValues)
        main_timer.start(200)

        secondary_timer = QtCore.QTimer(self)
        secondary_timer.timeout.connect(self.updateConsole)
        secondary_timer.start(3000)

        self.updateConsole()
        self.show()

    def checkboxStateChangeVisuals(self):
        self._thr_queue.put('visuals')
    
    def checkboxStateChangeMask(self):
        self._thr_queue.put('mask')

    def checkboxStateChangeMarkers(self):
        self._thr_queue.put('markers')

    def checkboxStateChangeAuth(self):
        _state = self._elements['checkboxes']['authCheck'].isChecked()

        if _state:
            # check auth key
            _plaintext = self._elements['inputs']['authenticationInput'].text()

            # hashing
            _cmp_hash = self.envHandle.getenv('userAuthHashSha256')
            _hash = hashlib.sha256(_plaintext.encode()).hexdigest()

            if (_hash != _cmp_hash) and (_cmp_hash != ''):
                return self.LockInterface()
            
            return self.UnlockInterface()

        self.LockInterface()

    def UnlockInterface(self):
        self.locked = False
        self._elements['buttons']['ResetDefective'].setEnabled(True)
        self._elements['buttons']['ResetGood'].setEnabled(True)
        self._elements['checkboxes']['EnableCounter'].setEnabled(True)
        self._elements['inputs']['authenticationInput'].setEnabled(False)

    def LockInterface(self):
        self.locked = True
        self._elements['buttons']['ResetDefective'].setEnabled(False)
        self._elements['buttons']['ResetGood'].setEnabled(False)
        self._elements['checkboxes']['EnableCounter'].setEnabled(False)
        self._elements['checkboxes']['VisualStream'].setChecked(False)
        self._elements['checkboxes']['MaskedStream'].setChecked(False)
        self._elements['checkboxes']['TrackingStream'].setChecked(False)
        self._elements['inputs']['authenticationInput'].setEnabled(True)
        
        self._elements['checkboxes']['VisualStream'].setEnabled(False)
        self._elements['checkboxes']['MaskedStream'].setEnabled(False)
        self._elements['checkboxes']['TrackingStream'].setEnabled(False)
        self._elements['checkboxes']['authCheck'].setChecked(False)
        self._elements['checkboxes']['EnableCounter'].setChecked(False)

        self.killCounterSubroutine()

    def ResetDefective(self):
        # Get currently max db key
        try:
            with DbCursor(self._dbCon) as cur:
                ProductsTable = Products(cur)
                _res = ProductsTable.Select('id')
                _res = max(_res)[0]

                self.defectiveCount = 0
                self.defective_min_key = _res

                self.UpdateDisplays()
        except:
            pass
        
    def ResetGood(self):
        # Get currently max db key
        try:
            with DbCursor(self._dbCon) as cur:
                ProductsTable = Products(cur)
                _res = ProductsTable.Select('id')
                _res = max(_res)[0]

                self.goodCount = 0
                self.good_min_key = _res

                self.UpdateDisplays()
        except:
            pass

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

            if (not self.locked):
                self.defectiveCount = _defect
                self.goodCount = _good
            else:
                self.defectiveCount = '-'
                self.goodCount = '-'

            self.UpdateDisplays()


    def updateConsole(self):
        with DbCursor(self._dbCon) as cur:
            ConsoleTable = Console(cur)
            _res = ConsoleTable.Select('*')

            self._elements['displays']['Console'].clear()

            if (self.locked):
                return

            for i in np.flip(_res):
                (_id, _log, _date) = i
                self._elements['displays']['Console'].addItem(f'[{_date}]: {_log}')
                self._elements['displays']['Console'].repaint()
            
    def UpdateDisplays(self):
        self._elements['displays']['DefectiveCounter'].display(self.defectiveCount)
        self._elements['displays']['GoodCounter'].display(self.goodCount)

    def killCounterSubroutine(self):
        self._elements['checkboxes']['VisualStream'].setChecked(False)
        self._elements['checkboxes']['MaskedStream'].setChecked(False)
        self._elements['checkboxes']['TrackingStream'].setChecked(False)

        self._elements['checkboxes']['VisualStream'].setEnabled(False)
        self._elements['checkboxes']['MaskedStream'].setEnabled(False)
        self._elements['checkboxes']['TrackingStream'].setEnabled(False)

        try:
            self.counterThread.terminate()
            self.counterThread.join()
            self.counterThread = None
        except:
            pass

    def startCounterSubroutine(self):
        self._elements['checkboxes']['VisualStream'].setEnabled(True)
        self._elements['checkboxes']['MaskedStream'].setEnabled(True)
        self._elements['checkboxes']['TrackingStream'].setEnabled(True)

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

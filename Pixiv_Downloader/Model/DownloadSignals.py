from PyQt6 import QtCore
from PyQt6.QtCore import QObject


class DownloadSignals(QObject):
  finished = QtCore.pyqtSignal()
  error = QtCore.pyqtSignal(tuple)
  result = QtCore.pyqtSignal(object)
  progress = QtCore.pyqtSignal(int)
  

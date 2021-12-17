import sys
from Widgets.Main import Main
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu, QMessageBox, QMainWindow, QApplication
from PyQt6.QtGui import QIcon, QAction


class PixivDownloader(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__()
    self.initUI()
    
  
  def initUI(self):
    main = Main()
    self.setCentralWidget(main)
    self.setCloseAct()
    self.setMenuBar()
  
    self.setGeometry(300, 300, 300, 300)
    self.setWindowTitle("Pixiv Downloader")
    self.show()
    
    
  def setMenuBar(self):
    menuBar = self.menuBar()
    pdMenu = menuBar.addMenu("Pixiv Downloader")
    closeAct = QAction('Close', self)
    closeAct.triggered.connect(QApplication.instance().quit)
    pdMenu.addAction(closeAct)
    
    
  def setCloseAct(self):
    self.exitAct = QAction(QIcon('exit.png'), '&Exit', self)
    self.exitAct.setShortcut('Ctrl+Q')
    self.exitAct.setStatusTip('Exit Pixiv Downloader')
    self.exitAct.triggered.connect(QApplication.instance().quit)
    
    
  def closeEvent(self, event):
    reply = QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
    
    if reply == QMessageBox.StandardButton.Yes:
      event.accept()
    else:
      event.ignore()
    

if __name__ == '__main__':
  app = QApplication(sys.argv)
  pd = PixivDownloader()
  sys.exit(app.exec())

import os
import sys
import subprocess
from Widgets.Main import Main
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu, QMessageBox, QMainWindow, QApplication
from PyQt6.QtGui import QIcon, QAction


class PixivDownloader(QMainWindow):
  def __init__(self, *args, **kwargs):
    super().__init__()
    self.initUI()
    
  
  def initUI(self):
    basePath = self.chooseDirectory()
    self.createDefaultDownloadFolder(basePath)
    main = Main(basePath)
    self.setCentralWidget(main)
    self.setCloseAct()
    self.setMenuBar()
  
    self.setGeometry(300, 300, 300, 300)
    self.setWindowTitle("Pixiv Downloader")
    self.setWindowIcon(QIcon(f'{basePath}/Resources/DefaultUserIcon.png'))
    self.show()
    
    
  def createDefaultDownloadFolder(self, basePath):
    self.downloadImagesFolderPath = os.path.join(basePath, 'Download Images')
    if not os.path.exists(self.downloadImagesFolderPath):
      os.makedirs(self.downloadImagesFolderPath)
        
    
    
  def chooseDirectory(self):
    if getattr(sys, 'frozen', False):
      return sys._MEIPASS
    return os.path.abspath('.')
    
    
  def setMenuBar(self):
    menuBar = self.menuBar()
    pdMenu = menuBar.addMenu("Pixiv Downloader")
    
    openFolderAct = QAction('Open Download Images Folder', self)
    openFolderAct.triggered.connect(self.setOpenFolderAct)
    
    closeAct = QAction('Close', self)
    closeAct.triggered.connect(QApplication.instance().quit)
    
    pdMenu.addAction(openFolderAct)
    pdMenu.addAction(closeAct)
    
    
  def setOpenFolderAct(self):
    subprocess.Popen(['open', self.downloadImagesFolderPath])
    
    
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


setup(
)
